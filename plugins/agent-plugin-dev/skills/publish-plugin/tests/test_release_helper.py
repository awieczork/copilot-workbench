"""Guard tests for the read-only, per-plugin release helper."""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/release.sh"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


class ReleaseHelperTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
        self.root.mkdir()
        self.environment = os.environ.copy()
        self.environment["GIT_CONFIG_NOSYSTEM"] = "1"
        self.environment["GIT_CONFIG_GLOBAL"] = os.devnull
        subprocess.run(
            ["git", "init", "--initial-branch", "main", str(self.root)],
            check=True,
            capture_output=True,
            env=self.environment,
        )
        self.git("config", "user.name", "Fixture User")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "core.hooksPath", os.devnull)
        self.git("config", "commit.gpgsign", "false")
        self.write_catalog([])

    def tearDown(self):
        self.temporary_directory.cleanup()

    def git(self, *arguments):
        return subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=True,
            capture_output=True,
            text=True,
            env=self.environment,
        )

    def write_catalog(self, entries):
        path = self.root / ".github/plugin/marketplace.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "name": "ds-tools",
                    "owner": {"name": "Test owner"},
                    "plugins": entries,
                }
            ),
            encoding="utf-8",
        )

    def write_plugin(self, name, version, note):
        package = self.root / "plugins" / name
        package.mkdir(parents=True, exist_ok=True)
        (package / "plugin.json").write_text(
            json.dumps({"$schema": SCHEMA, "name": name, "version": version}),
            encoding="utf-8",
        )
        (package / "CHANGELOG.md").write_text(
            f"# Changelog\n\n## [{version}] - 2026-10-27\n\n- {note}\n",
            encoding="utf-8",
        )
        return {"name": name, "source": f"./plugins/{name}"}

    def commit_fixture(self, track_origin_main=True):
        self.git("add", "--all")
        subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "-c",
                "core.hooksPath=" + os.devnull,
                "-c",
                "commit.gpgsign=false",
                "commit",
                "-m",
                "fixture state",
            ],
            check=True,
            capture_output=True,
            text=True,
            env=self.environment,
        )
        if track_origin_main:
            self.git("update-ref", "refs/remotes/origin/main", "HEAD")

    def invoke(self, *arguments):
        return subprocess.run(
            ["bash", str(SCRIPT), *arguments],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
        )

    def state(self):
        branch = self.git("branch", "--show-current").stdout.strip()
        head = subprocess.run(
            ["git", "-C", str(self.root), "rev-parse", "--verify", "HEAD"],
            capture_output=True,
            text=True,
            env=self.environment,
        )
        status = self.git("status", "--porcelain=v1", "--untracked-files=all").stdout
        tags = self.git("tag", "--list").stdout
        tracking_ref = subprocess.run(
            [
                "git",
                "-C",
                str(self.root),
                "rev-parse",
                "--verify",
                "refs/remotes/origin/main^{commit}",
            ],
            capture_output=True,
            text=True,
            env=self.environment,
        )
        return (
            branch,
            head.stdout.strip() if head.returncode == 0 else None,
            status,
            tags,
            tracking_ref.stdout.strip() if tracking_ref.returncode == 0 else None,
            self.git("ls-files", "--stage", "-z").stdout,
            self.git("remote", "-v").stdout,
            tuple((path.relative_to(self.root).as_posix(), path.read_bytes())
                  for path in sorted(self.root.rglob("*"))
                  if path.is_file() and ".git" not in path.relative_to(self.root).parts),
        )

    def test_strict_version_floor_includes_legacy_only_for_agent_team(self):
        self.write_catalog([self.write_plugin("agent-team", "0.1.3", "team note")])
        self.commit_fixture()
        self.git("tag", "v0.1.3")
        for version in ("0.1.3", "0.1.2", "0.2.0"):
            with self.subTest(version=version):
                if version != "0.1.3":
                    self.write_plugin("agent-team", version, "team note")
                    self.commit_fixture()
                before = self.state()
                result = self.invoke("preflight", "agent-team")
                self.assertEqual(result.returncode == 0, version == "0.2.0", result.stderr)
                if version != "0.2.0":
                    self.assertIn("strictly greater", result.stderr)
                self.assertEqual(self.state(), before)

    def test_unrelated_tags_do_not_raise_selected_package_floor(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        self.git("tag", "v99.0.0")
        self.git("tag", "plugin-two/v99.0.0")
        before = self.state()
        result = self.invoke("preflight", "plugin-one")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state(), before)
        self.git("tag", "plugin-one/v2.0.0")
        result = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("strictly greater", result.stderr)

    def test_used_namespaced_tag_refuses(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        self.git("tag", "plugin-one/v1.0.0")
        before = self.state()
        result = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists locally", result.stderr)
        self.assertEqual(self.state(), before)

    def test_unfinished_operation_refuses_on_clean_main(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        marker = self.root / ".git/CHERRY_PICK_HEAD"
        marker.write_text(self.git("rev-parse", "HEAD").stdout, encoding="utf-8")
        before = self.state()
        result = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unfinished Git operation", result.stderr)
        self.assertEqual(self.state(), before)
        self.assertTrue(marker.exists())

    def test_invalid_version_and_missing_notes_refuse(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0-rc.1", "one note")])
        self.commit_fixture()
        result = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("MAJOR.MINOR.PATCH", result.stderr)
        self.write_plugin("plugin-one", "1.0.0", "one note")
        (self.root / "plugins/plugin-one/CHANGELOG.md").write_text("# Changelog\n\n## Unreleased\n")
        self.commit_fixture()
        before = self.state()
        result = self.invoke("notes", "plugin-one")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("non-empty", result.stderr)
        self.assertEqual(self.state(), before)

    def test_ambiguous_catalog_selection_refuses(self):
        entry = self.write_plugin("plugin-one", "1.0.0", "one note")
        self.write_catalog([entry, entry])
        self.commit_fixture()
        result = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("more than once", result.stderr)

    def test_wrapper_runs_from_external_installation(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        installed = self.root.parent / "installed skill"
        shutil.copytree(SCRIPT.parent.parent, installed)
        before = self.state()
        result = subprocess.run(
            ["bash", str(installed / "scripts/release.sh"), "preflight", "plugin-one"],
            cwd=self.root, env=self.environment, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.state(), before)

    def test_missing_selection_refuses_without_mutation(self):
        before = self.state()

        result = self.invoke("preflight")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("select one plugin", result.stderr)
        self.assertEqual(self.state(), before)

    def test_empty_or_unlisted_catalog_selection_refuses(self):
        self.commit_fixture()
        before_empty = self.state()

        empty_result = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(empty_result.returncode, 0)
        self.assertIn("catalog is empty", empty_result.stderr)
        self.assertEqual(self.state(), before_empty)

        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        before_unlisted = self.state()
        unlisted_result = self.invoke("preflight", "plugin-two")
        self.assertNotEqual(unlisted_result.returncode, 0)
        self.assertIn("is not listed", unlisted_result.stderr)
        self.assertEqual(self.state(), before_unlisted)

    def test_wrong_branch_refuses_without_mutation(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        self.git("switch", "-c", "work/release")
        before = self.state()

        result = self.invoke("preflight", "plugin-one")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("current branch to be main", result.stderr)
        self.assertEqual(self.state(), before)

    def test_missing_commit_and_dirty_tree_refuse(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        before_no_commit = self.state()
        no_commit = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(no_commit.returncode, 0)
        self.assertIn("no committed state", no_commit.stderr)
        self.assertEqual(self.state(), before_no_commit)

        self.commit_fixture()
        (self.root / "plugins/plugin-one/CHANGELOG.md").write_text(
            "uncommitted change\n", encoding="utf-8"
        )
        before_dirty = self.state()
        dirty = self.invoke("preflight", "plugin-one")
        self.assertNotEqual(dirty.returncode, 0)
        self.assertIn("working tree is dirty", dirty.stderr)
        self.assertEqual(self.state(), before_dirty)

    def test_missing_origin_main_tracking_ref_refuses_without_mutation(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture(track_origin_main=False)
        before = self.state()

        result = self.invoke("preflight", "plugin-one")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("refs/remotes/origin/main", result.stderr)
        self.assertIn("missing", result.stderr)
        self.assertEqual(self.state(), before)

    def test_stale_origin_main_tracking_ref_refuses_without_mutation(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        (self.root / "README.md").write_text("local main commit\n", encoding="utf-8")
        self.commit_fixture(track_origin_main=False)
        before = self.state()

        result = self.invoke("preflight", "plugin-one")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("differs from cached refs/remotes/origin/main", result.stderr)
        self.assertEqual(self.state(), before)

    def test_matching_origin_main_tracking_ref_allows_preflight_without_mutation(self):
        self.write_catalog([self.write_plugin("plugin-one", "1.0.0", "one note")])
        self.commit_fixture()
        before = self.state()

        result = self.invoke("preflight", "plugin-one")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("local tag plugin-one/v1.0.0 is available", result.stdout)
        self.assertEqual(self.state(), before)

    def test_listed_package_directory_symlink_refuses_without_mutation(self):
        package = self.root / "plugins/real-plugin"
        package.mkdir(parents=True)
        (package / "plugin.json").write_text(
            json.dumps({"$schema": SCHEMA, "name": "alias-plugin", "version": "1.0.0"}),
            encoding="utf-8",
        )
        (package / "CHANGELOG.md").write_text(
            "# Changelog\n\n## [1.0.0] - 2026-10-27\n\n- note\n",
            encoding="utf-8",
        )
        alias = self.root / "plugins/alias-plugin"
        try:
            alias.symlink_to("real-plugin", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symbolic links are unavailable: {error}")
        self.write_catalog(
            [{"name": "alias-plugin", "source": "./plugins/alias-plugin"}]
        )
        self.commit_fixture()
        before = self.state()

        result = self.invoke("preflight", "alias-plugin")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not be a symbolic link", result.stderr)
        self.assertEqual(self.state(), before)

    def test_notes_are_limited_to_the_selected_plugin(self):
        first = self.write_plugin("plugin-one", "1.2.3", "FIRST_PLUGIN_NOTE")
        second = self.write_plugin("plugin-two", "9.8.7", "SECOND_PLUGIN_NOTE")
        self.write_catalog([first, second])
        self.commit_fixture()
        before = self.state()

        result = self.invoke("notes", "plugin-one")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FIRST_PLUGIN_NOTE", result.stdout)
        self.assertNotIn("SECOND_PLUGIN_NOTE", result.stdout)
        self.assertEqual(self.state(), before)


if __name__ == "__main__":
    unittest.main()
