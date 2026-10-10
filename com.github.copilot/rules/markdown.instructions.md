---
name: "Markdown"
description: "Use when writing or changing an ordinary Markdown document, such as a README, project documentation, notes, or a report. Supplies GitHub Flavored Markdown syntax, style, and language rules. Not for agent customization files."
applyTo: "**/*.md"
---

# Markdown

Write every document in GitHub Flavored Markdown (GFM), and apply the rules below from memory instead of fetching the specification.

## Scope

Do not apply these rules to a file that customizes an agent, such as an instructions, agent, prompt, or skill file, a file bundled in a skill folder, or a model memory file such as `AGENTS.md` or `CLAUDE.md`, because those files follow their own syntax authorities.

When a rule under Style or Prose language conflicts with a convention the edited document already applies to every instance of the same element, keep the document's convention and name the conflict in your result.
Apply the syntax and rendering rules in the other sections without this exception.

When a document opens with a YAML frontmatter block, leave its keys, order, and quoting untouched unless the request targets them.

The content column of a list item is the first column after its marker and the following space.

## Blocks

- Write headings as ATX: one to six `#` characters followed by a space, indented no more than three spaces.
  Never use Setext underlines, because the same `-` line makes a heading under text and a thematic break after a blank line.
- Start a document with one level-1 heading that names its subject, use that level once, and increase heading levels by one at a time.
- Open a fenced code block with at least three backticks and a language identifier, and close it with the same character and at least the same count.
  When the content contains a run of backticks, make the fence longer than that run, or fence the block with tildes instead.
  Use `text` when no language identifier fits.
- Indent a fenced code block inside a list item to the content column of that item; an under-indented fence ends the list item's content.
- Never rely on a four-space indent to mark code; a reader cannot distinguish it from list continuation.
- Give a table a header row and delimiter row with the same column count, set alignment with `:` in the delimiter row, and escape a literal pipe inside a cell as `\|`.
  Give each body row the intended column count rather than relying on GFM to insert empty cells or ignore excess cells.
  Keep the table free of blank lines, which terminate it.
- Write a thematic break as three or more `-` characters alone on a line, preceded by a blank line.
- Separate every heading, list, table, block quote, and fenced code block from the surrounding text with one blank line.

## Lists and block quotes

- Use `-` for every unordered list marker and `1.` for every ordered one, so that inserting an item leaves the other lines unchanged.
  Changing the marker character starts a new list.
- Indent a nested list or a continuation paragraph to the content column of its parent item.
- Keep one list either tight throughout or loose throughout; a single blank line between two items makes every item render as a paragraph.
- Write a task list checkbox as `[ ]` or `[x]` after the list marker and one space.
- Prefix every line of a block quote with `>`, including its blank lines, rather than relying on lazy continuation.

## Inlines

- Use `*` for emphasis and `**` for strong emphasis.
  Do not use `_` delimiters because GitHub Flavored Markdown treats them differently inside words.
- Write strikethrough as exactly `~~text~~`; three or more tildes render literally.
- Write links inline as `[descriptive text](destination)`, with no whitespace between the text and `(`.
  Wrap a destination containing spaces in angle brackets.
  Use a reference definition (`[label]: destination`) only when the same destination appears three or more times.
- Link to a file in the same repository by a relative path that resolves from the linking document.
- When a URL itself must remain visible, wrap it in angle brackets so that GFM autolinks it.
- Give every image alt text that names what the image shows; GFM renders the alt text as plain string content.
- Escape an ASCII punctuation character with `\` when it would otherwise start markup, such as a leading `#`, `-`, or `>` on a line.
  Put a literal `<` or `&` inside backticks when it could form valid raw HTML or an entity reference.
- Use backticks for a path, filename, command, field name, or literal value, and add a longer backtick run when the value itself contains a backtick.
- Never emit `<script>`, `<style>`, `<title>`, `<textarea>`, `<xmp>`, `<iframe>`, `<noembed>`, `<noframes>`, or `<plaintext>`; GFM escapes them.
  Use raw HTML only for a construct GFM has no syntax for, such as a nested table, and keep Markdown out of the HTML block, because Markdown inside it renders only where blank lines separate it from the tags.
- Write an intentional line break with a trailing `\` rather than two trailing spaces, which no diff shows.

## Style

- Write one sentence per line and do not hard-wrap at a fixed column, so that a diff shows one changed sentence per changed line.
- Use a table when every item carries the same fields, a list when the items are alternatives or ordered steps, and a paragraph otherwise.
- Use sentence case in headings and list items, and open every item in one list with the same part of speech.
- Use bold for a term the document defines and italics for a word the sentence stresses; never use bold in place of a heading.
- Delete a sentence whose only content is what the next section contains.
- Leave no trailing whitespace, end the document with one newline, and use LF line endings.

## Prose language

- Continue the language the edited document already uses, and never mix two languages in one document.
- Keep code, identifiers, paths, and commands unchanged regardless of the prose language.

## Validation

After changing a document, check that every relative link and image path resolves from the document that contains it.
