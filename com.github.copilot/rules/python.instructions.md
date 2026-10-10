---
name: "Python"
description: "Use when writing or changing a Python task script that the user runs directly. Supplies its shape, typing, comments, Polars data work, tests, formatting, and validation rules. Not for reusable modules, test suites, or application code."
---

# Python

Write Python as a working instrument for the user, who runs the script today and changes it tomorrow, not as production software.
Prefer the smallest implementation that produces the requested result.

Within a task script, follow the naming, structure, and idioms already established in the file.
When an established convention conflicts with a rule below, keep the file's convention and name the conflict in your result.

Target the Python version the project declares, and Python 3.11 when it declares none.

## Shape the script linearly

- Shape the script as "Preferred script shape" below shows, and give a script that does not import the project its inline script metadata block, so that it runs in its own environment.
- Put paths, thresholds, seeds, and other varying values in the constants block below the imports.
- Extract a helper only when it is called from more than one place, or when it replaces a distinct operation longer than 15 nonblank lines.
- Name intermediate results after their analytical role and keep them as visible variables.
- Set an explicit seed for every stochastic operation.
- Format the finished script with `uvx ruff format`, and when it fails, report the failed check instead of substituting another formatter.

Do not add classes, a command-line interface, configuration objects, plugin registries, dependency injection, or a logging framework to a script.
These layers cost more to read than the analysis they wrap, and a constant at the top of the file replaces most of them.
When the task appears to need one, report `Decision needed` with the purpose and the minimum shape, and do not add it.

Write a test for a task script only when an undetected error would cost more than the test, because the script answers one bounded question.

## Type only the boundaries

- Annotate function parameters and return values whose type cannot be read from the call site or the default value.
- When the target version is 3.10 or later, leave out `from __future__ import annotations`, because the version supports `str | None` at runtime.
- Leave local variables unannotated.
- When a type checker reports an error in a script, simplify the code or report the finding rather than annotating around it.

## Comment what the code cannot say

- Write a one-line comment where the code cannot show the reason for a step: a business threshold, a data quirk, a deliberate exclusion.
- Do not restate in a comment what the next line does, and do not record your change or its history there; the diff already carries both.
- Do not add a docstring to a local helper; keep only the module docstring in a task script.

## Work on tabular data with Polars

- Use `polars` for tabular work.
- Add `pandas` only for a reason the brief or the user names, because a second frame library doubles the conversions and idioms a reader must follow.
- Express transformations as Polars expressions instead of `iter_rows()`, `map_elements()`, or Python row loops.
- Read Parquet for a lazy workflow with `pl.scan_parquet()`.
- End a lazy chain with `sink_parquet()` when the result goes to Parquet, and with `.collect()` when the next step needs the frame in memory.
- Use `pl.read_parquet()` only when the next operation requires an eager frame, because `read_parquet()` materializes the file and loses scan-level optimizations even when followed by `.lazy()`.
- Prefix DataFrame variables with `df_`.
- Convert to NumPy or another representation only at the boundary of a library that requires it.

## Keep validation proportionate

Assume the input data is what the user says it is.
Fixing a script that breaks on bad input costs less than validation that outgrows the analysis and buries it.

- Add a plain `assert` with a short message only for an assumption whose failure would silently change the result, such as join cardinality that could duplicate rows.
- Let unexpected failures raise; a `try/except` that logs and continues can turn a visible error into a wrong number.
- Do not check the output for a property you already asserted on the input; inspect the transformation between them instead.
- Keep the checking code shorter than the transformation it protects.

## Preferred script shape

```python
# /// script
# requires-python = ">=3.11"
# dependencies = ["polars"]
# ///
"""Summarize daily event volume for the current question."""

from datetime import date
from pathlib import Path

import polars as pl

EVENTS_PATH = Path("data/processed/events.parquet")
# Records before the migration carry statuses that are not comparable.
CUTOFF_DATE = date(2024, 1, 1)


def main():
    df_daily = (
        pl.scan_parquet(EVENTS_PATH)
        .filter(pl.col("event_date") >= CUTOFF_DATE)
        .group_by("event_date")
        .agg(pl.len().alias("events"), pl.col("value").sum())
        .sort("event_date")
        .collect()
    )
    print(df_daily)


if __name__ == "__main__":
    main()
```
