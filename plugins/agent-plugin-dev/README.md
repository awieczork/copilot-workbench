# agent-plugin-dev

`agent-plugin-dev` provides skills for authoring, checking, and releasing plugins for GitHub Copilot in VS Code.
The package is independent and uses the Local harness in an editor window.

## Install

In a VS Code editor window, select the **Local** harness and run **Chat: Open Customizations**.
Under **Browse**, select **Configure Marketplaces**, add `awieczork/copilot-workbench`, and install `agent-plugin-dev`.

## Skills

| Skill | Purpose |
| --- | --- |
| [copilot-customization](skills/copilot-customization/SKILL.md) | Create and review project instructions, scoped instructions, custom agents, and skills. |
| [build-plugin](skills/build-plugin/SKILL.md) | Author package components and check Agent Plugins 1.0 structure. |
| [start-dev](skills/start-dev/SKILL.md) | Start or resume one local plugin or repository cycle. |
| [commit-dev](skills/commit-dev/SKILL.md) | Screen and commit explicit cycle-scoped changes, with a separate push gate. |
| [merge-dev](skills/merge-dev/SKILL.md) | Verify a cycle squash, push with permission, and prove any authorized cleanup. |
| [publish-plugin](skills/publish-plugin/SKILL.md) | Preflight one package and publish only its confirmed version and notes. |

## Runtime requirements

- `uv` and Python 3.11 or later for the checker and Python helpers; the checker declares its PyYAML dependency.
- Git for lifecycle commands, including `git merge-tree --write-tree` for merge verification.
- Bash and GNU `stat` for path screening; Bash and GitHub CLI (`gh`) with local authentication for publication.

Tests use disposable repositories and local bare remotes, not the owner's services or credentials.

## Good to know

- The [manifest](plugin.json) holds the package version; [release notes](CHANGELOG.md) and [GitHub releases](https://github.com/awieczork/copilot-workbench/releases) record its history.
- Skill discovery, package coexistence, and repository pointer selection remain unverified in a client; the owner waived runtime verification on 2026-10-28.
- The package ships no agents, scoped rules, or Model Context Protocol (MCP) configuration; use the current agent's tools for documentation lookup.
- The owner maintains the package for personal use; no public support or external contribution workflow is provided.
