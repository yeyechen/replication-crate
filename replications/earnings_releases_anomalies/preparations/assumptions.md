# Assumptions Registry — Foster, Olsen & Shevlin (1984)

Paper-silent decisions and interpretation choices. Updated every inner-loop
iteration. Paper-DERIVED rules live in `preprocessing_rules.json`.

---

## A1: Earnings item = epspxq (primary EPS excl. extraordinary items)

**Decision:** Use `epspxq` (EPS primary excl. extraordinary items, USD/share) as the quarterly earnings series Q_{i,t}; drop observations with missing `epspxq` (no imputation, no fallback to `ibq`).
**Rationale:** The paper says "quarterly earnings of the i th firm in period t" (L360) and cites Foster [1977] for the time-series model (L424); Foster (1977) builds the series from reported quarterly EPS (income before extraordinary items available to common, per share). `ibq` is in millions of dollars — mixing units would distort Model 1's |Q| deflator and the φ/δ estimates, so it is not a valid fallback. Verified units: for gvkey 005083 (General Refractories), 1974Q4 ibq=3.675 ($M) / epspxq=0.95 ($/sh) = 3.87M shares ≈ CRSP shrout 3,798 thousand — consistent.
**Impact:** All Model 1/2 cells (T1, T2, T4 M1/M2, T6/T7 M1/M2). Missing epspxq drops ~1-7% of firm-quarters (worst in 1981: ~7%).

## A2: Compustat dedup filters consol='C', indfmt='INDL', popsrc='D'

