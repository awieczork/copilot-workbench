---
name: redshift
description: "Run read-only queries against a user-provided Amazon Redshift target and perform targeted or explicit source exploration. Use the official Redshift MCP tools first and fall back to the bundled Python runner only for tool, transport, authentication, or access failures. Do not use for data changes, cluster administration, credential management, or other database engines."
argument-hint: "Name the Redshift cluster and database, and describe the data to query"
---

# Redshift read-only analysis

## Scope

Use this skill for read-only work against the Amazon Redshift target supplied by the user:

- the selected cluster and database;
- schemas, tables, views, and columns needed by the task;
- bounded or complete `SELECT` statements.

Use the official Redshift Model Context Protocol (MCP) tools as the primary channel. Use the bundled Python runner as the fallback channel only after a failure classified in `Resolve the target and access`.

Both channels can technically accept statements that change data or schema. This skill authorizes only one read-only `SELECT` or `WITH ... SELECT` statement per execution. `EXPLAIN` is also permitted because it returns a plan without changing database state.

The scope is complete when the task stays within read-only access to the user-provided cluster and database.

## Resolve the target and access

1. Resolve the cluster identifier and database name from the user's prompt or their explicit answer in the current task.
2. When either value is missing or ambiguous, ask the user for it before discovery or execution; when running as a subagent, return the missing target to the delegating agent instead of asking directly.
3. Confirm that the required Redshift MCP execution or discovery tool is available. When it is available, select MCP as the active channel.
4. Pass the resolved cluster identifier in `cluster_identifier` to every MCP call. Pass the resolved database name in `schema_database_name` for schema discovery, `table_database_name` for table discovery, `column_database_name` for column discovery, and `database_name` for query execution.
5. Keep the target unchanged across discovery, execution, validation, and fallback. Do not select another target from available resources or a previous task, because access does not identify the user's intended source.
6. Switch to the Python fallback when an MCP tool is unavailable, the MCP server cannot start or communicate, MCP authentication fails, an explicit permission or access denial occurs, or an object is not visible with evidence that access restrictions caused it.
7. Do not switch channels when the user denies tool execution, SQL has a syntax or semantic error, an object is missing without evidence of an access restriction, execution times out or returns `ABORTED`, or a result is bounded or too large.
8. After selecting the Python fallback, keep it as the active channel for the remainder of the task and record the MCP failure category as the fallback reason.

The target step is complete when the user-provided target is resolved and an active channel is selected, or the missing target or failure has been reported.

## Prepare the Python fallback

Run this section only when the Python fallback is the active channel.

1. Check for `.env` at the workspace root. Do not inspect or report its values.
2. When `.env` is absent, report the missing prerequisite and propose creating this blank workspace-root template:

	```dotenv
	REDSHIFT_USER=
	REDSHIFT_PASSWORD=
	REDSHIFT_HOST=
	REDSHIFT_PORT=
	REDSHIFT_DATABASE=
	```

3. Create the blank template only after the user approves that exact action. Tell the user the file is ready to fill, then stop without requesting credentials in chat or running a query.
4. When `.env` exists, ask the user to confirm that its host, port, and database identify the resolved target; require all five variables to be populated locally and do not inspect their values. Create one `.sql` file under `sql/redshift/` at the workspace root for each statement that must run only after that confirmation.
5. First resolve the [query runner](scripts/query_redshift.py) as a resource of this skill and retain the absolute path returned by the client when that path exists.
6. When the client does not return an existing runner path, check `<workspace>/.github/skills/redshift/scripts/query_redshift.py` and use it when the file exists. Do not infer any other workspace or plugin installation path.
7. From the workspace root, quote both paths and run `uv run "<resolved-query-runner-path>" "<workspace-sql-path>"`.
8. Use the active terminal's path syntax. When the resolved runner path uses Windows syntax and the terminal runs in Windows Subsystem for Linux (WSL), convert only that path with `wslpath -u` before invoking `uv`.

When running as a subagent, return a required configuration confirmation to the delegating agent instead of asking directly.

The fallback is prepared when the user has confirmed local configuration for the same target, the SQL file contains one approved read-only statement, and either the skill resource or the classic workspace path resolves to an existing runner that can be invoked from the workspace root.

## Choose the minimum verification

Use the smallest verification level that can establish correctness:

1. When the resolved target, schema-qualified objects, required columns, and SQL are known, execute the statement without broad discovery.
2. When a schema, table, view, column, view definition, join relationship, bounded sample, profile, distribution, or temporal coverage check is unknown or explicitly requested, read only the corresponding section from [exploration patterns](references/exploration-patterns.md).
3. When MCP is active and a schema is unknown, call #tool:awslabs.redshift-mcp-server/list_schemas with the resolved `cluster_identifier` and database name in `schema_database_name`.
4. When MCP is active and a table or view is unknown, call #tool:awslabs.redshift-mcp-server/list_tables with the resolved `cluster_identifier`, database name in `table_database_name`, and selected `table_schema_name`.
5. When MCP is active and a column is unknown or the object is unfamiliar, call #tool:awslabs.redshift-mcp-server/list_columns with the resolved `cluster_identifier`, database name in `column_database_name`, selected `column_schema_name`, and `column_table_name`.
6. When Python is active, use only the targeted catalog query in the corresponding section of [exploration patterns](references/exploration-patterns.md).
7. When the table containing a required column is unknown, read the Column search section in [exploration patterns](references/exploration-patterns.md).
8. When the user explicitly requests exploration, inspect only the schema, object, or column classes named in the request.
9. When a query fails because a specific object or column is unknown, run one discovery call or catalog query limited to that item before considering broader exploration.
10. When join cardinality is not established by supplied evidence, read the relationship section and run a bounded or aggregated read-only check that tests the proposed relationship.

