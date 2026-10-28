---
name: build-plugin
description: "Use when creating, changing, or reviewing components for a plugin under `plugins/<name>/`. Supplies Agent Plugins 1.0 layout and authoring contracts. Not for commits or release publication."
---

# Build a plugin

Create or revise one selected plugin package while keeping its components portable and correctly placed.
As a subagent, return each question or choice for the owner to the delegating agent instead of asking the owner.

## Procedure

1. Select one explicitly requested package under `plugins/<name>/` and inspect its catalog entry before editing. For an existing package, confirm the matching entry; for a new package, add the matching `./plugins/<name>` entry to `.github/plugin/marketplace.json` in the same change.
2. Read [packaging](references/packaging.md) when changing a manifest, package layout, or component path.
3. Read [the skill contract](references/skill-contract.md) when creating or revising a skill.
4. Put the portable root manifest at `plugins/<name>/plugin.json`, portable skills in `skills/`, and MCP configuration in `mcp.json`.
5. Put Copilot-specific agents and rules under `com.github.copilot/agents/` and `com.github.copilot/rules/`; keep optional commands and hooks under the same namespace.
6. Keep package resources inside the selected plugin directory and link to local files with paths that resolve from the linking file.
7. Run `uv run --no-project .github/skills/build-plugin/scripts/check_package.py` from the repository root after changing package files.

## Boundaries

- Keep edits to an existing package scoped to that package. Creating an explicitly requested new plugin also includes its matching catalog entry in the same change.
- Do not add a root `plugin.json` or unrequested sample or placeholder package payload. An empty catalog is the starting scaffold, not a prohibition on an explicitly requested plugin.
- Treat the checker as a local static scaffold check; a successful run does not establish client installation or runtime compatibility.
- Use one package's own authoring contracts and do not impose a team, worker, or model taxonomy on other plugins.

The work is complete when the selected package passes the static checker and every requested component is present at its Agent Plugins 1.0 location.
