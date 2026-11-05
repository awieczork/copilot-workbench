# agent-plugin-dev

`agent-plugin-dev` provides skills for authoring, checking, and releasing plugins for GitHub Copilot in VS Code.

## Components

### Skills

| Skill | User can invoke | Agent can select | Purpose |
| --- | --- | --- | --- |
| [publish-plugin](skills/publish-plugin/SKILL.md) | Yes | No | Preflight one package and publish only its confirmed version and notes. |
| [build-plugin](skills/build-plugin/SKILL.md) | Yes | Yes | Author package components and check Agent Plugins 1.0 structure. |
| [copilot-customization](skills/copilot-customization/SKILL.md) | Yes | Yes | Create and review project instructions, scoped instructions, custom agents, and skills. |

The package ships no agents, scoped rules, or Model Context Protocol (MCP) configuration; use the current agent's tools for documentation lookup.

## Requirements

- `uv` and Python 3.11 or later for the checker and Python helpers; the checker declares its PyYAML dependency.
- Git, Bash, and GitHub CLI (`gh`) with local authentication for publication.

Tests use disposable repositories and local bare remotes, not the owner's services or credentials.

## Install

Install `agent-plugin-dev` from the `awieczork-tools` marketplace by the [root README](https://github.com/awieczork/copilot-workbench#install), only where you need the development tools.

## Usage

Installed plugin commands use the `agent-plugin-dev:` prefix.

1. Describe the package changes you need.
   The agent uses `build-plugin` and `copilot-customization` to author components and runs the package checker.
1. Before integration, prepare each changed package's version and versioned notes by the [versioned-notes format](skills/publish-plugin/references/versioned-notes.md).
   To use the `project-workflow` development cycle, name this format as its release preparation in your project instructions.
1. Optionally run `/agent-plugin-dev:publish-plugin <name>` for one package on `main`.
   Review its exact version, commit, tag, and notes before approving tag creation, tag push, and GitHub release creation.

## Limits

- The package targets the Local harness in a VS Code editor window.
- Skill discovery, package coexistence, and repository pointer selection remain unverified in a client; the owner waived runtime verification on 2026-10-28.
- The skills target GitHub Copilot plugins; Claude Code runtime compatibility is unverified.

## Version

The [manifest](plugin.json) holds the package version; [release notes](CHANGELOG.md) and [GitHub releases](https://github.com/awieczork/copilot-workbench/releases) record its history.
