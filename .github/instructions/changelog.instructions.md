---
name: "Changelog Entries"
description: "Standards for writing clear, user-facing entries in CHANGELOG.md"
applyTo: "CHANGELOG.md"
---

# Changelog entries

Use this instruction to reconcile `## Unreleased` and its bullets in `CHANGELOG.md`.
Treat `## Unreleased` as the current user-visible difference from the latest release, not as a history of commits or intermediate implementation states.
When preparing a versioned entry or a GitHub Release body, read the [release-note rules](../skills/publish-plugin/references/release-notes.md) before handing off that work; the handoff is complete only when their release-note checklist passes.

## Name the component and result

- Write one bullet for one distinct user-visible result.
- Lead with what a user can do, observe, or rely on after the change.
- Name the capability or behavior instead of the internal implementation step.
- Include a product name, command, path, or configuration value only when it is part of the user's visible result.
- Keep each bullet to one sentence.

This section is complete only when every bullet under `## Unreleased` states one distinct user-visible result and uses one sentence.

## Use consistent language

- Write in plain English and the past tense.
- Start every bullet under `## Unreleased` with `Added`, `Changed`, or `Fixed`.
- Use `Added` only for a new capability or workflow that the latest release baseline did not provide.
- Use `Changed` for altered behavior, output, usage, a removed capability without a replacement, or an existing component whose behavior or scope changed.
- Use `Fixed` only for a user-visible defect corrected by the current change set.
- Use active voice and name the changed component or capability after the opening verb.
- Omit a role or person name unless it is part of the user-facing capability.
- Describe a replacement by the available user result.
- Mention a former component only when migration or user discoverability requires its name.
- Describe an internal refactor with `Changed` only when it affects user-visible behavior or usage; otherwise omit it from `## Unreleased`.
- Omit branch operations and repository maintenance unless they change a user-visible result.
- Use neutral, verifiable wording.
- Omit `now`, superlatives, intensifiers, and evaluative adjectives.

This section is complete only when every bullet under `## Unreleased` uses plain English, past tense, active voice, and the category that matches its user-visible result.

## Prefer concrete phrasing

Preferred:

```text
- Added the `analyst` agent with an exploration-first workflow for evidence-backed data-science tasks and SQL Server exploration.
- Added the Redshift MCP Server for read-only queries.
```

Avoid:

```text
- Added SQL Server exploration through the `analyst` agent.
- Implemented the `ReportExporter` refactor for CSV support.
- Promoted the `login` component with improved error handling.
```

The preferred form states the user-facing result. The avoided form describes internal status or implementation history.

## Reconcile current results

Use these repository-visible sources as the authoritative reconciliation evidence:

- The current `CHANGELOG.md` provides the existing `## Unreleased` bullets and versioned entries.
- A latest released versioned entry or tag provides the prior release baseline.
- For an Unreleased update, the governed worktree change set is the path set explicitly selected for the current operation; inspect staged, unstaged, and untracked changes for those paths.
- For a release comparison, use the release evidence defined by the linked release-note rules.

When classifying a result as new, changed, or fixed against a previous release, require a latest released versioned entry or tag as the prior baseline.
When no versioned entry or local or remote release tag exposes that baseline, report `Missing input` and do not infer it.
When preparing an Unreleased update, use the governed worktree change set to identify current changed paths and user-visible results.
When no path set is explicitly selected for an Unreleased update, report `Missing input` and do not infer it.
When the governed worktree change set is unavailable, report `Missing input` and do not infer it.

- Compare each proposed bullet with the existing `## Unreleased` bullets and the latest release baseline before adding or revising it.
- Update an existing bullet when a later change extends or clarifies the same user result.
- Merge bullets when separate development changes produce one final user result.
- Remove a bullet when a later change replaces the described behavior or when the current evidence no longer exposes that result.
- Keep separate bullets when users receive independent capabilities or outcomes.

Reconciliation is complete only when every current user-visible result in the authoritative reconciliation evidence has exactly one distinct bullet under `## Unreleased`, every remaining bullet is supported by that evidence, and no bullet describes an intermediate or superseded state.
