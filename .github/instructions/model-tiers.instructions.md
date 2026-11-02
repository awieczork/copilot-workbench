---
description: "Use when choosing agent-team worker models. Preserves the existing worker model tiers. Not for entry agents or other packages."
applyTo: "plugins/agent-team/com.github.copilot/agents/challenger.agent.md,plugins/agent-team/com.github.copilot/agents/data-explorer.agent.md,plugins/agent-team/com.github.copilot/agents/database-explorer.agent.md,plugins/agent-team/com.github.copilot/agents/developer.agent.md,plugins/agent-team/com.github.copilot/agents/explorer.agent.md,plugins/agent-team/com.github.copilot/agents/researcher.agent.md,plugins/agent-team/com.github.copilot/agents/reviewer.agent.md"
---

# Model tiers

Give each worker one default `model`, choosing the cheapest model that does the role well at the context sizes it reaches.
Give a role that needs a strong model a strong default.
Delegating agents select alternatives through `brief-subagent`, including when the author and checker need different model families; alternatives do not belong in the worker's frontmatter.

| Strength | Claude | GPT |
| --- | --- | --- |
| Light | `Claude Haiku 5.5 (copilot)` | `GPT-6 Luna (copilot)` |
| Medium | `Claude Sonnet 5.5 (copilot)` | |
| Strong | `Claude Opus 5.5 (copilot)` | `GPT-6.1 Sol (copilot)` |
