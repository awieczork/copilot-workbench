---
name: "Project Status"
description: "Use when updating PROJECT-STATUS.md, the project's state, focus, roadmap, and blockers. Supplies the format and the update rules. Not for task-folder state or history."
applyTo: "PROJECT-STATUS.md"
---

# Project status

`PROJECT-STATUS.md` is the short handoff that tells the user and any agent where the project stands and what comes next.
Keep it to current and planned work, because git, `CHANGELOG.md`, and the other root records keep the history.

## Format

```markdown
# Project status

- **State:** {`active` | `blocked` | `paused` | `complete`}
- **Updated:** {today's date as YYYY-MM-DD}
- **Objective:** {the intended outcome in one sentence}
- **Focus:** {one or two sentences: the active phase and why it matters now}

## Roadmap

1. `{active | planned | blocked | paused}` {phase and its expected outcome}
   1. [ ] {task}

## Blockers

- [OI-{nn}](OPEN-ISSUES.md): {what it blocks}
```

## Update the status

- Take the objective, scope, phase order, task order, and completion from the user's decisions, and the current state from the repository.
- When neither establishes the objective, scope, or order, ask the user, or return the question to the delegating agent when you run as a subagent, because a guessed roadmap misdirects every later task.
- Rewrite `Focus` for the present rather than appending to it, so that it never becomes a history log.
- Give numbered tasks only to the active phase, and add tasks to a planned phase when it becomes active.
- Treat the first unticked task of the active phase as the next action.
- When a task or phase finishes, record its lasting effect in the record that owns it, such as `CHANGELOG.md` or `ARCHITECTURE.md`, then remove the task or phase.
- Under `Blockers`, link only the `OPEN-ISSUES.md` rows that block an active task, and write `- None.` when nothing blocks.
- When the project is complete, set `State` to `complete` and write `- None.` under `Roadmap`.
- Keep temporary task detail in the task folder that the `task-context` skill keeps, instead of in this file.
