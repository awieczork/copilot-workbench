# [Project instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

Project instructions hold the guidance that VS Code adds to every chat request in a workspace.

## Choose the file

| File | Location | Use when |
| --- | --- | --- |
| `copilot-instructions.md` | `.github/` | The workspace keeps its configuration under `.github/` |
| `AGENTS.md` | Repository root, and optionally subfolders | Coding agents need a shared instructions file instead of the `.github/` configuration |

Keep one canonical source of project guidance, because separate always-on policies drift apart and give the agent conflicting guidance.
The Local agent also loads `CLAUDE.md` by default (`chat.useClaudeMdFile`); when it sits beside `.github/copilot-instructions.md`, keep it as the proxy described below.
Nested `AGENTS.md` files in subfolders are experimental and load for the Local agent only when the user enables `chat.useNestedAgentsMdFiles`, which is off by default.

For personal guidance across workspaces, use `~/.copilot/copilot-instructions.md` in Copilot Agent Host sessions, or a user-scope rule with `applyTo: "**"` for the Local agent.
A plugin cannot ship either file; it ships a rule with `applyTo: "**"` instead, which VS Code attaches to every request.
Project instructions take no frontmatter.

## Template

Include only the sections the workspace needs:

```markdown
# {Project name}

## Code style
{Language and formatting preferences, with a pointer to a file that shows the pattern.}

## Architecture
{Major components, their boundaries, and the reason behind non-obvious structure.}

## Build and test
{Exact commands to install, build, and test.}

## Conventions
{Patterns that differ from common practice, with a short example.}
```

## Principles

- Keep only what nearly every task needs, because the file loads on every request; move rules for one language, framework, or folder into scoped instructions.
- Point to existing documentation with the condition for reading it, such as "Use `docs/database.md` for schema changes", and leave out what the documentation, linters, or formatters already cover.

## CLAUDE.md proxy

When Claude Code needs the workspace's `.github/` configuration, create a root `CLAUDE.md` that imports the shared project instructions and links to rules and skills under their loading conditions.
Keep policy and procedures in the linked files, so the proxy cannot become a separate source of guidance.
For a skill with `disable-model-invocation: true`, state the user's explicit request as its link's use condition, so the agent can apply the condition before reading the skill.
Use [Claude Code's import syntax](https://code.claude.com/docs/en/memory) outside code fences in the resulting file, and include only links that exist in the target workspace:

```markdown
# {Project name}

@.github/copilot-instructions.md

Links in that file are relative to `.github/`.

## Instructions

Before starting work, read each linked rule whose `applyTo` matches a file or whose description matches the task.

- [{Rule name}](.github/instructions/{name}.instructions.md): {use condition}.

## Skills

Read the linked `SKILL.md` when its description matches the task or the user requests it.
Read a skill with `disable-model-invocation: true` only when the user names it or explicitly requests its action.

- [{Skill name}](.github/skills/{name}/SKILL.md): {use condition}.
```

## Validate

- [ ] One file owns project guidance; any `CLAUDE.md` beside `.github/copilot-instructions.md` contains only the import, the link-base note, links, and loading conditions.
- [ ] Every named command, path, and file exists in the repository.
