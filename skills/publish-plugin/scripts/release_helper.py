# /// script
# requires-python = ">=3.11"
# ///
"""Provide read-only preflight and notes for one marketplace plugin release."""

import json
import re
import subprocess
import sys
from pathlib import Path

PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
CHANGELOG_HEADER = re.compile(r"^## \[([^\]]+)\](?: - \d{4}-\d{2}-\d{2})?$")


def fail(message: str, code: int = 1) -> int:
    print(f"FAIL: {message}", file=sys.stderr)
    return code


def run_git(root: Path | None, *arguments: str) -> subprocess.CompletedProcess:
    command = ["git"]
    if root is not None:
        command.extend(("-C", str(root)))
    command.extend(arguments)
    return subprocess.run(command, capture_output=True, text=True, check=False)


def find_repository_root() -> Path | None:
    result = run_git(None, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def require_clean_main(root: Path) -> str | None:
    branch = run_git(root, "branch", "--show-current")
    if branch.returncode != 0:
        return "cannot determine the current Git branch"
    if branch.stdout.strip() != "main":
        return "publishing requires the current branch to be main"

    head = run_git(root, "rev-parse", "--verify", "HEAD^{commit}")
    if head.returncode != 0:
        return "no committed state exists; HEAD must identify a commit"

    status = run_git(
        root,
        "--no-optional-locks",
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--ignore-submodules=none",
    )
    if status.returncode != 0:
        return "cannot read Git worktree status"
    if status.stdout:
        return "working tree is dirty; commit or resolve all changes before release"
    tracking_ref = run_git(
        root, "rev-parse", "--verify", "refs/remotes/origin/main^{commit}"
    )
    if tracking_ref.returncode != 0:
        return (
            "cached refs/remotes/origin/main is missing or does not resolve to a commit; "
            "obtain owner-authorized remote refresh/review, then rerun preflight"
        )
    if tracking_ref.stdout.strip() != head.stdout.strip():
        return (
            "main HEAD differs from cached refs/remotes/origin/main; reconcile committed "
            "main with the reviewed tracking ref before release"
        )
    return None


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, f"{path.name} is missing"
    except (OSError, UnicodeError):
        return None, f"{path.name} cannot be read as UTF-8 JSON"
    except json.JSONDecodeError:
        return None, f"{path.name} contains invalid JSON"


def package_path(root: Path, name: str) -> tuple[Path | None, str | None]:
    plugins_root = root / "plugins"
    package_root = plugins_root / name
    if not package_root.is_dir():
        return None, f"listed plugin directory plugins/{name} is missing"
    if package_root.is_symlink():
        return None, f"plugins/{name} must not be a symbolic link"
    try:
        plugins_real = plugins_root.resolve(strict=True)
        package_real = package_root.resolve(strict=True)
    except (OSError, RuntimeError):
        return None, f"plugins/{name} cannot be resolved"
    if not plugins_real.is_relative_to(root):
        return None, "plugins directory escapes the repository root"
    if not package_real.is_relative_to(plugins_real):
        return None, f"plugins/{name} escapes plugins/"
    return package_root, None


def extract_notes(changelog: str, version: str) -> str | None:
    lines = changelog.splitlines()
    matches = []
    for index, line in enumerate(lines):
        match = CHANGELOG_HEADER.fullmatch(line)
        if match and match.group(1) == version:
            matches.append(index)
    if len(matches) != 1:
        return None
    start = matches[0] + 1
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    notes = "\n".join(lines[start:end]).strip()
    return notes or None


def inspect_plugin(root: Path, name: str) -> tuple[dict | None, str | None]:
    catalog_path = root / ".github/plugin/marketplace.json"
    catalog, problem = read_json(catalog_path)
    if problem:
        return None, f".github/plugin/marketplace.json: {problem}"
    if not isinstance(catalog, dict) or not isinstance(catalog.get("plugins"), list):
        return None, "marketplace catalog must contain a plugins array"
    entries = catalog["plugins"]
    if not entries:
        return None, "marketplace catalog is empty; no plugin is available to publish"

    matches = [
        entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("name") == name
    ]
    if not matches:
        return None, f"plugin {name!r} is not listed in the marketplace catalog"
    if len(matches) != 1:
        return (
            None,
            f"plugin {name!r} appears more than once in the marketplace catalog",
        )
    if matches[0].get("source") != f"./plugins/{name}":
        return None, f"catalog source for {name!r} must be './plugins/{name}'"

    package_root, problem = package_path(root, name)
    if problem:
        return None, problem
    manifest_path = package_root / "plugin.json"
    manifest_real = manifest_path.resolve()
    if not manifest_real.is_relative_to(package_root.resolve()):
        return None, f"plugins/{name}/plugin.json escapes the plugin directory"
    manifest, problem = read_json(manifest_path)
    if problem:
        return None, f"plugins/{name}/plugin.json: {problem}"
    if not isinstance(manifest, dict):
        return None, f"plugins/{name}/plugin.json must be a JSON object"
    if manifest.get("$schema") != SCHEMA:
        return (
            None,
            f"plugins/{name}/plugin.json must declare the Agent Plugins 1.0 schema",
        )
    if manifest.get("name") != name:
        return None, f"manifest name must match catalog and directory name {name!r}"

    version = manifest.get("version")
    if not isinstance(version, str) or not SEMVER.fullmatch(version):
        return (
            None,
            "release policy requires plugin.json version in MAJOR.MINOR.PATCH form",
        )

    changelog_path = package_root / "CHANGELOG.md"
    changelog_real = changelog_path.resolve()
    if not changelog_real.is_relative_to(package_root.resolve()):
        return None, f"plugins/{name}/CHANGELOG.md escapes the plugin directory"
    try:
        changelog = changelog_path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None, f"plugins/{name}/CHANGELOG.md is missing"
    except (OSError, UnicodeError):
        return None, f"plugins/{name}/CHANGELOG.md cannot be read as UTF-8"
    notes = extract_notes(changelog, version)
    if notes is None:
        return (
            None,
            f"plugins/{name}/CHANGELOG.md needs one non-empty ## [{version}] entry",
        )

    tag = f"{name}/v{version}"
    ref = f"refs/tags/{tag}"
    if run_git(root, "check-ref-format", ref).returncode != 0:
        return None, f"release tag {tag!r} is not a valid Git ref"
    existing_tag = run_git(root, "show-ref", "--verify", "--quiet", ref)
    if existing_tag.returncode == 0:
        return None, f"release tag {tag!r} already exists locally"
    if existing_tag.returncode not in (1,):
        return None, "cannot check whether the release tag already exists"

    return {"name": name, "version": version, "tag": tag, "notes": notes}, None


def main(arguments=None) -> int:
    arguments = sys.argv[1:] if arguments is None else arguments
    if len(arguments) != 2 or arguments[0] not in {"preflight", "notes"}:
        return fail(
            "select one plugin: usage release.sh preflight <plugin-name> | "
            "release.sh notes <plugin-name>; all-plugin releases are not supported",
            2,
        )
    action, name = arguments
    if name == "all":
        return fail(
            "select one catalog plugin; all-plugin releases are not supported", 2
        )
    if (
        not isinstance(name, str)
        or not 1 <= len(name) <= 64
        or not PLUGIN_NAME.fullmatch(name)
    ):
        return fail("plugin name must be a valid catalog name", 2)

    root = find_repository_root()
    if root is None:
        return fail("run this helper from inside a Git repository")
    problem = require_clean_main(root)
    if problem:
        return fail(problem)
    selected, problem = inspect_plugin(root, name)
    if problem:
        return fail(problem)
    if action == "preflight":
        print(
            f"ok: selected {selected['name']}@{selected['version']}; "
            f"local tag {selected['tag']} is available; main matches cached "
            "refs/remotes/origin/main; read-only preflight"
        )
        return 0
    print(selected["notes"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
