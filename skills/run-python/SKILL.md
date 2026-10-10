---
name: run-python
description: "Use when running a Python script or inline Python. Supplies the uv prefix choice and command forms. Not for Python coding standards."
---

# Run Python with uv

Run Python through `uv`, because uv supplies the interpreter and the dependencies the code needs, while a bare `python` runs whatever environment the shell holds.

Choose the prefix by whether the code needs the project's environment, because inside a project `uv run` syncs the project before every run: use `uv run` when the code imports the project or its dependencies, and `uv run --no-project` otherwise.

- Run a script as `{prefix} path/to/script.py`, without `python`, because uv reads the script's inline dependency block only in this form; a script with that block runs outside the project with either prefix, so leave the block out of a script that imports the project.
- Run inline code as `{prefix} python -c "{code}"`.
- For inline code, and for a script you may not change, add `--with <package>` after the prefix for each package the environment lacks.
- For a script you write that does not import the project, declare the package in its inline dependency block instead, because the user reruns the script without your command line.
