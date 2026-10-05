# SQL Server exploration patterns

Use sections 1-4 for targeted discovery or verification of unknown source details. Do not use those discovery patterns when the supplied SQL already identifies every required object and column. Read sections 5-8 when the task explicitly requests a sample or a quality check. Replace `dbo.TableName` and column placeholders with exact schema-qualified objects.

---

## 1. Relationship discovery

Run every SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass the SQL in `query`, classify it with `queryTypes: ["SELECT"]` and any applicable `JOIN` or `CTE`, and use the matching `queryIntent`.

Inspect relationships when a join path or cardinality is unknown. Start with declared foreign keys, then verify an undeclared relationship with key uniqueness and row-count checks.

### Relationships touching one table (both directions)

```sql
SELECT
    fk.[name] AS ForeignKeyName,
    OBJECT_SCHEMA_NAME(fk.parent_object_id) + '.' + OBJECT_NAME(fk.parent_object_id) AS ParentTable,
    parent_column.[name] AS ParentColumn,
    OBJECT_SCHEMA_NAME(fk.referenced_object_id) + '.' + OBJECT_NAME(fk.referenced_object_id) AS ReferencedTable,
    referenced_column.[name] AS ReferencedColumn
FROM sys.foreign_keys AS fk
INNER JOIN sys.foreign_key_columns AS fk_column
    ON fk.object_id = fk_column.constraint_object_id
INNER JOIN sys.columns AS parent_column
    ON fk_column.parent_object_id = parent_column.object_id
    AND fk_column.parent_column_id = parent_column.column_id
INNER JOIN sys.columns AS referenced_column
    ON fk_column.referenced_object_id = referenced_column.object_id
    AND fk_column.referenced_column_id = referenced_column.column_id
WHERE fk.parent_object_id = OBJECT_ID(N'dbo.TableName')
    OR fk.referenced_object_id = OBJECT_ID(N'dbo.TableName')
ORDER BY ParentTable, ForeignKeyName, fk_column.constraint_column_id;
```

Relationship discovery is complete when declared relationships touching the requested table are reported with their paired columns or no declared relationship is found.

Warehouse and enterprise resource planning schemas commonly declare no foreign keys, yet still have join paths. Use the column search below only when the join path is unknown, then verify every proposed join with the key-uniqueness check.

### Join-key uniqueness check

Before joining on a candidate key, confirm which side is unique — a key that silently duplicates fans out the join and inflates every downstream aggregate.

```sql
SELECT TOP 20
    source_table.CandidateKey,
    COUNT(*) AS DuplicateCount
FROM dbo.TableName AS source_table
GROUP BY source_table.CandidateKey
HAVING COUNT(*) > 1
ORDER BY DuplicateCount DESC;
```

Zero rows means the key has no duplicate non-NULL values in the checked population. Any row means the join can multiply rows; state the expected cardinality and check the joined row count.

Join-key verification is complete when uniqueness status, expected cardinality, and any row multiplication are reported.

Relationship analysis is complete when every requested join path has a declared relationship or a tested cardinality, or the limitation is reported.

---

## 2. Exact object and column discovery

Run every SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass the SQL in `query`, classify it with `queryTypes: ["SELECT"]` and any applicable `JOIN` or `CTE`, and use the matching `queryIntent`.

### Find one known object

```sql
SELECT
    schema_object.[name] AS SchemaName,
    source_object.[name] AS ObjectName,
    source_object.[type_desc] AS ObjectType,
    source_object.create_date AS CreatedDate,
    source_object.modify_date AS ModifiedDate
FROM sys.objects AS source_object
INNER JOIN sys.schemas AS schema_object
    ON source_object.schema_id = schema_object.schema_id
WHERE schema_object.[name] = N'dbo'
    AND source_object.[name] = N'ObjectName'
ORDER BY source_object.[type_desc];
```

Zero rows means the named object is not visible in the active database. More than one row means the name resolves to multiple object classes and requires an explicit type choice.

Object discovery is complete when one intended object is identified, or zero or multiple matches are reported with the required correction.

### Inspect columns and types for one object

```sql
SELECT
    column_object.column_id AS ColumnId,
    column_object.[name] AS ColumnName,
    type_object.[name] AS DataType,
    column_object.max_length AS MaxLength,
    column_object.[precision] AS NumericPrecision,
    column_object.scale AS NumericScale,
    column_object.is_nullable AS IsNullable
FROM sys.columns AS column_object
INNER JOIN sys.types AS type_object
    ON column_object.user_type_id = type_object.user_type_id
WHERE column_object.object_id = OBJECT_ID(N'dbo.ObjectName')
ORDER BY column_object.column_id;
```

Inspection is complete when every column used by the planned query appears with its type and nullability.

---

## 3. View definition inspection

Run the SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass the SQL in `query` with `queryTypes: ["SELECT"]` and `queryIntent: "schema_exploration"`.

Databases can encode business logic in views. Read the definition when hidden filters or joins could affect the requested result, unless the definition is already supplied.

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID(N'dbo.ViewName')) AS ViewDefinition;
```

Inspection is complete when the definition is available or its unavailability is reported before interpretation.

`OBJECT_DEFINITION` can return `NULL` for an encrypted, non-visible, or otherwise unavailable definition. Treat `NULL` as a verification limit, not as proof that the view has no definition.

---

## 4. Column search

Run the SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass the SQL in `query` with `queryTypes: ["SELECT"]` and `queryIntent: "schema_exploration"`.

Find tables containing columns that match a name pattern — also the fallback for join-path guessing when foreign keys are undeclared.

```sql
SELECT TOP 100
    column_info.TABLE_SCHEMA,
    column_info.TABLE_NAME,
    column_info.COLUMN_NAME,
    column_info.DATA_TYPE,
    column_info.IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS AS column_info
