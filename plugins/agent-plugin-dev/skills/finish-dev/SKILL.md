---
name: finish-dev
description: "Use when the owner asks to prepare a reviewed plugin or repository-maintenance cycle for integration. Prepares checked cycle work and presents exact effects for approval before integration. Not for release publication."
argument-hint: "[optional plugin/<name> or repo/<topic>]"
disable-model-invocation: true
---

# Finish a development cycle

Prepare one checked cycle for integration, then integrate it only after the owner approves the exact effects.
An explicit `/finish-dev` invocation starts preparation; it does not authorize integration, a push, branch cleanup, or publication.
As a subagent, return required owner questions to the delegating agent.

## Procedure

1. Require one current `plugin/<name>` or `repo/<topic>` branch and an active `start-dev` grant for that exact branch in this session. A branch name or `/finish-dev` request does not establish the grant. If it is absent or expired, stop and request an explicit `/start-dev` start or resume. Check the current branch, worktree, and unfinished Git operations before preparation; do not fetch or switch branches.
2. Complete the cycle's checks and review. Resolve findings, then commit only checked in-scope work by the [cycle commit procedure](../start-dev/references/commit.md). Preserve unrelated paths and staged selections. Stop on unclear scope, screening findings that need owner resolution, or a failed hook.
3. For a plugin cycle with package changes, confirm the changed package is in the source catalog and use the version selected by the owner. Prepare its manifest and versioned notes with the [versioned-notes format](../publish-plugin/references/versioned-notes.md). If the owner has not selected a version, finish the independent checks and ask for that choice before editing release content. For a repository-only cycle with no package changes, omit package-version preparation.
4. Commit version preparation on the cycle branch through the same [cycle commit procedure](../start-dev/references/commit.md). Run the affected checks and review the committed source. Require a clean worktree, record the exact cycle branch and full source commit ID, and confirm the branch still points to that ID.
5. Present the prepared source, change summary, check and review results, selected package version and notes or `none`, integration target `main`, and each proposed effect: local integration into `main`, push of `main`, remote deletion of the exact cycle branch, and local deletion of the exact cycle branch. Ask for approval after preparation. One confirmation may approve several effects only when it names each effect and its exact branch or target. Without integration approval, stop and retain the cycle branch.
6. If the cycle branch changes after review or while approval is pending, stop. Repeat the affected checks and review, update the source ID and proposal, and get fresh integration approval before proceeding.
7. After explicit approval for integration into `main`, run `git fetch origin`; stop on failure, then repeat the branch and clean-state checks. Resolve the exact local cycle tip as `source_tip` and cached `refs/remotes/origin/main` as `base` with `git rev-parse --verify <ref>^{commit}`. Keep both full object IDs; do not substitute moving branch names later. Confirm the local cycle ref still equals the reviewed `source_tip`.
8. Compare local `main` with `base` using `git merge-base --is-ancestor`: continue only when local `main` equals or is an ancestor of `base`. Stop when local `main` is ahead, diverged, missing, or cannot be verified. Run `git ls-remote --heads origin "refs/heads/<cycle-branch>"`; stop on command failure. If it returns a ref, fetch it with `git fetch origin "refs/heads/<cycle-branch>:refs/remotes/origin/<cycle-branch>"`, record its exact tip with `git rev-parse --verify refs/remotes/origin/<cycle-branch>^{commit}`, and require `git merge-base --is-ancestor <remote-tip> <source_tip>` to succeed. Stop if fetch or ancestry verification fails; do not adopt an absent remote ref.
9. Inspect the recorded base/source diff for shipped package changes. For each changed package retained in the source catalog, require its prepared numeric version and one non-empty versioned changelog entry in the source commit. The version must exceed its base version when one exists and its published tag floor; only `agent-team` includes legacy `v*` tags. For a repository-only cycle with no package changes, skip this check. If preparation is missing, return to preparation, use the owner's version selection, and commit through the active `start-dev` grant; do not integrate without it.
10. Before switching branches, run `git merge-tree --write-tree --no-messages <recorded-base> <recorded-source-tip>`. Stop on any non-zero exit; record its first output line as `expected_tree`, read the base tree with `git rev-parse --verify <recorded-base>^{tree}`, and stop if both trees match because the squash is empty. Then switch to `main`. If it was behind `base`, run `git merge --ff-only <recorded-base>`; if it was equal, do not update it. Run `git merge --squash <recorded-source-tip>`, then create one cycle-specific commit with normal hooks and the format in the [cycle commit procedure](../start-dev/references/commit.md). Explicit approval for integration authorizes this local squash commit on `main`; the cycle commit grant does not. Stop on conflict or hook failure without resetting or cleaning the index or worktree. Record the squash commit's full object ID.
11. Resolve the installed [squash verifier](scripts/squash_check.py), then run `uv run --no-project` with its absolute path and `<recorded-base> <recorded-source-tip> <squash-commit>` from the target repository. Require exit status zero and `PASS`. If verification fails, leave the local squash commit and both cycle branches intact.
12. Before a `main` push, confirm the cycle branch still equals the reviewed `source_tip`. Require separate explicit permission to push `main`; integration approval alone does not authorize it. Push only with `git -c push.followTags=false push origin main:refs/heads/main`, without force options or a forced refspec. If the push fails, retain both cycle branches and report that the squash commit is local and unpushed.
13. After a successful push, run `git fetch origin`; stop on failure. Require a clean `main` and verify `git merge-base --is-ancestor <squash-commit> refs/remotes/origin/main`.
14. If cleanup was approved, read [cycle cleanup](references/cleanup.md) after the verified push and before any deletion. Require separate named permission for each remote or local branch deletion. Otherwise, retain cycle branches and report the integration result.

## Verifier

The installed [verifier](scripts/squash_check.py) requires Python 3.11+ and Git.
It accepts the three object IDs from step 11 as full lowercase hexadecimal strings of 40 or 64 characters.
It recomputes the merge tree with `git merge-tree --write-tree` and requires the squash commit to have exactly the recorded base as its sole parent and the computed merge tree.
Exit `0` prints `PASS` to standard output; exit `1` prints `FAIL: ...` to standard error, including for invalid arguments.
The verifier does not inspect branch, worktree, or remote state.
Git may write the computed tree object, but the command does not update refs, the index, worktree, or remotes.

When changing the verifier or integration commands, run the [proof tests](tests/test_squash_check.py) and [cycle command tests](tests/test_cycle_integration.py) with `uv run --no-project python -m unittest discover -s` followed by this skill's absolute test-directory path.

## Boundaries

- Stop cleanup after a failed proof, push, deletion, or remote-absence check, or a changed source tip. Retain any remaining cycle branches and report completed effects; cleanup is not atomic.
- Do not tag, publish, create a release, change credentials, bypass hooks, or rewrite shared history.
- Treat local fixtures as command-behavior checks only; they do not prove authentication, branch protection, remote hooks, or client activation.

## Completion

Report completed effects even on failure, because cleanup is not atomic.

```markdown
- Base and source: {recorded full object IDs}
- Squash commit: {full object ID | not created}
- Main push: {result | not approved | not requested}
- Remote branch deletion: {result | not approved | not requested}
- Local branch deletion: {result | not approved | not requested}
- Remaining branches or blockers: {exact refs and unresolved checks or permissions | none}
```
