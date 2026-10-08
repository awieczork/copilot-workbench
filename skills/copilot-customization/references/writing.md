# Writing guidance

Read this before writing or changing any customization; the type references add only what one type needs.
Write for a capable model: it handles nuance well, takes wording literally, and does worse under detail it does not need.

## Decide what to write

- Write what the agent would get wrong without the text: the goal, the reason behind a non-obvious choice, the completion criterion where stopping early would change the result, and the facts it cannot find by looking, such as an unwritten convention or a gotcha.
- Leave out what the agent does by default, what one file or command shows, and generic "verify" or "think carefully" wording, and delete the whole sentence rather than trimming it.
- Add a rule only after a correction, a failed run, or repository evidence shows the gap, and word it for the class of cases, because a fix fitted to one run fails on the next.
- Ask for the result and its evidence rather than the reasoning steps, because current models reason internally.

## Match strictness to the work

- Give direction where several approaches work: the goal and its reason, because the agent generalizes from the reason to cases the text does not name.
- Prescribe exactly only what tolerates no variation, such as an irreversible step, an exact command, or a fixed sequence, and pair it with the check that confirms it; move logic that must run the same way every time into a script.
- Give one default approach, and name an alternative only with the condition that selects it.
- Write at the same level for every model; when a lighter model runs the artifact, narrow its task rather than lengthening its recipe.

## Word the rules

- Address the agent with imperatives, one rule per sentence, the condition before the action, and a short reason for a non-obvious rule.
- State the wanted behavior; keep a prohibition only for a hard limit, beside the wanted behavior, its scope, and its reason.
- Express importance through a reason or an ordering word such as `before`, in plain case, because uppercase emphasis and labels such as `IMPORTANT` make current models apply a rule too broadly or stop early.
- Use one term for each concept, and the exact spelling of names, fields, paths, and tools; replace vague modifiers such as `properly` or `as needed` with an observable condition.
- Name an exact path, command, value, or version only when the repository or official documentation confirms it.
- Describe the current state, and keep dates and history out of rules, because a dated statement goes wrong silently.
- Give a rule a scope rather than claiming priority over other instructions, because VS Code sets no precedence between instructions that load together; only an agent the user talks to may state that the user's explicit instructions win over a skill's.

Preferred example:

```text
Change the source schema and run `make generate`. Do not edit generated clients, because regeneration overwrites direct edits.
```

Avoided example:

```text
NEVER edit generated files.
```

## Place the content

- Keep a concept's rules, caveats, and examples under one heading, and put steps before reference material.
- Number steps only when their order changes the result, and write a step's procedure only where the model could not infer it from the goal.
- Keep in the main file what every use needs, move what only some uses need into a resource, and link it one level deep with the exact condition for reading it.
- Keep each rule in one place and point to it from everywhere else.
- Split an artifact only when activation, permissions, or lifecycle differ, because overly narrow artifacts load together and conflict.
- Wrap pasted input, an example, or a quoted document in `<input>`, `<example>`, or `<document>` tags when a heading would blur where it ends.

## Templates and examples

- Give an artifact that returns a structured result a fenced output template with `{placeholder}` slots.
- Prefer a short example to a description of the same shape, and keep every detail of it one you want copied, because the agent reproduces incidental details too.
- Write the artifact in the style its output should have, because the agent mirrors the formatting it reads.
- Check every example presented as runnable with its parser, formatter, or type checker.

## Descriptions, triggers, and names

- Front-load the trigger in each `description`, `applyTo` pattern, and resource link.
- State what the artifact does and when to use it, with one trigger for each distinct task rather than its whole domain, and add the closest case it must not handle when false activation is likely.
- Keep a description to two or three short sentences, without its steps or the identity its location supplies, because descriptions load on every request and an agent may follow a summary of the steps instead of the body.
- Keep the description and the body in step: the body handles every case the description names, and the description names every case the body handles.
- Write a tool or skill trigger as "Use X when {condition}", because "If in doubt" or "You must" wording makes the agent use X far beyond the intended cases.
- Name an artifact for what it covers.

Write a tool mention in the body as `#tool:<frontmatter-tool-name>` followed by a space, including before punctuation.

## Keep the artifact portable

- Bundle the resources the artifact needs and link them with relative paths.
- Keep it usable without files or conventions that exist only where it was written, except repository facts that define its intended behavior there.

## Check the writing

- [ ] Every sentence changes behavior, and nothing restates a default.
- [ ] Strictness matches the work: direction where approaches vary, exact steps only where nothing may vary.
- [ ] Rules state the wanted behavior in plain case, with reasons where they are not obvious.
- [ ] Each rule lives in one place, and every resource link has an exact reading condition.
- [ ] Every description is short, names its tasks, and matches its body.
- [ ] No contradiction remains within the artifact or with the artifacts that load alongside it.
