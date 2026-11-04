# agent-plugin-dev

`agent-plugin-dev` provides skills for authoring, checking, and releasing plugins for GitHub Copilot in VS Code.

## Components

### Skills

| Skill | User can invoke | Agent can select | Purpose |
| --- | --- | --- | --- |
| [start-dev](skills/start-dev/SKILL.md) | Yes | No | Start or resume a cycle and grant checked local commits on its exact branch in the current session. |
| [finish-dev](skills/finish-dev/SKILL.md) | Yes | No | Prepare a cycle, then gate squash integration, pushes, and named cleanup effects. |
| [publish-plugin](skills/publish-plugin/SKILL.md) | Yes | No | Preflight one package and publish only its confirmed version and notes. |
| [build-plugin](skills/build-plugin/SKILL.md) | Yes | Yes | Author package components and check Agent Plugins 1.0 structure. |
| [copilot-customization](skills/copilot-customization/SKILL.md) | Yes | Yes | Create and review project instructions, scoped instructions, custom agents, and skills. |

The package ships no agents, scoped rules, or Model Context Protocol (MCP) configuration; use the current agent's tools for documentation lookup.

## Requirements

- `uv` and Python 3.11 or later for the checker and Python helpers; the checker declares its PyYAML dependency.
- Git for lifecycle commands, including `git merge-tree --write-tree` for finish verification.
- Bash and GNU `stat` for path screening; Bash and GitHub CLI (`gh`) with local authentication for publication.

Tests use disposable repositories and local bare remotes, not the owner's services or credentials.

## Install

Install `agent-plugin-dev` from the `awieczork-tools` marketplace by the [root README](https://github.com/awieczork/copilot-workbench#install), only where you need the development tools.

## Usage

Installed plugin commands use the `agent-plugin-dev:` prefix.

1. Run `/agent-plugin-dev:start-dev plugin <name>` or `/agent-plugin-dev:start-dev repo <topic>` to start or resume one cycle.
   Resolve any dirty-work question before the agent changes branches.
1. Describe the changes you need.
   The agent uses the authoring skills, checks complete units of work, and commits them locally within the selected cycle scope without another approval for each commit.
   A new session requires a new start or resume request; carrying existing dirty work does not by itself authorize committing it.
1. Run `/agent-plugin-dev:finish-dev` when the work is ready.
   The agent completes checks and review, prepares the version you select and its notes, and presents the exact source and integration effects for approval.
1. Approve local integration into `main` and each other effect you want: a `main` push and any exact local or remote cycle-branch deletion.
   One confirmation can name several effects; no unlisted effect is authorized.
   Pushing `main` changes the marketplace files even without a tag or release.
1. Optionally run `/agent-plugin-dev:publish-plugin <name>` for one package.
   Review its exact version, commit, tag, and notes before approving tag creation, tag push, and GitHub release creation.

## Limits

- The package targets the Local harness in a VS Code editor window.
- Skill discovery, package coexistence, and repository pointer selection remain unverified in a client; the owner waived runtime verification on 2026-10-28.
- The skills target GitHub Copilot plugins; Claude Code runtime compatibility is unverified.

## Version

The [manifest](plugin.json) holds the package version; [release notes](CHANGELOG.md) and [GitHub releases](https://github.com/awieczork/copilot-workbench/releases) record its history.
