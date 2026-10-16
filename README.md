# copilot-workbench

`copilot-workbench` is a public, owner-maintained Copilot-format plugin for GitHub Copilot in VS Code, using the Copilot harness in Agent Host.
It bundles reusable skills, custom agents, scoped rules, and Model Context Protocol (MCP) server configuration for software development and data analysis.

## Maintenance

The owner maintains this plugin for personal use.
Public access supports installation without repository credentials; this repository does not accept external contributions or provide public support.

## Requirements

- VS Code with GitHub Copilot, using the Copilot harness in Agent Host.
- `uv` with `uvx` on `PATH` for Python execution and the Redshift MCP server.
- Node.js with `npx` on `PATH` for the context7 MCP server.
- The SQL Server extension `ms-mssql.mssql` or the Redshift MCP server, locally configured access, and read-only database permissions for database work.

## Installation

### Install from the marketplace

The `awieczork-tools` marketplace lists this repository's root plugin.

In a VS Code chat session with the **Copilot** harness selected, run these commands one at a time:

```text
/plugin marketplace add awieczork/copilot-workbench
/plugin install copilot-workbench@awieczork-tools
/plugin list
```

To update, refresh the catalog and then update the plugin:

```text
/plugin marketplace update awieczork-tools
/plugin update copilot-workbench@awieczork-tools
```

Manage this installation through `/plugin`.

### Replace an installation from source

If you installed the plugin with **Chat: Install Plugin From Source**, uninstall that copy in the Agent Customizations editor before installing the marketplace copy, so that both copies do not load together.
Source installation remains available: run **Chat: Install Plugin From Source** from the Command Palette and enter `https://github.com/awieczork/copilot-workbench`.

## Package contents

### Skills

| Skill | Purpose |
| --- | --- |
| `brief-subagent` | Supplies self-contained briefs for one-shot delegation and how to act on the status each worker returns. |
| `copilot-customization` | Guides writing and reviewing Copilot instructions, skills, and agents. |
| `interview-me` | Clarifies the user's intent before work continues; only the user invokes it. |
| `redshift` | Runs read-only queries against user-provided Redshift targets, with an MCP-first workflow and a bounded Python fallback. |
| `run-python` | Runs Python scripts and inline code through `uv`, with or without the project environment. |
| `seed-task` | Turns the current conversation, such as a forked discussion, into a task folder that an independent session starts from; only the user invokes it. |
| `sql-server` | Runs read-only SQL Server queries against user-provided targets through saved connections. |
| `task-context` | Keeps one task's state in a Git-ignored task folder that the task holder maintains, with a result file for a delegated result that must survive the session. |

### Agents

Entry agents appear in the agent picker.
Workers run as subagents of an allowed entry agent or producer.

| Agent | Kind | Purpose |
| --- | --- | --- |
| `lead` | Lead | Delivers or plans any work in the workspace by deciding the approach, splitting it into parts for workers, and judging results. |
| `data-lead` | Lead | Handles work that touches or rests on data: frames the question, has workers run the queries, and owns the interpretation and the conclusion. |
| `discuss` | Chat | Shapes an unfinished idea into a request for a lead, and edits the documentation the user asks for. |
| `explorer` | Helper | Searches the workspace for one question and returns locations with findings. |
| `database-explorer` | Helper | Finds and profiles the SQL Server and Redshift objects and join paths for one data question, drafts and runs read-only queries. |
| `data-explorer` | Helper | Finds and profiles the local dataset files for one data question and runs the analyses a brief specifies without changing the files. |
| `researcher` | Helper | Gathers sourced external evidence for one bounded question. |
| `planner` | Producer | Produces an executable plan for a change or an analysis with dependent steps or open design decisions. |
| `developer` | Producer | Implements a change to code, tests, configuration, documentation, build, dependencies, or CI. |
| `ui-developer` | Producer | Implements an interface change, checks it in the running app in a browser. |
| `reviewer` | Checker | Assesses a finished result against its goal without repairing it. |
| `challenger` | Helper | Tests one decision or framing with the strongest objection, the cheapest settling check, and a recommendation. |

### Rules

| Rule | Scope |
| --- | --- |
| `changelog` | The Keep a Changelog entries of a project's `CHANGELOG.md`. |
| `markdown` | Markdown documents; customization files get only its syntax rules. |
| `open-issues` | A project's `OPEN-ISSUES.md` register of unresolved decisions, missing inputs, and verified limitations. |
| `project-status` | A project's `PROJECT-STATUS.md` state, roadmap, and blockers. |
| `python` | User-run task scripts; reusable code follows its project conventions. |
| `sql` | Read-only SQL Server or Redshift queries: schema reading, result bounding, and query text; connection handling and execution safety belong to the database skills. |

### MCP servers

| Server | Launcher | Purpose |
| --- | --- | --- |
| `awslabs.redshift-mcp-server` | `uvx` | Provides Redshift query and catalog tools. |
| `context7` | `npx` | Provides current library documentation; uses `CONTEXT7_API_KEY` when set, or anonymous access with lower rate limits. |

The configuration is in [.mcp.json](.mcp.json).
The SQL Server tools and the Redshift fallback runner can accept writes; the skills and agents authorize read-only work, and read-only logins provide an additional boundary.

## Context7 API key

Create an API key in the [Context7 dashboard](https://context7.com/dashboard).
Set `CONTEXT7_API_KEY` in the environment on the machine that runs the Context7 MCP server, before VS Code and Agent Host start.
The packaged server reads this variable directly; no change to [.mcp.json](.mcp.json) is required.
Keep the real key out of chat and repository files.

Set it in the environment that Agent Host starts from, and fully quit and restart VS Code after a change; for a remote, Windows Subsystem for Linux (WSL), or container session, set it where the MCP server runs.

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
