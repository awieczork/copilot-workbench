---
name: publish-plugin
description: Publish an approved Agent Plugin release from `develop` to package-only `main`, correct existing release history, reconcile release-state records, and verify the package tree. Use when the owner asks to prepare, publish, or correct a plugin release.
argument-hint: "[release goal or version]"
user-invocable: true
disable-model-invocation: true
---

# Publish an approved plugin release

Prepare and publish one approved plugin release.

Treat `develop` as the source branch and package-only `main` as the user distribution branch.
Publish only this allowlist:

- `.gitignore`
- `CHANGELOG.md`
- `README.md`
- `plugin.json`
- `mcp.json`
- `com.github.copilot/`
- `skills/`

Keep build metadata, local source material, tests, and working output on `develop`.

## Compatibility condition

This workflow assumes a Git repository with a `develop` branch, a configured `origin`, an `origin/main` package branch, authenticated GitHub CLI (`gh`), and an active `main` ruleset enforcing `deletion` and `non_fast_forward`.
Treat the ruleset protection as an environment condition.
Do not replace the condition with a runtime ruleset lookup.
Report a push rejection caused by absent protection and stop publication.

## Stop on preflight failure

1. Read the current branch, working tree state, branch tracking, remotes, and git worktree list.
2. Require the current branch to be exactly `develop`.
3. Require a clean develop working tree with no staged, unstaged, or untracked paths.
4. Require no detached `HEAD`, merge, rebase, cherry-pick, or bisect in progress.
5. Fetch `origin/develop`, `origin/main`, and tags before comparing local refs.
6. Require `origin`, `origin/develop`, and `origin/main` to exist, and require local `develop` to contain `origin/develop`.
7. Require no existing git worktree to have package `main` checked out, and require the sibling path `"$(git rev-parse --show-toplevel).plugin-worktree"` to be absent.
8. When local `main` exists, require it to equal `origin/main`.
9. Require `develop` to have no unpushed commit whose subject starts with `chore(release):`.
10. Require `gh auth status` to succeed.

Stop and report the failed check before asking for a version when any requirement fails.

This skill publishes one release from a clean state and does not resume an interrupted run.
When a later check finds leftover release state, report the state, the branches and commits that hold it, and the manual recovery required.
Do not repair it inside this skill.

The preflight is complete only when every listed condition passes.

## Correct release history

When the request names an existing versioned `CHANGELOG.md` entry or published `v<version>` release, run this path instead of the new-release path.

Read the existing versioned entry and compare it with:

```bash
gh release view "v<version>" --json body --jq .body
```

Draft one corrected component-first entry that preserves the verified user results and the existing version, date, and non-empty subsections.

Ask the owner to approve the exact replacement before changing `CHANGELOG.md`, `main`, or the GitHub Release.

After approval, set `notes_file` to an unused temporary file outside the repository and write the complete approved replacement to it.

Require `test -s "$notes_file"` to succeed before continuing.

Update `CHANGELOG.md` on `develop` and commit it as `docs(release): correct notes for v<version>`.

Build and verify a package-only `main` snapshot from that commit without creating or moving a tag.

After the owner confirms the exact correction, push `develop` and `main`, then update the GitHub Release with:

```bash
gh release edit "v<version>" --notes-file "$notes_file"
```

Do not route a versioned-entry correction through `commit-dev`.

Stop on any failed command and report which branch, release body, or local file was updated.

The release-history path is complete only when `CHANGELOG.md`, package-only `main`, and the GitHub Release carry the same approved correction.

## Ask for the version

Read the current `version` from `plugin.json` on `develop`.
Treat this as the initial release when `origin/main` has no `CHANGELOG.md` or its `CHANGELOG.md` has no versioned `## [x.y.z]` entry, and no local or remote `v<current-version>` tag exists.
Ask the owner with `#tool:vscode/askQuestions` for the approved semantic version.
Show the current version and require the answer without a leading `v`.
For the initial release, accept the current version or a greater version when it is valid semantic versioning and carries no existing `v<version>` tag locally or on `origin`.
For a later release, accept the version only when it is valid semantic versioning, greater than the current version, and carries no existing `v<version>` tag locally or on `origin`.
Stop when the owner does not approve a version or supplies an invalid version, a version below the current version for the initial release, a non-increasing later-release version, or an already tagged version.

Do not edit `plugin.json`, `CHANGELOG.md`, create a tag, or update a branch before the version answer is accepted.

The version gate is complete only when one approved version is recorded for this run.

## Draft and approve release notes

