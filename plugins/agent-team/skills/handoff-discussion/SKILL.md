---
name: handoff-discussion
description: "Transfer a confirmed request from discuss to lead in a new session. Not for other agents or unfinished discussions."
disable-model-invocation: true
---

# Hand off a discussion

Carry the confirmed request from a `discuss` conversation to a new `lead` session without starting the work.

## Procedure

1. Use the confirmed shaped request from this `discuss` conversation.
   When the current agent is not `discuss` or the request is absent or unconfirmed, ask the user to finish or confirm it with `discuss` and stop without writing task state.
2. Load the `task-context` skill.
   Reuse the task folder `discuss` holds for this request, or create one when it has none.
   Write the confirmed request into the summary as `task-context` describes for a handoff, with the first action for `lead` as `Next action`.
3. Return the folder and start prompt in the output format, and leave the folder to the new `lead` session, because two sessions that write one summary overwrite each other.

The handoff is done when the folder holds the confirmed request and the user has the start prompt.

## Output format

```markdown
Task `{task folder path}`: {objective in one line}

Select `lead` in a new session and start with: Resume the task in `{task folder path}`.
```
