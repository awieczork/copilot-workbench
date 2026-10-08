---
name: redshift
description: "Use when a task needs data or metadata from an Amazon Redshift database. Supplies target resolution, the read-only query gate, the MCP tools with a Python fallback, and exploration patterns. Not for data or schema changes, cluster administration, or other database engines."
argument-hint: "Name the Redshift cluster and database, and describe the data to query"
---

# Redshift read-only queries

Answer a question from the Amazon Redshift target the user named, with read-only queries whose results are either complete or marked as bounded.

## Procedure

1. Resolve the cluster identifier and the database from the request.
   When either is missing or ambiguous, ask the user, or return it to the delegating agent when you run as a subagent.
2. Use the Redshift MCP tools as the channel, and switch to the [Python fallback](#python-fallback) only when an MCP tool is unavailable, the server cannot start or connect, authentication fails, or access is denied.
   Keep MCP for a user's denial of a tool call, a SQL error, a missing object, a timeout or `ABORTED` state, and a large result, because the fallback cannot fix any of them.
   Once the fallback is active, keep it for the rest of the task and report the MCP failure that caused the switch.
3. Look up only the unknowns that could change the result, such as an object, a column, a view definition, or a join's cardinality, with the matching section of [exploration patterns](references/exploration-patterns.md).
4. Run each statement after it passes the [read-only gate](#read-only-gate).

## Read-only gate

Check each statement before sending it, because the fallback runner executes what it receives.

- Send one query expression built from `SELECT`, optional common table expressions, and set operators such as `UNION ALL`, or one `EXPLAIN` of such a query.
- Refuse data or schema changes, `SELECT INTO`, `UNLOAD`, procedure execution, transaction control, temporary objects, and multiple statements, and report a request for them as outside this skill.
- Keep the user's cluster and database for every statement and across a channel switch, because access to another source does not make it the one the user meant.

## Python fallback

1. Check that `.env` exists at the workspace root without reading its values, because it holds the user's credentials.
   When it is missing, report that the fallback needs `REDSHIFT_USER`, `REDSHIFT_PASSWORD`, `REDSHIFT_HOST`, `REDSHIFT_PORT`, and `REDSHIFT_DATABASE` there, and stop.
2. Ask the user to confirm that the host, port, and database in `.env` identify the resolved target, or return the confirmation to the delegating agent when you run as a subagent, because the file can point to another cluster.
3. Run [the runner](scripts/query_redshift.py) from this skill's folder as a script by the `run-python` skill, from the workspace root, and pipe the statement on standard input in the active shell's syntax.
4. Read the one JSON object it prints: `columns`, `row_count`, `truncated`, and either `rows` or the absolute `csv_path` of a result over 100 rows in the system temporary directory.

The runner exits with `2` for invalid input, `3` for missing configuration or a failed connection, and `4` for a failed query, and writes the reason to standard error without credentials.

## Bound the result

- Add `LIMIT 100` for a sample of an unfamiliar object, and leave the bound out when the question needs the full population.
- Before returning rows without `LIMIT`, count them with an aggregate; when the count is too large to read, aggregate, ask for a narrower population, or bound the query with the user's agreement.
- Treat a result as complete only when its row count matches the expected count and the channel reports no truncation, and state whether `LIMIT` was applied.

## Rules

- Read every object, column, and type from the catalog before relying on it, and read a view's definition before interpreting its filters or joins, because a guessed name or a hidden filter yields a confident wrong answer.
- When Redshift rejects a statement, report the error instead of changing the query's meaning or target to make it run.
- Report unavailable metadata as unverified instead of inferring it.
- Never request, read, or print credentials, and report a configuration error by the variable name only.

## Gotchas

- Every MCP call takes `cluster_identifier`, but the database parameter is named per tool: `schema_database_name` for #tool:awslabs.redshift-mcp-server/list_schemas , `table_database_name` for #tool:awslabs.redshift-mcp-server/list_tables , `column_database_name` for #tool:awslabs.redshift-mcp-server/list_columns , and `database_name` for #tool:awslabs.redshift-mcp-server/execute_query .
- #tool:awslabs.redshift-mcp-server/execute_query itself rejects writes and multiple statements, while the fallback runner does not.
- The runner returns at most 1,000 rows, and its `row_count` counts the returned rows, not every matching row; treat `truncated: true` as an incomplete result and revise the query.
- When this skill's path is a Windows path and the terminal runs in Windows Subsystem for Linux (WSL), convert the runner path with `wslpath -u` before running it.
- Windows PowerShell 5.1 replaces non-ASCII characters in piped text with `?`, so set `$OutputEncoding = [System.Text.UTF8Encoding]::new()` before piping a statement that contains them.
- Redshift constraints are informational and often absent, so report `no declared constraint` rather than no relationship, and test a join path with the key checks in the exploration patterns.
