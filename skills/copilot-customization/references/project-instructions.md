# [Project instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

Project instructions hold the guidance that VS Code adds to every chat request in a workspace.

## Choose the file

| File | Location | Use when |
| --- | --- | --- |
| `copilot-instructions.md` | `.github/` | Only GitHub Copilot reads the guidance |
| `AGENTS.md` | Repository root, and optionally subfolders | Other coding agents share the guidance, or subfolders need their own guidance |

Use one of the two files, never both, because two always-on files drift apart and give the agent conflicting guidance.
The Local agent also loads `CLAUDE.md` by default (`chat.useClaudeMdFile`), so a `CLAUDE.md` beside either file is a second always-on file.
Nested `AGENTS.md` files in subfolders are experimental and load for the Local agent only when the user enables `chat.useNestedAgentsMdFiles`, which is off by default.

For personal guidance across workspaces, use `~/.copilot/copilot-instructions.md`.
An Agent Plugins 1.0 package cannot ship either file; it ships a rule with `applyTo: "**"` instead, which VS Code attaches to every request.

## Frontmatter

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

## Validate

- [ ] Exactly one of `copilot-instructions.md` and `AGENTS.md` exists at its documented location.
- [ ] Every section applies to most tasks in the workspace.
- [ ] Every named command, path, and file exists in the repository.
- [ ] Rules for a single file type or folder have moved to scoped instructions.