Read [release note rules](references/release-notes.md) before drafting.
Read the [changelog instruction](../../instructions/changelog.instructions.md) before drafting or revising any bullet.
Run `git diff --name-status origin/main..develop` and inspect the changed paths.
Use `origin/main` as the published-state reference, because a local package branch can be absent before the package-tree setup creates it.
Inspect changed paths and the behavior they implement before writing a note.
Read the current `## Unreleased` section in `CHANGELOG.md` as a working description of the current difference, not as a change history.
Consolidate, update, merge, or remove its bullets so that each remaining bullet describes one distinct user-visible result present in the final `origin/main..develop` state.
Classify every user-visible change in the `origin/main..develop` diff as covered by an approved final bullet or explicitly omitted as internal.
Write the draft in English to match this repository's current `CHANGELOG.md` and documentation.
Run the draft checklist in the reference before asking for approval.

Ask the owner with `#tool:vscode/askQuestions` to approve the exact draft.
Include the proposed version and the complete note body in that question.
Revise the draft when the owner requests a change and ask for approval of the complete replacement.
Stop without release changes when the owner rejects or does not approve the draft.

After approval, set `notes_file` to an unused temporary file outside the repository and write the complete approved versioned entry to it, including its version heading, date, non-empty subsections, and bullets.
Require `test -s "$notes_file"` to succeed before continuing.

The notes gate is complete only when the owner has approved the exact entry that will enter the changelog and the GitHub release.

## Prepare the source commit

After both approvals, update only the `version` field in `plugin.json` on `develop` when the approved version differs from the current version.
Apply the approved versioned entry from `notes_file` to `CHANGELOG.md`.
Use the same text in `CHANGELOG.md` and the GitHub Release; do not add a separate introduction, summary, or migration section to either one.
Preserve earlier versioned entries below the new entry and apply the release-note rules for any first-release placeholder.
Keep the entry headings and non-empty sections from the release-note reference.
Run `git status --porcelain` and require `CHANGELOG.md` and, when the version changed, `plugin.json` to be the only modified paths.
Read `git diff -- plugin.json CHANGELOG.md` and require the approved changelog transition and, when applicable, the version bump to be the only content changes.
Stop when another path is modified or the diff carries a change that is neither the approved changelog transition nor the applicable version bump.
When source preparation fails, follow `Handle pre-publication failure` before building the package tree.

Stage `CHANGELOG.md` and, when the version changed, `plugin.json` by name.
Inspect `git diff --cached --name-status` and require exactly the changed paths.
When staging or the commit fails, follow `Handle pre-publication failure` and stop.
Create the local conventional commit `chore(release): prepare v<version>` on `develop`.
Stop and report when the develop working tree is not clean after the commit.
When the post-commit cleanliness check fails, follow `Handle pre-publication failure` and stop.

The source commit is complete only when `develop` contains the approved version and notes, the release changelog has no duplicated `Unreleased` bullets, and `git status --porcelain` on `develop` returns no output.

## Build the package tree in a git worktree

Set `repo_root` to the output of `git rev-parse --show-toplevel`.
Set `plugin_worktree` to `"${repo_root}.plugin-worktree"`, a sibling directory of the repository root.
When local `main` exists, run `git worktree add "$plugin_worktree" main`.
When local `main` is absent, run `git worktree add -b main "$plugin_worktree" origin/main`.

When `git worktree add` fails, remove `notes_file`, report the failed command and the retained source commit, and stop.

In the plugin git worktree, reset the index and the checked-out files to an empty tree:

```bash
empty_tree="$(git mktree </dev/null)"
git -C "$plugin_worktree" read-tree --reset -u "$empty_tree"
```

Restore and stage the allowlist explicitly from `develop`:

```bash
git -C "$plugin_worktree" restore --source=develop --staged --worktree -- \
  .gitignore CHANGELOG.md README.md plugin.json mcp.json com.github.copilot skills
```

Read `git -C "$plugin_worktree" status --short` and require every listed path to belong to the allowlist.
Stage the allowlist by name rather than with `git add`, because `git add` silently skips a path that the copied `.gitignore` matches.
Stop when a path outside the allowlist is staged or when a required allowlisted path cannot be restored.
When a command after `git worktree add` fails, follow `Handle pre-publication failure` before requesting push confirmation.

The package-tree preparation is complete only when the plugin git worktree contains the explicitly staged allowlist and no other staged path.

## Verify the package tree

Commit the staged snapshot in the plugin git worktree as `chore(release): publish v<version>`.
Before any push, compare the candidate commit with `develop` over the allowlist:

```bash
git -C "$plugin_worktree" diff --quiet develop HEAD -- \
  .gitignore CHANGELOG.md README.md plugin.json mcp.json com.github.copilot skills
```

Then enumerate every file in the candidate tree and reject any path outside the allowlist:

```bash
git -C "$plugin_worktree" ls-tree -r --name-only HEAD
```

