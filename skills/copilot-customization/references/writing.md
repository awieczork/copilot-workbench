# Writing guidance

Read this before writing or changing the content of any customization.
The rules apply to every artifact type; the type references add only what is specific to one type.

## Write only what changes behavior

- Give the artifact the context, procedures, and output templates its task needs, so that it works from its own text without the authoring conversation.
- Test each sentence, rule, example, and resource by asking whether the agent would get the task wrong without it; delete it when the answer is no.
- Delete the whole sentence when the agent would follow it by default, rather than trimming its words.
- Record what the agent cannot find by looking: an unwritten convention, the reason behind a choice, a gotcha; leave out what one file or one command shows.
- Leave out rules for anticipated needs until a correction, a failed run, or repository evidence shows the gap.
- Keep the main file to what every branch needs and move the rest behind conditional pointers, because an exhaustive file buries the rules that matter; a skill's `SKILL.md` stays under 500 lines.
- Leave out generic "verify", "double-check", and "think carefully" instructions, because current models already check their work and such wording adds extra rounds; name a specific check only where a known failure needs it.
- Ask for the result and the evidence behind it rather than the reasoning steps, because current models reason internally and can decline to reproduce that reasoning.

Preferred example:

```text
After editing Markdown, run `git diff --check`.
```

Avoided example:

```text
It is important to carefully validate the result after making changes so that the files maintain a high level of quality.
```

## Match strictness to fragility

- Give freedom where several approaches work, and pair it with the reason behind the goal, because the agent generalizes from the reason to cases the text does not name.
- Prescribe an exact sequence where a deviation breaks the result, and pair it with the check that confirms it.
- Calibrate each part of an artifact on its own, because most artifacts mix flexible and fragile work.
- Give one default approach instead of a menu of options, and name an alternative only together with the condition that selects it.
- Write for the model that reads the artifact: give a capable model the goal, the reason, and the completion criterion, and give a smaller model exact steps with their checks, because a detailed recipe constrains a capable model while a smaller model needs it.
- When models of different strength load the same artifact, keep it goal-oriented, and prescribe exact steps only where a deviation breaks the result.

## Write direct rules

- Address the agent with an imperative such as `Read`, `Compare`, `Create`, `Run`, `Report`, or `Stop`.
- State one action or rule per sentence or list item.
- Place a condition before its action.
- Give each non-obvious rule one short reason clause.
- State the intended behavior before a prohibition, because a bare prohibition puts the unwanted behavior into context without a target.
- Give a necessary prohibition its scope, its reason, and the allowed alternative.
- Do not claim priority over other instructions, because VS Code sets no precedence between instructions that load together; give the rule a scope instead.
- As the one exception, let an agent the user talks to state that the user's explicit instructions win over a skill's, because unclear or conflicting skill text otherwise makes the agent stop or depart from the request.

Match the form of a rule to the failure it prevents:

| Failure | Form |
| --- | --- |
| The agent skips a rule | A prohibition with its reason |
| The output has the wrong shape | A positive recipe that lists the parts in order |
| The output omits an element | A required slot in the output template |
| The behavior depends on a condition | A rule keyed to an observable condition |

Preferred example:

```text
Change the source schema and run `make generate`. Do not edit generated clients, because regeneration overwrites direct edits.
```

Avoided example:

```text
Never edit generated files.
```

## Use precise terms

- Use one term for one concept across the artifact and its resources.
- Preserve the exact spelling and case of artifact names, fields, paths, and tool names.
- Expand an abbreviation on first use.
- Replace vague modifiers such as `properly`, `carefully`, `appropriate`, `best practices`, and `as needed` with an observable condition.
- Name an exact path, command, value, or version only when the repository or official documentation confirms it.
- Prefer a well-known word that carries the intended meaning, such as `tight` or `idempotent`, to a phrase repeated across the artifact; define a word only when you coin it.

## Use emphasis sparingly

- Express importance through a reason or an ordering word such as `first`, `before`, or `after`, because forceful emphasis makes current models apply a rule too broadly.
- Bold only a term label or the short phrase that carries a key rule.
- Leave out importance labels such as `IMPORTANT`, `Critical`, or `Note well`, because they rank a rule without scoping it.
- Use an uppercase `DO NOT`, `ONLY`, `NEVER`, or `MUST` only for a hard limit whose misuse is costly, only inside a `Constraints` section, and always with a reason clause.
- Write a tool or skill trigger as "Use X when {condition}" instead of "If in doubt, use X" or "You must use X", because both make the agent use X far beyond the intended cases.

Preferred example:

```text
## Constraints

- NEVER run `git push`, because publication needs the user's approval.
```

Avoided example:

```text
IMPORTANT: ALWAYS CAREFULLY FOLLOW EVERY RULE IN THIS SECTION.
```

## Structure the content

