---
name: commit-dev
description: "Use only when the owner explicitly requests a local commit or push. Screens and commits requested work on the currently selected branch. Not for publishing a plugin release."
argument-hint: "[explicit commit or push request and scope]"
disable-model-invocation: true
---

# Commit development changes

Commit only changes the owner requested on the currently selected branch, and push only after a separate explicit request.

## Permissions

- Treat `commit` and `push` as separate actions; a request to commit never authorizes a push.
- On an active `plugin/<name>` or `repo/<topic>` branch, a plain `/commit-dev` requests the changes demonstrably tied to that cycle.
- On `main`, a detached `HEAD`, or any other branch, stop and point to `/start-dev` unless the owner explicitly names `main` and requests a commit there.
- Do not infer a push or an all-files scope from an ambiguous request, and never switch branches.
- Do not require or switch to `develop`.
- Never create missing catalog or changelog content as part of a commit request; ask the owner when a required scope file is missing.
- Never set credentials, bypass hooks, force-push, amend, rebase, reset, or rewrite shared history, and never merge a cycle into `main`.

## Procedure

1. From the repository root, run `git branch --show-current`, `git status --short --branch`, and `git status`. Stop on detached `HEAD` or an unfinished Git operation. A plain `/commit-dev` is allowed only on an active `plugin/<name>` or `repo/<topic>` branch; on `main` or another branch, stop unless the owner explicitly requested a commit on `main`.
2. Resolve the exact cycle from the current branch name. Inspect `git diff --cached`, `git diff`, and `git ls-files --others --exclude-standard`; include only paths demonstrably tied to the requested cycle, plus needed catalog, repository guidance, and changelog changes. For a plugin cycle, stop if any changed path belongs to another `plugins/<name>/` directory. Ask about every path whose relationship to the cycle is unclear.
3. Use `git diff --cached --name-only`, `git diff --name-only`, and `git ls-files --others --exclude-standard` to list staged, unstaged, and untracked paths separately. Treat an in-scope pre-staged path as part of the proposed commit. If any pre-staged path is outside scope, stop and ask the owner to resolve scope; do not unstage, overwrite, or otherwise alter the index. If a path is both staged and unstaged, ask whether to preserve the staged selection or replace it with the complete worktree file. While unresolved, do not stage that path or change its staged content; whole-file `git add` requires explicit approval.
4. Run the [screen_paths.sh](scripts/screen_paths.sh) command with `bash .github/skills/commit-dev/scripts/screen_paths.sh` from the repository root. Ask the owner to resolve every flagged in-scope secret or large path before staging it; leave unrelated flagged paths untouched and report them.
5. Show the exact in-scope paths and proposed commit message or messages. After confirming unclear scope and screening results, stage only approved paths with `git add -- <exact paths>`, excluding any unresolved partially staged path or one whose staged selection the owner chose to preserve. Create only the requested commit with hooks enabled. Keep independently reversible changes in separate commits when that changes the reviewable result.
6. Push only when the owner separately and explicitly requests it. On a cycle branch, push only that exact branch with `git push origin HEAD:refs/heads/<cycle-branch>`; never add a force option or forced refspec. Stop on rejection without changing `main`.
7. After the commit or explicit push, rerun `git status --short --branch` and the separate staged, unstaged, and untracked path commands. Report each commit, the explicit push result when requested, and every remaining path.

The [screen_paths.sh](scripts/screen_paths.sh) script prints one `{path}<TAB>{secret|large}` line for each changed path matching its secret-name patterns or exceeding 5,000,000 bytes. It reads Git path state and file sizes; it does not stage or modify files.

The request is complete when each explicitly requested commit or push succeeds and every excluded or unresolved path is reported.
