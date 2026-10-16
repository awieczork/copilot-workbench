---
name: "Changelog Entries"
description: "Use when adding, revising, or reconciling entries in CHANGELOG.md. Supplies the Keep a Changelog sections, the wording, and the reconciliation rules."
applyTo: "CHANGELOG.md"
---

# Changelog entries

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/): `## Unreleased` states the current user-visible difference from the latest release, not a history of commits or intermediate states.

## Write each entry

- Keep only the Keep a Changelog headings that have bullets, in the specification's order.
- Write one bullet, in one sentence, for one distinct user-visible result, and open it with the changed component or capability.
- Name the result a user can do, observe, or rely on after the change, and name a product, path, former component, role, or implementation step only when it is part of that result.
- Write in plain, neutral, present-tense English in the active voice, without `now`, intensifiers, or evaluative adjectives.

```markdown
### Added

- The `explorer` worker locates workspace evidence for one question.
- The Redshift MCP server runs read-only queries.
```

## Reconcile with the current result

- Take the existing bullets and versioned entries from `CHANGELOG.md`, the prior baseline from the latest versioned entry or release tag, and the changes from the paths the current request covers, including their staged, unstaged, and untracked changes.
- When the request names no paths, take every change since the baseline, and state that assumption in your result.
- Compare each proposed bullet with the existing bullets and the baseline before writing it: update a bullet that a later change extends, merge bullets that produce one final result, remove a bullet whose behavior was replaced or no longer appears, and keep separate bullets for independent results.
