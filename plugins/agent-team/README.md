# agent-team

`agent-team` provides agents, skills, rules, and Model Context Protocol (MCP) tools for software development and data analysis in GitHub Copilot for VS Code.
Use it with the Local harness in an editor window.

## Good to know

- The [manifest](plugin.json) holds the package version; [release notes](CHANGELOG.md) and [GitHub releases](https://github.com/awieczork/copilot-workbench/releases) record its history.
- The marketplace serves `main`, so package changes can appear without a new release.
- The owner has tested the plugin, but did not specify the client version, configuration, or test scope; static checks do not prove runtime compatibility.
- The owner maintains the plugin for personal use; no public support or external contribution workflow is provided.

## Requirements

- VS Code with GitHub Copilot, using the Local harness in the editor window.
- The `chat.subagents.allowInvocationsFromSubagents` setting enabled when `developer` must run its `reviewer` check, because Local blocks subagent calls from subagents by default.
- `uv` with `uvx` on `PATH` for Python execution and the Redshift MCP server.
- Node.js with `npx` on `PATH` for the context7 MCP server.
- The SQL Server extension `ms-mssql.mssql` or the Redshift MCP server, locally configured access, and read-only database permissions for database work.

## Installation

Uninstall the original `copilot-workbench` plugin first, so both copies do not load together.
Use the interface that installed it, including for a copy installed with `/plugin` or the Copilot CLI.
Do not install `project-records` beside `agent-team` `0.2.0`; its record rules were removed in `0.3.0`.

1. In a VS Code editor window, select the **Local** harness and run **Chat: Open Customizations**.
1. Under **Browse**, select **Configure Marketplaces** and add `awieczork/copilot-workbench` if needed.
1. Install `agent-team`, review the trust prompt, and confirm it is enabled on the **Plugins** page.

When **Browse** is unavailable, select **Plugins**, then **Browse Marketplace**.
To update, use **Check for and Apply Updates** or **Chat: Update Plugins**, then start a new session.
See the [VS Code plugin documentation](https://code.visualstudio.com/docs/agent-customization/agent-plugins) for plugin management.

## Package contents

### Skills

| Skill | Purpose |
| --- | --- |
| [brief-subagent](skills/brief-subagent/SKILL.md) | Selects models and prepares self-contained delegation briefs. |
| [data-analysis](skills/data-analysis/SKILL.md) | Frames data questions and checks evidence and interpretations. |
| [handoff-discussion](skills/handoff-discussion/SKILL.md) | Transfers a confirmed `discuss` request to a new `lead` session; user-invoked. |
| [interview-me](skills/interview-me/SKILL.md) | Clarifies the user's intent; user-invoked. |
| [planning](skills/planning/SKILL.md) | Creates and follows a proportional plan. |
| [redshift](skills/redshift/SKILL.md) | Queries a user-provided Redshift target read-only, with an MCP-first workflow and bounded Python fallback. |
| [run-python](skills/run-python/SKILL.md) | Runs Python through `uv`, with or without the project environment. |
| [seed-task](skills/seed-task/SKILL.md) | Saves a conversation as task context for an independent session; user-invoked. |
| [sql-server](skills/sql-server/SKILL.md) | Queries a user-provided SQL Server target read-only through a saved connection. |
| [task-context](skills/task-context/SKILL.md) | Keeps temporary task state and delegated results in a Git-ignored folder. |

After confirming a request with `discuss`, run `/agent-team:handoff-discussion`, then select `lead` in a new session and use the start prompt the skill returns.

### Agents

Entry agents are intended to appear in the agent picker; workers run as optional subagents of an allowed entry agent or producer.
The lead may work directly and owns acceptance of every result.

| Agent | Kind | Purpose |
| --- | --- | --- |
| `lead` | Lead | Delivers work directly or with workers and owns the result. |
| `discuss` | Chat | Shapes an idea into a request without implementing it. |
| `explorer` | Helper | Finds workspace evidence for one question. |
| `database-explorer` | Helper | Profiles database objects and join paths and runs read-only queries. |
| `data-explorer` | Helper | Profiles local datasets and runs analyses without changing the files. |
| `researcher` | Helper | Gathers sourced external evidence for one question. |
| `developer` | Producer | Implements changes to code, tests, configuration, documentation, and builds. |
| `reviewer` | Checker | Assesses a finished result without repairing it. |
| `challenger` | Helper | Tests a decision or framing and recommends a check. |

### Rules

| Rule | Scope |
| --- | --- |
| `markdown` | Markdown documents; customization files get only its syntax rules. |
| `python` | User-run task scripts; reusable code follows its project conventions. |
| `sql` | Read-only SQL Server or Redshift queries: schema reading, result bounding, and query text; connection handling and execution safety belong to the database skills. |

### MCP servers

| Server | Launcher | Purpose |
| --- | --- | --- |
| `awslabs.redshift-mcp-server` | `uvx` | Provides Redshift query and catalog tools. |
| `context7` | `npx` | Provides current library documentation; uses `CONTEXT7_API_KEY` when set, or anonymous access with lower rate limits. |

The configuration is in [mcp.json](mcp.json).
The SQL Server tools and the Redshift fallback runner can accept writes; the skills and agents authorize read-only work, and read-only logins provide an additional boundary.

## Context7 API key

Create an API key in the [Context7 dashboard](https://context7.com/dashboard).
Set `CONTEXT7_API_KEY` in the environment on the machine that runs the Context7 MCP server, before VS Code starts.
The packaged server reads this variable directly; no change to [mcp.json](mcp.json) is required.
Keep the real key out of chat and repository files.

Fully quit and restart VS Code after a change; for a remote, Windows Subsystem for Linux (WSL), or container session, set it where the MCP server runs.

## Database access

Supply the target server or Redshift cluster and the database in the request.
Keep credentials in local configuration and never provide them in chat or commit them to the package.

For SQL Server, create a saved connection in the SQL Server extension.
The [SQL Server skill](skills/sql-server/SKILL.md) connects to the saved server, verifies the active target, and disconnects when the task ends or becomes blocked.

The Redshift MCP configuration uses the local AWS profile `redshift-mcp`.
Configure that profile's credentials and region on the machine that runs the server; no cluster or database target is encoded in the skills.
The [Redshift skill](skills/redshift/SKILL.md) uses MCP first and switches to its Python fallback only when MCP cannot reach the cluster.

The fallback requires a workspace-root `.env` with these locally supplied settings:

```dotenv
REDSHIFT_USER=
REDSHIFT_PASSWORD=
REDSHIFT_HOST=
REDSHIFT_PORT=
REDSHIFT_DATABASE=
```

The runner reports the host and database it connected to, and the skill discards a result from another target.
The runner returns at most 100 rows and reports truncation.
