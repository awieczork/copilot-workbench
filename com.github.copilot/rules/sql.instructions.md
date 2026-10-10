---
name: "SQL"
description: "Use when writing or reviewing a read-only SELECT query for SQL Server or Redshift. Supplies formatting, correctness, and performance rules. Not for view definitions, procedural batches, or statements that change data or schema."
applyTo: "**/*.sql"
---

# SQL

Every rule applies to both SQL Server and Redshift unless a section names one engine.

Determine the target engine from the file path, the header comment, or the surrounding code before writing engine-specific SQL.
When none of them identifies the engine, ask the user, because a Redshift pattern silently fails on SQL Server and the reverse.

## Format and name

Format SQL so that a reader finds an entity by grep and sees the join graph without reformatting.

- Write keywords in uppercase, indent with 4 spaces, and put one column per line with trailing commas in `SELECT` lists.
- Name aliases after the entity (`sub`, `lic`, `cal`, `ord`) rather than by a single letter.
- Qualify each table or view with its schema.
- Write every join explicitly, because a comma join with the condition in `WHERE` hides the join graph.
- Name new aliases, CTEs, and column aliases in English, and spell existing schema objects exactly as the source system spells them, including non-English ERP names.
- Target 80 characters per line and keep every line at or below 120, breaking before `AND`, `OR`, or `JOIN`, or after a comma.
- Comment the intent, business context, or threshold reasoning, never the mechanics; document every numeric threshold, because an undocumented magic number in feature logic is an unrecorded analytical decision.
- Divide a query with distinct analytical phases into phases with `-- === SECTION NAME ===` separators.
- When the query is kept as a file, open it with a `/* */` header stating purpose and target engine.

```sql
/* Purpose: Rolling revenue metrics per customer
    Engine:  Redshift */

-- === BASE POPULATION ===
WITH active_customers AS (
    SELECT
        cust.id_klient_zbiorczy_dwh AS customer_id,
        ord.order_date,
        ord.revenue
    FROM schema.dm_klient AS cust
    INNER JOIN schema.orders AS ord
        ON cust.customer_key = ord.customer_key
    -- The metric excludes orders before the reporting baseline.
    WHERE ord.order_date >= CAST('2024-01-01' AS DATE)
        AND ord.status = 'completed'
)

-- === WINDOW AGGREGATIONS ===
SELECT
    ac.customer_id,
    ac.order_date,
    SUM(ac.revenue) OVER (
        PARTITION BY ac.customer_id
        ORDER BY ac.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS revenue_cumulative,
    AVG(ac.revenue) OVER (
        PARTITION BY ac.customer_id
        ORDER BY ac.order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS revenue_avg_running
FROM active_customers AS ac
ORDER BY ac.customer_id, ac.order_date;
```

## Keep results correct

The expensive analytical failure is silent: a wrong number that looks right.
These rules make NULL handling, join fan-out, and type coercion visible.

- Handle NULL with `COALESCE` on both engines; `ISNULL` (SQL Server) and `NVL` (Redshift) do not port across them.
- Give every `CASE` expression an explicit `ELSE` so the fallback value is visible.
- When the relationship is known and not obvious from declared keys, record the expected join cardinality in a comment immediately before the join.
- Use `NOT EXISTS` instead of `NOT IN` against a subquery that can return NULL, because a single NULL makes `NOT IN` return no rows.
- Fix a duplicate-producing join at its source rather than masking it with `DISTINCT`, which adds a sort and hides the defect.
- Cast types explicitly when operands differ or a literal's inferred type is not the intended type.

## Keep the plan fast

These patterns prevent the plans that dominate analytical run time on both engines.

- List the required columns in every `SELECT`; `SELECT *` reads unnecessary columns and makes the result contract depend on schema changes.
- Keep predicates SARGable by leaving the column bare in `WHERE`; wrapping it in a function such as `YEAR(date_col)` blocks index seeks and block skipping, so rewrite the condition as a range.
- Put a table-specific predicate in that table's earliest query block when doing so preserves outer-join semantics.
- Replace a correlated subquery in a `SELECT` list with a window function or join when the optimizer cannot decorrelate it, and replace repeated self-selects with `CASE` conditional aggregation.

## Structure intermediate results and windows

- Use a common table expression or subquery to name a distinct intermediate result inside the single read query.
- When a window aggregate has `ORDER BY`, write an explicit `ROWS BETWEEN ...` frame, because Redshift requires one and SQL Server's default frame groups ties as peers.
- When peer behavior is intended on SQL Server, state it in an adjacent comment.
- Repeat the inline `OVER (...)` specification for a window reused across expressions, because the named `WINDOW` clause does not port between the engines.
- Stage a nested window calculation in a CTE or subquery, because nesting window functions directly is invalid SQL.
- Replace `COUNT(DISTINCT x) OVER (...)` with a `DENSE_RANK` construction or a subquery, because neither engine supports it as a window aggregate.

## Apply SQL Server specifics

- Write Unicode string literals as `N'...'` when the compared value or target column is `NVARCHAR`.
- Keep scalar user-defined functions out of `WHERE` and `JOIN` predicates, because they often run once per row.

## Apply Redshift specifics

- Align filters, joins, grouping, and window partitions with the sort and distribution keys where the question allows, because Redshift then skips blocks and avoids moving data between nodes, and check `EXPLAIN` for redistribution.
