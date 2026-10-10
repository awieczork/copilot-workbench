#!/usr/bin/env bash
# Release helper for publish-plugin; run from the repository root.
#   release.sh allowlist          print the package paths
#   release.sh preflight          check that a release can start; print each failed check
#   release.sh build <version>    build and verify the package-only main snapshot in a sibling git worktree
set -uo pipefail
ALLOWLIST=(CHANGELOG.md README.md plugin.json mcp.json com.github.copilot skills)
root="$(git rev-parse --show-toplevel)"
worktree="${root}.plugin-worktree"
failed=0
fail() {
  echo "FAIL: $*"
  failed=1
}

case "${1:-}" in
allowlist)
  printf '%s\n' "${ALLOWLIST[@]}"
  ;;
preflight)
  [ "$(git branch --show-current)" = develop ] || fail "the current branch is not develop"
  [ -z "$(git status --porcelain)" ] || fail "the working tree is not clean"
  gitdir="$(git rev-parse --git-dir)"
  for state in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD BISECT_LOG; do
    [ -e "$gitdir/$state" ] && fail "an unfinished operation is in progress ($state)"
  done
  git fetch --quiet origin develop main --tags || fail "fetching origin failed"
  git rev-parse -q --verify origin/develop >/dev/null || fail "origin/develop is missing"
  git rev-parse -q --verify origin/main >/dev/null || fail "origin/main is missing"
  git merge-base --is-ancestor origin/develop develop 2>/dev/null || fail "develop does not contain origin/develop"
  git worktree list --porcelain | grep -x 'branch refs/heads/main' >/dev/null && fail "a git worktree has main checked out"
  [ -e "$worktree" ] && fail "$worktree exists"
  if git rev-parse -q --verify refs/heads/main >/dev/null; then
    [ "$(git rev-parse main)" = "$(git rev-parse origin/main)" ] || fail "local main differs from origin/main"
  fi
  git log --format=%s origin/develop..develop | grep '^chore(release):' >/dev/null && fail "develop has an unpushed chore(release) commit"
  gh auth status >/dev/null 2>&1 || fail "gh auth status failed"
  uv run -q "$root/.github/skills/build-plugin/scripts/check_package.py" "$root" >/dev/null ||
    fail "the package check failed; run .github/skills/build-plugin/scripts/check_package.py for details"
  [ "$failed" = 0 ] && echo ok
  exit "$failed"
  ;;
build)
  version="${2:?usage: release.sh build <version>}"
  set -e
  if git rev-parse -q --verify refs/heads/main >/dev/null; then
    git worktree add --quiet "$worktree" main
  else
    git worktree add --quiet -b main "$worktree" origin/main
  fi
  git -C "$worktree" read-tree --reset -u "$(git mktree </dev/null)"
  git -C "$worktree" restore --source=develop --staged --worktree -- "${ALLOWLIST[@]}"
  git -C "$worktree" commit --quiet -m "chore(release): publish v$version"
  git -C "$worktree" diff --quiet develop HEAD -- "${ALLOWLIST[@]}" || {
    echo "FAIL: the snapshot differs from develop over the allowlist"
    exit 1
  }
  pattern="$(printf '%s\n' "${ALLOWLIST[@]}" | sed 's/\./\\./g' | paste -sd '|')"
  outside="$(git -C "$worktree" ls-tree -r --name-only HEAD | grep -vE "^($pattern)(/|$)" || true)"
  [ -z "$outside" ] || {
    echo "FAIL: the snapshot holds paths outside the allowlist:"
    echo "$outside"
    exit 1
  }
  git -C "$worktree" rev-parse HEAD
  ;;
*)
  echo "usage: release.sh allowlist | preflight | build <version>" >&2
  exit 2
  ;;
esac
