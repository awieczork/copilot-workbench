# Entry agent models

Read this when writing an entry agent's `model` field or choosing its step detail.

| Kind | `model` | Step detail |
| --- | --- | --- |
| Lead | `["Claude Opus 5.5 (copilot)", "GPT-6.1 Sol (copilot)"]` | Goals, reasons, and completion criteria, because leads run on the Strong tier |
| Chat | Leave `model` out, so that the agent runs on the model the user selects in the chat | Goal-oriented, with exact steps only where a deviation breaks the result, because any model may read it |

A lead's list is a fallback for availability, not an escalation path: a lead does not escalate itself.
Workers' models and escalation ladders sit in each worker's own `model` list, which the lead reads when it delegates.
