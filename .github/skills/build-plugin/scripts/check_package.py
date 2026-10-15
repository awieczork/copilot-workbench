# /// script
# requires-python = ">=3.11"
# dependencies = ["jsonschema>=4.23", "pyyaml>=6"]
# ///
"""Check the static conformance of the Agent Plugins package in a directory.

Usage: uv run check_package.py [plugin-root]   (default: the current directory)
Prints one "{path}: {problem}" line per failure and exits with status 1 when any check fails.
"""

import json
import re
import sys
import urllib.request
from pathlib import Path

import jsonschema
import yaml

PAYLOAD = [
    ".github/plugin/marketplace.json",
    "plugin.json",
    "mcp.json",
    "skills",
    "com.github.copilot",
    "README.md",
    "CHANGELOG.md",
]
SUFFIXES = {"agents": ".agent.md", "rules": ".instructions.md"}
SKILL_NAME = re.compile(r"^(?!.*--)[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?$")
LINK = re.compile(r"\]\(([^)\s]+)\)")
CODE = re.compile(r"(`{3,}|~{3,}).*?\1|`[^`\n]*`", re.DOTALL)
ABSOLUTE = re.compile(r"^(?:/|~|[A-Za-z]:[\\/])")

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
failures: list[str] = []


def fail(path: Path, problem: str) -> None:
    failures.append(f"{path.relative_to(root)}: {problem}")


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)


def check_manifest(name: str) -> dict | None:
    path = root / name
    if not path.exists():
        if name == "plugin.json":
            fail(path, "missing")
        return None
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        fail(path, f"invalid JSON: {error}")
        return None
    if not isinstance(document, dict):
        fail(path, "expected a JSON object")
        return None
    schema_url = document.get("$schema", "")
    try:
        with urllib.request.urlopen(schema_url, timeout=20) as response:
            schema = json.load(response)
        jsonschema.validators.validator_for(schema)(schema).validate(document)
    except jsonschema.ValidationError as error:
        fail(path, f"schema violation: {error.message}")
    except Exception as error:
        fail(path, f"schema {schema_url!r} could not be checked: {error}")
    for value in strings(document):
        if ABSOLUTE.match(value):
            fail(path, f"absolute path {value!r}")
    return document


def check_marketplace(plugin: dict):
    path = root / ".github/plugin/marketplace.json"
    try:
        marketplace = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        fail(path, "missing")
        return
    except json.JSONDecodeError as error:
        fail(path, f"invalid JSON: {error}")
        return
    schema = {
        "type": "object",
        "required": ["name", "owner", "plugins"],
        "properties": {
            "name": {
                "type": "string",
                "maxLength": 64,
                "pattern": "^[a-z0-9]+(?:-[a-z0-9]+)*$",
            },
            "owner": {
                "type": "object",
                "required": ["name"],
                "properties": {"name": {"type": "string", "minLength": 1}},
            },
            "plugins": {"const": [{"name": plugin.get("name"), "source": "./"}]},
        },
    }
    try:
        jsonschema.validate(marketplace, schema)
    except jsonschema.ValidationError as error:
        fail(path, f"marketplace contract violation: {error.message}")


def frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(path, "no frontmatter")
        return None
    try:
        data = yaml.safe_load(text.split("---\n", 2)[1])
    except yaml.YAMLError as error:
        fail(path, f"invalid frontmatter: {error}")
        return None
    return data if isinstance(data, dict) else {}


plugin = check_manifest("plugin.json")
mcp = check_manifest("mcp.json")
plugin_version = (
    re.search(r"/schemas/([^/]+)/", plugin.get("$schema", "")) if plugin else None
)
mcp_version = re.search(r"/schemas/([^/]+)/", mcp.get("$schema", "")) if mcp else None
if mcp_version and plugin_version and mcp_version[1] != plugin_version[1]:
    fail(
        root / "mcp.json",
        f"schema version {mcp_version[1]} differs from plugin.json {plugin_version[1]}",
    )
if plugin is not None:
    check_marketplace(plugin)

for skill in sorted((root / "skills").glob("*/SKILL.md")):
    data = frontmatter(skill)
    if data is None:
        continue
    name, description = data.get("name", ""), data.get("description", "")
    if name != skill.parent.name or not SKILL_NAME.match(str(name)):
        fail(
            skill,
            f"name {name!r} must equal the folder name and meet the skill name rule",
        )
    if not 1 <= len(str(description)) <= 1024:
        fail(skill, "description must have 1 to 1024 characters")

for folder, suffix in SUFFIXES.items():
    for path in sorted((root / "com.github.copilot" / folder).glob("*")):
        if not path.name.endswith(suffix):
            fail(path, f"expected the suffix {suffix}")
        else:
            frontmatter(path)

for entry in PAYLOAD:
    base = root / entry
    paths = (
        [base] if base.is_file() else sorted(base.rglob("*")) if base.is_dir() else []
    )
    for path in paths:
        if path.is_symlink() and not path.resolve().is_relative_to(root):
            fail(path, "symlink leaves the plugin root")
        if path.suffix != ".md" or not path.is_file():
            continue
        prose = CODE.sub("", path.read_text(encoding="utf-8"))
        for target in LINK.findall(prose):
            if re.match(r"^[a-z]+:|^#", target):
                continue
            resolved = (path.parent / target.split("#")[0]).resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                fail(path, f"link {target!r} does not resolve inside the plugin root")

print("\n".join(failures) if failures else "ok")
sys.exit(1 if failures else 0)
