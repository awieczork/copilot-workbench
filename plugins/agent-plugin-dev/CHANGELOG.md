# Changelog

## Unreleased

## [0.3.0] - 2026-11-05

### Changed

- The `publish-plugin` versioned-notes format defines the release preparation of each package a cycle changes, with a version greater than the package's version on the integration base and every existing tag of that package.

### Removed

- The `start-dev` and `finish-dev` skills move to the `project-workflow` package as generic `start-dev` and `end-dev` skills.

## [0.2.2] - 2026-11-04

### Added

- The `agent-plugin-dev` manifest declares the MIT license.

### Changed

- The package README follows the shared components, requirements, install, usage, limits, and version structure, and links to the root installation guidance instead of repeating it.

## [0.2.1] - 2026-11-03

### Added

- The `copilot-customization` skill includes a `CLAUDE.md` proxy template that reuses `.github/` project instructions, scoped rules, and skills without duplicating their policy.

## [0.2.0] - 2026-11-03

### Added

- The `finish-dev` skill completes cycle checks and version preparation, then presents exact integration, push, and named branch-cleanup effects for approval.

### Changed

- The user-invoked `start-dev` skill grants checked local commits within the exact cycle branch and scope for the current session, while preserving staged selections and separate effect approvals.
- The package README identifies user-only lifecycle commands and user-and-agent authoring skills, and describes the complete start, finish, and optional publication workflow.

### Removed

- The `commit-dev` and `merge-dev` skills and commands are replaced by the cycle commit grant and `finish-dev`, with their screening, squash-verification, and cleanup safeguards retained.

## [0.1.4] - 2026-11-02

### Changed

- The package README includes marketplace installation and concise runtime requirements.

## [0.1.3] - 2026-11-02

### Changed

- The `copilot-customization` skill describes custom agent fields, tool aliases, and `#tool:` references for the Local harness without per-harness qualifiers.

## [0.1.2] - 2026-11-02

### Changed

- The `copilot-customization` skill describes tool references, model identifiers, and agent configuration by harness.

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
