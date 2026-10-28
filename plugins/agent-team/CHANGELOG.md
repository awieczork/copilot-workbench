# Changelog

## Unreleased

### Removed

- The `agent-team` package excludes `copilot-customization`; the separate `agent-plugin-dev` package supplies the skill.

## [0.1.3] - 2026-10-16

### Added

- **Continue a discussion in another session.** Invoke `seed-task` to turn the part of a conversation you choose into a task you can start separately. You confirm what it carries, then receive a start prompt so the next session has the context it needs.

### Changed

- **Use one lead for workspace changes.** Select `lead`, which replaces `software-lead`, for code, documentation, configuration, or a change that needs data evidence. It coordinates specialists, runs independent work in parallel, and checks that the parts work together before delivering the result.
- **Resume planned work after an interruption.** When `lead` or `data-lead` uses a plan, it saves the accepted plan with its amendments and completed tasks. A resumed session follows that current plan rather than reconstructing progress from the conversation.
- **See what supports a data answer.** Use `data-lead` for work that uses or depends on data. Analysis results include row counts, filter checks, and coverage; before an analysis supports a decision, the lead also checks its framing and has key figures recomputed independently.
- **Develop an idea and its documentation in one discussion.** Ask `discuss` to investigate an idea, create or edit documentation, and shape a request for a lead. Use `seed-task` when you want to carry the discussion into a new session instead of continuing through a handoff.
- **Review a draft before settling customization choices.** When the scope or type of an agent customization is unclear, `copilot-customization` shows proposed content before asking you to choose, so the decision rests on a concrete draft.
- **Use the Redshift fallback without confirming its target by hand.** The fallback reports the host and database it used, and results from another target are rejected. Scripts that call the runner must handle exit status `1` for input, connection, and query errors instead of the former separate error codes.

## [0.1.2] - 2026-10-15

### Fixed

- The plugin uses the Copilot plugin format for agent discovery in Copilot (Agent Host) sessions and agent and rule discovery in the Agent Customizations editor.

## [0.1.1] - 2026-10-15

### Added

- The `awieczork-tools` marketplace provides installation and updates for `copilot-workbench` through VS Code's `/plugin` commands.
- The README explains how to set `CONTEXT7_API_KEY` in the MCP server's environment for authenticated Context7 access.

### Changed

- The documented VS Code setup uses the Copilot harness in Agent Host.

## [0.1.0] - 2026-10-10

### Added

- The `software-lead` agent delivers or plans software changes by deciding the approach, briefing workers, and judging their results.
- The `data-lead` agent answers data-science questions with evidence, explicit uncertainty, and decisions left to the user.
- The `discuss` agent shapes an unfinished idea into a request for a lead or a self-contained prompt for a new session.
- The `explorer` worker locates workspace evidence for one question.
- The `database-explorer` worker discovers and profiles SQL Server and Redshift objects for one data question, verifies join paths, and returns read-only queries.
- The `data-explorer` worker profiles local datasets, their joins, and their splits without changing source files.
- The `researcher` worker gathers sourced external evidence with its support, conflicts, and gaps.
- The `planner` worker produces executable plans for software changes and data analyses, and returns open decisions to the delegating agent.
- The `developer` worker implements software changes with tests scaled to the cost of an undetected error.
- The `ui-developer` worker implements interface changes and checks them in the running app in a browser.
- The `reviewer` worker assesses finished results against their goal without repairing them.
- The `challenger` worker tests one decision or framing and recommends whether to proceed, revise, or reject it.
- The `copilot-customization` skill guides choosing, writing, and reviewing Copilot project instructions, scoped instructions, custom agents, and Agent Skills for VS Code.
- The `brief-subagent` skill supplies self-contained, one-shot briefs and how to act on the status each worker returns.
- The `task-context` skill keeps a task's summary and delegated results in a Git-ignored folder, so that a task survives the session and resumes later.
- The user-invoked `interview-me` skill confirms the user's intent before work continues.
- The `redshift` skill runs read-only queries against user-provided targets with an MCP-first workflow and a Python fallback that returns at most 100 rows.
- The `sql-server` skill runs read-only queries against user-provided targets through verified saved connections.
- The `run-python` skill runs Python scripts and inline code through `uv`, with or without the project environment.
- The `markdown` rule supplies document syntax, formatting, and prose rules, and only its syntax rules for customization files.
- The `python` rule supplies conventions for user-run task scripts with proportionate validation.
- The `sql` rule supplies schema reading, result bounding, and query text rules for read-only SQL Server and Redshift queries.
- The `changelog` rule keeps a project's `CHANGELOG.md` in Keep a Changelog sections.
- The `project-status` rule keeps a project's `PROJECT-STATUS.md` as a short handoff with its roadmap and blockers.
- The `open-issues` rule records and closes a project's unresolved decisions, missing inputs, and verified limitations in `OPEN-ISSUES.md`.
- The Redshift MCP server runs database queries and catalog discovery with local AWS configuration.
- The context7 MCP server provides current library documentation.
