# Skill contract

Read this before writing or changing a plugin skill.
A plugin skill owns the access to one system or one procedure; agents load it through its `description`, name it at the point where it loads when it is core to their work, and do not restate it.

## Own the work

- Hold the access path, the procedure, the gate, and the traps of the system in the skill, because the agents that load it rely on it instead of restating them.
- Leave another skill's rules to that skill, and name it only at a step that depends on it, as `redshift` names `run-python` for its runner.
- Keep task state only through the `task-context` skill, because agents look for task state only in its folder.
- Leave the communication style out of the skill, because entry agents own it; an output format holds only the content of the skill's result.

## Subagent line

When a step that a subagent may run asks the user, and the skill does not set `disable-model-invocation: true`, add this line unchanged after the opening sentence, and let the other steps say "ask the user":

```markdown
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.
```

## Content

- Write a gate as an allow-list followed by the look-alikes it refuses, because a principle read loosely lets a look-alike through.

## Check the skill contract

- [ ] The skill owns one system or procedure, and names another skill only at a step that depends on it.
- [ ] A skill whose subagent-run steps ask the user, and that a model can load, carries the subagent line unchanged after its opening sentence.
- [ ] Task state goes only through `task-context`, and the skill carries no communication style.
- [ ] A gate is an allow-list with its look-alikes.
