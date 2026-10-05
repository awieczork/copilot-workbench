---
name: sql-server
description: "Run read-only queries against a user-provided SQL Server target and perform targeted or explicit source exploration through Microsoft SQL Server tools. Use when the user needs a query result, object verification, or data inspection. Do not use for data changes, schema changes, deployment, or server administration."
---

# SQL Server read-only analysis

## Scope

Use this skill for read-only work against the SQL Server target supplied by the user:

- connect to the selected server;
- inspect databases, schemas, tables, views, and functions when the task requires them;
- inspect object definitions, columns, types, keys, and relationships with read-only SQL;
- sample, profile, count, or analyze data with a bounded or complete `SELECT`.

The tool `mssql_run_query` can technically accept statements that change data or schema. This skill authorizes only one read-only `SELECT` or `WITH ... SELECT` statement per call.

The scope is complete when the task stays within read-only SQL Server access and the user-provided target.

## Resolve the target and access

1. Resolve the server and database from the user's prompt or their explicit answer in the current task. A database is not required when the task only lists databases on the selected server.
2. When the server or a required database is missing or ambiguous, ask the user for it before connecting; when running as a subagent, return the missing target to the delegating agent instead of asking directly.
3. Confirm that the SQL Server connection and query tools are available. Stop when the required tool is unavailable.
4. Call #tool:ms-mssql.mssql/mssql_list_servers before #tool:ms-mssql.mssql/mssql_connect and find saved profiles whose returned `server` matches the resolved server.
5. When no profile matches the resolved server, report the missing saved connection and stop. Do not select another server or request credentials in chat.
6. When multiple profiles match, prefer profiles whose default database matches the requested database. When none defaults to that database, retain the server-matching profiles. When multiple profiles still fit, ask the user to select one by profile name and database; subagents return the ambiguity to the delegating agent.
7. Call #tool:ms-mssql.mssql/mssql_connect with the selected `profileId`.
8. Call #tool:ms-mssql.mssql/mssql_get_connection_details after connecting and confirm that the active server matches the resolved server.
9. When the requested database differs from the active database, call #tool:ms-mssql.mssql/mssql_change_database with the active `connectionId` and requested `database`, then verify both the server and database in the new connection details.
10. When the user requests database discovery, call #tool:ms-mssql.mssql/mssql_list_databases on the resolved server and report the result without choosing a database for further queries.
11. When the connection fails or the active target differs from the resolved target after verification, report the failure and stop. Keep the target unchanged across execution and validation.

Report only the server, database, authentication type, and user identifier from connection details. Do not report passwords, connection strings, tokens, or other secrets.

The target step is complete when the active connection matches the user-provided target, or the missing target or failure has been reported.

## Choose the minimum verification

Use the smallest verification level that can establish correctness:

1. When the resolved server, active database, schema-qualified objects, required columns, and SQL are known, execute the statement without broad catalog exploration.
2. When one object, column, view definition, join relationship, bounded sample, profile, distribution, or temporal coverage check is unknown or explicitly requested, read only the corresponding section from [exploration patterns](references/exploration-patterns.md).
3. When a database choice is required, use the result from the target step and do not list databases again.
4. When the object class is unknown, call #tool:ms-mssql.mssql/mssql_list_schemas, #tool:ms-mssql.mssql/mssql_list_tables, #tool:ms-mssql.mssql/mssql_list_views, or #tool:ms-mssql.mssql/mssql_list_functions as the task requires.
5. When the table containing a required column is unknown, read the Column search section in [exploration patterns](references/exploration-patterns.md) before using column metadata discovery.
6. When the user explicitly requests exploration, use the relevant listing tool and targeted catalog query without enumerating unrelated object classes.
7. When a query fails because a specific object or column is unknown, diagnose that item with one targeted check before considering broader exploration.

Do not enumerate databases, schemas, tables, views, functions, or columns solely to reconfirm a complete target and query.

Inspect columns and types before relying on unfamiliar columns. Inspect a view definition before interpreting filters or joins hidden inside that view. Check join cardinality when the relationship is not established by a declared key or supplied evidence.

