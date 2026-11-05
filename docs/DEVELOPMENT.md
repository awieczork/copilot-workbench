# Development

This repository contains the source and checks for the `awieczork-tools` marketplace packages.
The [project-workflow development cycle](../plugins/project-workflow/README.md#development-cycle) provides the cycle commands, and the [agent-plugin-dev workflow](../plugins/agent-plugin-dev/README.md#usage) provides the authoring and release commands.

## Branch model

`main` is the full-repository distribution branch and marketplace source.
A push to `main` makes package files available through the marketplace even without a new tag or GitHub release.

A **cycle branch** holds one bounded change before it is integrated into `main` with a squash merge, which combines the cycle into one commit.
Package changes use `plugin/<exact-name>`; repository maintenance uses `repo/<lowercase-kebab-topic>`.

Local and remote `develop` are retired.
`archive/develop-before-marketplace` preserves their frozen tip, and the full-repository history and legacy tags remain unchanged.

## Development workflow

Installed skill commands use their package prefix, such as `project-workflow:` or `agent-plugin-dev:`.

1. Start or resume one cycle with `/project-workflow:start-dev plugin <name>` or `/project-workflow:start-dev repo <topic>`.
1. Make and check the changes on that cycle branch.
	The `build-plugin` and `copilot-customization` skills support package authoring and review; the agent can select them, or the user can invoke them directly.
1. Run `/project-workflow:end-dev` to check and review the cycle, prepare package versions and notes, and integrate the completed work into `main`.
1. Optionally run `/agent-plugin-dev:publish-plugin <name>` to check and publish one package already on `main`.

Each package README describes its commands, requirements, and limits.

## Versions and releases

Each package's `plugin.json` is its version authority.
Catalogs omit versions, and each package's `CHANGELOG.md` records its own history.
The [root changelog](../CHANGELOG.md) records repository and marketplace changes.

Prepare package versions and versioned notes on the cycle branch before integration, because distribution changes when `main` is pushed.
Publication selects one catalog package from clean, committed `main` and uses its version and notes.
Release versions must increase; for `agent-team`, this comparison also includes the legacy `v*` tags.

Tags use `<package>/v<version>`, for example `agent-team/v0.3.0`.
Each tag points to a full-repository commit, not a filtered package snapshot.
Tags and [GitHub releases](https://github.com/awieczork/copilot-workbench/releases) identify a release; they do not control marketplace file availability.

## Static checks

Run these commands from the repository root with `uv` and Git installed.
The package checker declares its Python and PyYAML dependencies.

```bash
uv run --no-project plugins/agent-plugin-dev/skills/build-plugin/scripts/check_package.py
git diff --check
```

The checker validates package structure, manifests, catalog identity, component names, repository skill pointers, and local package links.
It does not prove installation, client discovery, service connections, or runtime compatibility.
After Markdown changes, also check relative links and heading anchors from each changed document.

When changing a checker or lifecycle helper, run its tests:

```bash
uv run --no-project --with pyyaml python -m unittest discover -s plugins/agent-plugin-dev/skills/build-plugin/tests
uv run --no-project python -m unittest discover -s plugins/project-workflow/skills/end-dev/tests
uv run --no-project python -m unittest discover -s plugins/agent-plugin-dev/skills/publish-plugin/tests
```

These tests use local fixtures and do not establish live service permissions or client behavior.

## Contributions and license

The repository is maintained for personal use and does not accept external contributions or provide public support.
You can study, use, and adapt the code under the [MIT license](../LICENSE).
