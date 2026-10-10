# Model tiers

Read this when writing a worker's `model` list.

The `model` list holds the full ladder: the default model first, then the escalation targets in order.
A delegating agent overrides the list by passing a `model` in the call, so the ladder sets the default and documents the escalation path.

Build a ladder by these principles:

- Default to the cheapest model that does the role well, because most delegations are routine.
- Escalate to the other model family at the same strength before a stronger model, because another family often solves what one family misses.
- Give a checker a model at least as strong as the author's, because a weaker checker misses what the author got wrong.
- Give a challenger a model from another family than the author's, because one family shares its blind spots.

| Worker | `model` |
| --- | --- |
| `explorer`, `data-explorer`, `database-explorer`, `researcher` | `["GPT-6 Luna (copilot)", "Claude Haiku 5.5 (copilot)", "Claude Sonnet 5.5 (copilot)"]` |
| `developer` | `["GPT-6 Luna (copilot)", "Claude Haiku 5.5 (copilot)", "Claude Sonnet 5.5 (copilot)", "GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |
| `ui-developer` | `["Kimi K3 (copilot)", "GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |
| `planner` | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]` |
| `reviewer` | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]` |
| `challenger` | `["GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |
