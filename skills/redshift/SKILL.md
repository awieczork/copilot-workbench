---
name: redshift
description: "Use when a task needs data or metadata from an Amazon Redshift database. Supplies target resolution, the read-only query gate, the MCP tools with a Python fallback, and the catalog gotchas. Not for data or schema changes, cluster administration, or other database engines."
---

# Redshift read-only queries

Answer a question from the Amazon Redshift target the user named, with read-only queries whose results are either complete or marked as bounded.
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.

## Procedure

1. Resolve the cluster identifier and the database from the request.
   When either is missing or ambiguous, ask the user.
2. Use the Redshift MCP tools, and switch to the Python fallback below only when MCP cannot reach the cluster, because the fallback changes only the access path and fixes no query error; a user's denial of a tool call and a timeout are not access failures, so keep MCP for them.
   Once the fallback is active, keep it for the rest of the task and report the MCP failure that caused the switch.
3. Run each statement after it passes the read-only gate below.

## Read-only gate

Check each statement before sending it, because the fallback runner executes what it receives.

- Send one query expression built from `SELECT`, optional common table expressions, and set operators such as `UNION ALL`, or one `EXPLAIN` of such a query.
- Refuse anything else, including statements that look like a read but write, such as `SELECT INTO`, and report a request for them as outside this skill.
- Keep the user's cluster and database for every statement and across a channel switch, because access to another source does not make it the one the user meant.

## Python fallback

1. Run the fallback only after the user confirms that the host, port, and database in `.env` identify the resolved target, because the file can point to another cluster; as a subagent, run it only when the brief states that confirmation, and otherwise return `Decision needed`.
2. Run [the runner](scripts/query_redshift.py), located in this skill's folder, as a script by the `run-python` skill with the workspace root as the working directory, and pipe the statement on standard input.
3. Read the one JSON object it prints: it holds `rows`, or `csv_path` for a result over 100 rows.
   When the runner fails, read the reason on standard error.

## Bound the result

- Add `LIMIT 100` for a sample of an unfamiliar object, and leave the bound out when the question needs the full population.
- Before returning rows without `LIMIT`, count them with an aggregate; when the count is too large to read, aggregate, or ask the user for a narrower population.
- Treat a result as complete only when its row count matches the expected count and the channel reports no truncation, and state whether `LIMIT` was applied; the runner's `row_count` counts only the returned rows, so `truncated: true` means the result is incomplete.

## Rules

- Read every object, column, and type from the catalog before relying on it, and read a view's definition before interpreting its filters or joins, because a guessed name or a hidden filter yields a confident wrong answer.
- Correct a misspelled name from the catalog; when a fix would change what the query means or targets, report the error instead.
- When metadata is denied or unavailable, use another read-only query that establishes the same fact, or report the fact as unverified.
- Never request, read, or print credentials, and report a configuration error by the variable name only.

## Gotchas

- `svv_all_tables` lists the views and the base, external, and shared tables the user can access, while `information_schema.columns` misses external and shared objects, so zero rows there does not prove a column is absent.
- When `svv_columns` is denied, query `svv_redshift_columns`, which names the schema `schema_name` and lacks length, precision, and scale.
- `pg_catalog.pg_views` covers only standard views, so read a materialized, external, or shared view's definition from the catalog that holds it, or report its filters and joins as unverified.
- Redshift constraints are informational and often absent, so report `no declared constraint` rather than no relationship, and test a join path with key checks.
