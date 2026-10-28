# Architecture

## Catalog and packages

The marketplace catalog is `.github/plugin/marketplace.json`; it is not a plugin package and has no plugin version.
Catalog entries point to package directories with repository-root-relative sources such as `./plugins/<name>`.
The catalog currently has no entries, and the repository has no root `plugin.json`.
Repository maintenance files stay under `.github/` and are not included in plugin payloads.

Each future `plugins/<name>/` directory is an independent package with its own manifest, documentation, changelog, and optional components.
Keep package files inside their package directory, and do not make one plugin depend on another plugin's files or use paths outside its package by default.

## Package format

Use the Agent Plugins 1.0 manifest and canonical schema for packages when the target client supports that format.
Portable skills live under `skills/`, and portable MCP configuration lives in root `mcp.json`.
Copilot-specific files use the `com.github.copilot/` namespace; commands and hooks are client-specific capabilities, not portable component types.
Confirm client support before relying on a component or describing a package as compatible.

## Development cycles and releases

The root `CHANGELOG.md` records marketplace changes, and each plugin owns a separate `CHANGELOG.md` for its package changes.
Version plugins independently and tag plugin releases as `<plugin-name>/v<version>`.
Keep one development branch per coherent plugin or repository-maintenance cycle, named `plugin/<exact-plugin-name>` or `repo/<short-kebab-topic>`.
Resume that branch across tasks and sessions; after verified cleanup, create the next cycle branch from the current `main`, with optional name reuse.
An explicit [start-dev](.github/skills/start-dev/SKILL.md) request authorizes safe branch creation or switching only, never a commit or push.
An explicit [commit-dev](.github/skills/commit-dev/SKILL.md) request authorizes scoped local commits; pushing the cycle branch needs a separate explicit request.
Review locally before an explicit [merge-dev](.github/skills/merge-dev/SKILL.md) request, which authorizes one squash commit on `main`, a normal push of `main` to `origin`, and verified cleanup of local and remote cycle branches, when present.
An explicit expected-tip lease protects only an authorized single-branch deletion and never authorizes forced commit updates.
The skills use direct Git checks for routine state; the squash verifier checks only that a commit's sole parent and tree match the recorded merge.
Merge approval does not authorize publication; [publish-plugin](.github/skills/publish-plugin/SKILL.md) remains a separate per-plugin action.

## Validation boundary

Local checks can validate catalog JSON, package structure, repository documentation, squash content, and cleanup commands in disposable Git fixtures.
The empty catalog has no plugin to install, so local checks cannot establish consumer installation or runtime behavior.
