---
name: build-skill
description: "Build an Agent Skill in the current project that extends the copilot-workbench plugin."
argument-hint: "Describe what the skill should do"
disable-model-invocation: true
---

# Build a project skill

Create an Agent Skill under the project's `.github/skills/` that fits the copilot-workbench plugin's agents and skills.

## Procedure

1. Load the `copilot-customization` skill and follow its procedure for an Agent Skill, and read the [skill contract](references/skill-contract.md) before writing, because it defines how a skill fits the plugin's agents.
2. Draft a specification from the request and the workspace, and present it with only the questions whose answers change it:
   - `name`, `description`, and invocation settings;
   - sections and bundled resources;
   - the project skills, project instructions, and plugin skills it overlaps, with a recommendation to reuse or extend one that covers the need;
   - whether the capability would serve any project, in which case it would also fit the plugin itself;
   - how agents will load it: by description, or through a project instruction.
3. After the user confirms the specification, write the skill at `.github/skills/<name>/`.
4. When the skill only supplies knowledge, connect it by [Connect the skill to agents](#connect-the-skill-to-agents).
5. Validate the files on disk against the Agent Skills validation list, the writing checklist, and the skill contract checklist, and repair each failure.
6. Report the result in the [output format](#output-format).

## Connect the skill to agents

Plugin agents cannot be edited inside a project, and agents often skip a skill that only supplies knowledge.
When the skill only supplies knowledge, name it in the project instruction that matches its scope, because a skill with a procedure loads by its description:

- For files of one language, framework, or folder, add a pointer to a scoped instruction with a matching `applyTo` and `description`.
- For guidance most tasks need, add a pointer to the project's `copilot-instructions.md` or `AGENTS.md`.

Write the pointer with its condition first, such as "When writing a database migration, load the `sql-migrations` skill."

## Output format

```markdown
## Result
Created `.github/skills/{name}/`: {one-sentence purpose}

## Files
- `{path}`: {created | changed}

## Loading
{slash command only | by description | through `{instruction path}`}

## Checks
- {checklist}: {pass | fail: reason}

## Open questions
- {question, or None}
```
