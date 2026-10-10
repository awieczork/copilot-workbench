---
name: sql-server
description: "Use when a task needs data or metadata from a SQL Server database through the Microsoft SQL Server tools. Supplies target resolution, the read-only query gate, and the catalog traps. Not for data or schema changes, deployment, or server administration."
---

# SQL Server read-only queries

Answer a question from the SQL Server target the user named, with read-only queries whose results are either complete or marked as bounded.

## Procedure

1. Resolve the server and the database from the request; a database is optional when the task only lists databases.
   When either is missing or ambiguous, ask the user, or return it to the delegating agent when you run as a subagent.
2. Connect through the saved connection for that server; when the server has none, report the missing saved connection and stop, because the saved connection holds the credentials.
3. Before the first query, confirm the server and database with #tool:ms-mssql.mssql/mssql_get_connection_details , because the connection can land on the server's default database; when the database differs, switch and confirm again.
4. Run each statement after it passes the [read-only gate](#read-only-gate).
5. Disconnect when the task finishes or stops after a connection exists.

## Read-only gate

#tool:ms-mssql.mssql/mssql_run_query executes any statement, so check each one before sending it.

- Send one query expression built from `SELECT`, optional common table expressions, and set operators such as `UNION ALL`.
- Refuse anything else, including statements that look like a read but write or reach another source, such as `SELECT INTO`, `OPENROWSET`, and `OPENQUERY`, and report a request for them as outside this skill.
- Keep the user's server and database for every statement, because access to another source does not make it the one the user meant.

## Bound the result

- Add `TOP 100` for a sample of an unfamiliar object, and leave the bound out when the question needs the full population.
- Before returning rows without `TOP`, count them with an aggregate; when the count is too large to read, aggregate, or ask the user for a narrower population, or return the choice to the delegating agent when you run as a subagent.
- Treat a result as complete only when its row count matches the expected count, and state whether `TOP` was applied.

## Rules

- Read every object, column, and type from the catalog before relying on it, and read a view's definition before interpreting its filters or joins, because a guessed name or a hidden filter yields a confident wrong answer.
- Correct a misspelled name from the catalog; when a fix would change what the query means or targets, report the error instead.
- When metadata is denied or unavailable, use another read-only query that establishes the same fact, or report the fact as unverified.
- Report the server, database, authentication type, and user from the connection details, and never a password, connection string, or token.

## Gotchas

- A column search through the catalog covers only the active database, so repeat it in each database the task spans.
- Warehouse and enterprise resource planning (ERP) schemas often declare no foreign keys, so report `no declared foreign key` rather than no relationship, and test a join path with key checks.
