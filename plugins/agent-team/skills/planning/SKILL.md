---
name: planning
description: "Use when a change or analysis needs an explicit plan, or when following or resuming one. Supplies a proportional plan, its template, and a workflow for maintaining it. Not for routine work that needs no plan."
user-invocable: false
---

# Plan the work

Create and maintain a plan that makes the next slice executable and scales its detail to the task.
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.

When the plan or progress must survive the session, the task starts from a task folder, or the plan must be handed off, use `task-context` before creating the plan.
Before following an accepted plan, use `task-context` to keep it in the task folder.
When the user requests a plan as a deliverable elsewhere, give them a snapshot rather than maintaining a second working plan.
Otherwise keep a draft plan in the current context, or at the user-requested location when it is a deliverable.

## Create the plan

1. Establish the goal, scope, constraints, and observable result, and inspect the affected behavior, sources, and checks.
   When the goal or expected result cannot be established, report `Missing input` and stop without a plan.
   Trace the affected behavior through its callers, data flow, and tests when they exist.
   For a defect, confirm it before designing a fix; report a missing premise when it cannot be confirmed.
2. Resolve routine reversible choices from the evidence.
   For a decision reserved to the user or one that changes the behavior, scope, or an irreversible effect, state the affected parts and a recommendation, and leave the affected work until the user decides.
3. State the intended behavior, including relevant failure or edge cases, the approach and its boundaries, and a check for each behavior.
   Reuse existing patterns before adding new mechanisms, and explain consequential alternatives and compatibility effects.
   Distinguish confirmed decisions, assumptions, and unverified evidence, and cite the sources the plan relies on.
4. For dependent or parallel work, identify independently checkable tasks, their dependencies, and their key checks.
   Name the targets and, when work is split, who owns each task, so that each executor has what it needs without settling a reserved decision.
   Keep the plan to a slice the user can assess, and name later work separately.
   When an independent challenge of a consequential disputed decision can change the result, use `brief-subagent` to brief `challenger` on a falsifiable claim and its evidence.
   Record the disposition of each objection, and report a challenge that could not run or returned an incomplete result with its cause and open questions.

When creating a plan, use the [plan template](references/plan-template.md), omitting sections that do not affect the task.
Before execution, the task holder accepts or amends the plan; this does not require user approval unless the user requests it or a decision or effect requires it.
When the user asks only for a plan, deliver it and ask about unresolved user decisions without starting implementation.

## Follow and update the plan

1. Start a task only when its dependencies are complete, and do independent tasks in parallel when that benefits the work.
   Keep decisions and acceptance with the task holder whether the work is direct or delegated.
2. Update the plan and any task list when work starts, finishes, or becomes blocked.
   Mark a task done only after its key check passes; record a failed or unavailable check, its impact, and what would unblock it.
3. When new evidence changes the approach, dependencies, checks, or assumptions, amend the plan before the affected work continues.
   Complete work independent of an unresolved user decision, then ask about that decision and stop the affected work.
4. When the slice ends, compare its results with the intended behavior and checks, and report any gaps, open decisions, and follow-up work.
