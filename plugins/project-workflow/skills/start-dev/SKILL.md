---
name: start-dev
description: "Use when the user explicitly asks to start or resume one development cycle on a Git branch. Establishes the exact cycle branch and a session-scoped grant for checked local commits within that cycle. Not for integration or remote effects."
argument-hint: "[kind] [topic]"
disable-model-invocation: true
---

# Start a development cycle

Start or resume exactly one local cycle and grant bounded commit permission after the user resolves any ambiguous name or unsafe working state.
A cycle is one bounded change on a `<kind>/<topic>` branch that [end-dev](../end-dev/SKILL.md) later integrates into the integration branch with one squash commit.
As a subagent, return required user questions to the delegating agent.

## Project conventions

When project instructions define cycle kinds, naming rules, or the scope of each kind, follow them.
Otherwise, accept any lowercase kind word, such as `feat`, `fix`, or `docs`, and scope the cycle to paths demonstrably related to its topic.
The integration branch is the branch the project instructions name, or else the default branch that `git symbolic-ref --short refs/remotes/origin/HEAD` resolves, without its `origin/` prefix.

## Commit permission

An explicit user request to start or resume a cycle grants permission for new local commits of complete, checked work within that cycle, on the exact selected branch.
A branch name or permission to carry existing dirty work does not grant commit permission; a new session needs a new explicit start or resume request.
The grant ends when the selected branch changes, the cycle closes, or the user revokes it.
Never use the grant for the integration branch, another cycle, pushes, integration, or publication.
Use the [cycle commit procedure](references/commit.md) for each permitted commit.

## Procedure

1. Require one kind and one topic, such as `/start-dev feat csv-export`. Ask for a missing value when the request does not resolve to exactly one `<kind>/<topic>` branch. The kind is one lowercase word and the topic is lowercase hyphen-separated words, unless project naming rules say otherwise. Require `git check-ref-format --branch <target>` to succeed.
2. Run `git branch --show-current`, `git status --short --branch`, and `git status`. Stop on detached `HEAD` or an unfinished operation. Check Git paths for `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`, `rebase-merge`, `rebase-apply`, and `sequencer`; resolve each with `git rev-parse --git-path`. List staged, unstaged, and untracked paths separately and require explicit permission to carry dirty work. Never stash, reset, discard, or edit those paths.
3. Resolve the integration branch. Stop and ask when the repository has no `origin` remote or the default branch cannot be resolved.
4. If `refs/heads/<target>` exists, report that it is already current or resume it. If only `refs/remotes/origin/<target>` exists, ask how to handle that remote-only branch; do not recreate it or configure tracking implicitly.
5. Before creating a branch, require committed `refs/heads/<integration-branch>` and cached `refs/remotes/origin/<integration-branch>`; compare full commit IDs with `git rev-parse --verify`. Stop if either is missing or they differ. Do not fetch or update the integration branch.
6. Immediately before switching or creating, repeat the status and unfinished-operation checks. If new dirty paths appear, stop for explicit permission to carry them without changing them. Repeat the integration branch equality check for a new branch. Resume with `git switch -- <target>` or create with `git switch --no-guess -c <target> <integration-branch>`.
7. Confirm the exact target with `git branch --show-current` and report `git status --short --branch`. Verify that the paths permitted for carry-over remain present; do not resolve their changes for the user.

## Completion

This procedure changes only local branch selection or creation; it does not create a commit or contact a remote.
Report the exact cycle scope and the active commit grant, which applies only in the current session.
Report the verified result:

```markdown
- Branch: {exact target}
- Operation: {already current | resumed | created}
- Integration branch: {exact branch}
- Cycle scope: {scope the project defines for the kind | paths related to the topic}
- Carried paths: {explicitly permitted paths | none}
- Commit permission: {active for checked local commits on this branch in this session}
```
