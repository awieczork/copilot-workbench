# Open issues

| OI | Area | State | Issue | Rule until closure | Closure condition |
| --- | --- | --- | --- | --- | --- |
| OI-02 | Repository interactions | Verified limitation | GitHub limits collaborator-only interaction restrictions to six months; the current restriction expires at `2027-04-15T10:41:08Z`. | Renew before expiry with `gh api --method PUT repos/awieczork/copilot-workbench/interaction-limits -f limit=collaborators_only -f expiry=six_months` and update this expiry from the response; keep external contributions unsupported. | GitHub provides and the owner enables a permanent repository-level restriction, or the owner changes the contribution policy. |
