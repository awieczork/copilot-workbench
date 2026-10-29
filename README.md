# copilot-workbench

`copilot-workbench` is the public, owner-maintained repository for the `awieczork-tools` marketplace for GitHub Copilot in VS Code.
The primary target is the Copilot harness in Agent Host, in both the editor window and the Agents window; the Local harness in the editor window is an additional target.
Each package has one purpose and bundles the resources it needs without requiring another package.

## Packages

| Package | Purpose | Publication state |
| --- | --- | --- |
| [agent-team](plugins/agent-team/README.md) | Agents for software development and data analysis, with supporting skills, rules, and Model Context Protocol (MCP) configuration. | Version `0.3.0` is prepared; tagged publication pending; runtime support unverified. |
| [agent-plugin-dev](plugins/agent-plugin-dev/README.md) | Six reusable customization, build, and development lifecycle skills. | Version `0.1.0` is published; runtime support unverified. |
| [project-records](plugins/project-records/README.md) | Three project-record rules and an automatically selectable skill for evidence-based updates. | Version `0.1.0` is in development, not published; runtime support unverified. |

The [catalog](.github/plugin/marketplace.json) lists the packages present on this branch.
The `agent-team` README holds its component inventory and runtime requirements.
It also gives package-specific installation steps with runtime support still unverified; this root guide owns marketplace setup and removal of the original plugin.
The development-package README lists its six skills and execution requirements.
The records-package README owns its three-rule and one-skill inventory.

## Publication status

The catalog uses full-repository `main` as its source; a push changes the available package files independently of tag or GitHub release creation.
The `agent-team` manifest and versioned notes are prepared at `0.3.0`; its tagged publication is pending.
The verified releases before this preparation are `agent-team` `0.2.0` and `agent-plugin-dev` `0.1.0`.
The catalog includes `project-records` `0.1.0`; its first tagged release has not been created.
Do not load the new package beside published `agent-team` `0.2.0`, because that version contains the same three rule identities.
The split requires `agent-team` `0.3.0`, which excludes those rules, rather than an older installed copy.
The catalog no longer lists the original root Copilot-format `copilot-workbench` package.
[OI-03](OPEN-ISSUES.md) remains open until the agents and rules pass checks in a real Copilot Agent Host session.
The owner waived runtime verification on 2026-10-28 and authorized publication without changing the selected format.
This waiver is not evidence of runtime support; namespaced agent and rule loading, skill discovery, package coexistence, and repository pointer selection remain unverified.
See [Project status](PROJECT-STATUS.md) for current work and [Architecture](ARCHITECTURE.md) for package boundaries.

## Installation

These steps use VS Code `1.144` as the setup baseline; they do not establish runtime compatibility.
The intended configurations are:

| Window | Harness | Execution environments | Priority |
| --- | --- | --- | --- |
| Editor | Copilot | Windows and Windows Subsystem for Linux (WSL) | Primary |
| Agents | Copilot | Windows and WSL | Primary |
| Editor | Local | Windows and WSL | Additional |

Local is a harness name, not a synonym for execution on your own computer.
It is not available in the Agents window.
The four harness-and-environment setup contexts do not necessarily need four plugin copies: check discovery before installing another copy.
No repository clone or manual copying of agents, rules, or skills is required.

### 1. Prepare Windows and WSL

Install VS Code on Windows, sign in to GitHub Copilot, and confirm that a Copilot session can start.
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

These checks confirm terminal access, not access from Agent Host.
After changing tools or environment variables, fully quit and restart VS Code; restart the WSL server or Agent Host as needed to pick up its environment.

### 2. Remove the original plugin if present

For a new installation, skip this step.
Otherwise, uninstall `copilot-workbench` before installing `agent-team`, so both copies do not load together.
For a copy installed through `/plugin`, run this in a Copilot chat:

```text
/plugin uninstall copilot-workbench@awieczork-tools
```

For a copy installed through the Extensions view, Agent Customizations, or **Chat: Install Plugin From Source**, uninstall it in **Agent Plugins - Installed** or Agent Customizations.
The editor and `/plugin` use separate inventories; manage each installation through the interface where you installed it.
Check both Windows and WSL contexts for old copies.

### 3. Install for Copilot on Windows

Open a Windows folder in an editor window without a WSL connection.
Start a new chat and select the **Copilot** harness.
Run each command separately in chat, not in the terminal:

```text
/plugin marketplace add awieczork/copilot-workbench
/plugin marketplace update awieczork-tools
/plugin install agent-team@awieczork-tools
/plugin list
```

