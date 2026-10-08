# copilot-workbench

`copilot-workbench` is a private Agent Plugins package for GitHub Copilot in VS Code.
It bundles reusable skills, custom agents, scoped rules, and Model Context Protocol (MCP) server configuration for software development and data analysis.
The first release, `v0.1.0`, is in preparation.

## Requirements

- VS Code with GitHub Copilot and Agent Plugins support.
- Git access to the package source when installing from source.
- `uv` with `uvx` on `PATH` for Python execution and the Redshift MCP server.
- Node.js with `npx` on `PATH` for the context7 MCP server.
- `chat.subagents.allowInvocationsFromSubagents` enabled when producers call their checkers.

Database workflows also need Microsoft SQL Server tools or the Redshift MCP server, locally configured access, and read-only database permissions.
The SQL Server extension is `ms-mssql.mssql`.

## Installation

Open the VS Code Command Palette and run `Chat: Install Plugin From Source`.
Select the repository source and reload VS Code when installation completes.
Before the first release, treat source installation as development use rather than a released package.

The package repository is [copilot-workbench](https://github.com/awieczork/copilot-workbench).
For a released package, the installed version must match [plugin.json](plugin.json) and its versioned [changelog entry](CHANGELOG.md).

## Package contents

### Skills

| Skill | Purpose |
| --- | --- |
| `brief-subagent` | Supplies self-contained briefs for one-shot delegation. |
| `build-entry-agent` | Builds a lead or chat agent in a project that delegates to project and plugin workers. |
| `build-skill` | Builds a skill in a project that plugin agents load through project instructions. |
| `build-worker-agent` | Builds a worker in a project that a project entry agent delegates to. |
| `copilot-customization` | Guides writing and reviewing Copilot instructions, skills, and agents. |
| `interview-me` | Clarifies the user's intent before work continues; only the user invokes it. |
| `redshift` | Runs read-only queries against user-provided Redshift targets, with an MCP-first workflow and a bounded Python fallback. |
| `run-python` | Runs Python through `uv` in project or no-project mode. |
| `sql-server` | Runs read-only SQL Server queries against user-provided targets through saved connection profiles. |
| `task-context` | Keeps temporary task summaries and delegated results under `.github/context/`. |

### Agents

User-facing agents appear in the agent picker.
Workers run as subagents of an allowed entry agent or producer.

| Agent               | Kind   | Purpose                                                                                     |
| :------------------ | :----- | :------------------------------------------------------------------------------------------ |
| `software-lead`     | Lead   | Delivers software changes by deciding the approach, briefing workers, and judging results.  |
| `data-lead`         | Lead   | Answers data-science questions with evidence and owns the conclusion.                       |
| `discuss`           | Entry  | Shapes an unfinished idea and hands it to a lead.                                           |
| `explorer`          | Worker | Searches the workspace for one question and returns locations with findings.                |
| `database-explorer` | Worker | Finds and profiles the tables, columns, and join paths for one data question.               |
| `data-explorer`     | Worker | Finds and profiles the local dataset files for one data question without changing them.     |
| `researcher`        | Worker | Gathers sourced external evidence for one bounded question.                                 |
| `planner`           | Worker | Produces an executable plan for work with significant decisions.                            |
| `developer`         | Worker | Implements a change with its tests and runs review when the brief asks.                     |
| `ui-developer`      | Worker | Implements and checks interface changes in the browser.                                     |
| `reviewer`          | Worker | Assesses a finished result against its goal without repairing it.                           |
| `challenger`        | Worker | Tests one decision or framing with the strongest objection and the cheapest settling check. |

### Rules

| Rule | Scope |
| --- | --- |
| `markdown` | Ordinary Markdown documents; excludes customization files and bundled skill resources. |
| `python` | Owner-run task scripts; reusable code follows its project conventions. |
| `sql` | One read-only SQL Server or Redshift query; connection handling and execution safety belong to the database workflows. |

### MCP servers

| Server | Launcher | Purpose |
| --- | --- | --- |
| `awslabs.redshift-mcp-server` | `uvx` | Provides Redshift query and catalog tools. |
| `context7` | `npx` | Provides current library documentation. |

The configuration is in [mcp.json](mcp.json).
Database tools can accept writes; the skills and agents authorize read-only work, and read-only logins provide an additional boundary.

## Database access

Supply the target server or Redshift cluster and the database in the request.
The skills ask for missing target details; delegated workers return missing details to their caller.
Keep credentials in local configuration and never provide them in chat or commit them to the package.

For SQL Server, create a saved connection profile in the SQL Server extension.
The [SQL Server skill](skills/sql-server/SKILL.md) connects to the saved server, verifies the active target, and disconnects when the task ends or becomes blocked.

The Redshift MCP configuration currently uses the local AWS profile label `redshift-mcp`.
Configure that profile's credentials and region on the machine that runs the server; no cluster or database target is encoded in the skills.
The [Redshift skill](skills/redshift/SKILL.md) uses MCP first and permits its Python fallback only after the documented access or tool failures.

The fallback requires a workspace-root `.env` with these locally supplied settings:

```dotenv
REDSHIFT_USER=
REDSHIFT_PASSWORD=
REDSHIFT_HOST=
REDSHIFT_PORT=
REDSHIFT_DATABASE=
```

Confirm that the fallback settings identify the requested target before execution.
The runner returns at most 1,000 rows and explicitly reports truncation.
Read-only enforcement in this workflow relies on the skill instructions and database permissions; the runner is not a SQL authorization parser.

## Documentation access

The context7 server starts through the package's MCP configuration.
Configure provider credentials locally when required by the service and check server diagnostics without printing keys.
Consult the [context7 documentation](https://context7.com/docs) for its current authentication options.

## Use the package

1. Open the target project folder in VS Code before using a file-producing workflow.
2. Select a skill from the slash-command menu when the task matches its purpose.
3. Select an agent from the VS Code agent picker when the task needs a distinct role.

The scoped rules apply when their file patterns match.
File-producing workflows write to the selected target workspace.
The package source remains separate from generated project files.
Project-specific agents, skills, and rules belong in that project's repository.

## Package layout

```text
copilot-workbench/
├── .gitignore
├── com.github.copilot/
│   ├── agents/
│   └── rules/
├── skills/
│   └── <skill>/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
├── CHANGELOG.md
├── mcp.json
├── plugin.json
└── README.md
```

## Troubleshooting

| Symptom | Action |
| --- | --- |
| The plugin or a skill is missing | Check the source installation and component name, then reload VS Code. |
| A bundled reference is unavailable | Record the skill and resource path; do not repair an installed package by copying unrelated files into it. |
| A file-producing workflow stops | Open the intended project folder and check the reported missing input. |
| A producer cannot call its checker | Enable `chat.subagents.allowInvocationsFromSubagents` and reload VS Code. |
| A database target is missing | Supply the intended server or cluster and database; do not supply credentials in chat. |
| SQL Server cannot connect | Check the selected saved profile and its local authentication. |
| Redshift MCP cannot start or access data | Check `uvx`, the configured local AWS profile, region, authentication, and server diagnostics. |
| The Redshift fallback rejects configuration | Populate every required local variable, confirm the intended target, and check that the port is valid. |
| context7 is unavailable | Check `npx`, server diagnostics, and the service's current local authentication requirements. |

## Repository maintenance

`develop` holds the authoring workspace and durable project records.
`main` is reserved for package-only distribution; its payload still needs preparing before the first release.
Branch protection is intentionally disabled.
Repository-local instructions and skills under `.github/` are not plugin components.
Architecture describes the design, project status holds the roadmap and near-term queue, and open issues holds unresolved project-level limitations and decisions.
