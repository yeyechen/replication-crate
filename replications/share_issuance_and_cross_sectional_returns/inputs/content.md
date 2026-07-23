# Page 1

THE JOURNAL OF FINANCE • VOL. LXIII, NO. 2 • APRIL 2008

# Share Issuance and Cross-sectional Returns

JEFFREY PONTIFF and ARTEMIZA WOODGATE*

## ABSTRACT

Post-1970, share issuance exhibits a strong cross-sectional ability to predict stock returns. This predictive ability is more statistically significant than the individual predictive ability of size, book-to-market, or momentum. Our finding is related to research that finds that long-run returns are associated with share repurchase announcements, seasoned equity offerings, and stock mergers, although our results remain strong even after exclusion of the data used in these studies. We estimate the issuance relation pre-1970 and find no statistically significant predictive ability for most holding periods.

Whether or not long-run stock returns following seasoned equity offerings, share repurchase announcements, and stock mergers reflect mispricing is the subject of debate in the finance literature. Proponents of the mispricing story include Loughran and Ritter (1995), who argue that long-run stock performance following seasoned equity offerings reflects negative abnormal returns, Ikenberry, Lakonishok, and Vermaelen (1995, 2000) who show that share repurchase announcements precede positive abnormal returns, and Loughran and Vijh (1997), who argue that acquirers that complete stock mergers experience negative long-run excess returns. All of these studies focus on returns with holding periods of 3 or more years. The behavioral interpretation of this literature is that firms issue equity when it is overvalued and retire equity when it is undervalued. However, inference from long-run studies is very sensitive to statistical specification issues. Mitchell and Stafford (2000), for instance, show that inference from some long-run return specifications is influenced by whether heteroskedasticity and cross-sectional correlation are controlled for adequately. Schultz (2003) shows that if the decision to issue or repurchase shares is correlated with past stock performance, a spurious estimation bias will produce average estimates of long-run returns that are similar in

*Pontiff is at Boston College’s Carroll School of Management. Woodgate is at the University of Washington and Russell Investment Group. We thank an anonymous referee, Malcolm Baker, Larry Dann, Ozgur Demirtas, Espen Eckbo, Cliff Holderness, David Ikenberry, Robert Kieschnick, Wayne Mikkelson, Jon Reuter, Andy Siegel, Cliff Stephens, Jeff Wurgler, Patrick Zimmerman, and workshop participants at Baruch University, Boston University, the University of Georgia, the University of Oregon, the University of Texas—Dallas, the University of Washington, as well as the Boston College brown bag workshop for useful comments. We thank Ken French for providing both data and detailed comments. Artemiza Woodgate would like to gratefully acknowledge financial support from the School of Business and Administration at the University of Washington, as well as the Albert O. Foster Endowment for their fellowships.

921

---

# Page 2

922

The Journal of Finance

magnitude to those in the long-run literature, even if the returns are generated under the null hypothesis of zero abnormal performance.

Using the method of Stephens and Weisbach (1998), we construct an annual issuance measure that we show is well suited to ascertain the events that are featured in the aforementioned long-run studies. Because we can construct this measure for all stocks, we use Fama–Macbeth (1973) estimation, thereby eliminating the statistical issues that plague the long-run literature. We perform an extensive analysis and comparison of our annual measure and the 5-year measure used by Daniel and Titman (2006).

Our study provides three interesting findings. First, using post-1970 data, both measures of share issuance are strongly related to the future cross-section of stock returns. Our results remain strong for holding periods ranging from one month to 3 years. The annual issuance measure is stronger than popular predictors of cross-sectional returns such as book-to-market, size, and momentum. Although we do not address whether the source of this predictability is mispricing or a rational response to an asset pricing model, it appears doubtful that these results can be explained solely by a risk-based asset pricing model. Book-to-market, size, and momentum typically explain between two to eight times of the cross-sectional return variation that is explained by annual issuance. Thus, it is unlikely that issuance is a market-wide risk factor. We cannot rule out that a non-risk-based asset pricing model, such as a transaction cost model, may explain these results.

Second, we show that our results are essentially unaffected by data associated with seasoned equity offerings (SEOs), repurchases, or stock mergers. We interpret this finding as evidence that post-SEO, post-repurchase, and post-stock merger return performance is part of a broader share issuance effect.

Third, using pre-1970 data we find a very different relation between both share issuance measures and the cross-section of future stock returns. Before 1970, 5-year issuance is insignificantly related to four of the return holding periods, and positively and significantly related to the second year’s annual return. Annual issuance has a negative and statistically significant relation in only 1 out of 40 specifications. The early sample’s departure from the latter sample appears to be driven by the World War II time period. Since the long-run literature, accounting-based issuance literature, and Daniel and Titman (2006) focus on the post-1970 time period, our pre-1970 finding suggests that their results may be sample specific. This interpretation of our results coincides with Gompers and Lerner (2003), who show that long-run initial public offering (IPO) returns before 1972 are generally insignificant, in stark contrast to the typical finding of long-run IPO underperformance in later samples. Our findings are consistent with evidence that share issuance is drastically different before and after 1970. Specifically, we find that since 1970, the proportion of firms with net annual share issuance has increased by 105% and the proportion of firms with zero net issuance has decreased by 61.3%.

The remainder of the paper is organized as follows. Section I discusses data and estimation procedures. Section II presents estimation results for the 1970

---

# Page 3

Share Issuance and Cross-sectional Returns

923

to 2003 period. Section III presents out-of-sample estimation results using pre-1970 data, and Section IV concludes.

## I. Data and Estimation

**Sample.** Our paper is motivated by long-run return studies and Daniel and Titman, both of which use data between 1970 and the present. Accordingly, we choose this time period as the starting point of our study. However, since our variable of interest, equity issuance (ISSUE), does not rely on Compustat data, we are able to extend our results to a sample before 1970. For each month, we select only those firms that have a nonmissing return entry in that month, and that have been in the CRSP database for at least 6 months, allowing us to compute their past 6-month returns. Our primary sample consists of all firm observations that are in the CRSP database as of January 1970. This leaves us with 2,494,343 firm-month observations. We conduct an out-of-sample test of the explanatory power of the share issuance variable for the September 1932 to December 1969 sample period. Our starting date of September 1932 allows for the lagged share issuance variables to be constructed as detailed below. For this period we have 568,449 firm-month observations.

**Share Issuance.** For each company we obtain from CRSP the number of shares outstanding and the *Factor to Adjust Shares Outstanding*. We compute the number of real shares outstanding, which adjusts for distribution events such as splits and rights offerings, as follows. We first compute a total factor at time $t$ , which represents the cumulative product of the CRSP-provided factor $f$ up to period $t$ inclusive:

$$
\text{Total Factor}_t = \prod_{i=1}^{t} (1 + f_i).
\quad (1)
$$

We compute the number of shares outstanding adjusted for splits and other events as

$$
\text{AdjustedShares}_t = \text{SharesOutstanding}_t / \text{Total Factor}_t.
$$

We use this measure of adjusted shares to compute annual share issuance at time $t$ as

$$
\text{ISSUE}_{t,t-11} = \text{Ln}(\text{AdjustedShares}_t) - \text{Ln}(\text{AdjustedShares}_{t-11}).
\quad (2)
$$

This measure is a logged version of the variable used by Stephens and Weisbach (1998), who show that repurchase announcements are associated with decreases in shares outstanding. Analogously our 5-year issuance measure is

$$
\text{ISSUE}_{t,t-59} = \text{Ln}(\text{AdjustedShares}_t) - \text{Ln}(\text{AdjustedShares}_{t-59}).
\quad (3)
$$

1540624. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540-6241.2008.01335 by University of Hong Kong Libraries, Wiley Online Library on 22/07/2020. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library. All rights reserved. Published by the applicable Creative Commons License.

---

# Page 4

924

$\text{The Journal of Finance}$

In our regression tables we refer to the annual issuance variable as $ISSUE$ and the 5-year Daniel and Titman issuance variable as $DT\text{-}ISSUE$ .

Both of our share issuance measures are constructed using the same method as Daniel and Titman (2006). We originally use the annual issuance measure in a previous version of this paper, independent of Daniel and Titman (2006). We choose an annual horizon for several reasons. First, accounting statements have a minimum reporting frequency of 12 months and CRSP uses these reports to construct their shares outstanding variable. Further, following Fama and French (1992), this frequency is consistent with our market capitalization and book value measures. Third, the annual issuance measure gives us a natural frequency to ascertain the correspondence of our share issuance data with Thompson’s SDC data. We choose the 5-year issuance measure in response to Daniel and Titman. Given Daniel and Titman’s main focus is on the importance of tangible and nontangible information, they do not fully investigate their important finding of return predictability with 5-year issuance. We build upon their study by comparing the predictive ability of their issuance measure with other commonly used predictive variables, as well as investigating the predictive ability of their measure in an earlier sample.

We cannot compute a 5-year issuance measure for firms that have been exchange-listed for less than 5 years. In such instances, we assign the firm’s 5-year issuance measure a value of zero and set the D-T dummy variable equal to zero; otherwise, the D-T dummy variable is set to one. Using this dummy variable allows us to use all stock returns regardless of whether the security is newly listed, without affecting inference of the slope coefficient on five-year issuance.

Sometimes there appears to be a timing mismatch between shares outstanding and CRSP-reported shares outstanding. It is CRSP’s intention to report shares outstanding when the information is publicly disclosed. We compare the timing of CRSP shares outstanding with Compustat shares outstanding and find that in some cases CRSP data correspond to the end-of-quarter date, and in others they correspond to dates a month or two after the end-of-quarter date. In order to be conservative and ensure that the shares outstanding numbers are available to investors, we only use share changes using 6 month-old CRSP data to predict returns. Thus, current returns (at time 0) are predicted either using $ISSUE_{-17,-6}$ or $ISSUE_{-65,-6}$ . Our decision is influenced by Fama and French (1992), who delay using book value data until at least six months after the fiscal year-end.

Some CRSP shares outstanding data appear to be erroneous. We create the following rule: If the number of shares outstanding changes by more than 20% and subsequently 95% of the change is reversed within three months, then we treat the change as an erroneous entry and we correct the shares outstanding to the level previous to the change. This correction affects a total of 2,189 observations (i.e., 0.07% of the total observations). The return estimation

---

# Page 5

Share Issuance and Cross-sectional Returns

regressions are calculated with and without this correction and our inference remains unaffected.$^{1}$

**Book-to-market.** We use the annual COMPUSTAT book value of common equity (data60) to construct the book-to-market variable. If the previous year’s book value is unavailable, we use the book value 2 years ago. We follow the Fama–French (1992) procedure in constructing the natural log of the book-to-market ratio. Book value is divided by size, where size is constructed using CRSP’s firm market value at the end of December the previous year (concurrent with the book value of common equity). This variable is used to forecast returns from July of the current year to June of the following year.

When the book value of equity is unavailable or it is negative, the book value variable is assigned a value of zero and the book value dummy variable is set equal to zero. Otherwise, the dummy variable is set to one. Using this dummy variable allows us to include all stock returns regardless of whether the security has COMPUSTAT coverage, without affecting inference of the slope coefficient on book-to-market.

**Size.** From CRSP, we construct the monthly market value of equity variable. We use the natural logarithm of the share price times the number of shares outstanding for that month. The SIZE from the month of June is used to predict returns from July of the current year through June of the following year.

**Momentum.** The momentum proxy is the 6-month holding period return of the stock between month 1 and month 6. The momentum variable is lagged by 1 month to avoid losing predictive ability due to positive autocorrelation attributable to bid-ask bounce.

