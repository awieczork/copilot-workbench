# agent-plugin-dev

`agent-plugin-dev` provides reusable plugin development skills in the Agent Plugins 1.0 format.
It is under development on the migration branch, not yet published or verified in a real client.

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

The checker and Python helpers use `uv` and Python 3.11 or later; the checker declares its PyYAML dependency.
Lifecycle commands use Git; merge verification requires `git merge-tree --write-tree`.
Path screening uses Bash and GNU `stat`; the release wrapper uses Bash, and confirmed publication uses GitHub CLI (`gh`) with existing local authentication.
Tests use disposable repositories and local bare remotes, not the owner's services or credentials.

This package ships no agents, scoped rules, or Model Context Protocol (MCP) configuration and does not require `agent-team`.
Use the tools of the current agent for documentation lookup.

## Maintenance

The owner maintains this package for personal use.
Public access supports installation without repository credentials; no public support or external contribution workflow is provided.
