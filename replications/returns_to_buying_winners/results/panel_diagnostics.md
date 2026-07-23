# Panel diagnostics — returns_to_buying_winners (Jegadeesh-Titman 1993)
Generated: 2026-07-22T18:14:21

## 1. Panel dimensions, columns, dtypes
rows x cols: 1,097,807 x 15
unique permnos: 5,522   unique months: 762
month range: 1926-07-01 .. 1989-12-01
  permno       int32              nulls=        0 ( 0.00%)
  month        datetime64[us]     nulls=        0 ( 0.00%)
  ret          float64            nulls=    3,778 ( 0.34%)
  ret_raw      float64            nulls=    3,778 ( 0.34%)
  ret_skip5    float64            nulls=    5,982 ( 0.54%)
  ret_skip5_raw float64            nulls=    5,982 ( 0.54%)
  cumret_3     float64            nulls=   17,283 ( 1.57%)
  cumret_3_raw float64            nulls=   17,283 ( 1.57%)
  cumret_6     float64            nulls=   34,325 ( 3.13%)
  cumret_6_raw float64            nulls=   34,325 ( 3.13%)
  cumret_9     float64            nulls=   51,111 ( 4.66%)
  cumret_9_raw float64            nulls=   51,111 ( 4.66%)
  cumret_12    float64            nulls=   67,644 ( 6.16%)
  cumret_12_raw float64            nulls=   67,644 ( 6.16%)
  me_millions  float64            nulls=    3,778 ( 0.34%)
rows with ret NaN but cumret_3 present (formation-only ghost rows): 3,778
first month with any cumret_3 non-null: 1926-10-01   cumret_12: 1927-07-01 (expected 1926-10 and 1927-07; the first 6-month formation for the Table VIII back-test is 1927-01, cumret_6 over 1926-07..1926-12)

## 2. Average stocks per month (ret non-NULL), by year and decade
  by decade (pre-1962 universe check, audit-1 M1 / P21):
    1926-1935: mean=   655.9  min=   528.2 (1926)  max=   719.3 (1930)
    1936-1945: mean=   776.0  min=   714.3 (1936)  max=   826.1 (1945)
    1946-1955: mean=   977.7  min=   867.8 (1946)  max=  1034.9 (1955)
    1956-1965: mean=  1399.8  min=  1034.2 (1956)  max=  2075.5 (1965)
    1966-1975: mean=  2307.3  min=  2100.4 (1966)  max=  2529.2 (1973)
    1976-1985: mean=  2223.1  min=  2063.0 (1985)  max=  2414.5 (1976)
    1986-1989: mean=  2008.6  min=  1972.0 (1989)  max=  2026.6 (1988)
  selected years:
    1927:    558.8 stocks/month
    1935:    691.4 stocks/month
    1941:    781.3 stocks/month
    1950:    984.1 stocks/month
    1960:   1080.6 stocks/month
    1965:   2075.5 stocks/month
    1970:   2277.8 stocks/month
    1975:   2449.4 stocks/month
    1980:   2213.2 stocks/month
    1985:   2063.0 stocks/month
    1989:   1972.0 stocks/month
  overall: min=523 (1926-07) max=2534 (1973-03)
  (NYSE + AMEX combined common-stock universe via dsenames PIT windows; pre-1962 the daily-file-era windows end at 1962-07 and the pre-daily-era windows cover the earlier period — counts are continuous across the 1962-07 split, P21)

## 3. Exact stock counts in formation months 1979-12 and 1989-11
  1979-12-01: ret=2238  cumret_3=2223  cumret_6=2209  cumret_9=2184  cumret_12=2174
  1989-11-01: ret=1959  cumret_3=1945  cumret_6=1912  cumret_9=1893  cumret_12=1871

## 4. cumret_6 summary stats
  overall: n=1,063,482 mean=0.079228 median=0.042859 std=0.353290 min=-1.000000 max=18.384538 p1=-0.560975 p99=1.249818   null%=3.13%
  1980:    n=26,157 mean=0.153549 median=0.090382 std=0.341268 min=-1.000000 max=5.145820 p1=-0.409957 p99=1.343894   null%=1.95%

## 5. Monthly ret stats and delisting-adjustment counts
  ret: n=1,094,029 mean=0.012762 median=0.000002 std=0.134847 min=-1.000000 max=7.499997 p1=-0.292909 p99=0.433778
  dsedelist events 1926-07..1989-12: 8,462 (dlret NULL: 2188, dlret sentinel <-1 mapped to NULL: 0)
  in-universe stock-months with a delisting event in the month: 3,377
    - dlret applied:                        2,873
    - dlret NULL, dlstcd>=500 -> -0.30:     470
    - dlret NULL, dlstcd<500  -> adj 0:     34
  ret < -0.90 stock-months (severe delistings): 134
  ret == -1.0 exactly (dlret=-1 worthless):     131

## 6. Cross-check vs crsp_202601.msf (20 random non-delisting permno-months, 1970-1985)
  matched 20/20   max|diff|=0.000539   mean|diff|=0.000042   n(|diff|>0.002)=0
    worst: permno=38906 1982-05 panel=0.040539 msf=0.04
    worst: permno=36740 1980-10 panel=-0.007020 msf=-0.006783
    worst: permno=35051 1974-10 panel=0.111979 msf=0.111923

## 7a. Delisting double-count verification (dsf final day vs dlret vs msf)
  D = daily compound of dsf.ret over the delisting month (excl. dlret);
  M = msf.ret; adj = (1+D)(1+dlret)-1. If M~=D and M!=adj, dsf excludes dlret.
  permno=11683 1975-07 dlret=-0.051724: D=-0.064516 M=-0.064516 adj=-0.112903 |M-D|=0.000000 |M-adj|=0.048387
  permno=32520 1979-10 dlret=-0.0981: D=-0.058826 M=-0.058824 adj=-0.151155 |M-D|=0.000002 |M-adj|=0.092331
  permno=36688 1984-09 dlret=-0.156174: D=-0.148148 M=-0.148148 adj=-0.281186 |M-D|=0.000000 |M-adj|=0.133038

## 7b. One delisting traced by hand
  permno=17793 dlstdt=1933-05-13 dlstcd=584 dlret_raw=-0.176471 dlret_clean=-0.176471
  dsf daily returns in the delisting month (valid days):
    [('1933-05-01', -0.268293), ('1933-05-02', 0.133333), ('1933-05-03', 0.088235), ('1933-05-04', 0.027027), ('1933-05-05', 0.026316), ('1933-05-06', 0.0), ('1933-05-08', -0.025641), ('1933-05-09', -0.052632), ('1933-05-10', -0.111111), ('1933-05-11', 0.0625), ('1933-05-12', 0.0), ('1933-05-13', 0.0)]
  D (daily compound, excl. dlret)      = -0.170733
  (1+D)(1+dlret)-1                     = -0.317074
  panel ret for 1933-05               = -0.317074   (match within 1e-6: True)

## 8. me_millions sanity
  all stock-months: n=1,094,029 mean=342.237452 median=41.273500 std=1636.103089 min=0.002500 max=102022.285125 p1=0.681000 p99=5130.976500
  1980:             n=26,559 mean=465.123517 median=86.914750 std=1705.059524 min=0.358500 max=40049.206875 p1=1.989580 p99=5706.950960
  units re-check 1989-12-29: sum(abs(prc)*shrout*1000) over ALL dsf stocks = $3.357T vs dsi.totval = 3.306e+09 (thousands of $ -> $3.306T; 6,813 index stocks); gap 1.52%

