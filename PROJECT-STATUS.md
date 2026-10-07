# Project Status

- **State:** `active`
- **Updated:** `2026-10-07`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Focus:** Audit the plugin and `.github/` customizations against the pillars before release, fixing only owner-approved findings; the audit scope and batch order come first.

## Roadmap

1. `active` Audit and polish the plugin and `.github/` customizations in batches, with owner-approved findings before each fix.
   1. [ ] Agree on the audit scope, criteria, and batch order; the proposed criteria are the three pillars, the `copilot-customization` review, guidance that holds what its description promises, and explicit precedence between conflicting guidance.
   2. [ ] Batch 1: `copilot-customization`, `build-skill`, `build-worker-agent`, and `build-entry-agent`, including the writing points routed from the pillar interview: references read only in part when chained, leaving out default behavior, examples followed closely, precise triggers, descriptive names, and statements free of dates; and the conflicting rule to give a smaller model exact steps.
   3. [ ] Batch 2: the `.github/instructions/` files and the `.github/skills/` skills.
   4. [ ] Batch 3: the entry agents `software-lead`, `data-lead`, and `discuss`.
   5. [ ] Batches 4 and 5: the nine worker agents, including the missing output format in `database-explorer` and the missing one-checker-round rule in `developer` and `reviewer`.
   6. [ ] Batch 6: `brief-subagent`, `task-context`, `interview-me`, and `run-python`.
   7. [ ] Batch 7: the `redshift` and `sql-server` skills and the three scoped rules.
2. `planned` Clean up stale record statements, `.gitignore`, and the local setup, including `CLAUDE.md`.
3. `planned` Revalidate the package, then run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes; the previous history and tags stay in the verified bundle `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.

## Blockers

- None.
