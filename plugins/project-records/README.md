# project-records

`project-records` maintains a project's durable status, open issues, and changelog for GitHub Copilot in VS Code.
It is a self-contained Agent Plugins 1.0 package with no dependency on another plugin.

## Publication status

Version `0.1.0` is in development and has not been published.
Static checks do not establish client compatibility; rule discovery, skill selection, and execution remain unverified in a real client.

## Components

### Rules

| Rule | Record |
| --- | --- |
| [Project status](com.github.copilot/rules/project-status.instructions.md) | The current objective, state, focus, roadmap, and blockers in `PROJECT-STATUS.md`. |
| [Open issues](com.github.copilot/rules/open-issues.instructions.md) | Unresolved decisions, missing inputs, and verified limitations in `OPEN-ISSUES.md`. |
| [Changelog](com.github.copilot/rules/changelog.instructions.md) | User-visible results and their reconciliation in `CHANGELOG.md`. |

### Skill

[update-project-records](skills/update-project-records/SKILL.md) coordinates record updates when completed work, a phase change, an accepted decision, or a confirmed or resolved blocker changes the project's durable state.
It also handles an explicit request to reconcile project records.
Only records with an evidenced change are updated, and their rules are read when selected.

The model may select the skill automatically; manual invocation remains available.
Automatic selection is not a post-task hook and does not guarantee invocation after every task.
Project permissions and update timing still apply, including any restriction on changelog edits.

## Scope

The package maintains durable project records, not transient task or session state.
It uses existing records and creates missing ones only when the request or project instructions calls for them.
It does not invent objectives, priorities, decisions, or completion.
Git history supplies previous changelog baselines and issue identifiers when the rules require them.
The package bundles no agents, Model Context Protocol (MCP) configuration, or runtime scripts.
