# Worker contract

Read this before writing or changing a worker of the plugin's team.
A worker is a hidden subagent that performs one specialized task from a self-contained brief and returns one result to the agent that delegated it.

## Choose the kind

Pick the kind by what the worker returns.

| Kind | Returns | Writes | Calls a checker |
| --- | --- | --- | --- |
| Helper, such as `explorer`, `database-explorer`, `data-explorer`, `researcher`, or `challenger` | Evidence | Its result file only | No |
| Producer, such as `developer`, `ui-developer`, or `planner` | A change or a plan | Files in the brief's scope; a planner only its plan | Yes, by [For a producer](#for-a-producer) |
| Checker, such as `reviewer` | A verdict on another worker's result | Its result file only | No |

## Frontmatter

- Set `user-invocable: false`, because a worker runs only as a subagent.
- Grant only the tools a workflow step uses.
- For a producer, add `agent` and set `agents` to its checker alone; leave both out of helpers and checkers.
- Take the `model` list from [model-tiers.md](model-tiers.md).

## Shared block

Open with a role line that states what the worker does and what it does not do.
Follow it with this block unchanged, because every worker needs it before it loads any skill:

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
- Name the skill that holds access or procedure at the phase where it loads, and do not restate its rules.
- End with a stop rule, a stop after three failed attempts at the same step that reports the error and what was tried, and the return of an out-of-role request as a blocker.

## For a producer

When the producer writes code or a plan, add this line unchanged:

```markdown
Before you rely on a library, an external API, or a tool in code or a plan, read its documentation for the version the project uses with #tool:context7/* , and when it cannot answer, read the official documentation through `web` and record the gap, because what you remember of an interface can be outdated.
```

Add these review rules:

- Run one review round with the checker when the brief marks review `Required`, and otherwise when an error would be costly to find later, naming those cases in the producer's terms.
- Call the checker through #tool:agent with the delegating agent's goal verbatim, the changed paths, and the brief's `Checker model` as the call's model when the brief names one.
- Fix the findings the producer accepts, give every finding a disposition, and report whether the review ran and why.

## Output format

Give a fenced output template that starts with `Status: {done | blocked | Decision needed | Missing input}`, keeps a verdict in its own slot, gives slots in the role's terms that the delegating agent acts on, most important first, and ends with an `Open questions and blockers` slot in which each entry names its cause and what would remove it.

## Check the worker contract

- [ ] `user-invocable` is `false`, and the role line states one role with what the worker does and does not do.
- [ ] Every tool serves a workflow step, and only a producer has `agent`, with `agents` naming only its checker.
- [ ] The `model` list matches a row in `model-tiers.md`.
- [ ] The shared block follows the role line unchanged, with the result-file line exactly when the worker holds `edit` or `edit/createFile`.
- [ ] The workflow has numbered phases, names each skill at its loading point without restating it, and ends with the stop rule, the three-failure stop, and the out-of-role blocker.
- [ ] A producer carries the documentation line and the review rules.
- [ ] The output template starts with the `Status` line and ends with the `Open questions and blockers` slot.
