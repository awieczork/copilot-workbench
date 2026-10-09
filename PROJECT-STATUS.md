# Project Status

- **State:** `active`
- **Updated:** `2026-10-09`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Focus:** The plugin-authoring layer is separated and validated in the working tree, so `v0.1.0` ships only the agent team and general-use skills and rules; it awaits the owner's review and commit before the release phase starts.

## Roadmap

1. `active` Separate the plugin-authoring layer: the plugin ships the agent team and general-use skills and rules, including `copilot-customization` and the project-record rules, and the workbench's `.github/` holds the meta layer; projects keep only standalone customizations, and nothing in a project joins the plugin's team.
   1. [x] Create the repository skill `.github/skills/build-plugin-component/` with a short procedure that points to `copilot-customization`, and move the worker, model-tier, entry, and skill contracts into its `references/` without their project-side wording or the skill-name collision rule.
   2. [x] Remove `build-entry-agent`, `build-worker-agent`, and `build-skill` from `skills/`.
   3. [x] Route plugin-component authoring in the repository instructions to the new skill.
   4. [x] Update `ARCHITECTURE.md`, the `README.md` inventory, and the `CHANGELOG.md` `Unreleased` section.
   5. [x] Validate frontmatter, links, and stale references, and run `git diff --check`.
   6. [x] Ship the `changelog`, `project-status`, and `open-issues` rules as general-use plugin rules, keeping one copy under `com.github.copilot/rules/` and pointing Claude Code to it from `CLAUDE.md`.
2. `planned` Revalidate the package, then run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes; the previous history and tags stay in the verified bundle `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.

## Blockers

- None.