**Returns.** The dependent variable in our regressions is the stock return for holding periods of 1 month and 6 months, as well as the annual stock return in the first, second, and third year. We examine returns in the second and third year. Since all of the long-run event study literature claims to find predictability for 3-year intervals. If return information is missing in CRSP for a given month, we construct the holding period return by replacing the missing stock return with the return of the CRSP equally weighted market portfolio with dividends reinvested (EWRETD). Most studies estimate holding period returns by ignoring missing returns. These studies’ holding period returns represent the return that one would receive from holding the stock, and once the stock delists, investing the remaining value in a zero-interest riskless security. Our holding period return represents the return from holding the stock until delisting and investing the remaining value in a CRSP equally weighted index. We believe

---

$^{1}$ An example is Advantage Marketing Inc. (CRSP PERMNO 85523). CRSP reports shares outstanding from the 31st of December 1999 to the 31st of March 2000 of 4.14 million shares. For the 28th of April 2000, CRSP reports 6.33 million shares outstanding, and from the 31st of May until the 11th of November 2000 the shares outstanding are reported to be 4.29 million. The quarterly company filings available on EDGAR report 4.24 million shares outstanding on the 15th of March, 4.29 million shares outstanding on May 8th, and 4.34 million shares by the 31st of August. We treat the CRSP entry of 6.33 million shares as an erroneous entry.

---

# Page 6

926

The Journal of Finance

that our holding period computation is more realistic, although we do not expect that it will significantly affect our inference.

*Estimation.* Our regressions estimate linear relations between returns and our independent variables. We do not know what the true functional form of our independent variables should be. Because of our ignorance regarding the correct specification of the independent variables, our results may be sensitive to extreme observations. Thus, in order to avoid giving any observations undue weight in the regression estimation, we winsorize all right-hand-side variables by setting the smallest and largest 1% of the observations equal to the value of the observation at the respective 1% tail. We do not transform the holding period returns that are used as dependent variables.

In the same vein as Fama and MacBeth (1973), for each month of data, we estimate separate regressions using returns as our dependent variable. We report the average slope coefficients, intercepts, and adjusted-$R^2$s. Using the same procedure as in Pontiff (1996), $t$-statistics for the slope coefficients are calculated with autocorrelation-consistent standard errors that consider the holding period overlap. This procedure estimates a regression using each month’s slope estimate where the residuals of the process follow an $n^{th}$-order autoregressive process, with $n$ equal to one minus the length of the holding period (in months). The standard error of the intercept from this estimation is used as the overlap-consistent standard error of our average slope coefficient. This technique is general in that it does not rely on the assumption of no monthly return autocorrelation.

## II. In-Sample Estimation Results

Panel A of Table I presents univariate statistics for the variables used in our study. Of particular interest is share issuance. Despite the fact that we are examining the log changes, this variable still exhibits a strong right skew. The mean annual issuance, 0.04, is greater than the value of share change at the 75th percentile, 0.03. This skewness seems less extreme for the 5-year measure in that the mean issuance of 0.12 is less than the 75th percentile, 0.14. We find that 56.6% of the time annual issuance is positive, 24.2% of the time it is zero, and 19.2% of the time is negative.$^2$

Panel C of Table I describes the time-series correlation structure of our in-sample (1970 to 2003) data. From the lead-lag structure of share issuance, it tends to be persistent. If the firm buys (sells) shares, it continues to buy (sell) shares in future periods. The positive correlation between $R_{-11,-0}$ and both $ISSUE_{-11,0}$ and $ISSUE_{1,12}$, shows that share issuance tends to increase (decrease) after periods of high (low) returns. The negative correlation between $ISSUE_{-23,-12}$ and $R_{-11,0}$ and $R_{1,12}$ is a precursor to our results—share issuance predicts returns. From Panel B, the correlations between future returns and book-to-market, market value of equity, and momentum are consistent with the

$^2$ Due to rounding, Table I cannot be used to infer the proportion of zero SHRCHG observations.

1540631. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540-631.2008.01335 by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020] 3e:the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 7

# Share Issuance and Cross-sectional Returns

## Table I

### Descriptive Statistics, 1970 to 2003

Panel A: Simple Statistics. The variables used are: the natural logarithm of the ratio of the book value of equity to the market value of equity measured at the end of December $t-1$ , $BM$ ; the natural logarithm of market equity measured at the end of the previous June, $ME$ ; the past 6 months stock return as a proxy for momentum, $MOM$ ; the change in the logarithm of the number of shares outstanding adjusted for splits to capture the effect of share repurchases and SEOs; $ISSUE_{-11,0} = [\text{Log(shares outstanding, } t) - \text{Log(shares outstanding, } t-11)]$ ; $ISSUE_{-59,0} = [\text{Log(shares outstanding, } t) - \text{Log(shares outstanding, } t-59)]$ ; and the 1-year return $R_{-11,0}$ contemporaneous with the $ISSUE_{-11,0}$ variable. The variables are measured at the end of December for the period between 1970 and 2003. Shares associated with splits and stock dividends are not included in the computation of shares outstanding. The sample observations range between 2,285,189 observations (for $MOM$ ) and 2,312,597 observations (for $ISSUE_{-11,0}$ ). Panels B and C: Correlations. Correlations between the variables defined in Panel A, that is, $ISSUE_{-11,0}$ , $ISSUE_{-59,0}$ , $BM$ , $ME$ , $MOM$ , and $R_{-11,0}$ , as well as the 12-month lead and lag of the change in shares outstanding variable, $ISSUE_{-23,-12}$ and $ISSUE_{1,12}$ , and the 12-month lead of the 1-year return, $R_{1,12}$ . Panel B shows the contemporaneous correlations, while Panel C looks at the time-series correlations.

<table>
  <thead>
    <tr>
      <th colspan="6">Panel A: Simple statistics</th>
    </tr>
    <tr>
      <th>Variable</th>
      <th>Mean</th>
      <th>25<sup>th</sup> Percentile</th>
      <th>Median</th>
      <th>75<sup>th</sup> Percentile</th>
      <th>Standard deviation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> $ISSUE_{-11,0}$ </td>
      <td>0.04</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.03</td>
      <td>0.15</td>
    </tr>
    <tr>
      <td> $ISSUE_{-59,0}$ </td>
      <td>0.12</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.14</td>
      <td>0.33</td>
    </tr>
    <tr>
      <td>BM</td>
      <td>-0.34</td>
      <td>-0.79</td>
      <td>-0.07</td>
      <td>0.00</td>
      <td>0.94</td>
    </tr>
    <tr>
      <td>ME</td>
      <td>11.11</td>
      <td>9.63</td>
      <td>10.97</td>
      <td>12.46</td>
      <td>2.02</td>
    </tr>
    <tr>
      <td>MOM</td>
      <td>0.06</td>
      <td>-0.16</td>
      <td>0.02</td>
      <td>0.22</td>
      <td>0.41</td>
    </tr>
    <tr>
      <td> $R_{-11,0}$ </td>
      <td>0.14</td>
      <td>-0.23</td>
      <td>0.05</td>
      <td>0.34</td>
      <td>0.88</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="6">Panel B: Contemporaneous correlations</th>
    </tr>
    <tr>
      <th>Variable</th>
      <th> $ISSUE_{-11,0}$ </th>
      <th>BM</th>
      <th>ME</th>
      <th>MOM</th>
      <th> $R_{-11,0}$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BM</td>
      <td>-0.08</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>ME</td>
      <td>0.01</td>
      <td>-0.30</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>MOM</td>
      <td>-0.01</td>
      <td>0.06</td>
      <td>0.03</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td> $R_{-11,0}$ </td>
      <td>0.03</td>
      <td>0.01</td>
      <td>0.05</td>
      <td>0.54</td>
      <td></td>
    </tr>
    <tr>
      <td> $ISSUE_{-59,0}$ </td>
      <td>0.39</td>
      <td>-0.08</td>
      <td>0.07</td>
      <td>-0.03</td>
      <td>-0.03</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="5">Panel C: Noncontemporaneous correlations</th>
    </tr>
    <tr>
      <th>Variable</th>
      <th> $ISSUE_{-23,-12}$ </th>
      <th> $ISSUE_{-11,0}$ </th>
      <th> $ISSUE_{1,12}$ </th>
      <th> $R_{-11,0}$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> $ISSUE_{-11,0}$ </td>
      <td>0.17</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td> $ISSUE_{1,12}$ </td>
      <td>0.14</td>
      <td>0.16</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td> $R_{-11,0}$ </td>
      <td>-0.03</td>
      <td>0.04</td>
      <td>0.06</td>
      <td></td>
    </tr>
    <tr>
      <td> $R_{1,12}$ </td>
      <td>-0.03</td>
      <td>-0.03</td>
      <td>0.04</td>
      <td>-0.03</td>
    </tr>
  </tbody>
</table>

literature on stock return predictability (for example, Fama and French (1992) and Jegadeesh and Titman (1993)).

Both issuance measures are negatively correlated with book-to-market ratios. If the anomalous performance of value over growth (Fama and French

---

# Page 8

928

The Journal of Finance

(1992)) is the outcome of mispricing, this result is consistent with firms acting opportunistically to exploit the mispricing. This finding is reasonable given that value firms’ insiders are more likely to buy their firm’s shares and growth firms’ insiders are more likely to sell their firm’s shares (see, e.g., Lakonishok and Lee (2001)). The relation between issuance and value is further analyzed by Bali, Demirtas, and Hovakimian (2005), who document that the value effect is particularly strong among firms that repurchase shares.

*Share issuance events.* Our first goal is to assess the extent to which share issuance proxies for SEO offerings, repurchase announcements, and merger announcements. We gather these data from Thomson Financial’s SDC Platinum. We select all SEOs from the U.S. common stock database that involved some primary shares and were not involved in a spin-off. Repurchase announcements and merger announcements come from the domestic merger database. Our search yields 14,556 SEOs, 15,800 repurchase announcements, and 36,683 merger announcements. We separate our merger announcement data into 16,724 mergers that SDC lists as involving common stock transactions and 19,959 mergers for which SDC does not have the means of payment. The SDC merger data include mergers in which the target is private or a subsidiary of another firm. The SEO data start in 1971, the repurchase data start in 1981, and the merger data start in 1978.

Panel A of Table II conducts Fama–MacBeth regressions of annual share issuance on various lead and lag dummy variables for whether the firm had an SEO, announced a repurchase, announced a stock merger, or announced a merger with unknown consideration. The second panel also considers levels of book-to-market, market value of equity, and momentum, from the period directly before the share change is calculated. Consistent with our expectations, as well as those of Stephens and Weisbach (1998) who show that repurchase announcements forecast lower share issuance, we find that the current period’s annual share issuance is negatively related to whether a repurchase was announced 1, 2, or 3 years ago, and is positively related to whether an SEO occurred in the past 12 months. Interestingly, an SEO announcement between months –35 and –24 is negatively related to current share issuance, implying a reversal in the total number of shares issued. Overall, the slope coefficients are large and statistically highly significant. A repurchase announcement within the current time interval corresponds to about a 4% to 6% (log) decrease in share issuance. An SEO in the current period is associated with about a 15% to 17% increase in issuance. A stock merger announcement is associated with a contemporaneous 11% increase in issuance, whereas a merger with unknown consideration is associated with a contemporaneous decrease in issuance of about 1% to 2%. This finding leads us to question the extent to which stock is used as consideration in these mergers.

