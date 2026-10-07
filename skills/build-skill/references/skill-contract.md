# Skill contract

Read this before writing a skill that the copilot-workbench plugin's agents may load, in the plugin or in a project.

## Rules

- Give the skill a `name` that differs from every plugin and project skill, so that the slash commands stay distinct.
- When workers may load the skill, return open questions in its output instead of asking the user, because workers run as subagents, which cannot ask.
- Leave the tone and format of replies to the user out of the skill, because entry agents define how they communicate.
- Name a plugin skill where it applies instead of restating its rules:

| Need | Plugin skill |
| --- | --- |
| Running Python, including bundled scripts | `run-python` |
| Keeping task state across sessions or agents | `task-context`, because agents look for task state only in its folder |
| Writing a task for a subagent | `brief-subagent` |
| Writing customizations in general | `copilot-customization` |

## Check the skill contract

- [ ] The `name` differs from every plugin and project skill.
- [ ] No step asks the user when workers may load the skill.
- [ ] The skill names a plugin skill instead of restating it, and creates no task-state folder of its own.
