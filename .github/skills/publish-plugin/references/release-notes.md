# Release note rules

## Prepare the release body

Write the entry by the [changelog rule](../../../../com.github.copilot/rules/changelog.instructions.md), and treat the current `## Unreleased` bullets as working material to update, merge, or remove before approval.
Use one approved, final-state entry, unchanged, as both the versioned `CHANGELOG.md` entry and the GitHub Release body.

## Verify release evidence

- Verify every technical detail against the release diff that `publish-plugin` runs before writing it.
- Classify every changed path and user-visible capability in that diff as covered by an approved bullet or as an internal change with no changelog entry, and state the classification for every omitted change in the approval question.
- Resolve each user-visible capability into one approved final-state bullet, and remove intermediate or superseded states.
- Exclude a change that alters no command, path, output, or message the user meets.
- Leave no TODO, placeholder, or unverified claim in the approved body.

## Shape the versioned entry

```markdown
## [<version>] - <YYYY-MM-DD>

### Added

- The `explorer` worker locates workspace evidence for one question.
```

Place the newest version entry above previous entries, move the approved entry out of `## Unreleased`, and keep an empty `## Unreleased` heading for future changes.
