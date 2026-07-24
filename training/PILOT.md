# MiniMax pilot — 2026-07-23

## Outcome

Correcting the case record did most of the work. A compact rules prompt was
enough to make MiniMax M3:

- accept the freshly replayed gross-profitability result;
- quarantine QMJ despite its superficially close headline numbers; and
- distinguish paper targets, candidate observations, and external
  corroboration.

No DSPy or prompt-optimization framework was used.

## Profitability replay

`the_other_side_of_value` was rebuilt in an isolated `/tmp` replication root
using read-only ClickHouse queries. The SQL filter was corrected from
`ret > -1` to `ret >= -1`, restoring 274 valid total-loss stock-month returns
in the 2,284,523-row panel. The regenerated `results/table_2.md` is byte-for-byte
identical to the committed file. The core result therefore remains:

- gross GP/A high-minus-low: 0.317% per month, t = 2.506;
- FF3 alpha: 0.543% per month, t = 4.582; and
- HML loading: -0.453.

The 72 MB generated cache is preserved locally under the case's ignored
`data/` directory. It is not committed.

## Prompt comparison

All calls used the same corrected profitability evidence.

| Prompt | Result | API tokens |
|---|---|---:|
| Generic baseline | Economically accurate, but no acceptance status and an ambiguous “HML spread” label | 1,436 |
| Full two-example few-shot | Correct status, but copied asset-growth persistence claims into the profitability answer | 2,852 |
| Compact rules only | Correct `ACCEPTED` status, grounded trade/results/reassurance, no cross-case claims | 2,478 |

The full few-shot mode was removed from the runner. Its extra examples both
cost tokens and created evidence contamination. The remaining default is the
rules-only prompt.

## Negative-control result

The same rules-only prompt classified `quality_minus_junk` as `QUARANTINE` and
named the actual blockers: wrong beta construction, non-per-share growth,
incorrect accounting timing, mismatched risk factors, and no persisted monthly
factor/leg series. This is the behavior the legacy tolerance/Tier system did not
reliably elicit.

## Framework decision

DSPy is not justified at this stage. There are only a few corrected examples,
and the main error source is evidence quality rather than prompt wording. Add an
optimizer only after:

1. more cases have corrected primary-result records;
2. a small held-out set shows recurring prompt failures; and
3. the gain is measured against the compact direct prompt.