Panel B of Table II incorporates cross-sectional firm proxies in the estimation. Consistent with the univariate results in Table I, book-to-market is strongly negatively related to issuance, that is, value firms repurchase stock while growth firms issue stock. The coefficient on size is the opposite of the simple correlations—large firms tend to issue less, whereas small firms tend to

1540631. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540631.2008.01335 by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020]. See the Terms and Conditions. https://onlinelibrary.wiley.com/terms-and-conditions on Wiley Online Library. All rights reserved by the applicable Creative Commons License

---

# Page 9

1546234, 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/j.1546-2341.2008.01355.x by University of Hong Kong Libraries, Wiley Online Library on 22/07/2020. See the Terms and Conditions, https://onlinelibrary.wiley.com/terms-and-conditions on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

# Share Issuance and Cross-sectional Returns

929

## Table II

### Fama–Macbeth Cross-Sectional Regressions with the Change in Shares Outstanding as the Dependent Variable, 1970–2003

The dependent variable is the change in the logarithms of the number of shares outstanding adjusted for splits to capture the effect of share repurchases and SEOs, $ISSUE_{-11,0}$ or a repurchase (REP) between the intervals $[-35, -24]$ , $[-23, -12]$ , and $[-11, 0]$ , and dummy variables for whether there was an SEO (SEO) or a merger and acquisition of unknown type (UMA) between the intervals $[-11, 0]$ and $[-23, -12]$ . Panel B looks at the relation between $ISSUE_{-11,0}$ and dummy variables for whether there was a stock merger and acquisition (SMA) or a merger and stock merger and acquisition (SMA) in the interval $[-11, 0]$ , an SEO or a repurchase between the intervals $[-35, -24]$ , $[-23, -12]$ , and $[-11, 0]$ , as well as firm-specific book-to-market, size, and momentum variables. The firm-specific variables are: the natural logarithm of the ratio of the book value of equity to the market value of equity from December $t-1$ , $BM$ ; a book-to-market dummy variable that is zero if BM is missing, $BM$ Dum; the natural logarithm of market equity from June $t-1$ , ME; the natural logarithm of the market value of the firm as of June $t$ and the past 6 months stock return as a proxy for momentum, MOM. The $BM$ , $BM$ Dum, $ME$ , and $MOM$ variables are all lagged by 12 months. Shares associated with splits and stock dividends are not included in the computation of shares outstanding. The Average $R^2$ is the average of the adjusted- $R^2$ obtained from the cross-sectional regressions, in percent. The results presented in the table are the regression coefficients and the $t$ -statistics in brackets. Multimonth holding period results utilize overlap consistent $t$ -statistics. These regressions are for the 197 months for which all variables are identified, from June 1983 to December 2003, with a total of 1,867,323 firm-observations. Coefficients with significant $t$ -statistics are bolded.

#### Panel A

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>REP $_{-35, -24}$ </th>
      <th>REP $_{-23, -12}$ </th>
      <th>REP $_{-11, 0}$ </th>
      <th>REP $_{12}$ </th>
      <th>SEO $_{-35, -24}$ </th>
      <th>SEO $_{-23, -12}$ </th>
      <th>SEO $_{-11, 0}$ </th>
      <th>SEO $_{12}$ </th>
      <th>ISSUE $_{-23, -12}$ </th>
      <th>ISSUE $_{-11, 0}$ </th>
      <th>SMA $_{-23, -12}$ </th>
      <th>SMA $_{-11, 0}$ </th>
      <th>UMA $_{-23, -12}$ </th>
      <th>UMA $_{-11, 0}$ </th>
      <th>Avg. $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>4.05</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>4.43</td>
    </tr>
    <tr>
      <td>(14.83)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>3.89</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>4.73</td>
    </tr>
    <tr>
      <td>(14.03)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>3.20</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>11.68</td>
    </tr>
    <tr>
      <td>(24.21)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>3.64</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>12.40</td>
    </tr>
    <tr>
      <td>(19.86)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>5.99</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.44</td>
    </tr>
    <tr>
      <td>(10.17)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>6.39</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.54</td>
    </tr>
    <tr>
      <td>(9.50)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>4.83</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>8.38</td>
    </tr>
    <tr>
      <td>(10.96)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>5.43</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>8.97</td>
    </tr>
    <tr>
      <td>(9.40)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>3.93</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>12.43</td>
    </tr>
    <tr>
      <td>(17.11)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

(continued)

---

# Page 10

930

The Journal of Finance

Table II—Continued

Panel B

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>REP$_{35-24}$</th>
      <th>REP$_{23-12}$</th>
      <th>REP$_{11,0}$</th>
      <th>REP$_{1,12}$</th>
      <th>SEO$_{35-24}$</th>
      <th>SEO$_{23-12}$</th>
      <th>SEO$_{11,0}$</th>
      <th>SEO$_{1,12}$</th>
      <th>SMA$_{11,0}$</th>
      <th>ISSUE$_{23-12}$</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>Avg. R$^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>17.14</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-1.26</td>
      <td>-0.80</td>
      <td>-1.11</td>
      <td>1.82</td>
      <td>2.99</td>
    </tr>
    <tr>
      <td>(12.58)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-7.47)</td>
      <td>(-2.05)</td>
      <td>(-9.88)</td>
      <td>(2.85)</td>
      <td></td>
    </tr>
    <tr>
      <td>17.08</td>
      <td></td>
      <td></td>
      <td>-3.88</td>
      <td></td>
      <td></td>
      <td></td>
      <td>17.33</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-1.13</td>
      <td>-0.85</td>
      <td>-1.13</td>
      <td>0.86</td>
      <td>8.65</td>
    </tr>
    <tr>
      <td>(12.29)</td>
      <td></td>
      <td></td>
      <td>(-11.47)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(31.40)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-7.12)</td>
      <td>(-2.00)</td>
      <td>(-10.22)</td>
      <td>(1.59)</td>
      <td></td>
    </tr>
    <tr>
      <td>15.67</td>
      <td></td>
      <td></td>
      <td>-3.71</td>
      <td></td>
      <td></td>
      <td></td>
      <td>16.67</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-0.95</td>
      <td>-0.59</td>
      <td>-1.07</td>
      <td>0.95</td>
      <td>10.64</td>
    </tr>
    <tr>
      <td>(13.29)</td>
      <td></td>
      <td></td>
      <td>(-10.85)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(32.99)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-7.07)</td>
      <td>(-2.02)</td>
      <td>(-11.06)</td>
      <td>(1.85)</td>
      <td></td>
    </tr>
    <tr>
      <td>16.83</td>
      <td>-1.47</td>
      <td>-2.96</td>
      <td>-3.33</td>
      <td>0.18</td>
      <td>0.33</td>
      <td>2.68</td>
      <td>16.63</td>
      <td>2.48</td>
      <td></td>
      <td>13.56</td>
      <td>-1.06</td>
      <td>-0.69</td>
      <td>-1.10</td>
      <td>0.79</td>
      <td>9.30</td>
    </tr>
    <tr>
      <td>(11.93)</td>
      <td>(-5.36)</td>
      <td>(-14.60)</td>
      <td>(-8.29)</td>
      <td>(0.81)</td>
      <td>(1.78)</td>
      <td>(7.57)</td>
      <td>(31.22)</td>
      <td>(9.64)</td>
      <td></td>
      <td>(5.77)</td>
      <td>(-7.16)</td>
      <td>(-1.78)</td>
      <td>(-9.94)</td>
      <td>(1.53)</td>
      <td></td>
    </tr>
    <tr>
      <td>15.42</td>
      <td>-1.02</td>
      <td>-2.46</td>
      <td>-3.30</td>
      <td>0.19</td>
      <td>0.03</td>
      <td>0.61</td>
      <td>16.30</td>
      <td>2.32</td>
      <td></td>
      <td></td>
      <td>-0.92</td>
      <td>-0.48</td>
      <td>-1.03</td>
      <td>0.90</td>
      <td>10.99</td>
    </tr>
    <tr>
      <td>(13.04)</td>
      <td>(-4.73)</td>
      <td>(-12.13)</td>
      <td>(-8.24)</td>
      <td>(0.91)</td>
      <td>(0.23)</td>
      <td>(1.75)</td>
      <td>(31.22)</td>
      <td>(8.86)</td>
      <td></td>
      <td></td>
      <td>(-7.20)</td>
      <td>(-1.72)</td>
      <td>(-10.78)</td>
      <td>(1.85)</td>
      <td></td>
    </tr>
    <tr>
      <td>18.04</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>12.54</td>
      <td></td>
      <td>-1.06</td>
      <td>-1.06</td>
      <td>-1.24</td>
      <td>1.41</td>
      <td>7.68</td>
    </tr>
    <tr>
      <td>(13.55)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(7.33)</td>
      <td></td>
      <td>(-6.84)</td>
      <td>(-2.83)</td>
      <td>(-11.51)</td>
      <td>(2.49)</td>
      <td></td>
    </tr>
    <tr>
      <td>17.97</td>
      <td></td>
      <td></td>
      <td>-4.71</td>
      <td></td>
      <td></td>
      <td></td>
      <td>16.71</td>
      <td></td>
      <td>12.49</td>
      <td></td>
      <td>-0.94</td>
      <td>-1.09</td>
      <td>-1.26</td>
      <td>0.49</td>
      <td>13.11</td>
    </tr>
    <tr>
      <td>(13.39)</td>
      <td></td>
      <td></td>
      <td>(-4.61)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(32.24)</td>
      <td></td>
      <td>(8.54)</td>
      <td></td>
      <td>(-6.52)</td>
      <td>(-2.60)</td>
      <td>(-12.59)</td>
      <td>(1.05)</td>
      <td></td>
    </tr>
    <tr>
      <td>16.33</td>
      <td>-1.11</td>
      <td>-2.51</td>
      <td>-4.32</td>
      <td>-0.07</td>
      <td>-0.23</td>
      <td>0.40</td>
      <td>15.87</td>
      <td>2.01</td>
      <td>11.90</td>
      <td>11.40</td>
      <td>-0.76</td>
      <td>-0.69</td>
      <td>-1.15</td>
      <td>0.56</td>
      <td>14.97</td>
    </tr>
    <tr>
      <td>(14.03)</td>
      <td>(-4.97)</td>
      <td>(-13.60)</td>
      <td>(-2.95)</td>
      <td>(-0.39)</td>
      <td>(-1.58)</td>
      <td>(1.36)</td>
      <td>(29.86)</td>
      <td>(9.28)</td>
      <td>(8.70)</td>
      <td>(5.75)</td>
      <td>(-6.10)</td>
      <td>(-2.71)</td>
      <td>(-13.12)</td>
      <td>(1.39)</td>
      <td></td>
    </tr>
  </tbody>
</table>


1546031. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1546031.2008.01353 by University of Hong Kong Libraries, Wiley Online Library on 22/07/2020. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 11

# Share Issuance and Cross-sectional Returns

issue more. This difference can be attributed to the fact that the Table I results are cross-sectionally and intertemporally pooled, whereas the Table II results are pure cross-sectional results. In the time series, one way that firms attain higher market capitalization is by issuing stocks.

