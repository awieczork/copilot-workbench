# Changelog

## Unreleased

### Fixed

- The package README identifies version `0.1.0` as published while retaining the unverified runtime warning.

## [0.1.0] - 2026-10-28

Runtime verification is waived by the owner; skill discovery, package coexistence, and repository pointer selection remain unverified in a real client.

### Added

- The `copilot-customization` skill guides choosing, writing, and reviewing Copilot instructions, custom agents, and skills.
- The `build-plugin` skill guides Agent Plugins 1.0 authoring and checks package layout, component identities, local links, and repository discovery pointers.
- The `start-dev` skill starts or resumes a local plugin or repository cycle after checking its branch and working state.
- The `commit-dev` skill screens and commits cycle-scoped changes with normal hooks and separate push permission.
- The `merge-dev` skill checks release readiness and verifies squash integration before separately authorized pushes and branch cleanup.
- The `publish-plugin` skill checks one package's version, notes, and tag history before separately authorized publication from clean `main`.
