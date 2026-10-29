---
name: publish-plugin
description: "Use only when the owner explicitly requests preflight or publication of one catalog plugin. Checks one package from clean `main` and selects only its version and changelog. Not for all-plugin releases or package snapshot builds."
argument-hint: "[one explicit plugin name and release request]"
disable-model-invocation: true
---

# Publish one plugin

Check readiness or publish exactly one selected catalog plugin from a clean, committed `main` branch.
As a subagent, return required owner questions to the delegating agent.

Prepare versions and versioned notes on the cycle before integration, using the bundled [versioned-notes format](references/versioned-notes.md).
If preparation changes the project roadmap, use [the status format](references/project-status.md) on that cycle; do not record a release as complete before publication is verified.
This publication procedure does not prepare a commit or change records on `main`.

## Procedure

1. Require one exact plugin name from `.github/plugin/marketplace.json`; refuse an empty catalog, an unlisted name, or an all-plugin request.
2. Resolve the [package checker](../build-plugin/scripts/check_package.py) from this skill's loaded location, then run `uv run --no-project` with its absolute path from the target repository root. Stop on failure; this is static validation, not the `build-plugin` authoring workflow.
3. Obtain owner authorization for `git fetch origin` and review the fetched state before using cached `refs/remotes/origin/main`; the helper checks this cached ref only and cannot establish live remote freshness.
4. Resolve [release.sh](scripts/release.sh) from this skill's loaded location, then run `bash` with its absolute path and `preflight <plugin-name>` from the target repository root. Stop on failure.
5. Run the same installed wrapper with `notes <plugin-name>` to capture the package-local notes. Read the version from the selected package's manifest and resolve the current full commit ID with `git rev-parse --verify HEAD^{commit}`. Show that version, `<plugin-name>/v<version>` tag, full commit ID, and captured notes for review. For a preflight-only request, report local checks and any unverified remote state, then stop without requesting publication permissions.
6. For an explicit publication request, read [publication](references/publication.md) after preflight and before remote publication checks or effects. Require confirmation naming local tag creation, that exact tag's push, and GitHub release creation; preflight alone authorizes none of them.

## Read-only helper

The [wrapper](scripts/release.sh) requires Bash and `uv`; its Python helper requires Python 3.11+ and Git.
Run it from the target repository root with exactly `preflight <plugin-name>` or `notes <plugin-name>`; neither action has a default plugin or all-plugin mode.
Both actions enforce the same checks below.
`preflight` prints one status line with the selected plugin and version, local tag availability, and cached-main parity.
`notes` prints only the selected versioned notes; its output is not capped.
Exit `0` means checks passed; exit `2` means invalid arguments or plugin-name syntax, and other validation failures exit `1` with `FAIL: ...` on standard error.

- Require current branch `main`, an existing commit, a clean worktree without an unfinished operation, one listed package, matching manifest and directory names, numeric `MAJOR.MINOR.PATCH`, a strictly increasing version, selected package versioned notes, and an unused local tag. Version ordering includes legacy `v*` tags only for `agent-team`.
- Version and notes come only from `plugins/<plugin-name>/plugin.json` and `plugins/<plugin-name>/CHANGELOG.md`; another package's version or changelog is never selected.
- The helper checks only local Git refs: main parity uses cached `refs/remotes/origin/main`; it does not fetch or establish live remote freshness, and it does not check remote tag or release state.
- The helper does not create commits or tags, push, call GitHub, fetch, switch branches, build snapshots, or claim client installation/runtime compatibility.

When changing the helper, run [its tests](tests/test_release_helper.py) with `uv run --no-project python -m unittest discover -s` followed by this skill's absolute test-directory path.
The tests use disposable local repositories and do not test live service permissions or publication.

## Safety and scope

- This repository keeps its full tree on `main`; the plugin tag points to a whole-repository commit and is not a filtered package archive.
- If package changes are not already committed on `main`, stop; this skill does not create commits or move changes between branches.
- Never change credentials or authentication, bypass a Git hook, force-push, or rewrite shared history; on an authentication or hook failure, report the failure and stop.

## Completion

A preflight request is complete when the selected package's checks and notes are reported without publication effects.
A publication request is complete only when the owner-approved tag push and GitHub release both succeed.

```markdown
- Plugin and version: {selected package and version}
- Commit: {reviewed full commit ID}
- Checks: {static, local preflight, and authorized remote results; unresolved checks}
- Tag creation and push: {exact tag and completed effects | not requested}
- GitHub release: {verified URL | not requested | failure and completed effects}
```
