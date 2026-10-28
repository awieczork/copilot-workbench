#!/usr/bin/env bash
# Release helper for publish-plugin; run from the repository root.
#   release.sh allowlist          print the package paths
#   release.sh preflight          check that a release can start; print each failed check and a pending release commit
#   release.sh build <version>    build and verify the package-only main snapshot in a sibling git worktree
#   release.sh notes <version>    print the body of the version's CHANGELOG.md entry
#   release.sh clean              remove the sibling git worktree when it holds no changes
set -uo pipefail
ALLOWLIST=(.github/plugin/marketplace.json CHANGELOG.md README.md plugin.json .mcp.json agents rules skills)
RELEASE_FILES=(plugin.json CHANGELOG.md PROJECT-STATUS.md)
root="$(git rev-parse --show-toplevel)"
worktree="${root}.plugin-worktree"
failed=0
fail() {
  echo "FAIL: $*"
  failed=1
}

# Print the sibling path's state: absent, clean (a registered worktree without changes), or other.
worktree_state() {
  if [ ! -e "$worktree" ]; then
    echo absent
  elif git worktree list --porcelain | grep -qxF "worktree $worktree" &&
    [ -z "$(git -C "$worktree" status --porcelain --ignored)" ]; then
    echo clean
  else
    echo other
  fi
}

# Remove the sibling worktree when it is registered and clean; return 1 when the path holds anything else.
remove_worktree() {
  case "$(worktree_state)" in
  absent) return 0 ;;
  clean) git worktree remove "$worktree" ;;
  *) return 1 ;;
  esac
}

case "${1:-}" in
allowlist)
  printf '%s\n' "${ALLOWLIST[@]}"
  ;;
preflight)
  [ "$(git branch --show-current)" = develop ] || fail "the current branch is not develop"
  [ -z "$(git status --porcelain -- "${RELEASE_FILES[@]}")" ] ||
    fail "uncommitted changes in a release file: ${RELEASE_FILES[*]}"
  gitdir="$(git rev-parse --git-dir)"
  for state in MERGE_HEAD rebase-merge rebase-apply CHERRY_PICK_HEAD BISECT_LOG; do
    [ -e "$gitdir/$state" ] && fail "an unfinished operation is in progress ($state)"
  done
  git fetch --quiet origin develop main --tags || fail "fetching origin failed"
  git rev-parse -q --verify origin/develop >/dev/null || fail "origin/develop is missing"
  git rev-parse -q --verify origin/main >/dev/null || fail "origin/main is missing"
  git merge-base --is-ancestor origin/develop develop 2>/dev/null || fail "develop does not contain origin/develop"
  git worktree list --porcelain | awk -v wt="$worktree" '/^worktree /{p=substr($0,10)} /^branch refs\/heads\/main$/ && p!=wt {f=1} END{exit !f}' &&
    fail "a git worktree other than $worktree has main checked out"
  [ "$(worktree_state)" = other ] && fail "$worktree holds changes or is not a git worktree; inspect and remove it"
  gh auth status >/dev/null 2>&1 || fail "gh auth status failed"
  git log --format='%H %s' origin/develop..develop | grep ' chore(release): prepare v' | sed 's/^/PENDING: /'
  [ "$failed" = 0 ] && echo ok
  exit "$failed"
  ;;
build)
  version="${2:?usage: release.sh build <version>}"
  set -e
  git worktree prune
  remove_worktree || {
    echo "FAIL: $worktree holds changes or is not a git worktree"
    exit 1
  }
  git worktree add --quiet -B main "$worktree" origin/main
  # From here the worktree is this run's own state, so remove it on any failure.
  build_fail() {
    echo "FAIL: $*"
    git worktree remove --force "$worktree"
    exit 1
  }
  trap 'build_fail "a git command failed"' ERR
  git -C "$worktree" read-tree --reset -u "$(git mktree </dev/null)"
  git -C "$worktree" restore --source=develop --staged --worktree -- "${ALLOWLIST[@]}"
  git -C "$worktree" commit --quiet -m "chore(release): publish v$version"
  trap - ERR
  git -C "$worktree" diff --quiet develop HEAD -- "${ALLOWLIST[@]}" ||
    build_fail "the snapshot differs from develop over the allowlist"
  pattern="$(printf '%s\n' "${ALLOWLIST[@]}" | sed 's/\./\\./g' | paste -sd '|')"
  outside="$(git -C "$worktree" ls-tree -r --name-only HEAD | grep -vE "^($pattern)(/|$)" || true)"
  [ -z "$outside" ] || build_fail "the snapshot holds paths outside the allowlist: $(echo $outside)"
  uv run -q "$root/.github/skills/build-plugin/scripts/check_package.py" "$worktree" ||
    build_fail "the package check failed on the snapshot"
  git -C "$worktree" rev-parse HEAD
  ;;
notes)
  version="${2:?usage: release.sh notes <version>}"
  body="$(git show develop:CHANGELOG.md | awk -v h="## [$version]" '
    index($0, h) == 1 {on=1; next}
    on && /^## / {exit}
    on {print}' | sed -e '/./,$!d')"
  [ -n "$body" ] || {
    echo "FAIL: CHANGELOG.md on develop has no entry for $version" >&2
    exit 1
  }
  printf '%s\n' "$body"
  ;;
clean)
  remove_worktree || {
    echo "FAIL: $worktree holds changes; it was kept"
    exit 1
  }
  echo ok
  ;;
*)
  echo "usage: release.sh allowlist | preflight | build <version> | notes <version> | clean" >&2
  exit 2
  ;;
esac
