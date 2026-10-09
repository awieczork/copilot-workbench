# Model tiers

Read this when writing a worker's `model` list.

## Tiers

| Tier | Models |
| --- | --- |
| Strong | `"Claude Opus 5.5 (copilot)"`, `"GPT-6.1 Sol (copilot)"` |
| Standard | `"Claude Sonnet 5.5 (copilot)"` |
| Economy | `"GPT-6 Luna (copilot)"` |
| Fast | `"Gemini 3.8 Flash (copilot)"` |
| UI | `"Kimi K3 (copilot)"` |

## Worker ladders

The `model` list holds the full ladder: the default model first, then the escalation targets in order.
A delegating agent overrides the list by passing a `model` in the call, so the ladder sets the default and documents the escalation path.

| Worker | Default tier | Escalation | `model` |
| --- | --- | --- | --- |
| `explorer`, `data-explorer`, `database-explorer`, `researcher` | Economy | Fast for quick lookups | `["GPT-6 Luna (copilot)", "Gemini 3.8 Flash (copilot)"]` |
| `developer` | Economy | Standard, then Strong | `["GPT-6 Luna (copilot)", "Claude Sonnet 5.5 (copilot)", "GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |
| `ui-developer` | UI | Strong | `["Kimi K3 (copilot)", "GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |
| `planner` | Strong | Strong, second model family | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]` |
| `reviewer` | Strong, at least the author's tier | Strong, second model family | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]` |
| `challenger` | Strong, a different model family from the author | None | `["GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |

For a new worker, copy the row of the worker whose kind and load are closest.
