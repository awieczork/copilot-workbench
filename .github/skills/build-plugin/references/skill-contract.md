# Skill contract

A plugin skill owns the access to one system or one procedure.

## Own the work

- Hold the access path, the procedure, the gate, and the traps of the system in the skill, because the agents that load it rely on it instead of restating them.
- Write a gate as an allow-list followed by the look-alikes it refuses, because a principle read loosely lets a look-alike through.
- Leave another skill's rules to that skill, and name it only at a step that depends on it, as `redshift` names `run-python` for its runner.
- Keep task state only through the `task-context` skill, because agents look for task state only in its folder.
- Leave the communication style out of the skill, because entry agents own it; an output format holds only the content of the skill's result.

## Subagent line

When a step that a subagent may run asks the user, and the skill does not set `disable-model-invocation: true`, add this line unchanged after the opening sentence, and let the other steps say "ask the user":

```markdown
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.
```
