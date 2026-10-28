# Versioned release notes

Prepare the selected package's manifest version and matching changelog entry on its cycle before integration.
Use the committed numeric `MAJOR.MINOR.PATCH` version, greater than that package's existing version tags; only `agent-team` also inherits legacy `v*` tags.

The selected package's changelog must have exactly one non-empty entry headed `## [MAJOR.MINOR.PATCH] - YYYY-MM-DD`, with `## Unreleased` above it.
Use only populated Keep a Changelog sections in this order: `Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`.
Notes describe the final user-visible changes of that package, not repository maintenance or another package's changes.

The read-only helper selects this entry only; publication does not prepare versions, write notes, or create a release-preparation commit.
