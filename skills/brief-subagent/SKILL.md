---
name: brief-subagent
description: "Use when delegating a task to a subagent. Supplies the brief template, the rules that make a one-shot delegation self-contained, and how to act on the returned status. Not for a producer's call to its own checker."
---

# Brief a subagent

Write a brief that lets a subagent finish its task from the brief alone and return a result the delegating agent can use without a follow-up.
Delegation is one-shot: the subagent starts from the brief and its own instructions, not the conversation, and returns one result without being asked again.

## Procedure

1. State one objective; split independent objectives into separate briefs.
2. Fill the template below, leaving out each section that has no content and each optional section whose condition below does not hold.
3. Send the brief, and act on the returned result by "Read the result" below.

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
`{exact path from the workspace root}`

## Return
{What the result must add to the subagent's output format}
```

- **Review** is optional and applies only to a producer, a subagent that calls a checker on its own work: write `Required` to enforce one review round, and leave it out to leave the review to the producer.
- **Checker model** is optional and goes under Review, with or without `Required`: include it when the checker's default model is weaker than the author's, or, for `challenger`, of the same model family, because a weaker checker misses what the author got wrong and one family shares its blind spots.
- **Result file** is optional: include it when the result must survive the session and the subagent holds `edit` or `edit/createFile`, with the path chosen by the `task-context` skill; for a subagent without either, save the returned result yourself.
- **Return** is optional: include it only when the result needs content that the subagent's output format lacks.

## Rules

- Pass paths and line ranges instead of pasted file contents, because the subagent reads the current file and the brief stays short.
- Repeat every technology, library, or language the user named as a constraint, because a subagent otherwise substitutes its own preference.
- Mark an assumption as an assumption, so that the subagent checks it instead of building on it.
- Write criteria the subagent can check itself, such as "the tests in `tests/api/` pass", not "the code works".
- Leave out instructions the subagent's own body already holds, such as its tools, its role, or its output format.
- For a follow-up brief, include the essentials of the earlier result, state what changes and what stays the same, and name what is still missing, because the new subagent did not see the earlier run.
- Write the brief in plain words that a newcomer reads one way, because the subagent cannot ask what a shorthand means.

## Read the result

Treat a returned result as a claim from a subagent that cannot be asked again, and choose the next step from its `Status`:

- `done`: check the result against the brief's `Done when` before building on it.
- `blocked`: act on the cause the subagent reports: send a correction brief with the failure evidence and unchanged scope when a correction can remove the cause, change the approach when the approach was wrong, and report the blocker to the user without retrying when only the user or the environment can remove it.
- `Decision needed`: settle the decision when it is yours, ask the user when it is theirs, and meanwhile continue only the work that does not depend on it.
- `Missing input`: run the cheapest read-only check that could settle the premise and send a new complete brief with it, or carry `Missing input` forward when it stays unsettled.

With any status, carry each open question, unverified claim, and finding marked `insufficient evidence` forward as unanswered instead of filling the gap.
Stop a line of work when a correction returns the same blocker without new evidence, because another brief cannot remove it.
