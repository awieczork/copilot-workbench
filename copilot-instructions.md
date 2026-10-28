# ds-copilot-workbench

This repository maintains the `ds-tools` marketplace and its independent plugin packages.
The catalog is `.github/plugin/marketplace.json`; it starts empty, and future packages belong under `plugins/<name>/`.

## Principles

- **Direction over detail.** State the goal, the reason for a non-obvious choice, and a useful approach; be exact where an action or value cannot vary.
- **Simple first, lean always.** Choose the simplest solution that meets the requirement. Add a file, step, or abstraction only when it solves a concrete problem.
- **Every word steers.** Use precise, plain wording and one term for each concept.

## Package boundaries

- Keep repository maintenance files under `.github/`; they are not plugin payload.
- Treat each `plugins/<name>/` directory as an independent package, and keep its files within that package.
- Add catalog sources only for packages under `./plugins/<name>` relative to the repository root; do not make plugins depend on other plugins or escape their package directories by default.
- Use the Agent Plugins 1.0 layout when the target client supports it: put `plugin.json` at the package root, portable skills under `skills/`, and MCP configuration in root `mcp.json`.
- Put Copilot-specific files under `com.github.copilot/`; treat commands and hooks as client-specific components, not portable Agent Plugins types, and verify client support before relying on them.
- Keep task state under `.github/context/` out of tracked documentation because it is local and is not present in other clones.

## Records

- Use `README.md` for the marketplace overview and its current empty state.
- Use `ARCHITECTURE.md` for package and catalog boundaries.
- Use the root `CHANGELOG.md` for marketplace changes; each plugin owns its own `CHANGELOG.md`.
- Use `plugins/README.md` for the future package layout and authoring rules.

## Versions and Git

- Version each plugin independently and tag its releases as `<plugin-name>/v<version>`; the root marketplace has no plugin version.
- Keep one development branch per coherent plugin or repository-maintenance cycle: `plugin/<exact-plugin-name>` or `repo/<short-kebab-topic>`. Resume it across tasks and sessions; after verified cleanup, create the next cycle branch from current `main`, with optional name reuse.
- Use [start-dev](skills/start-dev/SKILL.md) only for an explicit start or resume request; it may safely create or switch branches but never commits or pushes.
- Use [commit-dev](skills/commit-dev/SKILL.md) only for an explicit request to commit scoped active-cycle changes locally; pushing the cycle branch needs a separate explicit request.
- Review locally before an explicit [merge-dev](skills/merge-dev/SKILL.md) request, which authorizes one squash commit on `main`, a normal push to `origin`, and verified cleanup of local and remote cycle branches, when present.
- An explicit expected-tip lease protects only an authorized single-branch deletion, not commit updates. Never force-push or rewrite shared history, bypass hooks, or change credentials.
- Merge approval does not authorize publication; use [publish-plugin](skills/publish-plugin/SKILL.md) only for a separately approved per-plugin release.
- Report local scaffold checks separately from consumer installation tests. An empty catalog has no plugin to install, so scaffold checks do not prove that a consumer can install a plugin.
