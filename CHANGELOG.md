# Changelog

## Unreleased

### Task ownership

- Added the `software-lead` agent for software changes with bounded delegation and integrated results.
- Added the `data-lead` agent for evidence-backed analysis with explicit uncertainty and user-owned decisions.
- Added the `discuss` agent for clarifying unfinished requests and handing them to a lead or producing a self-contained prompt.

### Exploration and planning

- Added the `explorer` worker for locating workspace evidence for one question.
- Added the `database-explorer` worker for read-only object discovery, data profiling, join verification, and query drafting, including the Redshift Python fallback.
- Added the `data-explorer` worker for profiling local datasets without changing source files.
- Added the `researcher` worker for sourced external evidence with support, conflicts, and gaps.
- Added the `planner` worker for executable plans with explicit scope and unresolved decisions.

### Implementation and checking

- Added the `developer` worker for implementing software changes with focused tests and reported verification limits.
- Added the `ui-developer` worker for implementing interfaces and visually checking the changed experience.
- Added the `reviewer` worker for independent assessment of finished results without repairing them.
- Added the `challenger` worker for testing one decision or framing with a discriminating check.

### Customization

- Added the `copilot-customization` skill for writing and reviewing portable Copilot instructions, agents, and skills.

### Coordination

- Added the `brief-subagent` skill for self-contained, one-shot delegated assignments.
- Added the `task-context` skill for temporary task summaries and delegated results shared across agents and sessions.
- Added the user-invoked `interview-me` skill for confirming intent before work continues.

### Database and Python workflows

- Added the `redshift` skill for read-only queries against user-provided targets with an MCP-first workflow and a bounded, locally configured Python fallback.
- Added the `sql-server` skill for read-only queries against user-provided targets through verified saved connections.
- Added the `run-python` skill for Python execution through `uv` in project or no-project mode.

### Scoped rules

- Added the `markdown` rule for ordinary document syntax, formatting, and prose.
- Added the `python` rule for user-run task-script conventions and proportionate validation.
- Added the `sql` rule for the text of one read-only SQL Server or Redshift query.

### MCP servers

- Added the Redshift MCP server for database queries and catalog discovery using local AWS configuration.
- Added the context7 MCP server for current library documentation.
