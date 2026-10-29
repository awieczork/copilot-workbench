---
name: start-dev
description: "Use when the owner explicitly asks to start or resume a plugin or repository-maintenance cycle. Validates the requested branch and local Git state before switching or creating it. Not for committing or merging work."
argument-hint: "[plugin|repo] [name]"
---

# Start a development cycle

Start or resume exactly one local cycle after the owner resolves any ambiguous name or unsafe working state.
As a subagent, return required owner questions to the delegating agent.

## Procedure

1. Require one kind and one exact name, such as `/start-dev plugin sql-tools` or `/start-dev repo workflow-skills`. Ask for a missing value when the request does not resolve to exactly `plugin/<name>` or `repo/<lowercase-kebab-topic>`.
2. Run `git branch --show-current`, `git status --short --branch`, and `git status`. Stop on detached `HEAD` or an unfinished operation. Check Git paths for `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `rebase-merge`, `rebase-apply`, and `sequencer`; resolve each with `git rev-parse --git-path`. List staged, unstaged, and untracked paths separately and require explicit permission to carry dirty work. Never stash, reset, discard, or edit those paths.
3. Validate a repository topic as lowercase hyphen-separated words. A plugin name has 1-64 lowercase ASCII letters, digits, hyphens, or periods, begins and ends with a letter or digit, and contains neither `--` nor `..`. For an existing plugin, require its exact catalog name and inspect the catalog and `plugins/` for case-only collisions. Stop on a collision. Ask the owner to confirm that an absent plugin is new unless the request already says so. Require `git check-ref-format --branch <target>` to succeed.
4. If `refs/heads/<target>` exists, report that it is already current or resume it. If only `refs/remotes/origin/<target>` exists, ask how to handle that remote-only branch; do not recreate it or configure tracking implicitly.
5. Before creating a branch, require committed `refs/heads/main` and cached `refs/remotes/origin/main`; compare full commit IDs with `git rev-parse --verify`. Stop if either is missing or they differ. Do not fetch or update `main`.
6. Immediately before switching or creating, repeat the status and unfinished-operation checks. If new dirty paths appear, stop for explicit permission to carry them without changing them. Repeat main equality for a new branch. Resume with `git switch -- <target>` or create with `git switch --no-guess -c <target> main`.
7. Confirm the exact target with `git branch --show-current` and report `git status --short --branch`. Verify that the paths permitted for carry-over remain present; do not resolve their changes for the owner.

## Completion

This procedure changes only local branch selection or creation; it does not create a commit or contact a remote.
Report the verified result:

```markdown
- Branch: {exact target}
- Operation: {already current | resumed | created}
- Carried paths: {explicitly permitted paths | none}
```
