# Project status format

Keep the project's status record short and limited to current and planned work.
Use the owner's objective, scope, and phase order; ask when a missing decision changes the roadmap.
Git and changelogs keep history; temporary task state stays outside this record.

```markdown
# Project status

- State: {active | blocked | paused | complete}
- Updated: {YYYY-MM-DD}
- Objective: {intended outcome}
- Focus: {active phase and its immediate purpose}

## Roadmap

1. {active | planned | blocked | paused} {phase and outcome}
   1. [ ] {next bounded task in the active phase}

## Blockers

- {existing open-issue link and what it blocks, or None}
```

Rewrite the focus for the current phase rather than appending history.
Give task checkboxes only to the active phase; its first unticked task is next.
Remove finished tasks after their lasting facts are in the owning record.
When complete, set state to `complete` and roadmap to `None`.
Do not mark publication complete from static preflight alone.
