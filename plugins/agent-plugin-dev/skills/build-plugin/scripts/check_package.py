# /// script
# requires-python = ">=3.11"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Check the static structure of this Agent Plugins 1.0 marketplace."""

import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml

CANONICAL_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
CANONICAL_MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
PLUGIN_NAME = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
LEGACY_MANIFEST_FIELDS = {"agents", "skills", "mcpServers"}
LEGACY_PACKAGE_PATHS = {
    ".mcp.json",
    "agents",
    "rules",
    "commands",
    "hooks",
    "hooks.json",
    "mcpServers",
}
LEGACY_REPOSITORY_PATHS = {
    "plugin.json",
    ".mcp.json",
    "agents",
    "rules",
    "skills",
    "commands",
    "hooks",
    "mcpServers",
}
MANIFEST_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
AUTHOR_FIELDS = {"name", "email", "url"}
MAX_ERRORS = 50
MAX_MESSAGE_LENGTH = 240
MARKDOWN_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)")
MARKDOWN_CODE = re.compile(r"(?ms)^(`{3,}|~{3,}).*?^\1[ \t]*$|`[^`\n]*`")
URL_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def _object_without_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


class PackageChecker:
    def __init__(self, repository_root: Path):
        self.root = repository_root.resolve()
        self.errors = []
        self.error_count = 0
        self.expected_manifests = set()
        self.packages = []

    def fail(self, path: Path, message: str) -> None:
        self.error_count += 1
        if len(self.errors) >= MAX_ERRORS:
            return
        try:
            display_path = path.relative_to(self.root).as_posix()
        except ValueError:
            display_path = path.name or "."
        message = " ".join(message.split())
        if len(message) > MAX_MESSAGE_LENGTH:
            message = message[: MAX_MESSAGE_LENGTH - 3] + "..."
        self.errors.append(f"{display_path}: {message}")

    def read_json(self, path: Path):
        try:
            return json.loads(
                path.read_text(encoding="utf-8"),
                object_pairs_hook=_object_without_duplicate_keys,
            )
        except FileNotFoundError:
            self.fail(path, "missing JSON file")
        except (OSError, UnicodeError):
            self.fail(path, "cannot read UTF-8 JSON file")
        except json.JSONDecodeError:
            self.fail(path, "invalid JSON syntax")
        except ValueError as error:
            self.fail(path, str(error))
        return None

    def check_root_layout(self) -> None:
        for name in sorted(LEGACY_REPOSITORY_PATHS):
            path = self.root / name
            if path.exists() or path.is_symlink():
                self.fail(
                    path,
                    "repository-root component layout is not a plugin package; "
                    "place components inside plugins/<name>/",
                )

    def valid_name(self, value) -> bool:
        return (
            isinstance(value, str)
            and 1 <= len(value) <= 64
            and PLUGIN_NAME.fullmatch(value) is not None
        )

    def validate_manifest(self, package_root: Path, expected_name: str):
        path = package_root / "plugin.json"
        if not path.is_file():
            self.fail(path, "missing root plugin.json")
            return None
        document = self.read_json(path)
        if not isinstance(document, dict):
            self.fail(path, "manifest must be a JSON object")
            return None

        for field in document.keys() - MANIFEST_FIELDS:
            if field in LEGACY_MANIFEST_FIELDS:
                self.fail(
                    path,
                    f"legacy manifest path field {field!r}; Agent Plugins 1.0 "
                    "uses fixed component locations",
                )
            else:
                self.fail(path, f"unknown manifest field {field!r}")

        for field in ("$schema", "name"):
            if field not in document:
                self.fail(path, f"missing required manifest field {field!r}")

        if "$schema" in document and document["$schema"] != CANONICAL_SCHEMA:
            self.fail(path, f"$schema must be {CANONICAL_SCHEMA}")

        manifest_name = document.get("name")
        if not self.valid_name(manifest_name):
            self.fail(
                path,
                "name must be 1-64 lowercase ASCII letters, digits, hyphens, "
                "or periods; it must start/end alphanumeric and cannot contain "
                "'--' or '..'",
            )
        elif manifest_name != expected_name:
            self.fail(
                path,
                f"manifest name {manifest_name!r} does not match catalog and "
                f"directory name {expected_name!r}",
            )

        for field in ("version", "description", "homepage", "repository", "license"):
            if field in document and not isinstance(document[field], str):
                self.fail(path, f"{field!r} must be a string")

        author = document.get("author")
        if "author" in document:
            if not isinstance(author, dict):
                self.fail(path, "'author' must be an object")
            else:
                for field in author.keys() - AUTHOR_FIELDS:
                    self.fail(path, f"unknown author field {field!r}")
                for field, value in author.items():
                    if field in AUTHOR_FIELDS and not isinstance(value, str):
                        self.fail(path, f"'author.{field}' must be a string")

        keywords = document.get("keywords")
        if "keywords" in document:
            if not isinstance(keywords, list):
                self.fail(path, "'keywords' must be an array of strings")
            elif any(not isinstance(keyword, str) for keyword in keywords):
                self.fail(path, "every 'keywords' item must be a string")

        extensions = document.get("extensions")
        if "extensions" in document:
            if not isinstance(extensions, dict):
                self.fail(path, "'extensions' must be an object")
            else:
                for namespace, value in extensions.items():
                    if not isinstance(value, dict):
                        self.fail(
                            path,
                            f"extension {namespace!r} must contain an object",
                        )
        return document

    def check_catalog(self) -> None:
        catalog_path = self.root / ".github/plugin/marketplace.json"
        catalog = self.read_json(catalog_path)
        if not isinstance(catalog, dict):
            self.fail(catalog_path, "marketplace must be a JSON object")
            return
        if "name" not in catalog:
            self.fail(catalog_path, "missing required marketplace field 'name'")
        elif not self.valid_name(catalog["name"]):
            self.fail(catalog_path, "'name' must be a valid marketplace name")
        owner = catalog.get("owner")
        if not isinstance(owner, dict):
            self.fail(catalog_path, "'owner' must be an object")
        elif not isinstance(owner.get("name"), str) or not owner["name"].strip():
            self.fail(catalog_path, "'owner.name' must be a non-empty string")
        entries = catalog.get("plugins")
        if not isinstance(entries, list):
            self.fail(
                catalog_path, "'plugins' must be a non-empty array"
            )
            return
        if not entries:
            self.fail(catalog_path, "'plugins' must be a non-empty array")
            return

        seen = set()
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                self.fail(catalog_path, f"plugins[{index}] must be an object")
                continue
            name = entry.get("name")
            if not self.valid_name(name):
                self.fail(
                    catalog_path, f"plugins[{index}].name is not a valid plugin name"
                )
                continue
            if name in seen:
                self.fail(catalog_path, f"duplicate plugin name {name!r}")
                continue
            seen.add(name)

            expected_source = f"./plugins/{name}"
            source = entry.get("source")
            if not isinstance(source, str):
                self.fail(catalog_path, f"plugins[{index}].source must be a string")
                continue
            if source != expected_source:
                self.fail(
                    catalog_path,
                    f"plugins[{index}].source must be {expected_source!r}; "
                    "sources are relative to the repository root",
                )
                continue

            package_root = self.root / "plugins" / name
            if not package_root.is_dir():
                self.fail(package_root, "catalog package directory is missing")
                continue
            if package_root.is_symlink():
                self.fail(package_root, "package directory must not be a symbolic link")
                continue
            plugins_root = self.root / "plugins"
            try:
                package_real = package_root.resolve(strict=True)
                plugins_real = plugins_root.resolve(strict=True)
            except (OSError, RuntimeError):
                self.fail(package_root, "cannot resolve package directory")
                continue
            if not plugins_real.is_relative_to(self.root):
                self.fail(plugins_root, "plugins directory escapes the repository root")
                continue
            if not package_real.is_relative_to(plugins_real):
                self.fail(package_root, "package directory escapes plugins/")
                continue
            if not self.check_package_symlinks(package_root):
                continue

            manifest_path = package_root / "plugin.json"
            self.expected_manifests.add(manifest_path)
            manifest = self.validate_manifest(package_root, name)
            if manifest is not None:
                self.packages.append((name, package_root))
            self.check_package_layout(package_root)
            self.check_package_links(package_root)

    def check_package_layout(self, package_root: Path) -> None:
        for name in sorted(LEGACY_PACKAGE_PATHS):
            path = package_root / name
            if path.exists() or path.is_symlink():
                self.fail(
                    path,
                    "legacy component path; Agent Plugins 1.0 uses skills/, "
                    "mcp.json, and com.github.copilot/",
                )

        for name in ("skills", "com.github.copilot"):
            path = package_root / name
            if (path.exists() or path.is_symlink()) and not path.is_dir():
                self.fail(path, "expected a directory")

        for name in ("agents", "rules", "commands", "hooks"):
            path = package_root / "com.github.copilot" / name
            if (path.exists() or path.is_symlink()) and not path.is_dir():
                self.fail(path, "expected a directory")

        skills_root = package_root / "skills"
        if skills_root.is_dir():
            try:
                children = sorted(skills_root.iterdir())
            except OSError:
                self.fail(skills_root, "cannot read skills directory")
                children = []
            for child in children:
                if not child.is_dir():
                    self.fail(child, "skills/ may contain only skill directories")
                elif not (child / "SKILL.md").is_file():
                    self.fail(child / "SKILL.md", "each skill directory needs SKILL.md")

        mcp_path = package_root / "mcp.json"
        if mcp_path.exists() or mcp_path.is_symlink():
            if not mcp_path.is_file():
                self.fail(mcp_path, "expected a JSON file")
            else:
                self.check_mcp(mcp_path, package_root)

    def check_mcp(self, path: Path, package_root: Path) -> None:
        document = self.read_json(path)
        if not isinstance(document, dict):
            self.fail(path, "MCP configuration must be a JSON object")
            return
        for field in document.keys() - {"$schema", "mcpServers"}:
            self.fail(path, f"unknown MCP configuration field {field!r}")
        if "$schema" not in document:
            self.fail(path, "missing required MCP field '$schema'")
        elif document["$schema"] != CANONICAL_MCP_SCHEMA:
            self.fail(path, f"$schema must be {CANONICAL_MCP_SCHEMA}")
        servers = document.get("mcpServers")
        if not isinstance(servers, dict):
            self.fail(path, "'mcpServers' must be an object")
            return

        for name, server in servers.items():
            label = f"server {name!r}"
            if not isinstance(server, dict):
                self.fail(path, f"{label} must be an object")
                continue
            transport = server.get("type")
            if not isinstance(transport, str) or transport not in {
                "stdio",
                "streamable-http",
                "sse",
            }:
                self.fail(path, f"{label} needs type stdio, streamable-http, or sse")
                continue
            allowed = {"type", "command", "args", "env", "cwd"}
            required = {"type", "command"}
            if transport != "stdio":
                allowed = {"type", "url", "headers"}
                required = {"type", "url"}
            for field in server.keys() - allowed:
                self.fail(path, f"{label} has unsupported field {field!r}")
            for field in required - server.keys():
                self.fail(path, f"{label} is missing {field!r}")
            for field in ("command", "url", "cwd"):
                if field in server and not isinstance(server[field], str):
                    self.fail(path, f"{label} field {field!r} must be a string")
            for field in ("command", "url"):
                if (
                    field in server
                    and isinstance(server[field], str)
                    and not server[field]
                ):
                    self.fail(path, f"{label} field {field!r} must not be empty")
            if "args" in server and (
                not isinstance(server["args"], list)
                or any(not isinstance(arg, str) for arg in server["args"])
            ):
                self.fail(path, f"{label} field 'args' must be an array of strings")
            for field in ("env", "headers"):
                mapping = server.get(field)
                if field in server and (
                    not isinstance(mapping, dict)
                    or any(not isinstance(value, str) for value in mapping.values())
                ):
                    self.fail(
                        path, f"{label} field {field!r} must map strings to strings"
                    )
                if field == "env" and isinstance(mapping, dict):
                    for reserved in {"PLUGIN_ROOT", "PLUGIN_DATA"} & mapping.keys():
                        self.fail(
                            path,
                            f"{label} cannot override reserved environment key {reserved!r}",
                        )
            if transport == "stdio" and isinstance(server.get("command"), str):
                command = server["command"]
                if not command or any(character.isspace() for character in command):
                    self.fail(path, f"{label} command must be one executable token")
                if command.startswith("./"):
                    self.check_component_path(
                        path, package_root, command[2:], f"{label} command"
                    )
                elif "/" in command or "\\" in command or command in {".", ".."}:
                    self.fail(
                        path,
                        f"{label} command must be a bare executable or a package-relative ./ path",
                    )
            cwd = server.get("cwd")
            if isinstance(cwd, str):
                if cwd == "${PLUGIN_ROOT}":
                    cwd = "."
                elif cwd.startswith("${PLUGIN_ROOT}/"):
                    cwd = cwd[len("${PLUGIN_ROOT}/") :]
                    cwd = cwd or "."
                elif cwd.startswith("${PLUGIN_ROOT}"):
                    self.fail(path, f"{label} cwd must use a complete PLUGIN_ROOT path")
                    continue
                if cwd == "${PLUGIN_DATA}":
                    continue
                if cwd.startswith("${PLUGIN_DATA}/"):
                    data_path = cwd[len("${PLUGIN_DATA}/") :]
                    if data_path and not self.relative_path_stays_within(data_path):
                        self.fail(path, f"{label} cwd escapes PLUGIN_DATA")
                    continue
                if cwd.startswith("${PLUGIN_DATA}"):
                    self.fail(path, f"{label} cwd must use a complete PLUGIN_DATA path")
                    continue
                if cwd == "./":
                    cwd = "."
                elif cwd.startswith("./"):
                    cwd = cwd[2:]
                else:
                    self.fail(
                        path,
                        f"{label} cwd must start with ./, ${{PLUGIN_ROOT}}, or ${{PLUGIN_DATA}}",
                    )
                    continue
                self.check_component_path(path, package_root, cwd, f"{label} cwd")

    def relative_path_stays_within(self, value: str) -> bool:
        if not value or Path(value).is_absolute() or "\\" in value:
            return False
        depth = 0
        for part in Path(value).parts:
            if part == "..":
                depth -= 1
                if depth < 0:
                    return False
            elif part not in {"", "."}:
                depth += 1
        return True

    def check_component_path(
        self, source_path: Path, package_root: Path, value: str, label: str
    ) -> None:
        if not self.relative_path_stays_within(value):
            self.fail(source_path, f"{label} must stay inside the plugin directory")
            return
        target = (package_root / value).resolve()
        if not target.is_relative_to(package_root.resolve()):
            self.fail(source_path, f"{label} escapes the plugin directory")

    def check_package_symlinks(self, package_root: Path) -> bool:
        safe = True
        try:
            package_real = package_root.resolve(strict=True)
            for path in package_root.rglob("*"):
                if not path.is_symlink():
                    continue
                try:
                    target = path.resolve(strict=True)
                except (OSError, RuntimeError):
                    self.fail(path, "symbolic link is dangling or cannot be resolved")
                    safe = False
                    continue
                if not target.is_relative_to(package_real):
                    self.fail(path, "symbolic link escapes the plugin directory")
                    safe = False
        except (OSError, RuntimeError):
            self.fail(package_root, "cannot inspect package paths")
            return False
        return safe

    def check_package_links(self, package_root: Path) -> None:
        package_real = package_root.resolve()
        for path in package_root.rglob("*.md"):
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except (OSError, UnicodeError):
                self.fail(path, "cannot read Markdown file as UTF-8")
                continue
            content = MARKDOWN_CODE.sub("", content)
            for match in MARKDOWN_LINK.finditer(content):
                destination = unquote(match.group(1).removeprefix("<").removesuffix(">"))
                if "\x00" in destination:
                    self.fail(path, "link destination contains a NUL byte")
                    continue
                if (
                    not destination
                    or destination.startswith("#")
                    or URL_SCHEME.match(destination)
                ):
                    continue
                target_text = destination.split("#", 1)[0].split("?", 1)[0]
                if not target_text:
                    continue
                if Path(target_text).is_absolute() or re.match(
                    r"^[A-Za-z]:[\\/]", target_text
                ):
                    self.fail(
                        path, f"link {destination!r} is not a package-relative path"
                    )
                    continue
                try:
                    target = (path.parent / target_text).resolve()
                    if not target.is_relative_to(package_real):
                        self.fail(
                            path,
                            f"link {destination!r} does not resolve inside the package",
                        )
                        continue
                    target.stat()
                    exists = True
                except FileNotFoundError:
                    exists = False
                except (OSError, ValueError, RuntimeError):
                    self.fail(
                        path,
                        "cannot check link destination; shorten or correct its path",
                    )
                    continue
                if not exists:
                    self.fail(
                        path,
                        f"link {destination!r} does not resolve inside the package",
                    )

    def check_unlisted_manifests(self) -> None:
        plugins_root = self.root / "plugins"
        if not plugins_root.exists() and not plugins_root.is_symlink():
            return
        if not plugins_root.is_dir():
            self.fail(plugins_root, "expected a directory")
            return
        try:
            plugins_real = plugins_root.resolve(strict=True)
        except (OSError, RuntimeError):
            self.fail(plugins_root, "cannot resolve plugins directory")
            return
        if not plugins_real.is_relative_to(self.root):
            self.fail(plugins_root, "plugins directory escapes the repository root")
            return

        for current, directories, filenames in os.walk(plugins_root, followlinks=False):
            current_path = Path(current)
            if "plugin.json" in filenames:
                manifest_path = current_path / "plugin.json"
                if manifest_path not in self.expected_manifests:
                    self.fail(
                        manifest_path,
                        "unlisted package manifest; add a matching marketplace entry",
                    )
            for directory in list(directories):
                child = current_path / directory
                if child.is_symlink():
                    try:
                        target = child.resolve(strict=True)
                    except (OSError, RuntimeError):
                        self.fail(
                            child, "symbolic link is dangling or cannot be resolved"
                        )
                        directories.remove(directory)
                        continue
                    if not target.is_relative_to(plugins_real):
                        self.fail(child, "symbolic link escapes plugins/")
                    directories.remove(directory)

    def read_frontmatter(self, path: Path):
        try:
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---\n"):
                raise ValueError("missing frontmatter")
            header, body = text[4:].split("\n---\n", 1)
            metadata = yaml.safe_load(header)
            if not isinstance(metadata, dict):
                raise ValueError("frontmatter must be a mapping")
            return metadata, body
        except (OSError, UnicodeError, ValueError, yaml.YAMLError):
            self.fail(path, "expected readable Markdown with YAML mapping frontmatter")
            return None, ""

    def check_component_identities(self):
        owners = {}
        for package_name, package_root in self.packages:
            identities = []
            for path in (package_root / "skills").glob("*/SKILL.md"):
                metadata, body = self.read_frontmatter(path)
                if metadata is not None:
                    if metadata.get("name") != path.parent.name:
                        self.fail(path, "skill name must match its folder")
                    identities.append(("skill", path.parent.name, path))
            for path in (package_root / "com.github.copilot/agents").glob("*.agent.md"):
                metadata, body = self.read_frontmatter(path)
                if metadata is not None:
                    name = metadata.get("name", path.name.removesuffix(".agent.md"))
                    if not isinstance(name, str) or not name:
                        self.fail(path, "agent name must be a non-empty string")
                    else:
                        identities.append(("agent", name, path))
            for path in (package_root / "com.github.copilot/rules").glob("*.instructions.md"):
                identities.append(("rule", path.name, path))
            mcp_path = package_root / "mcp.json"
            if mcp_path.is_file():
                document = self.read_json(mcp_path)
                servers = document.get("mcpServers", {}) if isinstance(document, dict) else {}
                if isinstance(servers, dict):
                    identities.extend(("MCP server", name, mcp_path) for name in servers)
            for kind, name, path in identities:
                key = (kind, name)
                if key in owners and owners[key] != package_name:
                    self.fail(path, f"duplicate {kind} identity {name!r} in {owners[key]!r}")
                owners[key] = package_name

    def check_repository_pointers(self):
        directory = self.root / ".github/skills"
        if not directory.exists():
            return
        canonical_skills = {}
        for package_name, package_root in self.packages:
            for target in (package_root / "skills").glob("*/SKILL.md"):
                canonical_skills[target.resolve()] = target
        represented = set()
        pointer_names = set()
        for folder in directory.iterdir():
            pointer = folder / "SKILL.md"
            if not folder.is_dir() or folder.is_symlink() or pointer.is_symlink() or set(folder.iterdir()) != {pointer}:
                self.fail(folder, "repository skill must contain only its pointer SKILL.md")
                continue
            metadata, body = self.read_frontmatter(pointer)
            match = re.fullmatch(r"\[[^\]\n]+\]\(([^)\n]+)\)\s*", body.strip())
            if metadata is None or match is None:
                self.fail(pointer, "pointer body must contain exactly one canonical skill link")
                continue
            destination = unquote(match.group(1))
            if Path(destination).is_absolute() or URL_SCHEME.match(destination):
                self.fail(pointer, "pointer target must be a repository-relative canonical skill")
                continue
            try:
                resolved = (folder / destination).resolve(strict=True)
            except (OSError, ValueError, RuntimeError):
                self.fail(pointer, "canonical pointer target does not exist")
                continue
            target = canonical_skills.get(resolved)
            if target is None or target.parent.name != folder.name:
                self.fail(pointer, "pointer target must be the matching catalog package skill")
                continue
            canonical, unused_body = self.read_frontmatter(target)
            if canonical is None:
                continue
            fields = ("name", "description", "argument-hint", "disable-model-invocation")
            expected_metadata = {key: canonical[key] for key in fields if key in canonical}
            if metadata != expected_metadata or any(
                type(metadata[key]) is not type(expected_metadata[key])
                for key in metadata.keys() & expected_metadata.keys()
            ):
                self.fail(pointer, "pointer frontmatter must match canonical discovery fields")
            represented.add(target.parents[1])
            pointer_names.add(folder.name)
        for skills_root in represented:
            expected = {path.parent.name for path in skills_root.glob("*/SKILL.md")}
            if not expected.issubset(pointer_names):
                self.fail(directory, "missing canonical skill pointers")

    def run(self):
        self.check_root_layout()
        self.check_catalog()
        self.check_unlisted_manifests()
        self.check_component_identities()
        self.check_repository_pointers()
        if self.error_count > MAX_ERRORS:
            self.errors.append(
                f"...: {self.error_count - MAX_ERRORS} additional problems omitted"
            )
        return self.errors


def check_repository(repository_root: Path):
    return PackageChecker(repository_root).run()


def main(argv=None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if len(arguments) > 1:
        print("usage: check_package.py [repository-root]", file=sys.stderr)
        return 2
    repository_root = Path(arguments[0]) if arguments else Path.cwd()
    errors = check_repository(repository_root)
    if errors:
        print("\n".join(errors))
        return 1
    print("ok: static scaffold checks passed; client installation/runtime not tested")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
