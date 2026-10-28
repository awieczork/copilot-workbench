# Agent Plugins 1.0 packaging

Use the Agent Plugins 1.0 format for every package under `plugins/<name>/`.

## Package layout

```text
plugins/<name>/
  plugin.json
  README.md
  CHANGELOG.md
  skills/<skill-name>/SKILL.md
  mcp.json
  com.github.copilot/
    agents/
    rules/
    commands/
    hooks/hooks.json
```

The `skills/`, `mcp.json`, and `com.github.copilot/` components are optional when a package does not use them.
Keep every component path and relative Markdown link inside the plugin directory.
Each repository package also includes `README.md` and `CHANGELOG.md` as repository files, not Agent Plugins components; release preflight requires a non-empty changelog entry for the manifest version.

## Manifest

Put exactly one portable manifest at the package root and set `$schema` to `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`.
The Agent Plugins format requires `$schema` and `name`; `version` is optional in that format, but this repository's release preflight requires a semantic version.
Allowed top-level fields are `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, and `extensions`.
The name is 1-64 lowercase ASCII letters, digits, hyphens, or periods, begins and ends with a letter or digit, and contains neither `--` nor `..`.
`author` accepts only string values for `name`, `email`, and `url`; `keywords` is an array of strings; every `extensions` value is an object.
Do not add `agents`, `skills`, or `mcpServers` path fields to `plugin.json`; Agent Plugins 1.0 discovers components from fixed locations.

## Component locations

Put each skill in `skills/<skill-name>/SKILL.md` with any required resources below that skill directory.
Put portable MCP server definitions in root `mcp.json`, using the Agent Plugins MCP format with `mcpServers` at its top level.
Put Copilot-specific agents, rules, optional commands, and hooks in `com.github.copilot/agents/`, `com.github.copilot/rules/`, `com.github.copilot/commands/`, and `com.github.copilot/hooks/`.
Do not use the legacy `.mcp.json` file or root-level `agents/`, `rules/`, `commands/`, or `hooks/` directories in a package.

## Marketplace

The repository catalog is `.github/plugin/marketplace.json`; it lists packages using `./plugins/<name>` relative to the repository root.
Keep each catalog name, package directory name, and manifest name identical and unique.
Do not list paths that traverse outside `plugins/`, and do not use component symlinks that resolve outside the package.
The checker also rejects package manifests below `plugins/` that are not listed in the catalog.

## Check scope

Run `uv run --no-project .github/skills/build-plugin/scripts/check_package.py` from the repository root.
The checker accepts an empty `plugins` array and checks manifest field types and allowed keys, name patterns, catalog identity, package layout, local Markdown links, and path containment.
For `mcp.json`, it checks the canonical schema identifier, required and allowed fields, JSON types, reserved environment keys, and local command and working-directory containment.
It uses only the Python standard library and provides a bounded list of path-specific errors.
It is a local scaffold checker, not a complete semantic implementation of the specification and not a client installation or runtime test.
It does not verify URL semantics, remote service behavior, client-specific component behavior, or installation compatibility.

For the normative package and manifest contracts, see the [Agent Plugins manifest documentation](https://agent-plugins.org/plugin-authors/manifest), [MCP server documentation](https://agent-plugins.org/plugin-authors/mcp-servers), and [VS Code plugin reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference).
