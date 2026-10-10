# copilot-workbench

`copilot-workbench` is a private Agent Plugins package for GitHub Copilot in VS Code.
It bundles reusable skills, custom agents, scoped rules, and Model Context Protocol (MCP) server configuration for software development and data analysis.

## Requirements

- VS Code with GitHub Copilot.
- `uv` with `uvx` on `PATH` for Python execution and the Redshift MCP server.
- Node.js with `npx` on `PATH` for the context7 MCP server.
- The SQL Server extension `ms-mssql.mssql` or the Redshift MCP server, locally configured access, and read-only database permissions for database work.

## Installation

Open the VS Code Command Palette, run `Chat: Install Plugin From Source`, and enter `https://github.com/awieczork/copilot-workbench` when VS Code asks for the repository URL.

## Package contents

### Skills

| Skill | Purpose |
| --- | --- |
| `brief-subagent` | Supplies self-contained briefs for one-shot delegation and how to act on the status each worker returns. |
| `copilot-customization` | Guides writing and reviewing Copilot instructions, skills, and agents. |
| `interview-me` | Clarifies the user's intent before work continues; only the user invokes it. |
| `redshift` | Runs read-only queries against user-provided Redshift targets, with an MCP-first workflow and a bounded Python fallback. |
| `run-python` | Runs Python scripts and inline code through `uv`, with or without the project environment. |
| `sql-server` | Runs read-only SQL Server queries against user-provided targets through saved connections. |
| `task-context` | Keeps one task's state in a Git-ignored task folder that the task holder maintains, with a result file for a delegated result that must survive the session. |

### Agents

User-facing agents appear in the agent picker.
Workers run as subagents of an allowed entry agent or producer.

| Agent | Kind | Purpose |
| --- | --- | --- |
| `software-lead` | Lead | Delivers or plans software changes by deciding the approach, briefing workers, and judging results. |
| `data-lead` | Lead | Answers data-science questions with evidence and owns the conclusion. |
| `discuss` | Chat | Shapes an unfinished idea into a request for a lead or a prompt for a new session. |
| `explorer` | Helper | Searches the workspace for one question and returns locations with findings. |
| `database-explorer` | Helper | Finds and profiles the SQL Server and Redshift objects and join paths for one data question, drafts read-only queries, and returns the queries it ran. |
| `data-explorer` | Helper | Finds and profiles the local dataset files for one data question without changing them. |
| `researcher` | Helper | Gathers sourced external evidence for one bounded question. |
| `planner` | Producer | Produces an executable plan for a change or an analysis with dependent steps or open design decisions, and calls `challenger` when an error in a decision would be costly to find later. |
| `developer` | Producer | Implements a change with tests scaled to the cost of an undetected error, and calls `reviewer` when the brief requires it or an error would be costly to find later. |
| `ui-developer` | Producer | Implements an interface change, checks it in the running app in a browser, and calls `reviewer` when the brief requires it or an error would be costly to find later. |
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
| `context7` | `npx` | Provides current library documentation; runs without an API key, under the service's anonymous rate limits. |

The configuration is in [mcp.json](mcp.json).
The SQL Server tools and the Redshift fallback runner can accept writes; the skills and agents authorize read-only work, and read-only logins provide an additional boundary.

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

Confirm that the fallback settings identify the requested target before execution.
The runner returns at most 100 rows and reports truncation.
Read-only enforcement in this workflow relies on the skill instructions and database permissions; the runner is not a SQL authorization parser.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| SQL Server cannot connect | Check the selected saved connection and its local authentication. |
| Redshift MCP cannot start or access data | Check `uvx`, the configured local AWS profile, region, authentication, and server diagnostics. |
| The Redshift fallback rejects configuration | Populate every required local variable, confirm the intended target, and check that the port is valid. |
| context7 reports an error | Check `npx` and the server diagnostics; a rate-limit error means the anonymous quota is used up. |
