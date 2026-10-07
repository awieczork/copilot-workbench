---
name: "Project Status"
description: "Use when updating PROJECT-STATUS.md: the project's state, focus, roadmap with active tasks, and blockers"
applyTo: "PROJECT-STATUS.md"
---

# Project status

`PROJECT-STATUS.md` is the short handoff that tells the owner and any agent where the project stands and what comes next.
Keep it to current and planned work, because git, `CHANGELOG.md`, and the other root records keep the history.

## Format

```markdown
# Project Status

- **State:** {`active` | `blocked` | `paused` | `complete`}
- **Updated:** {today's date from `date +%F`}
- **Owner:** {person responsible for project decisions}
- **Objective:** {the intended outcome in one sentence}
- **Focus:** {one or two sentences: the active phase, why it matters now, and what blocks it}

## Roadmap

1. `{active | planned | blocked | paused}` {phase and its expected outcome}
   1. [ ] {task}

## Blockers

- [OI-{nn}](OPEN-ISSUES.md): {what it blocks}
```

## Update the status

- Take the objective, scope, phase order, task order, and completion from the owner's decisions, and the current state from the repository.
- Ask the owner when the objective, scope, or order cannot be established from either.
- Rewrite `Focus` for the present rather than appending to it, so that it never becomes a history log.
- Give numbered tasks only to the active phase, and add tasks to a planned phase when it becomes active.
- Treat the first unticked task of the active phase as the next action.
- When a task or phase finishes, record its lasting effect in the record that owns it, such as `CHANGELOG.md`, `ARCHITECTURE.md`, or `OPEN-ISSUES.md`, then remove the task or phase.
- Under `Blockers`, link only the `OPEN-ISSUES.md` rows that block an active task, and write `- None.` when nothing blocks.
- When the project is complete, set `State` to `complete` and write `- None remaining.` under `Roadmap`.
- Keep temporary task detail under `.github/context/` instead of this file.
