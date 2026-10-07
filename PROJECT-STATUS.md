# Project Status

- **State:** `active`
- **Updated:** `2026-10-07`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Focus:** Audit the plugin and `.github/` customizations against the pillars before release, one artifact at a time, measured against the reviewed `copilot-customization`, which is the yardstick for every later batch.

## Roadmap

1. `active` Audit and polish the plugin and `.github/` customizations slowly, taking each batch as a fresh, comprehensive look at its artifacts as a whole: their purpose, fit with the pillars, structure, coherence with each other and the repository instructions, accuracy against primary sources, and fitness for a capable model. Give an overall verdict per batch, then present findings one file at a time, fix only the findings the owner approves, and validate the whole batch before the next one starts.
   1. [ ] Batch 2: `build-skill`, `build-worker-agent`, and `build-entry-agent`, measured also against the reviewed `copilot-customization`, including their required stop rules, retry caps, refusals, per-phase completion conditions, and `Proceeds without asking:` line, which the reviewed agent template makes optional, and whether `build-skill`, which stops when a capability would serve any project, blocks plugin skills in this repository.
   2. [ ] Batch 3: `brief-subagent`, `task-context`, `interview-me`, and `run-python`.
   3. [ ] Batch 4: the `redshift` and `sql-server` skills and the Markdown, Python, and SQL scoped rules.
   4. [ ] Batch 5: the nine worker agents, including the missing output format in `database-explorer` and the missing one-checker-round rule in `developer` and `reviewer`.
   5. [ ] Batch 6: the entry agents `software-lead`, `data-lead`, and `discuss`.
   6. [ ] Batch 7: the `.github/instructions/` files and the `.github/skills/` skills.
2. `planned` Clean up stale record statements, `.gitignore`, and the local setup, including `CLAUDE.md`.
3. `planned` Revalidate the package, then run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes; the previous history and tags stay in the verified bundle `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.

## Blockers

- None.
