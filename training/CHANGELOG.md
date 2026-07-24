# Change log — every change cites the failure that caused it

Standing rule: no prompt, gold, perturbation, or grader change lands without
a commit + an entry here naming the observed failure it fixes. Speculative
rules are not accepted. (The improver-agent contract inherits this rule.)

## Prompt evolution (the only artifact the optimizer may edit)

**v1 -> v2 — flat status definitions replaced by an ordered decision
procedure (quarantine gates, then qualified conditions, else accepted).**
WHY: clean baseline failed in both directions at once — three real accepted
cases downgraded to QUALIFIED (asset growth, FF92, 52wh: over-weighting
absent-cache/weaker-t caveats) while the boundary set scored 1/5 including
reversed-legs -> ACCEPTED, a quarantine->ACCEPTED violation. Adjacent-status
ambiguity was the root cause; ordering resolves precedence mechanically.
WHY IT IMPROVES (mechanism): a flat rubric forces the model to weigh all
considerations at once, so verbose caveats crowd out decisive defects and
vice versa; an ordered procedure makes precedence part of the task itself,
which transfers to any record because it encodes HOW to decide, not WHAT
the answer is for particular papers.
Specific rules added, each to a specific miss:
- anchor-sign cross-check (reversed-legs perturbation was accepted);
- construction-difference = quarantine even when numbers land close
  (wrong-signal perturbation got only QUALIFIED);
- target-leakage rule, "closeness is never evidence of correctness"
  (target-copy perturbation);
- explicit no-downgrade caveat list: absent cache w/ prior audit, weaker t,
  missing secondary tables (the three real-case downgrades);
- verification definition: prior audit recomputation counts though the
  cache is now absent; candidate-only claims cap at QUALIFIED
  (stripped-verification perturbation was accepted).

**v2 -> v3 — quantified "materially attenuated" (less than ~half the
paper's claim; 80-110% with weaker t is a caveat).**
WHY: v2 downgraded FF92 (90% of paper magnitude) as attenuated. The corpus
distinction it had to encode: earnings (~50% magnitude) is qualified, FF92
(~90%) is accepted.
WHY IT IMPROVES: "material" was doing silent work; models resolve vague
quantifiers inconsistently run-to-run. Numeric bands turn a judgment call
into a measurement, and the band came from the corpus-wide contrast (50%
vs 90%), not from either single case, so it is a boundary, not a patch.

**v3 -> v4 — data-substitution rule (substituted/unavailable data =>
qualified).**
WHY: v3 flipped seasonality to ACCEPTED. Its 66-75% magnitude with a forced
FactSet->Compustat vendor substitution must stay qualified; magnitude
thresholds alone missed it because 66-75% > "half".
WHY IT IMPROVES: it names a genuinely distinct failure axis (evidence
quality vs result magnitude). Substitution can invalidate interpretation
even at decent magnitudes, so no magnitude threshold can subsume it; adding
the axis lets each rule stay simple instead of one rule overfitting both.

**v4 -> v5 (FROZEN) — data-substitution rule scoped by materiality AND
source-change; same-source vintage drift at 80-110% is a caveat.**
WHY: v4's rule was over-broad. FF92 missed QUALIFIED stably (3/3 runs)
because its record attributes a leg-level gap to a vintage composition
shift — MiniMax was correctly applying an incorrectly broad rule.
Disagreement routing was run first: the FF92 gold (accepted) was re-reviewed
and KEPT (same vendors as the paper, 90% magnitude, monotonic sort,
independent Fama-MacBeth corroboration) — so the prompt was fixed, not the
label.
WHY IT IMPROVES: scoping by materiality-AND-source separates "different
measurement of the same world" (vintage drift -- tolerable) from "a
different world measured" (vendor/universe/sample change -- interpretive
risk). That distinction is exactly the human rubric being distilled, and
each scoped rule now fires only on its own axis, which is what made 18/18
stable across runs rather than oscillating as v3/v4 did. Result: 18/18 majority-vote across train/dev/perturbations x3;
quarantine-recall 100% in all 15 runs.

