# [Scoped instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

Scoped instructions are `*.instructions.md` files that VS Code attaches when the agent edits matching files or when their description matches the task.

## Locations

| Scope | Location |
| --- | --- |
| Workspace | `.github/instructions/<name>.instructions.md` |
| User | VS Code profile storage for the Local agent, or `~/.copilot/instructions/` for Agent Host sessions |
| Agent Plugins 1.0 package | `com.github.copilot/rules/<name>.instructions.md` |

Use a lowercase kebab-case file name with the `.instructions.md` suffix.

## Frontmatter

```yaml
---
name: "Python Tests"
description: "Use when writing or updating Python unit tests and fixtures"
applyTo: "tests/**/*.py"
---
```

| Field | Required | Behavior |
| --- | --- | --- |
| `name` | No | Display name; defaults to the file name |
| `description` | No | Lets the agent load the file when the task matches, including tasks that edit no file |
| `applyTo` | No | Glob relative to the workspace root; attaches the file when the agent creates or modifies a matching file |

When a file has neither `description` nor `applyTo`, it loads only when the user attaches it manually.

## Activation

| Mode | Trigger | Use for |
| --- | --- | --- |
| `applyTo` | The agent creates or modifies a matching file | Language, framework, or folder standards |
| `description` | The agent judges the task relevant | Task-based guidance, such as migrations or reviews |
| Manual | The user adds the file as context | Occasional guidance |

`applyTo` accepts these forms:

```yaml
applyTo: "**/*.py"              # every Python file
applyTo: "src/api/**/*.ts"      # one folder and extension
applyTo: ["src/**", "lib/**"]   # several patterns, any may match
applyTo: "**"                   # every file; use only for rules that apply everywhere
```

Add a `description` as well as `applyTo` when the rules must reach a review or question that edits no file.

## Template

````markdown
---
description: "{Use when ... trigger phrases}"
applyTo: "{glob}"
---

# {Topic}

## {Concern}

- {Rule}, because {reason}.

## Example

```{language}
{short example of the shape the rules describe}
```
````

Add the `Example` section only when a short example shows a shape the rules describe.

## Principles

- Keep one concern in each file, such as testing, styling, or documentation.
- Group the rules under one heading per concern.
- Test each glob against an intended path, a nested path, and a near-miss path.

## Anti-patterns

- **Vague description:** "Helpful coding tips" never matches a task.
- **Broad glob:** `applyTo: "**"` for rules that concern one file type.
- **Mixed concerns:** testing, API design, and styling in one file.
- **Copied docs:** pasting documentation instead of linking it.
- **Foreign fields:** Claude `paths` or GitHub.com-only fields, which VS Code does not read for this file type.

## Validate

- [ ] The file sits at a documented location with the `.instructions.md` suffix.
- [ ] Frontmatter parses, and `applyTo` is a string or an array of strings.
- [ ] Every glob matches its intended paths and misses its near-miss paths.
- [ ] A `description` exists when the rules must load for requests that edit no file.
- [ ] The file covers one concern.
