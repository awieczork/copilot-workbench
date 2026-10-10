---
name: redshift
description: "Use when a task needs data or metadata from an Amazon Redshift database. Supplies target resolution, the read-only query gate, the MCP tools with a Python fallback, and the catalog gotchas. Not for data or schema changes, cluster administration, or other database engines."
---

# Redshift read-only queries

Answer a question from the Amazon Redshift target the user named, with read-only queries whose results are either complete or marked as bounded.
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.

## Procedure

1. Resolve the cluster identifier and the database from the request, and check them with the MCP cluster and database listings.
   When either is missing or ambiguous, list the candidates and ask the user to choose among them.
2. Use the Redshift MCP tools.
   Switch to the Python fallback below only when MCP cannot reach the cluster, because the fallback changes only the access path and fixes no query error; a denied tool call or a timeout is not an access failure.
   Report the MCP failure that caused the switch.
3. Run each statement after it passes the read-only gate below.

## Read-only gate

Check each statement before sending it, because the fallback runner executes what it receives.

- Send one query expression built from `SELECT`, optional common table expressions, and set operators such as `UNION ALL`, or one `EXPLAIN` of such a query.
- Refuse anything else, including statements that look like a read but write, such as `SELECT INTO`, and report a request for them as outside this skill.
- Keep the user's cluster and database for every statement and across a switch of access path, because access to another source does not make it the one the user meant.

## Python fallback

1. Run the fallback only after the user confirms that `.env` points to the resolved cluster and database, because the file can point to another cluster; ask without reading the file, because it holds the password; as a subagent, run it only when the brief states that confirmation, and otherwise return `Decision needed`.
2. Run [the runner](scripts/query_redshift.py), located in this skill's folder, as a script by the `run-python` skill with the workspace root as the working directory, and pipe the statement on standard input.
3. Read the one JSON object it prints: `columns`, `rows` (at most 100), `row_count`, and `truncated`, which is `true` when more rows exist.
   When the runner fails, read the reason on standard error.

## Rules

- Never request, read, or print credentials, and report a configuration error by the variable name only.

## Gotchas

- Discover objects and columns with the MCP listing tools, or in the fallback with `svv_all_tables` and `svv_all_columns`, because they cover local, external, and shared objects.
- When `svv_columns` is denied, query `svv_redshift_columns`, which names the schema `schema_name` and lacks length, precision, and scale.
