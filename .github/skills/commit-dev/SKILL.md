---
name: commit-dev
description: Commit and push day-to-day changes on `develop`, reconcile `CHANGELOG.md`, `PROJECT-STATUS.md`, and `OPEN-ISSUES.md`, and apply a safety screen for data files, secrets, and large files. Use when the owner asks to inspect, commit, or push build-workspace changes on the develop branch.
argument-hint: "[commit goal, action, or file list]"
disable-model-invocation: true
---

# Commit changes on develop

Handle day-to-day Git work on `develop`.

Treat an invocation that names no file, path, or action as approval to group, commit, and push every change in the working tree to `origin/develop`.
When the invocation names a file, a path, or an action, act on that set plus the repository documentation paths required by the synchronization step, and leave every other path untouched.

## Refuse another branch or an unfinished operation

Read the current branch and the repository state before inspecting or changing anything.
Require the branch to be exactly `develop`.
Stop and report the branch when `HEAD` is detached or any other branch is checked out.
Stop and report the unfinished Git operation when a merge, rebase, cherry-pick, bisect, or unresolved conflict is in progress, and leave its resolution to the owner.
Stop and report the upstream when local `develop` has no upstream or its upstream is not `origin/develop`.
When `git status --porcelain` returns no output, continue as a push-only run only for an invocation with no file or path, or one that explicitly names the `push` action; stop when no unpushed commit exists.

## Screen the working tree

Build the candidate path list as the NUL-delimited union of `git ls-files -mo --exclude-standard -z` and `git diff --cached --name-only -z`.
Apply every extension, secret, and size rule to that candidate path list.
Read staged changes, unstaged changes, and untracked files after the branch gate passes.
When the working tree is clean and unpushed commits exist, skip path screening and leave the working tree unchanged.

Screen every candidate path, tracked or untracked, against these patterns:

- Data and artifact extensions (`.csv`, `.parquet`, `.feather`, `.xlsx`, `.db`, `.pkl`, `.joblib`, `.rds`, model binaries) and directories whose path contains a data-like segment (`data`, `models`, `output`, `.ipynb_checkpoints`) — match on path segments, not exact names, so `raw_data/` and `output_v2/` are caught.
- Secret-bearing names (`.env`, `.env.*`, `credentials*`, `*secret*`, `*.pem`, `*.key`).
- Files larger than 5,000,000 bytes, measured for both unstaged and staged candidates with `(git ls-files -mo --exclude-standard -z; git diff --cached --name-only -z) | sort -zu | while IFS= read -r -d '' path; do test -f "$path" && du -b -- "$path"; done`.

Apply the secret rule first when a path matches more than one pattern.

Ask about all flagged paths in one question, through #tool:vscode/askQuestions when you hold it.
Offer a path that matches a secret-bearing name only two resolutions: add it to the repository-root `.gitignore`, or leave it out of every commit group.
Never offer to commit it, and point the owner at environment-based configuration instead.
Offer every other flagged path three resolutions: add it to the repository-root `.gitignore`, commit it deliberately, or leave it out of every commit group.
When the owner chooses `.gitignore` for a path that Git already tracks, state that ignoring alone leaves the file tracked, and stop for the owner to decide whether to untrack it.
Stop until the owner resolves every flagged path.

## Synchronize repository documentation

When the requested work will create one or more commits, read and reconcile `CHANGELOG.md`, `PROJECT-STATUS.md`, and `OPEN-ISSUES.md` before showing the commit plan.

Read the [changelog instruction](../../../com.github.copilot/rules/changelog.instructions.md), [project status instruction](../../../com.github.copilot/rules/project-status.instructions.md), and [open issues instruction](../../../com.github.copilot/rules/open-issues.instructions.md) before editing their corresponding files.

Update `CHANGELOG.md` with the current user-visible results selected for commit.
Apply the changelog instruction by updating, merging, or removing existing `## Unreleased` bullets when the selected changes alter the final result they describe.
Update `PROJECT-STATUS.md` when the selected changes alter the project state, focus, roadmap, or blockers, and refresh its `Updated` date.
Update `OPEN-ISSUES.md` when the selected changes add, resolve, or alter a project decision, missing input, or verified limitation.
Keep `PROJECT-STATUS.md` and `OPEN-ISSUES.md` factual: preserve identifiers and record unresolved behavior with its current rule and closure condition.

Update `README.md` only when the owner selected it or the requested change explicitly alters package documentation; README is not part of this synchronization gate.

Keep each required documentation update in the same commit group as the change it describes.
When one documentation update describes multiple groups, consolidate those related changes into one group or use a separate `docs:` group and state the dependency in the plan.
Leave one of the three required documentation files unchanged only after comparing it with the selected changes and confirming that no fact is stale or missing; record that comparison and result in the final report.

## Show the commit plan

Put two changes in separate commits when either could be reverted without the other.
Use conventional commit messages in the form `type: summary`, and add a `(scope)` only when the summary alone does not identify the area.
Use `feat` and `fix` according to the Conventional Commits specification, and use `docs:`, `chore:`, `refactor:`, or `test:` for other work.

Treat a new `version` value in `plugin.json`, or a new versioned `## [x.y.z]` heading in `CHANGELOG.md`, as release preparation.
Leave those two changes out of every commit group and direct the owner to `publish-plugin`, which owns versioning and the release snapshot.
Commit only edits inside `## Unreleased` through this skill.
Treat an edit inside a versioned changelog entry as release-history maintenance, leave it out of every commit group, and stop for the owner to resolve it outside this skill.

Show the proposed groups, their paths, and their messages once, then continue without waiting for a reply.
When no new commit group is needed, show the unpushed commits and push target once before pushing.
Update the plan in one line when an owner decision from the screen removes a path from it.

The plan is complete only when every path in scope belongs to exactly one group and every group has a message.

## Commit and push

Read the unpushed commits with `git log --oneline @{upstream}..HEAD`.
When any subject starts with `chore(release):`, stop and direct the owner to `publish-plugin`, because that commit belongs to a release and must not reach `origin/develop` through this skill.

Stage each group by naming its paths, and never with `git add -A` or `git add .`.
Create each commit with its planned conventional message.
When a staging command or a commit hook fails, report the command and its output and stop for the owner to decide; never retry with `--no-verify`.

Push the completed commits:

```bash
git push origin develop
```

When the push is rejected because `origin/develop` moved ahead, report the divergence and stop for the owner to choose between `git pull --rebase` and another resolution; never force-push or rewrite history in this skill.
When `origin` is unreachable, report the error and stop with the commits retained locally.

## Verify the result

After the push, read `git status --short --branch` and `git log --oneline -n <number of new commits>`.
Report each commit with its message, the push target, the resolution of every flagged path, and every path left uncommitted.
