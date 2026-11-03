# Changelog

## Unreleased

### Added

- The `awieczork-tools` marketplace catalog lists independent `agent-team`, `agent-plugin-dev`, and `project-records` packages.
- Repository discovery pointers expose the canonical plugin authoring and lifecycle skills without copying their implementations.

### Changed

- Team authoring contracts stay outside package payloads and describe the simplified `agent-team` entry agents, optional workers, model defaults, and Local `#tool:` references.
- Marketplace installation guidance covers the Local harness on Windows and Windows Subsystem for Linux in a separate guide linked from the repository README.
- Repository documentation groups the architecture and design references under `docs/`.
- Repository records limit supported development to the Local harness until the Copilot harness and the Agents window run plugins reliably on Windows and Windows Subsystem for Linux.
- Repository guidance uses start, finish, and optional publication with session-scoped local commit grants and explicit approval for integration and remote effects.
- Repository records reflect the owner's `agent-team` test confirmation without specifying the test scope.
- The `main` branch serves the full repository instead of a package-only snapshot, with catalog availability distinguished from tag and GitHub release creation.
- The `archive/develop-before-marketplace` tag preserves the frozen tip of the retired local and remote `develop` branches.

### Removed

- The open-issues register omits the renewal of collaborator-only interaction restrictions.
