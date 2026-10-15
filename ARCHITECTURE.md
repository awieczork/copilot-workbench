# Architecture

This document gives the high-level design of `copilot-workbench`, a private [Agent Plugins 1.0](https://agent-plugins.org/) package for GitHub Copilot in VS Code with the Copilot harness in Agent Host; each artifact defines its own behavior.

## Purpose

The package supports the owner's data science, scientific exploration, and hobby software projects, with Python as the general-purpose stack and other technologies chosen per project.
The [pillars](.github/copilot-instructions.md#pillars) set the vision for its development.

## Boundaries

| Layer | Holds |
| --- | --- |
| Plugin package | The agent team, general-use skills, scoped rules, MCP configuration, and bundled resources. |
| Marketplace catalog | Distribution metadata that lists the root plugin without duplicating its version. |
| Workbench | Plugin-authoring skills, team contracts, publication, and project records, outside the payload. |
| Project repository | Standalone project customizations, project instructions, source code, and durable project records. |
| Local environment | Credentials, saved connections, service configuration, and runtime dependencies. |
| Temporary task state | Session and delegated-work state in the layout of [`task-context`](skills/task-context/SKILL.md). |

The published payload is root [plugin.json](plugin.json) and [mcp.json](mcp.json), the `skills/` folders with their resources, the Copilot extensions under `com.github.copilot/`, the package metadata `README.md` and `CHANGELOG.md`, and the [marketplace catalog](.github/plugin/marketplace.json).
The package holds no project-specific datasets, database targets, credentials, or absolute paths.
The catalog is the only published file under `.github/`; this repository's customizations, the other root records, temporary task state, and source references stay outside the payload.

## Agents

The user selects an entry agent, which works directly or delegates bounded assignments to workers; a worker returns one status with its result to the delegating agent.
`discuss` hands a shaped request to a lead through a handoff the user confirms.

| Agent | May call |
| --- | --- |
| `data-lead` | Every worker |
| `software-lead` | Every worker except `database-explorer` and `data-explorer` |
| `discuss` | `explorer`, `researcher`, `challenger` |
| `developer`, `ui-developer` | `reviewer` |
| `planner` | `challenger` |

## Coordination

Every delegation is one-shot and self-contained, following [`brief-subagent`](skills/brief-subagent/SKILL.md) or, for a producer's call to its checker, the producer's review rules, and the delegating agent treats worker output as evidence while keeping conclusions and integration decisions.
Every worker returns one status, `done`, `blocked`, `Decision needed`, or `Missing input`, and the delegating agent acts on it as `brief-subagent` describes.
The task holder, the entry agent the user talks to that holds the task, keeps task state through [`task-context`](skills/task-context/SKILL.md), and a worker writes task state only to the result file its brief names.
Only entry agents ask the user.
Each role receives only the tools it needs, and read-only roles rest on instructions, because query and execution tools can also write.
Leads use strong models and workers the tier that fits their role, as defined in the [entry contract](.github/skills/build-plugin/references/entry-contract.md) and the [worker model tiers](.github/skills/build-plugin/references/model-tiers.md).

## Skills and rules

| Group | Components | Responsibility |
| --- | --- | --- |
| General customization | [`copilot-customization`](skills/copilot-customization/SKILL.md) | Artifact choice, metadata, writing guidance, and review. |
| Coordination | [`brief-subagent`](skills/brief-subagent/SKILL.md), [`task-context`](skills/task-context/SKILL.md), [`interview-me`](skills/interview-me/SKILL.md) | Self-contained assignments, temporary state, and intent clarification. |
| Execution | [`run-python`](skills/run-python/SKILL.md), [`redshift`](skills/redshift/SKILL.md), [`sql-server`](skills/sql-server/SKILL.md) | Runtime selection and bounded, read-only database work. |
| Scoped rules | [Markdown](com.github.copilot/rules/markdown.instructions.md), [Python](com.github.copilot/rules/python.instructions.md), [SQL](com.github.copilot/rules/sql.instructions.md) | Conventions for Markdown documents, user-run task scripts, and read-only queries. |
| Record rules | [Changelog](com.github.copilot/rules/changelog.instructions.md), [Project status](com.github.copilot/rules/project-status.instructions.md), [Open issues](com.github.copilot/rules/open-issues.instructions.md) | The content of a project's `CHANGELOG.md`, `PROJECT-STATUS.md`, and `OPEN-ISSUES.md`. |

General behavior belongs in agents and skills, not in language rules.
`interview-me` is a user-only skill for starting an interview with any agent ad hoc; it is independent of `discuss`, which runs its own interview phase, so their overlapping question rules are intended.

## Plugin authoring

The plugin changes only in this repository, the workbench.
A project may hold its own skills, agents, and instructions written with [`copilot-customization`](skills/copilot-customization/SKILL.md), but nothing in a project joins the plugin's team; a capability that should work with the leads goes into the plugin.

The repository skill [`build-plugin`](.github/skills/build-plugin/SKILL.md) holds the authoring method, the team contracts, and the packaging rules, and points to `copilot-customization` for the writing and the review questions.
It stays outside the payload, because only the workbench builds plugin components.
`copilot-customization` stays plugin-independent, so plugin conventions stay in `build-plugin`.

## Repository lifecycle

`develop` is the authoring branch, and `main` is the package-only distribution branch and the repository default.
The `awieczork-tools` marketplace on `main` lists the root `copilot-workbench` plugin with source `./`; the version and descriptive metadata belong to `plugin.json`.
VS Code with the Copilot harness in Agent Host is the primary target; the shared package format does not establish equivalent behavior in other Copilot clients.

## Capability candidates

These capabilities are outside the current design and may join it later.
Each candidate needs an agreed priority and a new specification before implementation.

| Candidate | Intended outcome |
| --- | --- |
| Quarto rule | Define scoped authoring and validation conventions for Quarto documents. |
| R rule | Define scoped conventions for R scripts and project code. |
| Analytical-task skill | Organize one analytical task's durable files and execution record without duplicating temporary task state. |
| Data-contracts skill | Create and maintain explicit contracts for datasets and their expected properties. |
| Mermaid skill | Create and validate diagrams from a newly agreed, bounded diagramming workflow. |
| Reporting skill | Create and maintain analytical reports with traceable evidence and stated limitations. |
| Project-instruction skill | Interview the owner and produce project-specific root instructions; first assess overlap with existing customization skills. |
| Scaffold skill | Initialize a new data-science workspace with optional application modules. |
| Python MCP server skill | Author, test, and diagnose Python MCP servers for VS Code using documentation for the selected versions. |
