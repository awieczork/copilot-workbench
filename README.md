# copilot-workbench

`copilot-workbench` is the public, owner-maintained repository for the `awieczork-tools` marketplace for GitHub Copilot in VS Code with the Copilot harness in Agent Host.
Each package has one purpose and bundles the resources it needs without requiring another package.

## Packages

| Package | Purpose | Migration state |
| --- | --- | --- |
| [agent-team](plugins/agent-team/README.md) | Agents for software development and data analysis, with supporting skills, rules, and Model Context Protocol (MCP) configuration. | Relocated locally to `plugins/agent-team/`; runtime verification is pending. |
| `agent-plugin-dev` | Reusable plugin authoring, validation, and development lifecycle capabilities. | Planned; no package or catalog entry exists yet. |

The [catalog](.github/plugin/marketplace.json) lists the packages present on this branch.
The `agent-team` README holds its component inventory and runtime requirements.

## Migration status

The local `repo/marketplace-migration` branch adopts Agent Plugins 1.0; it is not a published replacement for the existing plugin.
Published `main` still serves the root Copilot-format `copilot-workbench` package.
[OI-03](OPEN-ISSUES.md) remains open until the agents and rules pass checks in a real Copilot Agent Host session.
See [Project status](PROJECT-STATUS.md) for the remaining phases and [Architecture](ARCHITECTURE.md) for package boundaries.

## Installation after publication

Use the following steps only after runtime verification and authorized integration publish `agent-team` on `main`.
Run each command separately in a VS Code chat session with the **Copilot** harness selected.

1. Uninstall the original `copilot-workbench` before installing `agent-team`, so both copies do not load together.
   For an installation made through `/plugin`, use:

   ```text
   /plugin uninstall copilot-workbench@awieczork-tools
   ```

   For an installation made through the Agent Customizations editor, uninstall it there instead; that editor and `/plugin` use separate inventories.
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

To update an installation after publication:

```text
/plugin marketplace update awieczork-tools
/plugin update agent-team@awieczork-tools
```

The catalog has no compatibility alias for `copilot-workbench` and does not yet offer `agent-plugin-dev`.
The [VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) describes plugin management and its client requirements.

## Maintenance

The owner maintains these packages for personal use.
Public access supports installation without repository credentials; this repository does not accept external contributions or provide public support.
The root [changelog](CHANGELOG.md) records marketplace and repository changes; [agent-team history](plugins/agent-team/CHANGELOG.md) retains the original package releases.
