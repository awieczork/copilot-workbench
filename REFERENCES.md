# References

External resources that inform the design of `copilot-workbench`.
Consult them as structural inspiration when specifying a new agent or skill, not as tone or output templates.

## Plugin standard

| Resource | Relevance |
| --- | --- |
| [Agent Plugins](https://agent-plugins.org/) and its [specification](https://agent-plugins.org/specification) | The open, vendor-neutral 1.0 standard for packaging skills, MCP servers, and client extensions into portable plugins. |
| [VS Code Agent Plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins) | How VS Code discovers, installs, and loads an Agent Plugins package, including its Copilot extensions. |

## Customization and prompting guidance

The sources for writing GitHub Copilot customizations, with their full-text fetch methods, live in the [copilot-customization maintenance notes](skills/copilot-customization/README.md), because that skill's refresh procedure depends on them.

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
| Discuss | [Product Manager](https://github.com/github/awesome-copilot/blob/main/agents/se-product-manager-advisor.agent.md), [Idea Generator](https://github.com/github/awesome-copilot/blob/main/agents/simple-app-idea-generator.agent.md), and [VS Code planning](https://code.visualstudio.com/docs/agents/planning). |
| Explorer and data explorers | [Gem Researcher](https://github.com/github/awesome-copilot/blob/main/agents/gem-researcher.agent.md), [Context Architect](https://github.com/github/awesome-copilot/blob/main/agents/context-architect.agent.md), [Kusto Assistant](https://github.com/github/awesome-copilot/blob/main/agents/kusto-assistant.agent.md), [MongoDB Performance Advisor](https://github.com/github/awesome-copilot/blob/main/agents/mongodb-performance-advisor.agent.md), and [Research Harness Engineer](https://github.com/github/awesome-copilot/blob/main/agents/research-harness-engineer.agent.md). |
| Researcher | [Context7 Expert](https://github.com/github/awesome-copilot/blob/main/agents/context7-expert.agent.md), [Doublecheck](https://github.com/github/awesome-copilot/blob/main/agents/doublecheck.agent.md), and [Task Researcher](https://github.com/github/awesome-copilot/blob/main/agents/task-researcher.agent.md). |
| Planner | [Gem Planner](https://github.com/github/awesome-copilot/blob/main/agents/gem-planner.agent.md) and [One-Shot Feature Issue Planner](https://github.com/github/awesome-copilot/blob/main/agents/one-shot-feature-issue-planner.agent.md). |
| Developer | [Coder](https://gist.github.com/burkeholland/0e68481f96e94bbb98134fa6efd00436), [SWE](https://github.com/github/awesome-copilot/blob/main/agents/swe.agent.md), and [Gem Implementer](https://github.com/github/awesome-copilot/blob/main/agents/gem-implementer.agent.md). |
| UI Developer | [Gem Designer](https://github.com/github/awesome-copilot/blob/main/agents/gem-designer.agent.md), [Gem Browser Tester](https://github.com/github/awesome-copilot/blob/main/agents/gem-browser-tester.agent.md), and [DevTools Regression Investigator](https://github.com/github/awesome-copilot/blob/main/agents/devtools-regression-investigator.agent.md). |
| Reviewer | [Gem Reviewer](https://github.com/github/awesome-copilot/blob/main/agents/gem-reviewer.agent.md), [AI Team QA](https://github.com/github/awesome-copilot/blob/main/agents/ai-team-qa.agent.md), and [QA](https://github.com/github/awesome-copilot/blob/main/agents/qa.agent.md). |
| Challenger | [Critical Thinking](https://github.com/github/awesome-copilot/blob/main/agents/critical-thinking.agent.md), [Devil's Advocate](https://github.com/github/awesome-copilot/blob/main/agents/devils-advocate.agent.md), and [rubber duck](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck). |

## Skill and rule inspirations

| Component | Structural inspirations |
| --- | --- |
| Database exploration patterns | [SQL Code Review](https://github.com/github/awesome-copilot/blob/main/skills/sql-code-review/SKILL.md), for the unmatched-key check. |
