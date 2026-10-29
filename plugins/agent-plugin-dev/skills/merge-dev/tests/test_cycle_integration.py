"""Exercise squash verification and guarded cleanup in local Git fixtures."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BRANCH = "repo/fixture"
SCRIPT = Path(__file__).parents[1] / "scripts/squash_check.py"


class GitFixture:
    def __init__(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.root = root / "repository"
        self.origin = root / "origin.git"
        self.other = root / "other"
        self.home = root / "home"
        self.root.mkdir()
        self.home.mkdir()
        self.environment = os.environ.copy()
        for key in tuple(self.environment):
            if key.startswith("GIT_"):
                self.environment.pop(key)
        self.environment.update(
            {
                "HOME": str(self.home),
                "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_CONFIG_GLOBAL": os.devnull,
                "GIT_TERMINAL_PROMPT": "0",
                "GIT_AUTHOR_NAME": "Fixture User",
                "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                "GIT_COMMITTER_NAME": "Fixture User",
                "GIT_COMMITTER_EMAIL": "fixture@example.invalid",
            }
        )
        self.git("init", "--initial-branch=main")
        self.configure(self.root)
        self.git("init", "--bare", "--initial-branch=main", str(self.origin))
        self.write("README.md", "base\n")
        self.commit("fixture base")
        self.base = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("remote", "add", "origin", str(self.origin))
        self.git("push", "--set-upstream", "origin", "main")
        self.git("fetch", "origin")
        self.git("switch", "-c", BRANCH)
        self.write("cycle.txt", "cycle change\n")
        self.commit("cycle change")
        self.source = self.git("rev-parse", "HEAD").stdout.strip()
        self.git("push", "--set-upstream", "origin", BRANCH)
        self.git("fetch", "origin")
        self.git("switch", "main")
        self.git("merge", "--squash", self.source)
        self.git("commit", "-m", "fixture squash")
        self.squash = self.git("rev-parse", "HEAD").stdout.strip()

    def close(self):
        self.temporary_directory.cleanup()

    def configure(self, repository):
        self.git(repository, "config", "user.name", "Fixture User")
        self.git(repository, "config", "user.email", "fixture@example.invalid")
        self.git(repository, "config", "core.hooksPath", os.devnull)
        self.git(repository, "config", "commit.gpgsign", "false")

    def git(self, *arguments, check=True):
        repository = self.root
        if arguments and isinstance(arguments[0], Path):
            repository, *arguments = arguments
        result = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
        )
        if check and result.returncode:
            raise AssertionError(f"git {arguments!r} failed: {result.stderr}")
        return result

    def bare_git(self, *arguments, check=True):
        result = subprocess.run(
            ["git", "--git-dir", str(self.origin), *arguments],
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
        )
        if check and result.returncode:
            raise AssertionError(f"git --git-dir {arguments!r} failed: {result.stderr}")
        return result

    def write(self, relative_path, text, repository=None):
        path = (repository or self.root) / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def commit(self, message):
        self.git("add", "--all")
        self.git("commit", "-m", message)

    def verify(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), self.base, self.source, self.squash],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
            env=self.environment,
        )

    def delete_remote(self, expected_tip):
        return self.git(
            "push",
            f"--force-with-lease=refs/heads/{BRANCH}:{expected_tip}",
            "origin",
            f":refs/heads/{BRANCH}",
            check=False,
        )


class CycleIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.fixtures = []

    def tearDown(self):
        for fixture in self.fixtures:
            fixture.close()

    def fixture(self):
        fixture = GitFixture()
        self.fixtures.append(fixture)
        return fixture

    def test_squash_verification_and_remote_absence_commands(self):
        fixture = self.fixture()
        proof = fixture.verify()
        self.assertEqual(proof.returncode, 0, proof.stderr)
        self.assertEqual(proof.stdout.strip(), "PASS")
        self.assertEqual(
            fixture.git("show", "-s", "--format=%T%n%P", fixture.squash).stdout.splitlines()[1],
            fixture.base,
        )

        fixture.git("push", "origin", "main:refs/heads/main")
        fixture.git("fetch", "origin")
        self.assertEqual(
            fixture.git(
                "merge-base", "--is-ancestor", fixture.squash, "refs/remotes/origin/main", check=False
            ).returncode,
            0,
        )
        self.assertEqual(
            fixture.git("rev-parse", f"refs/heads/{BRANCH}").stdout.strip(), fixture.source
        )
        remote_tip = fixture.git(
            "rev-parse", f"refs/remotes/origin/{BRANCH}"
        ).stdout.strip()
        self.assertEqual(remote_tip, fixture.source)

        deletion = fixture.delete_remote(remote_tip)
        self.assertEqual(deletion.returncode, 0, deletion.stderr)
        absence = fixture.git(
            "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}", check=False
        )
        self.assertEqual(absence.returncode, 0, absence.stderr)
        self.assertEqual(absence.stdout, "")
        self.assertEqual(
            fixture.git("rev-parse", f"refs/heads/{BRANCH}").stdout.strip(), fixture.source
        )
        fixture.git("branch", "-D", "--", BRANCH)

    def test_stale_remote_deletion_lease_preserves_newer_work(self):
        fixture = self.fixture()
        fixture.git("clone", "--branch", BRANCH, str(fixture.origin), str(fixture.other))
        fixture.configure(fixture.other)
        fixture.write("newer-remote.txt", "preserve this work\n", fixture.other)
        fixture.git(fixture.other, "add", "newer-remote.txt")
        fixture.git(fixture.other, "commit", "-m", "newer remote work")
        newer_tip = fixture.git(fixture.other, "rev-parse", "HEAD").stdout.strip()
        fixture.git(fixture.other, "push", "origin", f"HEAD:refs/heads/{BRANCH}")

        deletion = fixture.delete_remote(fixture.source)

        self.assertNotEqual(deletion.returncode, 0)
        self.assertEqual(
            fixture.bare_git("rev-parse", f"refs/heads/{BRANCH}").stdout.strip(), newer_tip
        )
        self.assertEqual(
            fixture.git("rev-parse", f"refs/heads/{BRANCH}").stdout.strip(), fixture.source
        )

    def test_remote_delete_refusal_and_unreachable_query(self):
        fixture = self.fixture()
        fixture.bare_git("config", "receive.denyDeletes", "true")

        deletion = fixture.delete_remote(fixture.source)

        self.assertNotEqual(deletion.returncode, 0)
        self.assertEqual(
            fixture.bare_git("show-ref", "--verify", f"refs/heads/{BRANCH}").returncode, 0
        )
        fixture.git("remote", "set-url", "origin", str(fixture.root.parent / "missing-origin.git"))
        absence = fixture.git(
            "ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}", check=False
        )
        self.assertNotEqual(absence.returncode, 0)
        self.assertEqual(absence.stdout, "")

    def test_verifier_from_external_installation(self):
        fixture = self.fixture()
        installed = fixture.root.parent / "installed skill"
        shutil.copytree(SCRIPT.parent.parent, installed)
        result = subprocess.run(
            [sys.executable, str(installed / "scripts/squash_check.py"),
             fixture.base, fixture.source, fixture.squash],
            cwd=fixture.root, env=fixture.environment, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "PASS")

    def test_failed_main_push_retains_cycle_refs(self):
        fixture = self.fixture()
        fixture.bare_git("update-ref", "refs/heads/main", fixture.source)
        result = fixture.git("-c", "push.followTags=false", "push", "origin",
                             "main:refs/heads/main", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(fixture.bare_git("rev-parse", "refs/heads/main").stdout.strip(), fixture.source)
        self.assertEqual(fixture.git("rev-parse", f"refs/heads/{BRANCH}").stdout.strip(), fixture.source)
        self.assertEqual(fixture.bare_git("rev-parse", f"refs/heads/{BRANCH}").stdout.strip(), fixture.source)

    def test_hook_failure_retains_commit_and_cycle(self):
        fixture = self.fixture()
        hooks = fixture.root.parent / "hooks"
        hooks.mkdir()
        hook = hooks / "pre-commit"
        hook.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        hook.chmod(0o755)
        fixture.git("config", "core.hooksPath", str(hooks))
        fixture.write("blocked.txt", "blocked commit\n")
        fixture.git("add", "--", "blocked.txt")
        result = fixture.git("commit", "-m", "must fail", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(fixture.git("rev-parse", "HEAD").stdout.strip(), fixture.squash)
        self.assertIn("blocked.txt", fixture.git("diff", "--cached", "--name-only").stdout)
        self.assertEqual(fixture.git("rev-parse", f"refs/heads/{BRANCH}").stdout.strip(), fixture.source)

if __name__ == "__main__":
    unittest.main()
