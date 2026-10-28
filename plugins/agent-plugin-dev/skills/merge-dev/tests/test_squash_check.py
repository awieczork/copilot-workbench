"""Regression tests for exact squash-content verification."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/squash_check.py"


class SquashCheckTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
        self.root.mkdir()
        self.environment = os.environ.copy()
        for key in tuple(self.environment):
            if key.startswith("GIT_"):
                self.environment.pop(key)
        self.environment.update(
            {
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_AUTHOR_NAME": "Fixture User",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture User",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            }
        )
        self.git("init", "--initial-branch=main")
        self.git("config", "user.name", "Fixture User")
        self.git("config", "user.email", "fixture@example.invalid")
        self.write("README.md", "base\n")
        self.commit("fixture base")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("switch", "-c", "repo/fixture")
        self.write("cycle.txt", "cycle change\n")
        self.commit("cycle change")
        self.source = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("switch", "main")
        self.git("merge", "--squash", self.source)
        self.git("commit", "-m", "fixture squash")
        self.squash = self.git("rev-parse", "HEAD").stdout.strip()

    def tearDown(self):
        self.temporary_directory.cleanup()

    def git(self, *arguments, check=True):
        result = subprocess.run(
            ["git", "-C", str(self.root), *arguments],
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
        )
        if check and result.returncode:
            self.fail(f"git {arguments!r} failed: {result.stderr}")
        return result

    def write(self, relative_path, text):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message):
        self.git("add", "--all")
        self.git("commit", "-m", message)

    def invoke(self, *arguments):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *arguments],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
        )

    def assert_rejected(self, result):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL:", result.stderr)

    def test_accepts_recorded_squash(self):
        result = self.invoke(self.base, self.source, self.squash)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "PASS")

    def test_rejects_empty_merge(self):
        result = self.invoke(self.base, self.base, self.squash)
        self.assert_rejected(result)
        self.assertIn("no tree change", result.stderr)

    def test_rejects_mismatched_tree_or_parent(self):
        self.git("switch", "-c", "repo/wrong-tree", self.base)
        self.write("extra.txt", "not part of the merge\n")
        self.commit("wrong tree")
        wrong_tree = self.git("rev-parse", "HEAD").stdout.strip()
        tree_mismatch = self.invoke(self.base, self.source, wrong_tree)
        self.assert_rejected(tree_mismatch)
        self.assertIn("tree", tree_mismatch.stderr)

        expected_tree = self.git("merge-tree", "--write-tree", self.base, self.source)
        self.assertEqual(expected_tree.returncode, 0, expected_tree.stderr)
        self.git("switch", "-c", "repo/other-parent", self.base)
        self.write("other.txt", "another parent\n")
        self.commit("other parent")
        other_parent = self.git("rev-parse", "HEAD").stdout.strip()
        wrong_parent = self.git(
            "commit-tree",
            expected_tree.stdout.strip(),
            "-p",
            other_parent,
            "-m",
            "wrong parent",
        ).stdout.strip()

        parent_mismatch = self.invoke(self.base, self.source, wrong_parent)
        self.assert_rejected(parent_mismatch)
        self.assertIn("parent", parent_mismatch.stderr)

    def test_rejects_altered_base_or_source(self):
        self.git("switch", "-c", "fixture/advanced-main", self.base)
        self.write("main-only.txt", "advanced base\n")
        self.commit("advance base")
        altered_base = self.git("rev-parse", "HEAD").stdout.strip()
        wrong_base = self.invoke(altered_base, self.source, self.squash)
        self.assert_rejected(wrong_base)
        self.assertIn("parent", wrong_base.stderr)

        self.git("switch", "repo/fixture")
        self.write("later-cycle.txt", "later source work\n")
        self.commit("advance source")
        altered_source = self.git("rev-parse", "HEAD").stdout.strip()
        wrong_source = self.invoke(self.base, altered_source, self.squash)
        self.assert_rejected(wrong_source)
        self.assertIn("tree", wrong_source.stderr)

    def test_rejects_conflicts_and_missing_inputs(self):
        missing_arguments = self.invoke()
        self.assert_rejected(missing_arguments)

        missing_object = self.invoke("f" * 40, self.source, self.squash)
        self.assert_rejected(missing_object)

        self.git("switch", "repo/fixture")
        self.write("README.md", "source side\n")
        self.commit("conflicting source")
        conflicting_source = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("switch", "-c", "fixture/conflicting-main", self.base)
        self.write("README.md", "main side\n")
        self.commit("conflicting base")
        conflicting_base = self.git("rev-parse", "HEAD").stdout.strip()

        conflict = self.invoke(conflicting_base, conflicting_source, self.squash)
        self.assert_rejected(conflict)
        self.assertIn("merge", conflict.stderr)


if __name__ == "__main__":
    unittest.main()
