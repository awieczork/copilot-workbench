# awieczork-tools

`awieczork-tools` is a marketplace of agent plugins for GitHub Copilot in VS Code, with a discovery catalog for Claude Code.
This repository contains the plugin source, documentation, and static checks.

The supported VS Code configuration uses the **Local harness**, the chat agent runtime selected as **Local** in an editor window.
The plugins target Windows and Windows Subsystem for Linux (WSL).
Model Context Protocol (MCP) servers provide external tools to agents.

## Plugins

| Plugin | Purpose | GitHub Copilot (Local harness) | Claude Code |
| --- | --- | --- | --- |
| [agent-team](plugins/agent-team/README.md) | Agents and tools for software development and data analysis. | Agents, skills, rules, MCP servers | Skills, MCP servers |
| [agent-plugin-dev](plugins/agent-plugin-dev/README.md) | Authoring, checking, and release of plugins. | Skills | Skills |
| [project-records](plugins/project-records/README.md) | Maintenance of project status, open issues, and changelogs. | Rules, skill | Skill |

Each plugin includes what it needs and does not require the others.
Each plugin README lists its components, requirements, and limits.
Claude Code support is limited to listing and installation; see [Status](#status).

## Install

### GitHub Copilot in VS Code

1. In a VS Code editor window, select the **Local** harness and run **Chat: Open Customizations**.
1. Under **Browse**, select **Configure Marketplaces** and add `awieczork/copilot-workbench`.
1. Install the plugins you need, review the trust prompt, and start a new chat session.

The [installation guide](docs/installation.md) covers Windows and WSL setup, verification, updates, and upgrades from the original `copilot-workbench` plugin.

### Claude Code

```text
/plugin marketplace add awieczork/copilot-workbench
/plugin install agent-team@awieczork-tools
```

Replace `agent-team` with the plugin you need.
The [installation guide](docs/installation.md#claude-code) lists what Claude Code loads from each plugin and how to check it.

## Updates and versions

The marketplace serves the full repository from `main`, so a push changes the available plugin files without a new tag or release.
Each plugin's `plugin.json` holds its version, and its `CHANGELOG.md` records its history.
Releases use `<plugin>/v<version>` tags on [GitHub releases](https://github.com/awieczork/copilot-workbench/releases).
The root [changelog](CHANGELOG.md) records repository and marketplace changes.

## Repository layout

```text
.claude-plugin/marketplace.json   Claude Code catalog
.github/plugin/marketplace.json   GitHub Copilot catalog
.github/                          repository instructions and skill pointers, outside the plugins
docs/                             architecture, installation, development, and references
plugins/<name>/                   one Agent Plugins 1.0 package per plugin
```

## Status

- The supported target is the Local harness in a VS Code editor window on Windows and WSL; the Copilot harness and the Agents window do not run the plugins reliably and remain unsupported.
- The Claude Code catalog lists the same packages without changes; Claude Code runtime compatibility is unverified.
- Installation alone does not prove that a plugin's components work; check them in a fresh session in each environment.
- The owner maintains these plugins for personal use; the repository does not accept external contributions or provide public support.

## Documentation

- [Architecture](docs/ARCHITECTURE.md): package design, catalogs, and component boundaries.
- [Installation](docs/installation.md): setup and verification for each runtime.
- [Development](docs/DEVELOPMENT.md): branches, development workflow, versions, and static checks.
- [References](docs/REFERENCES.md): sources behind the design and its product facts.

## License

The repository and its plugins use the [MIT license](LICENSE).
