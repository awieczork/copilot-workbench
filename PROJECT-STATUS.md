# Project status

- State: `active`
- Updated: 2026-10-28
- Objective: Migrate `copilot-workbench` to the `awieczork-tools` marketplace with self-contained `agent-team` and `agent-plugin-dev` Agent Plugins 1.0 packages for VS Code with the Copilot harness in Agent Host.
- Focus: Obtain the exact effect permissions for fast-forward integration and publication of `agent-team` `0.2.0` and `agent-plugin-dev` `0.1.0`. The owner waived runtime verification, but runtime support stays unverified and [OI-03](OPEN-ISSUES.md) remains open.

## Roadmap

1. `active` Slice 5: integrate and publish the prepared packages with the runtime-verification waiver and separate effect permissions.
	1. [ ] Fast-forward `main` to the migration tree and push only after separate authorization.
	1. [ ] Publish each selected package's tag and release only after separate authorization.
	1. [ ] Check marketplace installation and updates only after separate client-effect authorization; do not treat unrun checks as passed.
1. `planned` Slice 6: retire `develop` after archive verification and separate ruleset and branch-deletion authorization.

## Blockers

- None.