Skip the add command if the marketplace is already registered.
Confirm the source when prompted and check that `agent-team` version `0.3.0` is installed and enabled.
Manage this installation through `/plugin`.

### 4. Configure Local on Windows

Start a new chat in the editor window and select **Local**.
If Local is not available, check the experimental `chat.editor.localAgent.enabled` setting; organization policy can restrict the choice.
Keep Copilot as the normal choice for new sessions.

Run **Chat: Open Customizations** and inspect the plugins available to Local.
The editor can discover Copilot CLI installations; if the existing copy provides its components to Local, do not install another copy.
Otherwise, install through Agent Customizations:

1. Select **Browse**, open the source menu, and select **Configure Marketplaces**.
2. Select **Add Marketplace** and enter `awieczork/copilot-workbench`, unless it is already listed.
3. Return to **Browse**, select that marketplace, and install `agent-team`.
4. Confirm that the plugin is enabled for the current profile if you want to use it across projects, rather than only in this workspace.

Manage a copy installed through the editor through that editor, not through `/plugin`.
Listing a plugin alone does not establish that its agents, rules, or tools work with Local.

### 5. Configure WSL

Open a project folder in the Linux home directory from a WSL terminal with `code .`.
Confirm that the editor's lower-left remote indicator identifies the intended WSL distribution.
Repeat steps 3 and 4 in that WSL-connected window, selecting Copilot and Local in separate new chats.
For each harness, inspect the existing installation first and install only if needed.

Do not assume that a Windows installation, executable, or credential is available to the WSL host.
Do not copy plugin installation directories between systems.
Configure tools, environment variables, and service access where their processes run.
The [agent-team requirements](plugins/agent-team/README.md#requirements), [Context7 setup](plugins/agent-team/README.md#context7-api-key), and [database access](plugins/agent-team/README.md#database-access) describe the package-specific configuration.
Keep keys and credentials out of chat and tracked files.
Bundled MCP servers can start when the plugin is enabled; configure their access before testing them.

### 6. Verify both windows and environments

In the Agents window, start a Copilot session with a Windows folder, then another with a folder on the WSL host.
Check the selected execution environment, not only the folder path, and run `/plugin list` in each session.
Changing windows alone is not a reason to install another copy.

Test all six combinations in the table: three window-and-harness choices on each of Windows and WSL.
Use a test folder outside this workbench so repository customizations do not mask plugin discovery.
Check the installed source and version, agent and rule discovery in Agent Customizations, and skill availability in a fresh session.
Select `lead` and ask it to delegate a read-only folder inspection to `explorer`, without edits or external services; confirm that the delegation actually runs.
Workers need not appear in the main agent picker.
Check required tools and script execution separately; tools supplied by editor extensions can differ in the Agents window.
A database connection failure is separate from plugin discovery and does not by itself establish an installation failure.

Record results separately for each configuration; keep [OI-03](OPEN-ISSUES.md) open until its editor and runtime closure checks pass.
Successful installation alone does not prove runtime support.

### Updates and optional tools

For a `/plugin` installation, run each command separately in a Copilot chat in the relevant environment:

```text
/plugin marketplace update awieczork-tools
/plugin update agent-team@awieczork-tools
/plugin list
```

For an editor-managed installation, use **Check for and Apply Updates** on the Plugins page or **Chat: Update Plugins**.
Start a fresh session and check the version and behavior after updating.
Plugin updates can also run automatically when `extensions.autoUpdate` is enabled; do not assume installations stay pinned between checks.

Install `agent-plugin-dev` only where you need the development tools, through the same interface used for that harness's setup.
For Copilot:

```text
/plugin install agent-plugin-dev@awieczork-tools
```

The packages do not require each other, and the catalog has no compatibility alias for `copilot-workbench`.
This workbench uses six repository discovery pointers to the canonical development skills; real-client pointer selection remains unverified.
The [VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) describes plugin management and its client requirements.

## Maintenance

The owner maintains these packages for personal use.
Public access supports installation without repository credentials; this repository does not accept external contributions or provide public support.
The root [changelog](CHANGELOG.md) records marketplace and repository changes; [agent-team history](plugins/agent-team/CHANGELOG.md) retains the original package releases, while [development-package history](plugins/agent-plugin-dev/CHANGELOG.md) and [records-package history](plugins/project-records/CHANGELOG.md) belong to their packages.
Local and remote `develop` are retired, and `archive/develop-before-marketplace` preserves their frozen tip; further work uses cycle branches and verified squash integration.
Prepare package versions and notes on a cycle before integration; publish one package at a time from clean full-repository `main`, with package-specific tags and separate publication permission.
