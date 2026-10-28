# Packaging

Package the plugin in the Copilot plugin format: a root `plugin.json` without `$schema`, with every component in its folder at the plugin root.
The [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference) is the authority for the manifest and the component locations, because the Copilot runtime behind Agent Host loads the plugin.
For VS Code behavior, follow [Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins) and [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-skills).
The [`ARCHITECTURE.md` package format note](../../../../ARCHITECTURE.md) gives the reason for this format and the condition for a change to Agent Plugins 1.0.

## Place every file

| Component | Path | Placement constraint |
| --- | --- | --- |
| Manifest | `plugin.json` | Exactly one, at the plugin root, without `$schema` |
| Skill | `skills/<skill-name>/SKILL.md` | Only immediate children of `skills/` are scanned |
| Skill support file | A path below `skills/<skill-name>/` | Referenced by `SKILL.md` when the agent must find it |
| MCP servers | `.mcp.json` | Plugin root only |
| Custom agent | `agents/<name>.agent.md` | |
| Rule | `rules/<name>.instructions.md` | VS Code default folder; no manifest field |
| Package metadata | `README.md`, `CHANGELOG.md` | Plugin root; not loaded as a component |
| Marketplace catalog | `.github/plugin/marketplace.json` | Distribution metadata; the only published file under `.github/` |

For any other component, such as commands or hooks, take the path from the GitHub Copilot CLI plugin reference.
Keep every packaged path inside the plugin root, copying a file instead of linking to it, because a client resolves component paths against the plugin root.
Leave generated runtime state, temporary results, and repository-only inputs out of the package.

## Marketplace catalog

Keep one catalog entry whose `name` matches root `plugin.json` and whose `source` is `./`, because the marketplace distributes this repository's single root plugin.
Keep the plugin version and descriptive metadata in `plugin.json` instead of duplicating them in the catalog.
Follow [GitHub's marketplace format](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace).

## plugin.json

- Write only fields that the GitHub Copilot CLI plugin reference documents; only `name` is required.
- Leave out `$schema`, because a root `plugin.json` with the Agent Plugins schema switches VS Code and the Copilot CLI to Agent Plugins 1.0, which ignores the root component folders.
- Declare `agents`, `skills`, and `mcpServers` with relative paths in the reference's form (`"agents/"`, `"skills/"`, `".mcp.json"`), so that the manifest states where each component is.
- Leave rules to the `rules/` default folder, because no official page documents a manifest field for rules and VS Code with Agent Host loads that folder from an installed plugin.

## .mcp.json

- Write only `mcpServers` at the top level.
- Give a stdio server `type` and `command`, with optional `args`, `env`, and `cwd`.
- Translate a native VS Code MCP block field by field rather than copying it, because a VS Code `mcp.json` uses `servers` and workspace keys such as `inputs`, which a plugin `.mcp.json` does not define.
- Write `command` as one executable token, a `./` path for an executable the package bundles and a bare name for one it does not, without relying on a `PATH` set in `env`, and move every argument into `args`.
- Use `${PLUGIN_ROOT}` for packaged files, only in `args`, `env` values, and `cwd`.
- Keep secrets and work-specific connection values in local configuration, and refer to them by their local configuration names.

## Check static conformance

Run `uv run .github/skills/build-plugin/scripts/check_package.py` from the repository root after any package change, and repair each failure it prints.
It prints `ok`, or one `{path}: {problem}` line per failure and exits with status 1; it does not check tool names, model names, or the `README.md` inventory, so check those by hand.
