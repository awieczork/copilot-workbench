---
name: build-skill
description: "Build an Agent Skill in the current project that extends the copilot-workbench plugin with project- or technology-specific capability."
argument-hint: "Describe what the skill should do"
disable-model-invocation: true
---

# Build a project skill

Create an Agent Skill under the project's `.github/skills/` that works alongside the copilot-workbench plugin's agents and skills.

## Procedure

1. Load the `copilot-customization` skill, and read its writing guidance and its Agent Skills reference, because they define the frontmatter, structure, and writing rules this procedure relies on.
2. Interview the user with #tool:vscode/askQuestions in one round of at most four questions, skipping any the request already answers:
   - what the skill does and what result it produces;
   - which requests should trigger it, and the closest request that should not;
   - who invokes it: the user, agents, or both;
   - which scripts, reference files, or templates it needs.
3. Check for overlap with the skills in `.github/skills/`, the project instructions, and the plugin skills under [Reuse plugin skills](#reuse-plugin-skills).
   When an existing skill covers the need, recommend extending or reusing it and stop until the user decides.
4. Present a short specification and wait for the user's confirmation:
   - `name` and `description`;
   - invocation settings;
   - sections and bundled resources;
   - the project instruction that will name the skill, when agents should load it.
5. Write the skill at `.github/skills/<name>/` by the template in the Agent Skills reference and the rules below.
6. When agents should load the skill, name it in a project instruction as described under [Connect the skill to agents](#connect-the-skill-to-agents).
7. Validate the files on disk against the Agent Skills validation list, the writing checklist, and [Check the plugin fit](#check-the-plugin-fit), and repair each failure.
8. Report the result in the [output format](#output-format).

The skill is done when the user confirmed the specification, every created file passes all three checklists, and the report lists every changed file.

## Fit the plugin

- Keep the skill project- or technology-specific; when the capability would serve any project, tell the user it belongs in the plugin itself and stop.
- Choose a `name` that differs from every plugin skill, so that the slash commands stay distinct.
- Set `disable-model-invocation: true` when only the user should trigger the skill, and give it a one-line description; otherwise write a description with one trigger per request branch.
- Write each step as its goal, its reason, and its completion condition, and prescribe an exact sequence with its check only where a deviation breaks the result, because agents on strong and economy models load the same skill.
- When a step can stop the agent or make it ask, have the step return the reason with the skill name and the quoted rule, so that the delegating agent sees why work paused.
- When agents may load the skill, have each step return an open question in its output rather than ask the user, because plugin workers run as subagents without #tool:vscode/askQuestions .
- Leave the tone and format of replies to the user out of the skill, because the plugin's chat and lead agents define how they communicate.
- Use Copilot tool names in the body, such as `read`, `edit`, `search`, `execute`, `web`, and `vscode/askQuestions`.
- Quote the `description` value with double quotes, and write one sentence per line without hard wrapping.

### Reuse plugin skills

| Need | Plugin skill |
| --- | --- |
| Running Python | `run-python`; bundled Python scripts run through `uv run` and declare dependencies inline |
| Keeping task state across sessions or agents | `task-context`; never create another state directory |
| Writing a task for a subagent | `brief-subagent` |
| Clarifying the user's intent | `interview-me`, which only the user invokes |
| Writing customizations in general | `copilot-customization` |

Name the plugin skill in the new skill's body where it applies instead of restating its rules.

### Connect the skill to agents

Plugin agents cannot be edited inside a project, and agents often skip a skill that only supplies knowledge.
When agents should load the skill, name it in the project instruction that matches its scope:

- For files of one language, framework, or folder, add a pointer to a scoped instruction with a matching `applyTo` and `description`.
- For guidance most tasks need, add a pointer to the project's `copilot-instructions.md` or `AGENTS.md`.

Write the pointer with its condition first, such as "When writing a database migration, load the `sql-migrations` skill."

## Check the plugin fit

- [ ] The skill is project- or technology-specific, and its `name` differs from every plugin skill.
- [ ] Invocation settings match who should trigger the skill.
- [ ] No step asks the user when agents may load the skill.
- [ ] Every step that can stop the agent returns the reason with the skill name and the quoted rule.
- [ ] The skill names a plugin skill instead of restating it, and creates no state directory of its own.
- [ ] A project instruction names the skill when agents should load it.

## Output format

```markdown
## Result
Created `.github/skills/{name}/`: {one-sentence purpose}

## Files
- `{path}`: {created | changed}

## Loading
{slash command only | loaded by agents through `{instruction path}`}

## Checks
- {checklist}: {pass | fail: reason}

## Open questions
- {question, or None}
```
