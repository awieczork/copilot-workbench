# ds-copilot-workbench

This repository is the authoring workspace for the `ds-tools` plugin marketplace.
The catalog is [`.github/plugin/marketplace.json`](.github/plugin/marketplace.json) and currently contains no plugins.
There is no root plugin manifest or distributed plugin payload.

## Repository guide

| File or directory | Purpose |
| --- | --- |
| [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Workspace guidance and package boundaries |
| [`ARCHITECTURE.md`](ARCHITECTURE.md) | Catalog, package, and release boundaries |
| [`plugins/README.md`](plugins/README.md) | Future package layout and authoring rules |
| [`CHANGELOG.md`](CHANGELOG.md) | Marketplace-level changes |
| `plugins/<name>/` | Independent plugin packages when added |

## Development cycles and releases

Each plugin owns its version and uses tags in the form `<plugin-name>/v<version>`.
The root `CHANGELOG.md` records marketplace changes, and each plugin keeps its own `CHANGELOG.md`.
Keep one development branch per coherent plugin or repository-maintenance cycle, named `plugin/<exact-plugin-name>` or `repo/<short-kebab-topic>`.
Resume that branch across tasks and sessions; after cleanup, start the next cycle from the current `main` on a fresh branch, with optional name reuse.
An explicit `/start-dev` request authorizes safe cycle-branch creation or switching only; it never commits or pushes.
An explicit `/commit-dev` request commits only scoped active-cycle changes locally, and pushing the cycle branch needs a separate explicit request.
Review the cycle locally before `/merge-dev`; that explicit request authorizes one squash commit on `main`, a normal push of `main` to `origin`, and verified cleanup of local and remote cycle branches, when present.
Cleanup proceeds only after verification succeeds; an explicit expected-tip lease protects only an authorized single-branch deletion, never commit updates.
The skills use direct Git checks for routine state and cleanup; the narrow verifier checks only exact squash content.
Merge approval does not authorize plugin publication, which remains a separate per-plugin action.
When `main` has no commits, starting a real cycle requires committed `main` and cached `origin/main` first.
The initial commit and push require a separate owner request and are not part of cycle start.

## Maintenance skills

- Use [build-plugin](.github/skills/build-plugin/SKILL.md) to create or change a selected package.
- Use [start-dev](.github/skills/start-dev/SKILL.md) for an explicit request to start or resume a development cycle.
- Use [commit-dev](.github/skills/commit-dev/SKILL.md) for an explicit scoped local commit or separately requested cycle-branch push.
- Use [merge-dev](.github/skills/merge-dev/SKILL.md) only after local review and explicit merge approval.
- Run [publish-plugin](.github/skills/publish-plugin/SKILL.md) only to check or publish one selected plugin.

## Verification

Run the local static checker from the repository root with `uv` installed:

```bash
uv run --no-project .github/skills/build-plugin/scripts/check_package.py
```

Run the focused Git workflow tests against local repositories and bare remotes:

```bash
uv run --offline --no-project python -m unittest discover -s .github/skills/merge-dev/tests
```

These local checks can validate the catalog, package layout, squash verification, guarded cleanup commands, and repository files.
They do not prove that skills activate in VS Code, GitHub remote operations succeed, or a consumer can install or run a plugin.
Because the catalog is empty, a consumer installation smoke test cannot run yet.