Do not enumerate schemas, tables, views, or columns solely to reconfirm a complete target and query. Report unavailable metadata as a verification limit instead of inferring it.

The verification step is complete when every unknown that could change the result is resolved or reported as a limitation.

## Execute one read-only statement

Before execution, verify that the submitted text contains exactly one read-only query expression built from `SELECT`, optional common table expressions, and optional set operators such as `UNION ALL`, or one `EXPLAIN` of such a query.

Reject statements containing data or schema mutation, `SELECT INTO`, `UNLOAD`, procedure execution, transaction control, temporary-object creation, or multiple statements. When the user requests such an operation, report that it is outside this skill's read-only scope.

Schema-qualify every table and view reference. Use explicit columns instead of `SELECT *`. For a `WITH` statement, verify that every common table expression closes, commas separate adjacent expressions, and the final statement is a `SELECT`.

When MCP is active, call #tool:awslabs.redshift-mcp-server/execute_query with the resolved cluster identifier in `cluster_identifier`, database name in `database_name`, and complete SQL text. When Python is active, follow `Prepare the Python fallback` and read the single JSON object written to standard output.

Execute one statement per call or SQL file. Run an additional statement only when it validates a named condition or discovers the exact missing object or column.

The execution step is complete when the active channel receives one read-only statement for the resolved database.

## Bound only what needs bounding

Apply `LIMIT 100` only when the object is unfamiliar or the user requests a bounded sample. Omit the bound when the query is intended to return a complete result.

Before returning non-aggregated rows without `LIMIT`, establish the expected row count with a read-only aggregate or other supplied evidence. When the expected result is too large to inspect completely, return an aggregate, ask the user for a narrower population, or apply an explicit bound with the user's agreement.

The Python runner returns at most 1,000 rows. Its `row_count` is the number of returned rows, not the total matching row count. When `truncated` is `true`, treat the result as incomplete and revise the query before drawing a conclusion.

Do not infer completeness from the absence of `LIMIT`. Treat a result as complete only when the returned row count matches the expected row count and the active channel reports no truncation or pagination gap.

State whether `LIMIT` was applied. Treat a bounded result as incomplete for any question that requires the full population.

The bounding step is complete when the result clearly states the bound or its absence and any channel output limit.

## Validate and report the result

Read the complete response from the active channel. For MCP, report `query_id`, returned columns, row count, and rows when provided. For Python, report `row_count`, `truncated`, and either the inline rows or the returned CSV path; read the CSV only when `csv_path` is present.

Report:

- the cluster and database;
- the active execution channel and any fallback reason;
- the request intent and source objects;
- the SQL statement or a reproducible description of the exploration;
- the `LIMIT` bound or its absence;
- the result, quality checks, and limitations.

Run only applicable checks. Depending on the request, check result grain, duplicate keys, nulls, extreme values, row counts, and temporal coverage. State why a check does not apply.

Read the corresponding section from [exploration patterns](references/exploration-patterns.md) before constructing an additional quality query. Keep validation filters, population, and target aligned with the result being checked.

Do not perform extra discovery only to decorate the report. Run an additional validation query only when its result can change the interpretation or establish a stated quality check.

Keep observations, conclusions, and hypotheses separate. Do not present co-occurring changes as causes.

The result is complete when the target, active channel, fallback reason if any, SQL, result shape, bound, applicable checks, and limitations are stated.

## Handle failures

- When an MCP failure matches one of the five fallback conditions in `Resolve the target and access`, record its category and continue through `Prepare the Python fallback`.
- When a required `.env` value is absent or `REDSHIFT_PORT` is invalid, report the configuration error without requesting or printing credentials.
- When Redshift rejects the SQL, report the error and do not silently change its meaning or target.
- When a schema, table, view, or column is missing without evidence of access restrictions, report the exact missing item and the smallest next discovery step.
- When execution times out or returns `ABORTED`, report the execution state, mark the result incomplete, and propose narrowing the population, reducing selected columns, or aggregating while preserving the requested metric.
- When metadata is unavailable, report the verification limit before interpreting the result.
- When the result is bounded, truncated, or missing a required check, mark the result incomplete.

For Python runner failures, exit code `2` identifies SQL input failure, exit code `3` identifies configuration or connection failure, and exit code `4` identifies query execution failure.

Failure handling is complete when the failure category, failed step, effect on the result, active channel, and next allowed action are stated.

## Scope boundary

This skill covers read-only Amazon Redshift access, source discovery, metadata verification, data inspection, and `SELECT` analysis.

It does not cover data or schema changes, cluster administration, credential management, deployment, or sources outside Amazon Redshift.

Scope handling is complete when the request is supported or its unsupported boundary is reported.
