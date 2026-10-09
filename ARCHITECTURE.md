# Architecture

This document gives the high-level design of `copilot-workbench`, a private [Agent Plugins 1.0](https://agent-plugins.org/) package for GitHub Copilot in VS Code; each artifact defines its own behavior.
[Project status](PROJECT-STATUS.md) holds planned work, [open issues](OPEN-ISSUES.md) holds verified limitations and unresolved decisions, the [README](README.md) inventories the components, and [references](REFERENCES.md) lists the external sources behind the design.

## Purpose

The package supports the owner's data science, scientific exploration, and hobby software projects, with Python as the general-purpose stack and other technologies chosen per project.
Its design principles are personal use, technology independence, modular components, and plugin authoring kept in the workbench, and the [pillars](.github/copilot-instructions.md#pillars) set the vision for its development.

## Boundaries

| Layer | Holds |
| --- | --- |
| Plugin package | The agent team, general-use skills, scoped rules, MCP configuration, and bundled resources. |
| Workbench | Plugin-authoring skills, team contracts, publication, and project records, outside the payload. |
| Project repository | Standalone project customizations, project instructions, source code, and durable project records. |
| Local environment | Credentials, saved connections, service configuration, and runtime dependencies. |
| Temporary task state | Session and delegated-work state in the layout of [`task-context`](skills/task-context/SKILL.md). |

The payload is root [plugin.json](plugin.json), optional root [mcp.json](mcp.json), `skills/<name>/SKILL.md` files, and Copilot extensions under `com.github.copilot/`.
The package holds no project-specific datasets, database targets, credentials, or absolute paths.
This repository's `.github/` customizations, root records, temporary task state, and source references stay outside the payload.

## Agents

The user selects an entry agent, which works directly or delegates bounded assignments to workers; a worker returns evidence, artifacts, or blockers to its caller.
`discuss` consults `explorer`, `researcher`, and `challenger`, and hands a shaped request to a lead through a handoff the user confirms; both leads may delegate to every worker, `developer` and `ui-developer` call `reviewer`, and `planner` calls `challenger`.

| Agent | Kind | Role |
| --- | --- | --- |
| [`discuss`](com.github.copilot/agents/discuss.agent.md) | Chat | Clarifies an unfinished request, then hands it to a lead or produces a self-contained prompt. |
| [`software-lead`](com.github.copilot/agents/software-lead.agent.md) | Lead | Owns the approach and integration of software changes. |
| [`data-lead`](com.github.copilot/agents/data-lead.agent.md) | Lead | Owns the analytical question, evidence, and conclusion. |
| [`explorer`](com.github.copilot/agents/explorer.agent.md) | Helper | Locates workspace evidence for one question, read-only. |
| [`database-explorer`](com.github.copilot/agents/database-explorer.agent.md) | Helper | Discovers and profiles database objects, read-only. |
| [`data-explorer`](com.github.copilot/agents/data-explorer.agent.md) | Helper | Discovers and profiles local dataset files without changing them. |
| [`researcher`](com.github.copilot/agents/researcher.agent.md) | Helper | Gathers sourced external evidence. |
| [`planner`](com.github.copilot/agents/planner.agent.md) | Producer | Produces an executable plan with settled implementation decisions. |
| [`developer`](com.github.copilot/agents/developer.agent.md) | Producer | Implements and checks a bounded software change. |
| [`ui-developer`](com.github.copilot/agents/ui-developer.agent.md) | Producer | Implements and visually checks interface changes. |
| [`reviewer`](com.github.copilot/agents/reviewer.agent.md) | Checker | Assesses a finished result against its goal. |
| [`challenger`](com.github.copilot/agents/challenger.agent.md) | Helper | Tests one consequential decision or framing. |

## Coordination

Every delegation is one-shot and self-contained, following [`brief-subagent`](skills/brief-subagent/SKILL.md), and the lead treats worker output as evidence while keeping conclusions and integration decisions.
The lead works directly when a brief would cost more than the change, runs independent work in parallel, and never lets two writers edit overlapping files at once.
A producer reports a failed result by failure class, and the lead retries a fixable failure and routes the others.
Only entry agents ask the owner; workers return missing decisions, and an open question blocks only the work that depends on it.
Each role receives only the tools it needs, and read-only roles rest on instructions, because query and execution tools can also write.
Leads use strong models and workers the tier that fits their role, as defined in the [entry contract](.github/skills/build-plugin-component/references/entry-contract.md) and the [worker model tiers](.github/skills/build-plugin-component/references/model-tiers.md).

## Skills and rules

| Group | Components | Responsibility |
| --- | --- | --- |
| General customization | [`copilot-customization`](skills/copilot-customization/SKILL.md) | Artifact choice, metadata, writing guidance, and review. |
| Coordination | [`brief-subagent`](skills/brief-subagent/SKILL.md), [`task-context`](skills/task-context/SKILL.md), [`interview-me`](skills/interview-me/SKILL.md) | Self-contained assignments, temporary state, and intent clarification. |
| Execution | [`run-python`](skills/run-python/SKILL.md), [`redshift`](skills/redshift/SKILL.md), [`sql-server`](skills/sql-server/SKILL.md) | Runtime selection and bounded, read-only database work. |
| Scoped rules | [Markdown](com.github.copilot/rules/markdown.instructions.md), [Python](com.github.copilot/rules/python.instructions.md), [SQL](com.github.copilot/rules/sql.instructions.md) | Conventions for ordinary documents, user-run task scripts, and read-only query text. |

General behavior belongs in agents and skills, not in language rules.

## Plugin authoring

The plugin changes only in this repository, the workbench.
A project may hold its own skills, agents, and instructions written with [`copilot-customization`](skills/copilot-customization/SKILL.md), but nothing in a project joins the plugin's team; a capability that should work with the leads goes into the plugin.

The repository skill [`build-plugin-component`](.github/skills/build-plugin-component/SKILL.md) holds the authoring procedure and the team contracts: what makes a worker, entry agent, or skill fit the team, such as worker kinds and their tools, shared rule blocks, model ladders, entry-agent skeletons, and output slots.
It points to `copilot-customization` for the writing and stays outside the payload, because only the workbench builds plugin components.

| Artifact | Destination | Connection |
| --- | --- | --- |
| Skill | `skills/<name>/` | The plugin agents that need it name it in their body. |
| Worker | `com.github.copilot/agents/<name>.agent.md` | The plugin leads list it in `agents` and their routing tables. |
| Entry agent | `com.github.copilot/agents/<name>.agent.md` | Its `agents` list and handoffs name plugin agents. |

Every new or renamed component also updates the [README](README.md) inventory, this document, and the [changelog](CHANGELOG.md).
A change to a team contract updates the plugin agents it governs in the same change, so that shipped agents keep matching the contract.

## Repository lifecycle

`develop` is the authoring branch, and `main` is the package-only distribution branch and the repository default.
The operational roadmap lives only in [project status](PROJECT-STATUS.md).

## Capability candidates

These capabilities are outside the current design and may join it later.
Each candidate needs an agreed priority and a new specification before implementation; no earlier specification, implementation file, or workspace link is an input to it.

| Candidate | Intended outcome |
| --- | --- |
| Quarto rule | Define scoped authoring and validation conventions for Quarto documents. |
| R rule | Define scoped conventions for R scripts and project code. |
| Analytical-task skill | Organize one analytical task's durable files and execution record without duplicating temporary task state. |
| Data-contracts skill | Create and maintain explicit contracts for datasets and their expected properties. |
| Mermaid skill | Create and validate diagrams from a newly agreed, bounded diagramming workflow. |
| Reporting skill | Create and maintain analytical reports with traceable evidence and stated limitations. |
| Project-instruction skill | Interview the owner and produce project-specific root instructions; first assess overlap with existing customization skills. |
| Scaffold skill | Initialize a new data-science workspace with optional application modules; define the new scope and templates from scratch. |
| Python MCP server skill | Author, test, and diagnose Python MCP servers for VS Code using documentation for the selected versions. |
