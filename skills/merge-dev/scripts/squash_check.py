# /// script
# requires-python = ">=3.11"
# ///
"""Check that a squash commit matches its recorded base and source commits."""

import re
import subprocess
import sys

OBJECT_ID = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")


def run_git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments], capture_output=True, text=True, check=False
    )


def fail(message: str) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return 1


def main(arguments: list[str]) -> int:
    if len(arguments) != 3:
        return fail("usage: squash_check.py <base-commit> <source-commit> <squash-commit>")
    base, source, squash = arguments
    if not all(OBJECT_ID.fullmatch(value) for value in arguments):
        return fail("base, source, and squash must be full object IDs")

    merge = run_git("merge-tree", "--write-tree", "--no-messages", base, source)
    if merge.returncode != 0:
        return fail("recorded base and source do not produce a clean merge tree")
    merge_tree = merge.stdout.splitlines()[0] if merge.stdout.splitlines() else ""
    if not OBJECT_ID.fullmatch(merge_tree):
        return fail("Git did not return a merge tree object ID")

    base_tree = run_git("rev-parse", "--verify", f"{base}^{{tree}}")
    if base_tree.returncode != 0:
        return fail("recorded base is not a commit")
    if base_tree.stdout.strip() == merge_tree:
        return fail("recorded base and source produce no tree change")

    commit = run_git("show", "-s", "--format=%T%n%P", squash)
    if commit.returncode != 0:
        return fail("squash input is not a commit")
    fields = commit.stdout.splitlines()
    commit_tree = fields[0] if fields else ""
    parents = fields[1].split() if len(fields) > 1 else []
    if parents != [base]:
        return fail("squash commit must have the recorded base as its only parent")
    if commit_tree != merge_tree:
        return fail("squash commit tree does not match the recorded merge")

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
