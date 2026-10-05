---
name: "Project Status"
description: "Maintain the root project status handoff with verified state, roadmap, decisions, and next action"
applyTo: "PROJECT-STATUS.md"
---

# Project status

Maintain the root-level `PROJECT-STATUS.md` as the operational handoff for the project owner and agents.

## Establish the status

- Read the current `PROJECT-STATUS.md`, project documentation, source configuration, tests, and existing project records before changing the status.
- Treat explicit owner decisions as authoritative for the objective, roadmap, scope, task order, and completion status.
- Treat source files, configuration, tests, and project records as evidence for the current verified state.
- Restrict status evidence to `PROJECT-STATUS.md`, `README.md`, `plugin.json`, `CHANGELOG.md`, `OPEN-ISSUES.md`, the root `.github/copilot-instructions.md`, paths linked by the affected status entry, and source, configuration, or test files directly implicated by the requested status change.
- Ask the owner before writing when the objective, owner, current state, next action, roadmap, task order, scope, or authoritative source cannot be established from evidence.
- Do not ask the owner for facts that the workspace can establish with a read-only check.

Status establishment is complete only when each required field and section has support in the bounded evidence or an explicit owner decision.

## Keep the status format

- Use one level-one heading named `Project Status`.
- Keep these header fields in this order:

	- `State`: `active`, `blocked`, `paused`, or `complete`.
	- `Updated`: the current date in `YYYY-MM-DD` format.
	- `Owner`: the resolved person or team responsible for project decisions.
	- `Objective`: the intended outcome in one sentence.
	- `Current`: verified facts about the present state.
	- `Next`: `None remaining.` when `State` is `complete`; otherwise the exact text and links of the first planned task, excluding its list marker and checkbox.

- Keep these sections in this order:

	1. `Roadmap` for high-level phases and expected outcomes.
	2. `Open Questions` for the index of unresolved project-level issues.
	3. `Planned Tasks` for the ordered near-term queue.

- Use `Open Questions` as an index of every row currently present in `OPEN-ISSUES.md`, including rows labeled `Decision needed`, `Missing input`, and `Verified limitation`.
- Treat `OPEN-ISSUES.md` as canonical for `OI-*` identifiers and lifecycle.
- Link each present issue row once using its canonical `OI-*` identifier as the link text to `OPEN-ISSUES.md`; do not duplicate issue details.
- Synchronize the index additively: add an index item for each canonical row, retain it while that row remains present, and remove it only after the canonical row is removed.
- Mark each roadmap phase with `complete`, `active`, `planned`, `blocked`, or `paused`.
- Use `- No roadmap agreed.` only when the project owner confirms that no roadmap exists.
- Use `- None identified.` under `Open Questions` only when `OPEN-ISSUES.md` has no rows.
- Keep at least one planned task for `active`, `blocked`, and `paused` states.
- Write each non-empty planned task as a sequentially numbered Markdown task-list item, such as `1. [ ]`, `2. [ ]`, or `3. [x]`, and renumber the list after adding or removing a task.
- Make the first planned task the action that resolves a block or resumes work when the state is `blocked` or `paused`.
- Use `- None remaining.` under `Planned Tasks` only when the state is `complete`; in that state, set `Next` to `None remaining.`.

Status format is complete only when all required header fields and sections are present in the stated order, and the complete-state or non-complete-state representation is applied without mixing their values.

## Apply an update

- Preserve valid information outside the requested change.
- Update every affected header field and status section in one edit.
- Read the current date with `date +%F` for every status update and set `Updated` to that output.
- Record verified effects in `Current` before removing completed tasks or resolved questions.
- Keep detailed history and the full backlog in their canonical locations.
- Do not put temporary task detail in `PROJECT-STATUS.md`.
- Do not edit source files to make `PROJECT-STATUS.md` appear consistent.

The update step is complete only when every affected header and section is updated in one edit, `Current` records verified effects, and the complete or non-complete `Next` representation is valid.

## Validate the result

- Verify that the file is at the repository root and every header field is resolved and ordered correctly.
- Verify that `Next` is `None remaining.` and `Planned Tasks` is `- None remaining.` when `State` is `complete`; otherwise verify that `Next` exactly matches the text and links of the first planned task.
- For each value in `State`, `Owner`, `Objective`, and `Current`, identify the supporting path in the bounded evidence or the explicit owner decision; verify that `Updated` equals the output of `date +%F`, and that each roadmap phase, issue-index item, and planned task matches its corresponding evidence.
- Verify that `Open Questions` contains exactly one link whose text is the canonical `OI-*` identifier for every row in `OPEN-ISSUES.md`, and that no index item remains for a canonical row that has been removed.
- Verify that every relative link resolves from `PROJECT-STATUS.md`.
- Verify that the file has LF line endings, no trailing whitespace, and one final newline.
- Report the changed path, resulting `State`, current `Next` action, evidence checked, and every project owner decision that remains open.

The update is complete only when the status describes the verified project state, the open-question index matches the canonical issue rows, every validation check passes, and either `State` is `complete` with `Next` equal to `None remaining.` and `Planned Tasks` equal to `- None remaining.`, or `Next` exactly matches the text and links of the first planned task.
