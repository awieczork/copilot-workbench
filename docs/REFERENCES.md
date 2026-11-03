# References

These sources inform the design of `copilot-workbench`.
Use inspiration sources for structure, not as tone or output templates.

## Plugin format

- [Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference): Copilot-format fields and component locations.
- [VS Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins): discovery, installation, updates, and loading.
- [Plugin marketplaces](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) and [marketplace reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson): catalog metadata and sources.
- [VS Code agent harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses): harness choice and client-dependent capabilities.
- [VS Code plugin authoring reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference): Agent Plugins 1.0 manifest and component locations.
- [Manifest schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json) and [MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json): canonical identifiers and static validation.

The 1.0 layout and schema were checked on 2026-10-28 for the migration.
Static checks do not prove runtime behavior; the owner's separate plugin test did not specify its client version or configuration.
This check did not refresh the customization facts below.

## Claude Code catalog

- [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference): `.claude-plugin/marketplace.json`, required catalog fields, repository-relative sources, and entries that serve as manifests when a package has no Claude manifest.
- [Manifest reference](https://code.claude.com/docs/en/plugins/manifest-reference): optional `.claude-plugin/plugin.json`, default `skills/`, `agents/`, and `.mcp.json` locations, and explicit component paths, including [MCP JSON paths](https://code.claude.com/docs/en/plugins/manifest-reference#mcpservers).
- [Plugin commands reference](https://code.claude.com/docs/en/plugins/cli-reference): marketplace registration, `plugin list --json --available`, and `plugin validate` checks and limits.
- [Plugin loading reference](https://code.claude.com/docs/en/plugins/loading): source-based versions when neither a Claude manifest nor its marketplace entry supplies a version.
- [Plugin MCP lifecycle](https://code.claude.com/docs/en/mcp#plugin-provided-mcp-servers): server definitions and automatic startup when a plugin is enabled.

Checked on 2026-11-03 against Anthropic's documentation and the Context7 index of that documentation.
The [Claude Code discovery catalog](../.claude-plugin/marketplace.json) reuses the Copilot catalog's identity and package sources without changing package payloads.
The catalog supplies entry manifest fields; `agent-team` sets `mcpServers` to `./mcp.json`, resolved from the plugin root.
This path registers the existing server configuration without copying it; Copilot agents and automatic rules remain unregistered.
These sources establish the documented discovery approach, not runtime compatibility; native validation and live discovery have not run in the authoring Linux workspace because Claude Code is unavailable there.

## Tools and configuration

- [PyYAML documentation](https://pyyaml.org/wiki/PyYAMLDocumentation): `safe_load` parses YAML without constructing arbitrary Python objects.
- [GitHub CLI release creation](https://cli.github.com/manual/gh_release_create) and [release listing](https://cli.github.com/manual/gh_release_list): publication with `--verify-tag` and notes from standard input; a limited release list does not prove complete absence. Checked on 2026-10-28.
- [Context7 MCP setup](https://github.com/upstash/context7/blob/master/packages/mcp/README.md) and [developer guide](https://context7.com/docs/resources/developer): the server reads `CONTEXT7_API_KEY` from its environment.
- [Models and pricing for GitHub Copilot](https://docs.github.com/en/copilot/reference/copilot-billing/models-and-pricing): model strengths, prices, and context thresholds behind the [model tiers](../.github/instructions/model-tiers.instructions.md) and [`brief-subagent` alternatives](../plugins/agent-team/skills/brief-subagent/references/model-selection.md). Checked on 2026-11-02.

## Customization guidance

The [`copilot-customization`](../plugins/agent-plugin-dev/skills/copilot-customization/SKILL.md) skill ships without its authoring process, so its sources and refresh procedure stay here.
Product facts were last checked on 2026-10-10, except for plugin agent and rule locations, rechecked on 2026-10-29 against the [VS Code plugin authoring reference](https://code.visualstudio.com/docs/agents/reference/agent-plugin-reference).
Agent Plugins 1.0 uses `com.github.copilot/agents/` and `com.github.copilot/rules/`; root `agents/` and `rules/` are Copilot-format locations.
Treat other claims as stale when current documentation differs.

The microsoft/vscode source alone confirms these facts because documentation omits them or differs:

- A Local subagent call accepts a per-call `model` but no reasoning-effort parameter: `src/vs/workbench/contrib/chat/common/tools/builtinTools/runSubagentTool.ts`.
- A skill with a different `name` loads under its folder name, and a plugin agent without `name` gets a plugin-prefixed ID: `promptsServiceImpl.ts`.
- `applyTo` accepts comma-separated patterns and matches relative patterns at any depth, ignoring case: `computeAutomaticInstructions.ts`.
- The Local `web` tool set contains `web/fetch`, `web/githubRepo`, and `web/githubTextSearch`: `extensions/copilot/package.json`.

### Primary sources

- VS Code: [custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions), [custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents), [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills), [Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins), [subagents](https://code.visualstudio.com/docs/agents/run/subagents), and [tools reference](https://code.visualstudio.com/docs/agents/reference/tools-reference).
- [Agent Skills specification](https://agentskills.io/specification).
- [microsoft/vscode source](https://github.com/microsoft/vscode) for behavior the documentation does not cover.

### Writing and structure

- [VS Code built-in `agent-customization` skill](https://github.com/microsoft/vscode/tree/main/extensions/copilot/assets/prompts/skills/agent-customization).
- Agent Skills: [best practices](https://agentskills.io/skill-creation/best-practices), [descriptions](https://agentskills.io/skill-creation/optimizing-descriptions), and [scripts](https://agentskills.io/skill-creation/using-scripts).
- [Matt Pocock `writing-for-agents`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md).
- Anthropic: [`skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md), [skill authoring](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), [prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), and [prompt engineering](https://claude.com/blog/best-practices-for-prompt-engineering).
- Awesome Copilot: [creating skills](https://awesome-copilot.github.com/learning-hub/creating-effective-skills/), [defining instructions](https://awesome-copilot.github.com/learning-hub/defining-custom-instructions/), and [building agents](https://awesome-copilot.github.com/learning-hub/building-custom-agents/).
- OpenAI: [model guide for the GPT-6 family](https://openai.com/index/practical-guide-building-gpt-6/), [rethinking skills and prompts](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), and [using GPT-6](https://developers.openai.com/api/docs/guides/latest-model).

### Fetch full text

Read sources in full, because summaries can omit fields and qualifiers.

- For a VS Code page, fetch `https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/<path>.md`, where `<path>` follows `/docs/` in its URL.
- For an agentskills.io page, append `.md` to its URL.
- For a GitHub repository file, use `raw.githubusercontent.com`.
- For a platform.claude.com or developers.openai.com page, append `.md` to its URL.
- For an Awesome Copilot Learning Hub page, fetch `https://raw.githubusercontent.com/github/awesome-copilot/main/website/src/content/docs/learning-hub/<page>.md`, where `<page>` follows `/learning-hub/` in its URL.
- For an openai.com page, ask the owner for a local copy because automated fetches are blocked.

### Refresh product facts

1. Check the primary VS Code pages and Agent Skills specification for changed fields, defaults, locations, and experimental labels.
1. Compare the VS Code built-in `agent-customization` skill for fields the public docs do not list yet.
1. Recheck each source-only fact above in microsoft/vscode.
1. Update product facts only from primary sources, and writing guidance only when evidence shows a changed behavior or credible failure.
1. Update the date under Customization guidance.

## Agent and context engineering

- [Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents): context as a finite budget.
- [When to fold subagents into the main loop](https://claude.com/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop): progressive disclosure and focused delegation.
- [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents): start with the simplest solution.
- [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents): focused, high-signal tools.
- [12-factor agents](https://humanlayer.dev/blog/12-factor-agents): deterministic software and bounded agents.
- [Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents): carry decisions into delegated work.
- [Comprehension debt](https://addyosmani.com/blog/comprehension-debt/): keep work understandable to its owner.

## Agent inspirations

- Entry agents: [Gem Orchestrator](https://github.com/github/awesome-copilot/blob/main/agents/gem-orchestrator.agent.md), [Orchestrator](https://gist.github.com/burkeholland/0e68481f96e94bbb98134fa6efd00436), [RUG](https://github.com/github/awesome-copilot/blob/main/agents/rug-orchestrator.agent.md), and [AI Team Producer](https://github.com/github/awesome-copilot/blob/main/agents/ai-team-producer.agent.md).
- Discuss: [Product Manager](https://github.com/github/awesome-copilot/blob/main/agents/se-product-manager-advisor.agent.md), [Idea Generator](https://github.com/github/awesome-copilot/blob/main/agents/simple-app-idea-generator.agent.md), and [VS Code planning](https://code.visualstudio.com/docs/agents/run/planning).
- Explorer and data explorers: [Gem Researcher](https://github.com/github/awesome-copilot/blob/main/agents/gem-researcher.agent.md), [Context Architect](https://github.com/github/awesome-copilot/blob/main/agents/context-architect.agent.md), [Kusto Assistant](https://github.com/github/awesome-copilot/blob/main/agents/kusto-assistant.agent.md), [MongoDB Performance Advisor](https://github.com/github/awesome-copilot/blob/main/agents/mongodb-performance-advisor.agent.md), [Research Harness Engineer](https://github.com/github/awesome-copilot/blob/main/agents/research-harness-engineer.agent.md), and [SQL Code Review](https://github.com/github/awesome-copilot/blob/main/skills/sql-code-review/SKILL.md) for unmatched-key checks.
- Researcher: [Context7 Expert](https://github.com/github/awesome-copilot/blob/main/agents/context7.agent.md), [Doublecheck](https://github.com/github/awesome-copilot/blob/main/agents/doublecheck.agent.md), and [Task Researcher](https://github.com/github/awesome-copilot/blob/main/agents/task-researcher.agent.md).
- Planning: [Gem Planner](https://github.com/github/awesome-copilot/blob/main/agents/gem-planner.agent.md) and [One-Shot Feature Issue Planner](https://github.com/github/awesome-copilot/blob/main/agents/one-shot-feature-issue-planner.agent.md).
- Developer: [Coder](https://gist.github.com/burkeholland/0e68481f96e94bbb98134fa6efd00436), [SWE](https://github.com/github/awesome-copilot/blob/main/agents/swe-subagent.agent.md), and [Gem Implementer](https://github.com/github/awesome-copilot/blob/main/agents/gem-implementer.agent.md).
- Reviewer: [Gem Reviewer](https://github.com/github/awesome-copilot/blob/main/agents/gem-reviewer.agent.md), [AI Team QA](https://github.com/github/awesome-copilot/blob/main/agents/ai-team-qa.agent.md), and [QA](https://github.com/github/awesome-copilot/blob/main/agents/qa-subagent.agent.md).
- Challenger: [Critical Thinking](https://github.com/github/awesome-copilot/blob/main/agents/critical-thinking.agent.md), [Devil's Advocate](https://github.com/github/awesome-copilot/blob/main/agents/devils-advocate.agent.md), and [rubber duck](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck).
