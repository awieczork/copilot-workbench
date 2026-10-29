# Architecture

This document gives the high-level design of `copilot-workbench`, a public, owner-maintained marketplace for GitHub Copilot in VS Code with the Copilot harness in Agent Host; each artifact defines its own behavior.

## Purpose

The `agent-team` package supports the owner's data science, scientific exploration, and hobby software projects, with Python as the general-purpose stack and other technologies chosen per project.
The `agent-plugin-dev` package provides reusable plugin authoring, validation, and development lifecycle capabilities.
The `project-records` package supplies durable project-record conventions and coordinated updates from established results, independently of any agent team.
The [pillars](.github/copilot-instructions.md#pillars) set the vision for its development.

## Boundaries

| Layer | Holds |
| --- | --- |
| `agent-team` package | The agent team, supporting skills, language-scoped rules, Model Context Protocol (MCP) configuration, and bundled resources under `plugins/agent-team/`. |
| `agent-plugin-dev` package | Six reusable customization, build, and lifecycle skills with their resources under `plugins/agent-plugin-dev/`; no agents, rules, or MCP configuration. |
| `project-records` package | Three rules for project status, open issues, and changelogs, with the automatically selectable `update-project-records` skill under `plugins/project-records/`; no agents or MCP configuration. |
| Marketplace catalog | Distribution metadata that lists each package by its repository-relative source without duplicating its version. |
| Workbench | Repository instructions, four team-specific scoped contracts, six discovery pointers, and project records, outside package payloads. |
| Project repository | Standalone project customizations, project instructions, source code, and durable project records. |
| Local environment | Credentials, saved connections, service configuration, and runtime dependencies. |
| Temporary task state | Session and delegated-work state in the layout of [`task-context`](plugins/agent-team/skills/task-context/SKILL.md). |

The `agent-team` payload is [plugin.json](plugins/agent-team/plugin.json), [mcp.json](plugins/agent-team/mcp.json), `com.github.copilot/agents/`, `com.github.copilot/rules/`, `skills/` with their resources, and package [README.md](plugins/agent-team/README.md) and [CHANGELOG.md](plugins/agent-team/CHANGELOG.md).
The working-tree [marketplace catalog](.github/plugin/marketplace.json) lists `agent-team`, `agent-plugin-dev`, and `project-records` with their matching `./plugins/<name>` sources.
Each package has one purpose and bundles the resources it needs, without requiring another package.
Packages hold no project-specific datasets, database targets, credentials, or absolute paths.
Repository records and `.github/` authoring files stay outside package payloads in the full-repository distribution source.

### Package format

All packages use [Agent Plugins 1.0](https://agent-plugins.org/): each has a root `plugin.json` with the canonical `$schema`, portable `skills/`, optional root `mcp.json`, and Copilot-specific components under `com.github.copilot/`.
Published `main` serves `agent-team` `0.2.0` and `agent-plugin-dev` `0.1.0`, each with its own versioned changelog notes, namespaced tag, and GitHub release.
The working tree extracts the three record rules from `agent-team` into `project-records` `0.1.0`; this extraction and the new package are not published.
Prepare an updated `agent-team` release before distributing both packages together, because published `agent-team` `0.2.0` still contains the same record-rule identities.
The owner waived runtime verification on 2026-10-28; the selected Agent Plugins 1.0 format remains unchanged and runtime support stays unverified.
[OI-03](OPEN-ISSUES.md) remains open: schema and path checks do not prove Agent Host runtime support.
The canonical [packaging guide](plugins/agent-plugin-dev/skills/build-plugin/references/packaging.md) and checker define static 1.0 checks; they do not prove runtime support.

## Agents

The user selects an entry agent.
A lead splits the task into parts for workers, runs the independent parts in parallel, and integrates their results.
A chat agent delegates its evidence gathering to helper workers.
A worker returns one status with its result to the delegating agent.
`discuss` hands a shaped request to a lead through a handoff the user confirms.

| Agent | May call |
| --- | --- |
| `data-lead` | Every worker |
| `lead` | Every worker |
| `discuss` | `explorer`, `researcher`, `challenger` |
| `developer`, `ui-developer` | `reviewer` |
| `planner` | `challenger` |

## Coordination

Every delegation is one-shot and self-contained, following [`brief-subagent`](plugins/agent-team/skills/brief-subagent/SKILL.md) or, for a producer's call to its checker, the producer's review rules, and the delegating agent treats worker output as evidence while keeping conclusions, integration decisions, and the choice of which results get a review or a kept test.
Every worker returns one status, `done`, `blocked`, `Decision needed`, or `Missing input`, and the delegating agent acts on it as `brief-subagent` describes.
The task holder, the entry agent the user talks to that holds the task, keeps task state through [`task-context`](plugins/agent-team/skills/task-context/SKILL.md), and a worker writes task state only to the result file its brief names.
Only entry agents ask the user.
Each role receives only the tools it needs, and read-only roles rest on instructions, because query and execution tools can also write.
Leads use strong models and workers the tier that fits their role, as defined in the [entry contract](.github/instructions/entry-contract.instructions.md) and the [worker model tiers](.github/instructions/model-tiers.instructions.md).

## Skills and rules

| Group | Components | Responsibility |
| --- | --- | --- |
| General customization | [`copilot-customization`](plugins/agent-plugin-dev/skills/copilot-customization/SKILL.md) | Artifact choice, metadata, writing guidance, and review in `agent-plugin-dev`. |
| Plugin development | [`build-plugin`](plugins/agent-plugin-dev/skills/build-plugin/SKILL.md), [`start-dev`](plugins/agent-plugin-dev/skills/start-dev/SKILL.md), [`commit-dev`](plugins/agent-plugin-dev/skills/commit-dev/SKILL.md), [`merge-dev`](plugins/agent-plugin-dev/skills/merge-dev/SKILL.md), [`publish-plugin`](plugins/agent-plugin-dev/skills/publish-plugin/SKILL.md) | Static package checks and explicitly authorized local cycles, commits, integration, and per-package publication. |
| Coordination | [`brief-subagent`](plugins/agent-team/skills/brief-subagent/SKILL.md), [`task-context`](plugins/agent-team/skills/task-context/SKILL.md), [`interview-me`](plugins/agent-team/skills/interview-me/SKILL.md), [`seed-task`](plugins/agent-team/skills/seed-task/SKILL.md) | Self-contained briefs, temporary state, intent clarification, and seeds for independent sessions. |
| Execution | [`run-python`](plugins/agent-team/skills/run-python/SKILL.md), [`redshift`](plugins/agent-team/skills/redshift/SKILL.md), [`sql-server`](plugins/agent-team/skills/sql-server/SKILL.md) | Runtime selection and bounded, read-only database work. |
| Scoped rules | [Markdown](plugins/agent-team/com.github.copilot/rules/markdown.instructions.md), [Python](plugins/agent-team/com.github.copilot/rules/python.instructions.md), [SQL](plugins/agent-team/com.github.copilot/rules/sql.instructions.md) | Conventions for Markdown documents, user-run task scripts, and read-only queries. |
| Record rules | [Changelog](plugins/project-records/com.github.copilot/rules/changelog.instructions.md), [Project status](plugins/project-records/com.github.copilot/rules/project-status.instructions.md), [Open issues](plugins/project-records/com.github.copilot/rules/open-issues.instructions.md) | The content of a project's `CHANGELOG.md`, `PROJECT-STATUS.md`, and `OPEN-ISSUES.md`, owned by `project-records`. |
| Record maintenance | [update-project-records](plugins/project-records/skills/update-project-records/SKILL.md) | Evidence-based updates after a durable state change or an explicit reconciliation request; reads only the rules for selected records and respects project update permissions. |

General behavior belongs in agents and skills, not in language rules.
Record maintenance does not require the team's task-state layout, and automatic skill selection is not a guaranteed post-task hook.
`interview-me` is a user-only skill for starting an interview with any agent ad hoc; it is independent of `discuss`, which runs its own interview phase, so their overlapping question rules are intended.

## Plugin authoring

The packages change only in this repository, the workbench.
A project may hold its own skills, agents, and instructions written with [`copilot-customization`](plugins/agent-plugin-dev/skills/copilot-customization/SKILL.md), but nothing in a project joins the plugin's team.
Team roles and delegation capabilities belong in `agent-team`; durable record conventions and maintenance belong in `project-records`.

The canonical [`build-plugin`](plugins/agent-plugin-dev/skills/build-plugin/SKILL.md) owns general authoring, package checks, and generic skill guidance, and uses `copilot-customization` for writing and review.
Repository `.github/skills/` contains only six discovery pointers to the development package, with matching discovery metadata and one link per file; implementations, scripts, tests, and references stay canonical in that package.
The scoped [team conventions](.github/instructions/team.instructions.md), [entry contract](.github/instructions/entry-contract.instructions.md), [worker contract](.github/instructions/worker-contract.instructions.md), and [model tiers](.github/instructions/model-tiers.instructions.md) govern only `agent-team` authoring.
No package depends on those workbench instructions to run.
The extraction leaves agent roles and delegation contracts unchanged; the three record rules are supplied only by `project-records` in the working tree.
`copilot-customization` stays plugin-independent.
Static checks cover package isolation, component identity collisions, and pointer shape; real discovery and co-installed selection remain client-runtime checks.

## Repository lifecycle

The migration transferred the archived `develop` tree without merging unrelated histories and fast-forwarded `main` to the reviewed full-repository commit `4b91750ca6db1e51b7972b7f6dda6e3853a7c581` under explicit owner authorization.
Both package release tags point to that commit; later record-only commits do not move those tags.
Local and remote `develop` are retired; the published annotated tag `archive/develop-before-marketplace` preserves their frozen tip.
`main` is the full-repository distribution branch and repository default; the working-tree catalog lists `agent-team`, `agent-plugin-dev`, and `project-records`, with no legacy package alias.
Development cycles use `plugin/<exact-name>` or `repo/<lowercase-kebab-topic>` and squash integration; local creation requires local `main` to equal cached `origin/main`, and dirty carry-over needs explicit permission.
Commits use exact scoped paths and normal hooks; a commit request does not authorize a push.
The squash workflow verifies recorded base and source IDs, the expected tree, and the sole parent before a normal `main` push. Cleanup needs named deletion permission and remote-absence proof.
Prepare package versions and versioned notes on the cycle before integration, because the marketplace serves `main` immediately.
Publication selects one catalog package from clean full-repository `main`, uses `<package>/v<version>` tags and that package's notes, and requires separate confirmation for tags, pushes, and releases.
Release versions must increase; only `agent-team` also inherits the legacy `v*` version floor. The root changelog owns repository changes, and package changelogs own package history.
Commits, pushes, integration, releases, and branch retirement require separate authorization.
Legacy tags and releases remain unchanged; future package versions belong to their manifests and use package-specific release tags.

The repository is public for installation without repository credentials, not for external contributions or public support.
The owner is the only repository collaborator; Issues, Projects, Discussions, and Wiki are disabled.
Branch rules prevent deletion and force pushes on `main`, without required pull requests, reviews, or status checks, so direct authoring and package publication remain available.
The authorized retirement removed only the `develop` selector from ruleset `25154483`; `main` protection is unchanged.
Secret scanning and secret push protection are enabled.
GitHub Actions uses read-only token permissions by default and cannot approve pull requests; workflows from all external contributors require owner approval.
Collaborator-only interaction restrictions also block external pull requests and comments while active ([OI-02](OPEN-ISSUES.md)).

Keep repository instructions and discovery pointers under `.github/` tracked in the full repository, because they reproduce the development environment on another machine; reusable authoring tools stay in `agent-plugin-dev`.
`.github/context/`, editor settings, and credentials remain Git-ignored local state.
Public visibility applies to every branch and its history, regardless of what the package includes.

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
