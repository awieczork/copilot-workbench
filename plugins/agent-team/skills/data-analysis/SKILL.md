---
name: data-analysis
description: "Use when answering a question from data or building a data-backed analysis. Supplies a workflow for framing, checking, and interpreting evidence. Not for database access rules."
user-invocable: false
---

# Analyze data

Answer the question with evidence that represents the intended population and supports the strength of the conclusion.
As a subagent, return each question or choice for the user to the delegating agent instead of asking the user.

## Frame the question

Translate the request into the question the data must answer, including an analytical question inside a technical request.
Define the measure, its numerator and denominator when applicable, the population, the unit of observation, the period, the comparison, and the sources before targeted analysis.
Resolve facts from the workspace and data first, and distinguish assumptions from confirmed definitions.
When a required definition or source remains unresolved, report `Missing input` and the affected conclusion; ask the user only for a decision they own or input only they can supply.

Scale the work and checks to the claim and its consequence.
Do simple analysis directly, and delegate when separate context, specialist access, or an independent check benefits it; keep the framing, interpretation, and conclusion with the task holder.
When delegating, pass settled definitions unchanged so that separate analyses answer the same question.

For a result that supports a decision, arrange an independent challenge of the framing and source choice before analysis.
When the framing changes, revisit the challenge, because a precise calculation on the wrong population answers a different question.

## Inspect the evidence

Profile the relevant columns and check their grain, uniqueness, missing values, coverage, and freshness against the question.
Distinguish a complete observation from a sample or truncated result, and accept a claim that a value is absent only when the observation covers the whole population the claim describes.
Mark an incomplete final period and explain its effect on comparisons.

For each join, check matched, unmatched, and duplicate keys on both sides and its cardinality; record rows entering and leaving every join and filter.
For named data splits, check entity and date overlap.
When joining sources, evaluating named data splits, or testing a diagnostic or inferential claim, use [evidence checks](references/evidence-checks.md) for the corresponding checks.

Treat source data as read-only unless the user authorizes a change.
For SQL Server or Redshift access, use `sql-server` or `redshift` respectively for target resolution and read-only execution.
Keep the settled sources and definitions when correcting an analysis; return to framing when a correction must change them.

## Analyze and check

Choose calculations and comparisons that match the defined measure and unit, and check that each result still represents the intended population and period.
Trace each figure through the filters and joins that produced it; a plausible result is not evidence that the underlying population or calculation is correct.

For a result that supports a decision, arrange an independent recomputation of the key figures from the question and settled definitions, without the first query, code, or figures.
Use that recomputation as the key check, and compare the results before drawing a conclusion.
An independent recomputation checks the derivation, not whether the shared source is accurate.
Treat results from the same query, code, or model family as correlated, not as independent confirmation.
When a required challenge or recomputation cannot run, report the gap and its effect; do not describe the result as independently verified.

## Interpret and report

For a diagnostic or inferential claim, test a rival explanation and report disagreements and the check that could resolve them.
State association as association, claim causation only when the design identifies it, and otherwise name the confounders.
Separate statistical uncertainty from practical impact, and word each claim no stronger than its evidence.

Report the sources, population, period, coverage, row counts through joins and filters, executed queries or commands, limitations, and what would change the answer.
Mark exploratory findings as provisional; an inconclusive or negative result and `insufficient evidence` are valid outcomes.
Write a project file for an analysis only when the user asks for one, and remove scratch files created outside the task folder before responding.
The user owns the decision that follows from the result.