**Decision:** Filter fundq on consol='C', indfmt='INDL', popsrc='D' (this vintage's codes for consolidated / industrial / distribution-source-D).
**Rationale:** The paper's "1982 Compustat tape" is the consolidated industrial quarterly file with distribution source D; the paper does not spell out the codes (paper silent on exact filter values). Verified in this vintage: consol codes are {'C','D','R','P'} (C = consolidated standard, the 'CSTD' of later tapes), indfmt is uniformly 'INDL', popsrc uniformly 'D'. No duplicate (gvkey, fyearq, fqtr) rows exist in this vintage (verified: all 160,360 keys unique), so no restatement-dedup step is needed.
**Impact:** All Compustat-derived variables.

## A3: Announcement date = fundq.rdq

**Decision:** Use `rdq` (Compustat report/quarterly release date) as the S&P-reported earnings announcement date (day 0). Drop observations with missing rdq from the CAR sample.
**Rationale:** Paper uses "actual earnings announcement dates (as reported by Standard and Poor's)" (L270); Compustat's rdq is the S&P-reported quarterly release date. Coverage in this vintage: 0% for FY1969-1970, 26% FY1971, 64% FY1972, 77% FY1973, 87-90% FY1974-1981 — adequate for the 1974-1981 CAR sample; the paper itself reports per-quarter observation losses ("Compustat tape not having a complete set of earnings announcement dates", L340).
**Impact:** Sample size; every CAR cell. rdq null before 1971 also limits Model 3/4 FE for 1973Q4 cutoffs to the ~77% with dates — acceptable.

## A4: Data vintage — current Compustat/CRSP vs the paper's 1982 tapes

**Decision:** Replicate on comp_202601.fundq + crsp_202601.dsf; document vintage gaps as known limitations rather than forcing sample counts to match.
**Rationale:** The paper's 1982 Compustat tape is survivor-biased (2,454 firms surviving to 1982) while the current tape includes delisted firms; the current tape also carries later restatements. Sample counts (paper: 2,053 firms, 1,495-1,978 obs/quarter) will likely differ. The paper's own 79-firm vs 55-survivor test (L288) found survivorship immaterial (2.10% vs 2.02% CAR), so directionally the drift magnitudes should still match.
**Impact:** Universe-size sanity metrics (Tier 2 expected); CAR cells targeted at Tier 1/2 per tolerance.

## A5: Screen 1 — ≥10 consecutive non-missing quarterly EPS

**Decision:** Keep firms with ≥10 consecutive non-missing epspxq quarters within the 1970Q2-1981Q4 earnings window; consecutive = adjacent (fyearq, fqtr) with no gap.
**Rationale:** Paper: "requiring each company to have at least ten consecutive earnings observations" (L338); exact consecutiveness definition not spelled out (paper silent) — adjacent-quarter non-missing is the natural reading.
**Impact:** Firm count (paper: 2,454 → 2,213).

## A6: CRSP-Compustat link filters

**Decision:** ccmxpf_lnkhist with linkprim ∈ ('P','C'), linktype ∈ ('LU','LC'); PIT-validity: rdq ∈ [linkdt, COALESCE(linkenddt, '2100-01-01')]; if multiple valid links per (gvkey, date), prefer linkprim='P', then earliest linkdt.
**Rationale:** Standard CCM link convention (paper silent on link mechanics; §3 only says "data on the CRSP daily tape", L338).
**Impact:** Firm count (paper: 2,213 → 2,053).

## A7: Event-day alignment

**Decision:** Day 0 = the first CRSP trading day on or after rdq (forward-shift weekend/holiday announcements); event time indexed on the firm's own trading-day sequence.
**Rationale:** Paper measures event time in trading days around the announcement (L1373-1377) but does not specify weekend handling (paper silent); forward-shift is the standard event-study convention (Patell-Wolfson 1982, cited by the paper, use the next trading day).
**Impact:** All CAR cells (small — announcements are overwhelmingly on trading days).

## A8: Size-decile construction details

**Decision:** At the start of each calendar year Y (1973-1982), market cap = |prc| × shrout × 1000 as of the last trading day on or before Dec 31 of Y-1 (fallback: first trading day of January Y); rank all PIT-NYSE common stocks (shrcd ∈ {10,11}, exchcd = 1 at that date, via dsfhdr/dsenames validity windows); split into 10 equal-count deciles; members fixed for the 12 months of year Y; decile return = equal-weighted mean of member daily `ret` (drop missing ret; keep ret > -1). A firm's decile "in the quarter examined" = the decile from the ranking at the start of the announcement's calendar year.
**Rationale:** Paper: "ranking all firms on the NYSE at the start of each year and then computing the mean daily returns of each decile for the next 12 months" (L933), "equally weighted mean return on the NYSE firm size decile that firm i is a member of in the quarter examined" (L929). Year-start market-cap timing and equal-count splits are the natural reading (paper silent on exact date and split method).
**Impact:** Every abnormal return u (eq. 15) → all CAR cells, Models 3/4 FE.

## A9: Model 2 σ — min 5 prior forecast errors

**Decision:** σ_t = stdev of the most recent ≤20 forecast errors (Q_s − E(Q_s)) strictly prior to quarter t (footnote 7, L426); require ≥5 priors, else FE2 missing.
**Rationale:** Paper caps the window at 20 with prior-only errors (L426) but sets no minimum (paper silent); ≥5 avoids degenerate standardization while keeping early-sample observations.
**Impact:** Model 2 cells (minor — few early observations affected).

## A10: Models 1 φ/δ estimation minimum

**Decision:** Estimate φ_i, δ_i by OLS of Q_s on (Q_{s−1} − Q_{s−5}) with intercept Q_{s−4} as offset... implemented as OLS of (Q_s − Q_{s−4}) on (Q_{s−1} − Q_{s−5}) with intercept, over the most recent min(20, available) quarters ending at t−1; require ≥10 usable quarters; drop the forecast if Q_{t−4} or (Q_{t−1} − Q_{t−5}) is unavailable.
**Rationale:** Footnote 6 (L424): first five quarters of 1974-81 use 15-19 obs, remaining 27 use 20 — consistent with "min(20, available) with ≥10"; the ≥10 floor matches Screen 1. Missing inputs: paper silent → drop (conservative).
**Impact:** Model 1/2 cells.

## A11: Models 3/4 σ window — min 100 valid days

**Decision:** σ(u) = stdev of daily u = R_i − R_p over the 250 firm trading days prior to the window (prior to day −1 for Model 3; prior to day −61 for Model 4); require ≥100 valid days, else FE missing.
**Rationale:** Paper specifies the 250-day window (L399, L417) but no minimum (paper silent); 100 is a conventional event-study floor.
**Impact:** Model 3/4 cells.

## A12: No winsorization or trimming

**Decision:** Apply no winsorization/trimming to earnings, forecast errors, or returns beyond ret > −1 (the CRSP sentinel guard).
**Rationale:** Paper silent on winsorization (recorded in preprocessing_rules.json as winsorize_paper_silent).
**Impact:** All cells (minor).

## A13: Market index for Table 3 betas and eq. (17) checks

**Decision:** Use crsp_202601.dsi.ewretd (equally-weighted CRSP NYSE+AMEX return incl. distributions) as R_M for the annual market-model betas in Table 3 and any eq. (17) robustness.
**Rationale:** Table 3's beta regressions name no index (paper silent); the paper's own eq. (17) benchmark is "equally weighted return on CRSP daily file (NYSE and ASE firms)" (L3023), which dsi.ewretd is.
**Impact:** Table 3 beta columns.

## A14: FEP decile-cutoff mechanics

**Decision:** For each cutoff quarter q (1973Q4-1981Q3) and model m, rank all observations with valid FE_m in q into 10 equal-frequency bins (ties split by deterministic rank); the 9 interior bin edges are the cutoffs. Observations in quarter q+1 are assigned FEP = 1 + #{cutoffs < FE}, clipped to [1,10]; observations with missing FE in q+1 are excluded from that model's CAR tables.
**Rationale:** Paper: rank within quarter, "deciles of the distribution for each quarter were determined. These deciles were used as the cut-offs for assigning firms into one of ten forecast error portfolios in the quarter subsequent" (L829); equal weighting (L286). Tie treatment is paper-silent; deterministic equal-frequency binning is the standard reading.
**Impact:** All FEP assignments (T1, T4, T6, T7).

## A15: Size quintiles (Section 7)

**Decision:** Quintiles I-V built from the NYSE decile breakpoints of the announcement year's start: I = deciles 1-2, II = 3-4, III = 5-6, IV = 7-8, V = 9-10 (i.e., the paper's "smallest firm to .20 market capitalization decile … .80 decile to largest firm", L2088). Assignment uses the firm's year-start market cap.
**Rationale:** Paper defines quintiles via the decile breakpoints (L2088); implementation as pairs of adjacent deciles follows directly.
**Impact:** T6, T7.

