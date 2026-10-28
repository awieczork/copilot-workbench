# Changelog format

Use Keep a Changelog: `## Unreleased` describes the current user-visible difference from the latest release, not the sequence of commits.
Keep versioned entries unchanged during commit preparation.

Use only sections with bullets, in this order: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
Write one sentence for one distinct result, naming the component or capability first.
Use neutral, present-tense English in the active voice, without `now` or evaluative claims.

Compare existing bullets, the latest versioned entry or release tag, and the staged, unstaged, and untracked changes in the requested group.
Extend an existing bullet for an extended result, combine bullets for one final result, remove superseded results, and keep independent results separate.
Do not include unrelated changes or use the entire working tree as implicit scope.

For release preparation on a cycle, move the completed selected package's Unreleased bullets under `## [MAJOR.MINOR.PATCH] - YYYY-MM-DD`, keep `## Unreleased` above it, and set the matching manifest version before integration.
The root changelog records repository and marketplace results; each package owns its versioned history.
