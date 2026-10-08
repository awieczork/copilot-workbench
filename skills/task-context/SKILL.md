---
name: task-context
description: "Use when task state must survive the session or pass between agents, when a brief or handoff names a task folder or result path, or when an interrupted task resumes. Supplies the task folder layout under .github/context/ and the rules for its summary and result files. Not for finished deliverables, durable project knowledge, or tracked records."
---

# Task context

Keep the working state of one task in a Git-ignored task folder, so that it survives the session and reaches every agent that works on the task.
Keep short work in the conversation, and keep deliverables and approved knowledge in their canonical locations, because a task folder holds working state, not a source of truth.

## Owner and subagents

The **owner** is the agent the user talks to that holds the task, such as a chat agent while it shapes a request, then the lead that receives the handoff.
Only the owner creates, resumes, archives, or removes a task folder, writes `summary.md` and `notes.md`, and asks the user about the folder.
A subagent follows only [Delegate with a result file](#delegate-with-a-result-file), because it cannot ask the user and the owner integrates its result.

## Layout

```text
.github/context/
├── active/
│   └── YYYY-MM-DD-<slug>/
│       ├── summary.md          # current state, kept by the owner
│       ├── notes.md            # optional decisions, ideas, and discussion notes
│       └── results/
│           └── <role>-<n>.md   # one file per delegated result
└── archive/
```

- Create one task folder per objective, dated on creation.
- Form the slug from lowercase ASCII letters, digits, and single hyphens, because the folder must stay a direct child of `active/`.
- Before the first write, check that the repository ignores `.github/context/`; when it does not, tell the user and ask before writing, because the folder holds unreviewed working notes.
- When the folder already exists, keep it and ask the user whether to reuse it or choose another slug.

## Keep the summary

Keep these fields in `summary.md`:

```markdown
# {Objective}

Status: {active | blocked | done}
Next action: {one action}

## Decisions
- {decision}: {who made it}

## Open questions
- {question, or None}

## Files
| File | Owner | Purpose |
| --- | --- | --- |
| `{path}` | {agent} | {purpose} |

## Sources
- {link to a canonical file or document}
```

Update the summary after a verified result, a failed step, a confirmed decision, or a change of the next action, because the context can be compacted at any point and the work then continues from the saved state.
When the context fills, continue the task instead of stopping or shortening the work to save context.

## Hand off a task

1. Before the handoff, the chat agent writes the current state into `summary.md` and names the task folder path in the handoff prompt.
2. The lead agent reads `summary.md` and `notes.md`, becomes the owner, and records the change in the summary.

## Delegate with a result file

When a delegated result must survive the session, the owner registers a result path in the `Files` table, such as `results/reviewer-1.md`, and passes the exact path in the brief.

A subagent that receives a result path:

1. Checks that the path lies inside the task folder and does not exist yet; otherwise it returns the problem without starting work.
2. Writes its complete result to that path before every return, including a blocked, failed, or partial one.
3. Names the path in its response.

- Write only that result file, never `summary.md`, `notes.md`, or another agent's file, because the owner integrates results.
- Treat a result file from another agent as unverified evidence, because saving a claim does not check it.

## Resume a task

Select the active task folder whose objective and status match the request, and continue from its `summary.md`.
When none or several match, list the candidates and ask the user to choose.

## Keep the folder lean

- Record concise state and link to files instead of copying them.
- Keep structured state, such as the status of each item or test, as a table in `notes.md` or a result file, and keep progress notes as free text, because a table shows what is left at a glance.
- Leave out credentials, personal data, secrets, full command output, and conversation transcripts.

## Archive or remove

- Leave a finished or abandoned task folder in `active/` until the user asks to archive or remove it.
- To archive, move the folder to `archive/` with its name unchanged; when the destination exists, stop and report it.
- Before removing a folder, list its contents and get the user's confirmation of the exact path.
