---
name: "Open Issues"
description: "Maintain the repository register of unresolved decisions, missing inputs, and verified limitations"
applyTo: "OPEN-ISSUES.md"
---

# Open issues

Maintain the root-level `OPEN-ISSUES.md` as the durable register of unresolved project decisions, missing inputs, and verified limitations.

## Establish bounded evidence

Before changing `OPEN-ISSUES.md`, read this bounded pre-change evidence set:

- `OPEN-ISSUES.md`.
- `PROJECT-STATUS.md`.
- `.github/copilot-instructions.md`.
- Source files directly implicated by the proposed issue.
- The applicable task state under `.github/context/active/`, when present; follow the [`task-context`](../../skills/task-context/SKILL.md) skill for that state.

Run the lowest-cost read-only check that could establish each proposed working fact before classifying it as `Missing input`.
Classify the fact as `Missing input` only when that check does not establish it.

**Completion criterion:** Every applicable source in the bounded evidence set has been read, and every proposed `Missing input` has a completed lowest-cost read-only check that did not establish the fact.

## Classify and promote unresolved work

- Keep uncertainty that is local to the active task in `.github/context/active/`.
- Promote task uncertainty to `OPEN-ISSUES.md` when it affects project work beyond the active task or requires a durable owner decision or verified limitation.
- Treat an explicit owner decision as authoritative.
- Classify a missing fact reserved for the owner as `Decision needed`.
- Classify a working premise as `Missing input` only after the required read-only check does not establish it.
- Record an issue only when repository evidence or an owner decision shows that it remains unresolved.

**Completion criterion:** Every unresolved item is either task-local state with no project-level effect or one project-level row in `OPEN-ISSUES.md` with exactly one of the three permitted states.

## Record active rows

- Use one row for one unresolved issue.
- Use a Markdown table with the columns `OI`, `Area`, `State`, `Issue`, `Rule until closure`, and `Closure condition`.
- Assign a stable identifier in the form `OI-01`, `OI-02`, and so on.
- Never reuse an issue identifier, including after its row is removed.
- Treat every row currently present in `OPEN-ISSUES.md` as an active row.
- State the issue as one question, missing fact, or verified limitation.
- State the `Rule until closure` and make its effect observable in the affected work.
- State a closure condition that another agent can verify from an owner decision or repository evidence.
- Use `Decision needed` for an unresolved owner decision, `Missing input` for an unavailable working fact, and `Verified limitation` for a confirmed constraint that remains relevant.
- Update an existing row when later evidence changes its issue, rule, state, or closure condition.
- Remove a resolved row after recording its effect in `PROJECT-STATUS.md` or the canonical source.
- When no unresolved issue remains, write `- None identified.` below the `# Open Issues` heading instead of keeping an empty table.

**Completion criterion:** Every active row has one never-reused identifier, one permitted state, one concrete issue, one `Rule until closure`, and one checkable closure condition.

## Keep ownership and scope

- Keep all unresolved project-level decisions, missing inputs, and verified limitations in `OPEN-ISSUES.md`.
- Keep temporary task state under `.github/context/active/` and use the [`task-context`](../../skills/task-context/SKILL.md) skill for that state.
- Use `PROJECT-STATUS.md` only to index active issue identifiers and summarize the resulting verified project state.
- Use `canonical source` for the project file that carries the effect of a resolved decision, established input, or limitation that no longer requires an active row.
- Do not add a speculative issue, a resolved issue, or an issue whose only evidence is an unverified assumption.

**Completion criterion:** Every unresolved project-level item has exactly one active row in `OPEN-ISSUES.md`, every task-local item remains in task state, and each resolved effect is recorded in its canonical source.

## Close active rows

Close an active row only with the evidence required by its state:

- Close `Decision needed` only after an explicit owner decision.
- Close `Missing input` only after repository or other read-only evidence establishes the missing fact.
- Close `Verified limitation` only after evidence shows that the limitation no longer applies or that its durable effect has moved to the canonical source.

When the required evidence is absent, keep the active row and update its `Rule until closure` or `Closure condition` when the evidence changes.
Record the resulting effect in `PROJECT-STATUS.md` or the canonical source before removing the row.

**Completion criterion:** Every active row is either retained with current closure evidence requirements or removed only after its state-specific closure evidence and resulting effect are recorded.

## Validate and report

- Verify that every row has a unique identifier, one of the states `Decision needed`, `Missing input`, or `Verified limitation`, a concrete issue, a `Rule until closure`, and a `Closure condition`.
- Verify that every linked path exists and resolves from `OPEN-ISSUES.md`.
- Verify that the file has one level-one heading, valid table columns, no unresolved placeholders, no trailing whitespace, LF line endings, and one final newline.
- Report the changed issue identifiers, the bounded evidence checked, the state-specific closure evidence, and every owner decision that remains unresolved.

**Final reporting criterion:** The report states whether every executable phase completed, names each changed issue identifier, lists the evidence checked, identifies unresolved owner decisions, and confirms whether every active row has a current `Rule until closure` and checkable `Closure condition`.

The update is complete only when every validation check and final reporting criterion passes.
