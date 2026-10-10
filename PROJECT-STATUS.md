# Project status

- **State:** `active`
- **Updated:** `2026-10-10`
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Focus:** The pillar-alignment pass rewrites the agents, skills, and authoring contracts as direction, with `data-lead` as the reference lead, so that the first release ships the new shape.

## Roadmap

1. `active` Align the plugin and its authoring skills with the pillars, by refining one example per component kind, writing it into the contract, and applying the contract to the rest.
   1. [x] Rewrite the skill contract from `sql-server` and `redshift`, then align the other plugin skills.
   2. [x] Review the plugin rules other than `sql` with the pillar questions.
   3. [x] Align `copilot-customization` by its refresh procedure in `REFERENCES.md`.
   4. [ ] Update `ARCHITECTURE.md`, `README.md`, and `CHANGELOG.md` for moved boundaries and user-visible changes.
2. `planned` Revalidate the package, then run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes; the previous history and tags stay in the verified bundle `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.

## Blockers

- None.
