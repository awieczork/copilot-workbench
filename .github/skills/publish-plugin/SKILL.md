---
name: publish-plugin
description: "Use when the owner runs it to publish a plugin release from `develop` to package-only `main`."
argument-hint: "[release goal or version]"
disable-model-invocation: true
---

# Publish a plugin release

Publish one release from `develop` to package-only `main`, and keep every public effect behind one confirmation from the owner.
Run `bash .github/skills/publish-plugin/scripts/release.sh <command>` from the repository root; it holds the package paths and the checks, so do not repeat them.
Ask the owner each question through #tool:vscode/askQuestions .

## Procedure

1. **Preflight:** run `preflight`, and stop and report its `FAIL:` lines.
   For a `PENDING:` line, an unpushed release commit from an earlier run at the tip of `develop`, ask the owner whether to publish its version, continuing at `build` in step 3, or to drop it with `git reset --keep <commit>~1`; both stay local until the push.
2. **Version and notes:** propose the next semantic version from the `## Unreleased` bullets, greater than the newest `v*` tag and not yet tagged.
   Reconcile the `## Unreleased` bullets by the [changelog rule](../../../rules/changelog.instructions.md), and check each bullet against `git diff --name-status origin/main develop -- $(bash .github/skills/publish-plugin/scripts/release.sh allowlist)`.
   Note each user-visible change in that diff that no bullet covers.
3. **Commit and build:** move the entry under a `## [<version>] - <YYYY-MM-DD>` heading above the previous entries, keep an empty `## Unreleased` heading, set `version` in `plugin.json`, and update `PROJECT-STATUS.md` to the released state by the [project status rule](../../../rules/project-status.instructions.md).
   Commit them with `git commit -m "chore(release): prepare v<version>" -- plugin.json CHANGELOG.md PROJECT-STATUS.md`, which leaves other staged paths out, then run `build <version>`, which prints the snapshot commit, or a `FAIL:` line or Git's error with a non-zero exit.
4. **Confirm once:** show the version, the output of `notes <version>`, the uncovered changes, and both commits, and ask one question that covers creating the annotated tag `v<version>` on `main`, pushing `develop`, `main`, and the tag to `origin`, and creating the GitHub release.
   When the owner corrects the notes, amend the release commit with `git commit --amend --no-edit -- CHANGELOG.md`, rerun `build`, and ask again; when the owner declines, run `clean` and keep the local commits, which the next run offers to publish or drop.
5. **Publish:**

   ```bash
   git tag -a "v<version>" main -m "Release v<version>"
   git push --atomic origin develop main "v<version>" || { git tag -d "v<version>"; exit 1; }
   bash .github/skills/publish-plugin/scripts/release.sh notes <version> | gh release create "v<version>" --verify-tag --title "v<version>" --notes-file -
   ```

   Then run `clean`, and report the version, the commits, the tag, the release result, and `git status --short --branch`.

The release is done when the atomic push and the GitHub release report success.

## Rules

- Push only with `--atomic`, and create the GitHub release only with `--verify-tag`, because a partial push or a release that creates its own tag publishes the wrong commit.
- Never force-push, move a published tag, or retry a rejected push, and leave the GitHub CLI authentication unchanged, because each of these acts on shared state the owner controls.
- When a step before the push fails, report the failed command and the effects already completed, run `clean`, and stop; every effect is local, so the next run recovers from it.
- When `gh release create` fails after the push succeeded, report that the tag and branches are public, and give the owner the release command from step 5 to run again.
