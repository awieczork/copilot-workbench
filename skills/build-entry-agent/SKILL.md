---
name: build-entry-agent
description: "Build an entry agent in the current project, a lead or a chat agent, that the user talks to directly and that delegates to project workers and the copilot-workbench plugin's workers."
argument-hint: "Describe the entry agent's role and whether it is a lead or a chat agent"
disable-model-invocation: true
---

# Build a project entry agent

Create an entry agent under the project's `.github/agents/`: an agent the user starts a conversation with, either a lead that handles a task by delegating to workers, or a chat agent that shapes a request and hands it to a lead.

## Procedure

1. Load the `copilot-customization` skill and follow its procedure for a custom agent, and read the [entry contract](references/entry-contract.md) before writing, because it defines how an entry agent fits the plugin's team.
2. Draft a specification from the request and the workspace, and present it with only the questions whose answers change it:
   - `name`, `description`, and kind;
   - `tools`, `agents`, `model`, and `handoffs`, naming project workers and plugin workers by their plain names;
   - what proceeds without asking and what needs the user's approval;
   - the workflow phases, the routing table, and the output slots;
   - the project entry agents and plugin entry agents it overlaps, with a recommendation to reuse one that covers the role; a plugin lead cannot delegate to project workers;
   - the project chat agents that should hand off to it.
3. When the request rewrites an existing project entry agent, read its whole file first, keep the content that still fits the contract, and list what you drop in the specification.
4. After the user confirms the specification, write the agent at `.github/agents/<name>.agent.md`.
5. Connect the agent by [Connect the entry agent](#connect-the-entry-agent).
6. Validate the files on disk against the custom agents validation list, the writing checklist, and the entry contract checklist, and repair each failure.
7. Report the result in the [output format](#output-format).

The agent is done when the user confirmed the specification, every changed file passes all three checklists, and the report lists every connection made or still missing.

## Connect the entry agent

Plugin agents cannot be edited inside a project, so the plugin's `discuss` agent cannot hand off to a project lead, and plugin leads cannot list project workers.

- List in `agents` every project worker and plugin worker the routing table names.
- When a project chat agent should hand a shaped request to a new lead, add a handoff to that chat agent.
- When a connection would need a plugin agent to change, report it, and name the project agent that can take its place.

## Output format

```markdown
## Result
Created `{path}`: {one-sentence role}

## Files
- `{path}`: {created | changed}

## Connections
- {agents-list or handoff change, or the connection a plugin agent cannot make}

## Checks
- {checklist}: {pass | fail: reason}

## Open questions
- {question, or None}
```