**v5 -> v6 — status measures replication-record quality; weak in-window
results are findings, not defects.**
WHY: user-directed semantics clarification during minted-exam gold review
("I don't care if they're weak in window, I care about our replication").
The minted batch surfaced the ambiguity: 40/60 reference implementations
are faithful and verified but show weak/null in-window premia; v5 would
have downgraded them all.
WHY IT IMPROVES: it separates the two questions an evaluator conflates at
its peril -- "is the replication trustworthy?" (the status) and "what did
it find?" (the content). Downgrades now require a REPLICATION-SIDE cause
(substituted/restated source, truncation, implementation gap), which is
consistent with every existing corpus label (earnings=restated data,
seasonality=vendor swap, f_score=truncation) -- so the corpus gold needed
no changes, only the rule's stated scope. Honest weak findings become
successes, which is exactly the production incentive we want the evaluator
to enforce on future MiniMax replications.

## Grader changes (calibration phase only; hard-frozen since)

- Percent/decimal display variants in number-grounding. WHY: gold answers
  legitimately write 0.1047 as "10.47 percentage points"; self-test failed
  on contrarian.
- Narrowed legacy "tolerance" pattern. WHY: false positive on gold text
  "the paper's own tolerance" (FF92).
- Whitespace-robust STATUS token + broken-section-header normalization.
  WHY: MiniMax emission glitch splits words across blank lines
  ("QUARANT\n\nINE", "TR\n\nADE") — correct content, transport artifact.
- Contamination filter ignores round multiples of ten. WHY: answers echoing
  the prompt's own "80-110%" phrasing collided with a foreign anchor number
  (false-positive contamination).
Post-freeze: no changes. A grader change now requires reopening calibration
with a justification here.

## Gold/corpus changes

- time_series_momentum: added the paper's monthly R2 (0.14) to
  paper_anchors; reworded a caveat off "Tier" vocabulary. WHY: its gold
  answer cited a number missing from the record; vocabulary ban consistency.
- FF92: one gold_answer phrase reworded off "tolerance". WHY: same ban.
- FF92 status accepted KEPT after explicit disagreement-routing review (see
  v5 above) — recorded here because the alternative (relabeling) was
  considered and rejected with reasons.
- Splits: dev(7) carved into dev(4) + sealed(3) (contrarian, tsmom, share
  issuance). WHY: the optimizer sees dev results every iteration; a set the
  optimizer has never conditioned on is required for the final number.

## Perturbations

- P1 (momentum, verification stripped) also scrubs audit/recomputation
  language from caveats and adds an explicit no-audit statement. WHY: the
  original perturbation was internally contradictory — caveats still
  referenced the audit trail, so MiniMax reasonably counted it as verified;
  the miss was a perturbation bug, not a model error.

## Harness (transport, not judgment)

- Removed reasoning_split from API calls. WHY: it splits reasoning/content
  at an arbitrary token boundary, chopping the head off answers.
- <think>-strip + STATUS-recovery fallback + broad exception retry +
  4000-token default. WHY: observed truncated/empty answers (reasoning
  exhausting budget) and an uncaught socket timeout that killed a run.
- Panel checkers: 3 attempts at escalating budgets (2500/5000/7500). WHY:
  checker reasoning exhausted 2500 tokens before emitting JSON;
  a PARSE_FAIL on the verification checker wrongly downgraded asset growth.
- Panel aggregator fails closed: unparseable hard-gate checker =>
  QUARANTINE. WHY: asymmetric costs apply to infrastructure failure too.

## Architecture A/B: checker panel vs monolithic prompt (2026-07-24)

Panel (6 targeted checkers + mechanical aggregator + composer) vs monolith
v5 on identical cases and grader: train 4/9 vs 9/9, dev 1/4 vs 4/4,
boundary 4/5 vs 5/5. PANEL SHELVED.
WHY IT LOST: isolated checkers over-fire on caveat language without the
holistic record context (earnings/f_score/industry momentum wrongly
quarantined); scoped judgment rules (regression-only, vendor-vs-vintage)
degrade when split across contextless specialists; fail-closed parse
handling further inflated quarantines. Context integration is load-bearing
for these records — the opposite of the pre-registered hypothesis; recorded
as a negative result. Possible future variant (checkers as ADVISORS whose
findings feed the monolith, no status authority) deliberately NOT pursued
now: the monolith already meets the bar, and un-asked-for architecture is
how overengineering restarts.
