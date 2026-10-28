---
name: publish-plugin
description: "Use only when the owner explicitly requests preflight or publication of one catalog plugin. Checks one package from clean `main` and selects only its version and changelog. Not for all-plugin releases or package snapshot builds."
argument-hint: "[one explicit plugin name and release request]"
disable-model-invocation: true
---

# Publish one plugin

Prepare or publish exactly one selected catalog plugin from a clean, committed `main` branch.

## Procedure

1. Require one exact plugin name from `.github/plugin/marketplace.json`; refuse an empty catalog, an unlisted name, or an all-plugin request.
2. Run `uv run --no-project .github/skills/build-plugin/scripts/check_package.py` from the repository root.
3. Obtain owner authorization for the repository's normal remote refresh/review and confirm it has updated local `refs/remotes/origin/main`; the helper checks this cached ref only and cannot establish live remote freshness.
4. Run `bash .github/skills/publish-plugin/scripts/release.sh preflight <plugin-name>` from the repository root and stop on any `FAIL:` line.
5. Run `bash .github/skills/publish-plugin/scripts/release.sh notes <plugin-name>` and show the selected package's version, `<plugin-name>/v<version>` tag, and notes for owner review.
6. Obtain explicit owner confirmation naming the selected plugin, version, local tag creation, push of that tag to `origin`, and GitHub release creation before any of those effects.
7. After confirmation, create an unsigned annotated tag on `main` without `--force`, push only that exact tag, and create the GitHub release with `--verify-tag` and the selected package's notes.
8. If tag creation, push, or release creation fails, report the completed effects and stop; never delete, move, force, or silently retry a tag or release.

For the confirmed publication, capture the notes before creating the tag, because the read-only helper rejects a tag that already exists locally:

```bash
plugin='<plugin-name>'
version='<version>'
tag="$plugin/v$version"
notes="$(bash .github/skills/publish-plugin/scripts/release.sh notes "$plugin")" &&
git tag -a "$tag" main -m "Release $plugin v$version" &&
git push origin "$tag" &&
printf '%s\n' "$notes" | gh release create "$tag" --verify-tag --title "$plugin v$version" --notes-file -
```

## Safety and scope

- The helper is read-only and accepts only `preflight <plugin-name>` or `notes <plugin-name>`; it has no default plugin or all-plugin mode.
- Preflight requires current branch `main`, an existing commit, a clean worktree, one listed package, a matching manifest and directory name, a semantic version, the selected package's versioned `CHANGELOG.md` entry, and an unused local tag.
- Version and notes come only from `plugins/<plugin-name>/plugin.json` and `plugins/<plugin-name>/CHANGELOG.md`; another package's version or changelog is never selected.
- The helper checks only local Git refs: main parity uses cached `refs/remotes/origin/main`; it does not fetch or establish live remote freshness, and it does not check remote tag or release state.
- This repository keeps its full tree on `main`; the plugin tag points to a whole-repository commit and is not a filtered package archive.
- The helper does not create commits or tags, push, call GitHub, fetch, switch branches, build snapshots, or claim client installation/runtime compatibility.
- If package changes are not already committed on `main`, stop; this skill does not create commits or move changes between branches.
- Never change credentials or authentication, bypass a Git hook, force-push, or rewrite shared history; on an authentication or hook failure, report the failure and stop.

The release is complete only when the owner-approved tag push and GitHub release both succeed.
