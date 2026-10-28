# copilot-workbench

`copilot-workbench` is the public, owner-maintained repository for the `awieczork-tools` marketplace for GitHub Copilot in VS Code with the Copilot harness in Agent Host.
Each package has one purpose and bundles the resources it needs without requiring another package.

## Packages

| Package | Purpose | Publication state |
| --- | --- | --- |
| [agent-team](plugins/agent-team/README.md) | Agents for software development and data analysis, with supporting skills, rules, and Model Context Protocol (MCP) configuration. | Version `0.2.0` is published; runtime support unverified. |
| [agent-plugin-dev](plugins/agent-plugin-dev/README.md) | Six reusable customization, build, and development lifecycle skills. | Version `0.1.0` is published; runtime support unverified. |

The [catalog](.github/plugin/marketplace.json) lists the packages present on this branch.
The `agent-team` README holds its component inventory and runtime requirements.
It also gives package-specific installation steps with runtime support still unverified; this root guide owns the repository migration instructions.
The development-package README lists its six skills and execution requirements.

## Publication status

Published `main` serves both Agent Plugins 1.0 packages, with separate namespaced tags and GitHub releases.
The catalog no longer lists the original root Copilot-format `copilot-workbench` package.
[OI-03](OPEN-ISSUES.md) remains open until the agents and rules pass checks in a real Copilot Agent Host session.
The owner waived runtime verification on 2026-10-28 and authorized publication without changing the selected format.
This waiver is not evidence of runtime support; namespaced agent and rule loading, skill discovery, package coexistence, and repository pointer selection remain unverified.
See [Project status](PROJECT-STATUS.md) for the migration outcome and [Architecture](ARCHITECTURE.md) for package boundaries.

## Installation

The following steps manage the published packages; runtime support remains unverified.
Run each command separately in a VS Code chat session with the **Copilot** harness selected.

1. Uninstall the original `copilot-workbench` before installing `agent-team`, so both copies do not load together.
   For an installation made through `/plugin`, use:

   ```text
   /plugin uninstall copilot-workbench@awieczork-tools
   ```

   For an installation made through the Extensions view, the Agent Customizations editor, or **Chat: Install Plugin From Source**, uninstall it in the **Agent Plugins - Installed** view or the Agent Customizations editor.
   The editor and `/plugin` use separate inventories; manage an installation through the interface where you installed it.
1. Register the marketplace if it is not already registered, then refresh it:

   ```text
   /plugin marketplace add awieczork/copilot-workbench
   /plugin marketplace update awieczork-tools
   ```

1. Install the replacement and check its status:

   ```text
   /plugin install agent-team@awieczork-tools
   /plugin list
   ```

To update an installation:

```text
/plugin marketplace update awieczork-tools
/plugin update agent-team@awieczork-tools
```

Install the development tools separately when needed:

```text
/plugin install agent-plugin-dev@awieczork-tools
```

The packages do not require each other, and the catalog has no compatibility alias for `copilot-workbench`.
This workbench uses six repository discovery pointers to the canonical development skills; real-client pointer selection remains unverified.
The [VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) describes plugin management and its client requirements.

## Maintenance

The owner maintains these packages for personal use.
Public access supports installation without repository credentials; this repository does not accept external contributions or provide public support.
The root [changelog](CHANGELOG.md) records marketplace and repository changes; [agent-team history](plugins/agent-team/CHANGELOG.md) retains the original package releases, and [development-package history](plugins/agent-plugin-dev/CHANGELOG.md) belongs to that package.
Local and remote `develop` are retired, and `archive/develop-before-marketplace` preserves their frozen tip; further work uses cycle branches and verified squash integration.
Prepare package versions and notes on a cycle before integration; publish one package at a time from clean full-repository `main`, with package-specific tags and separate publication permission.
