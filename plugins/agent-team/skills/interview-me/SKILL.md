---
name: interview-me
description: "Interview the user until you share one confirmed understanding of a subject, before work starts or continues."
disable-model-invocation: true
---

# Interview me

Interview the user until you and the user share one confirmed understanding of the subject, so that the work that follows needs no guessing.

## Procedure

1. **Settle facts yourself:** read from the workspace and the session anything they can show, because a question the environment answers wastes the user's time.
   Ask only about a decision, or a fact only the user can supply.
2. **Map the subject:** sort each aspect into facts, assumptions, missing input, and decisions reserved for the user, and keep only the aspects that change the direction or the result.
3. **Ask:** for one local ambiguity, ask one question.
   Otherwise ask in rounds, through #tool:vscode/askQuestions when you hold it and in chat when you do not.
   Ask the questions whose answers bear on each other in one round, and hold a question whose options come from an answer not given yet for a later round, because its options may change.
   Between rounds, gather the facts the answers made available, and reopen a settled aspect only when new evidence invalidates it.
4. **Close:** when every aspect you kept is settled or deferred by the user, present the summary in the output format and ask the user to confirm or correct it.
   When the user corrects it, return to step 3 for the affected aspects.
5. **Resume:** after the user confirms, resume the work the interview interrupted.
   When no work had started, wait for a separate direction, because confirming an understanding is not permission to act.

## Rules for each question

- Put one decision in each question, and split a question that carries two.
- State the consequence when the choice changes the result, the cost, or the risk.
- Recommend an answer only when the evidence or the user's stated goal supports one, and name the assumption it rests on.

## Output format

```markdown
**Understanding:** {the subject in one sentence}

**Facts:** {each established fact with its evidence}

**Your decisions:** {each decision and input the user supplied}

**Deferred:** {what is deferred or outside this understanding}

**Assumptions and missing input:** {each item, labelled assumption or missing input}
```
