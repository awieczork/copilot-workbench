# Changelog

## Unreleased

### Added

- The `awieczork-tools` marketplace catalog lists independent `agent-team`, `agent-plugin-dev`, and `project-records` packages.
- Repository discovery pointers expose the six canonical development skills without copying their implementations.

### Changed

- Team authoring contracts stay outside package payloads and describe the simplified `agent-team` entry agents, optional workers, model defaults, and Local `#tool:` references.
- Marketplace installation guidance covers the Local harness in the editor window on Windows and Windows Subsystem for Linux, with installation, updates, and runtime checks in the Agent Customizations editor.
- Repository records limit supported development to the Local harness until the Copilot harness and the Agents window run plugins reliably on Windows and Windows Subsystem for Linux.
- Repository guidance separates local cycle work, verified squash integration, and package publication with explicit permissions.
- Repository records reflect the owner's `agent-team` test confirmation without specifying the test scope.
- The `main` branch serves the full repository instead of a package-only snapshot, with catalog availability distinguished from tag and GitHub release creation.
- The `archive/develop-before-marketplace` tag preserves the frozen tip of the retired local and remote `develop` branches.

### Removed

- The open-issues register omits the renewal of collaborator-only interaction restrictions.