- Create a section only for a distinct decision or ordered procedure.
- Keep a concept's definition, rules, and caveats under one heading.
- Put steps before reference material in the same file.
- Number steps when their order changes the result, and write the procedure of each step whose procedure the reading model could not infer from its goal.
- Group reference content by concern as rules or tables; an artifact may mix steps and reference content.
- Use a tight unordered list for three or more peer rules, a table when every item has the same fields, and prose for one rule or one coupled pair.
- Mark sections with Markdown headings.
- Wrap a clearly bounded block in an XML tag when a heading would blur where it ends, and use the shared tag names below, because the agent recognizes a block by a name it has seen before.
- Use one structure convention in every artifact of the same type, because consistency matters more than the choice between headings and tags.

| Tag | Wraps |
| --- | --- |
| `<input>` | Pasted variable content, such as user text, a log, or command output |
| `<example>`, inside `<examples>` when there are several | One example, kept apart from the instructions |
| `<document>`, with `<source>` and `<document_content>` | A quoted source document |

## Disclose context progressively

- Keep in the main file what every branch of the task needs.
- Move material that only some branches need into a bundled resource, and link it from the main file with the exact condition for reading it.
- Give each resource one purpose and keep links one level deep from the main file.
- Keep each rule in one place and point to it from everywhere else.
- Split an artifact only when activation, permissions, or lifecycle differ, and keep a coherent unit of work together, because overly narrow artifacts load together and conflict.

Preferred example:

```text
Only after the API returns a non-zero status, read `references/errors.md`.
```

Avoided example:

```text
Read the references for more information.
```

## Mark completion

- Give a workflow a checkable completion criterion for its core process and for each major step whose premature end would change the result.
- Make a criterion exhaustive when the work must cover every item, such as "every changed file has a verdict".
- Give reference content an exhaustive criterion, such as "every rule in this section applied", when skipping a rule is a likely failure.
- Leave completion criteria out of definitions, syntax tables, source lists, and minor steps, because they add length without changing behavior.

## Write examples and templates

- Give an artifact that returns a structured result a fenced output template with `{placeholder}` slots in the order the reader needs them, because the agent copies a shown shape more reliably than a described one.
- Prefer a short example to a paragraph that describes the same shape.
- Keep every detail of an example one you want copied, because the agent reproduces details of examples, including incidental ones.
- Add another example only when the first one does not produce the intended output, when it prevents a likely syntax error, or when it separates two close choices; vary the examples so that no incidental pattern repeats.
- Write the artifact in the style its output should have, because the agent mirrors the formatting it reads; an artifact that wants prose output keeps its own Markdown light.
- Label preferred and avoided examples, and use plausible placeholder data.
- Check every example presented as runnable with its parser, formatter, or type checker.

## Write descriptions and pointers

- Front-load the trigger in each `description`, `applyTo` pattern, and resource link.
- State in a `description` what the artifact does and when to use it, and add the closest case it must not handle when false activation is likely.
- Scope each trigger to the task the artifact serves, not to its domain, because a domain-wide trigger loads the artifact for every loosely related task.
- Give each distinct request branch one trigger, and collapse synonyms that name the same branch.
- Leave the steps out of a `description`, because an agent that reads a summary of the steps may follow the summary instead of the body.
- Remove identity the destination already supplies, such as the artifact type or name.

Preferred example:

```text
Create and validate Postgres schema migrations. Use when adding or changing a migration, or reviewing its rollout.
```

Avoided example:

```text
Create and validate Postgres schema migrations. Use when working with databases, queries, models, or persistence.
```

## Reference tools

Write a tool mention in the body as `#tool:<frontmatter-tool-name>` followed by a space, including before punctuation.

Preferred example: `#tool:web/fetch .`

Avoided example: `#tool:web/fetch.`

## Keep the artifact portable

- Bundle the resources the artifact needs and link them with relative paths.
- Keep the artifact usable without files, instructions, or conventions that exist only where it was written.
- Keep repository-specific facts when they define the intended behavior in the target repository.

## Check the writing

- [ ] Every sentence changes behavior or prevents a likely failure.
- [ ] Each rule is an imperative with its condition first, and each non-obvious rule has a reason.
- [ ] Each prohibition follows the intended behavior and has a scope, reason, and alternative.
- [ ] One term names one concept, and no vague modifier remains.
- [ ] No importance label or uppercase emphasis appears outside a `Constraints` section.
- [ ] Material every branch needs is inline, and every resource link has an exact reading condition.
- [ ] Completion criteria sit only on the core process, major steps, and reference content where skipping is likely.
- [ ] An artifact that returns a structured result has an output template.
- [ ] Every example shows only details meant to be copied.
- [ ] Every trigger names a task, not a domain.
- [ ] Step detail matches the model that reads the artifact.
- [ ] No contradiction remains within the artifact or with the artifacts that load alongside it.
