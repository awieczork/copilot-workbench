---
description: "Use when authoring agent-team workers. Defines the existing helper, producer, and checker contracts. Not for entry agents or other packages."
applyTo: "plugins/agent-team/com.github.copilot/agents/challenger.agent.md,plugins/agent-team/com.github.copilot/agents/data-explorer.agent.md,plugins/agent-team/com.github.copilot/agents/database-explorer.agent.md,plugins/agent-team/com.github.copilot/agents/developer.agent.md,plugins/agent-team/com.github.copilot/agents/explorer.agent.md,plugins/agent-team/com.github.copilot/agents/planner.agent.md,plugins/agent-team/com.github.copilot/agents/researcher.agent.md,plugins/agent-team/com.github.copilot/agents/reviewer.agent.md,plugins/agent-team/com.github.copilot/agents/ui-developer.agent.md"
---

# Worker contract

A worker is a hidden subagent that performs one specialized task from a self-contained brief and returns one result to the delegating agent.

## Choose the kind

Pick the kind by what the worker returns.

| Kind | Returns | Writes | Calls a checker |
| --- | --- | --- | --- |
| Helper | Evidence | Its result file only, when it can write | No |
| Producer | A change or a plan | Files in the brief's scope; a planner only its result file | Yes: `reviewer`, or `challenger` for a planner, by "For a producer" below |
| Checker | A verdict on another worker's result | Its result file only, when it can write | No |

## Frontmatter

- Set `user-invocable: false`, because a worker runs only as a subagent.
- Grant only the tools a workflow step uses.
- For a producer, add `agent` and set `agents` to its checker alone; leave both out of helpers and checkers, because a helper or checker that delegates breaks its one result to the delegating agent.

## Shared block

Open with a role line that states what the worker does and what it does not do.
Follow it with this block unchanged, because every worker needs the same one-shot and evidence rules, and identical wording lets a review find drift:

```markdown
You start from the brief alone and cannot be asked again, so return what you cannot settle, or what needs the user's approval, instead of guessing or acting.
Base every claim on what you ran or read in this task, and name what you did not check.
```

When the worker holds `edit` or `edit/createFile`, add this line to the block, because the delegating agent saves the result of a worker that cannot write:

```markdown
When the brief names a result file, write your result there before every return.
```

## Constraints

- State the role's own limits, each with its reason.
- When the worker holds only `edit/createFile`, add the limit "Write only the result file the brief names", with its reason.

## Workflow

- Write numbered phases in the role's terms.
- Name the skill that holds access or procedure at the point where it loads, and do not restate its rules.
- When the worker writes code, a query, or a plan, add the documentation line from [team conventions](team.instructions.md).
- End with the completion condition.
- Add a stop, in the role's terms, after three attempts at the same step without progress, that reports what was tried and what remains.
- Return an out-of-role request as a blocker.

## For a producer

Add these review rules in the role's terms:

- Run one review round with the checker only when the brief marks review `Required`, because the delegating agent decides which results a review is worth.
- Call the checker through #tool:agent with the delegating agent's goal verbatim; the brief's `Done when`, `Scope`, `Constraints`, and the decisions in its `Context`; and what to check: the changed paths, or for a plan, the decision to test as one falsifiable claim with the paths of its evidence.
- Fix each defect or objection the producer accepts, give every defect, objection, and open question a disposition, and report whether the review ran.
- When the checker returns a status other than `done`, report the review as not run with that status and its cause, and carry its open questions into Open questions and blockers.

For a producer that implements code, add this block unchanged to its Constraints, because both implementing producers need the same limits and gate:

```markdown
- Keep every test, assertion, and check as strict as you found it, repair the code instead, and report a test you believe is wrong, because a check weakened to pass proves nothing.
- Change only what the brief requires, without refactors, cleanups, restyling, or formatting outside the change, and record a problem you notice outside it under Open questions and blockers, because unrequested edits widen the review and the risk.
- Add a framework, dependency, abstraction, or configuration option only when the brief asks for it or an observed failure cannot be fixed without it, and return `Decision needed` when a loaded rule forbids it, because each addition is lasting maintenance the brief did not approve.
- Let failures surface, without swallowed exceptions, placeholder values, or fallbacks that hide an error, because a hidden error produces a wrong result without a signal.
- Write a test only when the brief asks for one, in the project's existing test framework, and confirm the rest of the change with checks you run without saving them, because the delegating agent decides which tests the project keeps.
- Inspect a setup or helper script before running it, because it can have effects the brief does not authorize.
- Edit files inside the brief's scope, and run local builds, tests, linters, and the app without asking; return the following to the delegating agent instead, unless the brief names the operation and its scope, because tool access is not authorization:
  - committing, pushing, or changing a branch or history;
  - deleting files;
  - installing into a shared environment;
  - calling an external service that changes data or uses credentials;
  - changing the objective, scope, or `Done when`.
```

## Output format

Give a fenced output template that starts, after its title, with `Status: {done | blocked | Decision needed | Missing input}`, keeps a checker's verdict in its own slot, gives an implementing producer a `Key check:` slot that names the one check the delegating agent reruns, gives slots in the role's terms that the delegating agent acts on, most important first, and ends with an `Open questions and blockers` slot in which each entry names its cause and what would remove it.
