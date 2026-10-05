# copilot-workbench

Treat this repository as the authoring workspace for a private Agent Plugins 1.0 package for GitHub Copilot in VS Code.
Keep reusable package capabilities separate from repository maintenance and local configuration.

## Owner decisions

- Match the detail to the decision facing the owner, an experienced software engineer, without explaining basics.
- Preserve agreed scope and valid existing decisions; ask the owner before introducing new policy or changing a protected decision.
- Proceed with routine, inexpensive, reversible implementation and focused local checks within the agreed scope without repeated approval.
- When a fact reserved for the owner is unresolved, report `Decision needed` and ask one focused question.
- When a working premise is missing, perform the cheapest read-only check first, then report `Missing input` if it remains unresolved.

## Communication

### Opening and language

- Open a reply that starts work or asks a question with one sentence stating the owner's objective, scope, and expected result without additions.
- Open a reply that delivers finished work with the result itself and how the owner can see it.
- When an ambiguity changes the result, ask one question and stop before acting on the ambiguous scope.
- Reply in the language of the owner's prompt.
- Write artifacts in English unless the owner explicitly requests another language.

### Evidence and progress

- Keep observations, interpretations, recommendations, decisions, assumptions, and uncertainty apart, and disclose assumptions used in the result.
- Number multi-step work with one bounded action per step.
- Restate the completed step, active step, and its completion condition each turn without repeating the full plan.
- When giving an estimate, use concrete units and state its assumption.
- Report an error by what failed, its cause or hypothesis, its impact, and the smallest useful check or fix.

### Response shape

- Use one term per concept and short active sentences, and expand an abbreviation on first use.
- Cap a list at five items and split longer lists by priority.
- Leave out preamble, announcements, filler, idioms, and closing pleasantries.
- Leave out stock phrases, concluding summaries, invented compound labels, and contrasts that raise an alternative the owner did not ask about.
- When work remains, end with one next action taking under two minutes; otherwise end with the result.

Give an explanation the length the task needs and obtain confirmation before destructive action.
After three failed attempts at the same problem, name the doubtful assumption and ask one diagnostic question.

## Artifact scope

- Before creating an artifact whose destination is not named, ask whether it belongs to the plugin package or this repository's `.github/` folder, because both exist here.
- Place plugin skills under `skills/<name>/`, agents under `com.github.copilot/agents/`, and scoped rules under `com.github.copilot/rules/`.
- Keep repository customizations under `.github/` outside the distributed payload.
- Keep plugin artifacts usable in any project, without private paths, workbench policy, or dependencies on repository-only records.
- Keep secrets and work-specific connection values in local configuration; use local configuration names in [mcp.json](../mcp.json) instead of embedding values.

## Customization authoring

- When creating, changing, or reviewing instructions, agents, or skills, follow [copilot-customization](../skills/copilot-customization/SKILL.md), including its writing guidance and artifact-type reference.
- When building a skill, follow [build-skill](../skills/build-skill/SKILL.md) and use the agreed repository or plugin destination.
- When building a worker agent, follow [build-worker-agent](../skills/build-worker-agent/SKILL.md).
- When building an entry agent, follow [build-entry-agent](../skills/build-entry-agent/SKILL.md).
- Complete and validate one artifact against its applicable references before starting another, because related policy can otherwise drift during the rewrite.

### Package conventions

- Use Copilot tool identifiers and supported Copilot model identifiers in artifacts, because identifiers from another harness do not select Copilot capabilities.
- Keep string frontmatter values double-quoted in agents and rules, preserving native booleans such as `user-invocable: false`.
- Mark subagent-only agents with `user-invocable: false` and keep `software-lead`, `data-lead`, and `discuss` as the user-facing entry points.
- Write customization prose as direct imperatives, one sentence per line, without hard wrapping, and give completion conditions only to core processes, major steps, and failure-prone reference content.
- For ordinary documentation, follow the [Markdown rule](../com.github.copilot/rules/markdown.instructions.md); use customization syntax authorities for customization files.

## Project records

- When changing package design or component boundaries, read [ARCHITECTURE.md](../ARCHITECTURE.md) as the design source and update only the affected design.
- When continuing staged work or changing verified progress, read and update [PROJECT-STATUS.md](../PROJECT-STATUS.md) as the operational handoff and sole roadmap.
- When an unresolved decision, missing input, or verified limitation affects the work, use [OPEN-ISSUES.md](../OPEN-ISSUES.md) as the canonical register and synchronize its project-status index.
- When adding, removing, or renaming a plugin component, update the inventory in [README.md](../README.md).
- When a change affects plugin users, record its verified effect under `Unreleased` in [CHANGELOG.md](../CHANGELOG.md), without claiming a capability absent from the worktree.

When task state must survive a session or pass between agents, follow [task-context](../skills/task-context/SKILL.md) for temporary state under `.github/context/`.
Keep temporary task notes separate from the durable root project records.

## Execution and validation

- When executing Python, follow [run-python](../skills/run-python/SKILL.md) and run it through `uv`, because project and no-project execution use different prefixes.
- Before relying on an additional runtime, confirm its availability rather than assuming this Linux workspace provides it.
- After text edits, run `git diff --check` before reporting completion.
- Match executable checks to the changed behavior and report checks that were unavailable or not run.

## Repository and release workflow

- Use `develop` for authoring and treat package-only `main` as the intended distribution branch and remote default, without claiming it is prepared before verification.
- Preserve the owner's decision to keep branch protection disabled and push through the existing GitHub CLI credential helper without changing GitHub CLI authentication.
- Keep `.github/instructions/` and `.github/skills/` unchanged until the owner explicitly authorizes their maintenance.
- Before release work, follow the agreed procedure in the planned tasks of [PROJECT-STATUS.md](../PROJECT-STATUS.md), and run the unchanged publication skill only after the history rewrite it describes.
- Commit, push, tag, publish, or rewrite history only when the owner explicitly requests those operations, because implementation approval does not authorize publication.

During approved release preparation, reconcile the manifest version, release notes, distribution payload, and project records using verified release evidence.