Although our issuance measure picks up SDC share-changing events such as stock mergers, SEOs, and repurchases, the events documented by SDC only give us a partial view of share issuance. First, SDC coverage is not exhaustive. SDC only carries a subset of events. This coverage is more likely to be spotty in the 1980s than in the 1990s. Second, these events do not offer a complete list of how firms issue and repurchase stocks. Using the sample of S&P 100 firms Fama and French (2005) examine issuance activity between the years 1999 and 2001. Besides share repurchase, SEOs and mergers, Fama and French document that shares are issued through executive compensation, conversion of convertible debt, and warrant exercise. In comparing the differences between repurchasing and issuing firms, mergers are the number one explanation for differences between these groups, followed by share repurchases. The third explanation is executive compensation, which is followed by SEOs. We suspect that SEOs play a larger part in our sample than Fama–French’s S&P 100 sample, since Fama–French’s sample is geared toward large firms and other evidence in their paper points toward the fact that SEOs are more important issuance mechanisms for smaller firms. Also, executive stock options, a large component of executive stock compensation, were more pronounced during Fama–French’s sample than during the 1970s and early 1980s, which comprises the bulk of our sample.

*Return predictability.* Our test of return predictability in the 1970 to 2003 period is presented in Table III. Five return holding periods are considered; 1-month returns, 6-month returns, annual returns, second-year annual returns, and third-year annual returns. Panel A presents the 1-month estimation results. The first four rows present a “horse race” by considering separate estimation for book-to-market ($BM$), size ($ME$), momentum ($MOM$), annual issuance ($ISSUE$), and 5-year issuance ($DT-ISSUE$). The sign of the slope coefficients on $BM$, $ME$, and $MOM$ is consistent with previous literature. The slope coefficient on $BM$ is positive and statistically significant, although the estimate of the slope coefficient is smaller than that reported by Fama and French (1992). The slope on $MOM$ is positive but insignificant. The size effect is less pronounced in our sample period. The coefficient on $ME$ is negative and statistically significant.

From the monthly holding period regressions, annual share issuance has a slope of $-2.23$, implying that a one-standard deviation change (0.15) in share issuance is associated with a 0.33% decrease in the monthly cross-sectional return. The $t$-statistic on this slope is $-7.08$, which is considerably more significant than the $t$-statistics on $BM$, $ME$, and $MOM$. Five-year issuance has a slope of $-0.71$, implying that a one-standard deviation change (0.33) is associated with a 0.23% decrease in monthly returns. When a specification that includes both measures simultaneously is considered, both remain negative and statistically significant.

Our estimates from the regression of 5-year issuance on monthly returns are close to Daniel and Titman’s results. We find a slope on 5-year issuance of

---

# Page 12

932

The Journal of Finance

Table III

**Fama–MacBeth Cross-Sectional Regressions, 1970–2003**

Fama–MacBeth cross-sectional regressions results are computed for stock returns of various holding periods (each panel gives the appropriate holding period) on the following variables: the natural logarithm of the ratio of the book value of equity to the market value of equity measured at the end of December $t-1$, $BM$; a book-to-market dummy variable that is zero if $BM$ is missing, $BM\ Dum.$; the natural logarithm of market equity measured at the end of June, $ME$; the past 6 months stock return as a proxy for momentum, $MOM$; and the change in the logarithm of the number of shares outstanding adjusted for splits to capture the effect of share repurchases and SEOs. $ISSUE = [\text{Log(shares outstanding, } t-6) - \text{Log(shares outstanding, } t-17)]$; $DT\text{-}ISSUE = [\text{Log(shares outstanding, } t-6) - \text{Log(shares outstanding, } t-65)]$; if shares outstanding exist at $t-65$ , zero otherwise. $DT\text{-}Dum$ is a dummy variable set to one if shares outstanding exists at $t-65$ (hence $DT\text{-}ISSUE$ is zero), and zero otherwise. The Average $R^2$ is the average of the adjusted- $R^2$ obtained from the cross-sectional regressions, in percent. Shares associated with splits and stock dividends are not included in the computation of shares outstanding. The results presented in the table are the regression coefficients and the $t$ -statistics in brackets. These regressions are for the 396 months from January 1970 to December 2003, with a total of 2,155,945 firm-observations. Multimonth holding period results utilize overlap consistent $t$ -statistics. Coefficients with significant $t$ -statistics are bolded.

Panel A: Dependent variable is the 1-month stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum.</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT- ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0.80</td>
      <td>0.39</td>
      <td>0.73</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.66</td>
    </tr>
    <tr>
      <td>(3.04)</td>
      <td>(5.86)</td>
      <td>(8.86)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>2.69</td>
      <td></td>
      <td></td>
      <td>−0.13</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.23</td>
    </tr>
    <tr>
      <td>(3.67)</td>
      <td></td>
      <td></td>
      <td>(−2.50)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>1.19</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.62</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.23</td>
    </tr>
    <tr>
      <td>(4.56)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(1.84)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>2.06</td>
      <td>0.28</td>
      <td>0.74</td>
      <td>−0.12</td>
      <td>0.55</td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.84</td>
    </tr>
    <tr>
      <td>(2.97)</td>
      <td>(4.28)</td>
      <td>(9.72)</td>
      <td>(−2.42)</td>
      <td>(1.77)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>1.36</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−2.23</td>
      <td></td>
      <td></td>
      <td>0.22</td>
    </tr>
    <tr>
      <td>(4.88)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−7.08)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>1.48</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−0.71</td>
      <td>−0.41</td>
      <td>0.53</td>
    </tr>
    <tr>
      <td>(5.74)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−4.92)</td>
      <td>(−3.19)</td>
      <td></td>
    </tr>
    <tr>
      <td>1.48</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−1.77</td>
      <td>−0.38</td>
      <td>−0.31</td>
      <td>0.63</td>
    </tr>
    <tr>
      <td>(5.75)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−6.90)</td>
      <td>(−3.03)</td>
      <td>(−2.61)</td>
      <td></td>
    </tr>
    <tr>
      <td>2.48</td>
      <td>0.21</td>
      <td>0.68</td>
      <td>−0.14</td>
      <td>0.47</td>
      <td>−1.43</td>
      <td>−0.29</td>
      <td>−0.32</td>
      <td>3.15</td>
    </tr>
    <tr>
      <td>(3.68)</td>
      <td>(3.58)</td>
      <td>(9.03)</td>
      <td>(−2.79)</td>
      <td>(1.57)</td>
      <td>(−6.72)</td>
      <td>(−2.82)</td>
      <td>(−3.88)</td>
      <td></td>
    </tr>
  </tbody>
</table>

Panel B: Dependent variable is the 6-month stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT- ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>4.61</td>
      <td>2.39</td>
      <td>4.57</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.18</td>
    </tr>
    <tr>
      <td>(3.10)</td>
      <td>(6.05)</td>
      <td>(5.69)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>14.23</td>
      <td></td>
      <td></td>
      <td>−0.60</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.52</td>
    </tr>
    <tr>
      <td>(3.56)</td>
      <td></td>
      <td></td>
      <td>(−2.33)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>7.40</td>
      <td></td>
      <td></td>
      <td></td>
      <td>7.30</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.23</td>
    </tr>
    <tr>
      <td>(5.17)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(5.53)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>11.35</td>
      <td>1.69</td>
      <td>4.59</td>
      <td>−0.64</td>
      <td>6.86</td>
      <td></td>
      <td></td>
      <td></td>
      <td>3.73</td>
    </tr>
    <tr>
      <td>(2.88)</td>
      <td>(3.79)</td>
      <td>(6.43)</td>
      <td>(−2.31)</td>
      <td>(5.63)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>8.11</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−13.82</td>
      <td></td>
      <td></td>
      <td>0.43</td>
    </tr>
    <tr>
      <td>(5.42)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−7.26)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

(continued)

1540631_2008_2_Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540631_2008.01335 by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020] See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 13

Share Issuance and Cross-sectional Returns

933

Table III—Continued

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT- ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>8.80</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-4.20$</td>
      <td>$-2.47$</td>
      <td></td>
    </tr>
    <tr>
      <td>(6.61)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-4.84$)</td>
      <td>($-2.34$)</td>
      <td>1.06</td>
    </tr>
    <tr>
      <td>8.81</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-10.92$</td>
      <td>$-2.30$</td>
      <td>$-1.93$</td>
      <td></td>
    </tr>
    <tr>
      <td>(6.62)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-6.89$)</td>
      <td>($-2.87$)</td>
      <td>($-1.88$)</td>
      <td>1.24</td>
    </tr>
    <tr>
      <td>13.53</td>
      <td>1.31</td>
      <td>4.23</td>
      <td>$-0.73$</td>
      <td>6.47</td>
      <td>$-8.65$</td>
      <td>$-1.55$</td>
      <td>$-1.62$</td>
      <td></td>
    </tr>
    <tr>
      <td>(3.73)</td>
      <td>(3.40)</td>
      <td>(6.04)</td>
      <td>($-2.79$)</td>
      <td>(5.57)</td>
      <td>($-7.14$)</td>
      <td>($-2.44$)</td>
      <td>($-2.35$)</td>
      <td>4.35</td>
    </tr>
  </tbody>
</table>


Panel C: Dependent variable is the one-year stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT- ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>10.36</td>
      <td>4.56</td>
      <td>8.39</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(3.84)</td>
      <td>(5.41)</td>
      <td>(7.54)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.37</td>
    </tr>
    <tr>
      <td>28.88</td>
      <td></td>
      <td></td>
      <td>$-1.15$</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(3.21)</td>
      <td></td>
      <td></td>
      <td>($-1.76$)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.28</td>
    </tr>
    <tr>
      <td>15.92</td>
      <td></td>
      <td></td>
      <td></td>
      <td>9.62</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(7.17)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(3.61)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.17</td>
    </tr>
    <tr>
      <td>23.30</td>
      <td>3.33</td>
      <td>8.58</td>
      <td>$-1.20$</td>
      <td>8.66</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(2.71)</td>
      <td>(3.65)</td>
      <td>(9.48)</td>
      <td>($-1.93$)</td>
      <td>(3.58)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>3.59</td>
    </tr>
    <tr>
      <td>16.95</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-27.32$</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(7.32)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-7.51$)</td>
      <td></td>
      <td></td>
      <td>0.49</td>
    </tr>
    <tr>
      <td>18.17</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-8.38$</td>
      <td>$-4.68$</td>
      <td></td>
    </tr>
    <tr>
      <td>(8.95)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-5.94$)</td>
      <td>($-2.32$)</td>
      <td>1.22</td>
    </tr>
    <tr>
      <td>18.20</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-20.71$</td>
      <td>$-4.81$</td>
      <td>$-3.60$</td>
      <td></td>
    </tr>
    <tr>
      <td>(8.94)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-5.08$)</td>
      <td>($-2.87$)</td>
      <td>($-1.74$)</td>
      <td>1.43</td>
    </tr>
    <tr>
      <td>27.25</td>
      <td>2.59</td>
      <td>7.96</td>
      <td>$-1.37$</td>
      <td>8.02</td>
      <td>$-16.52$</td>
      <td>$-3.41$</td>
      <td>$-3.24$</td>
      <td></td>
    </tr>
    <tr>
      <td>(3.38)</td>
      <td>(3.33)</td>
      <td>(8.54)</td>
      <td>($-2.32$)</td>
      <td>(3.50)</td>
      <td>($-5.61$)</td>
      <td>($-2.60$)</td>
      <td>($-2.63$)</td>
      <td>4.27</td>
    </tr>
  </tbody>
</table>


