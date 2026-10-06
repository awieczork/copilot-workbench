# copilot-customization maintenance notes

This file supports maintaining the skill.
`SKILL.md` does not link to it, so agents never load it at run time.

## Scope

The skill is a plugin-independent reference for agents that write GitHub Copilot customizations in VS Code.
It holds only what an agent needs while writing: artifact types and when to use them, supported frontmatter, and writing guidance.
Keep plugin-specific conventions and process for human authors, such as evaluation runs or baseline comparisons, out of the skill.

## Sources

Product facts were last checked on 2026-10-04.
The subagent `model` and `reasoning-effort` behavior was checked in the microsoft/vscode source (`src/vs/workbench/contrib/chat/common/tools/builtinTools/runSubagentTool.ts`), because the docs do not cover effort.
Treat a claim as stale when current documentation differs.

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

## Fetch full text

Read sources in full rather than through a summarizing fetch, because summaries drop fields and qualifiers.

- For a VS Code page, fetch `https://raw.githubusercontent.com/microsoft/vscode-docs/main/docs/<path>.md`, where `<path>` follows `/docs/` in the page URL.
- For an agentskills.io page, append `.md` to the page URL.
- For a GitHub repository file, fetch it from `raw.githubusercontent.com`.
- For a platform.claude.com or developers.openai.com page, append `.md` to the page URL.
- For an Awesome Copilot Learning Hub page, fetch `https://raw.githubusercontent.com/github/awesome-copilot/main/website/src/content/docs/learning-hub/<page>.md`, where `<page>` follows `/learning-hub/` in the page URL.
- For an openai.com page, which blocks automated fetches, ask the owner for a local copy.

## Refresh the skill

1. Check the primary VS Code pages and the Agent Skills specification for changed fields, defaults, locations, and experimental labels.
1. Compare the VS Code built-in `agent-customization` skill for newly documented fields, such as `reasoning-effort`, which appeared there before the public docs.
1. Update product facts only from primary sources, and update writing guidance only when evidence shows a changed behavior or a credible failure.
1. Update the date under Sources.
