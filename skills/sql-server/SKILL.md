---
name: sql-server
description: "Use when a task needs data or metadata from a SQL Server database through the Microsoft SQL Server tools. Supplies target resolution, the read-only query gate, and exploration patterns. Not for data or schema changes, deployment, or server administration."
---

# SQL Server read-only queries

Answer a question from the SQL Server target the user named, with read-only queries whose results are either complete or marked as bounded.

## Procedure

1. Resolve the server and the database from the request; a database is optional when the task only lists databases.
   When either is missing or ambiguous, ask the user, or return it to the delegating agent when you run as a subagent.
2. Find the server among the names #tool:ms-mssql.mssql/mssql_list_servers returns, and connect with #tool:ms-mssql.mssql/mssql_connect using that `serverName` and the requested `database`.
   Pass `profileId` only when the user named a saved profile.
   When the server is not listed, report the missing saved connection and stop, because the saved connection holds the credentials.
3. Before the first query, confirm the server and database with #tool:ms-mssql.mssql/mssql_get_connection_details , because the connection can land on the server's default database.
   When the database differs, switch with #tool:ms-mssql.mssql/mssql_change_database and confirm again.
4. Look up only the unknowns that could change the result, such as an object, a column, a view definition, or a join's cardinality, with the matching section of [exploration patterns](references/exploration-patterns.md).
5. Run each statement through #tool:ms-mssql.mssql/mssql_run_query after it passes the [read-only gate](#read-only-gate).
6. Disconnect with #tool:ms-mssql.mssql/mssql_disconnect when the task finishes or stops after a connection exists.

## Read-only gate

#tool:ms-mssql.mssql/mssql_run_query executes any statement, so check each one before sending it.

- Send one query expression built from `SELECT`, optional common table expressions, and set operators such as `UNION ALL`.
- Refuse data or schema changes, `SELECT INTO`, procedure execution, transaction control, temporary objects, `OPENROWSET`, `OPENQUERY`, and multiple statements, and report a request for them as outside this skill.
- Keep the user's server and database for every statement, because access to another source does not make it the one the user meant.

## Bound the result

- Add `TOP 100` for a sample of an unfamiliar object, and leave the bound out when the question needs the full population.
- Before returning rows without `TOP`, count them with an aggregate; when the count is too large to read, aggregate, ask for a narrower population, or bound the query with the user's agreement.
- Treat a result as complete only when its row count matches the expected count, and state whether `TOP` was applied.

## Rules

- Read every object, column, and type from the catalog before relying on it, and read a view's definition before interpreting its filters or joins, because a guessed name or a hidden filter yields a confident wrong answer.
- When SQL Server rejects a statement, report the error instead of changing the query's meaning or target to make it run.
- When a catalog query is denied, use another read-only query that establishes the same fact, or report the fact as unverified.
- Report the server, database, authentication type, and user from the connection details, and never a password, connection string, or token.

## Gotchas

- #tool:ms-mssql.mssql/mssql_run_query requires `queryTypes` and `queryIntent`, which only feed telemetry; classify the statement briefly, such as `["SELECT", "CTE"]` and `data_exploration`.
- Warehouse and enterprise resource planning (ERP) schemas often declare no foreign keys, so report `no declared foreign key` rather than no relationship, and test a join path with the key checks in the exploration patterns.
