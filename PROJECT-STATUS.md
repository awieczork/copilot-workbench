# Project Status

- **State:** `active`
- **Updated:** `2026-10-05`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Current:** `develop` holds the validated package with manifest version `0.1.0` on root commit `91f2eff`; `main` holds only the empty root commit `a856fa8`, and nothing is published; before release, the owner requires plugin pillars in the repository instructions, a seven-batch audit of the plugin and `.github/` customizations, and repository hygiene, followed by revalidation and publication; the protection of `.github/instructions/` and `.github/skills/` is withdrawn, while its rule remains in the repository instructions until their rewrite; the Redshift fallback in `database-explorer` is verified statically, without a live Copilot delegation; the previous history and tags are kept in a verified bundle at `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`.
- **Next:** Interview the owner on the plugin pillars, using current external guidance for the latest models, such as the local copy of the GPT-6 family guide at `.github/context/openai-gpt-6-family-model-guide-2026-10-02.md`.

## Roadmap

- `complete` Establish authoring branches and remove obsolete tags while preserving commits and uncommitted work.
- `complete` Make Redshift and SQL Server skills use user-provided targets and keep connection values outside their bundled resources.
- `complete` Consolidate root documentation and rewrite repository instructions for the agreed first-release state.
- `complete` Validate the package and replace the history of `develop` and `main` with new root commits.
- `active` Rewrite the repository instructions and the local `CLAUDE.md` around plugin pillars agreed in an owner interview and grounded in current external guidance for the latest models.
- `planned` Audit and polish the plugin and `.github/` customizations in seven batches, with owner-approved findings before each fix.
- `planned` Clean up stale record statements, `.gitignore`, the local setup, and the structure of the root records and their instructions.
- `planned` Revalidate the package and publish an owner-approved `v0.1.0` snapshot to package-only `main`.
- `paused` Reconsider deferred capability candidates after the first-release work; agree on their priority and write new specifications before implementation.

The following candidates retain only their intended outcomes.
No previous specifications, implementation files, or workspace links are migration inputs.

| Candidate | Intended outcome |
| --- | --- |
| Quarto rule | Define scoped authoring and validation conventions for Quarto documents. |
| R rule | Define scoped conventions for R scripts and project code. |
| Analytical-task skill | Organize one analytical task's durable files and execution record without duplicating temporary task state. |
| Data-contracts skill | Create and maintain explicit contracts for datasets and their expected properties. |
| Mermaid skill | Create and validate diagrams from a newly agreed, bounded diagramming workflow. |
| Reporting skill | Create and maintain analytical reports with traceable evidence and stated limitations. |
| Project-instruction skill | Interview the owner and produce project-specific root instructions; first assess overlap with existing customization skills. |
| Scaffold skill | Initialize a new data-science workspace with optional application modules; define the new scope and templates from scratch. |
| Python MCP server skill | Author, test, and diagnose Python MCP servers for VS Code using documentation for the selected versions. |

## Open Questions

- None identified.

## Planned Tasks

1. [ ] Interview the owner on the plugin pillars, using current external guidance for the latest models, such as the local copy of the GPT-6 family guide at `.github/context/openai-gpt-6-family-model-guide-2026-10-02.md`.
2. [ ] Rewrite `.github/copilot-instructions.md` with the agreed pillars, remove the withdrawn folder-protection rule, link the pillars from [ARCHITECTURE.md](ARCHITECTURE.md) in place of its design-principles sentence, and polish the untracked local `CLAUDE.md`.
3. [ ] Agree on the audit scope with the owner.
4. [ ] Audit batch 1: `copilot-customization`, `build-skill`, `build-worker-agent`, and `build-entry-agent`.
5. [ ] Audit batch 2: the `.github/instructions/` files and the `.github/skills/` skills.
6. [ ] Audit batch 3: the entry agents `software-lead`, `data-lead`, and `discuss`.
7. [ ] Audit batches 4 and 5: the nine worker agents, including the missing output format in `database-explorer`.
8. [ ] Audit batch 6: `brief-subagent`, `task-context`, `interview-me`, and `run-python`.
9. [ ] Audit batch 7: the `redshift` and `sql-server` skills and the three scoped rules.
10. [ ] Agree on and complete the repository hygiene: stale record statements, `.gitignore`, `CLAUDE.md` and the local setup, and the root record structure.
11. [ ] Revalidate the package, run the unchanged publication skill for the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes, and update the project records from the release evidence.
