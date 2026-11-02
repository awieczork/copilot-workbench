# Evidence checks

Use the checks for the analysis at hand; record what was not checked when a missing observation limits the result.

## Joins

Before joining, identify the intended grain and count matched, unmatched, and duplicate keys on each side, including missing keys.
State whether the relationship is one-to-one, one-to-many, or many-to-many, and compare it with the relationship the measure requires.
After each join, compare rows and distinct grain keys before and after it, so that dropped records and fan-out are visible.
For example, summing an account-level balance after joining to several transactions per account repeats that balance; aggregate at the intended grain or explain why the repetition is valid.

## Data splits

For each named split pair, count shared entity identifiers and compare date ranges.
Judge overlap against the intended prediction or evaluation setting: the same entity or future information in another split can make a result look better than it will be on new data.
Report the overlap and its consequence rather than treating overlap alone as proof of leakage.

## Diagnostic and inferential claims

Name an alternative explanation that could also produce the observation, then choose a comparison or measurement that would distinguish it from the proposed explanation.
Check whether selection, missing data, changes over time, or a third variable could affect that comparison.
Report disagreements without averaging them away, and name the evidence needed when the available data cannot distinguish the explanations.
