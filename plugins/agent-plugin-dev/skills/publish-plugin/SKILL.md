---
name: publish-plugin
description: "Use only when the owner explicitly requests preflight or publication of one catalog plugin. Checks one package from clean `main` and selects only its version and changelog. Not for all-plugin releases or package snapshot builds."
argument-hint: "[one explicit plugin name and release request]"
disable-model-invocation: true
---

# Publish one plugin

Prepare or publish exactly one selected catalog plugin from a clean, committed `main` branch.

Prepare versions and versioned notes on the cycle before integration, using the bundled [versioned-notes format](references/versioned-notes.md).
If preparation changes the project roadmap, use [the status format](references/project-status.md) on that cycle; do not record a release as complete before publication is verified.
This publication procedure does not prepare a commit or change records on `main`.

## Procedure

1. Require one exact plugin name from `.github/plugin/marketplace.json`; refuse an empty catalog, an unlisted name, or an all-plugin request.
2. Use [build-plugin](../build-plugin/SKILL.md) for static package validation of the target repository; stop on a reported failure.
3. Obtain owner authorization for the repository's normal remote refresh/review and confirm it has updated local `refs/remotes/origin/main`; the helper checks this cached ref only and cannot establish live remote freshness.
4. Resolve [release.sh](scripts/release.sh) from this skill's loaded location, then run `bash` with its absolute path and `preflight <plugin-name>` from the target repository root. Stop on failure.
5. Run the same installed wrapper with `notes <plugin-name>` and show the selected version, `<plugin-name>/v<version>` tag, full `main` commit ID, and package-local notes for review.
6. With authorized read-only remote access, require live remote `main` to equal the reviewed commit. Query remote tags successfully and require the selected tag to be absent and the version to exceed every selected-package version tag; include legacy `vMAJOR.MINOR.PATCH` tags only for `agent-team`. Establish release absence through a successful complete release listing, not a failed query or an incomplete first page. Stop if freshness, identity, or absence is unknown. Obtain explicit owner confirmation naming the plugin, version, reviewed commit, local tag creation, that tag's push, and GitHub release creation before any publication effect.
7. Recheck clean `main`, commit equality, and tag/release absence after confirmation. Create an annotated tag on that recorded full commit ID without `--force`, push only the exact tag with automatic tag following disabled, and create the GitHub release with `--verify-tag` and the reviewed package notes.
8. If tag creation, push, or release creation fails, report the completed effects and stop; never delete, move, force, or silently retry a tag or release.

For the confirmed publication, capture the notes before creating the tag, because the read-only helper rejects a tag that already exists locally:

```bash
plugin='<plugin-name>'
version='<version>'
tag="$plugin/v$version"
release_script='<absolute path to this installed skill>/scripts/release.sh'
release_commit='<reviewed full commit ID>'
notes="$(bash "$release_script" notes "$plugin")" &&
git tag -a "$tag" "$release_commit" -m "Release $plugin v$version" &&
git -c push.followTags=false push origin "refs/tags/$tag:refs/tags/$tag" &&
printf '%s\n' "$notes" | gh release create "$tag" --verify-tag --title "$plugin v$version" --notes-file -
```

## Safety and scope

- The helper is read-only and accepts only `preflight <plugin-name>` or `notes <plugin-name>`; it has no default plugin or all-plugin mode.
- Preflight requires current branch `main`, an existing commit, a clean worktree without an unfinished operation, one listed package, matching manifest and directory names, numeric `MAJOR.MINOR.PATCH`, a strictly increasing version, selected package versioned notes, and an unused local tag. Version ordering includes legacy `v*` tags only for `agent-team`.
- Version and notes come only from `plugins/<plugin-name>/plugin.json` and `plugins/<plugin-name>/CHANGELOG.md`; another package's version or changelog is never selected.
- The helper checks only local Git refs: main parity uses cached `refs/remotes/origin/main`; it does not fetch or establish live remote freshness, and it does not check remote tag or release state.
- This repository keeps its full tree on `main`; the plugin tag points to a whole-repository commit and is not a filtered package archive.
- The helper does not create commits or tags, push, call GitHub, fetch, switch branches, build snapshots, or claim client installation/runtime compatibility.
- If package changes are not already committed on `main`, stop; this skill does not create commits or move changes between branches.
- Never change credentials or authentication, bypass a Git hook, force-push, or rewrite shared history; on an authentication or hook failure, report the failure and stop.

The release is complete only when the owner-approved tag push and GitHub release both succeed.

Run the [helper tests](tests/test_release_helper.py) with `uv run --no-project python -m unittest discover -s` followed by this skill's absolute test-directory path.
The tests use disposable local repositories and do not test live service permissions or publication.
