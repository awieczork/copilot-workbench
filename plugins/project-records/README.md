# project-records

`project-records` provides rules and a skill for maintaining a project's status, open issues, and changelog in GitHub Copilot for VS Code.

## Components

### Rules

| Rule | Record |
| --- | --- |
| [Project status](com.github.copilot/rules/project-status.instructions.md) | The current objective, state, focus, roadmap, and blockers in `PROJECT-STATUS.md`. |
| [Open issues](com.github.copilot/rules/open-issues.instructions.md) | Unresolved decisions, missing inputs, and verified limitations in `OPEN-ISSUES.md`. |
| [Changelog](com.github.copilot/rules/changelog.instructions.md) | User-visible results and their reconciliation in `CHANGELOG.md`. |

### Skill

[update-project-records](skills/update-project-records/SKILL.md) updates records when established results change the project's durable state, or when the user requests reconciliation.
It reads the rules for affected records and changes only records supported by evidence.

The package bundles no agents, Model Context Protocol (MCP) configuration, or runtime scripts.

## Install

Install `project-records` from the `awieczork-tools` marketplace by the [root README](https://github.com/awieczork/copilot-workbench#install).
Do not install it beside `agent-team` `0.2.0`, which contains the same record rules; use `agent-team` `0.3.0` or newer.

## Usage

The model may select the skill automatically, or the user can invoke it.
Automatic selection is not a post-task hook; project permissions and update timing still apply.

The package maintains durable records, not transient task state, and creates missing records only when requested or required by project instructions.
It does not invent objectives, priorities, decisions, or completion; its rules use Git history when needed.

## Limits

- The package targets the Local harness in a VS Code editor window.
- Static checks do not prove client compatibility; rule discovery, skill selection, and execution remain unverified in a real client.
- In Claude Code, only the skill is registered; the rules do not load automatically.

## Version

The [manifest](plugin.json) holds the package version; [release notes](CHANGELOG.md) and [GitHub releases](https://github.com/awieczork/copilot-workbench/releases) record its history.
