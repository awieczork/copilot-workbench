# Worker contract

Read this before writing a worker for the copilot-workbench plugin's team, in the plugin or in a project.
A worker is a hidden subagent that performs one specialized task from a self-contained brief and returns one result to the agent that delegated it.

## Choose the kind

| Kind | Examples | Tools | Writes | Review | Output slots |
| --- | --- | --- | --- | --- | --- |
| Helper | Explorer, Researcher, Challenger | `read`, `search`, and the role's own tools; `edit/createFile` only for a result file | Its result file only | None | Findings with their evidence, `insufficient evidence` when the evidence does not settle the question, and what was not searched or checked |
| Producer | Developer, UI Developer, Planner | The role's tools and `context7/*`, plus `agent` with `agents` naming only its checker, such as Reviewer for Developer or Challenger for Planner | Files in the brief's scope; a planner writes only its plan | By [Review](#review) | Changed, checked, not checked, still open, review findings with their dispositions; a planner returns its plan sections in place of Changed and its challenge record in place of review findings |
| Checker | Reviewer | `read`, `search`, `execute`; `edit/createFile` only for a result file | Its result file only | None; it never delegates | Verdict, checked, not checked, findings with evidence |

Pick the kind by what the worker returns: evidence makes a helper, a change or a plan makes a producer, and a verdict on another worker's result makes a checker.

## Frontmatter

- Set `user-invocable: false`, because a worker runs only as a subagent.
- Grant the tools of its kind, and add a tool only when a workflow step uses it.
- For a producer, set `agents` to its checker alone; leave `agent` and `agents` out of helpers and checkers.
- Copy the `model` ladder from [model-tiers.md](model-tiers.md).

## Shared rules

Follow the role line with this block unchanged, because every worker needs it and a worker cannot be relied on to load a skill first:

```markdown
The brief is your complete assignment, because you start without the delegating agent's conversation.
Delegation is one-shot: return open questions and blockers instead of guessing, because nobody can prompt you again.
When a skill or instruction stops you or makes you ask, return the reason with its file name and the quoted rule.
```

When the worker holds `edit` or `edit/createFile`, add this line to the block; leave it out otherwise, because the delegating agent saves the result of a worker that cannot write:

```markdown
When the brief names a result file, load the `task-context` skill and write your result there before every return.
```

## Constraints

- Have the worker return an approval item to the delegating agent instead of acting on it, because a worker cannot ask the user.
- Give a helper or checker that holds `edit/createFile` the limit "Write only the result file the brief names".

## Workflow

- For a helper or checker, read a source before making a claim about it, and mark what it did not search or check.
- For a producer that changes code, match testing to the size of the change, test that the code is correct rather than that it matches itself, report a wrong test instead of working around it, and remove temporary files before returning.

### Documentation

- Before a producer writes code or a plan that uses a library, framework, or tool API, have it read that API's documentation at the version the project pins through #tool:context7/* , because current documentation keeps the work off outdated APIs.
- When context7 is unavailable, fall back to the official documentation through `web` and record the gap; when neither covers the pinned version, return a blocker.
- Skip the phase when the work touches no external API.

### Review

- Run one review round with the checker when the brief marks review `Required`, and otherwise when the producer judges an independent check adds value, such as for authentication, persisted data, an irreversible effect, a public interface change, or low confidence in its result, because the delegating agent cannot foresee every risk the work uncovers.
- Call the checker through #tool:agent with the delegating agent's goal verbatim, the changed paths, and the brief's `Checker model` as the call's model when the brief names one.
- Fix the findings the producer accepts, give every finding a disposition, and report whether the review ran and why.

## Output format

- Give the worker a fenced output template with the slots of its kind, most important first, and an `Open questions and blockers` slot.
- Write the slots so that a person can read the result, because the delegating agent may pass it on unchanged.

## Check the worker contract

- [ ] `user-invocable` is `false`, and the worker has one role.
- [ ] `tools` match its kind, and only a producer has `agent`, with `agents` naming only its checker.
- [ ] The `model` list matches a row in `model-tiers.md`.
- [ ] The shared rules block follows the role line unchanged, with the result-file line exactly when the worker holds `edit` or `edit/createFile`.
- [ ] A producer reads current documentation before writing code or a plan that uses an external API.
- [ ] A producer's review phase runs on `Required` or on its own judgment, passes the brief's `Checker model` when named, and reports whether the review ran and why.
- [ ] The output template has every slot of its kind and an `Open questions and blockers` slot.
