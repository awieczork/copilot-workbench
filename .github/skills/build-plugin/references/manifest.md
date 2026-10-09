# Manifest and MCP reference

Use the [Agent Plugins specification](https://agent-plugins.org/specification) as the normative authority for portable package behavior.
Use [the plugin schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and [the MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) for machine-readable validation.
When the specification and a schema conflict, follow the specification.
The target client is VS Code with GitHub Copilot Chat; client-extension claims below are scoped to its documented static package format.

## plugin.json fields

The top-level schema is closed.
These are the only permitted fields.

| Field         | Required | Type and constraint                                                              |
| ------------- | -------- | -------------------------------------------------------------------------------- |
| `$schema`     | Yes      | String equal to `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`     |
| `name`        | Yes      | String, 1-64 characters matching the regex pattern below                         |
| `version`     | No       | String; Semantic Versioning recommended, not validated by the schema             |
| `description` | No       | String                                                                           |
| `author`      | No       | Object with optional string fields `name`, `email`, `url` and no others          |
| `homepage`    | No       | String; no URL format validation                                                 |
| `repository`  | No       | String; no URL format validation                                                 |
| `license`     | No       | String; SPDX recommended, not validated                                          |
| `keywords`    | No       | Array of strings                                                                 |
| `extensions`  | No       | Object whose keys are reverse-DNS client namespaces and whose values are objects |

Constrain `name` to 1-64 characters matching:

```text
^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$
```

No field declares a schema default, so omitting a field leaves it absent rather than filled.

The `$schema` value selects Agent Plugins 1.0 semantics.
Without this marker, VS Code applies another detected plugin format or its default Copilot format.
Write the canonical URL for an Agent Plugins 1.0 package.

## Unknown fields and failure boundaries

The specification requires a client to report and ignore an unknown top-level field or a non-object `extensions` value, and to reject the plugin on any other manifest violation.
VS Code is more lenient: it ignores unknown and malformed optional fields and accepts any agent-plugins.org schema revision, so validate against the schema yourself, because VS Code does not report the error.

Carry documented Copilot-specific configuration under `extensions["com.github.copilot"]`, not in an unknown top-level field that VS Code discards without applying it.
Add a key under `extensions["com.github.copilot"]` only when current VS Code documentation defines that key and its effect.
Otherwise leave the object out.

## mcp.json structure

Root `mcp.json` accepts only `$schema` and `mcpServers`.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {
    "validator": {
      "type": "stdio",
      "command": "./bin/validator",
      "args": ["--data", "${PLUGIN_DATA}/validator"],
      "env": { "CONFIG": "${PLUGIN_ROOT}/config.json" },
      "cwd": "${PLUGIN_ROOT}"
    },
    "deployment-api": {
      "type": "streamable-http",
      "url": "https://deploy.example.com/mcp",
      "headers": { "X-Tenant": "public-tenant" }
    }
  }
}
```

| Transport         | Required          | Optional             |
| ----------------- | ----------------- | -------------------- |
| `stdio`           | `type`, `command` | `args`, `env`, `cwd` |
| `streamable-http` | `type`, `url`     | `headers`            |
| `sse`             | `type`, `url`     | `headers`            |

Each server entry is closed to its own transport.
The specification makes a `url` on a `stdio` entry, or a `command` on a remote entry, invalid and requires the client to skip that server; VS Code ignores the foreign field instead, so only schema validation catches it.

This format differs from native VS Code MCP configuration, which uses the top-level `servers`, `inputs`, and `sandbox`, the `http` type, and the per-server `oauth`, `envFile`, `dev`, and `sandboxEnabled`.
Translate a native block field by field into the table above rather than copying it, because the plugin schema rejects every one of those keys.
The current [VS Code Agent Plugins page](https://code.visualstudio.com/docs/agent-customization/agent-plugins) does not reproduce the plugin MCP schema and defers to the specification; treat the fetched schema as the authority when the two disagree.

Keep the `mcp.json` schema version equal to the `plugin.json` schema version.

## stdio command and paths

`command` is one executable token, not a shell command line.
Use a plugin-relative path starting with `./` for an executable bundled with the package.
Use a bare executable name only for an executable the package does not bundle, because the client resolves it with the platform's executable search; do not rely on a `PATH` set in `env` to change that search.
Move every argument into `args`.

`cwd` defaults to the plugin root.
An explicit value must stay inside the directory its own prefix names, and must match:

```text
^(?:\./|\$\{PLUGIN_ROOT\}(?:/|$)|\$\{PLUGIN_DATA\}(?:/|$))
```

Use `${PLUGIN_ROOT}` for packaged files and `${PLUGIN_DATA}` for writable server state only in stdio `args`, `env` values, and `cwd`.
Do not use these placeholders in `command`, environment variable keys, URLs, or headers.

## Remote server constraints

- Use an absolute HTTP or HTTPS URL with no user information and no fragment.
- Use HTTPS for any non-loopback endpoint.
