# Project Status

- **State:** `active`
- **Updated:** `2026-10-08`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Focus:** Batch 6 of the pre-release audit is next: the entry agents, reviewed by the `Customization authoring` section of the project instructions with the entry contract, their inspirations, and the pillars; nothing blocks it.

## Roadmap

1. `active` Audit and polish the plugin and `.github/` customizations slowly, taking each batch as a fresh, comprehensive look at its artifacts as a whole: their purpose, fit with the pillars, structure, coherence with each other and the repository instructions, accuracy against primary sources, and fitness for a capable model. Give an overall verdict per batch, then present findings one file at a time, fix only the findings the owner approves, and validate the whole batch before the next one starts.
   1. [ ] Batch 6: the entry agents `software-lead`, `data-lead`, and `discuss` against the entry contract, including whether the leads keep their three-retry caps, removing the `Checker model` condition both leads restate from `brief-subagent`, branching the leads' retry rule on the producers' failure classes, and deciding whether repeated failures route to `challenger`, who marks review per planned task, and whether the planner replans after a failed task.
   2. [ ] Batch 7: the `.github/instructions/` files and the `.github/skills/` skills.
2. `planned` Clean up stale record statements, `.gitignore`, and the local setup, including `CLAUDE.md`.
3. `planned` Revalidate the package, then run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes; the previous history and tags stay in the verified bundle `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.

## Blockers

- None.
