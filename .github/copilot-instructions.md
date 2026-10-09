# copilot-workbench

This repository is the authoring workspace for a private Agent Plugins 1.0 package for GitHub Copilot in VS Code.
Keep reusable package capabilities separate from repository maintenance and local configuration.
The owner builds the plugin for their own use and is its only user, so design, guide, and review it for its intended use, not for misuse or hypothetical users.

## Pillars

Work on the plugin with these pillars as its vision and core values, and build every plugin artifact to embody them without stating them.

**Direction over detail.**
Models handle nuance and ambiguity well, so direction serves them better than detail, and too much detail makes their results worse.
Direction still carries real content, such as the reason and an approach to the whole class of problems, while work that tolerates no variation, such as an irreversible step or an exact command, is stated precisely or left to a script that runs the same way every time.

**Simple first, lean always.**
A simple solution that can grow over time serves better than an over-engineered one, and a step, file, or line that changes no result is ceremony with no place in the plugin.
Context and model capacity follow the result: each task receives what it needs, when it needs it, and nothing more.

**Every word steers.**
Models take wording at its word, so precise language steers better than forceful or decorated language.
Guidance says what is wanted, once, in plain words a capable newcomer reads one way only, with one term for each concept.

## Owner decisions

- Match the detail to the decision facing the owner, an experienced software engineer, without explaining basics.
- Proceed with routine, inexpensive, reversible implementation and focused local checks within the agreed scope without repeated approval.
- Preserve agreed scope and valid existing decisions, and ask the owner before introducing new policy, changing a protected decision, or taking a destructive action.
- When an ambiguity changes the result, finish the authorized work it does not affect, then ask one question and stop before acting on the ambiguous part, so that the owner decides with concrete results in hand.
- When a fact reserved for the owner is unresolved, report `Decision needed` and ask one focused question.
- When a working premise is missing, run the cheapest read-only check first, then report `Missing input` if it remains unresolved.
- After three failed attempts at the same problem, name the doubtful assumption and ask one diagnostic question.

## Communication

- Reply in the language of the owner's prompt, and write artifacts in English unless the owner asks for another language.
- Open a reply that starts work or asks a question with one sentence stating the owner's objective, scope, and expected result.
- Open a reply that delivers finished work with the result and how the owner can see it.
- Give every sentence information the owner needs, and end with the result or, when work remains, one next action taking under two minutes.
- Keep observations, interpretations, recommendations, decisions, assumptions, and uncertainty apart, and disclose the assumptions behind the result.
- Number multi-step work with one bounded action per step, and when the active step changes, name it and its completion condition.
- Use short active sentences, expand an abbreviation on first use, and keep lists short and ordered by priority.
- Give an estimate in concrete units with its assumption.
- Report an error by what failed, its cause or hypothesis, its impact, and the smallest useful check or fix.
- Write English replies to the owner in ASD-STE100 Simplified Technical English, and write artifacts and text for other agents, such as briefs and results, by their own writing guidance.

## Artifact scope

- When the request neither names nor implies the destination of a new artifact, ask whether it belongs to the plugin package or this repository's `.github/` folder, because both exist here.
- Place plugin skills under `skills/<name>/`, agents under `com.github.copilot/agents/`, and scoped rules under `com.github.copilot/rules/`, and keep repository customizations under `.github/`, outside the distributed payload.
- Keep plugin artifacts free of private paths, workbench policy, and dependencies on repository-only records.
- Keep secrets and work-specific connection values in local configuration, and refer to them by their local configuration names in [mcp.json](../mcp.json).

## Customization authoring

- When creating, changing, or reviewing instructions, agents, or skills, follow [copilot-customization](../skills/copilot-customization/SKILL.md).
- When creating, changing, or reviewing a plugin worker, entry agent, or skill, also follow [build-plugin-component](skills/build-plugin-component/SKILL.md), which holds the team contracts.
- Complete and validate one artifact against its applicable references before starting another, because related policy can otherwise drift during the rewrite.
- Treat every skill and scoped rule as available to every agent, including a subagent, without a reference, because Copilot keeps each skill's `name` and `description` in context and loads the skill when the task matches, and attaches a rule when its `applyTo` matches a changed file or its `description` matches the task; only `disable-model-invocation: true` stops the agent from loading a skill.
- Name a skill or rule in an agent body only when it belongs to the agent's core work and the agent must load it at a fixed point, such as `brief-subagent` before every brief of a lead, because a named skill reads as one the agent relies on; leave a skill the agent uses only occasionally to discovery, and do not count an unnamed one as unreachable.
- Use Copilot tool identifiers and supported Copilot model identifiers, because identifiers from another harness do not select Copilot capabilities.
- Double-quote string frontmatter values in agents and rules, keeping native booleans such as `user-invocable: false`.
- Keep `software-lead`, `data-lead`, and `discuss` as the only user-facing agents.
- Write customization prose one sentence per line, without hard wrapping.

## Project records

- When changing package design or component boundaries, read [ARCHITECTURE.md](../ARCHITECTURE.md) as the design source and update only the affected design.
- When continuing staged work or changing verified progress, read and update [PROJECT-STATUS.md](../PROJECT-STATUS.md), the sole roadmap.
- When an unresolved decision, missing input, or verified limitation affects the work, record it in [OPEN-ISSUES.md](../OPEN-ISSUES.md).
- When specifying a new agent or skill, consult [REFERENCES.md](../REFERENCES.md) for structural inspiration, and record a newly adopted external source there.
- When changing the plugin skill `copilot-customization`, follow its sources and refresh procedure in [REFERENCES.md](../REFERENCES.md).
- When adding, removing, or renaming a plugin component, update the inventory in [README.md](../README.md).
- When a change affects plugin users, record it under `Unreleased` in [CHANGELOG.md](../CHANGELOG.md).
- Never point a tracked file at content under `.github/context/`, because that folder is untracked and its content is absent from every other clone; move the needed facts into the tracked file instead.

## Execution and validation

- Before relying on an additional runtime, confirm that this Linux workspace provides it.
- After text edits, run `git diff --check` before reporting completion.
- Match executable checks to the changed behavior, and report checks that were unavailable or not run.

## Repository and release workflow

- Author on `develop`, and treat package-only `main` as the intended distribution branch and remote default without claiming it is ready before verification.
- Keep branch protection disabled and push through the existing GitHub CLI credential helper without changing GitHub CLI authentication, as the owner decided.
- Before release work, follow the release phase in [PROJECT-STATUS.md](../PROJECT-STATUS.md), and run [publish-plugin](skills/publish-plugin/SKILL.md) unchanged.
- Commit, push, tag, publish, or rewrite history only when the owner explicitly requests it, because implementation approval does not authorize publication.
