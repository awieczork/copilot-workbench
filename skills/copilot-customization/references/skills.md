# [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

An Agent Skill is a folder with a `SKILL.md` file and optional resources that the agent loads only when a task needs it.
VS Code follows the [Agent Skills specification](https://agentskills.io/specification).

## Locations

| Scope | Location |
| --- | --- |
| Workspace | `.github/skills/<name>/`, `.agents/skills/<name>/`, or `.claude/skills/<name>/` |
| User | `~/.copilot/skills/<name>/`, `~/.agents/skills/<name>/`, or `~/.claude/skills/<name>/` |
| Copilot plugin | `skills/<name>/` |

```text
<name>/
├── SKILL.md        # required
├── references/     # documents the agent reads under a stated condition
├── scripts/        # code the agent runs
└── assets/         # templates and static files
```

Create only the folders the skill uses.

## Frontmatter

```yaml
---
name: sql-migrations
description: "Use when writing or reviewing SQL migrations. Supplies naming, locking, and rollback rules. Not for schema design."
---
```

| Field | Required | Behavior |
| --- | --- | --- |
| `name` | Yes | 1–64 lowercase letters, digits, and single hyphens, not starting or ending with a hyphen, and matching the folder name, because a mismatched skill may not load or may load under another name |
| `description` | Yes | Up to 1024 characters; with `name`, the only text the agent sees before it decides to load the skill |
| `argument-hint` | No | Hint shown when the user runs the skill as a slash command |
| `user-invocable` | No | `false` removes the slash command; defaults to `true` |
| `disable-model-invocation` | No | `true` stops the agent from loading the skill on its own; defaults to `false` |

- Set `disable-model-invocation: true` when the skill should run only on the user's request, and give it a one-line description of its task.
- Do not add a plugin namespace to `name`, because VS Code adds the plugin prefix itself.
- Leave out `context: fork`, `license`, `compatibility`, `metadata`, and `allowed-tools` unless the user asks, because VS Code either marks them experimental or does not document them.

## Progressive disclosure

- Put everything that decides activation into the `description`, because the body is invisible until the skill loads; a `When to use` section in the body cannot trigger anything.
- Keep `SKILL.md` under 500 lines and about 5,000 tokens; when it grows past that, move a branch into a reference.

## Template

````markdown
---
name: {skill-name}
description: "{Use when ... trigger per branch}. {What it supplies}. Not for {closest non-target}."
---

# {Title}

{One sentence that states what the skill does and its result.}

## Procedure

1. {Step with its procedure.}
2. {Step with its procedure.}

{Procedure} is done when {condition}.

## Rules

- {Rule grouped by concern}, because {reason}.

## Output format

```markdown
{Template with {placeholder} slots.}
```

## Gotchas

- {Trap a capable model gets wrong in this environment.}
````

- Keep only the sections the skill uses, and add `Output format` only when the skill returns a result.
- Add a gotcha only when a correction reveals it, and leave out platform or shell branches, tool parameters, and catalogs of queries or commands the model writes itself.

## Scripts

Bundle a script when the agent would otherwise rewrite the same logic on each run, or when exact behavior and error handling matter.

- State each script in `SKILL.md` with what it does, when to run it, how to give it its input, its working directory, and every output field and limit the agent reads, because the agent sees only what `SKILL.md` states and cannot see the script.
- Make the script non-interactive, taking its input from arguments or standard input, because the agent cannot answer a prompt.
- Write the data to standard output and the diagnostics to standard error, keep the output size bounded, and state in each error message what was expected, because the agent acts only on what the run returns.
- Make a script that changes files or systems safe to run again, and give it a dry run when its effect cannot be undone.
- Declare dependencies inline or pin their versions, and keep credentials out of the code.

## Validate

- [ ] The folder sits at a documented location and contains `SKILL.md`.
- [ ] `name` matches the folder and its syntax, and `description` is present and at most 1024 characters.
