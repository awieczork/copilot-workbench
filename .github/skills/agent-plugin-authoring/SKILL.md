---
name: agent-plugin-authoring
description: "Use when work changes plugin.json, mcp.json, package structure, component placement, packaged paths, or the static integration of com.github.copilot components. Supplies Agent Plugins 1.0 packaging and static-conformance rules. Not for component wording, installation, runtime operation, or publication."
---

# Agent plugin authoring

Apply these rules within the user's current task rather than running a separate packaging workflow or producing a separate report.

## Keep the responsibility bounded

- Govern the Agent Plugins 1.0 package structure, manifests, component placement, path containment, and static conformance.
- Treat skills and Model Context Protocol (MCP) servers as portable Agent Plugins 1.0 components.
- Treat files under `com.github.copilot/` as VS Code client extensions rather than portable component types.
- Accept the content of a skill, agent, command, instruction, or hook as task input.
- Validate load-critical metadata and placement without rewriting the component's instructional content.
- Keep installation, editor settings, interactive surfaces, runtime behavior, credential handling, updates, release timing, tagging, and publication outside this skill.

## Recognize the package

Treat a directory as Agent Plugins 1.0 only when root `plugin.json` declares:

```json
{
    "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
    "name": "example-plugin"
}
```

The manifest selects the package format before component discovery.
Do not infer Agent Plugins 1.0 semantics from directory names alone.
Read [Manifest and MCP reference](references/manifest.md) when work creates, changes, or validates `plugin.json` or `mcp.json`.

## Place every file

```text
<plugin-root>/
├── plugin.json                      # required
├── mcp.json                         # optional MCP servers
├── skills/<skill-name>/SKILL.md     # optional skills
├── scripts/                         # optional hook scripts and supporting executables
├── servers/                         # optional bundled MCP server binaries
└── com.github.copilot/              # optional Copilot file formats
    ├── agents/<name>.agent.md
    ├── commands/<name>.prompt.md
    ├── rules/<name>.instructions.md
    └── hooks/hooks.json
```

| Component | Path | Placement constraint |
| --- | --- | --- |
| Manifest | `plugin.json` | Exactly one, at the plugin root |
| Skill | `skills/<skill-name>/SKILL.md` | Only immediate children of `skills/` are scanned; a skill one level deeper is never discovered |
| MCP server | `mcp.json` | Root only; uses the plugin MCP schema, not the native VS Code `servers` format |
| Custom agent | `com.github.copilot/agents/<name>.agent.md` | Copilot role definition |
| Prompt file | `com.github.copilot/commands/<name>.prompt.md` | Copilot prompt-file format |
| Instruction file | `com.github.copilot/rules/<name>.instructions.md` | Copilot instruction-file format |
| Hook | `com.github.copilot/hooks/hooks.json` | One JSON file, not a directory of files |
| Hook script or bundled server executable | A contained path inside the plugin root | Referenced from `hooks.json` or `mcp.json` with the path form required by that format |
| Skill support file | A path below `skills/<skill-name>/` | Remains inside its skill directory and is referenced by `SKILL.md` when the agent must discover it |
| Other packaged support file | A path inside the plugin root | Referenced by a component and included with the package |
| Package metadata | `README.md`, `LICENSE`, `CHANGELOG.md` | Plugin root; not loaded as a component |

Keep every packaged path resolvable inside the plugin root.
Replace any symlink, junction, or relative path that resolves outside the root with a copy inside it, because VS Code rejects a path that leaves the package.
In a stdio MCP server, `${PLUGIN_DATA}` may name writable server state outside the packaged files in `args`, `env`, and `cwd`.

Include component support files that are referenced by packaged configuration or content.
Exclude generated runtime state, temporary results, and unrelated repository inputs from the package.

## Name a skill inside the plugin

VS Code invokes a plugin skill as the skill command `/<plugin-name>:<skill-name>`, adding the prefix itself.
Keep the prefix out of the skill `name`, because a prefixed name makes the skill fail to load.

A plugin `name` may contain a period; a skill `name` may not.
Rewrite the plugin name in plain kebab-case before reusing it as a skill name, because a period there makes the skill fail to load.

Give each immediate child of `skills/` that contains `SKILL.md` a `name` equal to its directory name, with 1-64 lowercase letters, digits, or hyphens, starting and ending with a letter or digit, and no consecutive hyphens.

## Check static conformance

Apply every relevant check to changed package files and relationships:

- Parse every changed JSON document and YAML frontmatter block.
- Validate `plugin.json` and `mcp.json` against their declared schemas when the schemas are reachable, because VS Code loads a manifest or MCP entry that the specification rejects.
- Apply the normative Agent Plugins specification when its text adds a semantic constraint or conflicts with a machine-readable schema.
- Verify every immediate child of `skills/` that contains `SKILL.md` against the Agent Skills frontmatter, directory-name, resource-link, and path-containment requirements.
- Verify each `com.github.copilot` file has the documented suffix, canonical path, and parseable format for its type.
- Resolve every packaged path, symlink, junction, component reference, and relative resource link inside the plugin root.
- Read `plugin.json`, `mcp.json`, and hook commands in full for machine-specific absolute paths and unsupported fields.

## Use current authorities

Use these sources when a package rule is absent from the bundled reference or current evidence contradicts it:

- [Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins) for VS Code package structure and `com.github.copilot` extensions.
- [Agent Plugins specification](https://agent-plugins.org/specification) for the normative portable package contract.
- [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills) for load-critical skill metadata recognized by VS Code.

Keep the bundled reference as a concise working summary, not as authority over current primary documentation.
