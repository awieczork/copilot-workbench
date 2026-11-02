# Select a subagent model

Use this decision tree for any subagent, independently of its role:

1. **Does the check need independence from its author?** Choose a model from the other family at least as strong as the author's.
   The configured default can satisfy this condition without an override.
   When the author's family or strength cannot be established, report that model independence is unverified.
2. **Is the default unavailable?** Choose an available model at the same strength, then a stronger model when none is available.
3. **Did a result fail its criterion because of the model?** Try the other family at the same strength, then a stronger model.
   Repair a deficient brief or obtain missing input instead when either caused the failure.
4. **Otherwise:** leave the model out of the call and use the configured default.

| Strength | Claude | GPT |
| --- | --- | --- |
| Light | `Claude Haiku 5.5` | `GPT-6 Luna` |
| Medium | `Claude Sonnet 5.5` | |
| Strong | `Claude Opus 5.5` | `GPT-6.1 Sol` |

Pass the selected model, available in the session, in the subagent call; it overrides the worker's default `model`.
