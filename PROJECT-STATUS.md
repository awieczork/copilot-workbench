# Project Status

- **State:** `active`
- **Updated:** `2026-10-09`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Focus:** The pillar-alignment pass rewrites the agents, skills, and authoring contracts as direction, with `data-lead` as the reference lead, so that the first release ships the new shape.

## Roadmap

1. `active` Align the plugin and its authoring skills with the pillars, by refining one example per component kind, writing it into the contract, and applying the contract to the rest.
   1. [ ] Create the `build-plugin` skill from `build-plugin-component` and `agent-plugin-authoring`, with the pillar questions and the authoring method, and reduce the customization section of the project instructions to an overview and a link.
   2. [ ] Rewrite the entry contract from `data-lead`, then align `software-lead` and `discuss`.
   3. [ ] Refine `database-explorer`, rewrite the worker contract from it, then align the other workers.
   4. [ ] Refine `sql-server`, rewrite the skill contract from it, then align the other plugin skills.
   5. [ ] Review the plugin rules with the pillar questions.
   6. [ ] Align `copilot-customization` by its refresh procedure in `REFERENCES.md`.
   7. [ ] Update `ARCHITECTURE.md`, `README.md`, and `CHANGELOG.md` for moved boundaries and user-visible changes.
2. `planned` Revalidate the package, then run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes; the previous history and tags stay in the verified bundle `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.

## Blockers

- None.
