---
name: tidy-tasks
description: "Archive finished task folders, remove archived ones older than seven days, and review live tasks."
disable-model-invocation: true
---

# Tidy tasks

Clear finished work out of `.github/context/`, so that `active/` holds only live tasks, and change only the folders the user approves.

## Procedure

1. Load the `task-context` skill, because it owns the folder layout and the archive and remove rules that this procedure applies.
1. Read `summary.md` in each folder under `active/` and `archive/`, and sort each item under `.github/context/`:
   - A folder in `active/` with `State: done` is to archive.
   - A folder in `active/` with `State: active` or `State: blocked` is a live task.
   - A folder in `archive/` whose `Archived:` date is more than seven days before today is to remove.
   - A folder in `archive/` without an `Archived:` line, a folder without `summary.md` or without a `State:` of `active`, `blocked`, or `done`, and any other item are not handled and stay unchanged, because nothing shows their age or owner.
1. For each folder to archive, list the decisions and open questions that outlive the task, with the record that owns each, or `no record` when none does.
1. Present the plan in the output format, and in the same round ask the user to approve it, to name the record for each `no record` item, and to mark any live task as done, through #tool:vscode/askQuestions when you hold it and in chat when you do not.
1. For each live task the user marks done, set `State: done` in its summary, list its outliving decisions and open questions as in step 3, and add it to the folders to archive after the user approves that list.
1. Move each approved outliving item into its record, then archive and remove exactly the approved folders.
1. Report the result in the output format, with the paths archived and removed under `Archive` and `Remove`, and the items left unchanged under `Live tasks` and `Not handled`.

Tidying is done when every approved folder is archived or removed and the user has the report.

## Rules

- Leave a live task unchanged unless the user marks it done, because another session may hold it and only its summary shows that the work is finished.
- Remove only the exact paths the user approved in this run, because a removal cannot be undone.

## Output format

```markdown
## Archive

- `{folder}`: {objective}; outliving: {item → owning record | none}

## Remove

- `{folder}`: archived {YYYY-MM-DD}; contents: {files}

## Live tasks

- `{folder}`: {state}, {days since folder date} days; next action: {Next action}

## Not handled

- `{path}`: {reason}
```
