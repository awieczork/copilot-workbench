# project-workflow

`project-workflow` provides rules and skills for maintaining a project's status, open issues, and changelog, and for running a gated development cycle on Git branches, in GitHub Copilot for VS Code.

## Components

### Rules

| Rule | Record |
| --- | --- |
| [Project status](com.github.copilot/rules/project-status.instructions.md) | The current objective, state, focus, roadmap, and blockers in `PROJECT-STATUS.md`. |
| [Open issues](com.github.copilot/rules/open-issues.instructions.md) | Unresolved decisions, missing inputs, and verified limitations in `OPEN-ISSUES.md`. |
| [Changelog](com.github.copilot/rules/changelog.instructions.md) | User-visible results and their reconciliation in `CHANGELOG.md`. |

### Skills

| Skill | User can invoke | Agent can select | Purpose |
| --- | --- | --- | --- |
| [start-dev](skills/start-dev/SKILL.md) | Yes | No | Start or resume a `<kind>/<topic>` cycle and grant checked local commits on its exact branch in the current session. |
| [end-dev](skills/end-dev/SKILL.md) | Yes | No | Prepare a cycle, then gate squash integration, pushes, and named cleanup effects. |
| [update-project-records](skills/update-project-records/SKILL.md) | Yes | Yes | Update records when established results change the project's durable state, or on a reconciliation request. |

The package bundles no agents or Model Context Protocol (MCP) configuration.

## Requirements

- Git with an `origin` remote for the development cycle, including `git merge-tree --write-tree` for squash verification.
- `uv` and Python 3.11 or later for the squash verifier.
- Bash and GNU `stat` for path screening before commits.

The record rules and `update-project-records` need no tools.
Tests use disposable repositories and local bare remotes, not the user's services or credentials.

## Install

Install `project-workflow` from the `awieczork-tools` marketplace by the [root README](https://github.com/awieczork/copilot-workbench#install).
Do not install it beside `project-records`, which contains the same rules and record skill, or beside `agent-team` `0.2.0`; use `agent-team` `0.3.0` or newer.

## Usage

Installed plugin commands use the `project-workflow:` prefix.

### Records

The model may select `update-project-records` automatically, or the user can invoke it.
Automatic selection is not a post-task hook; project permissions and update timing still apply.
The package maintains durable records, not transient task state, and creates missing records only when requested or required by project instructions.
It does not invent objectives, priorities, decisions, or completion; its rules use Git history when needed.

### Development cycle

1. Run `/project-workflow:start-dev <kind> <topic>`, such as `feat csv-export`, to start or resume one cycle branch from the integration branch.
   Resolve any dirty-work question before the agent changes branches.
1. Describe the changes you need.
   The agent checks complete units of work and commits them locally within the cycle scope without another approval for each commit.
   A new session requires a new start or resume request; carrying existing dirty work does not by itself authorize committing it.
1. Run `/project-workflow:end-dev` when the work is ready.
   The agent completes checks and review, completes any release preparation with the values you select, and presents the exact source and integration effects for approval.
1. Approve local integration and each other effect you want: a push of the integration branch and any exact local or remote cycle-branch deletion.
   One confirmation can name several effects; no unlisted effect is authorized.

The integration branch is the default branch of `origin`.
Project instructions can name another integration branch, limit the cycle kinds and their scope, set the commit message format, and define release preparation, such as versions and versioned notes.
Without them, any lowercase kind is accepted, a cycle covers the paths related to its topic, commits use Conventional Commits, and no release preparation applies.

## Limits

- The package targets the Local harness in a VS Code editor window.
- Static checks do not prove client compatibility; rule discovery, skill selection, and execution remain unverified in a real client.
- In Claude Code, only the skills are registered; the rules do not load automatically.
- The development cycle integrates only by one squash commit and requires an `origin` remote; it does not open pull requests.

## Version

The [manifest](plugin.json) holds the package version; [release notes](CHANGELOG.md) and [GitHub releases](https://github.com/awieczork/copilot-workbench/releases) record its history.