Check every path the second command prints against the allowlist above.
Stop publication when the first command exits non-zero or the second prints a path outside the allowlist.
When tree verification fails, follow `Handle pre-publication failure` before stopping.
Both commands read the committed candidate through `HEAD`, so neither reports uncommitted working-tree state.

The tree verification is complete only when `git diff --quiet` exits zero and every printed path matches the allowlist.

## Handle pre-publication failure

When source preparation fails, including a failed post-commit cleanliness check, run `git status --short`, report the failed command and every remaining path, and remove `notes_file`.
Leave the versioned files on disk for owner resolution.
Do not push them with `commit-dev`.
Stop until the owner resolves the failure and the main working tree is clean.

When a command after `git worktree add` fails before the push confirmation, remove `notes_file` and run `git -C "$plugin_worktree" status --short`.
Remove the plugin git worktree when that status is empty.
When the status is not empty, stop and report the path for manual cleanup.
Do not continue to tag or push after a failed command.

Failure handling is complete only when the failure, remaining paths, and cleanup result are reported.

## Get one push confirmation

Verify that the local package `main` tip is the candidate commit.
Create no tag before this confirmation.

Show the owner the version, both commit identifiers, the two passing tree checks, and the exact publication actions.
Ask one question with `#tool:vscode/askQuestions` that covers all of these actions:

- create annotated tag `v<version>` on package `main`;
- push `develop`, `main`, and `v<version>` to `origin`;
- create the GitHub release with `gh release create --notes-file`.
- after those effects succeed, reconcile `README.md` and `PROJECT-STATUS.md`, commit the records on `develop`, and push a second package-only `main` snapshot without creating a new tag.

When the owner declines, continue to Clean the plugin git worktree.
Report the retained local source and package commits, their branches, identifiers, and version, and state that a later run stops until the owner resolves them.
Do not claim that publication completed.

The confirmation gate is complete only when one explicit approval covers the exact tag, branches, remote, and GitHub release.

## Push and publish

After the confirmation, create the annotated tag on the package `main` commit:

```bash
git tag -a "v<version>" main -m "Release v<version>"
```

Push the branches and the tag as one all-or-nothing update:

```bash
git push --atomic origin develop main "v<version>"
```

Use `--atomic`, because without it a partial failure leaves one branch or the tag pushed and the rest behind.

Create the GitHub release from the approved temporary notes file:

```bash
gh release create "v<version>" \
  --title "v<version>" \
  --notes-file "$notes_file"
```

Omit `--target`, because the tag already exists on `origin` at this point and `gh` ignores the flag for an existing tag.

Stop on any non-zero tag, push, or GitHub CLI result.
Do not force-push, move an existing tag, or retry a rejected push automatically.
Report the exact completed effects when a later command fails, and stop for the owner to decide the next step.
Continue to Clean the plugin git worktree after recording the failed result.

The initial publication is complete only when both branch pushes, the new tag, and the GitHub release report success.

## Reconcile release state

After the initial publication reports success, update `README.md` and `PROJECT-STATUS.md` to the published state.

Use the project status instruction for `PROJECT-STATUS.md` and remove pre-release claims such as `in preparation` or `no plugin version has been released`.

Keep `OPEN-ISSUES.md` unchanged unless the release itself resolved a recorded issue; remove a resolved issue only under the open-issues instruction.

Commit the record updates on `develop` as `docs: record v<version> publication`.

Reset the existing plugin worktree and restore the package allowlist from the new `develop` commit.

Verify that the resulting package-only snapshot differs from the previously published `main` only by the approved release-state metadata.

Commit the second snapshot as `chore(release): sync v<version> publication` and push `develop` and `main` without creating or moving a tag.

Stop and report the exact branch, snapshot, or record state when a post-publication reconciliation command fails.

The full publication workflow is complete only when the release effects and the post-publication record synchronization both succeed.

## Clean the plugin git worktree

Remove the temporary notes file once the run reaches this section by any path, unless an earlier failure branch already removed it.
Run `git -C "$plugin_worktree" status --short --ignored` and require no output.
Remove the plugin git worktree with `git worktree remove "$plugin_worktree"` when that status is empty.
Keep the git worktree path and stop when the status reports a path or the removal fails.
Skip both removals when `git worktree add` never succeeded.

Run `git status --short --branch`, `git worktree list`, and `git show --stat --oneline main` as the final checks, after the git worktree is gone.

Report the published version, the source and snapshot commits when present, the tag, the GitHub release result, and the final git worktree state.
After a successful publication, remind the owner to tell the users about the release and to recommend that they check for an update.

Cleanup is complete only when the temporary plugin git worktree is absent, the temporary notes file is absent, and the three final checks have been run and reported.
