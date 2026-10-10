---
name: publish-plugin
description: "Use when the owner runs it to publish a plugin release from `develop` to package-only `main`."
argument-hint: "[release goal or version]"
disable-model-invocation: true
---

# Publish an approved plugin release

Publish from `develop` to package-only `main` only the paths that `bash .github/skills/publish-plugin/scripts/release.sh allowlist` prints.
This skill publishes one release from a clean state and does not resume an interrupted run; when a check finds leftover release state, report the state, the branches and commits that hold it, and the manual recovery it needs, without repairing it.
Ask the owner each question through #tool:vscode/askQuestions .

## Stop on preflight failure

Run `bash .github/skills/publish-plugin/scripts/release.sh preflight` from the repository root.
It checks that `develop` is checked out with a clean working tree and no unfinished operation; fetches `origin`; requires `origin/develop` and `origin/main`, a local `develop` that contains `origin/develop`, no git worktree with `main` checked out, an absent sibling path `<repo>.plugin-worktree`, a local `main` equal to `origin/main` when it exists, and no unpushed `chore(release):` commit; runs `gh auth status`; and runs the package conformance check of `build-plugin`.
It prints one `FAIL:` line per failed check and exits with status 1; stop and report those lines before asking for a version.

## Ask for the version

Read the current `version` from `plugin.json` on `develop`, show it, and ask the owner for the approved semantic version without a leading `v`.
Accept a valid semantic version that has no `v<version>` tag locally or on `origin`, is greater than the newest `v*` tag when one exists, and is not lower than the current version; stop otherwise.

## Draft and approve release notes

Read the [release note rules](references/release-notes.md) before drafting, because they hold the evidence classification and the entry shape.
Run `git diff --name-status origin/main develop -- $(bash .github/skills/publish-plugin/scripts/release.sh allowlist)`, and inspect the changed paths and the behavior they implement.
Draft the versioned entry from the `## Unreleased` section and that diff.

Ask the owner to approve the exact draft, with the proposed version and the complete note body in the question.
Revise the draft when the owner requests a change and ask for approval of the complete replacement.
Stop without release changes when the owner rejects or does not approve the draft.

After approval, set `notes_file` to an unused temporary file outside the repository, write the complete approved versioned entry to it, and require `test -s "$notes_file"` to succeed.

## Prepare the source commit

After both approvals, update only the `version` field in `plugin.json` on `develop` when the approved version differs from the current version.
Apply the approved versioned entry from `notes_file` to `CHANGELOG.md` by the release note rules.
Update `PROJECT-STATUS.md` to the published state by the [project status rule](../../../com.github.copilot/rules/project-status.instructions.md).
Read `git diff -- plugin.json CHANGELOG.md PROJECT-STATUS.md` and require the approved changelog transition, the status update, and, when the version changed, the version bump to be the only content changes.
Stage the changed paths by name, require `git diff --cached --name-status` to list exactly them, and create the local commit `chore(release): prepare v<version>` on `develop`.

## Build and verify the package tree

Run `bash .github/skills/publish-plugin/scripts/release.sh build <version>`.
It creates the sibling git worktree `<repo>.plugin-worktree` on local `main`, from `origin/main` when local `main` is absent, replaces its tree with the allowlist from `develop`, commits `chore(release): publish v<version>`, checks that the snapshot equals `develop` over the allowlist and holds no other path, and prints the snapshot commit.
A non-zero exit prints the failed check.

## Handle pre-publication failure

When a check or command fails after preflight and before the push confirmation, report the failed command, the source commit when present, and every remaining path, then continue to "Clean the plugin git worktree" and stop; create no tag and push nothing.

## Get one push confirmation

Verify that the local `main` tip is the snapshot commit, and create no tag before this confirmation.
Show the owner the version, both commit identifiers, the passing build checks, and ask one question that covers all of these actions:

- create annotated tag `v<version>` on local `main`;
- push `develop`, `main`, and `v<version>` to `origin`;
- create the GitHub release with `gh release create --notes-file`.

When the owner declines, continue to "Clean the plugin git worktree", report the retained local source and snapshot commits with their branches, identifiers, and version, state that a later run stops until the owner resolves them, and do not claim that publication completed.

The confirmation gate is complete only when one explicit approval covers the exact tag, branches, remote, and GitHub release.

## Push and publish

After the confirmation, create the annotated tag on the local `main` commit:

```bash
git tag -a "v<version>" main -m "Release v<version>"
```

Push the branches and the tag as one all-or-nothing update:

```bash
git push --atomic origin develop main "v<version>"
```

Use `--atomic`, because without it a partial failure leaves one branch or the tag pushed and the rest behind.

Create the GitHub release from the approved notes file:

```bash
gh release create "v<version>" \
  --title "v<version>" \
  --notes-file "$notes_file"
```

Do not force-push, move an existing tag, or retry a rejected push automatically.
When a push fails on authentication, report it and leave the GitHub CLI authentication unchanged, because the owner set up the credential helper.
When a tag, push, or GitHub CLI command fails, report the exact completed effects, run "Clean the plugin git worktree", and stop for the owner to decide the next step.

The publication is complete only when the atomic push and the GitHub release report success.

## Clean the plugin git worktree

Remove `notes_file` when it exists.
When `git worktree add` succeeded, run `git -C "$plugin_worktree" status --short --ignored`, where `plugin_worktree` is `"$(git rev-parse --show-toplevel).plugin-worktree"`, and remove the git worktree with `git worktree remove "$plugin_worktree"` when the status is empty; keep the path and stop when the status reports a path or the removal fails.

Run `git status --short --branch`, `git worktree list`, and `git show --stat --oneline main` as the final checks.
Report the published version, the source and snapshot commits when present, the tag, the GitHub release result, and the final git worktree state.
