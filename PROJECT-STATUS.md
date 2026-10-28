# Project status

- State: `active`
- Updated: 2026-10-28
- Objective: Migrate `copilot-workbench` to the `awieczork-tools` marketplace with self-contained `agent-team` and `agent-plugin-dev` Agent Plugins 1.0 packages for VS Code with the Copilot harness in Agent Host.
- Focus: Obtain separate authorization for an optional push of the accepted Slice 3 documentation commits; `agent-team` behavior and package configuration are preserved. Published `main` remains unchanged, and [OI-03](OPEN-ISSUES.md) still requires real-client runtime verification before integration.

## Roadmap

1. `active` Slice 3: confirm contract alignment and correct package documentation without changing `agent-team` behavior.
	1. [ ] Push `repo/marketplace-migration` only if separately authorized; this step is optional.
1. `planned` Slice 4: verify each package alone, both packages together, and repository pointer discovery in a real client; resolve OI-03 from the results.
1. `planned` Slice 5: prepare package releases and refresh migration documentation before integration into `main`, then verify marketplace installation and updates under separate publication permissions.
1. `planned` Slice 6: retire `develop` after archive verification and separate ruleset and branch-deletion authorization.

## Blockers

- None.
