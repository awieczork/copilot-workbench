---
description: "Use when choosing agent-team worker models. Preserves the existing worker model tiers. Not for entry agents or other packages."
applyTo: "plugins/agent-team/com.github.copilot/agents/challenger.agent.md,plugins/agent-team/com.github.copilot/agents/data-explorer.agent.md,plugins/agent-team/com.github.copilot/agents/database-explorer.agent.md,plugins/agent-team/com.github.copilot/agents/developer.agent.md,plugins/agent-team/com.github.copilot/agents/explorer.agent.md,plugins/agent-team/com.github.copilot/agents/planner.agent.md,plugins/agent-team/com.github.copilot/agents/researcher.agent.md,plugins/agent-team/com.github.copilot/agents/reviewer.agent.md,plugins/agent-team/com.github.copilot/agents/ui-developer.agent.md"
---

# Model tiers

A worker's `model` list puts its default model first; VS Code runs the first available entry, so every later entry is also an availability fallback.

Give a worker one of two lists:

- A ladder, when a cheap model does the role well: the cheapest model that does it, then the models a delegating agent escalates to, in order, because most delegations are routine.
- A pair, when the role needs a strong model: the strong default, then the model of the same strength from the other family, as an alternative, not an escalation.

Build either list by these principles:

- In a ladder, take the other model family at the same strength before a stronger model, because another family often solves what one family misses.
- Give a checker a model at least as strong as the author's, because a weaker checker misses what the author got wrong.
- Give a challenger a model from another family than the author's, because one family shares its blind spots.
- At one strength, put first the model that is cheaper at the context sizes the role reaches, because a delegated run can grow past a price threshold; `GPT-6 Luna (copilot)` costs no more than `Claude Haiku 5.5 (copilot)` up to 100,000 input tokens and less above it.

| Strength | Claude | GPT |
| --- | --- | --- |
| Light | `Claude Haiku 5.5 (copilot)` | `GPT-6 Luna (copilot)` |
| Medium | `Claude Sonnet 5.5 (copilot)` | |
| Strong | `Claude Opus 5.5 (copilot)` | `GPT-6.1 Sol (copilot)` |
