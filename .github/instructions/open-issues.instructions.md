---
name: "Open Issues"
description: "Use when adding, updating, or closing rows in OPEN-ISSUES.md, the register of unresolved decisions, missing inputs, and verified limitations. Supplies the states, the row format, and the closure rules."
applyTo: "OPEN-ISSUES.md"
---

# Open issues

`OPEN-ISSUES.md` is the durable register of the project's unresolved decisions, missing inputs, and verified limitations.
Keep uncertainty that matters only to the active task in its task folder, following the [`task-context`](../../skills/task-context/SKILL.md) skill.

## Classify an issue

- Add an issue only when it affects work beyond the active task or needs a durable owner decision or verified limitation, and only when repository evidence or an owner decision shows that it is unresolved.
- Use `Decision needed` for an unresolved owner decision, `Missing input` for a working fact that the lowest-cost read-only check could not establish, and `Verified limitation` for a confirmed constraint that still applies.
- Treat an explicit owner decision as authoritative.

## Record a row

- Keep one row per issue in a table with the columns `OI`, `Area`, `State`, `Issue`, `Rule until closure`, and `Closure condition`.
- Number a new row one above the highest identifier the file has ever held, which `git log -p -- OPEN-ISSUES.md` shows, because an identifier is never reused, even after its row is removed.
- State the issue as one question, missing fact, or verified limitation, give a `Rule until closure` whose effect is observable in the affected work, and give a closure condition that another agent can verify from an owner decision or repository evidence.
- Update a row when later evidence changes its issue, rule, state, or closure condition.
- When no issue remains, write `- None identified.` below the heading instead of an empty table.
- Link a row from `PROJECT-STATUS.md` only while it blocks an active task.

## Close a row

- Close `Decision needed` only after an explicit owner decision, `Missing input` only after evidence establishes the fact, and `Verified limitation` only after evidence shows that it no longer applies.
- Before removing a row, record its lasting effect in the record that owns it, such as `ARCHITECTURE.md`, a rule, or a skill, because the register keeps only open issues.
- When the closure evidence is absent, keep the row, and update its rule or closure condition as the evidence changes.
