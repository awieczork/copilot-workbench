# Publish the reviewed package

Use the plugin, version, full commit ID, and package-local notes reviewed during preflight.
Run the following procedure from the target repository root only for an explicit publication request.

## Confirm and publish

1. With authorized read-only remote access, require live remote `main` to equal the reviewed commit. Query remote tags successfully and require the selected tag to be absent and the version to exceed every selected-package version tag; include legacy `vMAJOR.MINOR.PATCH` tags only for `agent-team`. Establish release absence through a successful complete release listing, not a failed query or an incomplete first page. Stop if freshness, identity, or absence is unknown.
2. Obtain explicit owner confirmation naming the plugin, version, reviewed commit, local tag creation, that tag's push, and GitHub release creation before any publication effect.
3. Recheck clean `main`, commit equality, and tag/release absence after confirmation. Create an annotated tag on that recorded full commit ID without `--force`, push only the exact tag with automatic tag following disabled, and create the GitHub release with `--verify-tag` and the reviewed package notes.
4. If tag creation, push, or release creation fails, report the completed effects and stop; never delete, move, force, or silently retry a tag or release.

## Commands after confirmation

Resolve the installed `publish-plugin` skill directory, not this reference's directory, for `release_script`.
Capture the notes before creating the tag, because the read-only helper rejects a tag that already exists locally:

```bash
plugin='<plugin-name>'
version='<version>'
tag="$plugin/v$version"
release_script='<absolute path to the installed publish-plugin skill>/scripts/release.sh'
release_commit='<reviewed full commit ID>'
notes="$(bash "$release_script" notes "$plugin")" &&
git tag -a "$tag" "$release_commit" -m "Release $plugin v$version" &&
git -c push.followTags=false push origin "refs/tags/$tag:refs/tags/$tag" &&
printf '%s\n' "$notes" | gh release create "$tag" --verify-tag --title "$plugin v$version" --notes-file -
```
