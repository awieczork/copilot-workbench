# Changelog

## Unreleased

### Added

- The `seed-task` skill turns the current conversation, such as a forked discussion, into a task folder that an independent session starts from; only the user invokes it.

### Changed

- The Redshift fallback runner reports its connected host and database so the `redshift` skill can discard results from another target without prior user confirmation.
- The Redshift fallback runner uses exit status `1` for input, connection, and query errors.
- The `redshift` skill uses `svv_redshift_columns` when access to `svv_all_columns` is denied.
- The `copilot-customization` skill drafts content before asking the user to settle an unresolved artifact scope or type.
- The `changelog` rule reconciles all changes since the release baseline when the request names no paths.
- The `sql` rule requires a row count before returning unbounded results without a fixed 100-row threshold.
- The `discuss` agent creates and edits the documentation the user asks for.
- The `discuss` agent returns a shaped request for a lead and leaves the start of a new session to the `seed-task` skill.
- The `lead` and `data-lead` agents keep every plan from `planner` in the task folder and keep it current with amendments and finished tasks, so that work resumes from the plan after an interruption.
- The `lead` agent, formerly `software-lead`, takes any work in the workspace.
- The `lead` agent briefs the `database-explorer` and `data-explorer` workers for the data facts a change depends on.
- The `lead` and `data-lead` agents split a task into parts for workers and run the independent parts in parallel, keeping the decisions, the integration, and the conclusion.
- The `discuss` agent gathers workspace and external evidence through workers that run in parallel.
- The `developer` worker implements configuration and documentation changes as well as code changes.
- The `planner` worker splits a plan into tasks with separate files or questions, so that tasks without a dependency run in parallel.
- The `data-lead` agent takes all work that touches or rests on data and has workers run the queries.
- The `data-lead` agent accepts a query result only when its row counts and coverage support it.
- The `data-lead` agent challenges the framing of a result that supports a decision first and has its key figures recomputed independently.
- The `database-explorer` and `data-explorer` workers run the analyses a brief specifies and return each result with its row counts in and out, a filter-value check, and its coverage.
- The `developer` and `ui-developer` workers write a test only when the brief asks for one.
- The `developer`, `ui-developer`, and `planner` workers run a review only when the brief requires one.
- The `lead` and `data-lead` agents rerun each part's key check and one check across the parts instead of a producer's whole suite.

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