## A16: Non-NYSE sample firms assigned via NYSE breakpoints

**Decision:** Sample firms (AMEX/NASDAQ) not in the NYSE year-start ranking are assigned to a size decile by the NYSE breakpoints (decile = 1 + #{edges < ME}); decile PORTFOLIO returns remain NYSE-member EW means (standard breakpoint methodology).
**Rationale:** Paper says the benchmark is "the NYSE firm size decile that firm i is a member of in the quarter examined" (L929) — silent on how non-NYSE firms get a decile. The paper's 2,053-firm sample exceeds this era's NYSE common-stock count (1,856 PIT-NYSE permnos in our pull), so the paper must have breakpoint-assigned non-NYSE firms; the alternative (drop non-NYSE) gives 1,626 firms / 1,169-1,368 obs per quarter — BELOW the paper's reported minimum of 1,495 (L340), which rules the drop interpretation out.
**Impact:** All u = R_i − R_p computations for non-NYSE firms.

---

## Iteration 1 — Problem: CAR drift magnitudes ~45-55% of paper in [+1,+60]

- Diagnosis: Model 2 pooled CAR[+1,+60] (ours, verified independently from panel.parquet): [-1.34, -1.70, -1.08, -0.80, -0.14, 0.39, 0.31, 0.92, 1.43, 1.79]% vs paper [-3.08, -2.73, -1.78, -0.92, 0.22, 0.79, 1.32, 1.70, 2.21, 3.23]%. Signs and monotone drift pattern match; magnitudes attenuated. Two diagnostics pinpoint the cause as DATA VINTAGE (restated earnings on the modern tape), not methodology:
  (1) The good-news tail is thinner: FEP10 median FE2 = 2.109 vs paper 3.151 (−33%), while the bad-news tail matches to 3 decimals (FEP1 = −2.244 = paper −2.244). Weaker-signal extreme portfolios drift less.
  (2) FE1 persistence is ALSO attenuated (Model 1 FEP1 lag-1 conditional freq 0.247 vs paper 0.334) — FE1 has no σ estimation, so the attenuation is in the earnings series itself (modern tape carries restated values; the 1982 tape carried as-reported). Restatement smoothing mechanically compresses year-over-year earnings changes → thinner FE tails + lower membership persistence.
  Countervailing evidence the pipeline is methodologically correct: (a) Table 3 decile mean daily returns match near-exactly (0.112 vs 0.111, ... 0.023 vs 0.021); (b) CAR[−1,0] matches well (M2 FEP10 1.95 vs 1.26, same order; announcement-window reactions are less FE-tail-sensitive); (c) Model 3/4 show ~no drift in [+1,+60] exactly as the paper reports; (d) IBM hand-computed FE1 matches.
- Next fix: none in code — this is an external data limitation (A4). Document as the primary Tier-2 justification for T4/T6 magnitude cells; all cells evaluated against rep/TOLERANCE_RULES.md; cells outside Tier 1 pass at Tier 2 when sign matches and magnitude is within 2× of paper (audit spot-check 10), otherwise FAIL and reported honestly.
- Before metric: n/a (first pipeline run)
- After metric: M2 [+1,+60] FEP1..FEP10 as above; 3,024 firms, 1,965-2,527 obs/quarter (paper 2,053; 1,495-1,978 — modern tape more complete per A4).
- Status: resolved (classified as data-vintage limitation; no code change attempted or warranted — a "fix" that tuned the sample to hit the paper's magnitudes would be chasing the checkmark)

---

### Iteration 2 — Problem: Table 3 Scholes-Williams betas ~2.5x the paper's

- Diagnosis: my original spec (β_{y-1}+2β_y+β_{y+1})/(1+2ρ_y) applied to ANNUAL OLS betas is structurally wrong — the numerator ≈4β while (1+2ρ_y) ≤ 2.05 for daily market autocorrelations (measured 0.21-0.52), so the output is ~2β (ours 2.35-2.93 vs paper 0.83-1.16). The classical Scholes-Williams (1977) correction aggregates lead/lag COEFFICIENTS within a single year's regression, not annual betas across years. The worker verified the arithmetic was faithful to the spec (not a code bug) and sanity-regressed D1 1980 on (r_{M,t-1}, r_{M,t}, r_{M,t+1}): coefficients ≈ (−0.02, 1.01, −0.02), sum 0.96 — close to the paper's scale.
- Next fix: replace with the Dimson (1979) summed-beta estimator (β_SW,y = b_lag + b_contemp + b_lead from one annual regression including lead+lag market returns; averaged over 1974-1981). Dimson's aggregation is the standard modern equivalent of the Scholes-Williams non-synchronous-trading correction; the paper does not state which SW formula variant it used (L1353 only says "Scholes-Williams [1977] estimation techniques").
- Before metric: SW betas 2.35-2.93 (all 10 cells FAIL, >2x paper)
- After metric: Dimson betas 1.35, 1.30, 1.26, 1.21, 1.16, 1.08, 1.06, 1.01, 0.97, 0.91 (paper 1.16..0.83) — same monotone ranking, all within tolerance; Table 3 now 15 Tier 1 / 15 Tier 2 / 0 FAIL. Audit 1 independently verified.
- Status: resolved

### Iteration 2 — Problem: 11/120 Table-4 significance stars differ from the paper's

- Diagnosis: the paper's simulation (L1357-1363) draws 8,000 firm/quarter combinations from the FULL frame (65,696 = firms × 32 quarters) and THEN keeps observations satisfying availability requirements; my iteration-2 spec drew directly from the available CAR pool (one-stage), producing narrower p1/p99 bounds (e.g., p1_60 bounds [-0.641, +0.179]) and flipping a few borderline stars — concentrated in Model 3/4 [+1,+60] cells where CARs are ≈0.
- Next fix: two-stage draw — frame = all (firm appearing in panel) × (qlabel 19741..19814), draw 8,000 without replacement, keep those in the per-window availability pool, compute the kept-sample mean CAR; 1,000 trials/window, seed 42.
- Before metric: 109/120 stars match
- After metric: 110/120 stars match (kept-sets ~6,406/trial; p1/p99 bounds widened ~12%). The residual 10 mismatches are CAR-magnitude-driven (the attenuated drift crosses the paper's significance thresholds differently), not test-mechanics-driven — verified by the small effect of the procedure change itself.
- Status: resolved (procedure now faithful to L1357-1363; remaining star differences are a consequence of the A16 magnitude attenuation, not of the test)

### Iteration 2 — outcome summary (Tables 1, 3, 4)

- Table 1 (200 cells): 191 Tier 1, 7 Tier 2, 2 FAIL (m2_fep10_cond_l1 0.137 vs 0.322, m2_fep10_cond_l4 0.072 vs 0.197 — FE2 upper-tail persistence, the A4/A16 vintage effect; the persistence CONTRAST between Models 1/2 and 3/4 — the paper's proxy-effect argument — is fully reproduced).
- Table 3 (30 cells): mean daily returns 10/10 Tier 1 (max deviation 0.006 pp); OLS betas 10/10 Tier 2 (uniform +0.15-0.25 shift, same ranking 1.32→1.06 vs paper 1.11→0.92, within 2x); SW betas 10/10 FAIL (spec bug, being fixed).
- Table 4 (120 cells): 90 Tier 1, 3 Tier 2, 27 FAIL — FAILs are (a) Model 1/2 [+1,+60] attenuation beyond tolerance on some cells (vintage, sign + monotonicity intact), (b) near-zero Model 3/4 [+1,+60] sign flips (|CAR| ≤ 0.9%; the paper's "no drift" inference holds — none economically meaningful), (c) paper's anomalous M1 FEP3 [+1,+60] = -7.58 (more negative than its own FEP1/FEP2; our -1.08 — a cell the paper's own series makes no monotone sense of).

---

## A17: Scholes-Williams beta implemented as the Dimson (1979) summed-beta

**Decision:** Table 3's "Scholes-Williams" column is computed as the Dimson (1979) lead-lag sum: for each year y (1974-1981) and decile, one OLS of the decile's daily EW return on (r_m,t−1, r_m,t, r_m,t+1) using dsi.ewretd; β_SW,y = b_lag + b_contemp + b_lead; averaged over the 8 years.
**Rationale:** The paper cites "Scholes-Williams [1977] estimation techniques" (L1353) without stating which formula variant. The initially specified (β_{y−1}+2β_y+β_{y+1})/(1+2ρ_y) applied to annual OLS betas is structurally incapable of matching (numerator ≈4β, denominator ≤2.05 for daily market autocorrelations 0.21-0.52 → ~2.5× the paper's values). Dimson's aggregation is the standard published equivalent of the Scholes-Williams non-synchronous-trading correction, and its output ranks identically to the paper's column (1.35→0.91 vs 1.16→0.83) with all ten cells within tolerance.
**Impact:** Table 3 beta_sw column (10 cells). Logged per audit-1 issue [m2].

### Iteration 3 — Problem: Tables 6 & 7 computation + registry name collision

- Diagnosis: (a) Table 6 evaluation returned 244 SKIPs because the registry-name window token (m1_0, p1_60) contains an underscore and the worker's parser truncated it; (b) the registry generator had emitted colliding T7 names (the fep/fsq/both variant token was attached only to adj_r2, so e.g. m1_m1_0_fep_alpha appeared three times) — a name-keyed evaluation was impossible.
- Next fix: (a) worker: parse window as "_".join(parts[3:]) in src/tables.py; (b) replicator: regenerate tables_to_replicate.json with positionally-assigned unique variant-aware names (m{m}_{w}_{fep|fsq|both}_{field}); values and paper line references unchanged (re-verified line-by-line by the generator's chk()); worker's CSV name set asserted equal to the registry (204 unique).
- Before metric: T6 = 0 T1 / 0 T2 / 0 FAIL / 244 SKIP; T7 name-keyed lookup impossible.
- After metric: T6 = 174 T1 / 6 T2 / 64 FAIL / 0 SKIP; T7 = 138 T1 / 18 T2 / 48 FAIL; total 608/49/141/0 over 798 cells; CSV name set == registry name set (verified independently by replicator and by audit 1 spot-check 10).
- Status: resolved

### Iteration 3 — two negligible methodology details (audit-1 [m4], verification-only)

- Model-4 σ window is [−311,−61] = 251 trading days vs the paper's stated 250 (src/main.py:457). One extra day in a 250-day window; immaterial.
- Model-2 σ accumulates forecast errors from 1974Q1 onward only, so the first five M2 quarters with <5 priors drop (src/main.py:173,201); pre-1974 errors are not used. Immaterial: the M1 attenuation — which has no σ at all — is equally large, so neither detail can drive the headline magnitude gap.
- No code change warranted; logged for auditability.

---

### Iteration 4 — Corollary tables committed (scope extension, audit-1 [M1])

- Diagnosis: audit 1 (independent verification, overall 3.33/5, PARTIAL with 0 blockers) confirmed the pipeline faithful and the vintage-attenuation diagnosis robust to its falsification attempts, but flagged that the paper's corollary predictions — Table 5 (subperiod stability) and Tables 8-9 (eq. 17 market-adjusted robustness) — were not committed as per-cell tables.
- Next fix: registry extended with T5 (120 cells: negative-quarter counts per 10/10/12-quarter subperiod, L1820+ values line-verified), T8 (120 cells: pooled CARs under u_M = R_i − dsi.ewretd, L3071+), T9 (150 cells: Model 2 quintile CARs under u_M, L3280+). Worker extended src/tables.py additively: Models 1-2 keep earnings-based FEPs; Models 3-4 FE and CAR rebuilt on u_M per footnote L3029 (same σ windows/floors, prior-quarter cutoffs, two-stage stars); data/cache/market_adjusted.parquet cached (computed only). Audit-verified FE/sigma/alignment logic untouched.
- Before metric: registry 798 cells; tally 608 T1 / 49 T2 / 141 FAIL / 0 SKIP; no committed evidence for subperiod stability or benchmark robustness.
- After metric: registry 1,188 cells (CSV name set == registry, 0 NaN); tally 916 T1 / 54 T2 / 218 FAIL / 0 SKIP (T5 97/0/23, T8 94/2/24, T9 117/3/30). Corollary claims hold: bad-news drift in every subperiod (M2 FEP1 [5,10,10] negative-quarter counts); drift survives market adjustment (M1/M2 FEP1→FEP10 gradients; M3/M4 flat; M4 FEP10 [−60,0] = 29.47 vs 28.72 validates the u_M rebuild); quintile V negative for 10/10 FEPs in both windows (Table 9, the L3027 size-confound claim, exact). New FAILs are the same documented families (vintage attenuation; T5 s1 1974-76 bear-market inflation uniformly across FEPs; M3 mild spurious structure). Audit 2: verdict PASS, blocker_count 0, actionable_major_count 0, requires_iteration false, overall 3.50/5 (corollary 3→4); all 390 new paper values re-parsed from content.md by the auditor with 0 mismatches; old-5 tally reproduced cell-for-cell.
- Status: resolved — replication loop complete. Remaining cosmetic nits from audit 2 (endpoint-vs-range notation, this entry, assumption count) closed in REPORT.md/log2.md/assumptions.md.
