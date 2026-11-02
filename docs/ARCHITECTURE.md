# Architecture

`copilot-workbench` is the owner's marketplace for GitHub Copilot in VS Code.
Its [design pillars](../.github/copilot-instructions.md#pillars) favor clear direction, simplicity, and precise wording.

## Packages

| Package | Purpose |
| --- | --- |
| [agent-team](../plugins/agent-team/README.md) | Agents, skills, rules, and tools for data science, scientific exploration, and hobby software projects. Python is the general-purpose stack; projects can use other technologies. |
| [agent-plugin-dev](../plugins/agent-plugin-dev/README.md) | Reusable skills for customization, plugin checks, and the development lifecycle. |
| [project-records](../plugins/project-records/README.md) | Project-record rules and evidence-based updates, independent of any agent team. |

Each package contains the resources it needs and does not depend on another package.
Packages do not contain project datasets, database targets, credentials, or absolute paths.
Project repositories hold their own customizations, code, and records; credentials, connections, service configuration, and runtime dependencies stay in the local environment.

The [marketplace catalog](../.github/plugin/marketplace.json) lists the packages by repository-relative source without duplicating their versions.
Packages use [Agent Plugins 1.0](https://agent-plugins.org/): a root `plugin.json`, portable skills and optional MCP configuration, and Copilot-specific components under `com.github.copilot/`.
The packages target the Local harness in a VS Code editor window on Windows and Windows Subsystem for Linux (WSL).
The Copilot harness and Agents window remain unsupported while [OI-05](../OPEN-ISSUES.md) applies.
Static package checks do not prove runtime discovery or support.

## How the team works

The user selects an entry agent.
`lead` performs work directly or delegates to workers; `discuss` gathers evidence and helps shape a request without implementing it.
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

## Repository and package boundaries

Packages are authored in this workbench, but project customizations do not join the plugin's team.
Team roles and delegation belong in `agent-team`; record conventions and maintenance belong in `project-records`.
General behavior belongs in agents and skills, not language rules.
User-interface specialization is outside the current team design.

The workbench's tracked `.github/` files hold repository instructions, four team contracts, and six discovery pointers to the canonical `agent-plugin-dev` skills.
The package holds the implementations, scripts, tests, and references; packages do not depend on workbench instructions to run.
Static checks cover package isolation, component identity collisions, and pointer shape; discovery and co-installed selection require client testing.
`interview-me` is a user-only skill independent of the `discuss` interview phase.
Record maintenance does not require the team's task-state layout, and automatic skill selection is not a guaranteed post-task hook.

The root [README](../README.md) introduces the marketplace, and the [installation guide](installation.md) owns marketplace setup and verification.
Repository records and `.github/` authoring files stay outside package payloads.
Temporary task state under `.github/context/`, editor settings, and credentials are Git-ignored.

## Development and releases

`main` is the full-repository distribution branch and marketplace source.
A push exposes package changes independently of tags or GitHub releases, so prepare package versions and versioned notes on the cycle before integration.
Use `plugin/<exact-name>` or `repo/<lowercase-kebab-topic>` cycle branches and verified squash integration.
Creating a cycle requires local `main` to match cached `origin/main`; dirty carry-over needs explicit permission.

Commits use exact scoped paths and normal hooks.
The squash workflow verifies the recorded base and source, expected tree, and sole parent before pushing `main`; branch cleanup needs named deletion permission and proof of remote absence.
Publication selects one catalog package from clean full-repository `main`, uses a `<package>/v<version>` tag and package-specific notes, and requires separate permission for tags, pushes, and releases.
Versions must increase; `agent-team` also inherits the legacy `v*` version floor.
The root changelog owns repository changes, and each package owns its history.

Local and remote `develop` are retired; `archive/develop-before-marketplace` preserves their frozen tip.
The marketplace's full-repository history and legacy tags remain unchanged.
Commits, pushes, integration, releases, and branch deletion each require explicit authorization.

The repository is public for installation, not external contributions or public support.
The owner is its only collaborator; Issues, Projects, Discussions, and Wiki are disabled.
`main` is protected against deletion and force pushes without required pull requests, reviews, or status checks.
Secret scanning and push protection are enabled; GitHub Actions uses read-only token permissions by default, cannot approve pull requests, and requires owner approval for external-contributor workflows.
Collaborator-only interaction restrictions block external pull requests and comments while active.
Public visibility applies to every branch and its history.

## Possible future capabilities

These ideas are outside the current design; each needs an agreed priority and specification before implementation.

- Quarto and R rules for scoped authoring conventions.
- An analytical-task skill for durable files and execution records, separate from temporary task state.
- A data-contracts skill for dataset expectations.
- Reassessment of combining local-file and database exploration when shared work justifies the tool access.
- Mermaid and reporting skills for diagrams and traceable analytical reports.
- A project-instruction skill, after assessing overlap with existing customization skills.
- A scaffold skill for data-science workspaces with optional application modules.
- A Python MCP server skill for authoring, testing, and diagnosing servers for VS Code.
