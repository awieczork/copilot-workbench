# Redshift exploration patterns

Use sections 1-4 for targeted discovery or verification of unknown source details. Do not use those discovery patterns when the supplied SQL already identifies every required object and column. Read sections 5-8 when the task explicitly requests a sample or a quality check. Replace schema, table, column, and view placeholders with exact names.

Execute each SQL pattern through the active channel selected in [the Redshift workflow](../SKILL.md). When MCP is active, pass the user-provided cluster identifier in `cluster_identifier` and database name in `database_name`. When Python is active, place one pattern in one workspace SQL file and run the bundled runner against the same confirmed target as defined by the workflow.

---

## 1. Relationship discovery

Inspect relationships when a join path or cardinality is unknown. Start with declared or informational constraints, then verify an undeclared relationship with key uniqueness and row-count checks.

### Declared constraints on one table

Execute this read-only query after replacing the placeholders:

```sql
SELECT
    table_schema,
    constraint_name,
    table_name,
    constraint_type
FROM information_schema.table_constraints
WHERE table_schema = 'schema_name'
    AND table_name = 'table_name'
ORDER BY constraint_type, constraint_name;
```

This query lists constraints declared on the requested table. It does not reveal inbound references from other tables. Redshift constraints can be informational and may be absent. No returned constraint means that the relationship is not declared, not that no relationship exists.

Relationship discovery is complete when constraints declared on the requested table are reported or no declared constraint is found. Inbound references remain unverified unless a separate supported catalog query establishes them.

### Join-key uniqueness check

Before joining on a candidate key, confirm which side is unique. Replace the placeholders with the exact schema and table names:

```sql
SELECT
    source_table.CandidateKey,
    COUNT(*) AS DuplicateCount
FROM schema_name.table_name AS source_table
GROUP BY source_table.CandidateKey
HAVING COUNT(*) > 1
ORDER BY DuplicateCount DESC
LIMIT 20;
```

Zero rows means the key has no duplicate values in the checked population. Any row means the join can multiply rows; state the expected cardinality and check the joined row count.

Join-key verification is complete when uniqueness status, expected cardinality, and any row multiplication are reported.

Relationship analysis is complete when every requested join path has a declared constraint or a tested cardinality, or the limitation is reported.

---

## 2. Exact object and column discovery

Use the MCP listing tools while MCP is active. Use the catalog queries while Python is active.

### Find one known schema

Call #tool:awslabs.redshift-mcp-server/list_schemas with the resolved cluster identifier in `cluster_identifier` and database name in `schema_database_name`. Identify the requested schema from the returned result.

When Python is active, execute this targeted query instead:

```sql
SELECT
    schema_name
FROM svv_all_schemas
WHERE schema_name = 'schema_name';
```

Schema discovery is complete when the requested schema is identified or no matching schema is reported.

### Find one known table or view

Call #tool:awslabs.redshift-mcp-server/list_tables with the resolved cluster identifier in `cluster_identifier`, database name in `table_database_name`, and exact `table_schema_name`. Identify the requested table or view from the returned result.

When Python is active, execute this targeted query instead:

```sql
SELECT
    all_tables.schema_name,
    all_tables.table_name,
    all_tables.table_type
FROM svv_all_tables AS all_tables
WHERE all_tables.schema_name = 'schema_name'
    AND all_tables.table_name LIKE '%object_name%'
ORDER BY all_tables.schema_name, all_tables.table_name
LIMIT 100;
```

`svv_all_tables` covers visible local and external objects. If the query returns 100 rows, narrow the object pattern before treating the result as complete.

Object discovery is complete when one intended object is identified, or no matching object is reported.

### Inspect columns for one object

Call #tool:awslabs.redshift-mcp-server/list_columns with the resolved cluster identifier in `cluster_identifier`, database name in `column_database_name`, exact `column_schema_name`, and `column_table_name`. Inspect every column used by the planned query.

When Python is active, execute this targeted query instead:

```sql
SELECT
    columns.ordinal_position,
    columns.column_name,
    columns.data_type,
    columns.character_maximum_length,
    columns.numeric_precision,
    columns.numeric_scale,
    columns.is_nullable
FROM svv_columns AS columns
WHERE columns.table_schema = 'schema_name'
    AND columns.table_name = 'table_name'
ORDER BY columns.ordinal_position;
```

When `svv_columns` is denied, use `svv_redshift_columns` for local tables and report that external-column coverage is unavailable.

Column inspection is complete when every required column is returned with its available type and nullability metadata, or the missing metadata is reported.

---

## 3. View definition inspection

Redshift view logic can contain filters and joins that affect the requested result. Read the definition when those hidden expressions could change interpretation.

Execute this read-only query after replacing the placeholders:

```sql
SELECT
    schemaname,
    viewname,
    definition
FROM pg_catalog.pg_views
WHERE schemaname = 'schema_name'
    AND viewname = 'view_name';
```

Inspection is complete when the definition is available or its unavailability is reported before interpretation.

