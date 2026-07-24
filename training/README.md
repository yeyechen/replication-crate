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

## Optimizer toolkit (added 2026-07-24)

- `grade.py` — deterministic grader (status, grounding, contamination,
  legacy vocabulary, format, trade legs). FROZEN during prompt optimization,
  along with cases.json gold labels. `--self-test` re-verifies calibration.
- `eval_minimax.py` — runs MiniMax over a split (or the perturbations) with
  any candidate prompt (`--prompt`) and writes answers for grading.
- `make_perturbations.py` / `perturbations.json` — five boundary cases
  derived from real records (stripped verification, wrong signal, leaked
  targets, no reassurance, reversed legs) so the prompt learns the
  accept/qualify/quarantine boundary, not the paper roster.
- Splits: train 9 / dev 4 / sealed 3. The sealed cases are scored ONCE,
  after optimization ends (`eval_minimax.py --split sealed --once`).

## Pilot records (added 2026-07-24)

The corpus now also includes 5 MiniMax-authored, examiner-certified
replication records (provenance class: `pilot`), integrated via
`integrate_pilots.py` from `/home/alan/minimax-pilot/`. All 5 are `train`
split; 4 `accepted`, 1 `qualified` (debt_me: ~55% paper-window coverage).

## Promotion criterion and process (after Thinking Machines' expert-judgment
## recipe, thinkingmachines.ai 2026)

MiniMax's evaluator role is promoted to production only when, with a frozen
prompt:
1. status accuracy on dev is >= 90%, AND
2. NO quarantine-class case (real or perturbed) is ever answered ACCEPTED
   (asymmetric costs: trusting a contaminated result is the expensive error),
3. and the sealed set (scored exactly once, at the end) is consistent with dev.

Process rules:
- Disagreement routing: a status miss is first treated as a possible GOLD
  error (review the record and its evidence), and only then as a prompt
  defect. Contested cases are label QA.
- Rule ablation: once dev plateaus, each prompt rule is removed one at a
  time; rules whose removal does not degrade train+dev+perturbation scores
  are deleted.
- Expert prompt over optimizer machinery: hand-edited rules from failure
  traces; automatic prompt search only if hand-editing measurably plateaus.
