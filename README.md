# copilot-workbench

`copilot-workbench` is the public, owner-maintained repository for the `awieczork-tools` marketplace for GitHub Copilot in VS Code.
The supported target is the Local harness in the VS Code editor window on Windows and Windows Subsystem for Linux (WSL); the Copilot harness and the Agents window stay unsupported while [OI-05](OPEN-ISSUES.md) applies.
Each package has one purpose and bundles the resources it needs without requiring another package.

## Packages

| Package | Purpose | Publication state |
| --- | --- | --- |
| [agent-team](plugins/agent-team/README.md) | Agents for software development and data analysis, with supporting skills, rules, and Model Context Protocol (MCP) configuration. | Version [0.4.1](https://github.com/awieczork/copilot-workbench/releases/tag/agent-team/v0.4.1) is published; the owner reports a plugin test. |
| [agent-plugin-dev](plugins/agent-plugin-dev/README.md) | Six reusable customization, build, and development lifecycle skills. | Version [0.1.3](https://github.com/awieczork/copilot-workbench/releases/tag/agent-plugin-dev/v0.1.3) is published; runtime support unverified. |
| [project-records](plugins/project-records/README.md) | Three project-record rules and an automatically selectable skill for evidence-based updates. | Version [0.1.0](https://github.com/awieczork/copilot-workbench/releases/tag/project-records/v0.1.0) is published; runtime support unverified. |

The [catalog](.github/plugin/marketplace.json) lists the packages present on this branch.
The `agent-team` README holds its component inventory and runtime requirements.
It also gives package-specific installation steps; this root guide owns marketplace setup and removal of the original plugin.
The development-package README lists its six skills and execution requirements.
The records-package README owns its three-rule and one-skill inventory.

## Publication status

The catalog uses full-repository `main` as its source; a push changes the available package files independently of tag or GitHub release creation.
The package versions listed above have annotated `<package>/v<version>` tags and public GitHub releases.
Do not load the new package beside published `agent-team` `0.2.0`, because that version contains the same three rule identities.
The split requires `agent-team` `0.3.0` or newer, rather than an older installed copy.
The catalog no longer lists the original root Copilot-format `copilot-workbench` package.
The owner confirms that the plugin was tested and considers the former OI-03 outdated.
The client version, configuration, and test scope were not specified; do not infer which configurations or components the test covered.
See [Project status](PROJECT-STATUS.md) for current work and [Architecture](ARCHITECTURE.md) for package boundaries.

## Installation

These steps use VS Code `1.144` as the setup baseline; they do not establish runtime compatibility.
The supported configuration is the **Local** harness in an editor window, on Windows and in WSL.
Local is a harness name, not a synonym for execution on your own computer.
No repository clone or manual copying of agents, rules, or skills is required.

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

### 2. Remove the original plugin if present

For a new installation, skip this step.
Otherwise, uninstall `copilot-workbench` before installing `agent-team`, so both copies do not load together.
Run **Chat: Open Customizations**, select **Plugins**, open `copilot-workbench`, and select **Uninstall**.
The **Plugins** page also lists a copy installed with `/plugin` or the Copilot CLI; uninstall that copy through the interface that installed it.
Check both Windows and WSL contexts for old copies.

### 3. Install on Windows

Open a Windows folder in an editor window without a WSL connection, and select the **Local** harness in a new chat.
Install through the Agent Customizations editor:

1. Run **Chat: Open Customizations**, select **Browse**, open the source menu, and select **Configure Marketplaces**.
2. Select **Add Marketplace** and enter `awieczork/copilot-workbench`, unless it is already listed.
3. Return to **Browse**, select that marketplace, and install `agent-team`.
4. Review the trust prompt, then confirm on the **Plugins** page that `agent-team` is enabled for the current profile if you want to use it across projects, rather than only in this workspace.

When the **Browse** page is not available, select **Plugins** and then **Browse Marketplace**.
Check that the installed `agent-team` version matches the [package manifest on `main`](https://github.com/awieczork/copilot-workbench/blob/main/plugins/agent-team/plugin.json).
Listing a plugin alone does not establish that its agents, rules, or tools work.

### 4. Configure WSL

Open a project folder in the Linux home directory from a WSL terminal with `code .`.
Confirm that the editor's lower-left remote indicator identifies the intended WSL distribution.
In that WSL-connected window, inspect the **Plugins** page first, and repeat step 3 only when `agent-team` is not available there.

Do not assume that a Windows installation, executable, or credential is available to the WSL host.
Do not copy plugin installation directories between systems.
Configure tools, environment variables, and service access where their processes run.
The [agent-team requirements](plugins/agent-team/README.md#requirements), [Context7 setup](plugins/agent-team/README.md#context7-api-key), and [database access](plugins/agent-team/README.md#database-access) describe the package-specific configuration.
Keep keys and credentials out of chat and tracked files.
Bundled MCP servers can start when the plugin is enabled; configure their access before testing them.

### 5. Verify both environments

In each of Windows and WSL, start a new **Local** session in a test folder outside this workbench, so repository customizations do not mask plugin discovery.
Check the installed source and version, agent and rule discovery in Agent Customizations, and skill availability in a fresh session.
Select `lead` and ask it to delegate a read-only folder inspection to `explorer`, without edits or external services; confirm that the delegation actually runs.
Workers need not appear in the main agent picker.
Check required tools and script execution separately.
A database connection failure is separate from plugin discovery and does not by itself establish an installation failure.

Record results separately for Windows and WSL.
Successful installation alone does not prove runtime support.

### Updates and optional tools

Use **Check for and Apply Updates** on the **Plugins** page or **Chat: Update Plugins**.
Start a fresh session and check the version and behavior after updating.
Plugin updates can also run automatically when `extensions.autoUpdate` is enabled; do not assume installations stay pinned between checks.

Install `agent-plugin-dev` only where you need the development tools, from the same marketplace in the Agent Customizations editor.
The packages do not require each other, and the catalog has no compatibility alias for `copilot-workbench`.
This workbench uses six repository discovery pointers to the canonical development skills; real-client pointer selection remains unverified.
The [VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) describes plugin management and its client requirements.

## Maintenance

The owner maintains these packages for personal use.
Public access supports installation without repository credentials; this repository does not accept external contributions or provide public support.
The root [changelog](CHANGELOG.md) records marketplace and repository changes; [agent-team history](plugins/agent-team/CHANGELOG.md) retains the original package releases, while [development-package history](plugins/agent-plugin-dev/CHANGELOG.md) and [records-package history](plugins/project-records/CHANGELOG.md) belong to their packages.
Local and remote `develop` are retired, and `archive/develop-before-marketplace` preserves their frozen tip; further work uses cycle branches and verified squash integration.
Prepare package versions and notes on a cycle before integration; publish one package at a time from clean full-repository `main`, with package-specific tags and separate publication permission.
