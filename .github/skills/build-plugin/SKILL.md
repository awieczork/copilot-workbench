---
name: build-plugin
description: "Use when creating, changing, or reviewing any plugin component: an agent, a skill, a rule, plugin.json, mcp.json, or a packaged path. Supplies the review questions, the authoring method, the team contracts, and the packaging rules. Not for commits or publication."
---

# Build the plugin

Change the plugin so that every component gives direction, fits the team, and ships in a valid package.
A component is any part of the plugin: an agent, a skill, a rule, `plugin.json`, `mcp.json`, or another packaged file.
Write each component by [copilot-customization](../../../skills/copilot-customization/SKILL.md) for its type; this skill adds what the plugin's team and package need.

## Work from an example

- When a change reaches several components of one kind, refine one real component with the owner first, write what it taught into the contract for its kind, and then apply the contract to the other components, because a contract written from an accepted example states the owner's expectation instead of a guess.
- When reviewing a component, number the findings in the `copilot-customization` review format, and apply them after the owner agrees.
- When a change alters a contract, update the components it governs in the same change, so that shipped components keep matching it.

## Ask the questions

Ask each question of every line, section, and file; a "no" marks a change to make.

Direction over detail:

- [ ] Is each rule the principle itself, with its reason, rather than one instance of a broader principle?
- [ ] Is each enumeration needed, or would the principle behind it steer the same way?
- [ ] Is precise detail kept for work that tolerates no variation, such as an approval gate, a protocol, or an exact command, and is a behavior that must repeat exactly left to a script?
- [ ] Does each rule sit in the component that owns the work, instead of restating a skill, a worker, or the harness?

Simple first, lean always:

- [ ] Would removing the line, step, section, or file change a result?
- [ ] Does a proportionality rule stand where the model would otherwise apply a classification, such as levels or a wording scale?
- [ ] Does each named skill, tool, or reference belong to the core work and load at a fixed point?
- [ ] Does each output slot carry something the reader acts on?

Every word steers:

- [ ] Is each rule stated once across the sections, the output template, and the skills the component loads?
- [ ] Does a capable newcomer read each sentence one way only, with one term per concept across the team?
- [ ] Does a reason, instead of emphasis or decoration, carry the weight of each rule?
- [ ] Do all lines pull in the same direction?
- [ ] Does each principle still change a concrete behavior, and each qualifier change behavior at all?

## Read the contract for the kind

- Entry agent: [entry contract](references/entry-contract.md).
- Worker: [worker contract](references/worker-contract.md), and [model tiers](references/model-tiers.md) for its `model` list.
- Skill: [skill contract](references/skill-contract.md).
- `plugin.json`, `mcp.json`, the package structure, or a packaged path: [packaging](references/packaging.md).
- Creating, changing, or validating `plugin.json` or `mcp.json`: also [manifest and MCP reference](references/manifest.md).

A rule has no contract.

## Keep the team's conventions

- Keep plugin artifacts free of private paths, workbench policy, and dependencies on repository-only records, because the plugin runs in other projects.
- Count every skill and rule as reachable by every agent, including a subagent, through its `description` or `applyTo`, so that an unnamed skill is no gap.
- Use Copilot tool identifiers and supported Copilot model identifiers, because identifiers from another harness select nothing in Copilot.
- Double-quote string frontmatter values in agents and rules, and keep native booleans such as `user-invocable: false`.
- Keep `software-lead`, `data-lead`, and `discuss` as the only user-facing agents.

## Add a component

1. Draft a specification from the request and the plugin, and present it to the owner with only the questions whose answers change it: `name`, `description`, and kind; tools, `agents`, `model`, and `handoffs`; what proceeds without asking; workflow phases and output slots; its connections; and the components it overlaps, with a recommendation to extend one that covers the need.
2. After the owner confirms, write the component at `com.github.copilot/agents/<name>.agent.md` or `skills/<name>/`, and connect it by [Connect the component](#connect-the-component).

## Connect the component

When you add, rename, or change the role of a component, keep its connections current:

- A worker sits in the `agents` list and the `Route the work` table of each lead that delegates to it, and in the `agents` list and workflow of `discuss` when a chat agent calls it.
- An entry agent lists in `agents` every worker its routing table names, and has a `discuss` handoff when it is a lead that receives shaped requests.
- A skill relies on its `description` for discovery.

## Validate

Validate the changed files on disk against the `copilot-customization` validation lists, the contract checklist for the kind, the questions above, and, for a package change, the static conformance checks in [packaging](references/packaging.md), and repair each failure.

The work is done when every connection is in place and every check passes.
