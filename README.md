# copilot-workbench

`copilot-workbench` is the owner-maintained repository for the `awieczork-tools` marketplace for GitHub Copilot in VS Code.
It provides independent plugins for software development, data analysis, and project records.

## Plugins

- [agent-team](plugins/agent-team/README.md): agents, skills, rules, and tools for software development and data analysis.
- [agent-plugin-dev](plugins/agent-plugin-dev/README.md): skills for authoring, checking, and releasing plugins.
- [project-records](plugins/project-records/README.md): rules and a skill for maintaining project status, open issues, and changelogs.

Each plugin includes what it needs and does not require the others.
See each plugin's README for its components and requirements.

## Install

### GitHub Copilot

In a VS Code editor window, select the **Local** harness and open **Chat: Open Customizations**.
Under **Browse**, select **Configure Marketplaces**, add `awieczork/copilot-workbench`, and install the plugins you need.

For Windows and Windows Subsystem for Linux (WSL) setup, removal of older plugins, updates, and verification, follow the [installation guide](docs/installation.md).

### Claude Code catalog

In Claude Code, register the separate [discovery catalog](.claude-plugin/marketplace.json):

```text
/plugin marketplace add awieczork/copilot-workbench
```

The catalog lists the same packages without changing their payloads; Claude Code runtime compatibility remains unverified.
See the [discovery scope and checks](docs/installation.md#claude-code-catalog-discovery) before using the packages in Claude Code.

## Good to know

- The supported target is the Local harness in the VS Code editor window on Windows and WSL.
  The Copilot harness and Agents window remain unsupported while [OI-05](OPEN-ISSUES.md) applies.
- The marketplace serves the full repository from `main`, so a push changes available plugin files without a new tag or release.
- Installation alone does not prove that a plugin's components work; check them in a fresh session in each environment.
- The owner maintains these plugins for personal use; the repository does not accept external contributions or provide public support.

## Project information

- [Architecture](docs/ARCHITECTURE.md): package boundaries and development workflow.
- [Project status](PROJECT-STATUS.md): current work and blockers.
- [References](docs/REFERENCES.md): sources behind the design.
- [Changelog](CHANGELOG.md): repository and marketplace changes; each plugin keeps its own release history.
