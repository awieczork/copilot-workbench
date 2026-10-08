# Redshift exploration patterns

Read only the section for the unknown item or the requested check.
Run each pattern through the read-only gate of the [Redshift skill](../SKILL.md) on the active channel, and replace the schema, table, view, and column placeholders with exact names.

## 1. Relationships

### Declared constraints on one table

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

The query lists constraints declared on this table only, not references from other tables.

### Join-key uniqueness

Check which side of a join is unique, because a duplicated key fans out the join and inflates every aggregate after it.

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

Zero rows means no duplicate key in the checked population.
Any row means the join can multiply rows, so state the expected cardinality and check the joined row count.

### Unmatched keys

Count the child rows whose key finds no parent, because an `INNER JOIN` drops them without a signal.
Run it after the uniqueness check confirms the parent key is unique, because a duplicated parent key inflates `ChildRows`.

```sql
SELECT
    COUNT(*) AS ChildRows,
    SUM(CASE WHEN parent_table.ParentKey IS NULL THEN 1 ELSE 0 END) AS UnmatchedRows
FROM schema_name.child_table AS child_table
LEFT JOIN schema_name.parent_table AS parent_table
    ON child_table.ParentKey = parent_table.ParentKey;
```

Rows with a NULL child key count as unmatched.

## 2. Schemas, objects, and columns

On MCP, use #tool:awslabs.redshift-mcp-server/list_schemas , #tool:awslabs.redshift-mcp-server/list_tables , and #tool:awslabs.redshift-mcp-server/list_columns ; on the fallback, use the catalog queries below.

### One named schema

```sql
SELECT
    schema_name
FROM svv_all_schemas
WHERE schema_name = 'schema_name';
```

### Tables and views matching a name

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

`svv_all_tables` lists the views and the base, external, and shared tables the current user can access.
A full 100 rows means the list may be incomplete, so narrow the name pattern.

### Columns of one object

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

When `svv_columns` is denied, query `svv_redshift_columns` with `schema_name` in place of `table_schema` and without the length, precision, and scale columns, which it lacks, and report external columns as unverified.

## 3. View definition

```sql
SELECT
    schemaname,
    viewname,
    definition
FROM pg_catalog.pg_views
WHERE schemaname = 'schema_name'
    AND viewname = 'view_name';
```

`pg_catalog.pg_views` covers standard views visible to the session.
For a materialized, external, or shared view, use the catalog that holds it, or report its filters and joins as unverified.

## 4. Column search

Find the tables that hold a column matching a name pattern; add `AND table_schema = 'schema_name'` to the `WHERE` clause when the schema is known.

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

`information_schema.columns` misses external and shared objects, so zero rows does not prove the column is absent when the target holds them.
A full 100 rows means the search may be incomplete, so narrow the pattern, or remove the bound when the task needs every match.

## 5. Sample

```sql
SELECT
    source_table.Column1,
    source_table.Column2,
    source_table.CreatedDate
FROM schema_name.table_name AS source_table
ORDER BY source_table.CreatedDate DESC
LIMIT 100;
```

Label a sample as incomplete and state its bound and ordering.

## 6. Profile

Profile only the columns that can change the interpretation, because each `UNION ALL` branch scans the table again.

### NULL share and distinct count of one column

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

### Numeric statistics

```sql
SELECT
    COUNT(*) AS TotalRows,
    COUNT(source_table.NumericColumn) AS NonNullCount,
    MIN(source_table.NumericColumn) AS MinValue,
    MAX(source_table.NumericColumn) AS MaxValue,
    AVG(CAST(source_table.NumericColumn AS DOUBLE PRECISION)) AS AvgValue
FROM schema_name.table_name AS source_table;
```

### Several columns at once

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

## 7. Value distribution

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

NULL forms its own group, and its share is a data-quality finding.

## 8. Temporal coverage

Run the date range first, because it shows whether the monthly counts fit on screen.

```sql
SELECT
    MIN(source_table.EventDate) AS EarliestDate,
    MAX(source_table.EventDate) AS LatestDate,
    COUNT(*) AS TotalRows
FROM schema_name.table_name AS source_table;
```

```sql
SELECT
    DATE_TRUNC('month', source_table.EventDate) AS MonthStart,
    COUNT(*) AS RowsInMonth
FROM schema_name.table_name AS source_table
GROUP BY DATE_TRUNC('month', source_table.EventDate)
ORDER BY MonthStart DESC
LIMIT 60;
```

The monthly query covers the latest 60 months; state that bound, and remove it only when the task needs full coverage and the date range keeps the output readable.
Report a missing month or a sudden drop in volume as a finding.
