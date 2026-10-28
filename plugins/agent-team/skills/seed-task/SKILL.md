---
name: seed-task
description: "Turn the current conversation into a task folder that an independent session starts from."
argument-hint: "Name what the seed should carry, such as a request, a plan direction, or a thread to continue"
disable-model-invocation: true
---

# Seed a task

Turn the thread the user names into a seed, the state that the resuming session needs to take over the task without this conversation, and write it to one task folder.

## Procedure

1. Draft the seed from the conversation: the objective, the first action of the resuming session, and what that session needs to take it without this conversation.
   Keep only what serves the objective, because a forked conversation also carries every other thread.
2. Show the draft, and in the same round ask only about the points the conversation leaves open that would change it, through #tool:vscode/askQuestions when you hold it and in chat when you do not; write after the user confirms or corrects it.
3. Load the `task-context` skill and create one task folder for the objective.
   Write the confirmed seed as `task-context` describes for a seed, with the first action as `Next action`, and put in `notes.md` the material the first action needs that does not fit a summary line.
4. Return the result in the output format, and leave the folder to the resuming session, because two sessions that write one summary overwrite each other.

The seed is done when the folder holds the confirmed seed and the user has the start prompt.

## Output format

```markdown
Seed `{task folder path}`: {objective in one line}

Start prompt: Resume the task in `{task folder path}`.
```
