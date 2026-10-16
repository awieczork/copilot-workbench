---
name: task-context
description: "Use when task state must survive the session or pass from one agent to another, or when a task starts or resumes from its task folder. Supplies the task folder layout under .github/context/, the rules for its summary and result files, and how to resume, hand off, archive, or remove a task. Not for finished deliverables, durable project knowledge, or tracked records."
user-invocable: false
---

# Task context

Keep the working state of one task in a Git-ignored task folder, so that it survives the session and reaches every agent that works on the task.
Create no task folder for work that one agent finishes in this session, and keep deliverables and approved knowledge in their canonical locations, because a task folder holds working state, not a source of truth.
The task holder, the agent the user talks to that holds the task, alone creates, resumes, archives, and removes the folder and writes `summary.md` and `notes.md`; a worker writes only the result file its brief names.

## Layout

```text
.github/context/
├── active/
│   └── YYYY-MM-DD-<slug>/
│       ├── summary.md          # current state, kept by the task holder
│       ├── notes.md            # optional working notes and ideas
│       └── results/
│           └── <role>-<n>.md   # one file per delegated result
└── archive/
```

- Create one task folder per objective, dated on creation, with a slug of lowercase ASCII letters, digits, and single hyphens, because the path must match exactly wherever it is typed.
- When the folder for a new objective already exists, add a numeric suffix to the new slug and keep the existing folder unchanged, because it holds another task's state.

## Keep the summary

Keep these fields in `summary.md`:

```markdown
# {Objective}

State: {active | blocked | done}
Next action: {one action}

## Decisions

- {decision}: {who made it}

## Open questions

- {question, or None}

## Files

| File | Writer | Purpose |
| --- | --- | --- |
| `{path}` | {agent} | {purpose} |

## Sources

- {link to a canonical file or document}
```

Update the summary whenever one of its fields changes, because the context can be compacted at any point.
Continue the work at full length when the context fills, because the summary carries it across compaction.

## Hand off a task

Before a handoff or a seed, write the request's decisions and open questions into the summary fields, and the other sections of the request after `Sources`.

## Resume a task

To take over or resume a task, select the active task folder whose objective and state match the request, read its `summary.md`, `notes.md`, and the file registered as `accepted plan`, and continue from them.
When none or several match, list the candidates and ask the user to choose.

## Delegate with a result file

For a delegated result, choose a path inside the task folder that does not exist yet, such as `.github/context/active/YYYY-MM-DD-<slug>/results/reviewer-1.md`, and register it in the `Files` table.

## Follow an accepted plan

Write into the plan's result file each amendment you make to the plan, from acceptance on, and mark each task finished when its key check passes; name the plan's next open task in `Next action`, because a resumed session follows the plan.
Register the accepted plan as `accepted plan` in the `Files` table, and mark a plan it replaces as superseded, because a resumed session must find the one plan to follow.

## Keep the folder lean

- Record concise state and link to files instead of copying them.
- Never link to a file in the folder from a tracked file, because the folder is Git-ignored and absent from every other clone.
- Leave out credentials, personal data, secrets, full command output, and conversation transcripts.

## Archive or remove

- Leave a finished or abandoned task folder in `active/` until the user asks to archive or remove it.
- Before archiving or removing a folder, move each decision and open question that outlives the task into the record that owns it.
- To archive, move the folder to `archive/` with its name unchanged; when the destination exists, add a numeric suffix as for a new folder.
- Before removing a folder, list its contents and get the user's confirmation of the exact path.