Panel D: Dependent variable is the second-year stock return.

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT- ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>12.98</td>
      <td>3.38</td>
      <td>5.75</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(5.52)</td>
      <td>(4.33)</td>
      <td>(5.50)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.02</td>
    </tr>
    <tr>
      <td>30.14</td>
      <td></td>
      <td></td>
      <td>$-1.13$</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(4.14)</td>
      <td></td>
      <td></td>
      <td>($-2.25$)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.45</td>
    </tr>
    <tr>
      <td>17.55</td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-2.78$</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(8.69)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-1.35$)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.46</td>
    </tr>
    <tr>
      <td>23.26</td>
      <td>2.38</td>
      <td>6.46</td>
      <td>$-0.93$</td>
      <td>$-3.69$</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(3.27)</td>
      <td>(3.28)</td>
      <td>(6.94)</td>
      <td>($-1.87$)</td>
      <td>($-1.97$)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.71</td>
    </tr>
    <tr>
      <td>17.93</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-20.03$</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(8.70)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-6.20$)</td>
      <td></td>
      <td></td>
      <td>0.31</td>
    </tr>
    <tr>
      <td>18.13</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-5.40$</td>
      <td>$-1.82$</td>
      <td></td>
    </tr>
    <tr>
      <td>(8.96)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-3.25$)</td>
      <td>($-0.44$)</td>
      <td>0.51</td>
    </tr>
    <tr>
      <td>18.19</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>$-13.69$</td>
      <td>$-3.55$</td>
      <td>$-1.70$</td>
      <td></td>
    </tr>
    <tr>
      <td>(8.98)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>($-4.00$)</td>
      <td>($-1.97$)</td>
      <td>($-0.41$)</td>
      <td>0.60</td>
    </tr>
    <tr>
      <td>23.81</td>
      <td>2.10</td>
      <td>6.32</td>
      <td>$-0.92$</td>
      <td>$-3.94$</td>
      <td>$-11.63$</td>
      <td>$-2.68$</td>
      <td>$-0.80$</td>
      <td></td>
    </tr>
    <tr>
      <td>(3.40)</td>
      <td>(3.02)</td>
      <td>(6.86)</td>
      <td>($-1.84$)</td>
      <td>($-2.19$)</td>
      <td>($-3.88$)</td>
      <td>($-1.86$)</td>
      <td>($-0.20$)</td>
      <td>3.14</td>
    </tr>
  </tbody>
</table>


Panel E: Dependent variable is the third-year stock return.

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT- ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>13.55</td>
      <td>3.17</td>
      <td>5.35</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(6.08)</td>
      <td>(3.87)</td>
      <td>(6.48)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.92</td>
    </tr>
  </tbody>
</table>


(continued)

1546231_2008_2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1

---

# Page 14

934

$\text{The Journal of Finance}$

$\text{Table III—Continued}$

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>27.81</td>
      <td></td>
      <td></td>
      <td>-0.91</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.37</td>
    </tr>
    <tr>
      <td>(4.03)</td>
      <td></td>
      <td></td>
      <td>(-1.87)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>17.77</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-1.72</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.79</td>
    </tr>
    <tr>
      <td>(9.26)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-0.54)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>21.67</td>
      <td>2.07</td>
      <td>5.90</td>
      <td>-0.75</td>
      <td>-2.24</td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.78</td>
    </tr>
    <tr>
      <td>(3.19)</td>
      <td>(2.80)</td>
      <td>(8.66)</td>
      <td>(-1.55)</td>
      <td>(-0.83)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>17.97</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-14.18</td>
      <td></td>
      <td></td>
      <td>0.25</td>
    </tr>
    <tr>
      <td>(9.14)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-3.17)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>18.12</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-4.38</td>
      <td>1.98</td>
      <td>0.44</td>
    </tr>
    <tr>
      <td>(9.44)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-2.27)</td>
      <td>(0.70)</td>
      <td></td>
    </tr>
    <tr>
      <td>18.13</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-9.52</td>
      <td>-2.96</td>
      <td>2.21</td>
      <td>0.50</td>
    </tr>
    <tr>
      <td>(9.43)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-2.34)</td>
      <td>(-1.50)</td>
      <td>(0.75)</td>
      <td></td>
    </tr>
    <tr>
      <td>21.90</td>
      <td>1.85</td>
      <td>5.79</td>
      <td>-0.73</td>
      <td>-2.42</td>
      <td>-9.00</td>
      <td>-2.14</td>
      <td>3.12</td>
      <td>3.10</td>
    </tr>
    <tr>
      <td>(3.25)</td>
      <td>(2.63)</td>
      <td>(8.77)</td>
      <td>(-1.50)</td>
      <td>(-0.94)</td>
      <td>(-2.97)</td>
      <td>(-1.27)</td>
      <td>(1.02)</td>
      <td></td>
    </tr>
  </tbody>
</table>

$-0.71$ , with a standard error of $0.14$ , whereas they find a slope of $-0.66$ , with a standard error of $0.15$ . The small difference between these results is likely due to the fact that our sample starts 17 months after theirs, and we use all CRSP firms, whereas they restrict their sample to firms with Compustat data.

The third row considers all variables except issuance, while the last row includes both issuance measures. When the share issuance measures are included with the other characteristics, the slope coefficients and $t$ -statistics on all variables except $ME$ shrink slightly, although significance is unaffected.

The longer holding period results are broadly consistent with the 1-month results. The signs of the slopes remain unchanged. The $t$ -statistics on the $BM$ slopes increase with holding period and, consistent with Jegadeesh and Titman (1993), the $t$ -statistic on the $MOM$ slope peaks at the 6-month holding period. Regardless of holding period, the $t$ -statistics on both issuance measures remain stable and strongly significant. The $t$ -statistics on annual issuance are stronger than the $t$ -statistics on $BE$ , $ME$ , and $MOM$ for all holding periods. For most holding periods, 5-year issuance tends to be more significant than $ME$ and $MOM$ , although less significant than $BM$ . When all independent variables are considered jointly, annual issuance has larger $t$ -statistics than any other independent variable. Although in the joint regressions 5-year issuance is significant for holding periods up to 1 year, it loses significance in the 2- and 3-year return joint regressions.

Overall, we interpret these results as evidence that both issuance measures predict cross-sectional returns, though annual issuance in particular has a stronger ability to predict cross-sectional returns than other popular variables. Since cross-sectional equity issuance is negatively related to future returns, these findings are consistent with a model in which managers issue equity when it is overvalued and repurchase equity when it is undervalued.

The average adjusted- $R^2$ s reported in Table III show a clear pattern. Compared with all of the other variables, issuance does not explain very much of the

154621. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/j.1546-2234.2008.01335.x by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 15

Share Issuance and Cross-sectional Returns

935

cross-sectional return variance. From the monthly regressions, annual issuance only explains 0.22% of the average cross-sectional return variance, whereas 5-year issuance only explains 0.53% of the average cross-sectional return variance. The explanatory power of annual issuance is one-third of $BM$ and nearly one-sixth of $MOM$ or $ME$, despite the strength of the issuance slope coefficient. Thus, issuance tends to have a consistent negative slope in most periods, although variables such as size pick up broad effects that cause swings in the returns of large and small capitalization stocks. Compared with the size, value, and momentum effects, the share issuance effect is less likely to be a risk effect: Common covariance shared between securities is not related to share change to the same extent as these other variables. However, this does not rule out the possibility that share change proxies for compensation in non-risk-based asset pricing models, such as the transaction cost-based model of Amihud and Mendelson (1986).

*Removal of SDC SEO, repurchase, and stock merger return data.* Table II shows that share issuance is strongly related to whether or not SDC identifies the firm as having an SEO, an announced repurchase, or a completed merger. Since some long-run return studies argue that anomalous long-run returns are evident post-SEO, post-repurchase, and post-stock merger announcement, we explore whether removing the data associated with these events affects our results. The share event data start, respectively, in February of 1971, June of 1981, and June of 1978. Our SEO, repurchase, and stock merger data come from SDC, which is the same source as the original long-run return studies. We reestimate the Fama–MacBeth regressions over the 1970 to 2003 sample, eliminating firm returns for the 3 years following a known SEO, repurchase, or stock merger. This reduces our sample to 1.58 million firm-month observations from the 2.16 million observations used to generate Table III. The results from this estimation are presented in Table IV.

Overall, Table IV shows that the removal of returns associated with SEOs and repurchases has a minor impact on the ability of annual share issuance to predict returns. The major difference is that the slope coefficients and the $t$-statistics on annual issuance shrink slightly toward zero. The slope on annual share issuance continues to reject the null for all return holding periods. The 5-year issuance measure does not fare as well: It is no longer significant at any holding period, although the slope coefficient is still always negative.

Our interpretation of these results is that the returns associated with SDC-identified SEOs, repurchases, and stock mergers are part of a broader predictability that includes annual share issuance. Thus, the claimed findings of the contentious long-run return literature are not driving the issuance effect.

## III. Out-of-Sample Estimation Results

The long-run SEO return literature focuses on the post-1970 time period, and the long-run repurchase and stock merger return literature focuses on the post-1980 time period. The time period of these long-run studies is dictated by data availability from Thompson’s Financial.

---

# Page 16

936

The Journal of Finance

Table IV

**Fama–MacBeth Cross-sectional Regressions with Stock Mergers, SEOs, and Share Repurchases Removed, 1970–2003**

Fama–MacBeth cross-sectional regressions results are computed for stock returns of various holding periods (each panel gives the appropriate holding period). All firm observations for three years after an SEO or repurchase announcement have been removed, and for 1 year after a merger and acquisition. The following independent variables are used: the natural logarithm of the ratio of the book value of equity to the market value of equity measured at the end of December $t-1$, $BM$; a book-to-market dummy variable that is zero if $BM$ is missing, $BM\,Dum$; the natural logarithm of market equity measured at the end of June, $ME$; the past 6 months stock return as a proxy for momentum, $MOM$; and the change in the logarithm of the number of shares outstanding adjusted for splits to capture the effect of share repurchases and SEOs. $ISSUE = [\text{Log(shares outstanding, } t-6) - \text{Log(shares outstanding, } t-17)]$ . $DT\text{-}ISSUE = [\text{Log(shares outstanding, } t-6) - \text{Log(shares outstanding, } t-65)]$ , if shares outstanding exist at $t-65$ , zero otherwise. $DT\text{-}Dum$ is a dummy variable set to one if shares outstanding exists at $t-65$ (hence $DT\text{-}ISSUE$ is zero), and zero otherwise. The Average $R^2$ is the average of the adjusted- $R^2$ obtained from the cross-sectional regressions, in percent. Shares associated with splits and stock dividends are not included in the computation of shares outstanding. The results presented in the table are the regression coefficients and the $t$ -statistics in brackets. Multimonth holding period results utilize overlap consistent $t$ -statistics. These regressions are for 396 months from January 1970 to December 2003, with a total of 1,491,739 firm-observations. Coefficients with significant $t$ -statistics are bolded.

