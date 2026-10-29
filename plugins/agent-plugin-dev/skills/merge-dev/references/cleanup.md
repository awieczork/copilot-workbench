# Clean up the integrated cycle

Run this procedure from the target repository root only after a successful, verified `main` push and a request for branch cleanup.
Use the recorded `base`, `source_tip`, squash commit, and exact cycle branch from integration.
Each remote or local deletion requires its own explicit permission; integration or push approval authorizes neither.

## Verify and delete

1. Require `git rev-parse --verify refs/heads/<cycle-branch>^{commit}` to equal the recorded `source_tip`. Query the remote cycle ref with `git ls-remote --heads origin "refs/heads/<cycle-branch>"`; stop on command failure. If it returns a ref, fetch that exact ref, record its fetched tip, and require it to be an ancestor of `source_tip`. Stop on fetch or ancestry failure.
2. If step 1 found a remote cycle ref, require explicit permission to delete that exact ref before running `git -c push.followTags=false push --force-with-lease="refs/heads/<cycle-branch>:<recorded-remote-tip>" origin ":refs/heads/<cycle-branch>"`. Without permission, stop and retain it. The exact-value lease protects this one deletion only; it cannot force a commit update. Do not retry a stale lease. If deletion fails or is refused, stop, retain the local branch, and report the remote state as unknown. If step 1 found no remote ref, do not issue a deletion.
3. Run `git ls-remote --heads origin "refs/heads/<cycle-branch>"`. Continue only when it exits successfully and returns no matching ref. A failed query is unknown, even with empty output; a matching ref is still present. In either case, retain the local branch and report completed effects.
4. Repeat the clean `main` check, confirm the local cycle ref still equals `source_tip`, verify remote `main` still contains the squash commit, and rerun the exact squash verifier with the recorded IDs. Require explicit permission to delete that exact local cycle branch, then repeat step 3's remote-absence query immediately before deletion. Only after a successful, empty result run `git branch -D -- <cycle-branch>`; squash commits do not make the source branch an ancestor. If local deletion fails, report that remote cleanup completed and the local branch remains.

Stop after a failed proof, push, deletion, or remote-absence check, or a changed source tip.
Retain any remaining cycle branches and report completed effects; cleanup is not atomic.
