# Investment-first training records

These records teach a model to report what an investor can actually infer from
a replication. They are deliberately narrower than the legacy paper reports.

For this corpus, “replicated” does **not** mean that every paper table or number
was reproduced. A case is usable as a positive example when:

1. the implemented signal and portfolio timing represent the same economic
   trade as the paper;
2. the primary investment result has no known defect that could invalidate its
   sign or interpretation;
3. the result is expressed in the position an investor would take (for example,
   low-minus-high rather than a table's high-minus-low convention); and
4. data, replay, transaction-cost, and scope limitations are stated plainly.

Corollaries are reassurance. They can increase confidence that the primary
result is not accidental, but missing reassurance does not by itself invalidate
a sound investment result.

`cases.json` uses three statuses:

- `accepted`: suitable as a positive demonstration.
- `qualified`: the primary result is informative, but an important
  implementation, replay, or investability limitation remains.
- `quarantine`: useful as an example of what the model must reject, but not as
  positive gold.

Do not train on the legacy `REPLICATED` verdicts, numeric quality scores,
per-cell tolerances, or Tier labels. Those fields were produced by the
candidate/evaluation loop and can reward target copying rather than correct
computation.

The intended weighting is approximately 80% primary strategy/result and 20%
reassurance/caveats. `run_minimax.py` makes a direct OpenAI-compatible MiniMax
call with the compact rules prompt. It needs only `MINIMAX_API_KEY`; no DSPy or
optimizer dependency is required.

A two-example few-shot version was tested and rejected: it copied
asset-growth persistence checks into the profitability answer. The rules-only
prompt was cheaper and stayed within the current case's evidence.

Examples:

```bash
python3 training/run_minimax.py \
  --case the_other_side_of_value \
  --mode rules

python3 training/run_minimax.py \
  --case the_other_side_of_value \
  --mode baseline
```
