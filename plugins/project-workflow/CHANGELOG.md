# Changelog

## Unreleased

## [0.2.0] - 2026-11-05

### Added

- The user-invoked `start-dev` skill starts or resumes a `<kind>/<topic>` cycle branch in any Git project and grants checked local commits within its scope for the current session; project instructions can set the cycle kinds, scope, integration branch, and commit message format.
- The user-invoked `end-dev` skill completes cycle checks and any release preparation that project instructions define, then presents exact squash integration, push, and named branch-cleanup effects for approval.

### Changed

- The `project-records` package is renamed `project-workflow`, with the same rules and `update-project-records` skill.

## [0.1.2] - 2026-11-04

### Added

- The `project-records` manifest declares the MIT license.

### Changed

- The package README follows the shared components, requirements, install, usage, limits, and version structure, and links to the root installation guidance instead of repeating it.

## [0.1.1] - 2026-11-02

### Changed

- The package README includes marketplace installation and compatibility guidance.

## [0.1.0] - 2026-10-29

Runtime support remains unverified under the owner's waiver; static checks do not establish client compatibility.

### Added

- The project-record rules define the content and structure of `PROJECT-STATUS.md`, `OPEN-ISSUES.md`, and `CHANGELOG.md` independently of an agent team.
- The `update-project-records` skill coordinates evidence-based updates after durable state changes or explicit reconciliation requests while respecting project edit permissions and task scope.
