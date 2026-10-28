# Changelog

## Unreleased

### Added

- The `awieczork-tools` marketplace publishes `agent-team` `0.2.0` and `agent-plugin-dev` `0.1.0` from separate package directories.
- Repository discovery pointers expose the six canonical development skills without copying their implementations.

### Changed

- Team authoring contracts apply only to `agent-team` and preserve its entry, worker, model, and shared conventions outside both packages.
- Repository guidance separates local cycle work, verified squash integration, and package publication with explicit permissions.
- Repository migration guidance records the owner's runtime-verification waiver while keeping runtime support unverified and integration and publication separately authorized.
- The `main` branch serves the full repository instead of a package-only snapshot.
- The `archive/develop-before-marketplace` tag preserves the frozen tip of the retired local and remote `develop` branches.
