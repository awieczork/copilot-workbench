# [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)

An Agent Skill is a folder with a `SKILL.md` file and optional resources that the agent loads only when a task needs it.
VS Code follows the [Agent Skills specification](https://agentskills.io/specification).

## Locations

| Scope | Location |
| --- | --- |
| Workspace | `.github/skills/<name>/`, `.agents/skills/<name>/`, or `.claude/skills/<name>/` |
| User | `~/.copilot/skills/<name>/`, `~/.agents/skills/<name>/`, or `~/.claude/skills/<name>/` |
| Agent Plugins 1.0 package | `skills/<name>/` |

```text
<name>/
├── SKILL.md        # required
├── references/     # documents the agent reads under a stated condition
├── scripts/        # code the agent runs
├── assets/         # static files used without rewriting
└── templates/      # starter files the agent adapts
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
| `name` | Yes | 1–64 lowercase letters, digits, and single hyphens, not starting or ending with a hyphen, and matching the folder name; an invalid name stops the skill from loading |
| `description` | Yes | Up to 1024 characters; the only text the agent sees before it decides to load the skill |
| `argument-hint` | No | Hint shown when the user runs the skill as a slash command |
| `user-invocable` | No | `false` removes the slash command; defaults to `true` |
| `disable-model-invocation` | No | `true` stops the agent from loading the skill on its own; defaults to `false` |

| Configuration | Slash command | Loaded by the agent |
| --- | --- | --- |
| Both fields omitted | Yes | Yes |
| `user-invocable: false` | No | Yes |
| `disable-model-invocation: true` | Yes | No |
| Both set | No | No |

- Set `disable-model-invocation: true` when the skill should run only on the user's request, and give it a one-line description of its task.
- Do not add a plugin namespace to `name`, because VS Code adds the plugin prefix itself.
- Leave out `context: fork`, `license`, `compatibility`, `metadata`, and `allowed-tools` unless the user asks, because VS Code either marks them experimental or does not document them.

## Progressive disclosure

A skill loads in three stages:

1. **Discovery:** the agent sees only `name` and `description`, about 100 tokens per skill.
2. **Instructions:** the agent reads the `SKILL.md` body once the skill matches or the user runs it.
3. **Resources:** the agent reads a bundled file only when the body links to it and its condition applies; an unlinked file never loads.

- Put everything that decides activation into the `description`, because the body is invisible until the skill loads; a `When to use` section in the body cannot trigger anything.
- Keep `SKILL.md` under 500 lines and about 5,000 tokens; when it grows past that, move a branch into a reference rather than cutting rules.
- Link every resource directly from `SKILL.md`, because a file linked only from another resource is read in part or missed.

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

- {Environment-specific fact that defies a reasonable assumption.}
````

- Keep only the sections the skill uses, and add `Output format` only when the skill returns a result.
- Keep gotchas in `SKILL.md`, and add one when a correction reveals a fact the agent could not have assumed.
- Name a skill that only supplies knowledge in the agent body or instructions that need it, because agents often skip such a skill on their own.

## Scripts

Bundle a script when the agent would otherwise rewrite the same logic on each run, or when exact behavior and error handling matter.

- List each script in `SKILL.md` with what it does and when to run it.
- Make the script non-interactive, with arguments and `--help`.
- Write data to standard output and diagnostics to standard error, and keep output size predictable.
- Validate input, and state in each error message what was expected.
- Make repeated runs safe, and provide `--dry-run` for changes to files or systems.
- Return meaningful exit codes.
- Declare dependencies inline or pin their versions, and keep credentials out of the code.

## Validate

- [ ] The folder sits at a documented location and contains `SKILL.md`.
- [ ] `name` matches the folder and its syntax, and `description` is present and under 1024 characters.
- [ ] `SKILL.md` is under 500 lines and holds what every use needs, and every resource is linked directly from it.
- [ ] Every script has `--help`, non-interactive arguments, clear errors, and safe repeated runs.
