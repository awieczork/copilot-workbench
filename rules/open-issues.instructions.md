---
name: "Open Issues"
description: "Use when adding, updating, or closing rows in OPEN-ISSUES.md, the register of unresolved decisions, missing inputs, and verified limitations. Supplies the states, the row format, and the closure rules."
applyTo: "OPEN-ISSUES.md"
---

# Open issues

`OPEN-ISSUES.md` is the durable register of the project's unresolved decisions, missing inputs, and verified limitations.

## Classify an issue

- Add an issue only when repository evidence or a user decision shows that it is unresolved.
- Add it only when it affects work beyond the active task, because the [`task-context`](../skills/task-context/SKILL.md) task folder holds the rest.
- Use `Decision needed` for an unresolved user decision, `Missing input` for a working fact that the lowest-cost read-only check could not establish, and `Verified limitation` for a confirmed constraint that still applies.

## Record a row

- Keep one row per issue in a table with the columns `OI`, `Area`, `State`, `Issue`, `Rule until closure`, and `Closure condition`.
- Write each identifier as `OI-{nn}`, and number a new row one above the highest identifier the file has ever held, which `git log -p -- OPEN-ISSUES.md` shows, because an identifier is never reused, even after its row is removed.
- State the issue as one question, missing fact, or verified limitation, give a `Rule until closure` whose effect is observable in the affected work, and give a closure condition that another agent can verify from a user decision or repository evidence.
- Update a row when later evidence changes its issue, rule, state, or closure condition.
- When no issue remains, write `- None.` below the heading instead of an empty table.

## Close a row

- Close `Decision needed` only after an explicit user decision, `Missing input` only after evidence establishes the fact, and `Verified limitation` only after evidence shows that it no longer applies.
- Before removing a row, record its lasting effect in the record that owns it, such as `ARCHITECTURE.md`, a rule, or a skill, because the register keeps only open issues.
- When removing a row, also remove its link from `PROJECT-STATUS.md`, because the link would point at no row.
- When the closure evidence is absent, keep the row.
