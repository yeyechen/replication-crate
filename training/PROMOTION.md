# Evaluator promotion evidence (v6.4, frozen 2026-07-24)

PRODUCTION POLICY: majority of 3 independent calls per case (eval_minimax.py
run three times, or evaluate.py in the successor harness). Single-call usage
is NOT the evaluated policy.

Numbers (all majority-of-3 unless noted):
- Corpus (16 papers + 5 boundary perturbations): 18/18, three consecutive
  prompt versions.
- Held-out batch-2 test (14 never-tuned minted cases, one-shot): 13/14 (93%),
  zero quarantine->ACCEPTED in any individual run, flip rate 1/14.
- Sealed corpus trio (scored once under v6.2 lineage): 2/3; the miss drove
  v6.4's precedence fixes, so a NEWLY sealed set must be minted before any
  future re-promotion claim (known limitation).
- Pilot judgment events (5 papers, certified + uncertified states): 9/9.
Caveats: holdout n is small (14); evidence lives in the examiner-reserved
jkp-library repo by design (gold must stay outside worker-visible repos).
