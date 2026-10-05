---
name: run-python
description: "Run Python scripts and inline Python through uv. Use when an agent needs to execute Python in a repository. Not for Python coding standards."
argument-hint: "Describe the Python script or check to run"
---

# Run Python with uv

Always run Python through `uv`. Never invoke `python` or `python3` directly.

1. Check only whether `pyproject.toml` exists in the repository root.
2. When it exists, run a script with `uv run python path/to/script.py`.
3. When it does not exist, run a script with `uv run --no-project python path/to/script.py`.
4. When the execution requires a package unavailable from the selected environment, add `--with <package>` for each explicitly required dependency before `python`.
5. For inline code, use the same prefix and pass the code after `-c` as one argument with quoting and escaping valid for the active shell.

Keep the working directory at the repository root unless the script requires another directory. Report the command and its exit status.

The task is complete when the Python code ran through the correct `uv` prefix and the command result is reported.
