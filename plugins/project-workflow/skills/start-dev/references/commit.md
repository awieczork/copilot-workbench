# Prepare a cycle commit

Use this procedure only while the current session has an active `start-dev` grant for the exact selected cycle branch.
The grant permits local commits only; it does not permit a push, integration, publication, or a commit on another branch.

## Rules

- Use the commit message format the project instructions define. Otherwise, use Conventional Commits messages in the form `type: summary`, adding `(scope)` only when the summary does not identify the area. Use `feat` and `fix` for their specified changes, and `docs`, `chore`, `refactor`, or `test` for other work.
- Include only paths within the cycle scope that `start-dev` reported, and stop on a changed path that the project's scope rules exclude. Ask about unclear ownership.
- List staged, unstaged, and untracked paths separately. Review the exact staged and unstaged diffs and the contents of in-scope untracked files before staging.
- Treat in-scope pre-staged paths as part of the proposed commit. If any pre-staged path is outside scope, stop and ask the user to resolve it; do not alter the index.
- If a path is both staged and unstaged, ask whether to commit the staged selection or the complete worktree file, and do not commit while that choice is unresolved. Preserve its staged content until the user decides; whole-file `git add` requires the complete-file choice. Check the chosen content before committing; checks of different worktree content do not validate the staged selection.
- Permission to carry existing dirty work does not by itself authorize a commit. Commit only after confirming the active grant, exact branch, cycle scope, and complete checked change.
- Never stage all files, switch branches, bypass hooks, amend, rebase, reset, or rewrite history.

## Procedure

1. Run `git branch --show-current`, `git status --short --branch`, and `git status`. Stop unless the current branch is the exact branch with the active grant. Stop on detached `HEAD` or an unfinished Git operation.
2. Use `git diff --cached --name-only`, `git diff --name-only`, and `git ls-files --others --exclude-standard` to list staged, unstaged, and untracked paths separately. Apply the scope and staged-selection rules above.
3. Resolve [screen_paths.sh](../scripts/screen_paths.sh) from this skill's loaded location, then run `bash` with its absolute path from the target repository root. Ask the user to resolve every flagged in-scope secret or large path before staging it; leave unrelated flagged paths untouched and report them.
4. When the commit changes user-visible behavior and the project keeps a `CHANGELOG.md` for the affected scope, reconcile its `## Unreleased` entry by the [changelog rule](../../../com.github.copilot/rules/changelog.instructions.md). Use only the in-scope commit group and keep existing versioned entries unchanged, except where release preparation adds one. Apply the same staged-selection rules to changelog files.
5. Show the exact in-scope paths and proposed commit message. After resolving unclear scope and screening results, stage only paths covered by the active grant with `git add -- <exact paths>`, excluding unresolved partially staged paths and staged selections the user chose to preserve. The active grant does not require another approval for each such commit. Create the commit with normal hooks. Stop on a hook failure without bypassing it or changing remaining selections.
6. After the commit, rerun `git status --short --branch` and the separate staged, unstaged, and untracked path commands. Report the commit and every remaining path.

## Screening result

The [screening script](../scripts/screen_paths.sh) takes no arguments and requires Bash, Git, `sort`, and GNU `stat`.
It prints one `{path}<TAB>{secret|large}` line per finding across staged, unstaged, and untracked non-ignored paths; one path can have both findings.
`large` means a file exceeds 5,000,000 bytes.
Output is not capped; exit `0` means screening completed, not that no findings exist.
On a nonzero exit, stop before staging because screening did not complete.
The script reads Git path state and file sizes; it does not stage or modify files.
