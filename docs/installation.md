# Installation

This guide installs the `awieczork-tools` plugins in GitHub Copilot for VS Code and registers the catalog in Claude Code.
No repository clone or manual copying of agents, rules, or skills is required.

## GitHub Copilot in VS Code

The steps use VS Code `1.144` as the setup baseline; they do not establish runtime compatibility.
The **Local harness** is the chat agent runtime selected as **Local** in a VS Code editor window.
The supported configuration uses this harness on Windows and Windows Subsystem for Linux (WSL).
Local is a harness name, not a synonym for execution on your own computer.

### 1. Prepare Windows and WSL

Install VS Code on Windows, sign in to GitHub Copilot, and confirm that a chat session with the **Local** harness can start.
If Local is not available, check the experimental `chat.editor.localAgent.enabled` setting; organization policy can restrict the choice.
For Linux work, install a WSL distribution and the [WSL extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-wsl); do not install a separate Linux desktop copy of VS Code.
See the [VS Code WSL setup guide](https://code.visualstudio.com/docs/remote/wsl).

Install Git, Node.js with `npx`, and `uv` with `uvx` separately on Windows and in WSL.
Check each command in PowerShell, then in a WSL terminal:

```text
git --version
node --version
npx --version
uv --version
uvx --version
```

These checks confirm terminal access only.
After changing tools or environment variables, fully quit and restart VS Code; restart the WSL server as needed to pick up its environment.

### 2. Install on Windows

If you used the original `copilot-workbench` plugin, first follow [Upgrade from copilot-workbench](#upgrade-from-copilot-workbench).

Open a Windows folder in an editor window without a WSL connection, and select the **Local** harness in a new chat.
Install through the Agent Customizations editor:

1. Run **Chat: Open Customizations**, select **Browse**, open the source menu, and select **Configure Marketplaces**.
1. Select **Add Marketplace** and enter `awieczork/copilot-workbench`, unless it is already listed.
1. Return to **Browse**, select that marketplace, and install `agent-team`.
1. Review the trust prompt, then confirm on the **Plugins** page that `agent-team` is enabled for the current profile if you want to use it across projects, rather than only in this workspace.

When the **Browse** page is not available, select **Plugins** and then **Browse Marketplace**.
Check that the installed `agent-team` version matches the [package manifest on `main`](https://github.com/awieczork/copilot-workbench/blob/main/plugins/agent-team/plugin.json).

Install `agent-plugin-dev` and `project-workflow` the same way, only where you need them.
The packages do not require each other.

### 3. Configure WSL

Open a project folder in the Linux home directory from a WSL terminal with `code .`.
Confirm that the editor's lower-left remote indicator identifies the intended WSL distribution.
In that WSL-connected window, inspect the **Plugins** page first, and repeat step 2 only when `agent-team` is not available there.

Do not assume that a Windows installation, executable, or credential is available to the WSL host.
Do not copy plugin installation directories between systems.
Configure tools, environment variables, and service access where their processes run.
The [agent-team requirements](../plugins/agent-team/README.md#requirements) and [configuration](../plugins/agent-team/README.md#configuration) describe the package-specific setup.
Keep keys and credentials out of chat and tracked files.
Bundled Model Context Protocol (MCP) servers can start when the plugin is enabled; configure their access before testing them.

### 4. Verify both environments

In each of Windows and WSL, start a new **Local** session in a test folder outside this repository, so repository customizations do not mask plugin discovery.

1. Check the installed source and version, and agent and rule discovery in Agent Customizations.
1. Check skill availability in a fresh session.
1. Select `lead` and ask it to delegate a read-only folder inspection to `explorer`, without edits or external services; confirm that the delegation actually runs.
1. Check required tools and script execution separately.

Workers need not appear in the main agent picker.
A database connection failure is separate from plugin discovery and does not by itself establish an installation failure.
Record results separately for Windows and WSL.

### Updates

Use **Check for and Apply Updates** on the **Plugins** page or **Chat: Update Plugins**.
Start a fresh session and check the version and behavior after updating.
Plugin updates can also run automatically when `extensions.autoUpdate` is enabled; do not assume installations stay pinned between checks.

The [VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) describes plugin management and its client requirements.

## Claude Code

The separate [Claude Code catalog](../.claude-plugin/marketplace.json) lists the same three packages without changing their payloads.
It enables registration and listing and declares the existing `agent-team` MCP servers; it does not establish Claude Code runtime compatibility.

### Register and install

With Claude Code installed, run these commands in your shell:

```bash
claude --version
claude plugin marketplace add awieczork/copilot-workbench
claude plugin list --json --available
```

Check that the combined installed and available lists contain `agent-team@awieczork-tools`, `agent-plugin-dev@awieczork-tools`, and `project-workflow@awieczork-tools`.
Marketplace registration does not install or enable the listed plugins, and it does not add the marketplace to Anthropic's official directory.
Install a plugin with `/plugin install <plugin>@awieczork-tools`.

### What Claude Code loads

| Component | Claude Code scope |
| --- | --- |
| `skills/` | The existing directories match Claude Code's standard layout; skill behavior remains unverified. |
| `com.github.copilot/agents/` and `com.github.copilot/rules/` | The catalog does not register these Copilot-specific components for Claude Code. |
| `agent-team` MCP servers | The catalog's `mcpServers` field points to `./mcp.json` within the plugin; native loading and server connections remain unverified. |

### Verify

When `agent-team` is enabled, Claude Code can start both bundled MCP servers automatically.
Before a live check, configure the [agent-team requirements](../plugins/agent-team/README.md#requirements) where Claude Code runs, and enable the plugin only when those processes may start.

1. Enable the plugin in a fresh session in a test folder outside this repository, so repository instructions do not mask plugin behavior.
1. Run `/mcp` and check for `plugin:agent-team:context7` and `plugin:agent-team:awslabs.redshift-mcp-server`.
1. Record whether each server is listed separately from whether it connects and exposes tools; a connection failure does not by itself mean discovery failed.
1. Test skill behavior in the same session.

To validate a checkout without registering it, run `claude plugin validate .` from the repository root.
Static checks and successful listing do not prove that skills, tools, or model references work.
The [architecture](ARCHITECTURE.md#catalogs-and-runtimes) explains how the catalog maps the packages without Claude Code manifests.

## Upgrade from copilot-workbench

The original single plugin was named `copilot-workbench`; `agent-team` replaces it, and the catalog has no compatibility alias.
For a new installation, skip this section.

1. Run **Chat: Open Customizations**, select **Plugins**, open `copilot-workbench`, and select **Uninstall**, so both copies do not load together.
1. Uninstall a copy installed with `/plugin` or the Copilot command-line interface (CLI) through the interface that installed it; the **Plugins** page also lists such copies.
1. Check both Windows and WSL contexts for old copies.

Do not load `project-workflow` beside `agent-team` `0.2.0`, because that version contains the same three rule identities.
The split requires `agent-team` `0.3.0` or newer.

## Upgrade from project-records

`project-workflow` replaces `project-records` and contains its rules and record skill; the catalog has no compatibility alias.
Uninstall `project-records` before you install `project-workflow`, so the same rule and skill identities do not load twice.
