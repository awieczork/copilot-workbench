# Versioned release notes

Prepare the manifest version and matching changelog entry of each package a cycle changes, on that cycle before integration; this is the cycle's release preparation.
Use the committed numeric `MAJOR.MINOR.PATCH` version that the owner selects, greater than the package's version on the integration base and every existing tag of that package; only `agent-team` also inherits legacy `v*` tags.

The selected package's changelog must have exactly one non-empty entry headed `## [MAJOR.MINOR.PATCH] - YYYY-MM-DD`, with `## Unreleased` above it.
Move the package's Unreleased bullets into that entry and leave `## Unreleased` empty above it.
Use only populated Keep a Changelog sections in this order: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
Notes describe the final user-visible changes of that package, not repository maintenance or another package's changes.

The read-only helper selects this entry only; publication does not prepare versions, write notes, or create a release-preparation commit.
