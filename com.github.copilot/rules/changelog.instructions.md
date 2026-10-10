---
name: "Changelog Entries"
description: "Use when adding, revising, or reconciling entries in CHANGELOG.md. Supplies the Keep a Changelog sections, the wording, and the reconciliation rules."
applyTo: "CHANGELOG.md"
---

# Changelog entries

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/): `## Unreleased` states the current user-visible difference from the latest release, not a history of commits or intermediate states.

## Write each entry

- Group the bullets under the type headings `### Added`, `### Changed`, `### Deprecated`, `### Removed`, `### Fixed`, and `### Security`, in that order, keeping only the headings that have bullets.
- File a capability the latest release did not provide under `Added`, altered behavior, output, usage, or scope under `Changed`, a capability removed without replacement under `Removed`, and a user-visible defect the current change set corrects under `Fixed`.
- Write one bullet, in one sentence, for one distinct user-visible result, and open it with the changed component or capability.
- Name the capability or behavior a user can do, observe, or rely on after the change, rather than the implementation step.
- Include a product name, command, path, or configuration value only when it is part of the user's visible result.
- Write in plain English, the present tense, and the active voice.
- Describe a replacement by the result now available, and name a former component only when migration or discoverability needs its name.
- Leave out internal refactors, branch operations, and repository maintenance that change no user-visible result, and leave out role or person names unless they are part of the capability.
- Use neutral, verifiable wording, without `now`, superlatives, intensifiers, or evaluative adjectives.

```markdown
### Added

- The `explorer` worker locates workspace evidence for one question.
- The Redshift MCP server runs read-only queries.
```

## Reconcile with the current result

- Take the existing bullets and versioned entries from `CHANGELOG.md`, the prior baseline from the latest versioned entry or release tag, and the changes from the paths the current request covers, including their staged, unstaged, and untracked changes.
- When no release exists yet, treat the baseline as empty, so that every bullet goes under `### Added`.
- When the paths the current request covers are unavailable, report `Missing input` instead of inferring them, because a guessed change set misfiles bullets.
- Compare each proposed bullet with the existing bullets and the baseline before writing it: update a bullet that a later change extends, merge bullets that produce one final result, remove a bullet whose behavior was replaced or no longer appears, and keep separate bullets for independent results.
