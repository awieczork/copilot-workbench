---
name: copilot-customization
description: "Use when creating, changing, or reviewing a GitHub Copilot customization for VS Code: project instructions, scoped instructions, a custom agent, or an Agent Skill. Supplies the type choice, frontmatter, templates, and writing rules. Not for prompt files, hooks, or MCP server configuration."
argument-hint: "[create|review] [project-instructions|instructions|agent|skill] [goal]"
---

# Copilot customization

Write GitHub Copilot customizations for VS Code that change agent behavior as intended and load only when they are needed.
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.

## Create or change an artifact

1. Determine the scope: workspace, user, or plugin package.
   Take it from the requested path or the repository layout; when neither settles it, ask one question and stop.
2. Choose the type from "Choose the artifact type" below.
   When the requested type does not fit the need, name the mismatch, recommend the fitting type, and ask before writing.
3. Before writing any content, read [Writing guidance](references/writing.md), then read the reference for the chosen type, linked in "Choose the artifact type" below.
4. For an existing artifact, read the whole file and its bundled resources first, and leave unchanged every decision the request does not touch.
5. Write the file at the path from the type reference, using its template.
6. Validate the file on disk against the type reference and the questions in Writing guidance, and repair each failure; the work is done when the file sits at its path and every item passes.

When a field or behavior is not covered here, read the official documentation linked at the top of the type reference instead of guessing.

## Review artifacts

1. Read the artifact, its bundled resources, and every other customization that can apply to the same task, because conflicts and gaps arise between files.
2. Ask the questions in [Writing guidance](references/writing.md) of the artifact, and check it against its type reference.
3. Flag a conflict where two files that load together give different instructions for the same case, and a gap where no loaded file covers a case the artifact must handle.
4. Report the findings in the format below, ordered by impact, and change files only when the user asks for fixes.

The review is done when every loaded file was read and every finding fills the template below.

```markdown
## Findings
1. `{path}:{line}` — "{quoted text}": {conflict | gap | failed question | validation failure}: {issue}; fix: {proposed text or removal}

## Checked
- `{path}`
```

## Choose the artifact type

| Type | Loads | Use for | Reference |
| --- | --- | --- | --- |
| Project instructions | On every chat request in the workspace | Guidance that nearly every task needs | [Project instructions](references/project-instructions.md) |
| Scoped instructions | When the agent creates or modifies a file that matches `applyTo`, or when the `description` matches the task | Standards for a language, framework, folder, or kind of task | [Scoped instructions](references/instructions.md) |
| Agent Skill | When the `description` matches the task, or when the user runs it as a slash command | A capability or procedure that only some tasks need, with optional scripts and reference files | [Agent Skills](references/skills.md) |
| Custom agent | When the user selects it, or when another agent delegates to it | A role that needs its own tools, model, or a context isolated from the conversation | [Custom agents](references/agents.md) |

Resolve the close calls by these questions:

- **Scoped instructions or skill:** rules tied to the files being edited belong in scoped instructions; a procedure or bundled files for a kind of task belong in a skill.
- **Skill or agent:** work that runs with the current tools and context belongs in a skill; work that needs other tools, another model, or an isolated context belongs in an agent.

Prompt files, hooks, and MCP server configuration are outside this skill; say so and stop when the request needs one of them.

## Gotchas

- Quote every frontmatter string that contains a colon and indent with spaces, because a YAML error can drop fields or the whole artifact.
