# Writing guidance

Write for a capable model: it handles nuance well, takes wording literally, and does worse under detail it does not need.
Ask each question below of every line, section, and file while writing and while reviewing; a "no" marks a change to make.

## Decide what to write

- [ ] Does the text give what the agent would get wrong without it: the goal, the reason behind a non-obvious choice, the completion criterion where stopping early would change the result, and the facts it cannot find by looking, such as an unwritten convention or a gotcha?
- [ ] Does it leave out what the agent does by default, what one file or command shows, and generic "verify" or "think carefully" wording, with the whole sentence deleted rather than trimmed?
- [ ] Would removing each line, step, section, or file change a result?
- [ ] Did a correction, a failed run, or repository evidence show the gap behind each guideline, and is the guideline worded for the class of cases, because a fix fitted to one run fails on the next?
- [ ] Does it ask for the result and its evidence rather than the reasoning steps, because current models reason internally?
- [ ] Does it name the safe routine work the agent may do without asking, such as running the local tests and fixing the failures the change caused, because without that permission capable models stop to ask?
- [ ] Does the agent ask only when the answer would change the result, and only after it has prepared a concrete, reviewable result, because an early question ends the work too soon?
- [ ] When a step that a subagent may run asks the user, does the text tell a subagent to return the question to the delegating agent, because a subagent cannot ask the user?

## Match strictness to the work

- [ ] Is each guideline the principle itself, with its reason, rather than one instance of a broader principle, because the agent generalizes from the reason to cases the text does not name?
- [ ] Is each enumeration needed, or would the principle behind it steer the same way?
- [ ] Is exact wording kept for work that tolerates no variation, such as an approval gate, an irreversible step, an exact command, or a fixed sequence, and paired with the check that confirms it?
- [ ] Does logic that must run the same way every time live in a script?
- [ ] Does one guideline that scales the work to its consequence stand where the text would otherwise sort cases into levels or a wording scale?
- [ ] Does it give one default approach, and name an alternative only with the condition that selects it?
- [ ] Is it written at the same level for every model, with a lighter model's task narrowed rather than its recipe lengthened?

## Word the guidelines

- [ ] Is each guideline an imperative, one guideline per sentence, with the condition before the action and a short reason for a non-obvious guideline?
- [ ] Does each guideline state the wanted behavior, with a prohibition kept only for a hard limit, beside the wanted behavior, its scope, and its reason?
- [ ] Does a reason or an ordering word such as `before`, in plain case, carry the weight of each guideline, because uppercase emphasis and labels such as `IMPORTANT` make current models apply a guideline too broadly or stop early?
- [ ] Does a capable newcomer read each sentence one way only?
- [ ] Is one term used for each concept across the artifacts that work together, with the exact spelling of names, fields, paths, and tools?
- [ ] Is each vague modifier, such as `properly` or `as needed`, replaced with an observable condition?
- [ ] Is an exact path, command, value, or version named only when the repository or official documentation confirms it?
- [ ] Does the text describe the current state, with dates and history kept out of guidelines, because a dated statement goes wrong silently?
- [ ] Does each guideline have a scope rather than a claim of priority over other instructions, because VS Code sets no precedence between instructions that load together, and only an agent the user selects may state that the user's explicit instructions win over a skill's?
- [ ] Is each tool mention in the body written as `#tool:<frontmatter-tool-name>` followed by a space, including before punctuation, because VS Code reads a following `.` or `-` as part of the tool name?
- [ ] Does each principle change a concrete behavior, and each qualifier change behavior at all?
- [ ] Do all lines pull in the same direction?

Preferred example:

```text
Change the source schema and run `make generate`. Do not edit generated clients, because regeneration overwrites direct edits.
```

Avoided example:

```text
NEVER edit generated files.
```

## Place the content

- [ ] Are a concept's guidelines, caveats, and examples under one heading, with steps before reference material?
- [ ] Are steps numbered only when their order changes the result, with a step's procedure written only where the model could not infer it from the goal?
- [ ] Does the main file hold what every use needs, with what only some uses need in a resource linked one level deep from the main file with the exact condition for reading it, because a file linked only from another resource is read in part or missed?
- [ ] Is each guideline stated once, in the artifact that owns the work, with every other section, output template, and artifact that loads with it pointing to it instead of restating it or what the harness already does?
- [ ] Is an artifact split only where activation, permissions, or lifecycle differ, because overly narrow artifacts load together and conflict?
- [ ] Is pasted input, an example, or a quoted document wrapped in `<input>`, `<example>`, or `<document>` tags when a heading would blur where it ends?

## Templates and examples

- [ ] Does an artifact that returns a structured result give a fenced output template with `{placeholder}` slots, each carrying something the reader acts on, because the delegating agent reads the result by its sections?
- [ ] Does a short example replace a description of the same shape, with every detail of it one you want copied, because the agent reproduces incidental details too?
- [ ] Is the artifact written in the style its output should have, because the agent mirrors the formatting it reads?
- [ ] Was every example presented as runnable checked with its parser, formatter, or type checker?

## Descriptions, triggers, and names

- [ ] Does each `description` and resource link front-load its trigger?
- [ ] Does each `description` state what the artifact does and when to use it, with one trigger for each distinct task rather than its whole domain, and the closest case it must not handle when false activation is likely?
- [ ] Is each `description` two or three short sentences, without its steps or the identity its location supplies, because descriptions load on every request and an agent may follow a summary of the steps instead of the body?
- [ ] Does the body handle every case the `description` names, and does the `description` name every case the body handles?
- [ ] Is each tool or skill trigger written as "Use X when {condition}", because "If in doubt" or "You must" wording makes the agent use X far beyond the intended cases?
- [ ] Is each skill, tool, or reference named in an agent or instructions body part of its core work and loaded at a fixed point, such as a delegation skill before every brief, because a named skill reads as one the agent relies on?
- [ ] Is each artifact named for what it covers?

## Keep the artifact portable

- [ ] Are the resources the artifact needs bundled and linked with relative paths?
- [ ] Is a section of the same file referred to by its heading in plain words, never by an anchor link, because the prompt diagnostics read `[x](#section)` and `[x](file.md#section)` as file paths and report them as missing?
- [ ] Is the artifact usable without files or conventions that exist only where it was written, except repository facts that define its intended behavior there?
