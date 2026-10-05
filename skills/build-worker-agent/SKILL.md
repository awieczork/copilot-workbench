---
name: build-worker-agent
description: "Build a worker agent that copilot-workbench lead and chat agents delegate one specialized task to."
argument-hint: "Describe the worker's role and the result it returns"
disable-model-invocation: true
---

# Build a worker agent

Create a worker: a hidden subagent that performs one specialized task from a self-contained brief and returns one result to the agent that delegated it.

## Procedure

1. Load the `copilot-customization` skill, and read its writing guidance and its custom agents reference, because they define the frontmatter, the body template, and the writing rules this procedure builds on.
2. Interview the user with #tool:vscode/askQuestions in one round of at most four questions, skipping any the request already answers:
   - the worker's role and the result it returns;
   - its kind from [Choose the kind](#choose-the-kind);
   - which agents delegate to it, and for a producer, which checker reviews its work;
   - tools or limits beyond its kind's defaults.
3. Check for overlap with the existing workers in the agents folder.
   When the request rewrites an existing worker, read its whole file first, keep the content that still fits the rules, and list what you drop in the specification.
   When another existing worker covers the role, recommend extending it and stop until the user decides.
4. Present a short specification and wait for the user's confirmation:
   - `name`, `description`, and kind;
   - `tools`, `agents`, and the `model` ladder from [model-tiers.md](references/model-tiers.md);
   - what proceeds without asking and what needs approval;
   - the workflow phases and the output slots;
   - the delegating agents that must list the worker.
5. Write the worker by [Write the worker](#write-the-worker) at the path the project instructions name for agents, or at `.github/agents/<name>.agent.md` when they name none.
6. Connect the worker by [Connect the worker](#connect-the-worker).
7. Validate the files on disk against the custom agents validation list, the writing checklist, and [Check the worker fit](#check-the-worker-fit), and repair each failure.
8. Report the result in the [output format](#output-format).

The worker is done when the user confirmed the specification, every changed file passes all three checklists, and the report lists every changed file.

## Choose the kind

| Kind | Examples | Tools | Writes | Review | Output slots |
| --- | --- | --- | --- | --- | --- |
| Helper | Explorer, Researcher, Challenger | `read`, `search`, and the role's own tools; `edit/createFile` only for a result file | Its result file only | None | Findings with their evidence, `insufficient evidence` when the evidence does not settle the question, and what was not searched or checked |
| Producer | Developer, UI Developer, Planner | The role's tools and `context7/*`, plus `agent` with `agents` naming only its checker, such as Reviewer for Developer or Challenger for Planner | Files in the brief's scope; a planner writes only its plan | One round with its checker when the brief requires it or the producer judges it adds value | Changed, checked, not checked, still open, review findings with their dispositions; a planner returns its plan sections in place of Changed and its challenge record in place of review findings |
| Checker | Reviewer | `read`, `search`, `execute`; `edit/createFile` only for a result file | Its result file only | None; it never delegates | Verdict, checked, not checked, findings with evidence |

Pick the kind by what the worker returns: evidence makes a helper, a change or a plan makes a producer, and a verdict on another worker's result makes a checker.

## Write the worker

Fill the custom agents template from `copilot-customization` in this order, because every worker in the plugin shares this layout and delegating agents read the output by its sections.

### Frontmatter

- Set `user-invocable: false`, because a worker runs only as a subagent.
- Write the `description` as the one task the worker performs and when to delegate it, because delegating agents choose a worker by its description.
- Grant the tools of its kind, and add a tool only when a workflow step uses it.
- For a producer, set `agents` to its checker alone; leave `agent` and `agents` out of helpers and checkers.
- Copy the `model` ladder from [model-tiers.md](references/model-tiers.md).
- Double-quote every frontmatter value, and use Copilot tool names such as `read`, `search`, `edit`, `execute`, `agent`, `web/fetch`, and `context7/*`.

### Role line and shared rules

Open the body with one role line, "You are {role}: you {own X}; you do not {Y}.", where Y is the nearest work the worker leaves to others; leave out seniority and praise.
Follow it with this block unchanged, because every worker needs it and a worker cannot be relied on to load a skill first:

```markdown
The brief is your complete assignment, because you start without the delegating agent's conversation.
Delegation is one-shot: return open questions and blockers instead of guessing, because nobody can prompt you again.
When a skill or instruction stops you or makes you ask, return the reason with its file name and the quoted rule.
```

When the worker holds `edit` or `edit/createFile`, add this line to the block; leave it out otherwise, because a worker without either cannot write a file and the delegating agent saves its result when it must persist:

```markdown
When the brief names a result file, load the `task-context` skill and write your result there before every return.
```

### Constraints

- List each hard limit and each action that needs approval, with its reason.
- Have the worker return an approval item to the delegating agent instead of acting on it, because a worker cannot ask the user.
- Close the section with `Proceeds without asking:` and the local, reversible actions and named safe workflows of the role, such as running the project's tests.
- Give a helper or checker that holds `edit/createFile` the limit "Write only the result file the brief names".

### Workflow

- Write the steps for the default tier of the worker's ladder, using the step detail in [model-tiers.md](references/model-tiers.md).
- Give each major phase a completion condition, and end the workflow with a stop rule: the success condition, a retry cap as a count, and a refusal for work outside the role.
- For a producer, add a documentation phase before it writes code or a plan: list the library, framework, and tool APIs the work touches at the versions the project pins, read that documentation with #tool:context7/* , fall back to the official documentation through `web` and record the gap when context7 is unavailable, and return a blocker when neither covers the pinned version, because current documentation keeps the work off outdated APIs; skip the phase when the work touches no external API.
- For a producer, add a review phase that runs when the brief marks review `Required`, and otherwise when the producer judges an independent check adds value, such as for authentication, persisted data, an irreversible effect, a public interface change, or low confidence in its result, because the delegating agent cannot foresee every risk the work uncovers.
- In the review phase, call the checker once through #tool:agent with the delegating agent's goal verbatim, the changed paths, and the brief's `Checker model` as the call's model when the brief names one; fix the findings the producer accepts, give every finding a disposition, and report whether the review ran and why.
- For a producer that changes code, match testing to the size of the change, test that the code is correct rather than that it matches itself, report a wrong test instead of working around it, and remove temporary files before returning.
- For a helper or checker, read a source before making a claim about it, and mark what it did not search or check.

### Output format

- Give the worker a fenced output template with the slots of its kind, most important first, and an `Open questions and blockers` slot.
- Write the slots so that a person can read the result, because the delegating agent may pass it on unchanged.

## Connect the worker

- When the delegating agents live in this repository, add the worker to the `agents` list of each one and name it where their routing or delegation guidance chooses workers.
- When they do not, such as plugin agents seen from a project repository, report which lead must list the worker, because only an agent's own repository can change its `agents` list.

## Check the worker fit

- [ ] `user-invocable` is `false`, and the worker has one role.
- [ ] The `description` states the one task and when to delegate it.
- [ ] `tools` match its kind, and only a producer has `agent`, with `agents` naming only its checker.
- [ ] The `model` list matches its row in `model-tiers.md`.
- [ ] The shared rules block follows the role line unchanged, with the result-file line exactly when the worker holds `edit` or `edit/createFile`.
- [ ] `Constraints` gives a reason for each limit and ends with what proceeds without asking.
- [ ] The step detail matches the default tier.
- [ ] A producer reads current documentation through `context7/*` before writing code or a plan that uses an external API.
- [ ] A producer's review phase runs on `Required` or on its own judgment, passes the brief's `Checker model` when named, and reports whether the review ran and why.
- [ ] The output template has every slot of its kind.
- [ ] Every delegating agent lists the worker, or the report names the lead that must.

## Output format

```markdown
## Result
Created `{path}`: {one-sentence role}

## Files
- `{path}`: {created | changed}

## Delegation
- {agent that lists the worker | lead that must list it}

## Checks
- {checklist}: {pass | fail: reason}

## Open questions
- {question, or None}
```
