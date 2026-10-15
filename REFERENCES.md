# References

External resources that inform the design of `copilot-workbench`.
Use them as structural inspiration, not as tone or output templates.

## Plugin format

| Resource | Relevance |
| --- | --- |
| [GitHub Copilot CLI plugin reference](https://docs.github.com/en/copilot/reference/cli-plugin-reference) | The Copilot plugin format: manifest fields, component locations, and loading rules of the Copilot runtime behind Agent Host. |
| [VS Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins) | How VS Code discovers, installs, and loads a Copilot-format plugin. |
| [GitHub plugin marketplaces](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-marketplace) and [marketplace reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-plugin-reference#marketplacejson) | Catalog location, metadata, and repository-relative plugin sources. |
| [VS Code agent harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses) | Copilot harness execution in Agent Host and client-dependent capabilities. |

## Service configuration

| Resource | Relevance |
| --- | --- |
| [Context7 MCP setup](https://github.com/upstash/context7/blob/master/packages/mcp/README.md) and [developer guide](https://context7.com/docs/resources/developer) | The local server reads `CONTEXT7_API_KEY` from its process environment without a packaged key or command-line argument. |

## Customization and prompting guidance

The plugin skill [`copilot-customization`](skills/copilot-customization/SKILL.md) ships without its authoring process, so its sources and refresh procedure live here.

### Sources

Product facts were last checked on 2026-10-10.
The microsoft/vscode source alone confirms these facts, because the docs do not cover them or state them differently:

- a subagent call takes a per-call `model` and has no reasoning-effort parameter: `src/vs/workbench/contrib/chat/common/tools/builtinTools/runSubagentTool.ts`;
- a skill whose `name` differs from its folder loads under the folder name, and a plugin agent without `name` gets a plugin-prefixed id: `promptsServiceImpl.ts`;
- `applyTo` takes comma-separated patterns and matches a relative pattern at any depth, ignoring case: `computeAutomaticInstructions.ts`;
- the `web` tool set holds `web/fetch`, `web/githubRepo`, and `web/githubTextSearch`: `extensions/copilot/package.json`.

Treat any other claim as stale when current documentation differs.

Primary sources:

- [VS Code custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [VS Code Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
- [VS Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins)
- [VS Code subagents](https://code.visualstudio.com/docs/agents/run/subagents)
- [VS Code tools reference](https://code.visualstudio.com/docs/agents/reference/tools-reference)
- [Agent Skills specification](https://agentskills.io/specification)
- [microsoft/vscode repository](https://github.com/microsoft/vscode), for behavior the docs do not cover

Structure and writing inspiration:

- [VS Code built-in `agent-customization` skill](https://github.com/microsoft/vscode/tree/main/extensions/copilot/assets/prompts/skills/agent-customization)
- [Agent Skills best practices](https://agentskills.io/skill-creation/best-practices), [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions), and [using scripts](https://agentskills.io/skill-creation/using-scripts)
- [Matt Pocock `writing-for-agents`](https://github.com/mattpocock/skills/blob/main/skills/productivity/writing-for-agents/SKILL.md)
- [Anthropic `skill-creator`](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md) and [Claude skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Awesome Copilot Learning Hub: creating effective skills](https://awesome-copilot.github.com/learning-hub/creating-effective-skills/), [defining custom instructions](https://awesome-copilot.github.com/learning-hub/defining-custom-instructions/), and [building custom agents](https://awesome-copilot.github.com/learning-hub/building-custom-agents/)
- [OpenAI: A model guide for the GPT-6 family](https://openai.com/index/practical-guide-building-gpt-6/), [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), and [Using GPT-6](https://developers.openai.com/api/docs/guides/latest-model)
- [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) and [Best practices for prompt engineering](https://claude.com/blog/best-practices-for-prompt-engineering)

### Fetch full text

Read sources in full rather than through a summarizing fetch, because summaries drop fields and qualifiers.

- For a VS Code page, fetch `https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/<path>.md`, where `<path>` follows `/docs/` in the page URL.
- For an agentskills.io page, append `.md` to the page URL.
- For a GitHub repository file, fetch it from `raw.githubusercontent.com`.
- For a platform.claude.com or developers.openai.com page, append `.md` to the page URL.
- For an Awesome Copilot Learning Hub page, fetch `https://raw.githubusercontent.com/github/awesome-copilot/main/website/src/content/docs/learning-hub/<page>.md`, where `<page>` follows `/learning-hub/` in the page URL.
- For an openai.com page, which blocks automated fetches, ask the owner for a local copy.

### Refresh the skill's product facts

1. Check the primary VS Code pages and the Agent Skills specification for changed fields, defaults, locations, and experimental labels.
2. Compare the VS Code built-in `agent-customization` skill for fields the public docs do not list yet.
3. Check each source-only fact under Sources again in microsoft/vscode.
4. Update product facts only from primary sources, and update writing guidance only when evidence shows a changed behavior or a credible failure.
5. Update the date under Sources.

## Agent and context engineering

| Resource | Relevance |
| --- | --- |
| [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Attention as a finite budget, guidance at the right altitude, and just-in-time context. |
| [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | The simplest solution first, with complexity added only when it pays. |
| [Writing tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | Few, well-defined tools with high-signal output. |
| [12-factor agents](https://humanlayer.dev/blog/12-factor-agents) | Deterministic software with model judgment where it adds value, and small, focused agents. |
| [Don't build multi-agents](https://cognition.com/blog/dont-build-multi-agents) | Delegated work carries the decisions already made. |
| [Comprehension debt](https://addyosmani.com/blog/comprehension-debt/) | Work stays understandable to the person who owns it. |

## Agent inspirations

| Role | Structural inspirations |
| --- | --- |
| Entry agents | [Gem Orchestrator](https://github.com/github/awesome-copilot/blob/main/agents/gem-orchestrator.agent.md), [Orchestrator](https://gist.github.com/burkeholland/0e68481f96e94bbb98134fa6efd00436), [RUG](https://github.com/github/awesome-copilot/blob/main/agents/rug-orchestrator.agent.md), and [AI Team Producer](https://github.com/github/awesome-copilot/blob/main/agents/ai-team-producer.agent.md). |
| Discuss | [Product Manager](https://github.com/github/awesome-copilot/blob/main/agents/se-product-manager-advisor.agent.md), [Idea Generator](https://github.com/github/awesome-copilot/blob/main/agents/simple-app-idea-generator.agent.md), and [VS Code planning](https://code.visualstudio.com/docs/agents/run/planning). |
| Explorer and data explorers | [Gem Researcher](https://github.com/github/awesome-copilot/blob/main/agents/gem-researcher.agent.md), [Context Architect](https://github.com/github/awesome-copilot/blob/main/agents/context-architect.agent.md), [Kusto Assistant](https://github.com/github/awesome-copilot/blob/main/agents/kusto-assistant.agent.md), [MongoDB Performance Advisor](https://github.com/github/awesome-copilot/blob/main/agents/mongodb-performance-advisor.agent.md), [Research Harness Engineer](https://github.com/github/awesome-copilot/blob/main/agents/research-harness-engineer.agent.md), and [SQL Code Review](https://github.com/github/awesome-copilot/blob/main/skills/sql-code-review/SKILL.md) for the unmatched-key check. |
| Researcher | [Context7 Expert](https://github.com/github/awesome-copilot/blob/main/agents/context7.agent.md), [Doublecheck](https://github.com/github/awesome-copilot/blob/main/agents/doublecheck.agent.md), and [Task Researcher](https://github.com/github/awesome-copilot/blob/main/agents/task-researcher.agent.md). |
| Planner | [Gem Planner](https://github.com/github/awesome-copilot/blob/main/agents/gem-planner.agent.md) and [One-Shot Feature Issue Planner](https://github.com/github/awesome-copilot/blob/main/agents/one-shot-feature-issue-planner.agent.md). |
| Developer | [Coder](https://gist.github.com/burkeholland/0e68481f96e94bbb98134fa6efd00436), [SWE](https://github.com/github/awesome-copilot/blob/main/agents/swe-subagent.agent.md), and [Gem Implementer](https://github.com/github/awesome-copilot/blob/main/agents/gem-implementer.agent.md). |
| UI Developer | [Gem Designer](https://github.com/github/awesome-copilot/blob/main/agents/gem-designer.agent.md), [Gem Browser Tester](https://github.com/github/awesome-copilot/blob/main/agents/gem-browser-tester.agent.md), and [DevTools Regression Investigator](https://github.com/github/awesome-copilot/blob/main/agents/devtools-regression-investigator.agent.md). |
| Reviewer | [Gem Reviewer](https://github.com/github/awesome-copilot/blob/main/agents/gem-reviewer.agent.md), [AI Team QA](https://github.com/github/awesome-copilot/blob/main/agents/ai-team-qa.agent.md), and [QA](https://github.com/github/awesome-copilot/blob/main/agents/qa-subagent.agent.md). |
| Challenger | [Critical Thinking](https://github.com/github/awesome-copilot/blob/main/agents/critical-thinking.agent.md), [Devil's Advocate](https://github.com/github/awesome-copilot/blob/main/agents/devils-advocate.agent.md), and [rubber duck](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck). |
