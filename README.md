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
| `brief-subagent` | Supplies self-contained briefs for one-shot delegation and how to act on the status each subagent returns. |
| `copilot-customization` | Guides writing and reviewing Copilot instructions, skills, and agents. |
| `interview-me` | Clarifies the user's intent before work continues; only the user invokes it. |
| `redshift` | Runs read-only queries against user-provided Redshift targets, with an MCP-first workflow and a bounded Python fallback. |
| `run-python` | Runs Python scripts and inline code through `uv`, with or without the project environment, and runs a script with an inline dependency block outside the project. |
| `sql-server` | Runs read-only SQL Server queries against user-provided targets through saved connections. |
| `task-context` | Keeps one task's state in a Git-ignored task folder that the agent the user talks to maintains, with a result file for each delegated result. |

### Agents

User-facing agents appear in the agent picker.
Workers run as subagents of an allowed entry agent or producer.

| Agent | Kind | Purpose |
| --- | --- | --- |
| `software-lead` | Lead | Delivers software changes by deciding the approach, briefing workers, and judging results. |
| `data-lead` | Lead | Answers data-science questions with evidence and owns the conclusion. |
| `discuss` | Chat | Shapes an unfinished idea and hands it to a lead. |
| `explorer` | Helper | Searches the workspace for one question and returns locations with findings. |
| `database-explorer` | Helper | Finds and profiles the SQL Server and Redshift objects and join paths for one data question, drafts read-only queries, and returns the queries it ran. |
| `data-explorer` | Helper | Finds and profiles the local dataset files for one data question without changing them. |
| `researcher` | Helper | Gathers sourced external evidence for one bounded question. |
| `planner` | Producer | Produces an executable plan for a change or an analysis with dependent steps or open design decisions, and calls `challenger` when an error in a decision would be costly. |
| `developer` | Producer | Implements a change with tests scaled to the cost of an undetected error, and calls `reviewer` when the brief requires it or an error would be costly to find later. |
| `ui-developer` | Producer | Implements an interface change, checks it in the running app in a browser, and calls `reviewer` when the brief requires it or an error would be costly to find later. |
| `reviewer` | Checker | Assesses a finished result against its goal without repairing it. |
| `challenger` | Helper | Tests one decision or framing with the strongest objection and the cheapest settling check. |

### Rules

| Rule | Scope |
| --- | --- |
| `changelog` | The `## Unreleased` entries of a project's `CHANGELOG.md`. |
| `markdown` | Ordinary Markdown documents; excludes customization files and bundled skill resources. |
| `open-issues` | A project's `OPEN-ISSUES.md` register of unresolved decisions, missing inputs, and verified limitations. |
| `project-status` | A project's `PROJECT-STATUS.md` state, roadmap, and blockers. |
| `python` | User-run task scripts; reusable code follows its project conventions. |
| `sql` | One read-only SQL Server or Redshift query; connection handling and execution safety belong to the database workflows. |

### MCP servers

| Server | Launcher | Purpose |
| --- | --- | --- |
| `awslabs.redshift-mcp-server` | `uvx` | Provides Redshift query and catalog tools. |
| `context7` | `npx` | Provides current library documentation. |

The configuration is in [mcp.json](mcp.json).
The SQL Server tools and the Redshift fallback runner can accept writes; the skills and agents authorize read-only work, and read-only logins provide an additional boundary.

## Database access

Supply the target server or Redshift cluster and the database in the request.
The skills ask for missing target details; delegated workers return missing details to their caller.
Keep credentials in local configuration and never provide them in chat or commit them to the package.

For SQL Server, create a saved connection in the SQL Server extension.
The [SQL Server skill](skills/sql-server/SKILL.md) connects to the saved server, verifies the active target, and disconnects when the task ends or becomes blocked.

The Redshift MCP configuration currently uses the local AWS profile label `redshift-mcp`.
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

The scoped rules apply when their file patterns or descriptions match the task.
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
| SQL Server cannot connect | Check the selected saved connection and its local authentication. |
| Redshift MCP cannot start or access data | Check `uvx`, the configured local AWS profile, region, authentication, and server diagnostics. |
| The Redshift fallback rejects configuration | Populate every required local variable, confirm the intended target, and check that the port is valid. |
| context7 is unavailable | Check `npx`, server diagnostics, and the service's current local authentication requirements. |
