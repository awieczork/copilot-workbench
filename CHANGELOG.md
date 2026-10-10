# Changelog

## Unreleased

### Task ownership

- Added the `software-lead` agent for software changes with bounded delegation and integrated results.
- Added the `data-lead` agent for evidence-backed analysis with explicit uncertainty and user-owned decisions.
- Added the `discuss` agent for clarifying unfinished requests and handing them to a lead or producing a self-contained prompt.

### Exploration and planning

- Added the `explorer` worker for locating workspace evidence for one question.
- Added the `database-explorer` worker for read-only discovery, profiling, and join verification of SQL Server and Redshift objects for one data question, returning drafted queries and the profiling queries it ran.
- Added the `data-explorer` worker for profiling local datasets without changing source files.
- Added the `researcher` worker for sourced external evidence with support, conflicts, and gaps.
- Added the `planner` worker for executable plans for software changes and data analyses, with open decisions returned to the delegating agent.

### Implementation and checking

- Added the `developer` worker for implementing software changes with tests scaled to the cost of an undetected error and reported verification limits.
- Added the `ui-developer` worker for implementing interfaces and visually checking the changed experience.
- Added the `reviewer` worker for independent assessment of finished results without repairing them.
- Added the `challenger` worker for testing one decision or framing with a discriminating check.

### Customization

- Added the `copilot-customization` skill for choosing, writing, and reviewing Copilot project instructions, scoped instructions, custom agents, and Agent Skills for VS Code.

### Coordination

- Added the `brief-subagent` skill for self-contained, one-shot delegated assignments and for acting on the status each subagent returns.
- Added the `task-context` skill for keeping a task's summary and delegated results in a Git-ignored folder, so that a task survives the session and resumes later.
- Added the user-invoked `interview-me` skill for confirming intent before work continues.

### Database and Python workflows

- Added the `redshift` skill for read-only queries against user-provided targets with an MCP-first workflow and a bounded, locally configured Python fallback.
- Added the `sql-server` skill for read-only queries against user-provided targets through verified saved connections.
- Added the `run-python` skill for running Python scripts and inline code through `uv`, with or without the project environment.

### Scoped rules

- Added the `markdown` rule for ordinary document syntax, formatting, and prose.
- Added the `python` rule for user-run task-script conventions and proportionate validation.
- Added the `sql` rule for the text of one read-only SQL Server or Redshift query.
- Added the `changelog` rule for writing and reconciling the `## Unreleased` entries of a project's `CHANGELOG.md`.
- Added the `project-status` rule for keeping a project's `PROJECT-STATUS.md` as a short handoff with its roadmap and blockers.
- Added the `open-issues` rule for recording and closing a project's unresolved decisions, missing inputs, and verified limitations in `OPEN-ISSUES.md`.

### MCP servers

- Added the Redshift MCP server for database queries and catalog discovery using local AWS configuration.
- Added the context7 MCP server for current library documentation.
