---
name: build-plugin-component
description: "Use when creating, changing, or reviewing a plugin worker, entry agent, or skill under com.github.copilot/agents/ or skills/. Supplies the team contracts and the connections that fit a component into the plugin's team. Not for packaging, manifests, or publication."
---

# Build a plugin component

Create or change a plugin worker, entry agent, or skill so that it fits the plugin's team and reaches the agents that use it.

## Procedure

1. Follow [copilot-customization](../../../skills/copilot-customization/SKILL.md) for the artifact type, and read the contract for the component's kind before writing, because the contract defines how it fits the team:
   - Worker: [worker contract](references/worker-contract.md), and [model tiers](references/model-tiers.md) for its `model` list.
   - Entry agent: [entry contract](references/entry-contract.md).
   - Skill: [skill contract](references/skill-contract.md).
2. For a new component, draft a specification from the request and the plugin, and present it to the owner with only the questions whose answers change it: `name`, `description`, and kind; tools, `agents`, `model`, and `handoffs`; what proceeds without asking; workflow phases and output slots; its connections; and the plugin components it overlaps, with a recommendation to extend one that covers the need.
3. After the owner confirms the specification, write the component at `com.github.copilot/agents/<name>.agent.md` or `skills/<name>/`, and connect it by [Connect the component](#connect-the-component).
4. Validate the files on disk against the `copilot-customization` validation lists, the contract checklist, and [Check the pillars](#check-the-pillars), and repair each failure.

The work is done when every connection is in place and every checklist item passes.

## Check the pillars

Ask each question of every line, section, and file of the component; a "no" marks a change to make.

Direction over detail:

- [ ] Does each rule give the goal and its reason, and cover the whole class of problems instead of listing cases?
- [ ] Is each enumeration needed, or would the principle behind it steer the same way?
- [ ] Is precise detail kept for work that tolerates no variation, such as an approval gate or an exact command, and is a behavior that must repeat exactly left to a script?
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
- [ ] Does each qualifier change behavior?

## Connect the component

- For a worker, add it to the `agents` list and the `Route the work` table of each lead that delegates to it, and to the `agents` list and workflow of `discuss` when it is a helper that a chat agent calls.
- For an entry agent, list in `agents` every worker its routing table names, and add a `discuss` handoff when it is a lead that receives shaped requests.
- For a skill, rely on its `description` for discovery, and name it in an agent body only under the naming rule in the [skills reference](../../../skills/copilot-customization/references/skills.md).
- When a change alters a contract, update the plugin agents it governs in the same change, so that shipped agents keep matching the contract.