WHERE column_info.COLUMN_NAME LIKE N'%SearchPattern%'
ORDER BY column_info.TABLE_SCHEMA, column_info.TABLE_NAME, column_info.COLUMN_NAME;
```

Add `AND column_info.DATA_TYPE IN (N'nvarchar', N'varchar')` or another type filter to narrow by kind.

This search covers the active database only. Run it after the target step has established the active database. If the task spans databases, repeat the search in each selected database.

Zero rows mean no visible match in the active database and catalog, not proof that the column is absent from every database or inaccessible object.

The query is bounded at 100 rows. If it returns 100 rows, report the search as potentially incomplete and narrow the pattern or remove the bound only when a complete search is required.

Search is complete when all matching candidates are reported within the bound, or the bound is reached and the search is marked potentially incomplete with its next action.

---

## 5. Data sampling

Run the SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass the SQL in `query` with `queryTypes: ["SELECT"]` and `queryIntent: "data_exploration"`.

### Recent rows (explicit columns, bounded)

```sql
SELECT TOP 100
    source_table.Column1,
    source_table.Column2,
    source_table.CreatedDate
FROM dbo.TableName AS source_table
ORDER BY source_table.CreatedDate DESC;
```

Sampling is complete when the bound and ordering are stated and the sample is labeled as non-complete.

---

## 6. Data profiling

Run every SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass each SQL statement in `query` with `queryTypes: ["SELECT"]` and `queryIntent: "data_exploration"`.

### NULL density and distinct count for a single column

```sql
SELECT
    COUNT(*) AS TotalRows,
    COUNT(source_table.ColumnName) AS NonNullCount,
    COUNT(*) - COUNT(source_table.ColumnName) AS NullCount,
    CAST(
        (COUNT(*) - COUNT(source_table.ColumnName)) * 100.0 / NULLIF(COUNT(*), 0)
        AS DECIMAL(5, 2)
    ) AS NullPercent,
    COUNT(DISTINCT source_table.ColumnName) AS DistinctCount
FROM dbo.TableName AS source_table;
```

### Numeric column statistics

```sql
SELECT
    COUNT(*) AS TotalRows,
    COUNT(source_table.NumericColumn) AS NonNullCount,
    MIN(source_table.NumericColumn) AS MinValue,
    MAX(source_table.NumericColumn) AS MaxValue,
    AVG(CAST(source_table.NumericColumn AS FLOAT)) AS AvgValue
FROM dbo.TableName AS source_table;
```

### Multi-column profile summary

Each UNION ALL branch scans the table again — on large tables profile the columns that matter, not everything.

```sql
SELECT
    'ColumnA' AS ColumnName,
    COUNT(*) AS TotalRows,
    COUNT(source_table.ColumnA) AS NonNullCount,
    COUNT(DISTINCT source_table.ColumnA) AS DistinctCount
FROM dbo.TableName AS source_table
UNION ALL
SELECT
    'ColumnB' AS ColumnName,
    COUNT(*) AS TotalRows,
    COUNT(source_table.ColumnB) AS NonNullCount,
    COUNT(DISTINCT source_table.ColumnB) AS DistinctCount
FROM dbo.TableName AS source_table;
```

Profiling is complete when every requested column has the applicable statistics and scan limitations are reported.

---

## 7. Value distributions

Run the SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass the SQL in `query` with `queryTypes: ["SELECT"]` and `queryIntent: "data_exploration"`.

The first question about any categorical column: what values does it take and how often — including how many rows the long tail hides.

### Top-N frequency for a categorical column

```sql
SELECT TOP 20
    source_table.CategoryColumn,
    COUNT(*) AS Frequency,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(5, 2)) AS Pct
FROM dbo.TableName AS source_table
GROUP BY source_table.CategoryColumn
ORDER BY Frequency DESC;
```

NULL appears as its own group when present — its rank in the output is itself a data-quality finding.

Distribution profiling is complete when the requested category values, frequencies, and NULL handling are reported.

---

## 8. Temporal coverage

Run every SQL block in this section through #tool:ms-mssql.mssql/mssql_run_query with the active `connectionId` for the user-provided server and database. Pass each SQL statement in `query` with `queryTypes: ["SELECT"]` and `queryIntent: "data_exploration"`.

Date range and per-month density reveal freshness, backfill gaps, and volume shifts before any time-based analysis is built on the table.

### Date range of a table

```sql
SELECT
    MIN(source_table.EventDate) AS EarliestDate,
    MAX(source_table.EventDate) AS LatestDate,
    COUNT(*) AS TotalRows
FROM dbo.TableName AS source_table;
```

### Rows per month

Run the date-range query first. Use the monthly query below as a recent 60-month inspection and report that bound. Remove `TOP 60` only when complete monthly coverage is required and the date range establishes that the output remains practical to inspect.

```sql
SELECT TOP 60
    DATEFROMPARTS(YEAR(source_table.EventDate), MONTH(source_table.EventDate), 1) AS MonthStart,
    COUNT(*) AS RowsInMonth
FROM dbo.TableName AS source_table
GROUP BY DATEFROMPARTS(YEAR(source_table.EventDate), MONTH(source_table.EventDate), 1)
ORDER BY MonthStart DESC;
```

A missing month or a sudden volume drop within the inspected range is a finding to report, not an artifact to skip past.

Temporal inspection is complete when the observed date range, the 60-month bound or its absence, expected period coverage, and missing or sparse periods within the inspected range are reported.

---
