# Project Status

- **State:** `active`
- **Updated:** `2026-10-07`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Focus:** Audit the plugin and `.github/` customizations against the pillars before release, one artifact at a time, starting with `copilot-customization` because it is the yardstick for every later batch.

## Roadmap

1. `active` Audit and polish the plugin and `.github/` customizations slowly, one artifact at a time: present each artifact's findings on their own, fix only the findings the owner approves, and validate the artifact before the next one starts. The criteria are the three pillars, the `copilot-customization` review, guidance that holds what its description promises, and explicit precedence between conflicting guidance.
   1. [ ] Batch 1: `copilot-customization`, including the writing points routed from the pillar interview: references read only in part when chained, leaving out default behavior, examples followed closely, precise triggers, descriptive names, and statements free of dates; and the conflicting rule to give a smaller model exact steps.
   2. [ ] Batch 2: `build-skill`, `build-worker-agent`, and `build-entry-agent`, measured also against the reviewed `copilot-customization`, including whether `build-skill`, which stops when a capability would serve any project, blocks plugin skills in this repository.
   3. [ ] Batch 3: `brief-subagent`, `task-context`, `interview-me`, and `run-python`.
   4. [ ] Batch 4: the `redshift` and `sql-server` skills and the Markdown, Python, and SQL scoped rules.
   5. [ ] Batch 5: the nine worker agents, including the missing output format in `database-explorer` and the missing one-checker-round rule in `developer` and `reviewer`.
   6. [ ] Batch 6: the entry agents `software-lead`, `data-lead`, and `discuss`.
   7. [ ] Batch 7: the `.github/instructions/` files and the `.github/skills/` skills.
2. `planned` Clean up stale record statements, `.gitignore`, and the local setup, including `CLAUDE.md`.
3. `planned` Revalidate the package, then run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes; the previous history and tags stay in the verified bundle `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.

## Blockers

- None.
