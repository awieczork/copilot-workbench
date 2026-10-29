# Changelog

## Unreleased

### Added

- The `awieczork-tools` marketplace catalog lists independent `agent-team`, `agent-plugin-dev`, and `project-records` packages.
- Repository discovery pointers expose the six canonical development skills without copying their implementations.

### Changed

- Team authoring contracts apply only to `agent-team` and preserve its entry, worker, model, and shared conventions outside package payloads.
- Marketplace installation guidance covers Copilot and Local on Windows and Windows Subsystem for Linux, with separate installation inventories and runtime checks.
- Repository guidance separates local cycle work, verified squash integration, and package publication with explicit permissions.
- Repository migration guidance records the owner's runtime-verification waiver while keeping runtime support unverified and integration and publication separately authorized.
- The `main` branch serves the full repository instead of a package-only snapshot, with catalog availability distinguished from tag and GitHub release creation.
- The `archive/develop-before-marketplace` tag preserves the frozen tip of the retired local and remote `develop` branches.
