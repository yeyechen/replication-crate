# Table 1: Sample Selection (Replication)

**Paper:** Balakrishnan, Bartov, Faurel (2009) — *Post Loss/Profit Announcement Drift*
**Period:** fiscal years 1976-2005 (120 fiscal quarters per paper)
**Tolerance:** ±2% on each count

## Replicated counts vs paper targets

| Stage | Firm-quarters (ours) | Firm-quarters (paper) | FQ flag | Distinct firms (ours) | Distinct firms (paper) | Firms flag |
|---|---:|---:|:---:|---:|---:|:---:|
| All firm-quarters with required quarterly data on Compustat and return data on CRSP during sample period 1976-2005 | 558,083 | 471,997 | GAP | 17,803 | 15,261 | GAP |
| With stock price five days prior to the quarterly earnings announcement date above $1 | 535,227 | 458,693 | GAP | 17,559 | 15,143 | GAP |
| Primary tests sample with additional data constraints to compute SUE (epspxq at q and q-12) | 459,106 | 359,909 | GAP | 15,284 | 12,824 | GAP |
| Primary tests sample with additional data constraints to compute book-to-market (ceqq, cshoq, prccq) | 518,066 | 448,500 | GAP | 17,464 | 15,101 | GAP |
| Primary tests sample with additional data constraints to compute accruals (ibq, oancfy, xidocy, atq at q and q-1, rdq >= 1988) | 317,828 | 267,416 | GAP | 13,612 | 10,695 | GAP |

## Panel metadata

- **panel rows**: 558,083
- **panel cols**: 17
- **distinct gvkeys (raw panel)**: 17,803
- **distinct permnos (raw panel)**: 18,240
- **rdq range**: 1976-01-02 .. 2005-12-30
- **cells within tolerance**: 0/10

## Per-cell comparison

| stage                                 |   ours |   paper |   abs_diff |   pct_diff_pct | within_tol   |
|:--------------------------------------|-------:|--------:|-----------:|---------------:|:-------------|
| primary_all (firm-quarters)           | 558083 |  471997 |      86086 |          18.24 | False        |
| primary_all (distinct firms)          |  17803 |   15261 |       2542 |          16.66 | False        |
| primary_after_price1 (firm-quarters)  | 535227 |  458693 |      76534 |          16.69 | False        |
| primary_after_price1 (distinct firms) |  17559 |   15143 |       2416 |          15.95 | False        |
| supp1_sue (firm-quarters)             | 459106 |  359909 |      99197 |          27.56 | False        |
| supp1_sue (distinct firms)            |  15284 |   12824 |       2460 |          19.18 | False        |
| supp2_bm (firm-quarters)              | 518066 |  448500 |      69566 |          15.51 | False        |
| supp2_bm (distinct firms)             |  17464 |   15101 |       2363 |          15.65 | False        |
| supp3_accruals (firm-quarters)        | 317828 |  267416 |      50412 |          18.85 | False        |
| supp3_accruals (distinct firms)       |  13612 |   10695 |       2917 |          27.27 | False        |
