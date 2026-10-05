# Project Status

- **State:** `active`
- **Updated:** `2026-10-05`
- **Owner:** Adam Wieczorkiewicz
- **Objective:** Prepare the first `v0.1.0` release of a private, reusable GitHub Copilot plugin.
- **Current:** `develop` is the authoring branch and tracks `origin/develop`; `main` remains the remote default branch and has not yet been reduced to the distribution payload; obsolete local and remote tags are removed, a verified bundle of the previous history and tags exists at `~/backups/copilot-workbench-pre-v0.1.0-2026-10-05.bundle`, and branch protection is intentionally disabled; the worktree contains 10 plugin skills, 12 agents, three scoped rules, and two Model Context Protocol (MCP) servers; the database skills use user-provided targets and their static checks and isolated runner checks passed, without live database verification; root documentation is consolidated and `docs/` is removed; repository instructions are rewritten with retained owner guidance, current package conventions, and verified root-document links; the open-issues instruction links task state to the `task-context` skill under owner authorization limited to that file; the manifest description no longer claims workspace scaffolding; `database-explorer` loads the database skills and holds a terminal tool and SQL-file scope for the Redshift fallback, verified statically without a live Copilot delegation; the manifest declares `0.1.0`; package validation on the current worktree passed for the manifest and MCP schemas, skill names, agent and rule frontmatter, subagent and skill references, 29 relative links inside the 41-file distribution allowlist, the README inventory, and a scan for machine-specific paths; the owner approved a publication procedure that rewrites `develop` and `main` to new root commits after a history bundle and then runs the unchanged publication skill, pushing through the existing GitHub CLI credential helper; publication has not been performed.
- **Next:** Replace `develop` with one root commit of the current tree and `main` with one empty root commit, then force-push both after owner confirmation.

## Roadmap

- `complete` Establish authoring branches and remove obsolete tags while preserving commits and uncommitted work.
- `complete` Make Redshift and SQL Server skills use user-provided targets and keep connection values outside their bundled resources.
- `complete` Consolidate root documentation and rewrite repository instructions for the agreed first-release state.
- `active` Validate the package, replace the history with new root commits, and publish an owner-approved `v0.1.0` snapshot to package-only `main`.
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

1. [ ] Replace `develop` with one root commit of the current tree and `main` with one empty root commit, then force-push both after owner confirmation.
1. [ ] Run the unchanged publication skill to publish the package-only `main` snapshot, the `v0.1.0` tag, and the GitHub Release with owner-approved notes, then update the project records from verified release evidence.
