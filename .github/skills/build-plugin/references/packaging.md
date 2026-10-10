# Packaging

Treat skills and Model Context Protocol (MCP) servers as portable Agent Plugins 1.0 components, and files under `com.github.copilot/` as VS Code client extensions.
The [Agent Plugins specification](https://agent-plugins.org/specification) is the authority: validate against [the plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and [the MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json), and follow the specification where a schema differs.
For VS Code behavior, follow [Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins) and [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills).

## Place every file

| Component | Path | Placement constraint |
| --- | --- | --- |
| Manifest | `plugin.json` | Exactly one, at the plugin root; `"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"` selects Agent Plugins 1.0 semantics |
| Skill | `skills/<skill-name>/SKILL.md` | Only immediate children of `skills/` are scanned |
| Skill support file | A path below `skills/<skill-name>/` | Referenced by `SKILL.md` when the agent must find it |
| MCP servers | `mcp.json` | Plugin root only |
| Custom agent | `com.github.copilot/agents/<name>.agent.md` | |
| Rule | `com.github.copilot/rules/<name>.instructions.md` | |
| Package metadata | `README.md`, `CHANGELOG.md` | Plugin root; not loaded as a component |

For any other component, such as commands, hooks, or automations, take the path from the VS Code Agent Plugins page.
Keep every packaged path inside the plugin root, copying a file instead of linking to it, because the specification requires a client to reject a path that leaves the package.
Leave generated runtime state, temporary results, and repository-only inputs out of the package.

## plugin.json

- Write only the schema's fields; the top level is closed, and only `$schema` and `name` are required.
- Validate the manifest yourself, because VS Code ignores unknown and malformed optional fields without reporting them.
- Carry Copilot-specific configuration under `extensions["com.github.copilot"]`, and add a key there only when current VS Code documentation defines it and its effect, because VS Code discards an unknown top-level field without applying it.

## mcp.json

- Write only `$schema` and `mcpServers` at the top level, with the same schema version as `plugin.json`, because a mismatch disables every MCP server of the plugin.
- Give a stdio server `type` and `command`, with optional `args`, `env`, and `cwd`, and validate each entry against the schema, because a foreign field invalidates the entry under the specification; for a remote server or an explicit `cwd`, read §7.2 of the specification.
- Translate a native VS Code MCP block field by field rather than copying it, because the MCP schema rejects its keys, such as `servers`, `inputs`, `sandbox`, the `http` type, `oauth`, `envFile`, `dev`, and `sandboxEnabled`.
- Write `command` as one executable token, a `./` path for an executable the package bundles and a bare name for one it does not, without relying on a `PATH` set in `env`, and move every argument into `args`.
- Use `${PLUGIN_ROOT}` for packaged files and `${PLUGIN_DATA}` for writable server state, only in `args`, `env` values, and `cwd`.
- Keep secrets and work-specific connection values in local configuration, and refer to them by their local configuration names.

## Check static conformance

Run `uv run .github/skills/build-plugin/scripts/check_package.py` from the repository root after any package change, and repair each failure it prints.
It checks the payload paths (`plugin.json`, `mcp.json`, `skills/`, `com.github.copilot/`, `README.md`, `CHANGELOG.md`): both manifests parse and validate against their declared schemas, the schema versions match, the manifests hold no absolute paths, every frontmatter block parses, each skill `name` equals its folder and meets the name rule, each skill `description` has 1 to 1,024 characters, each `com.github.copilot` file has its documented suffix, every relative link resolves inside the plugin root, and no symlink leaves it.
It prints one `{path}: {problem}` line per failure and exits with status 1 when any check fails, including when a schema cannot be fetched.
