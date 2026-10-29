# Changelog

## Unreleased

## [0.1.1] - 2026-10-29

Runtime support remains unverified under the owner's waiver; static checks do not establish client compatibility.

### Changed

- The development skills state script prerequisites, inputs, outputs, failure results, and completion reports while distinguishing static checks from client verification.
- The `copilot-customization` skill reads resources that control the requested behavior and distinguishes Copilot-format and Agent Plugins 1.0 component locations.
- The `merge-dev` and `publish-plugin` skills load branch-cleanup and publication procedures only for the requested stage while retaining separate effect permissions.

### Fixed

- The package README distinguishes the current manifest from tagged releases while retaining the unverified runtime warning.
- The `start-dev` skill requests permission to carry newly discovered dirty paths without changing them.
- The `merge-dev` skill repeats the successful remote-absence check immediately before deleting a local cycle branch.

## [0.1.0] - 2026-10-28

Runtime verification is waived by the owner; skill discovery, package coexistence, and repository pointer selection remain unverified in a real client.

### Added

- The `copilot-customization` skill guides choosing, writing, and reviewing Copilot instructions, custom agents, and skills.
- The `build-plugin` skill guides Agent Plugins 1.0 authoring and checks package layout, component identities, local links, and repository discovery pointers.
- The `start-dev` skill starts or resumes a local plugin or repository cycle after checking its branch and working state.
- The `commit-dev` skill screens and commits cycle-scoped changes with normal hooks and separate push permission.
- The `merge-dev` skill checks release readiness and verifies squash integration before separately authorized pushes and branch cleanup.
- The `publish-plugin` skill checks one package's version, notes, and tag history before separately authorized publication from clean `main`.
