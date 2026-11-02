---
name: brief-subagent
description: "Use when delegating a task or selecting a model for a subagent. Supplies model selection, a self-contained brief template, and how to act on the returned status. A producer uses only model selection when calling its own checker."
user-invocable: false
---

# Brief a worker

Write a brief that lets a worker finish its task from the brief alone and return a result the delegating agent can use without a follow-up.
Delegation is one-shot: the worker starts from the brief and its own instructions, not the conversation, and returns one result without being asked again.

## Procedure

1. State one objective; split independent objectives into separate briefs.
2. Fill the template below, leaving out each section that has no content and each optional section whose condition below does not hold.
3. Select the model by "Select a model" below, send the brief, and act on the returned result by "Read the result" below.

## Select a model

Use the worker's default for a routine delegation.
When the check needs independence from its author, such as a review of your change, a challenge, or a recomputation, the default is unavailable, or evidence points to the model as the cause of an insufficient result, read [model selection](references/model-selection.md) before the call.
A producer calling its own checker uses this section and its own review workflow, not the brief template.

## Template

```markdown
## Goal
{One objective, what the result is for, and who reads it.}

## Context
{The user's request in their words when the wording matters, decisions made so far with who made them, and facts already established.}

## Inputs
- `{path}`: {what to read it for}

## Scope
- In: {paths or areas the worker may work on}
- Out: {paths or areas it must not touch}

## Constraints
- {Limit}, because {reason}.

## Decision rights
- Decide: {choices the worker makes on its own, such as how to organize the result}
- Return: {choices it returns to you instead of making, such as a change of scope}

## Done when
- {Checkable criterion}

## Review
Required

## Result file
`{exact path from the workspace root}`

## Return
{What the result must add to the worker's output format}
```

- **Review** is optional and applies only to a producer: write `Required` to have it run one review round.
- **Result file** is optional: include it when the result is a plan, must survive the session, or can exceed the rows the worker returns inline, and the worker holds `edit` or `edit/createFile`, with the path chosen by the `task-context` skill; for a worker without either, save the returned result yourself.
- **Return** is optional: include it only when the result needs content that the worker's output format lacks.

## Rules

- Describe what to achieve, not how, and prescribe an implementation only when safety or compatibility requires it, because the worker reads what you have not.
- Pass paths and line ranges instead of pasted file contents, because the worker reads the current file and the brief stays short.
- Repeat every technology, library, or language the user named as a constraint, because a worker otherwise substitutes its own preference.
- Mark an assumption as an assumption, so that the worker checks it instead of building on it.
- Write criteria the worker can check itself, such as "the tests in `tests/api/` pass", not "the code works".
- Leave out instructions the worker's own body already holds, such as its tools, its role, or its output format.
- For a follow-up brief, include the essentials of the earlier result, state what changes and what stays the same, and name what is still missing, because the new worker did not see the earlier run.
- Write the brief in plain words that a newcomer reads one way, because the worker cannot ask what a shorthand means.
- When parts that change files run in parallel, add a constraint that names the files the other parts change at the same time and tells the worker to report, not repair, a failure or a change that traces to them, because parallel workers share one working tree and a producer passes its brief's `Constraints` to its reviewer.
## Read the result

Choose the next step from the result's `Status`:

- `done`: check the result against the brief's `Done when` before building on it, and give each finding that a producer left unfixed or a checker returned a disposition: a fix or correction brief, acceptance with a reason, or a question to the user.
- `blocked`: send a correction brief with the failure evidence and unchanged scope when a correction can remove the cause, change the approach when it was wrong, and otherwise report the blocker to the user without retrying.
- `Decision needed`: settle the decision when it is yours, ask the user when it is theirs, and meanwhile continue only the work that does not depend on it.
- `Missing input`: run the cheapest read-only check that could settle the premise and send a new complete brief with it, or carry `Missing input` forward when it stays unsettled.

With any status, carry each open question, unverified claim, and finding marked `insufficient evidence` (one the available evidence cannot settle) forward as unanswered instead of filling the gap.
Stop a line of work when a correction returns the same blocker without new evidence, because another brief cannot remove it.
