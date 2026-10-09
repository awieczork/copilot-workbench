# Release note rules

Apply these rules only while drafting the user-facing changelog entry and GitHub release body.

`CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Write no sentence in `CHANGELOG.md` about that convention or about the file's own format; the entries alone carry the document.

The closing checklist restates these rules on purpose, as a separate pass over a finished draft rather than as emphasis.

## Prepare the release body

Use the [Changelog Entries](../../../../com.github.copilot/rules/changelog.instructions.md) instruction for bullet language and user-facing phrasing.
Treat the current `## Unreleased` bullets as working material that may need to be updated, merged, or removed before approval.
Use one approved, final-state entry as the source for both the versioned `CHANGELOG.md` entry and the GitHub Release body.

## Verify release evidence

- Verify every technical detail against the `origin/main..develop` diff before writing it.
- Classify every changed path and user-visible capability in that diff as covered by an approved bullet or as an internal change with no changelog entry.
- Resolve every user-visible capability into one approved final-state bullet before asking for release-note approval.
- State the classification for every omitted change in the approval question.
- Exclude a change that alters no command, path, output, or message the user meets.
- Remove intermediate or superseded states from the draft instead of preserving them as development history.
- Leave no TODO, placeholder, or unverified claim in the approved body.

## Group the entry by impact

Group notes by theme, and put the most important theme first.
Judge each change by its user-facing content rather than by its commit label or file name.

Use these Keep a Changelog sections in this order:

```markdown
## [<version>] - <YYYY-MM-DD>
### Added
- The `explorer` worker provides the added user result.
### Changed
- The `interview-me` skill provides the changed user result.
```

Place the newest version entry above previous entries.
Move the approved final-state entry out of `## Unreleased` and into the versioned entry.
Retain an empty top-level `## Unreleased` heading for future changes.
On the initial release, remove the placeholder sentence `No plugin version has been released.` when it is present.
Omit an empty `###` subsection.

Use the complete approved versioned entry, including its version heading, date, subsections, and bullets, unchanged in `CHANGELOG.md` and the GitHub Release body.

## Check the draft before approval

Read the draft once more against this checklist and repair each failure before asking the owner to approve it.

- [ ] Every `## Unreleased` source bullet complies with the [Changelog Entries](../../../../com.github.copilot/rules/changelog.instructions.md) instruction.
- [ ] Each bullet names the changed component or capability near the start and states a distinct final user result.
- [ ] Each versioned and GitHub Release bullet starts with the changed component or capability and does not repeat `Added`, `Changed`, or `Fixed` from its subsection heading.
- [ ] The draft contains no intermediate, superseded, or commit-history-only bullet.
- [ ] Every technical detail, path, and name in the draft appears in the `origin/main..develop` diff.
- [ ] The version, the date, and the section order match the entry shape above, and no empty section is present.
- [ ] The complete approved entry is the exact text prepared for both `CHANGELOG.md` and the GitHub Release.

List every repair with its location, the current text, and the replacement in the approval question, so the owner approves the repaired body rather than the first draft.