The verification step is complete when every unknown that could change the result is resolved or reported as a limitation.

## Execute one read-only statement

Before calling #tool:ms-mssql.mssql/mssql_run_query, verify that the submitted text contains exactly one read-only query expression built from `SELECT`, optional common table expressions, and optional set operators such as `UNION ALL`.

Pass the active `connectionId`, the SQL in `query`, `queryTypes` with `SELECT` and any applicable classification such as `JOIN` or `CTE`, and a matching `queryIntent` such as `data_analysis`, `data_exploration`, or `schema_exploration`.

Reject statements containing data or schema mutation, `SELECT INTO`, procedure execution, transaction control, temporary-object creation, external-query execution such as `OPENROWSET` or `OPENQUERY`, or multiple statements. When the user requests such an operation, report that it is outside this skill's read-only scope.

Schema-qualify every table, view, and function reference when the source provides a schema. Use explicit columns instead of `SELECT *`.

For a `WITH` statement, verify that every common table expression closes, commas separate adjacent expressions, and the final statement is a `SELECT`.

Execute one statement per tool call. Run an additional statement only when it performs a named, read-only validation or a targeted discovery step.

The execution step is complete when the tool received one read-only statement with the correct connection and query classification.

## Bound only what needs bounding

Apply `TOP 100` only when the object is unfamiliar or the user requests a bounded sample. Omit the bound when the query is intended to return a complete result.

Before returning non-aggregated rows without `TOP`, establish the expected row count with a read-only aggregate or other supplied evidence. When the expected result is too large to inspect completely in the tool response, return an aggregate, ask the user for a narrower population, or apply an explicit bound with the user's agreement.

Treat a result as complete only when the returned row count matches the expected row count and the tool reports no truncation. Otherwise mark it incomplete.

State whether `TOP` was applied. Treat a bounded result as incomplete for any question that requires the full population.

The bounding step is complete when the result clearly states the bound or its absence.

## Validate and report the result

Read the complete response from #tool:ms-mssql.mssql/mssql_run_query and report the returned columns, row count, and rows relevant to the request.

Report:

- the server and database;
- the request intent and source objects;
- the SQL statement or a reproducible description of the exploration;
- the `TOP` bound or its absence;
- the result, quality checks, and limitations.

Run only applicable checks. Depending on the request, check result grain, duplicate keys, nulls, extreme values, row counts, and temporal coverage. State why a check does not apply.

Read the corresponding section from [exploration patterns](references/exploration-patterns.md) before constructing an additional quality query. Do not perform extra catalog exploration only to decorate the report. Run an additional validation query only when its result can change the interpretation or establish a stated quality check.

Keep observations, conclusions, and hypotheses separate. Do not present co-occurring changes as causes.

When a catalog query is denied, try a read-only fallback that establishes the same fact. When no fallback can establish it, report the verification limit.

The result is complete when the target, SQL, result shape, bound, applicable checks, and limitations are stated.

## Handle failures

- When a required SQL Server tool is unavailable, report the missing capability and stop.
- When no saved target matches the request, report the missing target and stop.
- When authentication or permissions fail, report the failure category without requesting or printing credentials.
- When a database or object is not visible, report the exact missing item and the smallest next discovery step.
- When SQL Server rejects the statement, report the error and do not silently change its meaning or target.
- When a view definition is unavailable, report that filters or joins inside the view could not be verified.
- When no foreign key is declared, report `no declared foreign key`; do not claim that no relationship exists.
- When the result is bounded, truncated, or missing a required check, mark the result incomplete.

Failure handling is complete when the failure category, failed step, effect on the result, and next allowed action are stated.

## Close the session

Call #tool:ms-mssql.mssql/mssql_disconnect with the active `connectionId` when the task finishes or becomes blocked after a connection is established.

The session is complete when the connection is closed or the tool reports that it could not be closed.

## Scope boundary

This skill covers read-only SQL Server access, source discovery, metadata verification, data inspection, and `SELECT` analysis.

It does not cover data or schema changes, deployment, server administration, credential management, or sources outside SQL Server.

Scope handling is complete when the request is supported or its unsupported boundary is reported.
