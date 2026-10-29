---
name: update-project-records
description: "Use when completed work, a phase change, an accepted decision, or a confirmed or resolved blocker changes project records, or when asked to reconcile them. Updates PROJECT-STATUS.md, OPEN-ISSUES.md, and CHANGELOG.md from evidence. Not for transient task state or formatting-only edits."
---

# Update project records

Bring the project's durable records into line with established results, changing only records whose content is affected.
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.

## Procedure

1. Establish the affected project, record paths, and update scope from the request and project instructions. Respect their permissions and timing for record updates, including deferred changelog edits; automatic skill selection grants no additional permission. Create a missing record only when the request or project instructions calls for it.
2. Compare completed work, confirmed findings, and accepted decisions with the current records. Select only records with an evidenced change; when none needs an update, report that result without editing files.
3. Before editing a selected record, read its rule: [project status](../../com.github.copilot/rules/project-status.instructions.md) for current state and planned work, [open issues](../../com.github.copilot/rules/open-issues.instructions.md) for unresolved decisions, missing inputs, and verified limitations, or [changelog](../../com.github.copilot/rules/changelog.instructions.md) for user-visible changes. Read related records when an update affects their links or meaning.
4. Update the selected records from that evidence without inventing objectives, priorities, decisions, or completion. Finish unaffected updates before reporting an unresolved decision as `Decision needed` or an unavailable working fact as `Missing input`.
5. Check the updated records together for contradictions, including completed work still marked active and blocker links to removed issues. Change another record only when this update requires it and its update is permitted; report a deferred correction instead of claiming consistency when permission is missing.

The update is complete when the selected records match the established result and their affected cross-references agree; report any unresolved input or deferred update.

## Output

```markdown
Updated: {record paths and established results, or none}
Deferred: {record paths and reason, or none}
Input needed: {unresolved decision or missing fact, or none}
```
