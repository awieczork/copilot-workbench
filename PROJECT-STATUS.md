# Project status

- State: `active`
- Updated: 2026-10-15
- Objective: Distribute the public, owner-maintained plugin through a marketplace for VS Code with the Copilot harness in Agent Host.
- Focus: The package on `develop` uses the Copilot plugin format, because Agent Host did not run the agents of the published Agent Plugins 1.0 package; the migrated package needs a release and a check in a Copilot session.

## Roadmap

1. `active` Release the migrated package and verify it in VS Code with the Copilot harness in Agent Host.
   1. [ ] Publish the release with `/publish-plugin`.
   2. [ ] Reinstall `copilot-workbench@awieczork-tools` and confirm in a Copilot session that its agents run, its rules apply ([OI-04](OPEN-ISSUES.md)), its skills and MCP servers are available, and the Agent Customizations editor lists its agents and rules.

## Blockers

- None.
