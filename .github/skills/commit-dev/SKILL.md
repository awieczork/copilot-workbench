---
name: commit-dev
description: "Use when the owner runs it to commit and push the working-tree changes on `develop`."
argument-hint: "[commit goal, file list, `commit`, or `push`]"
disable-model-invocation: true
---

# Commit changes on develop

Treat an invocation that names no file, path, or action as approval to group, commit, and push every change in the working tree to `origin/develop`.
When the invocation names files or paths, act on them and on the records that "Reconcile the project records" updates, and leave every other path untouched.
The invocation can also name the action `commit`, to commit without pushing, or `push`, to push the existing commits.
Ask the owner each question through #tool:vscode/askQuestions .

## Refuse another branch or an unfinished operation

Read the current branch and the repository state before inspecting or changing anything.
Stop and report the branch unless `develop` is checked out.
Stop and report the unfinished Git operation when a merge, rebase, cherry-pick, bisect, or unresolved conflict is in progress, and leave its resolution to the owner.
Stop and report the upstream when local `develop` has no upstream or its upstream is not `origin/develop`.
Read the unpushed commits with `git log --oneline @{upstream}..HEAD`; when any subject starts with `chore(release):`, stop and direct the owner to `publish-plugin`, because that commit belongs to a release.
When the working tree is clean and unpushed commits exist, push them when the invocation names nothing or `push`; otherwise stop.

## Screen the working tree

Run `bash .github/skills/commit-dev/scripts/screen_paths.sh` from the repository root.
It prints one `{path}<TAB>{secret|large}` line for each staged, unstaged, or untracked path whose name marks a secret (`.env`, `.env.*`, `credentials*`, `*secret*`, `*.pem`, `*.key`) or whose size exceeds 5,000,000 bytes, and marks a path that matches both as `secret`.

Ask about all flagged paths in one question.
Offer a `secret` path two resolutions: add it to the repository-root `.gitignore`, or leave it out of every commit group.
Offer a `large` path three resolutions: add it to the repository-root `.gitignore`, commit it deliberately, or leave it out of every commit group.
When the owner chooses `.gitignore` for a path that Git already tracks, state that ignoring alone leaves the file tracked, and stop for the owner to decide whether to untrack it.
Stop until the owner resolves every flagged path.

## Reconcile the project records

Before showing the commit plan, update each record that owns a fact the selected changes alter, as "Project records" in the project instructions lists them, and read the matching rule in `rules/` first for `CHANGELOG.md`, `PROJECT-STATUS.md`, and `OPEN-ISSUES.md`.
Leave a record unchanged only after confirming that the selected changes make no fact in it stale or missing.
Keep each record update in the same commit group as the change it describes; when one update describes several groups, merge those groups or use a separate `docs:` group and state the dependency in the plan.

## Show the commit plan

Put two changes in separate commits when either could be reverted without the other.
Use conventional commit messages in the form `type: summary`, and add a `(scope)` only when the summary alone does not identify the area.
Use `feat` and `fix` according to the Conventional Commits specification, and use `docs:`, `chore:`, `refactor:`, or `test:` for other work.

Treat a new `version` value in `plugin.json`, or a new versioned `## [x.y.z]` heading in `CHANGELOG.md`, as release preparation: leave both out of every commit group, and tell the owner to revert them and run `publish-plugin`, because it sets the version and the versioned entry itself and starts only from a clean working tree.
In `CHANGELOG.md`, commit only edits inside `## Unreleased`.
Treat an edit inside a versioned changelog entry as release-history maintenance, leave it out of every commit group, and stop for the owner to resolve it.

Show the proposed groups, their paths, and their messages once, then continue without waiting for a reply.
When no new commit group is needed, show the unpushed commits and push target once before pushing.
Update the plan in one line when an owner decision from the screen removes a path from it.

The plan is complete only when every path in scope belongs to exactly one group and every group has a message.

## Commit and push

Stage each group by naming its paths, because `git add -A` and `git add .` stage paths the screen did not clear.
Create each commit with its planned conventional message.
When a staging command or a commit hook fails, report the command and its output and stop for the owner to decide; do not retry with `--no-verify`, because it skips the hook that failed.
When the invocation named `commit`, skip the push and continue with "Verify the result".

Push the completed commits:

```bash
git push origin develop
```

When the push is rejected because `origin/develop` moved ahead, report the divergence and stop for the owner to choose between `git pull --rebase` and another resolution; never force-push or rewrite history in this skill.
When the push fails on authentication, report it and leave the GitHub CLI authentication unchanged, because the owner set up the credential helper.
When `origin` is unreachable, report the error and stop with the commits retained locally.

## Verify the result

After the push, or after the commits for `commit`, read `git status --short --branch` and `git log --oneline -n <number of new commits>`.
Report each commit with its message, the push target, the resolution of every flagged path, every path left uncommitted, and each record left unchanged with the reason.
