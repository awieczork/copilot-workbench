---
name: build-plugin
description: "Use when creating, changing, or reviewing components for a plugin under `plugins/<name>/`. Supplies Agent Plugins 1.0 layout and authoring contracts. Not for commits or release publication."
---

# Build a plugin

Create or revise one selected plugin package while keeping its components portable and correctly placed.
Write and review each customization by [copilot-customization](../copilot-customization/SKILL.md), including its type reference and writing questions.
As a subagent, return each question or choice for the owner to the delegating agent instead of asking the owner.

## Author and review

For a change to several components of one kind, refine one real example first and record its accepted pattern before applying it to the others.
When a contract changes, update the components it governs in the same change.
Identify each component's responsibility, connections, and overlap before adding it; ask only about unresolved choices that change the result.
Review the changed component within the package as well as on its own, and update references, delegation lists, and handoffs when names or responsibilities change.

## Procedure

1. Select one explicitly requested package under `plugins/<name>/` and inspect its catalog entry before editing. For an existing package, confirm the matching entry; for a new package, add the matching `./plugins/<name>` entry to `.github/plugin/marketplace.json` in the same change.
2. Read [packaging](references/packaging.md) when changing a manifest, package layout, or component path.
3. Read [the skill contract](references/skill-contract.md) when creating or revising a skill.
4. Complete and validate one component before starting the next, using the loaded contracts for its location and content.

## Static validation

Resolve [the checker](scripts/check_package.py) from this skill's loaded location, not from the target repository.
From the target repository root, run `uv run --no-project` followed by the checker's absolute path; an optional final argument selects another repository root.
The script declares Python and PyYAML dependencies inline.

Exit `0` prints a static-check success message; it does not establish client installation or runtime compatibility.
Exit `1` prints up to 50 `path: message` errors to standard output, with each message limited to 240 characters and a count of omitted errors.
Exit `2` reports incorrect arguments to standard error.
Repair failures caused by the change and rerun the checker.

When changing the checker, run [its tests](tests/test_check_package.py) with `uv run --no-project --with pyyaml python -m unittest discover -s` followed by the absolute test-directory path.

## Boundaries

- Keep edits to an existing package scoped to that package. Creating an explicitly requested new plugin also includes its matching catalog entry in the same change.
- Do not add a root `plugin.json` or an unrequested sample or placeholder package. A catalog must list at least one real package.
- Keep required resources inside the selected package and use relative links that resolve from the linking file.
- Use one package's own authoring contracts and do not impose a team, worker, or model taxonomy on other plugins.

The work is complete when the selected package passes the static checker and every requested component is present at its Agent Plugins 1.0 location.
