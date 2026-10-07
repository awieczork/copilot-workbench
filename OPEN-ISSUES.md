# Open Issues

| OI | Area | State | Issue | Rule until closure | Closure condition |
| --- | --- | --- | --- | --- | --- |
| OI-01 | `database-explorer` | Verified limitation | The Redshift fallback in delegated exploration is verified statically, without a live Copilot delegation. | Treat the delegated Redshift fallback as unproven at run time, and state that limit in any result that relies on it. | A live Copilot delegation exercises the fallback, and its result is recorded. |
