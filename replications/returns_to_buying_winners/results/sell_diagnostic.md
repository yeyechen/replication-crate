# PART 0 — residual sell-shortfall diagnostic (READ-ONLY)
Generated: 2026-07-22T21:04:53

Hypothesis: partial-month stock-months (few trading days) are INCLUDED in our EW
decile means via the raw daily compound, whereas a monthly-file-era vintage (the
paper's 1990 CRSP) EXCLUDES months for which CRSP produced no msf record with a
non-NULL return. Nothing in src/ treatment or data/ is modified by this diagnostic.

## 1. msf coverage set (crsp_202601.msf, ret IS NOT NULL, 1965-02 .. 1990-06)
  (permno, month) stock-months in the set: 1,406,859

## 2. PA 6/6 member stock-months (cohorts formed 1965-01..1989-12, raw deciles, h=1..6)
  SELL (decile 1): member stock-months with ret_raw non-NULL: 378,306 (all member stock-months incl. NULL ret_raw: 389,916)
    ABSENT from the msf set: 3,210  (0.849% of non-NULL members)
    mean ret_raw of ABSENT stock-months:  -0.036193
    mean ret_raw of present stock-months: 0.008350
  BUY (decile 10): member stock-months with ret_raw non-NULL: 367,489 (all member stock-months incl. NULL ret_raw: 388,308)
    ABSENT from the msf set: 4,350  (1.184% of non-NULL members)
    mean ret_raw of ABSENT stock-months:  0.016094
    mean ret_raw of present stock-months: 0.016297

## 3. PA 6/6 sell EW series with absent-msf stock-months EXCLUDED from the means
  (recomputed over the full strategy cohort set, formed 1964-07..1989-11,
   so the base reproduces the Table I PA 6/6 series exactly; 486,138 member
   stock-months fall outside the msf coverage window — of which 2,338 in
   Jan-1965 enter the strategy mean — and are KEPT in both means, unevaluable)
  base  sell: mean=0.008110  t=1.6151   (pre-A13 Table I raw primary was 0.006227, t=1.28; moved under the A13 timing correction)
  new   sell: mean=0.008544  t=1.7020
  shift:      +0.000434 per month
  new   buy-sell: mean=0.008364  t=2.7690   (base buy-sell 0.008797)
  residual vs paper: 0.0079 − 0.008110 = -0.000210
  FRACTION OF RESIDUAL CLOSED: (0.008544 − 0.008110) / (0.0079 − 0.008110) = -2.0626 (-206.26%)
  (buy decile: 4,350/367,489 absent = 1.184% — expected negligible vs sell's 0.849%)

## 4. Universe sensitivity — distinct stocks per 1980 month-end (dsenames PIT)
  (a) exchcd IN (1,2) only   vs   (b) exchcd IN (1,2) & shrcd IN (10,11)
    1980-01-31: exch-only= 2394   exch+shrcd= 2220
    1980-02-29: exch-only= 2389   exch+shrcd= 2216
    1980-03-31: exch-only= 2388   exch+shrcd= 2216
    1980-04-30: exch-only= 2384   exch+shrcd= 2212
    1980-05-31: exch-only= 2376   exch+shrcd= 2203
    1980-06-30: exch-only= 2379   exch+shrcd= 2206
    1980-07-31: exch-only= 2383   exch+shrcd= 2210
    1980-08-31: exch-only= 2383   exch+shrcd= 2209
    1980-09-30: exch-only= 2378   exch+shrcd= 2203
    1980-10-31: exch-only= 2381   exch+shrcd= 2206
    1980-11-30: exch-only= 2379   exch+shrcd= 2202
    1980-12-31: exch-only= 2379   exch+shrcd= 2202
  1980 avg stocks/month: (a) exch-only = 2382.8   (b) exch+shrcd (current) = 2208.8   removed by shrcd filter: 174.0 (7.30%)
