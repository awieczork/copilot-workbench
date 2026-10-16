---
name: commit-dev
description: "Use when the owner runs it to commit and push the working-tree changes on `develop`."
argument-hint: "[commit goal, file list, `commit`, or `push`]"
disable-model-invocation: true
---

# Commit changes on develop

Treat an invocation that names no file, path, or action as approval to group, commit, and push every change in the working tree to `origin/develop`.
When the invocation names files or paths, act on them, and leave every other path untouched.
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
It prints one `{path}<TAB>{secret|large}` line for each staged, unstaged, or untracked path whose name marks a secret (`.env`, `.env.*`, `credentials*`, `*secret*`, `*.pem`, `*.key`) or whose size exceeds 5,000,000 bytes.

Ask about all flagged paths in one question.
Offer each flagged path three resolutions: add it to the repository-root `.gitignore`, and untrack it with `git rm --cached` when Git already tracks it; leave it out of every commit group; or commit it, a `large` path deliberately and a `secret` path only as a file without a secret.

## Show the commit plan

Put two changes in separate commits when either could be reverted without the other.
Use conventional commit messages in the form `type: summary`, and add a `(scope)` only when the summary alone does not identify the area.
Use `feat` and `fix` according to the Conventional Commits specification, and use `docs:`, `chore:`, `refactor:`, or `test:` for other work.

Treat a new `version` value in `plugin.json`, or a new versioned `## [x.y.z]` heading in `CHANGELOG.md`, as release preparation: leave both out of every commit group, and tell the owner to revert them and run `publish-plugin`, because it sets the version and the versioned entry itself and requires `plugin.json`, `CHANGELOG.md`, and `PROJECT-STATUS.md` to be clean.
Commit edits inside versioned changelog entries in their own `docs:` group.

Show the proposed groups, their paths, and their messages once, then continue without waiting for a reply.
When no new commit group is needed, show the unpushed commits and push target once before pushing.

The plan is complete only when every path in scope belongs to exactly one group and every group has a message.

## Commit and push

Commit `## Unreleased` edits that are already uncommitted when the run starts as they are, in one `docs:` group before the others, because one file cannot be split between groups.
Before you stage a group with a user-visible result, write or update its `## Unreleased` bullets by the [changelog rule](../../../rules/changelog.instructions.md), and stage `CHANGELOG.md` with that group, so that reverting the group also reverts its bullets.
Leave the other records as the work left them, because the work that changes a fact updates the record that owns it.
Stage each group by naming its paths, because `git add -A` and `git add .` stage paths the screen did not clear.
Create each commit with its planned conventional message.
When a staging command or a commit hook fails, report the command and its output and stop for the owner to decide; do not retry with `--no-verify`, because it skips the hook that failed.
When the invocation named `commit`, skip the push and continue with "Verify the result".

Push the completed commits:

```bash
git push origin develop
```

When the push is rejected because `origin/develop` moved ahead, ask once whether to run `git pull --rebase --autostash origin develop` and push again, because the rebase moves only the unpushed commits; when the rebase stops on a conflict, report the conflicting paths, run `git rebase --abort`, which also restores the stashed paths, and stop.
Never force-push or rewrite pushed history in this skill.
When the push fails on authentication, report it and leave the GitHub CLI authentication unchanged, because the owner set up the credential helper.
When `origin` is unreachable, report the error and stop with the commits retained locally.

## Verify the result

After the push, or after the commits for `commit`, read `git status --short --branch` and `git log --oneline -n <number of new commits>`.
Report each commit with its message, the push target, the resolution of every flagged path, every path left uncommitted, and each changelog bullet written.