<table>
  <thead>
    <tr>
      <th>Dependent Variable</th>
      <th>Intercept</th>
      <th>BM</th>
      <th>Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1-month return</td>
      <td>2.73<br>(4.12)</td>
      <td>0.20<br>(3.66)</td>
      <td>0.63<br>(7.47)</td>
      <td>−0.16<br>(−3.19)</td>
      <td>0.34<br>(1.19)</td>
      <td>−1.25<br>(−5.13)</td>
      <td>−0.19<br>(−1.65)</td>
      <td>−0.31<br>(−3.79)</td>
      <td>2.87</td>
    </tr>
    <tr>
      <td>6-month return</td>
      <td>14.44<br>(3.99)</td>
      <td>1.24<br>(3.37)</td>
      <td>3.99<br>(5.81)</td>
      <td>−0.81<br>(−3.04)</td>
      <td>6.06<br>(5.55)</td>
      <td>−7.79<br>(−6.05)</td>
      <td>−0.99<br>(−1.35)</td>
      <td>−1.53<br>(−2.23)</td>
      <td>3.94</td>
    </tr>
    <tr>
      <td>1-year return</td>
      <td>29.08<br>(3.62)</td>
      <td>2.44<br>(3.03)</td>
      <td>7.78<br>(8.76)</td>
      <td>−1.53<br>(−2.59)</td>
      <td>7.34<br>(3.74)</td>
      <td>−15.34<br>(−5.31)</td>
      <td>−2.41<br>(−1.84)</td>
      <td>−3.00<br>(−2.33)</td>
      <td>3.82</td>
    </tr>
    <tr>
      <td>Second-year return</td>
      <td>24.41<br>(3.48)</td>
      <td>1.99<br>(2.90)</td>
      <td>5.57<br>(6.46)</td>
      <td>−0.95<br>(−1.90)</td>
      <td>−3.62<br>(−2.10)</td>
      <td>−9.87<br>(−3.59)</td>
      <td>−1.58<br>(−1.33)</td>
      <td>−0.21<br>(−0.05)</td>
      <td>2.86</td>
    </tr>
    <tr>
      <td>Third-year return</td>
      <td>21.04<br>(3.15)</td>
      <td>1.94<br>(2.82)</td>
      <td>5.21<br>(7.09)</td>
      <td>−0.63<br>(−1.30)</td>
      <td>−2.11<br>(−0.85)</td>
      <td>−3.62<br>(−0.85)</td>
      <td>−1.41<br>(−0.86)</td>
      <td>0.60<br>(0.38)</td>
      <td>2.86</td>
    </tr>
  </tbody>
</table>

Other studies of issuance use issuance measures that are constructed from Compustat accounting data. For example, Bradshaw, Richardson, and Sloan (2004) use a balance sheet measure of share issuance, which they relate to future stock returns as well as analyst earnings forecasts. They find a negative relation between their issuance measure and stock returns. Due to data limitations, their sample starts in 1971. Bali et al. (2005) focus on the period from 1972 to the present and show that an accounting-based issuance measure explains variation in the value-growth return relation. Daniel and Titman (2006) focus on a sample that starts in July of 1968. Using data from 1962 to 2002, Cooper, Gulen, and Schill (2006) investigate the ability of

1540631_2008_2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540631.2008.01353 by University of Hong Kong Libraries, Wiley Online Library on 22/07/2020. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 17

# Share Issuance and Cross-sectional Returns

## Table V

### Descriptive Statistics, 1932 to 1969

Panel A: Simple Statistics. The variables used are: the natural logarithm of the ratio of the book value of equity to the market value of equity measured at the end of December $t-1$ , $BM$ ; the natural logarithm of market equity measured at the end of the previous June, $ME$ ; the past 6 months stock return as a proxy for momentum, $MOM$ ; the change in the logarithm of the number of shares outstanding adjusted for splits to capture the effect of share repurchases and SEOs; $ISSUE_{-11,0} = [\text{Log(shares outstanding, } t) - \text{Log(shares outstanding, } t-11)]$ ; $ISSUE_{-59,0} = [\text{Log(shares outstanding, } t) - \text{Log(shares outstanding, } t-59)]$ ; and the 1-year return $R_{-11,0}$ contemporaneous with the $ISSUE_{-11,0}$ variable. The variables are measured at the end of December for the period between September 1932 and December 1969. Shares associated with splits and stock dividends are not included in the computation of shares outstanding. The sample observations range between 524,260 observations (for $MOM$ ) and 528,200 observations (for $R_{-11,0}$ ).

Panels B and C: Correlations. Correlations between the variables defined in Panel A, that is, $ISSUE_{-11,0}$ , $ISSUE_{-59,0}$ , $BM$ , $ME$ , $MOM$ , and $R_{-11,0}$ , as well as the 12-month lead and lag of the change in shares outstanding variable, $ISSUE_{-23,-12}$ and $ISSUE_{1,12}$ , and the 12-month lead of the 1-year return, $R_{1,12}$ . Panel B shows the contemporaneous correlations, while Panel C looks at the time-series correlations.

### Panel A: Simple statistics

<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th>Mean</th>
      <th>25th Percentile</th>
      <th>Median</th>
      <th>75th Percentile</th>
      <th>Standard Deviation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> $ISSUE_{-11,0}$ </td>
      <td>0.01</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.07</td>
    </tr>
    <tr>
      <td> $ISSUE_{-59,0}$ </td>
      <td>0.08</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.05</td>
      <td>0.24</td>
    </tr>
    <tr>
      <td>BM</td>
      <td>-0.12</td>
      <td>-0.56</td>
      <td>0.00</td>
      <td>0.11</td>
      <td>0.94</td>
    </tr>
    <tr>
      <td>ME</td>
      <td>10.28</td>
      <td>9.05</td>
      <td>10.22</td>
      <td>11.50</td>
      <td>1.80</td>
    </tr>
    <tr>
      <td>MOM</td>
      <td>0.09</td>
      <td>-0.09</td>
      <td>0.05</td>
      <td>0.20</td>
      <td>0.34</td>
    </tr>
    <tr>
      <td> $R_{-11,0}$ </td>
      <td>0.19</td>
      <td>-0.10</td>
      <td>0.11</td>
      <td>0.35</td>
      <td>0.60</td>
    </tr>
  </tbody>
</table>

### Panel B: Contemporaneous correlations

<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th> $ISSUE_{-11,0}$ </th>
      <th>BM</th>
      <th>ME</th>
      <th>MOM</th>
      <th> $R_{-11,0}$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>BM</td>
      <td>-0.03</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>ME</td>
      <td>0.02</td>
      <td>-0.40</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>MOM</td>
      <td>-0.01</td>
      <td>0.02</td>
      <td>0.02</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td> $R_{-11,0}$ </td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.04</td>
      <td>0.68</td>
      <td></td>
    </tr>
    <tr>
      <td> $ISSUE_{-59,0}$ </td>
      <td>0.43</td>
      <td>-0.07</td>
      <td>0.01</td>
      <td>-0.01</td>
      <td>0.00</td>
    </tr>
  </tbody>
</table>

### Panel C: Noncontemporaneous correlations

<table>
  <thead>
    <tr>
      <th>Variable</th>
      <th> $ISSUE_{-23,-12}$ </th>
      <th> $ISSUE_{-11,0}$ </th>
      <th> $ISSUE_{1,12}$ </th>
      <th> $R_{-11,0}$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td> $ISSUE_{-11,0}$ </td>
      <td>0.12</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td> $ISSUE_{1,12}$ </td>
      <td>0.07</td>
      <td>0.12</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td> $R_{-11,0}$ </td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>0.05</td>
      <td></td>
    </tr>
    <tr>
      <td> $R_{1,12}$ </td>
      <td>-0.01</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>0.03</td>
    </tr>
  </tbody>
</table>

asset growth to predict returns, which they relate to share issuance. In order to evaluate the performance of share issuance in another time period, we reestimate the Table II results using data from 1932 to 1969. This time period overlaps with neither Bradshaw et al., Bali et al., nor any of the long-run SEO,

---

# Page 18

938

The Journal of Finance

repurchases and stock merger studies. A small overlap (17 months) is shared with Daniel and Titman and a larger overlap (65 months) is shared with Cooper et al.

We obtain data on the book value of equity from Kenneth French for our out-of-sample study, since COMPUSTAT coverage is limited or nonexistent during this time period. These data are identical to those used by Davis, Fama, and French (2000).

The pecking order model (Myers (1984) and Myers and Majluf (1984)) predicts that costs associated with asymmetric information cause firms to issue equity only as a last resort after internal financing and debt issuance. Fama and French (2005) show that in the post-1973 period, firms frequently issue stock, in apparent violation of the pecking order. They note that share issuance was less frequent in the first half of their sample. Table V presents summary statistics from the pre-1970 period that suggest the frequency of issuance before the start of Fama and French’s sample is even lower than expected. In the pre-1970 period share issuance is 0.01 versus 0.04 in the post-1970 period. Also, the pre-1970 standard deviation of this annual share issuance is less than half that of the post-1970 level, at 0.07 versus 0.15. The breakdown of pre-1970 annual share issuance into positive, zero, and negative issuance tells a similar story—28.2% are positive, 62.6% are zero, and 9.2% are negative. Our results are not directly comparable to Fama and French’s since they focus on the subset of firms with both CRSP and Compustat data and they are able to disaggregate their results into purchases and sales. Some of our firms with zero annual issuance neither purchase nor sell shares, and some purchase and sell shares in quantities that perfectly counteract. As long as the proportion between the two types of firms remains stable before and after 1970, a comparison of the percentage of firms with zero share issuance before and after 1970 tells us about the change in the relative frequency that firms buy and sell their own shares in these two time periods. Prior to 1970, 62.6% of firms have no annual share issuance and after 1970, 24.2% of firms have no annual issuance, implying a decrease in the proportion of firms not engaging in equity transactions of 61.3%. Concentrating on the percentage of net share issuers, the pre- to post-1970 increase from 9.2% to 19.2% implies that equity issuance doubled. These numbers imply that after 1970, firms are much more likely to transact in their own stock. Although we do not test whether the pecking order theory would be rejected using an early sample, these back-of-the-envelope calculations imply that the pecking order theory is likely to be a more accurate description of pre-1970 share issuance than post-1970 share issuance.

A possible explanation for the drastic increase in the post-1970 variation of issuance is that the cost of changing capital structure decreased after 1970, and companies responded to this decrease in costs by more actively buying and selling their own shares. This explanation is consistent with Roberts and Leary (2005), who argue that transaction costs delay firms from adjusting their optimal capital structure as dictated by trade-off theory.

1540631. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540631.2008.01335 by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library. No part of this OA article are governed by the applicable Creative Commons License.

---

# Page 19

# Share Issuance and Cross-sectional Returns

## Table VI

### Out-of-Sample Fama–MacBeth Cross-sectional Regressions, 1932–1969

Fama–MacBeth cross-sectional regressions results are computed for stock returns of various holding periods (each panel gives the appropriate holding period) on the following variables: the natural logarithm of the ratio of the book value of equity to the market value of equity measured at the end of December $t-1$, $BM$; a book-to-market dummy variable that is zero if $BM$ is missing, $BM\ Dum$; the natural logarithm of market equity measured at the end of June, $ME$; the past 6 months stock return as a proxy for momentum, $MOM$; and the change in the logarithm of the number of shares outstanding adjusted for splits to capture the effect of share repurchases and SEOs. $ISSUE = [\text{Log(shares outstanding, } t-6) - \text{Log(shares outstanding, } t-17)]$; $DT\text{-}ISSUE = [\text{Log(shares outstanding, } t-6) - \text{Log(shares outstanding, } t-65)]$; if shares outstanding exist at $t-65$ , zero otherwise. $DT\text{-}Dum$ is a dummy variable set to one if shares outstanding exists at $t-65$ (hence $DT\text{-}ISSUE$ is zero), and zero otherwise. The Average $R^2$ is the average of the adjusted- $R^2$ obtained from the cross-sectional regressions, in percent. Shares associated with splits and stock dividends are not included in the computation of shares outstanding. The results presented in the table are the regression coefficients and the $t$ -statistics in brackets. These regressions are for the 444 months from September 1932 (to ensure the existence of shares outstanding) to December 1969, with a total of 373,590 firm-observations. Multimonth holding period results utilize overlap consistent $t$ -statistics. Coefficients with significant $t$ -statistics are bolded.

