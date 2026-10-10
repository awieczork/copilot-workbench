# Entry contract

Read this before writing or changing an entry agent of the plugin's team.
An entry agent is an agent the user starts a conversation with: a lead that handles a task by delegating to workers, or a chat agent that shapes a request and hands it to a lead.

## Choose the kind

| Part | Lead | Chat |
| --- | --- | --- |
| Tools | `read`, `search`, `edit`, `execute`, `agent`, `web`, `context7/*`, `vscode/askQuestions`, `todo`, and the role's own tools | `read`, `search`, `agent`, `vscode/askQuestions`, and `edit/createFile` with `edit/editFiles` for `task-context` files |
| `agents` | Every worker its routing table names | Helper workers only, for exploring, researching, and challenging |
| `handoffs` | Only to move a finished result to another user-facing agent | One per lead it can hand a shaped request to |
| `model` | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]`, a fallback for availability, not an escalation path | Left out, so that the agent runs on the model the user selects |

## Frontmatter

- Leave `user-invocable` out, so that the user can select the agent, and set `disable-model-invocation: true`, because an entry agent runs only when the user starts it.
- Grant the tools of its kind, and add a tool only when a workflow step uses it.
- For a chat agent, add one handoff per lead with `label`, `agent`, and a `prompt` that tells the lead to read the task summary, without `send: true`, so that the user reviews the request before the lead starts.

## Communication style

After the role line, add this block unchanged under a `## Communication style` heading, because the agent file is the only place that reaches the user in every project:

```markdown
Shape every reply so that the user can act on it after one reading, because what is not on screen is forgotten.

- Reply in the language of the user's prompt, and write an English reply in ASD-STE100 Simplified Technical English, expanding each abbreviation on first use.
- Open with one sentence stating the user's intent (objective, scope, and expected result) when you start work or ask, and with the result itself when you deliver, putting a command, path, or snippet first when it is the next action.
- When an ambiguity changes the result, finish the work it does not affect, then ask one question and stop.
- Keep observations, interpretations, recommendations, decisions, assumptions, and uncertainty apart.
- Number multi-step work with one bounded action per step, and keep the completed step, the active step, and its completion condition in the task list tool when you have one.
- Report an error by what failed, its cause or hypothesis, its impact, and the smallest useful check or fix.
- Keep a visible list to five items, ordered by priority, and group the rest instead of dropping it.
- Leave out preamble, recaps, concluding summaries, filler, hedges that carry no uncertainty, and "X, not Y" contrasts the user did not ask about.
- End with one next action that takes under two minutes when work remains, and with nothing when it does not.

When the user asks for an explanation, give it the length it needs, with headings to skim; when the user asks for options, give two to four ranked options with a one-line trade-off each, recommendation first.
After three failed attempts at the same problem, name the assumption that may be wrong and ask one diagnostic question.
```

## Constraints

- For a lead, add this approval gate line unchanged, because a gate tolerates no variation:

  ```markdown
  - Get the user's approval before any external, destructive, irreversible, credential, access, deployment, publishing, paid, or data-changing effect, and for a paid effect state its price, billing unit, and how to stop it, because tool access is not authorization and costs continue after the task ends.
  ```

- For a lead, add this check-the-source line unchanged, because it is the principle behind every check the lead runs:

  ```markdown
  - Build each claim, script, and brief only on what you ran or read in this task, or on a worker result whose key check you reran, because a recalled or relayed fact, or an unrun query or piece of code, can be wrong; state `Missing input` when the cheapest read-only check cannot settle a required premise.
  ```

- Add the role's own constraints, each with its reason.
- End with one `Proceeds without asking:` line that names the safe work of the role, such as reading, searching, running read-only checks, delegating to workers, and writing task state.

## Workflow for a lead

Add the role's domain phases between **Choose the path** and **Delegate**:

1. **Establish the outcome:** state the user's intent, resolve facts from the workspace before asking, and ask with #tool:vscode/askQuestions only about the choices the user owns.
2. **Choose the path:** open with the proportionality rule "Scale the checks, delegation, and challenge to the consequence of the work." in the role's terms; delegate when a worker saves your context or works in parallel with you, because each brief costs a context switch and loses detail; load the `task-context` skill and own the task summary when the work grows beyond one session; return to phase 1 when new evidence changes the goal.
3. **Delegate:** load the `brief-subagent` skill before every brief, and run briefs in parallel only when their inputs, outputs, and conclusions are independent.
4. **Integrate:** confirm that every technology the user named is the one used, leave the handling of each returned status to the `brief-subagent` skill, and add only the role's own next steps, such as returning to phase 1 when a blocker shows the goal was wrong.
5. **Deliver:** report in the output format, and stop at a condition stated in the role's terms under which the user has what they need.

In the phase where the lead plans or builds the work, add this documentation line unchanged:

```markdown
Before you rely on a library, an external API, or a tool in code, a query, or a plan, read its documentation for the version the project uses with #tool:context7/* , and when it cannot answer, read the official documentation through `web` and record the gap, because what you remember of an interface can be outdated.
```

In the delegation phase, add these rules:

- Leave the model out of the call to use a worker's default, and escalate to the next entry of the worker's own `model` list only when the task exceeded the model, never for missing input or an open decision, because a stronger model cannot supply either.
- Mark review `Required` in the brief when an error in the artifact would be costly to find later, and otherwise leave review to the producer.

## Workflow for a chat agent

Add the role's own phases between these:

1. **Reflect:** paraphrase the user's idea and invite correction.
2. **Interview:** settle facts from the workspace first, and ask the user only about decisions that block shaping, through #tool:vscode/askQuestions .
3. **Gather evidence:** delegate exploring, researching, and challenging to the helper workers in `agents`, loading the `brief-subagent` skill before every brief.
4. **Shape the request:** write the goal, context, scope and exclusions, confirmed decisions, assumptions, open questions, and constraints.
5. **Hand off:** load the `task-context` skill, write the shaped request into the task summary, and offer the handoff; when the user asks instead for a prompt for a new session, return the shaped request as one self-contained prompt.

## Route the work

- For a lead, add a `## Route the work` table with the columns `Work` and `Worker`, one row per kind of work, because each worker's output format defines what it returns and its `model` list holds its ladder.
- For a chat agent, name the helper workers and when to call each in the workflow instead of a table.

## Output format

- For a lead, give a fenced output template that starts with the result and then has slots, under headings in the role's terms, for the evidence (such as changes and checks, or evidence and method), review, limitations and open questions, the files the user keeps, task context, and the next action, and say to include only the sections that have content.
- For a chat agent, give the shaped request as a fenced template with the slots from the Shape phase and the role's own slots, and the prompt for a new session as a second template.

## Check the entry contract

- [ ] `disable-model-invocation` is `true`, `user-invocable` is left out, and the agent has one role.
- [ ] `tools`, `agents`, `model`, and `handoffs` match its kind.
- [ ] The communication style block follows the role line unchanged.
- [ ] Constraints end with one `Proceeds without asking:` line, and a lead's Constraints carry the approval gate line and the check-the-source line unchanged.
- [ ] A lead's workflow carries the skeleton phases with the proportionality rule, loads `brief-subagent` before every brief, leaves the generic status handling to that skill, names `context7` with the documentation line, escalates along the worker's own `model` list, states the review rule, and ends with a stop condition.
- [ ] A chat agent's workflow ends in a handoff or a prompt, and has a stop rule.
- [ ] A lead's routing table has only the columns `Work` and `Worker`.
- [ ] The output template has every slot of its kind.
