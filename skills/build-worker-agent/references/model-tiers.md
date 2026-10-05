# Model tiers

Read this when writing a worker's `model` list or choosing its step detail.
This file is the single place for model names; change a model here and in the `model` lists of the workers that use it.

## Tiers

| Tier | Models | Step detail |
| --- | --- | --- |
| Strong | `"Claude Opus 5.5 (copilot)"`, `"GPT-6.1 Sol (copilot)"` | Goals, reasons, and completion criteria |
| Standard | `"Claude Sonnet 5.5 (copilot)"` | Exact steps with their checks |
| Economy | `"GPT-6 Luna (copilot)"` | Exact steps with their checks |
| Fast | `"Gemini 3.8 Flash (copilot)"` | Exact steps with their checks |
| UI | `"Kimi K3 (copilot)"` | Exact steps with their checks |

Write a worker's steps for its default tier, the first entry of its ladder, because most runs use it and an escalated model follows detailed steps well.

## Worker ladders

The `model` list holds the full ladder: the default model first, then the escalation targets in order.
A delegating agent overrides the list by passing a `model` in the call, so the ladder sets the default and documents the escalation path.

| Worker | Default tier | Escalation | `model` |
| --- | --- | --- | --- |
| Explorer, Data Explorer, Database Explorer, Researcher | Economy | Fast for quick lookups | `["GPT-6 Luna (copilot)", "Gemini 3.8 Flash (copilot)"]` |
| Developer | Economy | Standard, then Strong | `["GPT-6 Luna (copilot)", "Claude Sonnet 5.5 (copilot)", "GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |
| UI Developer | UI | Strong | `["Kimi K3 (copilot)", "GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |
| Planner | Strong | Strong, second model family | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]` |
| Reviewer | Strong, at least the author's tier | Strong, second model family | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]` |
| Challenger | Strong, a different model family from the author | None | `["GPT-6.1 Sol (copilot)", "Claude Opus 5.5 (copilot)"]` |

For a new worker, take the row of the existing worker whose kind and load are closest, and name that choice in the specification.
