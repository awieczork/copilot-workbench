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

## Working with the owner

- Act without asking on work that is routine, inexpensive, and reversible within the agreed scope, and ask before introducing new policy, changing a protected decision, or taking an action you cannot undo.
- When an ambiguity changes the result, finish the work it does not affect, then ask one question and stop, so that the owner decides with concrete results in hand.
- When a fact reserved for the owner is unresolved, report `Decision needed` and ask one focused question; when a working premise is missing, run the cheapest read-only check, then report `Missing input` if it remains unresolved.
- Before relying on a runtime, tool, path, or external fact, confirm it in this Linux workspace or its primary documentation, because a recalled fact can be stale.
- After three failed attempts at the same problem, name the doubtful assumption and ask one diagnostic question.

## Communication

- Reply in the language of the owner's prompt, and write artifacts in English unless the owner asks for another language.
- Match the detail to the decision facing the owner, an experienced software engineer, without explaining basics.
- Write English replies to the owner in ASD-STE100 Simplified Technical English, and write artifacts and text for other agents by their own writing guidance.
- Open a reply that starts work or asks a question with one sentence stating the owner's objective, scope, and expected result, and open a reply that delivers finished work with the result and how the owner can see it.
- Give every sentence information the owner needs, and end with the result or, when work remains, one next action taking under two minutes.
- Keep observations, interpretations, recommendations, decisions, assumptions, and uncertainty apart, and disclose the assumptions behind the result.
- Number multi-step work with one bounded action per step, and when the active step changes, name it and its completion condition.
- Expand an abbreviation on first use, and keep lists short and ordered by priority.
- Give an estimate in concrete units with its assumption, and report an error by what failed, its cause or hypothesis, its impact, and the smallest useful check or fix.

## Where artifacts belong

- When the request neither names nor implies the destination of a new artifact, ask whether it belongs to the plugin package or this repository's `.github/` folder, because both exist here.
- Keep repository customizations under `.github/`, outside the distributed payload.
- Complete and validate one artifact before starting another, because related policy can otherwise drift during a rewrite.
- Keep secrets and work-specific connection values in local configuration, and refer to them by their local configuration names in [mcp.json](../mcp.json).

## Authoring

- When creating, changing, or reviewing any part of the plugin, follow [build-plugin](skills/build-plugin/SKILL.md), which holds the pillar questions, the contracts, and the packaging rules.
- When creating, changing, or reviewing a repository customization under `.github/`, follow [copilot-customization](../skills/copilot-customization/SKILL.md).

## Project records

Keep each fact in the record that owns it, and update that record in the same change:

- [ARCHITECTURE.md](../ARCHITECTURE.md): package design and component boundaries; read it before changing either.
- [PROJECT-STATUS.md](../PROJECT-STATUS.md): the sole roadmap and verified progress; read it before continuing staged work.
- [OPEN-ISSUES.md](../OPEN-ISSUES.md): unresolved decisions, missing inputs, and verified limitations that affect the work.
- [REFERENCES.md](../REFERENCES.md): external sources adopted for structure, consulted when specifying a new component; follow its sources and refresh procedure when changing `copilot-customization`.
- [README.md](../README.md): the inventory of plugin components.
- [CHANGELOG.md](../CHANGELOG.md): changes that affect plugin users, under `Unreleased`.

Never point a tracked file at content under `.github/context/`, because that folder is untracked and its content is absent from every other clone; move the needed facts into the tracked file instead.

## Validation

- After text edits, run `git diff --check` before reporting completion.
- Match executable checks to the changed behavior, and report checks that were unavailable or not run.

## Repository and release workflow

- Author on `develop`, and treat package-only `main` as the intended distribution branch and remote default without claiming it is ready before verification.
- Keep branch protection disabled and push through the existing GitHub CLI credential helper without changing GitHub CLI authentication, as the owner decided.
- Before release work, follow the release phase in [PROJECT-STATUS.md](../PROJECT-STATUS.md), and run [publish-plugin](skills/publish-plugin/SKILL.md) unchanged.
- Commit, push, tag, publish, or rewrite history only when the owner explicitly requests it, because implementation approval does not authorize publication.
