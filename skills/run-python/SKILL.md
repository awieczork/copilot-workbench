---
name: run-python
description: "Run Python scripts and inline Python through uv. Use when an agent needs to execute Python in a repository. Not for Python coding standards."
argument-hint: "Describe the Python script or check to run"
---

# Run Python with uv

Run Python through `uv`, because uv supplies the interpreter and the dependencies the code needs, while a bare `python` runs whatever environment the shell holds.

Choose the prefix by whether the code needs the project's environment, because inside a project `uv run` installs the project before every run:

- When the code imports the project or its dependencies, use `uv run`.
- Otherwise, use `uv run --no-project`.

Run from the repository root unless the code needs another directory, because uv finds the project from the working directory upward.

- Run a script as `{prefix} path/to/script.py`, without `python`, because uv reads the script's inline dependency block only in this form; a script with that block runs isolated from the project.
- Run inline code as `{prefix} python -c "{code}"`.
- Add `--with <package>` after the prefix for each package the environment lacks.
