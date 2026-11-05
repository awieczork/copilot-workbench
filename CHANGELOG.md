# Changelog

## Unreleased

### Added

- The repository and all three plugins use the MIT license, with license metadata in each package manifest and both marketplace catalogs.
- The `awieczork-tools` marketplace catalogs list independent `agent-team`, `agent-plugin-dev`, and `project-workflow` packages for GitHub Copilot and Claude Code discovery; the Claude Code catalog also registers the existing `agent-team` MCP servers.
- Repository discovery pointers expose the canonical plugin authoring, release, development cycle, and record skills without copying their implementations.

### Changed

- Team authoring contracts stay outside package payloads and describe the simplified `agent-team` entry agents, optional workers, model defaults, and Local `#tool:` references.
- Marketplace installation guidance covers the Local harness on Windows and Windows Subsystem for Linux and the separate Claude Code catalog registration and MCP verification steps, with discovery distinguished from runtime compatibility.
- Repository documentation explains architecture, installation, development, and design sources for any reader, with public guides under `docs/` and private lifecycle procedures in their owning skills.
- The root README lists each plugin's components per runtime and gives install commands for GitHub Copilot and Claude Code.
- The marketplace catalogs describe each plugin by its purpose.
- Runtime guidance limits supported development to the Local harness because the Copilot harness and the Agents window do not run plugins reliably on Windows and Windows Subsystem for Linux.
- Repository guidance uses the `project-workflow` start and end cycle and optional publication, with session-scoped local commit grants, plugin and repository cycle scopes, plugin versioned notes as release preparation, and explicit approval for integration and remote effects.
- GitHub repository metadata describes the marketplace scope, lists plugin technology topics, and permits squash merges only.
- Legacy `v0.1.0` through `v0.1.3` release titles identify `agent-team` while retaining their tags, notes, and the current Latest release.
- The `main` branch serves the full repository instead of a package-only snapshot, with catalog availability distinguished from tag and GitHub release creation.
- The `archive/develop-before-marketplace` tag preserves the frozen tip of the retired local and remote `develop` branches.

### Removed

- Repository distribution excludes the local project-status and open-issues records and links to them, while their working-tree copies remain unchanged.
