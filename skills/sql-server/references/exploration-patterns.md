# SQL Server exploration patterns

Read only the section for the unknown item or the requested check.
Run each pattern through the read-only gate of the [SQL Server skill](../SKILL.md) with the active connection, and replace `dbo.TableName` and the column placeholders with exact names.

## 1. Relationships

### Declared foreign keys touching one table

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

When no foreign key is declared, find candidate keys with the [column search](#4-column-search), then test each proposed join with the uniqueness check.

### Join-key uniqueness

Check which side of a join is unique, because a duplicated key fans out the join and inflates every aggregate after it.

```sql
SELECT TOP 20
    source_table.CandidateKey,
    COUNT(*) AS DuplicateCount
FROM dbo.TableName AS source_table
GROUP BY source_table.CandidateKey
HAVING COUNT(*) > 1
ORDER BY DuplicateCount DESC;
```

Zero rows means no duplicate non-NULL key in the checked population.
Any row means the join can multiply rows, so state the expected cardinality and check the joined row count.

### Unmatched keys

Count the child rows whose key finds no parent, because an `INNER JOIN` drops them without a signal.
Run it after the uniqueness check confirms the parent key is unique, because a duplicated parent key inflates `ChildRows`.

```sql
SELECT
    COUNT(*) AS ChildRows,
    SUM(CASE WHEN parent_table.ParentKey IS NULL THEN 1 ELSE 0 END) AS UnmatchedRows
FROM dbo.ChildTable AS child_table
LEFT JOIN dbo.ParentTable AS parent_table
    ON child_table.ParentKey = parent_table.ParentKey;
```

Rows with a NULL child key count as unmatched.

## 2. Objects and columns

### One named object

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

Zero rows means the object is not visible in the active database.
More than one row means the name belongs to several object types, so choose the type explicitly.

### Columns and types of one object

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

`MaxLength` is in bytes, so an `nvarchar` column shows twice its character length, and `-1` means `(max)`.

## 3. View definition

```sql
SELECT OBJECT_DEFINITION(OBJECT_ID(N'dbo.ViewName')) AS ViewDefinition;
```

`NULL` means the definition is encrypted, not visible, or otherwise unavailable, so report the view's filters and joins as unverified.

## 4. Column search

Find the tables that hold a column matching a name pattern.

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

Narrow by type with a filter such as `AND column_info.DATA_TYPE IN (N'nvarchar', N'varchar')`.
The search covers the active database only, so repeat it in each database the task spans.
Zero rows means no visible match in this database, not that the column exists nowhere.
A full 100 rows means the search may be incomplete, so narrow the pattern, or remove the bound when the task needs every match.

## 5. Sample

```sql
SELECT TOP 100
    source_table.Column1,
    source_table.Column2,
    source_table.CreatedDate
FROM dbo.TableName AS source_table
ORDER BY source_table.CreatedDate DESC;
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
    CAST(
        (COUNT(*) - COUNT(source_table.ColumnName)) * 100.0 / NULLIF(COUNT(*), 0)
        AS DECIMAL(5, 2)
    ) AS NullPercent,
    COUNT(DISTINCT source_table.ColumnName) AS DistinctCount
FROM dbo.TableName AS source_table;
```

### Numeric statistics

```sql
SELECT
    COUNT(*) AS TotalRows,
    COUNT(source_table.NumericColumn) AS NonNullCount,
    MIN(source_table.NumericColumn) AS MinValue,
    MAX(source_table.NumericColumn) AS MaxValue,
    AVG(CAST(source_table.NumericColumn AS FLOAT)) AS AvgValue
FROM dbo.TableName AS source_table;
```

### Several columns at once

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

## 7. Value distribution

```sql
SELECT TOP 20
    source_table.CategoryColumn,
    COUNT(*) AS Frequency,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS DECIMAL(5, 2)) AS Pct
FROM dbo.TableName AS source_table
GROUP BY source_table.CategoryColumn
ORDER BY Frequency DESC;
```

NULL forms its own group, and its share is a data-quality finding.

## 8. Temporal coverage

Run the date range first, because it shows whether the monthly counts fit on screen.

```sql
SELECT
    MIN(source_table.EventDate) AS EarliestDate,
    MAX(source_table.EventDate) AS LatestDate,
    COUNT(*) AS TotalRows
FROM dbo.TableName AS source_table;
```

```sql
SELECT TOP 60
    DATEFROMPARTS(YEAR(source_table.EventDate), MONTH(source_table.EventDate), 1) AS MonthStart,
    COUNT(*) AS RowsInMonth
FROM dbo.TableName AS source_table
GROUP BY DATEFROMPARTS(YEAR(source_table.EventDate), MONTH(source_table.EventDate), 1)
ORDER BY MonthStart DESC;
```

The monthly query covers the latest 60 months; state that bound, and remove it only when the task needs full coverage and the date range keeps the output readable.
Report a missing month or a sudden drop in volume as a finding.
