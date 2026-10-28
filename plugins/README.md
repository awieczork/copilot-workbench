# Plugin packages

This repository's `ds-tools` catalog follows GitHub Copilot CLI marketplace discovery, while plugin package contents use Agent Plugins 1.0 where the target client supports it.
The catalog is [`.github/plugin/marketplace.json`](../.github/plugin/marketplace.json) and currently has no entries.
This file documents the future package layout; it is not a plugin payload.

## Package layout

Create each package under `plugins/<name>/` and add a catalog source of `./plugins/<name>`, relative to the repository root, only when that package exists.
Keep each package self-contained; do not depend on another plugin's files or use paths outside the package by default.

```text
plugins/
  <name>/
    plugin.json
    README.md
    CHANGELOG.md
    skills/                   # optional portable skills
      <skill>/
        SKILL.md
    mcp.json                  # optional portable MCP configuration
    com.github.copilot/       # optional Copilot-specific components
      agents/                 # optional agents
      rules/                  # optional rules
      commands/               # optional client-specific commands
      hooks/                  # optional client-specific hooks
```

## Manifest

Use the canonical Agent Plugins 1.0 schema and keep the portable manifest at the package root as `plugin.json`.
This minimal manifest is an example only; do not create it at the repository root or add an example plugin directory.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "example-plugin",
  "version": "0.1.0"
}
```

## Component boundaries

Agent Plugins 1.0 discovers skills under `skills/` and MCP server configuration from root `mcp.json`; do not add component path fields to `plugin.json`.
Use `mcp.json`, not the legacy `.mcp.json` path.
Put Copilot-specific files under `com.github.copilot/` and treat commands and hooks as client-specific, not portable components.
Check the target client's current documentation before relying on a component or claiming compatibility.

## Versions and validation

Version each plugin in its own `plugin.json` and tag releases as `<plugin-name>/v<version>`.
Keep marketplace changes in the root `CHANGELOG.md` and package changes in each plugin's `CHANGELOG.md`.
Validate the package format and target-client behavior separately from the marketplace catalog.
The official marketplace guidance assumes one or more plugin packages; because this catalog is empty, no consumer installation smoke test is possible and no installation success is claimed.

## References

- [VS Code Agent Plugins authoring reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference)
- [Agent Plugins manifest](https://agent-plugins.org/plugin-authors/manifest)
- [GitHub Copilot CLI marketplace guidance](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace)
