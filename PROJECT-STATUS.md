# Project status

- State: `active`
- Updated: 2026-10-28
- Objective: Migrate `copilot-workbench` to the `awieczork-tools` marketplace with self-contained `agent-team` and `agent-plugin-dev` Agent Plugins 1.0 packages for VS Code with the Copilot harness in Agent Host.
- Focus: Review and accept the local Slice 1 commits on `repo/marketplace-migration` before planning Slice 2; the migration-branch push is optional and needs separate authorization. Published `main` remains unchanged; [OI-03](OPEN-ISSUES.md) still requires real-client runtime verification before integration.

## Roadmap

1. `active` Slice 1: complete and review the marketplace layout without publishing it.
	1. [ ] Review and accept the local Slice 1 commits.
	1. [ ] Push the migration branch only if separately authorized; this step is optional.
1. `planned` Slice 2: create `agent-plugin-dev`, adapt its lifecycle skills and checker, and replace repository skill implementations with discovery pointers.
1. `planned` Slice 3: update `agent-team` to the relocated contracts and Agent Plugins 1.0 conventions without changing its intended behavior.
1. `planned` Slice 4: verify each package alone, both packages together, and repository pointer discovery in a real client; resolve OI-03 from the results.
1. `planned` Slice 5: prepare package releases, integrate the full repository into `main`, and verify marketplace installation and updates under separate publication permissions.
1. `planned` Slice 6: retire `develop` after archive verification and separate ruleset and branch-deletion authorization.

## Blockers

- None.
