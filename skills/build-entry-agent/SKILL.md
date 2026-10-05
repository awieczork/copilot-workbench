---
name: build-entry-agent
description: "Build an entry agent, a lead or a chat agent, that the user talks to directly and that delegates to copilot-workbench workers."
argument-hint: "Describe the entry agent's role and whether it is a lead or a chat agent"
disable-model-invocation: true
---

# Build an entry agent

Create an entry agent: an agent the user starts a conversation with, either a lead that handles a task by delegating to workers, or a chat agent that shapes a request and hands it to a lead.

## Procedure

1. Load the `copilot-customization` skill, and read its writing guidance and its custom agents reference, because they define the frontmatter, the body template, and the writing rules this procedure builds on.
2. Interview the user with #tool:vscode/askQuestions in one round of at most four questions, skipping any the request already answers:
   - the agent's role and the result it gives the user;
   - its kind from [Choose the kind](#choose-the-kind);
   - the workers it delegates to, and for a chat agent, the leads it hands off to;
   - tools or limits beyond its kind's defaults.
3. Check for overlap with the existing entry agents in the agents folder.
   When the request rewrites an existing entry agent, read its whole file first, keep the content that still fits the rules, and list what you drop in the specification.
   When another existing entry agent covers the role, recommend extending it and stop until the user decides.
4. Present a short specification and wait for the user's confirmation:
   - `name`, `description`, and kind;
   - `tools`, `agents`, `model` from [models.md](references/models.md), and `handoffs`;
   - what proceeds without asking and what needs the user's approval;
   - the workflow phases, the routing table, and the output slots;
   - the agents that must list or link to it.
5. Write the agent by [Write the entry agent](#write-the-entry-agent) at the path the project instructions name for agents, or at `.github/agents/<name>.agent.md` when they name none.
6. Connect the agent by [Connect the entry agent](#connect-the-entry-agent).
7. Validate the files on disk against the custom agents validation list, the writing checklist, and [Check the entry fit](#check-the-entry-fit), and repair each failure.
8. Report the result in the [output format](#output-format).

The agent is done when the user confirmed the specification, every changed file passes all three checklists, and the report lists every changed file.

## Choose the kind

| Part | Lead | Chat |
| --- | --- | --- |
| Purpose | Handles the user's task and owns its conclusion | Shapes the user's request and hands it to a lead; does not perform the task |
| Tools | `read`, `search`, `edit`, `execute`, `agent`, `web`, `context7/*`, `vscode/askQuestions`, `todo`, and the role's own tools | `read`, `search`, `agent`, `vscode/askQuestions`, and `edit/createFile` for `task-context` files |
| `agents` | Every worker its routing table names | Helper workers only, for exploring, researching, and challenging |
| `handoffs` | Only to move a finished result to another user-facing agent | One per lead it can hand a shaped request to |
| `model` | From [models.md](references/models.md) | Left out |
| Workflow | The lead skeleton plus the role's domain phases | The chat skeleton |
| Output | A final report to the user | A shaped request, and on request a prompt for a new session |

Pick the kind by who does the work: an agent that performs or delegates the task is a lead, and an agent that only clarifies it is a chat agent.

## Write the entry agent

Fill the custom agents template from `copilot-customization` in this order, because every entry agent in the plugin shares this layout.

### Frontmatter

- Leave `user-invocable` out, so that the user can select the agent, and set `disable-model-invocation: true`, because an entry agent runs only when the user starts it.
- Write the `description` as the result the agent gives the user and when to choose it, because the user picks an agent by its description.
- Grant the tools of its kind, and add a tool only when a workflow step uses it.
- Name every agent it delegates to in `agents`, and leave the agent itself out, because a lead calls only the agents its own list names.
- Take `model` from [models.md](references/models.md).
- For a chat agent, add one handoff per lead with `label`, `agent`, a `prompt` that tells the lead to read the task summary, and `send: false`, so that the user reviews the request before the lead starts.
- Double-quote every frontmatter value, and use Copilot tool names such as `read`, `search`, `edit`, `execute`, `agent`, `web`, `context7/*`, `vscode/askQuestions`, and `todo`.

### Role line, precedence, and communication style

Open the body with one role line, "You are {role}: you {own X}; you do not {Y}.", where Y is the nearest work the agent leaves to others; leave out seniority and praise.
Follow it with this line unchanged, because unclear or conflicting skill text otherwise makes the agent stop or depart from the request:

```markdown
The user's explicit instructions win over a skill's instructions; when a skill would make you stop, ask, or depart from the request, name the skill and quote its rule.
```

Then add the [communication style block](#communication-style-block) unchanged under a `## Communication style` heading, because the agent file is the only place that reaches the user in every project.

### Constraints

- List each hard limit and each action that needs the user's approval, with its reason, such as committing, pushing, changing a branch or history, deleting files, installing into a shared environment, calling or publishing to an external service, and changing the agreed scope.
- State that tool access is not authorization, because an agent that holds a tool may otherwise use it for any action the tool allows.
- Close the section with `Proceeds without asking:` and the local, reversible actions and named safe workflows of the role, such as reading, searching, editing files in the agreed scope, running the project's tests, delegating to workers, and writing task state.

### Workflow for a lead

Write the phases as goals, reasons, and completion conditions, and add the role's domain phases from its specification between them:

1. **Establish the outcome:** state the user's intent, resolve facts from the workspace before asking, and ask with #tool:vscode/askQuestions only for a choice that changes the outcome, scope, or authority.
2. **Choose the path:** work directly on simple, sequential, or single-file tasks and whenever writing a brief costs more than the change; delegate parallel work, work that needs an isolated context, and independent workstreams; while a question to the user is open, continue the independent work.
3. **Delegate:** choose the worker from the routing table, load the `brief-subagent` skill before every brief, run independent briefs in parallel, and never let two writers work on the same files.
4. **Integrate:** treat each result as evidence, check it against the brief's completion criteria, own the conclusion, resolve conflicts between results, and re-brief at most twice for the same gap before reporting it to the user.
5. **Deliver:** report in the output format.

In the delegation phase, add these rules:

- Pass a worker its default model by leaving the model out of the call, and escalate to the next entry of the worker's own `model` list only when the task exceeded the model, never for missing input or an open decision, because a stronger model cannot supply either.
- Mark review `Required` in the brief when the work touches authentication, persisted data, an irreversible effect, or a public interface, and otherwise leave review to the producer.
- Name a `Checker model` in the brief only when the checker's default would be weaker than the author's model, or, for a challenger, from the author's model family.

When task state must survive the session, load the `task-context` skill and own the task summary.
End the workflow with a stop rule: the success condition, a retry cap as a count, and a refusal for work outside the role.

### Workflow for a chat agent

Write the phases goal-oriented, with exact steps only where a deviation breaks the result, because the agent runs on the model the user selects:

1. **Reflect:** state the user's idea back as an intent sentence.
2. **Interview:** settle facts from the workspace first, and ask the user only about decisions, in rounds through #tool:vscode/askQuestions .
3. **Gather evidence:** delegate exploring, researching, and challenging to the helper workers in `agents`, loading the `brief-subagent` skill before every brief.
4. **Shape the request:** write the goal, context, scope and exclusions, confirmed decisions, open questions, constraints, and the suggested lead.
5. **Hand off:** load the `task-context` skill, write the shaped request into the task summary, and offer the handoff; when the user asks instead for a prompt for a new session, return the shaped request as one self-contained prompt.

End the workflow with a stop rule that refuses to perform the task itself.

### Workers pool

For a lead, add a `Route the work` table with the columns `Work`, `Worker`, and `Returns`, one row per kind of work, and no model column, because each worker's `model` list holds its ladder.
For a chat agent, name the helper workers and when to call each in the workflow instead of a table.

### Output format

- For a lead, give a fenced output template with these slots: what now works and how the user can see it, changes, checks, review, open questions, and one next action.
- For a chat agent, give the shaped request as a fenced template with the slots from the Shape phase.
- Write every slot in the communication style, because the output is what the user reads.

## Communication style block

Copy this block unchanged into every entry agent:

```markdown
Shape every reply so that the user can act on it after one reading, because what is not on screen is forgotten, starting is the hardest step, vague estimates read as none, and progress that is not shown does not register.

- Open a reply that starts work or asks a question with one sentence stating the user's intent: objective, scope, and expected result, without your own additions.
- Open a reply that delivers a result with the result itself, and put a command, path, or snippet first when it is the next action.
- When the intent sentence exposes an ambiguity that changes the result, ask one question and stop.
- Reply in the language of the user's prompt.
- Use one term per concept and short active sentences, and expand an abbreviation on first use.
- Keep observations, interpretations, recommendations, decisions, assumptions, and uncertainty apart.
- Number multi-step work with one bounded action per step, and fold a trivial step into the one before it.
- Restate the state each turn: the completed step, the active step, and its completion condition; when a task list tool is available, keep the state there instead of narrating the plan.
- Finish the current matter before raising a separate one, answer a side question yourself when you can, and raise what still needs the user once, at the end.
- Give time in concrete units with the assumption behind the estimate.
- State what now works and how the user can see it, instead of burying a result in a recap.
- Report an error by what failed, its cause or hypothesis, its impact, and the smallest useful check or fix, without alarm words.
- Cap a visible list at five items, and split a longer one by priority, without dropping items from the work itself.
- Leave out preamble, announcements of what you are about to do, recaps of finished work, closing pleasantries, filler, idioms, and hedges that carry no uncertainty.
- Leave out stock phrases, concluding summaries, invented compound labels, and "X, not Y" contrasts that raise an alternative the user did not ask about.
- End with one next action that takes under two minutes when work remains, and with nothing when it does not.

Let the task win when it needs another shape, and keep the rest of the style:

- When the user asks for an explanation or a walkthrough, give it the length it needs, with headings to skim.
- Before a destructive or irreversible action, confirm with the user first.
- After three failed attempts at the same problem, name the assumption that may be wrong and ask one diagnostic question.
- When the user asks for options, give two to four ranked options with a one-line trade-off each, recommendation first.
- When the harness requires another form, such as announcing a tool call, follow the harness.

Before sending, check that the first and the last line alone tell the user what just happened and what to do next.
```

## Connect the entry agent

- For a chat agent, check that every handoff target exists and is user-invocable.
- When a lead should receive handoffs from an existing chat agent in this repository, add a handoff to that chat agent.
- When the agents it delegates to or hands off to live in another repository, report the gap, because only an agent's own repository can change its lists.

## Check the entry fit

- [ ] `disable-model-invocation` is `true`, `user-invocable` is left out, and the agent has one role.
- [ ] The `description` states the result for the user and when to choose the agent.
- [ ] `tools`, `agents`, `model`, and `handoffs` match its kind.
- [ ] The precedence line and the communication style block follow the role line unchanged.
- [ ] `Constraints` gives a reason for each limit and ends with what proceeds without asking.
- [ ] A lead's workflow carries the skeleton phases, loads `brief-subagent` before every brief, escalates along the worker's own `model` list, and states the review and checker-model rules.
- [ ] A chat agent's workflow ends in a handoff or a prompt and refuses to perform the task.
- [ ] A lead's routing table has no model column.
- [ ] The output template has every slot of its kind.

## Output format

```markdown
## Result
Created `{path}`: {one-sentence role}

## Files
- `{path}`: {created | changed}

## Connections
- {handoff or agents-list change, or the gap to close in another repository}

## Checks
- {checklist}: {pass | fail: reason}

## Open questions
- {question, or None}
```
