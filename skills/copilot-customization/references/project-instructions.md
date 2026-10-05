# [Project instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

Project instructions hold the guidance that VS Code adds to every chat request in a workspace.

## Choose the file

| File | Location | Use when |
| --- | --- | --- |
| `copilot-instructions.md` | `.github/` | Only GitHub Copilot reads the guidance |
| `AGENTS.md` | Repository root, and optionally subfolders | Other coding agents share the guidance, or subfolders need their own guidance |

Use one of the two files, never both, because two always-on files drift apart and give the agent conflicting guidance.
Nested `AGENTS.md` files in subfolders load for the Local agent only when the user enables `chat.useNestedAgentsMdFiles`, which is off by default.

For personal guidance across workspaces in Agent Host sessions, use `~/.copilot/copilot-instructions.md`.
An Agent Plugins 1.0 package cannot ship either file; it ships a rule with `applyTo: "**"` instead, which attaches only when the agent creates or modifies a file.

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

- Keep only what nearly every task needs, because the file loads on every request.
- Point to existing documentation instead of copying it, and inline only the gotchas that documentation does not cover.
- Give each document pointer the condition for reading it, such as "Use `docs/database.md` for schema changes", because required reading before every task spends context on tasks that do not need it.
- Permit safe routine workflows explicitly, such as running the local test suite and fixing the failures the change caused, because without that permission capable models stop to ask at each step.
- Leave out what linters and formatters already enforce.
- Move rules for one language, framework, or folder into scoped instructions.

## Anti-patterns

- **Both files:** keeping `copilot-instructions.md` and `AGENTS.md` side by side.
- **Kitchen sink:** collecting every preference instead of what matters for most tasks.
- **Copied docs:** pasting the README instead of linking it.
- **Obvious rules:** restating conventions the tooling already enforces.
- **Forced reading:** "Before every edit, read `architecture.md`, `database.md`, and `deployment.md`" instead of naming when each document applies.

## Validate

- [ ] Exactly one of `copilot-instructions.md` and `AGENTS.md` exists at its documented location.
- [ ] Every section applies to most tasks in the workspace.
- [ ] Every named command, path, and file exists in the repository.
- [ ] Rules for a single file type or folder have moved to scoped instructions.
