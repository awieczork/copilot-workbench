"""Regression tests for the static Agent Plugins marketplace checker."""

import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts/check_package.py"
SPEC = importlib.util.spec_from_file_location("check_package", SCRIPT)
check_package = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = check_package
SPEC.loader.exec_module(check_package)

SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"


class PackageCheckerTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name) / "repository"
        (self.root / ".github/plugin").mkdir(parents=True)

    def tearDown(self):
        self.temporary_directory.cleanup()

    def write_catalog(self, entries):
        path = self.root / ".github/plugin/marketplace.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "name": "ds-tools",
                    "owner": {"name": "Test owner"},
                    "plugins": entries,
                }
            ),
            encoding="utf-8",
        )

    def write_package(self, name, manifest_updates=None):
        package_root = self.root / "plugins" / name
        package_root.mkdir(parents=True, exist_ok=True)
        manifest = {"$schema": SCHEMA, "name": name}
        manifest.update(manifest_updates or {})
        (package_root / "plugin.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        return package_root

    def entry(self, name):
        return {"name": name, "source": f"./plugins/{name}"}

    def errors(self):
        return check_package.check_repository(self.root)

    def test_empty_catalog_is_a_valid_static_scaffold(self):
        self.write_catalog([])

        self.assertEqual(self.errors(), [])

    def test_catalog_name_and_owner_are_required_and_validated(self):
        invalid_catalogs = (
            (
                {"owner": {"name": "Test owner"}, "plugins": []},
                "required marketplace field",
            ),
            (
                {"name": 5, "owner": {"name": "Test owner"}, "plugins": []},
                "marketplace name",
            ),
            (
                {"name": "", "owner": {"name": "Test owner"}, "plugins": []},
                "marketplace name",
            ),
            (
                {"name": "bad_name", "owner": {"name": "Test owner"}, "plugins": []},
                "marketplace name",
            ),
            ({"name": "ds-tools", "plugins": []}, "owner"),
            ({"name": "ds-tools", "owner": "Test owner", "plugins": []}, "owner"),
            ({"name": "ds-tools", "owner": {}, "plugins": []}, "owner.name"),
            ({"name": "ds-tools", "owner": {"name": 5}, "plugins": []}, "owner.name"),
            (
                {"name": "ds-tools", "owner": {"name": "  "}, "plugins": []},
                "owner.name",
            ),
        )
        catalog_path = self.root / ".github/plugin/marketplace.json"

        for document, expected_error in invalid_catalogs:
            with self.subTest(document=document):
                catalog_path.write_text(json.dumps(document), encoding="utf-8")

                errors = self.errors()

                self.assertTrue(
                    any(expected_error in error for error in errors), errors
                )

    def test_two_independent_agent_plugins_are_valid(self):
        first = self.write_package("first-plugin", {"version": "1.2.3"})
        second = self.write_package("second.plugin", {"description": "Second"})
        (first / "skills/checker").mkdir(parents=True)
        (first / "skills/checker/SKILL.md").write_text("# Checker\n", encoding="utf-8")
        (second / "mcp.json").write_text(
            json.dumps(
                {
                    "$schema": MCP_SCHEMA,
                    "mcpServers": {
                        "local": {
                            "type": "stdio",
                            "command": "uv",
                            "cwd": "${PLUGIN_DATA}/cache",
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        self.write_catalog([self.entry("first-plugin"), self.entry("second.plugin")])

        self.assertEqual(self.errors(), [])

    def test_duplicate_catalog_names_and_manifest_name_mismatch_fail(self):
        self.write_package("plugin-one")
        self.write_catalog([self.entry("plugin-one"), self.entry("plugin-one")])
        self.assertTrue(
            any("duplicate plugin name" in error for error in self.errors())
        )

        self.write_package("plugin-one", {"name": "plugin-two"})
        self.write_catalog([self.entry("plugin-one")])
        self.assertTrue(
            any("does not match catalog" in error for error in self.errors())
        )

    def test_traversal_source_and_external_component_symlink_fail(self):
        package = self.write_package("plugin-one")
        self.write_catalog([{"name": "plugin-one", "source": "../outside"}])
        self.assertTrue(any("source must be" in error for error in self.errors()))

        outside = Path(self.temporary_directory.name) / "outside"
        outside.mkdir()
        skills = package / "skills"
        skills.mkdir()
        try:
            os.symlink(outside, skills / "outside", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symbolic links are unavailable: {error}")
        self.write_catalog([self.entry("plugin-one")])
        self.assertTrue(
            any("symbolic link escapes" in error for error in self.errors())
        )

    def test_listed_package_directory_cannot_be_a_symlink_alias(self):
        self.write_package("real-plugin")
        alias = self.root / "plugins/alias-plugin"
        try:
            alias.symlink_to("real-plugin", target_is_directory=True)
        except OSError as error:
            self.skipTest(f"symbolic links are unavailable: {error}")
        self.write_catalog([self.entry("alias-plugin")])

        self.assertTrue(
            any(
                "package directory must not be a symbolic link" in error
                for error in self.errors()
            )
        )

    def test_legacy_manifest_fields_and_paths_fail(self):
        package = self.write_package("plugin-one", {"skills": ["skills"]})
        (package / ".mcp.json").write_text("{}", encoding="utf-8")
        (package / "agents").mkdir()
        (package / "hooks.json").write_text("{}", encoding="utf-8")
        self.write_catalog([self.entry("plugin-one")])

        errors = self.errors()
        self.assertTrue(
            any("legacy manifest path field 'skills'" in error for error in errors)
        )
        self.assertTrue(
            any(
                ".mcp.json" in error and "legacy component path" in error
                for error in errors
            )
        )
        self.assertTrue(
            any(
                "agents" in error and "legacy component path" in error
                for error in errors
            )
        )
        self.assertTrue(
            any(
                "hooks.json" in error and "legacy component path" in error
                for error in errors
            )
        )

    def test_invalid_manifest_types_and_fields_fail(self):
        self.write_package(
            "plugin-one",
            {
                "name": 12,
                "unknown": True,
                "author": {"email": 7, "team": "tools"},
                "keywords": ["valid", 1],
                "extensions": {"com.example": "not-an-object"},
            },
        )
        self.write_catalog([self.entry("plugin-one")])

        errors = self.errors()
        self.assertTrue(
            any("unknown manifest field 'unknown'" in error for error in errors)
        )
        self.assertTrue(any("name must be" in error for error in errors))
        self.assertTrue(any("unknown author field 'team'" in error for error in errors))
        self.assertTrue(
            any("author.email' must be a string" in error for error in errors)
        )
        self.assertTrue(any("every 'keywords' item" in error for error in errors))
        self.assertTrue(any("extension 'com.example'" in error for error in errors))

    def test_root_legacy_manifest_and_unlisted_package_manifest_fail(self):
        self.write_catalog([])
        (self.root / "plugin.json").write_text("{}", encoding="utf-8")
        unlisted = self.root / "plugins/unlisted"
        unlisted.mkdir(parents=True)
        (unlisted / "plugin.json").write_text("{}", encoding="utf-8")

        errors = self.errors()
        self.assertTrue(
            any("repository-root component layout" in error for error in errors)
        )
        self.assertTrue(any("unlisted package manifest" in error for error in errors))

    def test_mcp_paths_cannot_escape_package_or_plugin_data(self):
        package = self.write_package("plugin-one")
        (package / "mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "bad-command": {"type": "stdio", "command": "../outside"},
                        "bad-cwd": {
                            "type": "stdio",
                            "command": "uv",
                            "cwd": "${PLUGIN_DATA}/../../outside",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        self.write_catalog([self.entry("plugin-one")])

        errors = self.errors()
        self.assertTrue(
            any(
                "bare executable or a package-relative ./ path" in error
                for error in errors
            )
        )
        self.assertTrue(any("cwd escapes PLUGIN_DATA" in error for error in errors))

    def test_mcp_schema_types_and_reserved_values_are_enforced(self):
        package = self.write_package("plugin-one")
        (package / "mcp.json").write_text(
            json.dumps(
                {
                    "mcpServers": {
                        "empty-url": {"type": "streamable-http", "url": ""},
                        "reserved-env": {
                            "type": "stdio",
                            "command": "uv",
                            "env": {"PLUGIN_ROOT": "/tmp"},
                        },
                        "bare-cwd": {
                            "type": "stdio",
                            "command": "uv",
                            "cwd": "cache",
                        },
                    }
                }
            ),
            encoding="utf-8",
        )
        self.write_catalog([self.entry("plugin-one")])

        errors = self.errors()

        self.assertTrue(
            any("missing required MCP field '$schema'" in error for error in errors)
        )
        self.assertTrue(
            any("field 'url' must not be empty" in error for error in errors)
        )
        self.assertTrue(
            any("reserved environment key 'PLUGIN_ROOT'" in error for error in errors)
        )
        self.assertTrue(any("cwd must start with ./" in error for error in errors))

    def test_overlong_markdown_link_returns_bounded_actionable_error(self):
        package = self.write_package("plugin-one")
        long_name = "a" * 300 + ".md"
        (package / "README.md").write_text(f"[long](<{long_name}>)\n", encoding="utf-8")
        self.write_catalog([self.entry("plugin-one")])

        errors = self.errors()

        self.assertEqual(len(errors), 1, errors)
        self.assertIn("cannot check link destination", errors[0])
        self.assertIn("shorten or correct its path", errors[0])
        self.assertLessEqual(len(errors[0]), 300)

    def test_nul_link_and_many_failures_produce_bounded_actionable_errors(self):
        package = self.write_package("plugin-one")
        (package / "readme.md").write_text("[bad](path%00name)\n", encoding="utf-8")
        self.write_catalog([self.entry("plugin-one")])
        self.assertTrue(
            any(
                "link destination contains a NUL byte" in error
                for error in self.errors()
            )
        )

        self.write_catalog([])
        plugins = self.root / "plugins"
        for index in range(check_package.MAX_ERRORS + 10):
            manifest = plugins / f"unlisted-{index}" / "plugin.json"
            manifest.parent.mkdir(parents=True)
            manifest.write_text("{}", encoding="utf-8")
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = check_package.main([str(self.root)])

        lines = output.getvalue().splitlines()
        self.assertEqual(exit_code, 1)
        self.assertEqual(len(lines), check_package.MAX_ERRORS + 1)
        self.assertTrue(all(": " in line for line in lines[:-1]))
        self.assertIn("additional problems omitted", lines[-1])

    def test_usage_error_returns_nonzero(self):
        output = io.StringIO()
        with redirect_stderr(output), redirect_stdout(output):
            exit_code = check_package.main(["one", "two"])

        self.assertEqual(exit_code, 2)


if __name__ == "__main__":
    unittest.main()
