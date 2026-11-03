# Installation

The GitHub Copilot steps use VS Code `1.144` as the setup baseline; they do not establish runtime compatibility.
The supported GitHub Copilot configuration is the **Local** harness in an editor window, on Windows and Windows Subsystem for Linux (WSL).
Local is a harness name, not a synonym for execution on your own computer.
No repository clone or manual copying of agents, rules, or skills is required.

## 1. Prepare Windows and WSL

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

## 2. Remove the original plugin if present

For a new installation, skip this step.
Otherwise, uninstall `copilot-workbench` before installing `agent-team`, so both copies do not load together.
Run **Chat: Open Customizations**, select **Plugins**, open `copilot-workbench`, and select **Uninstall**.
The **Plugins** page also lists a copy installed with `/plugin` or the Copilot CLI; uninstall that copy through the interface that installed it.
Check both Windows and WSL contexts for old copies.

Do not load `project-records` beside `agent-team` `0.2.0`, because that version contains the same three rule identities.
The split requires `agent-team` `0.3.0` or newer.

## 3. Install on Windows

Open a Windows folder in an editor window without a WSL connection, and select the **Local** harness in a new chat.
Install through the Agent Customizations editor:

1. Run **Chat: Open Customizations**, select **Browse**, open the source menu, and select **Configure Marketplaces**.
1. Select **Add Marketplace** and enter `awieczork/copilot-workbench`, unless it is already listed.
1. Return to **Browse**, select that marketplace, and install `agent-team`.
1. Review the trust prompt, then confirm on the **Plugins** page that `agent-team` is enabled for the current profile if you want to use it across projects, rather than only in this workspace.

When the **Browse** page is not available, select **Plugins** and then **Browse Marketplace**.
Check that the installed `agent-team` version matches the [package manifest on `main`](https://github.com/awieczork/copilot-workbench/blob/main/plugins/agent-team/plugin.json).
Listing a plugin alone does not establish that its agents, rules, or tools work.

## 4. Configure WSL

Open a project folder in the Linux home directory from a WSL terminal with `code .`.
Confirm that the editor's lower-left remote indicator identifies the intended WSL distribution.
In that WSL-connected window, inspect the **Plugins** page first, and repeat step 3 only when `agent-team` is not available there.

Do not assume that a Windows installation, executable, or credential is available to the WSL host.
Do not copy plugin installation directories between systems.
Configure tools, environment variables, and service access where their processes run.
The [agent-team requirements](../plugins/agent-team/README.md#requirements), [Context7 setup](../plugins/agent-team/README.md#context7-api-key), and [database access](../plugins/agent-team/README.md#database-access) describe the package-specific configuration.
Keep keys and credentials out of chat and tracked files.
Bundled MCP servers can start when the plugin is enabled; configure their access before testing them.

## 5. Verify both environments

In each of Windows and WSL, start a new **Local** session in a test folder outside this workbench, so repository customizations do not mask plugin discovery.
Check the installed source and version, agent and rule discovery in Agent Customizations, and skill availability in a fresh session.
Select `lead` and ask it to delegate a read-only folder inspection to `explorer`, without edits or external services; confirm that the delegation actually runs.
Workers need not appear in the main agent picker.
Check required tools and script execution separately.
A database connection failure is separate from plugin discovery and does not by itself establish an installation failure.

Record results separately for Windows and WSL.
Successful installation alone does not prove runtime support.

## Updates and optional tools

Use **Check for and Apply Updates** on the **Plugins** page or **Chat: Update Plugins**.
Start a fresh session and check the version and behavior after updating.
Plugin updates can also run automatically when `extensions.autoUpdate` is enabled; do not assume installations stay pinned between checks.

Install `agent-plugin-dev` only where you need the development tools, from the same marketplace in the Agent Customizations editor.
The packages do not require each other, and the catalog has no compatibility alias for `copilot-workbench`.
This workbench uses matching repository discovery pointers to the canonical plugin authoring and lifecycle skills; real-client pointer selection remains unverified.
The [VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) describes plugin management and its client requirements.

## Claude Code catalog discovery

The separate [Claude Code catalog](../.claude-plugin/marketplace.json) lists the same three packages without changing their payloads.
This catalog enables registration and listing; it does not establish Claude Code runtime compatibility.

With Claude Code installed, run these commands in your shell:

```bash
claude --version
claude plugin marketplace add awieczork/copilot-workbench
claude plugin list --json --available
```

Check that the combined installed and available lists contain `agent-team@awieczork-tools`, `agent-plugin-dev@awieczork-tools`, and `project-records@awieczork-tools`.
Registration does not add the marketplace to Anthropic's official directory.

| Component | Claude Code discovery scope |
| --- | --- |
| `skills/` | The existing directories match Claude Code's standard layout; skill behavior remains unverified. |
| `com.github.copilot/agents/` and `com.github.copilot/rules/` | The catalog does not register these Copilot-specific components for Claude Code. |
| `mcp.json` | The catalog does not declare these servers, and the filename differs from Claude Code's default `.mcp.json`. |

The catalog omits plugin versions to avoid a second version authority; Claude Code uses source-based versions when neither its manifest nor its entry supplies one.
The existing root `plugin.json` files remain Agent Plugins 1.0 manifests; the packages have no `.claude-plugin/plugin.json` manifests.
The marketplace entries supply Claude Code's metadata without adding files to the packages.

To validate a checkout without registering it, run `claude plugin validate .` from the repository root.
Static checks and successful listing do not prove that skills, tools, or model references work.
Test skill behavior in a fresh session in a folder outside this workbench, so repository instructions do not mask plugin behavior.
See Anthropic's [marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference) and [manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference) for the catalog and component rules.
