#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-dotenv",
#   "redshift-connector",
# ]
# ///

"""Execute one Redshift SQL file and emit a bounded JSON result."""

import argparse
import csv
import json
import os
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import redshift_connector
from dotenv import load_dotenv

INLINE_ROW_LIMIT = 100
RESULT_ROW_LIMIT = 1_000


class InputError(Exception):
    """Raised when the SQL input file is invalid."""


class ConfigurationError(Exception):
    """Raised when Redshift connection settings are invalid."""


class QueryError(Exception):
    """Raised when Redshift cannot execute or return a query result."""


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a Redshift SQL file and return a bounded JSON result."
    )
    parser.add_argument("sql_file", type=Path, help="Path to one .sql file")
    return parser.parse_args()


def read_query(sql_file: Path) -> str:
    """Read a non-empty SQL file."""
    if sql_file.suffix.lower() != ".sql":
        raise InputError(f"SQL input must be a .sql file: {sql_file}")
    if not sql_file.is_file():
        raise InputError(f"SQL file not found: {sql_file}")
    try:
        query = sql_file.read_text(encoding="utf-8")
    except OSError as error:
        raise InputError(f"Cannot read SQL file: {sql_file}") from error
    if not query.strip():
        raise InputError(f"SQL file is empty: {sql_file}")
    return query


def connection_settings() -> dict[str, Any]:
    """Read Redshift connection settings from the workspace environment."""
    load_dotenv(dotenv_path=Path.cwd() / ".env")
    required_names = (
        "REDSHIFT_USER",
        "REDSHIFT_PASSWORD",
        "REDSHIFT_HOST",
        "REDSHIFT_PORT",
        "REDSHIFT_DATABASE",
    )
    missing_names = [name for name in required_names if not os.environ.get(name)]
    if missing_names:
        raise ConfigurationError(
            "Missing required Redshift environment variables: "
            + ", ".join(missing_names)
        )
    try:
        port = int(os.environ["REDSHIFT_PORT"])
    except ValueError as error:
        raise ConfigurationError("REDSHIFT_PORT must be an integer") from error
    if not 1 <= port <= 65535:
        raise ConfigurationError("REDSHIFT_PORT must be between 1 and 65535")
    return {
        "user": os.environ["REDSHIFT_USER"],
        "password": os.environ["REDSHIFT_PASSWORD"],
        "host": os.environ["REDSHIFT_HOST"],
        "port": port,
        "database": os.environ["REDSHIFT_DATABASE"],
    }


def execute_query(
    query: str, settings: dict[str, Any]
) -> tuple[list[dict[str, str]], list[tuple[Any, ...]], bool]:
    """Run a query without committing and return at most RESULT_ROW_LIMIT rows."""
    connection = None
    cursor = None
    try:
        connection = redshift_connector.connect(**settings)
        cursor = connection.cursor()
        cursor.execute(query)
        if cursor.description is None:
            raise QueryError("Query did not return a result set")
        columns = [
            {"name": str(description[0]), "type": str(description[1])}
            for description in cursor.description
        ]
        rows = list(cursor.fetchmany(RESULT_ROW_LIMIT + 1))
        truncated = len(rows) > RESULT_ROW_LIMIT
        return columns, rows[:RESULT_ROW_LIMIT], truncated
    except QueryError:
        raise
    except Exception as error:
        if connection is None:
            raise ConfigurationError("Could not connect to Redshift") from error
        raise QueryError("Redshift could not execute the SQL query") from error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def csv_path_for(sql_file: Path) -> Path:
    """Create a workspace-relative path for a large result CSV."""
    safe_stem = re.sub(r"[^A-Za-z0-9_-]+", "-", sql_file.stem).strip("-") or "result"
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return Path(".tmp") / "redshift-results" / f"{safe_stem}-{timestamp}.csv"


def write_csv(
    path: Path, columns: list[dict[str, str]], rows: list[tuple[Any, ...]]
) -> None:
    """Write query rows to a CSV file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([column["name"] for column in columns])
        writer.writerows(rows)


def result_payload(
    sql_file: Path,
    columns: list[dict[str, str]],
    rows: list[tuple[Any, ...]],
    truncated: bool,
) -> dict[str, Any]:
    """Build the JSON result payload and write large results to CSV."""
    payload: dict[str, Any] = {
        "columns": columns,
        "row_count": len(rows),
        "truncated": truncated,
    }
    if len(rows) <= INLINE_ROW_LIMIT:
        payload["rows"] = rows
        return payload

    csv_path = csv_path_for(sql_file)
    write_csv(csv_path, columns, rows)
    payload["csv_path"] = str(csv_path)
    payload["note"] = "Rows are stored in csv_path."
    return payload


def main() -> int:
    """Run the requested SQL file and print exactly one JSON payload on success."""
    args = parse_args()
    try:
        query = read_query(args.sql_file)
        columns, rows, truncated = execute_query(query, connection_settings())
        print(
            json.dumps(
                result_payload(args.sql_file, columns, rows, truncated), default=str
            )
        )
        return 0
    except InputError as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2
    except ConfigurationError as error:
        print(f"Connection error: {error}", file=sys.stderr)
        return 3
    except QueryError as error:
        print(f"Query error: {error}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    raise SystemExit(main())
