---
name: merge-dev
description: "Use only when the owner explicitly approves merging a reviewed plugin or repository-maintenance cycle. Squashes the selected cycle onto main, pushes main normally, and removes cycle branches only after proof. Not for publication."
argument-hint: "[optional plugin/<name> or repo/<topic>]"
disable-model-invocation: true
---

# Merge a development cycle

Create one verified squash commit after explicit integration approval.
Require separate explicit scope for the `main` push and for each named remote or local branch deletion; integration approval alone authorizes neither.
Follow a project's explicitly selected exceptional integration path instead of this squash procedure.
As a subagent, return required owner questions to the delegating agent.

## Procedure

1. Require an explicit `/merge-dev` request after local review. Use the current `plugin/<exact-plugin-name>` or `repo/<lowercase-kebab-topic>` branch, or require the owner to name one. Run `git status --short --branch` and `git status`; stop on detached `HEAD`, an unfinished operation, or any staged, unstaged, or untracked path. If another cycle branch was named, confirm its local ref, switch to it, and repeat these checks.
2. Run `git fetch origin`; stop on failure, then repeat the branch and clean-state checks. Resolve the exact local cycle tip as `source_tip` and cached `refs/remotes/origin/main` as `base` with `git rev-parse --verify <ref>^{commit}`. Keep both full object IDs; do not substitute moving branch names later.
3. Compare local `main` with `base` using `git merge-base --is-ancestor`: continue only when local `main` equals or is an ancestor of `base`. Stop when local `main` is ahead, diverged, missing, or cannot be verified. Run `git ls-remote --heads origin "refs/heads/<cycle-branch>"`; stop on command failure. If it returns a ref, fetch it with `git fetch origin "refs/heads/<cycle-branch>:refs/remotes/origin/<cycle-branch>"`, record its exact tip with `git rev-parse --verify refs/remotes/origin/<cycle-branch>^{commit}`, and require `git merge-base --is-ancestor <remote-tip> <source_tip>` to succeed. Stop if fetch or ancestry verification fails; an absent remote ref is not adopted.
4. Before integration, inspect the recorded base/source diff for shipped package changes. For each changed package retained in the source catalog, require its prepared numeric version and one non-empty versioned changelog entry in the source commit, using [versioned notes](../publish-plugin/references/versioned-notes.md) for the entry format. The version must exceed its base version when one exists and its published tag floor; only `agent-team` includes legacy `v*` tags. For a repository-only cycle with no package changes, this check does not apply. If preparation is missing, stop on the cycle; resolve the version choice with the owner and commit preparation through `commit-dev` only under an explicit commit request. Do not prepare release content during integration.
5. Before switching branches, run `git merge-tree --write-tree --no-messages <recorded-base> <recorded-source-tip>`. Stop on any non-zero exit; record its first output line as `expected_tree`, read the base tree with `git rev-parse --verify <recorded-base>^{tree}`, and stop if both trees match because the squash is empty. This preflight does not update refs, index, or worktree. Then switch to `main`. If it was behind `base`, run `git merge --ff-only <recorded-base>`; if it was equal, do not update it. Run `git merge --squash <recorded-source-tip>`, then create one cycle-specific commit with normal hooks and the Conventional Commits format owned by `commit-dev`. Stop on conflict or hook failure without resetting or cleaning the index or worktree. Record the squash commit's full object ID.
6. Resolve [squash_check.py](scripts/squash_check.py) from this skill's loaded location, then run `uv run --no-project` with that absolute path and `<recorded-base> <recorded-source-tip> <squash-commit>` from the target repository. Require exit status zero and `PASS`. If verification fails, leave the local squash commit and both cycle branches intact.
7. Require explicit permission to push `main`; otherwise stop with the local result and retain cycle branches. Push only `main` with `git -c push.followTags=false push origin main:refs/heads/main`, without force options or a forced refspec. If the push fails, retain both cycle branches and report that the squash commit is local and unpushed.
8. After a successful push, run `git fetch origin`; stop on failure. Require a clean `main` and verify `git merge-base --is-ancestor <squash-commit> refs/remotes/origin/main`.
9. If branch cleanup was requested, read [cycle cleanup](references/cleanup.md) after the verified push and before any deletion. Otherwise, retain cycle branches and report the integration result.

## Verifier

The installed [verifier](scripts/squash_check.py) requires Python 3.11+ and Git.
It accepts the three object IDs from step 6 as full lowercase hexadecimal strings of 40 or 64 characters.
It recomputes the merge tree with `git merge-tree --write-tree` and requires the squash commit to have exactly the recorded base as its sole parent and the computed merge tree.
Exit `0` prints `PASS` to standard output; exit `1` prints `FAIL: ...` to standard error, including for invalid arguments.
Output is not capped.
The verifier does not inspect branch, worktree, or remote state.
Git may write the computed tree object, but the command does not update refs, the index, worktree, or remotes.

When changing the verifier or integration commands, run the [proof tests](tests/test_squash_check.py) and [cycle command tests](tests/test_cycle_integration.py) with `uv run --no-project python -m unittest discover -s` followed by this skill's absolute test-directory path.

## Boundaries

- Stop cleanup after a failed proof, push, deletion, or remote-absence check, or a changed source tip; retain any remaining cycle branches and report completed effects.
- Do not tag, publish, create a release, change credentials, bypass hooks, rewrite history, or use a blanket force option.
- Treat local fixtures as command-behavior checks only; they do not prove authentication, branch protection, remote hooks, or client activation.

## Completion

Report completed effects even on failure, because cleanup is not atomic.

```markdown
- Base and source: {recorded full object IDs}
- Squash commit: {full object ID | not created}
- Main push: {result | not requested}
- Remote branch deletion: {result | not requested}
- Local branch deletion: {result | not requested}
- Remaining branches or blockers: {exact refs and unresolved checks or permissions | none}
```
