---
name: "Changelog Entries"
description: "Use when adding, revising, or reconciling the `## Unreleased` entries in CHANGELOG.md. Supplies the wording, category, and reconciliation rules. Not for a versioned release entry."
applyTo: "CHANGELOG.md"
---

# Changelog entries

`## Unreleased` states the current user-visible difference from the latest release, not a history of commits or intermediate states.

## Write each bullet

- Write one bullet, in one sentence, for one distinct user-visible result.
- Name the capability or behavior a user can do, observe, or rely on after the change, rather than the implementation step.
- Include a product name, command, path, or configuration value only when it is part of the user's visible result.
- Write in plain English, the past tense, and the active voice, and name the changed component or capability right after the opening verb.
- Start every bullet with `Added` for a capability the latest release did not provide, `Changed` for altered behavior, output, usage, or scope, including a capability removed without replacement, or `Fixed` for a user-visible defect the current change set corrects.
- Describe a replacement by the result now available, and name a former component only when migration or discoverability needs its name.
- Leave out internal refactors, branch operations, and repository maintenance that change no user-visible result, and leave out role or person names unless they are part of the capability.
- Use neutral, verifiable wording, without `now`, superlatives, intensifiers, or evaluative adjectives.

Preferred:

```text
- Added the `explorer` worker for locating workspace evidence for one question.
- Added the Redshift MCP server for read-only queries.
```

Avoid:

```text
- Added workspace exploration through the `explorer` worker.
- Implemented the `ReportExporter` refactor for CSV support.
- Promoted the `login` component with improved error handling.
```

## Reconcile with the current result

- Take the existing bullets and versioned entries from `CHANGELOG.md`, the prior baseline from the latest versioned entry or release tag, and the changes from the paths the current request covers, including their staged, unstaged, and untracked changes.
- When the baseline or the paths the current request covers are unavailable, report `Missing input` instead of inferring it, because a guessed baseline turns `Changed` into `Added` or the reverse.
- Compare each proposed bullet with the existing bullets and the baseline before writing it: update a bullet that a later change extends, merge bullets that produce one final result, remove a bullet whose behavior was replaced or no longer appears, and keep separate bullets for independent results.
