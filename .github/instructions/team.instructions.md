---
description: "Use when authoring agent-team components. Supplies the existing shared team conventions. Not for other packages or project customizations."
applyTo: "plugins/agent-team/**"
---

# Team conventions

- Keep workbench policy and the root records out of plugin artifacts, because the plugin runs in other projects.
- Count every skill and rule as reachable by every agent, including a subagent, through its `description` or `applyTo`, so that an unnamed skill is no gap.
- Take each tool identifier from the VS Code tools reference or the tool list of the extension or MCP server that contributes it, and each model name from GitHub's supported-models list for VS Code, because VS Code silently ignores a name it does not recognize.
- Double-quote string frontmatter values in agents and rules, and keep native booleans such as `user-invocable: false`, because one quoting style keeps a colon in any value from breaking the frontmatter.
- Give every agent that writes code, a query, or a plan this documentation line unchanged, because it is the principle behind every check of an interface:

  ```markdown
  Before you rely on a library, an external API, or a tool in code, a query, or a plan, read its documentation for the version the project uses with the `context7` tools, and when they cannot answer, fetch the official documentation and record the gap, because what you remember of an interface can be outdated.
  ```

For a team skill:

- Keep task state only through the `task-context` skill, because agents look for task state only in its folder.
- Leave the communication style out of the skill, because entry agents own it; an output format holds only the content of the skill's result.

## Work from an example

- When a change reaches several components of one kind, refine one real component with the owner first, write what it taught into the contract for its kind, and then apply the contract to the other components, because a contract written from an accepted example states the owner's expectation instead of a guess.
- When a change alters a contract, update the components it governs in the same change, so that shipped components keep matching it.

## Add a component

1. Draft a specification of the component: every part its contract defines, its connections, and the components it overlaps.
1. Present it to the owner with only the questions whose answers change it, and recommend extending an overlapping component that covers the need.
1. After the owner confirms, write the component at the path the package defines for its kind, and connect it by "Connect the component" below.

## Connect the component

When you add, rename, or change the role of a component, keep its connections current:

- A worker sits in the `agents` list and the `Route the work` table of each lead that delegates to it, in the `agents` list and workflow of each chat agent that calls it, and, for a checker, in the `agents` list and review phase of each producer that calls it.
- A renamed component is renamed wherever another component names it, including `agents`, `handoffs`, and bodies.
- A lead that receives shaped requests is a `handoffs` target of each chat agent.

## Subagent line

When a step that a subagent may run asks the user, and the skill does not set `disable-model-invocation: true`, add this line unchanged after the opening sentence, and let the other steps say "ask the user":

```markdown
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.
```
