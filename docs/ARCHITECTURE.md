# Architecture

This repository contains the `awieczork-tools` marketplace packages for GitHub Copilot in VS Code and a discovery catalog for Claude Code.

## Design principles

- **Direction over detail:** give models the goal and approach; specify exact steps only where variation changes the result.
- **Simple first, lean always:** use the smallest solution and load only the context a task needs.
- **Every word steers:** state each idea once, in plain and precise language.

The [full design principles](../.github/copilot-instructions.md#pillars) guide package authoring.

## Packages

| Package | Purpose |
| --- | --- |
| [agent-team](../plugins/agent-team/README.md) | Agents, skills, rules, and tools for data science, scientific exploration, and hobby software projects. Python is the general-purpose stack; projects can use other technologies. |
| [agent-plugin-dev](../plugins/agent-plugin-dev/README.md) | Reusable skills for customization, plugin checks, and the development lifecycle. |
| [project-records](../plugins/project-records/README.md) | Project-record rules and evidence-based updates, independent of any agent team. |

Each package contains the resources it needs and does not depend on another package.
Packages do not contain project datasets, database targets, credentials, or absolute paths.
Project repositories hold their own customizations, code, and records; credentials, connections, service configuration, and runtime dependencies stay in the local environment.

Packages use [Agent Plugins 1.0](https://agent-plugins.org/): a root `plugin.json`, portable skills and optional Model Context Protocol (MCP) server configuration, and Copilot-specific components under `com.github.copilot/`.
The supported runtime is the **Local harness**, the chat agent runtime selected as **Local** in a VS Code editor window, on Windows and Windows Subsystem for Linux (WSL).
The Copilot harness and the Agents window do not run the plugins reliably and remain unsupported.
Static package checks do not prove runtime discovery or support.

## Catalogs and runtimes

Each **catalog** lists the marketplace's packages and the repository paths from which a client loads them.

| Catalog | Runtime | Entries |
| --- | --- | --- |
| [.github/plugin/marketplace.json](../.github/plugin/marketplace.json) | GitHub Copilot | Name, repository-relative source, description copied from `plugin.json`, and license. |
| [.claude-plugin/marketplace.json](../.claude-plugin/marketplace.json) | Claude Code | The same name and source, with entry manifest fields: description, license, and, for `agent-team`, `mcpServers`. |

Both catalogs use the marketplace identity `awieczork-tools` and omit plugin versions, so each `plugin.json` stays the only version authority.
Claude Code uses source-based versions when neither its manifest nor its entry supplies one.

The packages have no `.claude-plugin/plugin.json` manifests; the Claude Code catalog entries supply those fields without adding files to the packages.
Existing `skills/` directories match Claude Code's standard layout; the catalog does not map Copilot agents or automatic rules into Claude Code.
The `agent-team` entry sets `mcpServers` to `./mcp.json`, relative to the plugin root, and reuses the existing server definitions; Claude Code can start those servers automatically when the plugin is enabled.
The Claude Code catalog adds registration, listing, and this MCP server path without changing package payloads or establishing runtime compatibility.

## agent-team design

An **entry agent** is the agent the user selects for a conversation; a **worker** handles one delegated task.
`lead` performs work directly or delegates to workers.
`discuss` gathers evidence and helps shape a request without implementing it.
After the user confirms a request, `discuss` offers the user-invoked `handoff-discussion` skill for a new `lead` session.

| Agent | May call |
| --- | --- |
| `lead` | Every worker |
| `discuss` | `explorer`, `researcher`, `challenger` |
| `developer` | `reviewer` |

Delegations are one-shot and self-contained, using [`brief-subagent`](../plugins/agent-team/skills/brief-subagent/SKILL.md) or the producer's checker rules.
Workers return `done`, `blocked`, `Decision needed`, or `Missing input`; only entry agents ask the user.
The task holder keeps temporary task state through [`task-context`](../plugins/agent-team/skills/task-context/SKILL.md), while workers write only to their assigned result files.
Read-only roles rely on instructions because query and execution tools can also write.
The [entry contract](../.github/instructions/entry-contract.instructions.md), [worker contract](../.github/instructions/worker-contract.instructions.md), and [model tiers](../.github/instructions/model-tiers.instructions.md) define team authoring and model choices.

## Repository layout and boundaries

```text
.claude-plugin/marketplace.json   Claude Code catalog
.github/plugin/marketplace.json   GitHub Copilot catalog
.github/                          repository instructions and skill pointers
docs/                             public documentation and design sources
plugins/<name>/                   package manifest, components, tests, and documentation
LICENSE                           MIT license for the repository and plugins
```

Packages are authored in this repository, but project customizations do not join the plugin's team.
Team roles and delegation belong in `agent-team`; record conventions and maintenance belong in `project-records`.
General behavior belongs in agents and skills, not language rules.
User-interface specialization is outside the current team design.

The tracked `.github/` files hold repository instructions, four team contracts, and matching discovery pointers to the canonical `agent-plugin-dev` skills.
The package holds the implementations, scripts, tests, and references; packages do not depend on this repository's instructions to run.
Static checks cover package isolation, component identity collisions, and pointer shape; discovery and co-installed selection require client testing.
`interview-me` is a user-only skill independent of the `discuss` interview phase.
Record maintenance does not require the team's task-state layout, and automatic skill selection is not a guaranteed post-task hook.

Repository records and `.github/` authoring files stay outside package payloads.
Local project status and issue records, temporary task state under `.github/context/`, editor settings, and credentials are Git-ignored.

## Documentation map

| Document | Owns |
| --- | --- |
| [README](../README.md) | Marketplace introduction, plugin inventory, and quick install. |
| Each package README | The package's components, requirements, configuration, usage, and limits. |
| [Installation](installation.md) | Setup, verification, updates, and upgrades for each runtime. |
| [Development](DEVELOPMENT.md) | Branches, development cycles, releases, and repository settings. |
| [References](REFERENCES.md) | External sources behind the design and its product facts. |

## Ideas under consideration

These ideas are outside the current design; each needs an agreed priority and specification before implementation.

- Quarto and R rules for scoped authoring conventions.
- An analytical-task skill for durable files and execution records, separate from temporary task state.
- A data-contracts skill for dataset expectations.
- Reassessment of combining local-file and database exploration when shared work justifies the tool access.
- Mermaid and reporting skills for diagrams and traceable analytical reports.
- A project-instruction skill, after assessing overlap with existing customization skills.
- A scaffold skill for data-science workspaces with optional application modules.
- A Python MCP server skill for authoring, testing, and diagnosing servers for VS Code.