#### Panel A: Dependent variable is the 1-month stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1.40</td>
      <td>0.34</td>
      <td>−0.02</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.86</td>
    </tr>
    <tr>
      <td>(3.94)</td>
      <td>(3.05)</td>
      <td>(−0.19)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>3.58</td>
      <td></td>
      <td></td>
      <td>−0.22</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.58</td>
    </tr>
    <tr>
      <td>(3.79)</td>
      <td></td>
      <td></td>
      <td>(−3.04)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>1.35</td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.68</td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.27</td>
    </tr>
    <tr>
      <td>(4.56)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(1.34)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>2.77</td>
      <td>0.15</td>
      <td>0.17</td>
      <td>−0.16</td>
      <td>0.70</td>
      <td></td>
      <td></td>
      <td></td>
      <td>5.12</td>
    </tr>
    <tr>
      <td>(3.88)</td>
      <td>(2.08)</td>
      <td>(2.00)</td>
      <td>(−3.16)</td>
      <td>(1.59)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>1.52</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.52</td>
      <td></td>
      <td></td>
      <td>0.12</td>
    </tr>
    <tr>
      <td>(4.29)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(0.43)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>1.51</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.17</td>
    </tr>
    <tr>
      <td>(4.31)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−0.03)</td>
      <td>(0.12)</td>
      <td></td>
    </tr>
    <tr>
      <td>1.51</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.27</td>
      <td>0.06</td>
      <td>0.00</td>
      <td>0.23</td>
    </tr>
    <tr>
      <td>(4.32)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(0.21)</td>
      <td>(0.46)</td>
      <td>(0.11)</td>
      <td></td>
    </tr>
    <tr>
      <td>2.76</td>
      <td>0.15</td>
      <td>0.16</td>
      <td>−0.16</td>
      <td>0.72</td>
      <td>0.84</td>
      <td>0.06</td>
      <td>0.04</td>
      <td>5.33</td>
    </tr>
    <tr>
      <td>(3.90)</td>
      <td>(2.06)</td>
      <td>(1.93)</td>
      <td>(−3.15)</td>
      <td>(1.66)</td>
      <td>(0.68)</td>
      <td>(0.49)</td>
      <td>(0.78)</td>
      <td></td>
    </tr>
  </tbody>
</table>

#### Panel B: Dependent variable is the 6-month stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>8.77</td>
      <td>1.82</td>
      <td>−0.73</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>3.02</td>
    </tr>
    <tr>
      <td>(4.24)</td>
      <td>(3.06)</td>
      <td>(−0.92)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>20.73</td>
      <td></td>
      <td></td>
      <td>−1.23</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>4.01</td>
    </tr>
    <tr>
      <td>(3.54)</td>
      <td></td>
      <td></td>
      <td>(−2.90)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>8.25</td>
      <td></td>
      <td></td>
      <td></td>
      <td>7.20</td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.11</td>
    </tr>
    <tr>
      <td>(3.93)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(4.63)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>17.98</td>
      <td>0.76</td>
      <td>0.37</td>
      <td>−1.06</td>
      <td>6.82</td>
      <td></td>
      <td></td>
      <td></td>
      <td>6.87</td>
    </tr>
    <tr>
      <td>(3.39)</td>
      <td>(1.89)</td>
      <td>(0.65)</td>
      <td>(−2.93)</td>
      <td>(4.69)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>8.97</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−0.45</td>
      <td></td>
      <td></td>
      <td>0.14</td>
    </tr>
    <tr>
      <td>(4.43)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−0.12)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

(continued)

---

# Page 20

940

*The Journal of Finance*

Table VI—Continued

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>8.94</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.00</td>
      <td>0.16</td>
      <td></td>
    </tr>
    <tr>
      <td>(4.40)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(0.01)</td>
      <td>(0.60)</td>
      <td>0.21</td>
    </tr>
    <tr>
      <td>8.96</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-2.26</td>
      <td>0.59</td>
      <td>0.16</td>
      <td></td>
    </tr>
    <tr>
      <td>(4.41)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-0.61)</td>
      <td>(1.03)</td>
      <td>(0.60)</td>
      <td>0.27</td>
    </tr>
    <tr>
      <td>17.90</td>
      <td>0.75</td>
      <td>0.34</td>
      <td>-1.05</td>
      <td>6.85</td>
      <td>1.25</td>
      <td>0.65</td>
      <td>0.14</td>
      <td></td>
    </tr>
    <tr>
      <td>(3.39)</td>
      <td>(1.87)</td>
      <td>(0.60)</td>
      <td>(-2.91)</td>
      <td>(4.76)</td>
      <td>(0.27)</td>
      <td>(1.24)</td>
      <td>(0.48)</td>
      <td>7.15</td>
    </tr>
  </tbody>
</table>

Panel C: Dependent variable is the 1-year stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>18.27</td>
      <td>3.42</td>
      <td>-0.87</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(4.82)</td>
      <td>(3.00)</td>
      <td>(-0.62)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>3.04</td>
    </tr>
    <tr>
      <td>39.90</td>
      <td></td>
      <td></td>
      <td>-2.24</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(3.28)</td>
      <td></td>
      <td></td>
      <td>(-2.28)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>4.04</td>
    </tr>
    <tr>
      <td>17.01</td>
      <td></td>
      <td></td>
      <td></td>
      <td>9.90</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(5.62)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(4.62)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.84</td>
    </tr>
    <tr>
      <td>36.15</td>
      <td>1.37</td>
      <td>1.19</td>
      <td>-1.99</td>
      <td>8.83</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(3.33)</td>
      <td>(1.90)</td>
      <td>(0.72)</td>
      <td>(-2.31)</td>
      <td>(3.59)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>6.69</td>
    </tr>
    <tr>
      <td>18.20</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-13.80</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(5.50)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-1.72)</td>
      <td></td>
      <td></td>
      <td>0.14</td>
    </tr>
    <tr>
      <td>18.07</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>0.21</td>
      <td>-0.25</td>
      <td></td>
    </tr>
    <tr>
      <td>(5.51)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(0.15)</td>
      <td>(-0.65)</td>
      <td>0.16</td>
    </tr>
    <tr>
      <td>18.11</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-19.03</td>
      <td>1.63</td>
      <td>-0.25</td>
      <td></td>
    </tr>
    <tr>
      <td>(5.52)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-2.19)</td>
      <td>(1.11)</td>
      <td>(-0.65)</td>
      <td>0.23</td>
    </tr>
    <tr>
      <td>35.97</td>
      <td>1.35</td>
      <td>1.03</td>
      <td>-1.96</td>
      <td>8.84</td>
      <td>-11.95</td>
      <td>1.62</td>
      <td>-0.20</td>
      <td></td>
    </tr>
    <tr>
      <td>(3.34)</td>
      <td>(1.89)</td>
      <td>(0.65)</td>
      <td>(-2.30)</td>
      <td>(3.62)</td>
      <td>(-1.51)</td>
      <td>(1.30)</td>
      <td>(-0.63)</td>
      <td>6.92</td>
    </tr>
  </tbody>
</table>

Panel D: Dependent variable is the second-year stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>16.05</td>
      <td>2.56</td>
      <td>-0.19</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(4.08)</td>
      <td>(2.29)</td>
      <td>(-0.12)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.94</td>
    </tr>
    <tr>
      <td>31.57</td>
      <td></td>
      <td></td>
      <td>-1.53</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(2.52)</td>
      <td></td>
      <td></td>
      <td>(-1.51)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>3.88</td>
    </tr>
    <tr>
      <td>16.02</td>
      <td></td>
      <td></td>
      <td></td>
      <td>-6.63</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(5.06)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-1.95)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.48</td>
    </tr>
    <tr>
      <td>29.61</td>
      <td>1.34</td>
      <td>0.35</td>
      <td>-1.33</td>
      <td>-6.42</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(2.71)</td>
      <td>(2.03)</td>
      <td>(0.24)</td>
      <td>(-1.60)</td>
      <td>(-1.87)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>5.99</td>
    </tr>
    <tr>
      <td>5.93</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>6.23</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(4.80)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(0.68)</td>
      <td></td>
      <td></td>
      <td>0.11</td>
    </tr>
    <tr>
      <td>15.69</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.27</td>
      <td>-0.37</td>
      <td></td>
    </tr>
    <tr>
      <td>(4.78)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(1.63)</td>
      <td>(-1.33)</td>
      <td>0.14</td>
    </tr>
    <tr>
      <td>15.73</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>-3.63</td>
      <td>3.29</td>
      <td>-0.37</td>
      <td></td>
    </tr>
    <tr>
      <td>(4.80)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(-0.52)</td>
      <td>(2.47)</td>
      <td>(-1.33)</td>
      <td>0.22</td>
    </tr>
    <tr>
      <td>29.46</td>
      <td>1.36</td>
      <td>0.34</td>
      <td>-1.33</td>
      <td>-6.44</td>
      <td>0.23</td>
      <td>3.11</td>
      <td>-0.37</td>
      <td></td>
    </tr>
    <tr>
      <td>(2.73)</td>
      <td>(2.07)</td>
      <td>(0.24)</td>
      <td>(-1.61)</td>
      <td>(-1.86)</td>
      <td>(0.03)</td>
      <td>(2.56)</td>
      <td>(-1.17)</td>
      <td>6.22</td>
    </tr>
  </tbody>
</table>

Panel E: Dependent variable is the third-year stock return

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>17.84</td>
      <td>2.16</td>
      <td>-1.77</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>(4.15)</td>
      <td>(2.17)</td>
      <td>(-0.87)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.63</td>
    </tr>
  </tbody>
</table>

(continued)

154624, 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/154624.2008.01353, by University of Hong Kong Libraries, Wiley Online Library on 22/07/2020. Journals and Conferences (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 21

# Share Issuance and Cross-sectional Returns

941

## Table VI—Continued

<table>
  <thead>
    <tr>
      <th>Intercept</th>
      <th>BM</th>
      <th>BM Dum</th>
      <th>ME</th>
      <th>MOM</th>
      <th>ISSUE</th>
      <th>DT-ISSUE</th>
      <th>DT-Dum</th>
      <th>Avg. $R^2$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>31.75</td>
      <td></td>
      <td></td>
      <td>−1.47</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>3.56</td>
    </tr>
    <tr>
      <td>(2.67)</td>
      <td></td>
      <td></td>
      <td>(−1.58)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>16.58</td>
      <td></td>
      <td></td>
      <td></td>
      <td>−5.08</td>
      <td></td>
      <td></td>
      <td></td>
      <td>1.60</td>
    </tr>
    <tr>
      <td>(5.47)</td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−1.24)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>30.87</td>
      <td>0.98</td>
      <td>−1.48</td>
      <td>−1.25</td>
      <td>−5.10</td>
      <td></td>
      <td></td>
      <td></td>
      <td>5.74</td>
    </tr>
    <tr>
      <td>(2.79)</td>
      <td>(1.85)</td>
      <td>(−0.76)</td>
      <td>(−1.50)</td>
      <td>(−1.44)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>16.65</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>17.85</td>
      <td></td>
      <td></td>
      <td>0.13</td>
    </tr>
    <tr>
      <td>(4.95)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(1.30)</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>16.50</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>2.11</td>
      <td>0.41</td>
      <td>0.12</td>
    </tr>
    <tr>
      <td>(4.95)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(1.64)</td>
      <td>(1.42)</td>
      <td></td>
    </tr>
    <tr>
      <td>16.50</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>11.76</td>
      <td>2.46</td>
      <td>0.41</td>
      <td>0.21</td>
    </tr>
    <tr>
      <td>(4.97)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(1.03)</td>
      <td>(1.66)</td>
      <td>(1.42)</td>
      <td></td>
    </tr>
    <tr>
      <td>30.70</td>
      <td>1.02</td>
      <td>−1.40</td>
      <td>−1.26</td>
      <td>−4.95</td>
      <td>15.89</td>
      <td>2.16</td>
      <td>0.20</td>
      <td>5.92</td>
    </tr>
    <tr>
      <td>(2.83)</td>
      <td>(1.95)</td>
      <td>(−0.73)</td>
      <td>(−1.55)</td>
      <td>(−1.39)</td>
      <td>(1.22)</td>
      <td>(1.57)</td>
      <td>(1.39)</td>
      <td></td>
    </tr>
  </tbody>