`pg_catalog.pg_views` covers standard views visible to the session. When the object may be a materialized, external, shared, or otherwise separately cataloged view, use a catalog source available for that object and report the coverage limit before interpretation.

---

## 4. Column search

Search the catalog when the table containing a required column is unknown. Use a narrow pattern instead of enumerating every column. When the schema is known, add the schema predicate shown in the text below; when it is unknown, omit that predicate:

```sql
SELECT
    table_schema,
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE column_name ILIKE '%search_pattern%'
ORDER BY table_schema, table_name, column_name
LIMIT 100;
```

When the schema is known, add `AND table_schema = 'schema_name'` to the `WHERE` clause.

This search covers objects exposed through `information_schema.columns`. If the target can contain external, shared, or otherwise separately cataloged objects, report the catalog coverage limit and use an available catalog source for those objects instead of treating zero rows as proof that the column is absent.

The query is bounded at 100 rows. If it returns 100 rows, report the search as potentially incomplete and narrow the pattern or remove the bound only when a complete search is required.

Search is complete when all matching candidates are reported within the bound, or the bound is reached and the search is marked potentially incomplete with its next action.

---

## 5. Data sampling

### Recent rows with explicit columns

Use a bounded sample for an unfamiliar object or when the user requests a quick look:

```sql
SELECT
    source_table.Column1,
    source_table.Column2,
    source_table.CreatedDate
FROM schema_name.table_name AS source_table
ORDER BY source_table.CreatedDate DESC
LIMIT 100;
```

Sampling is complete when the bound and ordering are stated and the sample is labeled as non-complete.

---

## 6. Data profiling

### NULL density and distinct count for one column

```sql
SELECT
    COUNT(*) AS TotalRows,
    COUNT(source_table.ColumnName) AS NonNullCount,
    COUNT(*) - COUNT(source_table.ColumnName) AS NullCount,
    100.0 * (COUNT(*) - COUNT(source_table.ColumnName))
        / NULLIF(COUNT(*), 0) AS NullPercent,
    COUNT(DISTINCT source_table.ColumnName) AS DistinctCount
FROM schema_name.table_name AS source_table;
```

### Numeric column statistics

```sql
SELECT
    COUNT(*) AS TotalRows,
    COUNT(source_table.NumericColumn) AS NonNullCount,
    MIN(source_table.NumericColumn) AS MinValue,
    MAX(source_table.NumericColumn) AS MaxValue,
    AVG(CAST(source_table.NumericColumn AS DOUBLE PRECISION)) AS AvgValue
FROM schema_name.table_name AS source_table;
```

### Multi-column profile summary

```sql
SELECT
    'ColumnA' AS ColumnName,
    COUNT(*) AS TotalRows,
    COUNT(source_table.ColumnA) AS NonNullCount,
    COUNT(DISTINCT source_table.ColumnA) AS DistinctCount
FROM schema_name.table_name AS source_table
UNION ALL
SELECT
    'ColumnB' AS ColumnName,
    COUNT(*) AS TotalRows,
    COUNT(source_table.ColumnB) AS NonNullCount,
    COUNT(DISTINCT source_table.ColumnB) AS DistinctCount
FROM schema_name.table_name AS source_table;
```

Profile only the columns that can change the interpretation. A separate query for each profile can scan the source again.

Profiling is complete when every requested column has the applicable statistics and scan limitations are reported.

---

## 7. Value distributions

### Top-N frequency for a categorical column

```sql
SELECT
    source_table.CategoryColumn,
    COUNT(*) AS Frequency,
    100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER (), 0) AS Pct
FROM schema_name.table_name AS source_table
GROUP BY source_table.CategoryColumn
ORDER BY Frequency DESC
LIMIT 20;
```

A NULL value appears as its own group when present. Its frequency is a data-quality finding.

Distribution profiling is complete when the requested category values, frequencies, and NULL handling are reported.

---

## 8. Temporal coverage

### Date range of a table

```sql
SELECT
    MIN(source_table.EventDate) AS EarliestDate,
    MAX(source_table.EventDate) AS LatestDate,
    COUNT(*) AS TotalRows
FROM schema_name.table_name AS source_table;
```

### Rows per month

Run the date-range query first. Use the monthly query below as a recent 60-month inspection and report that bound. Remove `LIMIT 60` only when complete monthly coverage is required and the date range establishes that the output remains practical to inspect.

```sql
SELECT
    DATE_TRUNC('month', source_table.EventDate) AS MonthStart,
    COUNT(*) AS RowsInMonth
FROM schema_name.table_name AS source_table
GROUP BY DATE_TRUNC('month', source_table.EventDate)
ORDER BY MonthStart DESC
LIMIT 60;
```

A missing month or sudden volume drop within the inspected range is a finding to report, not an artifact to skip.

Temporal inspection is complete when the observed date range, the 60-month bound or its absence, expected period coverage, and missing or sparse periods within the inspected range are reported.
