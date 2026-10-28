---
name: start-dev
description: "Use when the owner explicitly asks to start or resume a plugin or repository-maintenance cycle. Validates the requested branch and local Git state before switching or creating it. Not for committing or merging work."
argument-hint: "[plugin|repo] [name]"
---

# Start a development cycle

Start or resume exactly one local development-cycle branch after the owner has resolved any ambiguous name or unsafe working state.
When acting as a subagent, return any required owner question to the delegating agent instead of asking the owner or guessing.

## Procedure

1. Require one kind and one exact name, such as `/start-dev plugin sql-tools` or `/start-dev repo workflow-skills`. Ask for the missing value when the request does not resolve to exactly `plugin/<name>` or `repo/<lowercase-kebab-topic>`.
2. Run `git branch --show-current`, `git status --short --branch`, and `git status`. Stop on detached `HEAD` or an unfinished Git operation. Use the full status output to identify staged, unstaged, and untracked paths; list each group and ask whether to carry dirty work onto the target branch. Continue only after an explicit yes, and never stash, reset, discard, or edit those paths.
3. Validate `repo/<name>` as lowercase hyphen-separated words. Require a plugin name of 1-64 lowercase ASCII letters, digits, hyphens, or periods, beginning and ending with a letter or digit and containing neither `--` nor `..`. For an existing plugin, use the exact catalog name and inspect `.github/plugin/marketplace.json` and `plugins/` for case-only spelling collisions; stop on a collision. Ask the owner to confirm when the plugin is new unless the request already confirms that it is new. Require `git check-ref-format --branch <target>` to succeed.
4. If `refs/heads/<target>` exists, report whether it is already current or resume it. If only `refs/remotes/origin/<target>` exists, stop and ask how to handle the remote-only branch; do not recreate or set up tracking implicitly.
5. Before creating a new branch, require committed `refs/heads/main` and cached `refs/remotes/origin/main`, and compare their commit IDs with `git rev-parse --verify`. Stop if either is missing or the IDs differ; do not fetch or update `main` in this procedure.
6. Rerun `git status --short --branch` and `git status` immediately before switching or creating. If dirty paths changed, report them and resolve the carry-over question again. Resume with `git switch -- <target>` or create with `git switch --no-guess -c <target> main`.
7. After a switch or creation, confirm `git branch --show-current` is the exact target and report `git status --short --branch`. Do not resolve changes on the owner's behalf.

## Completion

Report the exact target, whether it was already current, resumed, or created, and whether any paths were explicitly carried over. This procedure changes only local branch selection or creation; it does not create history or contact `origin`.