</table>

Table VI presents our estimation of pre-1970 return predictability. Construction of $DT-ISSUE$ requires 5 years of data, thus our estimation does not begin until 1932. For all regressions and all holding periods, $ME$ exhibits a statistically significant, negative relation with returns. $MOM$ exhibits positive slope coefficients for all regressions, although not all slope coefficients are significant. Specifically, none of the 1-month $MOM$ slope coefficients are significant and the 3-month simple regression slope is not significant, whereas the remaining $MOM$ slopes are significant. The share issuance results suffer the greatest impact from the pre-1970 estimation. Of the 40 regressions (five holding periods times eight specifications) annual issuance only has a negative and statistically significant slope coefficient in one specification when it is included with 5-year issuance in predicting annual returns. The pre-1970 results for 5-year issuance are more extreme. There is a significant and *positive* slope coefficient for two specifications, and the remaining 38 specifications produce insignificant slope coefficients.$^3$

If (as Table IV shows) post-SEO and share repurchase returns are part of a general the change in shares outstanding effect, our findings suggest that the results of the long-run SEO and repurchase literature and some of the results of Bradshaw et al. (2004) and Daniel and Titman (2006) may be sample specific. Our finding is similar to Gompers and Lerner (2003), who claim that the strong post-1974 IPO underperformance that Ritter (1991) demonstrates is not evident in their sample of pre-1972 IPOs.

Our results suggest that managerial opportunism in timing equity markets was less of a possibility before 1970. Baker and Wurgler’s (2000) study shows

$^3$ We also estimate regressions that omit $DT-ISSUE$ and use data that starts in 1927. This produces roughly similar results for all return frequencies other than the annual frequency. Somewhat similar to the post-1970 results, the annual frequency has a slope coefficient of $-18.25$ and a $t$-statistic of $-2.79$. All other frequencies produce insignificant slope coefficients and, except for the 6-month frequency, the slopes are positive.

1540624, 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6241.2008.01355.x by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library. All rights reserved by the applicable Creative Commons License.

---

# Page 22

942

The Journal of Finance

![image](image_1.png)

Figure 1. Trailing average slope coefficient from the regression of the 1-month return on ISSUE ($-6, -17$)

that the aggregate equity share of new issues predicts market returns in both the 1928 to 1962 and 1963 to 1997 subsamples. Since our test is cross-sectional, we cannot directly compare it to their time-series results. Both papers suggest a weaker link between equity issuance and returns in the earlier subsample.

Managerial opportunism may provide a possible explanation for both the increase in the return predictive ability of share issuance and the increase in firms’ activities in their share market. Consider an environment in which managers alter their capital structure to take advantage of mispricing and make adjustments that correspond to the trade-off theory. In this case, capital structure only changes if the total benefit is larger than the cost. If the cost of transacting in one’s own stock decreases, we would expect firms to transact in their own stock more frequently and we would also expect these transactions to convey more information about cross-sectional mispricing.

Figures 1 and 2 further investigate the time series of the slope coefficients on share issuance. Using the slope coefficients from a univariate regression of monthly returns on annual issuance, we compute the average slope over the past 12 months and the appropriate standard error from these 12 observations. These statistics are computed every month, giving us a rolling estimate of the share issuance’s slope and its standard error. As Figure 1 shows, after 1950 the average slope exhibits a remarkable tendency to be negative. The pre-1950 data, particularly the data from around the end of World War II, tend to produce positive slope coefficients, but more importantly, the variability of these slope coefficients is large.

1540621, 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540-6214.2008.01335 by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 23

# Share Issuance and Cross-sectional Returns

943

![image](image_1.png)

Figure 2. Trailing average slope coefficient from the regression of the 1-month return on ISSUE (−6, −17)

The drastic difference in the pre-1950 data is puzzling. Investigation of extreme data points confirms the accuracy of the CRSP data during this time period. Since the pre-1950 variation dwarfs the post-1950 variation, Figure 2 examines the post-1950 section of Figure 1. As Figure 2 shows, the slope coefficient on share issuance is usually negative. When the coefficient is positive, it tends to be of smaller magnitude than the negative realizations. There does not seem to be a time trend or structural breakpoint during this subperiod. Thus, the data do not support the contention that the introduction of the NASDAQ firms in 1972 contributed to the return predictability of share issuance or that the employee stock option awards of the 1980s and 1990s are the source of the predictability.

## IV. Conclusion

Share issuance occurs as a firm purchases or sells its own stock. Some participants in the long-run return debate argue that post-SEO and post-stock merger long-run returns are abnormally low, and that post-share repurchase long-run returns are abnormally high. This debate motivates us to examine whether share issuance can be used to forecast stock returns in the cross-section.

During the post-1970 time period, which most long-run studies focus on, we find that both annual and 5-year share issuance are strongly related to future returns. In fact, in the case of annual share issuance, statistical significance is greater than the previously documented predictability attributed to book-to-market, size, and momentum. These post-1970 results are consistent with

1540631. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6314.2008.01335.x by University of Hong Kong Libraries, Wiley Online Library on 22/07/2020. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.

---

# Page 24

944

The Journal of Finance

an opportunistic view of capital structure whereby decision makers (insiders) repurchase or sell shares in order to take advantage of variability in expected returns.

This post-1970 predictability is not caused by the data used in the long-run predictability research. Thus, we interpret the long-run returns associated with SEOs, repurchases, and stock mergers as part of a broader share issuance effect. This effect does not appear to be a manifestation of risk-based asset pricing, or at least not of the magnitude associated with the book-to-market, size, or momentum effects. The typical monthly explained return variation from these effects is several times greater than the explained variation attributed to annual share issuance.

Finally, we show that before 1970, the ability of 5-year share issuance to predict stock returns is statistically insignificant for all return holding periods, and the ability of annual share issuance to predict stock returns is statistically significant for only the annual holding period. The pre-1970 sample is interesting because it is out-of-sample relative to the data used by the SEO, repurchase, and stock merger literature, as well as the recent cross-sectional literature on share issuance. Closer examination reveals particularly large variation in the slope on share issuance during the 1940s. The fact that the predictability associated with share issuance is different in pre- and post-1970 samples suggests that the long-run returns attributed to SEO, repurchase, and stock merger announcements may be sample specific. These differences are consistent with another apparent discrepancy, namely, before 1970 share issuance was less frequent. The extent to which these two effects are related is left for future research. One possibility that may warrant investigation is whether both effects are influenced by a decrease in the cost that firms face when making capital structure decisions. In this case, lower transaction costs in the second half of the sample allow managers to use their perceptions of mispricing to adjust capital structure more frequently. This leads in turn to share issuance conveying more information about cross-sectional returns.

## REFERENCES

Amihud, Yakov, and Haim Mendelson, 1986, Asset pricing and the bid-ask spread, *Journal of Financial Economics* 17, 223–249.

Baker, Malcolm, and Jeffrey Wurgler, 2000, The equity share in new issues and aggregate stock returns, *Journal of Finance* 55, 2219–2257.

Bali, Turan K., Demirtas Ozgur, and Armen Hovakimian, 2005, Contrarian investment, new share issues and repurchases, Working paper, Baruch University.

Bradshaw, Mark, Scott Richardson, and Richard Sloan, 2004, The relation between corporate financing activities, analysts’ forecasts and stock returns, Working paper, University of Michigan.

Cooper, Michael J., Huseyin Gulen, and Michael J. Schill, 2006, What best explains the cross-section of stock returns? Exploring the asset growth effect, Working paper, University of Virginia—Darden School of Business.

Daniel, Kent, and Sheridan Titman, 2006, Market reaction to tangible and intangible information, Working paper, Northwestern University.

---

# Page 25

# Share Issuance and Cross-sectional Returns

945

Davis, James L., Eugene F. Fama, and Kenneth R. French, 2000, Characteristics, covariances, and average returns: 1929–1997, *Journal of Finance* 55, 389–406.

Fama, Eugene F., and Kenneth R. French, 1992, The cross-section of expected stock returns, *Journal of Finance* 47, 427–465.

Fama, Eugene F., and Kenneth R. French, 2005, Financing decisions: Who issues stock?, *Journal of Financial Economics* 76, 549–582.

Fama, Eugene F., and James D. Macbeth, 1973, Risk, return, and equilibrium: Empirical tests, *Journal of Political Economy* 71, 607–636.

Gompers, Paul A., and Josh Lerner, 2003, The really long-run performance of initial public offerings: the pre-Nasdaq evidence, *Journal of Finance* 58, 1355–1392.

Ikenberry, David, Josef Lakonishok, and Theo Vermaelen, 1995, Market underreaction to open market share repurchases, *Journal of Financial Economics* 39, 181–208.

Ikenberry, David, Josef Lakonishok, and Theo Vermaelen, 2000, Stock repurchases in Canada: Performance and strategic trading, *Journal of Finance* 55, 181–208.

Jegadeesh, Narasimhan, and Sheridan Titman, 1993, Returns to buying winners and selling losers: Implications for stock market efficiency, *Journal of Finance* 48, 65–91.

Lakonishok, Josef, and Inmoo Lee, 2001, Are insider trades informative? *Review of Financial Studies* 14, 79–111.

Loughran, T., and J. Ritter, 1995, The new issues puzzle, *Journal of Finance* 50, 23–51.

Loughran, T., and A. Vijh, 1997, Do long-term shareholders benefit from corporate acquisitions? *Journal of Finance* 52, 1765–1790.

Mitchell, Mark L., and Erik Stafford, 2000, Managerial decisions and long-term stock price performance, *Journal of Business* 73, 287–329.

Myers, S. C., 1984, The capital structure puzzle, *Journal of Finance* 39, 575–592.

Myers, S. C., and N.S. Majluf, 1984, Corporate financing and investment decisions when firms have information that investors do not have, *Journal of Financial Economics* 13, 187–221.

Pontiff, Jeffrey, 1996, Costly arbitrage and closed-end fund discounts, *Quarterly Journal of Economics* 111, 1135–1151.

Ritter, Jay R., 1991, The long-run performance of initial public offerings, *Journal of Finance* 46, 3–27.

Roberts, Michael R., and Mark Leary, 2005, Do firms rebalance their capital structures?, *Journal of Finance* 60, 2575–2619.

Schultz, Paul, 2003, Pseudo market timing and the long-run underperformance of IPOs, *Journal of Finance* 58, 483–517.

Stephens, Clifford P., and Michael S. Weisbach, 1998, Actual share acquisitions in open-market repurchase programs, *Journal of Finance* 52, 313–333.

1540624. 2008. 2. Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/1540-6241.2008.01335 by University of Hong Kong Libraries, Wiley Online Library on [22/07/2020]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use. OA articles are governed by the applicable Creative Commons License.