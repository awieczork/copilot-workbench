---
name: copilot-customization
description: "Use when creating, changing, or reviewing GitHub Copilot customizations for VS Code: copilot-instructions.md, AGENTS.md, scoped .instructions.md files, custom agents (.agent.md), and Agent Skills (SKILL.md). Supplies the type choice, frontmatter, templates, and writing rules. Not for prompt files, hooks, or MCP server configuration."
argument-hint: "[instructions|agent|skill] [goal]"
---

# Copilot customization

Write GitHub Copilot customizations for VS Code that change agent behavior as intended and load only when they are needed.

## Create or change an artifact

1. Determine the scope: workspace, user profile, or plugin package.
   Take it from the requested path or the repository layout; when neither settles it, ask one question and stop.
2. Choose the type from "Choose the artifact type" below.
   When the requested type does not fit the need, name the mismatch, recommend the fitting type, and ask before writing.
3. Before writing any content, read [Writing guidance](references/writing.md), then read the reference for the chosen type from "Locate the file" below.
4. For an existing artifact, read the whole file and its bundled resources first, and keep every decision outside the requested change.
5. Write the file at the path from the type reference, using its template.
6. Validate the file on disk against the type reference's validation list and the writing checklist, and repair each failure.

The work is done when the file sits at its path, its frontmatter parses, and every item on both validation lists passes.

When a field or behavior is not covered here, read the official documentation linked at the top of the type reference instead of guessing.

## Review artifacts

1. Read the artifact, its bundled resources, and every other customization that can apply to the same task, because conflicts and gaps arise between files.
2. Check it against [Writing guidance](references/writing.md) and the validation list of its type reference.
3. Flag conflicts: two loaded files that give different instructions for the same case, or that disagree on what to deliver, what the agent may do without asking, or what counts as done.
4. Flag silent gaps: a case the artifact must handle that no loaded file covers.
5. Flag over-constraint for current models: blanket "always ask" rules, required reading before every task, required or repeated testing regardless of the change, forceful emphasis, step-by-step recipes where a goal and a reason would do, and caps, refusals, or completion conditions that no observed failure called for.
6. Report the findings in the format below, and change files only when the user asks for fixes.

The review is done when every loaded file was read and every finding names its file and quotes its line.

```markdown
## Findings
- `{path}` — "{quoted line}": {conflict | gap | broken promise | over-constraint | checklist failure}: {issue}; fix: {proposed change}

## Checked
- `{path}`
```

## Choose the artifact type

| Type | Loads | Use for |
| --- | --- | --- |
| Project instructions | On every chat request in the workspace | Guidance that nearly every task needs |
| Scoped instructions | When the agent creates or modifies a file that matches `applyTo`, or when the `description` matches the task | Standards for a language, framework, folder, or kind of task |
| Agent Skill | When the `description` matches the task, or when the user runs it as a slash command | A capability or procedure that only some tasks need, with optional scripts and reference files |
| Custom agent | When the user selects it, or when another agent delegates to it | A role that needs its own tools, model, or a context isolated from the conversation |

Resolve the close calls by these questions:

- **Instructions or skill:** guidance for most tasks belongs in instructions; guidance for specific tasks belongs in a skill.
- **Scoped instructions or skill:** rules tied to the files being edited belong in scoped instructions; a procedure or bundled files for a kind of task belong in a skill.
- **Skill or agent:** work that runs with the current tools and context belongs in a skill; work that needs other tools, another model, or an isolated context belongs in an agent.
- **`copilot-instructions.md` or `AGENTS.md`:** use one of them, never both; choose `AGENTS.md` when other coding agents share the guidance or subfolders need their own guidance.

Prompt files, hooks, and MCP server configuration are outside this skill; say so and stop when the request needs one of them.

## Locate the file

| Type | Workspace path | Agent Plugins 1.0 path | Reference |
| --- | --- | --- | --- |
| Project instructions | `.github/copilot-instructions.md` or `AGENTS.md` | `com.github.copilot/rules/<name>.instructions.md` with `applyTo: "**"` | [Project instructions](references/project-instructions.md) |
| Scoped instructions | `.github/instructions/<name>.instructions.md` | `com.github.copilot/rules/<name>.instructions.md` | [Scoped instructions](references/instructions.md) |
| Custom agent | `.github/agents/<name>.agent.md` | `com.github.copilot/agents/<name>.agent.md` | [Custom agents](references/agents.md) |
| Agent Skill | `.github/skills/<name>/SKILL.md` | `skills/<name>/SKILL.md` | [Agent Skills](references/skills.md) |

Each reference lists the user-level locations, the frontmatter, a template, and a validation list for its type.

## Gotchas

- YAML frontmatter fails silently: a value with an unquoted colon, a tab indent, or a skill `name` that differs from its folder stops the artifact from loading without an error, so quote every string that contains a colon.
