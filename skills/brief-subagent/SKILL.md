---
name: brief-subagent
description: "Use when delegating a task to a subagent. Supplies the brief template and the rules that make a one-shot delegation self-contained. Not for a producer's call to its own checker."
---

# Brief a subagent

Write a brief that lets a subagent finish its task from the brief alone and return a result the delegating agent can use without a follow-up.

Delegation is one-shot:

- The subagent starts with the brief and its own instructions, not the conversation.
- The subagent returns one result and cannot be prompted again.
- Further work needs a new brief that carries everything the subagent needs.

## Procedure

1. State one objective; split independent objectives into separate briefs.
2. Fill the template below, leaving out the optional sections that do not apply.
3. Check the brief against [Check the brief](#check-the-brief), then send it.

## Template

```markdown
## Goal
{One objective, what the result is for, and who reads it.}

## Context
{The user's request in their words when the wording matters, decisions made so far with who made them, and facts already established.}

## Inputs
- `{path}`: {what to read it for}

## Scope
- In: {paths or areas the subagent may work on}
- Out: {paths or areas it must not touch}

## Constraints
- {Limit}, because {reason}.

## Decision rights
- Decide: {choices the subagent makes on its own, such as how to organize the result}
- Return: {choices it returns to you instead of making, such as a change of scope}

## Done when
- {Checkable criterion}

## Review
Required
Checker model: {model}

## Result file
{Path inside the task folder | None}

## Return
{Only what differs from the subagent's own output format}; list open questions and blockers instead of guessing.
```

- **Review** is optional and applies only when the subagent can call a checker on its own work: include `Required` to enforce one review round with that checker, and leave it out to let the subagent run its checker when it judges the check adds value.
- **Checker model** is optional: include it only when the checker's default model would break the rule that a reviewer is at least as strong as the author, or that a challenger comes from another model family.
- **Decision rights** is optional: include it when the task leaves choices open that change the result.
- **Result file** is optional: include it only when the result must survive the session and the subagent holds `edit` or `edit/createFile`, and take the path from the `task-context` skill; for a subagent without either, save the returned result yourself.

## Rules

- Pass paths and line ranges instead of pasted file contents, because the subagent reads the current file and the brief stays short.
- Restate the facts and decisions the subagent needs, because it cannot see the conversation.
- Repeat every technology, library, or language the user named as a constraint, because a subagent otherwise substitutes its own preference.
- Mark an assumption as an assumption, so that the subagent checks it instead of building on it.
- Write criteria the subagent can check itself, such as "the tests in `tests/api/` pass", not "the code works".
- Leave out instructions the subagent's own body already holds, such as its tools, its role, or its output format.
- For a follow-up brief, include the essentials of the earlier result, state what changes and what stays the same, and name what is still missing, because the new subagent did not see the earlier run.
- Write the brief in complete sentences, because the user can open the subagent call in chat and read the brief.

## Check the brief

- [ ] The brief has one objective and states what the result is for and who reads it.
- [ ] Choices that change the result are either the subagent's to decide or listed for return.
- [ ] Every fact, decision, and path the subagent needs is in the brief.
- [ ] Scope names what is in and what is out.
- [ ] Every `Done when` criterion is checkable by the subagent.
- [ ] The return asks for open questions and blockers, and adds only what the subagent's output format lacks.
