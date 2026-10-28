---
name: sql-server
description: "Use when a task needs data or metadata from a SQL Server database through the Microsoft SQL Server tools. Supplies target resolution, the read-only query gate, and the catalog gotchas. Not for data or schema changes, deployment, or server administration."
---

# SQL Server read-only queries

Answer a question from the SQL Server target the user named, with read-only queries whose results are either complete or marked as bounded.
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.

## Procedure

1. Resolve the server and the database from the request; a database is optional when the task only lists databases.
   When either is missing or ambiguous, list the candidate servers and databases and ask the user to choose among them.
2. Connect through the saved connection for that server; when the server has none, report the missing saved connection and stop, because the saved connection holds the credentials.
3. Before the first query, confirm the server and database with #tool:ms-mssql.mssql/mssql_get_connection_details , because the connection can land on the server's default database; when the database differs, switch and confirm again.
4. Run each statement after it passes the read-only gate below.
5. When you connected, disconnect when the task ends.

## Read-only gate

#tool:ms-mssql.mssql/mssql_run_query executes any statement, so check each one before sending it.

- Send one query expression built from `SELECT`, optional common table expressions, and set operators such as `UNION ALL`.
- Refuse anything else, including statements that look like a read but write or reach another source, such as `SELECT INTO`, `OPENROWSET`, and `OPENQUERY`, and report a request for them as outside this skill.
- Keep the server and the databases the user named for every statement, because access to another source does not make it the one the user meant.

## Rules

- Report the server, database, authentication type, and user from the connection details, and never a password, connection string, or token.

## Gotchas

- A column search through the catalog covers only the active database, so repeat it in each database the task spans.
