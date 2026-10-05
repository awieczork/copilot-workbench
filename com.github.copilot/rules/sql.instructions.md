---
name: "SQL"
description: "SQL Server and Redshift rules for the text of one read-only SELECT query with optional CTEs and set operators."
applyTo: "**/*.sql"
---

# SQL

Apply these rules only to the text of one read-only `SELECT` query with optional common table expressions and set operators.
Every rule applies to both SQL Server and Redshift unless a section names one engine.

Do not apply this file to view definitions, procedural batches, session settings, temporary objects, or statements that change data or schema.
The `applyTo` glob still matches those files because VS Code provides no documented exclusion syntax; this boundary relies on model compliance.
Query execution, connection handling, result bounds, and execution-tool safety are outside this file's scope.

Determine the target engine from the file path, the header comment, or the surrounding code before writing engine-specific SQL.
When none of them identifies the engine, ask the user, because a Redshift pattern silently fails on SQL Server and the reverse.

## Format and name

Format SQL so that a reader finds an entity by grep and sees the join graph without reformatting.

- Write keywords in uppercase, indent with 4 spaces, and put one column per line with trailing commas in `SELECT` lists.
- Name aliases after the entity (`sub`, `lic`, `cal`, `ord`) rather than by a single letter.
- Qualify each table or view with its schema.
- Write every join as an explicit `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`, or `CROSS JOIN`; a comma-join with the condition in `WHERE` hides the join graph.
- Name new aliases, CTEs, and column aliases in English, and spell existing schema objects exactly as the source system spells them, including non-English ERP names.
- Target 80 characters per line and keep every line at or below 120, breaking before `AND`, `OR`, or `JOIN`, or after a comma.
- Comment the intent, business context, or threshold reasoning, never the mechanics; document every numeric threshold, because an undocumented magic number in feature logic is an unrecorded analytical decision.
- Divide a query with distinct analytical phases into phases with `-- === SECTION NAME ===` separators.
- When the query is kept as a file, open it with a `/* */` header stating purpose and target engine.

The formatting is complete when every join is explicit, every alias is named, every threshold carries its reason, and each query with distinct analytical phases uses section separators.

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

- Compare against NULL with `IS NULL` or `IS NOT NULL`, because `= NULL` and `<> NULL` evaluate to UNKNOWN and drop the row.
- Handle NULL with `COALESCE` on both engines; `ISNULL` (SQL Server) and `NVL` (Redshift) do not port across them.
- Give every `CASE` expression an explicit `ELSE` so the fallback value is visible.
- When the relationship is known and not obvious from declared keys, record the expected join cardinality in a comment immediately before the join.
- Fix a duplicate-producing join at its source rather than masking it with `DISTINCT`, which adds a sort and hides the defect.
- Give every non-cross join a condition. Use `CROSS JOIN` only when the Cartesian product is intentional.
- Cast types explicitly when operands differ or a literal's inferred type is not the intended type.

The correctness pass is complete when every non-cross join has a condition, each known non-obvious relationship has an expected-cardinality comment, and each required type conversion is explicit.

## Keep the plan fast

These patterns prevent the plans that dominate analytical run time on both engines.

- List the required columns in every `SELECT`; `SELECT *` reads unnecessary columns and makes the result contract depend on schema changes.
- Keep predicates SARGable by leaving the column bare in `WHERE`; wrapping it in a function such as `YEAR(date_col)` blocks index seeks and block skipping, so rewrite the condition as a range.
- Choose the cheapest operator that expresses the condition: a comparison before `LIKE`, and `LIKE` before a regular expression.
- Put a table-specific predicate in that table's earliest query block when doing so preserves outer-join semantics.
- Replace a correlated subquery in a `SELECT` list with a window function or join when the optimizer cannot decorrelate it, and replace repeated self-selects with `CASE` conditional aggregation.

The performance pass is complete when every predicate is SARGable or its function use is justified, each table-specific filter is placed in the earliest safe query block, and each retained correlated subquery has a reason or none is present.

## Structure intermediate results and windows

- Use a common table expression or subquery to name a distinct intermediate result inside the single read query.
- When a window aggregate has `ORDER BY`, write an explicit `ROWS BETWEEN ...` frame when row-by-row behavior is intended. When peer behavior is intended, document that behavior in an adjacent comment. Treat the frame as part of the result contract rather than relying on engine defaults, because ties can change peer-based behavior.
- Repeat the inline `OVER (...)` specification for a window reused across expressions; the named `WINDOW` clause is unsupported on Redshift and needs SQL Server 2022 at compatibility level 160.
- Stage a nested window calculation in a CTE or subquery, because nesting window functions directly is invalid SQL.
- Replace `COUNT(DISTINCT x) OVER (...)` with a `DENSE_RANK` construction or a subquery, because neither engine supports it as a window aggregate.

The structure pass is complete when each intermediate result has a named CTE or subquery, every ordered window has an explicit frame or an adjacent comment naming the intended peer behavior, and nested windows are staged.

## Apply SQL Server specifics

- Write Unicode string literals as `N'...'` when the compared value or target column is `NVARCHAR`.
- Keep scalar user-defined functions out of `WHERE` and `JOIN` predicates unless the target's compatibility level and function definition make them eligible for scalar UDF inlining.

SQL Server-specific checks are complete when applicable Unicode literals and scalar UDF predicates follow these rules, or the query has no such construct.

## Apply Redshift specifics

- Filter and sort on the table's sort-key columns wherever the question allows, because a predicate on a leading sort-key column enables zone-map pruning.
- To qualify for one-phase aggregation, group only by sort-key columns beginning with the first sort key, and include a sort-key column that is also the distribution key.
- Join on the distribution key when both tables share it; otherwise inspect the plan for redistribution such as `DS_DIST_BOTH`, `DS_DIST_INNER`, `DS_DIST_OUTER`, or `DS_BCAST_INNER`.
- Align `PARTITION BY` columns with the DISTKEY where possible to keep window computation local to a slice.

Redshift-specific checks are complete when applicable sort and distribution choices follow these rules and any redistribution risk is reported, or the query has no such construct.
