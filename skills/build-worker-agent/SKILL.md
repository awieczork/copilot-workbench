---
name: build-worker-agent
description: "Build a worker agent in the current project that a project entry agent delegates one specialized task to, alongside the copilot-workbench plugin's workers."
argument-hint: "Describe the worker's role and the result it returns"
disable-model-invocation: true
---

# Build a project worker

Create a worker under the project's `.github/agents/`: a hidden subagent that performs one specialized task from a self-contained brief and returns one result to the agent that delegated it.

## Procedure

1. Load the `copilot-customization` skill and follow its procedure for a custom agent, and read the [worker contract](references/worker-contract.md) before writing, because it defines how a worker fits the plugin's team.
2. Draft a specification from the request and the workspace, and present it with only the questions whose answers change it:
   - `name`, `description`, and kind;
   - `tools`, `agents`, and the `model` ladder from [model tiers](references/model-tiers.md), naming the existing worker whose row it copies;
   - what proceeds without asking and what needs approval;
   - the workflow phases and the output slots;
   - the project workers and plugin workers it overlaps, with a recommendation to reuse or extend one that covers the role, because a project entry agent can list a plugin worker directly;
   - the project entry agent that will list it.
3. When the request rewrites an existing project worker, read its whole file first, keep the content that still fits the contract, and list what you drop in the specification.
4. After the user confirms the specification, write the worker at `.github/agents/<name>.agent.md`.
5. Connect the worker by [Connect the worker](#connect-the-worker).
6. Validate the files on disk against the custom agents validation list, the writing checklist, and the worker contract checklist, and repair each failure.
7. Report the result in the [output format](#output-format).

## Connect the worker

Plugin agents cannot be edited inside a project, so plugin leads never delegate to a project worker.

- When a project entry agent should delegate to the worker, add it to that agent's `agents` list and routing table.
- When the project has no entry agent, report that one must list the worker, and that the `build-entry-agent` skill builds it.

## Output format

```markdown
## Result
Created `{path}`: {one-sentence role}

## Files
- `{path}`: {created | changed}

## Delegation
- {project entry agent that lists the worker | entry agent still needed}

## Checks
- {checklist}: {pass | fail: reason}

## Open questions
- {question, or None}
```
