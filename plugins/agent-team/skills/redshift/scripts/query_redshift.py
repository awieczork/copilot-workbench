#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-dotenv",
#   "redshift-connector",
# ]
# ///

"""Execute one Redshift SQL statement from standard input and emit a bounded JSON result."""

import json
import os
import sys
from pathlib import Path
from typing import Any

import redshift_connector
from dotenv import load_dotenv

ROW_LIMIT = 100


def read_query() -> str:
    """Read a non-empty SQL statement from standard input."""
    if sys.stdin.isatty():
        raise SystemExit("Input error: Expected one SQL statement on standard input")
    try:
        query = sys.stdin.buffer.read().decode("utf-8")
    except UnicodeDecodeError as error:
        raise SystemExit("Input error: Standard input must be UTF-8 encoded") from error
    if not query.strip():
        raise SystemExit("Input error: Expected one SQL statement on standard input; got none")
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
        raise SystemExit(
            "Connection error: Missing required Redshift environment variables: "
            + ", ".join(missing_names)
        )
    try:
        port = int(os.environ["REDSHIFT_PORT"])
    except ValueError as error:
        raise SystemExit("Connection error: REDSHIFT_PORT must be an integer") from error
    if not 1 <= port <= 65535:
        raise SystemExit("Connection error: REDSHIFT_PORT must be between 1 and 65535")
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
    """Run a query without committing and return at most ROW_LIMIT rows."""
    connection = None
    cursor = None
    try:
        connection = redshift_connector.connect(**settings)
        cursor = connection.cursor()
        cursor.execute(query)
        if cursor.description is None:
            raise SystemExit("Query error: Query did not return a result set")
        columns = [
            {"name": str(description[0]), "type": str(description[1])}
            for description in cursor.description
        ]
        rows = list(cursor.fetchmany(ROW_LIMIT + 1))
        truncated = len(rows) > ROW_LIMIT
        return columns, rows[:ROW_LIMIT], truncated
    except Exception as error:
        if connection is None:
            raise SystemExit(
                f"Connection error: Could not connect to Redshift ({type(error).__name__})"
            ) from error
        raise SystemExit(
            f"Query error: Redshift could not execute the SQL query: {error}"
        ) from error
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def result_payload(
    columns: list[dict[str, str]],
    rows: list[tuple[Any, ...]],
    truncated: bool,
    settings: dict[str, Any],
) -> dict[str, Any]:
    """Build the JSON result payload, with the target the runner used and no credentials."""
    return {
        "target": {"host": settings["host"], "database": settings["database"]},
        "columns": columns,
        "rows": rows,
        "row_count": len(rows),
        "truncated": truncated,
    }


def main() -> int:
    """Run the SQL statement and print exactly one JSON payload on success."""
    query = read_query()
    settings = connection_settings()
    columns, rows, truncated = execute_query(query, settings)
    print(json.dumps(result_payload(columns, rows, truncated, settings), default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
