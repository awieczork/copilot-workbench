---
name: build-plugin
description: "Use when creating, changing, or reviewing any plugin component: an agent, a skill, a rule, plugin.json, .mcp.json, or another packaged file. Supplies the authoring method, the team contracts, and the packaging rules, and points to the review questions. Not for commits or publication."
---

# Build the plugin

Change the plugin so that every component gives direction, fits the team, and ships in a valid package.
Write each component by [copilot-customization](../../../skills/copilot-customization/SKILL.md) for its type; this skill adds what the plugin's team and package need.
As a subagent, return each question or choice for the owner to the delegating agent instead of asking the owner.

## Work from an example

- When a change reaches several components of one kind, refine one real component with the owner first, write what it taught into the contract for its kind, and then apply the contract to the other components, because a contract written from an accepted example states the owner's expectation instead of a guess.
- When a change alters a contract, update the components it governs in the same change, so that shipped components keep matching it.

## Review a component

Review a component by "Review artifacts" in `copilot-customization`, and ask each question of its [writing guidance](../../../skills/copilot-customization/references/writing.md) across the whole team as well as within the component, counting a block that a contract requires word for word as stated once.

## Read the contract for the kind

- Entry agent: [entry contract](references/entry-contract.md).
- Worker: [worker contract](references/worker-contract.md), and [model tiers](references/model-tiers.md) for its `model` list.
- Skill: [skill contract](references/skill-contract.md).
- `plugin.json`, `.mcp.json`, the package structure, or a packaged path: [packaging](references/packaging.md).

A rule has no contract.

## Keep the team's conventions

- Keep workbench policy and the root records out of plugin artifacts, because the plugin runs in other projects.
- Count every skill and rule as reachable by every agent, including a subagent, through its `description` or `applyTo`, so that an unnamed skill is no gap.
- Take each tool identifier from the VS Code tools reference or the tool list of the extension or MCP server that contributes it, and each model name from GitHub's supported-models list for VS Code, because VS Code silently ignores a name it does not recognize.
- Double-quote string frontmatter values in agents and rules, and keep native booleans such as `user-invocable: false`, because one quoting style keeps a colon in any value from breaking the frontmatter.
- Give every agent that writes code, a query, or a plan this documentation line unchanged, because it is the principle behind every check of an interface:

  ```markdown
  Before you rely on a library, an external API, or a tool in code, a query, or a plan, read its documentation for the version the project uses with the `context7` tools, and when they cannot answer, fetch the official documentation and record the gap, because what you remember of an interface can be outdated.
  ```

## Add a component

1. Draft a specification of the component: `name`, `description`, and kind; tools, `agents`, `model`, and `handoffs`; what proceeds without asking; workflow phases and output slots; its connections; and the components it overlaps.
2. Present it to the owner with only the questions whose answers change it, and recommend extending an overlapping component that covers the need.
3. After the owner confirms, write the component at the path [packaging](references/packaging.md) gives for its kind, and connect it by "Connect the component" below.

## Connect the component

When you add, rename, or change the role of a component, keep its connections current:

- A worker sits in the `agents` list and the `Route the work` table of each lead that delegates to it, in the `agents` list and workflow of each chat agent that calls it, and, for a checker, in the `agents` list and review phase of each producer that calls it.
- A renamed worker is renamed wherever another agent's body names it.
- A lead lists in `agents` every worker its routing table names, and a lead that receives shaped requests is a `handoffs` target of each chat agent.

## Validate

Validate the changed files on disk against the `copilot-customization` type reference and writing questions, the contract for the kind, and, for a package change, the check in [packaging](references/packaging.md), and repair each failure.

The work is done when every connection is in place and every check passes.
