# Page 1

# WILEY

---

## Evidence of Predictable Behavior of Security Returns

**Author(s):** Narasimhan Jegadeesh

**Source:** *The Journal of Finance*, Jul., 1990, Vol. 45, No. 3, Papers and Proceedings, Forty-ninth Annual Meeting, American Finance Association, Atlanta, Georgia, December 28-30, 1989 (Jul., 1990), pp. 881-898

**Published by:** Wiley for the American Finance Association

**Stable URL:** https://www.jstor.org/stable/2328797

---

JSTOR is a not-for-profit service that helps scholars, researchers, and students discover, use, and build upon a wide range of content in a trusted digital archive. We use information technology and tools to increase productivity and facilitate new forms of scholarship. For more information about JSTOR, please contact support@jstor.org.

Your use of the JSTOR archive indicates your acceptance of the Terms & Conditions of Use, available at https://about.jstor.org/terms

---

<div style="display: flex; align-items: center; gap: 10px;">
  ![image](image_1.png)
  <span>and Wiley are collaborating with JSTOR to digitize, preserve and extend access to *The Journal of Finance*</span>
</div>

<div style="text-align: center; font-size: 0.8em; margin-top: 20px;">
  This content downloaded from<br>
  147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC<br>
  All use subject to https://about.jstor.org/terms
</div>

---

# Page 2

THE JOURNAL OF FINANCE • VOL. XLV, NO. 3 • JULY 1990

# Evidence of Predictable Behavior of Security Returns

NARASIMHAN JEGADEESH*

## ABSTRACT

This paper presents new empirical evidence of predictability of individual stock returns. The negative first-order serial correlation in monthly stock returns is highly significant. Furthermore, significant positive serial correlation is found at longer lags, and the twelve-month serial correlation is particularly strong. Using the observed systematic behavior of stock returns, one-step-ahead return forecasts are made and ten portfolios are formed from the forecasts. The difference between the abnormal returns on the extreme decile portfolios over the period 1934–1987 is 2.49 percent per month.

THE CONCEPT OF MARKET efficiency is the foundation for much of the theoretical and empirical research in financial economics. The early tests surveyed by Fama (1970) generally provide evidence in support of the efficient market hypothesis. However, some recent papers report evidence of predictability of returns on market indices and size-sorted portfolios. For example, Fama and French (1988) report negative serial correlation in market returns over observation intervals of three to five years, and Lo and MacKinley (1988) report positive serial correlation in weekly returns. While the evidence of stock return predictability reported by Fama and French and Lo and MacKinley is statistically significant, it is not clear whether these results suggest economically important deviations from the random walk model for stock prices.

In the case of individual securities, statistical evidence against the random walk model for stock prices has been documented, but the extent of predictability of returns is generally considered economically insignificant. For instance, French and Roll (1986) report significant negative serial correlation in daily returns but suggest that it is “small in absolute magnitude” and that “it is hard to gauge their economic significance.” In a more recent paper, Lo and MacKinley (1988) consider weekly holding-period returns for individual securities and report that “the serial correlation is both statistically and economically insignificant” and suggest that the “idiosyncratic noise … makes it difficult to detect the presence of predictable components.”

This paper examines the predictability of monthly returns on individual securities. The results here provide new evidence of stock return predictability. The negative first-order serial correlation in monthly stock returns is highly significant.$^{1}$ Furthermore, significant positive serial correlation is found at longer

* University of California, Los Angeles. I would like to thank Michael Brennan, Bradford DeLong, Peter Frost, Bruce Lehmann, Suresh Sundaresan, Sheridan Titman, and Arthur Warga and particularly David Modest for helpful comments. I am solely responsible for all remaining errors.

$^{1}$ Following up on the results presented here, Lehmann (1988) examines the behavior of weekly returns of individual stocks and also finds significant negative first-order serial correlation.

881

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 3

882

The Journal of Finance

lags, and the twelve-month serial correlation is particularly strong. It is also found that the returns on securities in all size-sorted quintiles exhibit qualitatively similar patterns of serial correlation. Thus, the predictable pattern of stock returns documented here appears to be a pervasive phenomenon.

To investigate the economic significance of the observed empirical regularity, ten portfolios are formed based on returns predicted using ex ante estimates of the regression parameters. The difference between the risk-adjusted excess returns on the extreme decile portfolios thus formed is 2.49 percent per month over the period 1934–1987, 2.20 percent per month excluding January, and 4.37 percent per month when the month of January is considered separately. It is also found that the difference between the risk-adjusted excess returns on the extreme decile portfolios formed on the basis of one-month lagged returns is 1.99 percent per month over the sample period and 1.75 percent per month outside January, both statistically significant. These results appear quite striking and suggest that the extent to which security returns can be predicted based on past returns is economically significant.

The rest of the paper is organized as follows. In the next section the model for the empirical tests and the results are presented. The economic significance of these results is addressed in Section II. Possible explanations for the empirical regularity are investigated in Section III, and Section IV contains the concluding remarks.

# I. Empirical Test

## A. The Model

The model to examine the serial correlation properties of returns of individual securities is developed in this section. Let $\tilde{R}_{it}$ be the return on security $i$ in month $t$ , which is expressed as

$$
\tilde{R}_{it} = E(R_i) + \tilde{\eta}_{it},
$$

where $E(R_i)$ is the unconditional expected return on security $i$ and $\tilde{\eta}_{it}$ is the unexpected return in month $t$ , in an unconditional sense. Consider the following cross-sectional regression model: $^{2}$

$$
\tilde{R}_{it} = a_{0t} - \sum_{j=1}^{J} a_{jt} R_{it-j} + \tilde{u}_{it}.
$$

The expression for the slope coefficients in the multivariate regression above is

$$
\begin{bmatrix}
a_{1t} \\
\vdots \\
a_{Jt}
\end{bmatrix}
=
\begin{bmatrix}
\text{cov}_i \left\{
\begin{array}{c}
R_{it-1} \\
\vdots \\
R_{it-J}
\end{array}
\right\}
\end{bmatrix}^{-1}
\begin{bmatrix}
\text{cov}_i(R_{it}, R_{it-1}) \\
\vdots \\
\text{cov}_i(R_{it}, R_{it-J})
\end{bmatrix}.
$$

$^{2}$ A natural way to investigate the serial correlation properties of individual security returns would perhaps be to separately examine their time-series behavior either by using time-series regression tests as in Fama (1965) or by using the variance ratio tests as in Lo and MacKinlay (1988). However, under these procedures, the use of parameter estimates aggregated across securities for statistical inference would pose a problem due to the cross-sectional dependence of the estimates.

This content downloaded from 147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC All use subject to https://about.jstor.org/terms

---

# Page 4

# Evidence of Predictable Behavior of Security Returns

The subscript under covariance operator has been included to emphasize that this operation is carried out across the cross-section. Expanding the components of the second term on the right-hand side using (1) and taking expectations, we get

$$
\text{cov}_i(R_{it}, R_{it-J}) = \text{cov}_i(\eta_{it}, \eta_{it-J}) + \text{var}_i(E(R_i)).
$$

As can be seen from the expression above, the covariance term has two components. The first component is the average serial covariance of individual security returns. The second component is the cross-sectional variance of unconditionally expected returns. While the first component will be zero in the absence of serial correlation, the second component will be positive as long as the expected returns vary across the securities in the cross-section. Consider the following cross-sectional regression:

$$
\tilde{R}_{it} - \bar{R}_i = a_{0t} + \sum_{j=1}^{J} a_{jt} R_{it-j} + \tilde{u}_{it},
$$

where $\bar{R}_i$ is an unbiased estimate of the unconditional expected return of security $i$ obtained from a sample period which excludes months $t - J$ through $t$ . Now the covariance between the dependent variable and the $j$ th independent variable is

$$
\text{cov}_i(R_{it} - \bar{R}_i, R_{it-j}) = \text{cov}_i(\eta_{it}, \eta_{it-j}).
$$

In the latter regression the slope coefficients will be different from zero only if the security returns are serially correlated. The particular cross-sectional regression model used in the empirical tests is

$$
\tilde{R}_{it} - \bar{R}_{it} = a_{0t} + \sum_{j=1}^{12} a_{jt} R_{it-j} + a_{13t} R_{it-24} + a_{14t} R_{it-36} + \tilde{u}_{it}, \quad (2)
$$

where $\bar{R}_{it}$ is the mean monthly return of security $i$ in the sample period $t + 1$ to $t + 60$ . $^3$

## B. Results

The security returns data are obtained from the Center for Research in Security Prices (CRSP) monthly returns file. The regression model (2) is fitted separately for each month using the OLS procedure. $^4$ The parameter estimates and the test statistics are obtained from the time series of monthly cross-sectional regression estimates as in Fama and MacBeth (1973). The tests in this section are conducted over the period 1929–1982. $^5$

---

$^3$ The results of the regression were not sensitive to the choice of the sample period over which $\bar{R}_{it}$ ’s were estimated, and similar results were obtained even when $\bar{R}_{it}$ was estimated over a sample period of four or six years. Furthermore, the slope coefficients in the regression with the raw returns as the dependent variable were also close to the estimates reported here, which suggests that the effect of the cross-sectional differences in expected returns on the estimates of the slope coefficients is small (see Jegadeesh (1987) for details).

$^4$ The results using the weighted least squares procedure were also similar to those reported here. The standard deviations of individual security returns estimated in the sample period $t + 1$ to $t + 60$ were used to deflate the observations under the weighted least squares procedure.

$^5$ The starting and ending periods of the latest version of the CRSP monthly returns data set when this study was initiated were January 1926 and December 1987, respectively. Since the thirty-six month lagged return is used as an independent variable, the starting period for the tests is January 1929, and, since five years of ex post data are used to estimate the unconditional mean return of each security, the test period ends in December 1982.

---

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 5

884

The Journal of Finance

The results are presented in Table I. The regression estimates reveal a striking pattern of serial correlation. The slope coefficients ( $t$ -statistics) at lags one and twelve are particularly high at $-0.092$ ( $-18.58$ ) and $.034$ ( $9.09$ ), respectively. $^{6}$ While the coefficients $a_1$ and $a_2$ are negative, the rest are all positive. The coefficients $a_2$ and $a_8$ are insignificantly different from zero, $a_7$ is significant at the five percent level, and all the other slope coefficients are significant at the one percent level. Even the coefficients at lags twenty-four and thirty-six are significant, with $t$ -statistics of $4.76$ and $6.57$ , respectively. $^{7}$ The $F$ -statistic $^{8}$ under the hypothesis that all slope coefficients are jointly equal to zero is $48.97$ , which is significant at the one percent level. The rejection of the equality of the slope coefficients is not attributable solely to the significantly negative slope coefficient $a_1$ . The hypothesis that the coefficients $a_2$ to $a_{14}$ are jointly equal to zero is also rejected with an $F$ -statistic ( $p$ -value) of $17.59$ ( $0.00$ ). The average adjusted $R^2$ of the monthly cross-sectional regressions is $0.108$ ; i.e., on average the lagged returns considered here explain $10.8$ percent of the cross-sectional variation in individual security returns.

A number of earlier studies have documented that stock returns in January contain a predictable component, while the returns outside January have generally been reported as unpredictable. $^{9}$ Therefore, it is important to investigate whether the results presented here are entirely driven by the anomalous behavior of security returns in January. Hence, the tests are repeated within and outside the month of January.

$^{6}$ The estimate of $a_1$ here differs sharply from the estimate of the slope coefficient obtained by Rosenberg and Rudd (1982), using a univariate regression model. Their estimate of the slope coefficient is $-0.013$ ( $t$ -statistic $= -0.47$ ), which leads them to conclude that “for actual returns the serial correlation is indistinguishable from pure randomness.” Though there are some differences in the specification and estimation of the regression model, I am unable to fully explain the reason for the large difference in the estimates.

$^{7}$ DeBondt and Thaler (1985) report that the security returns can be predicted based on 3- to 5-year lagged returns. The results documented here differ fundamentally from their results. First, DeBondt and Thaler examine the predictive ability of lagged multi-year returns, while the predictive ability of monthly returns at different lags is examined here. The lagged long horizon returns used by DeBondt and Thaler predict future returns only in the month of January (see DeBondt and Thaler (1987)), while the empirical regularity documented here is observed in all calendar months. Finally, DeBondt and Thaler find a negative relation between lagged multi-year returns and the returns in the ensuing January, while a positive relation between the monthly returns and the returns at long lags is observed here in all calendar months.

$^{8}$ The $F$ -statistic is computed as follows. Let $K$ be the number of slope coefficients, and let $\delta$ be a $K \times 1$ vector with elements $\delta_i = \hat{a}_i$ . The $F$ -statistic is given by

$$
\frac{T(T-K)}{K(T-1)} \delta' \hat{\Sigma}^{-1} \delta \sim F(K, T-K),
$$

where $T$ is the number of cross-sectional regressions. $\hat{\Sigma}$ is the sample variance-covariance matrix of $\delta$ .

$^{9}$ For instance, Branch (1977) and Reinganum (1983) find that stock returns in January are negatively related to returns in the previous year, and DeBondt and Thaler (1987) find a similar relation between January returns and the returns in the previous three to five years. Jegadeesh (1989) reports that the long-term mean reversion of market returns reported by Fama and French (1988) is also concentrated in the month of January. However, none of these studies finds any significant predictable pattern outside January.

This content downloaded from 147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC All use subject to https://about.jstor.org/terms

---

# Page 6

# Evidence of Predictable Behavior of Security Returns

885

## Table I

### Cross-Sectional Regression Estimates

Model: $\bar{R}_{it} - \bar{R}_{it} = \alpha_{it} + \sum_{j=1}^{12} a_{jt} R_{it-j} + a_{14t} R_{it-24} + \hat{u}_{it}$ , where $R_{it}$ is the return on security $i$ in month $t$ and $\bar{R}_{it}$ is the average monthly return on security $i$ in the sample period $t+1$ to $t+60$ . The above cross-sectional regression is fitted each month across the full sample of securities and also within size-based subsamples. The securities in the quintile of small firms ( $Q1$ ), medium sized firms ( $Q3$ ), and large firms ( $Q5$ ) make up the three subsamples. The sample period is 1929–1982.

<table>
  <thead>
    <tr>
      <th>Sample Period</th>
      <th> $\hat{a}_0$ </th>
      <th> $\hat{a}_1$ </th>
      <th> $\hat{a}_2$ </th>
      <th> $\hat{a}_3$ </th>
      <th> $\hat{a}_4$ </th>
      <th> $\hat{a}_5$ </th>
      <th> $\hat{a}_6$ </th>
      <th> $\hat{a}_7$ </th>
      <th> $\hat{a}_8$ </th>
      <th> $\hat{a}_9$ </th>
      <th> $\hat{a}_{10}$ </th>
      <th> $\hat{a}_{11}$ </th>
      <th> $\hat{a}_{12}$ </th>
      <th> $\hat{a}_{13}$ </th>
      <th> $\hat{a}_{14}$ </th>
      <th> $R^2_{it}$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>All</td>
      <td>-0.0033</td>
      <td>-0.0923</td>
      <td>-0.0073</td>
      <td>0.0208</td>
      <td>0.0154</td>
      <td>0.0148</td>
      <td>0.0205</td>
      <td>0.0087</td>
      <td>0.0065</td>
      <td>0.0178</td>
      <td>0.0151</td>
      <td>0.0224</td>
      <td>0.0339</td>
      <td>0.0171</td>
      <td>0.0187</td>
      <td>0.108</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.78)</td>
      <td>(-18.58)</td>
      <td>(-1.73)</td>
      <td>(4.77)</td>
      <td>(3.75)</td>
      <td>(3.18)</td>
      <td>(4.75)</td>
      <td>(2.14)</td>
      <td>(1.65)</td>
      <td>(5.15)</td>
      <td>(4.38)</td>
      <td>(6.62)</td>
      <td>(9.09)</td>
      <td>(4.76)</td>
      <td>(6.57)</td>
      <td></td>
    </tr>
    <tr>
      <td>Jan</td>
      <td>0.0126</td>
      <td>-0.2261</td>
      <td>-0.0912</td>
      <td>-0.0645</td>
      <td>-0.0523</td>
      <td>-0.0042</td>
      <td>-0.0351</td>
      <td>-0.0279</td>
      <td>-0.0351</td>
      <td>-0.0272</td>
      <td>-0.0117</td>
      <td>-0.0802</td>
      <td>0.0292</td>
      <td>0.0337</td>
      <td>0.178</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(2.06)</td>
      <td>(-9.42)</td>
      <td>(-5.38)</td>
      <td>(-3.05)</td>
      <td>(-2.81)</td>
      <td>(-2.22)</td>
      <td>(-2.29)</td>
      <td>(-3.20)</td>
      <td>(-1.68)</td>
      <td>(-2.60)</td>
      <td>(-1.87)</td>
      <td>(-0.89)</td>
      <td>(4.81)</td>
      <td>(2.76)</td>
      <td>(2.64)</td>
      <td></td>
    </tr>
    <tr>
      <td>Feb-Dec</td>
      <td>-0.0047</td>
      <td>-0.0801</td>
      <td>0.0004</td>
      <td>0.0296</td>
      <td>0.0215</td>
      <td>0.0198</td>
      <td>0.0228</td>
      <td>0.0144</td>
      <td>0.0096</td>
      <td>0.0226</td>
      <td>0.0190</td>
      <td>0.0255</td>
      <td>0.0297</td>
      <td>0.0160</td>
      <td>0.0174</td>
      <td>0.102</td>
    </tr>
    <tr>
      <td></td>
      <td>(-2.45)</td>
      <td>(-17.20)</td>
      <td>(0.09)</td>
      <td>(6.78)</td>
      <td>(5.32)</td>
      <td>(4.15)</td>
      <td>(5.03)</td>
      <td>(3.50)</td>
      <td>(2.41)</td>
      <td>(6.47)</td>
      <td>(5.44)</td>
      <td>(7.35)</td>
      <td>(7.96)</td>
      <td>(4.21)</td>
      <td>(6.02)</td>
      <td></td>
    </tr>
    <tr>
      <td>Q1</td>
      <td>-0.0037</td>
      <td>-0.1342</td>
      <td>-0.0264</td>
      <td>0.0117</td>
      <td>0.0070</td>
      <td>0.0090</td>
      <td>0.0182</td>
      <td>0.0067</td>
      <td>0.0071</td>
      <td>0.0125</td>
      <td>0.0143</td>
      <td>0.0178</td>
      <td>0.0248</td>
      <td>0.0087</td>
      <td>0.0192</td>
      <td>0.093</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.06)</td>
      <td>(-19.03)</td>
      <td>(-4.54)</td>
      <td>(1.89)</td>
      <td>(1.30)</td>
      <td>(1.51)</td>
      <td>(3.06)</td>
      <td>(1.14)</td>
      <td>(1.25)</td>
      <td>(2.13)</td>
      <td>(2.56)</td>
      <td>(3.49)</td>
      <td>(4.38)</td>
      <td>(1.65)</td>
      <td>(3.65)</td>
      <td></td>
    </tr>
    <tr>
      <td>Jan</td>
      <td>0.0304</td>
      <td>-0.3117</td>
      <td>-0.1061</td>
      <td>-0.0907</td>
      <td>-0.0921</td>
      <td>-0.0609</td>
      <td>-0.0180</td>
      <td>-0.0713</td>
      <td>-0.0159</td>
      <td>-0.0368</td>
      <td>-0.0174</td>
      <td>-0.0070</td>
      <td>0.0691</td>
      <td>0.0050</td>
      <td>0.0344</td>
      <td>0.158</td>
    </tr>
    <tr>
      <td></td>
      <td>(2.41)</td>
      <td>(-8.79)</td>
      <td>(-5.18)</td>
      <td>(-3.10)</td>
      <td>(-3.73)</td>
      <td>(-2.14)</td>
      <td>(-0.99)</td>
      <td>(-3.07)</td>
      <td>(-0.71)</td>
      <td>(-1.80)</td>
      <td>(-0.75)</td>
      <td>(-0.33)</td>
      <td>(2.93)</td>
      <td>(0.33)</td>
      <td>(1.15)</td>
      <td></td>
    </tr>
    <tr>
      <td>Feb-Dec</td>
      <td>-0.0068</td>
      <td>-0.1181</td>
      <td>-0.0192</td>
      <td>0.0210</td>
      <td>0.0160</td>
      <td>0.0154</td>
      <td>0.0215</td>
      <td>0.0138</td>
      <td>0.0092</td>
      <td>0.0169</td>
      <td>0.0171</td>
      <td>0.0201</td>
      <td>0.0208</td>
      <td>0.0090</td>
      <td>0.0179</td>
      <td>0.087</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.88)</td>
      <td>(-17.86)</td>
      <td>(-3.20)</td>
      <td>(3.45)</td>
      <td>(3.02)</td>
      <td>(2.59)</td>
      <td>(3.43)</td>
      <td>(2.30)</td>
      <td>(1.56)</td>
      <td>(2.79)</td>
      <td>(3.01)</td>
      <td>(3.85)</td>
      <td>(3.60)</td>
      <td>(1.61)</td>
      <td>(3.52)</td>
      <td></td>
    </tr>
    <tr>
      <td>Q3</td>
      <td>-0.0043</td>
      <td>-0.0881</td>
      <td>-0.0060</td>
      <td>0.0200</td>
      <td>0.0187</td>
      <td>0.0117</td>
      <td>0.0192</td>
      <td>0.0053</td>
      <td>0.0030</td>
      <td>0.0121</td>
      <td>0.0142</td>
      <td>0.0226</td>
      <td>0.0256</td>
      <td>0.0253</td>
      <td>0.0181</td>
      <td>0.113</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.82)</td>
      <td>(-14.82)</td>
      <td>(-1.13)</td>
      <td>(3.38)</td>
      <td>(3.30)</td>
      <td>(1.99)</td>
      <td>(3.45)</td>
      <td>(0.97)</td>
      <td>(-0.54)</td>
      <td>(2.44)</td>
      <td>(2.99)</td>
      <td>(4.79)</td>
      <td>(5.41)</td>
      <td>(5.31)</td>
      <td>(3.83)</td>
      <td></td>
    </tr>
    <tr>
      <td>Jan</td>
      <td>0.0235</td>
      <td>-0.1662</td>
      <td>-0.0607</td>
      <td>-0.0758</td>
      <td>-0.0752</td>
      <td>-0.0624</td>
      <td>-0.0102</td>
      <td>-0.0076</td>
      <td>-0.0404</td>
      <td>-0.0312</td>
      <td>-0.0280</td>
      <td>-0.0177</td>
      <td>0.0478</td>
      <td>0.0282</td>
      <td>0.0120</td>
      <td>0.149</td>
    </tr>
    <tr>
      <td></td>
      <td>(3.33)</td>
      <td>(-7.11)</td>
      <td>(-3.24)</td>
      <td>(-3.27)</td>
      <td>(-3.35)</td>
      <td>(-2.99)</td>
      <td>(-0.51)</td>
      <td>(-0.38)</td>
      <td>(-1.94)</td>
      <td>(-1.60)</td>
      <td>(-1.85)</td>
      <td>(-1.00)</td>
      <td>(3.13)</td>
      <td>(1.81)</td>
      <td>(0.84)</td>
      <td></td>
    </tr>
    <tr>
      <td>Feb-Dec</td>
      <td>-0.0068</td>
      <td>-0.0810</td>
      <td>-0.0010</td>
      <td>0.0287</td>
      <td>0.0272</td>
      <td>0.0219</td>
      <td>0.0064</td>
      <td>0.0004</td>
      <td>0.0161</td>
      <td>0.0181</td>
      <td>0.0262</td>
      <td>0.0236</td>
      <td>0.0250</td>
      <td>0.0186</td>
      <td>0.109</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(-2.76)</td>
      <td>(-13.38)</td>
      <td>(-0.19)</td>
      <td>(4.81)</td>
      <td>(4.78)</td>
      <td>(3.78)</td>
     

---

# Page 7

886

The Journal of Finance

In the sample period excluding January,$^{10}$ the one-month lagged return coefficient is still negative, while the other slope coefficients are positive (see Table I). As before, the coefficients $a_1$ and $a_{12}$ are bigger in absolute magnitude than the rest. These estimates ($t$-statistics) are $-0.80$ ($-17.2$) and $0.030$ ($7.96$), respectively. Here again, even the thirty-six month lagged return coefficient is significant at $0.017$ ($6.02$). Interestingly, the coefficients at lags three, six, and nine appear bigger than those at the lags adjacent to them. The $F$-statistic under the hypothesis that all the slope coefficients are jointly equal to zero is $43.51$, which suggests rejection of the hypothesis at the conventional levels of significance.$^{11}$ Thus, the results are not driven by anomalous return behavior in January.

When the month of January is considered separately, a different pattern of returns behavior emerges. All slope coefficients up to lag eleven are negative, while the higher order lag coefficients are positive. Strong negative serial correlation over long lags that is observed in January is consistent with the findings of Branch (1977) and Reinganum (1983) that “losers” in the previous year experience abnormally high returns in January. The $F$-statistic ($p$-value) under the hypothesis that all slope coefficients in January are jointly equal to the corresponding coefficients in the other months is $11.64$ ($0.00$). Thus, the pattern of returns behavior in January appears to be significantly different from that outside January. In the month of January, most of the slope coefficients are significant at the five percent level, and the insignificant coefficients in this sample period are generally of the same order of magnitude as the corresponding estimates over the entire period. The statistical insignificance of these estimates could perhaps be attributed to the lower power of the test due to fewer number of time series observations when January is considered separately. The point estimates of the coefficients at short lags and the coefficients at lags twelve and twenty-four are more than twice as large in absolute value as the corresponding coefficients in the other months. For instance, coefficients $a_1$ and $a_{12}$ are $-0.226$ and $0.080$, respectively, in January, while the corresponding estimates outside January are $-0.80$ and $0.030$. The $F$-statistic ($p$-value) under the hypothesis that all slope coefficients in January are jointly equal to zero is $10.73$ ($0.00$).

Next, the pattern of serial correlation across different size groups of stocks is examined. The stocks in the sample are sorted on the basis of market value of equity and assigned to five size-based groups. The group $Q1$ contains the quintile of small firm stocks, $Q2$ contains the stocks in the next size quintile, and so on. The groups are revised every month based on firm size at the end of the previous month, and the regression model (2) is fitted within each group. The parameter estimates for $Q1$, $Q3$, and $Q5$ are presented in Table I.$^{12}$ The pattern of serial correlation outside January appears similar across all size-based quintiles. In the month of January, however, the absolute magnitudes of the slope coefficients for the group of small firm stocks are generally bigger than the corresponding

---

$^{10}$ Specifically, cross-sectional regressions where January returns enter as the dependent variables are excluded from the sample.

$^{11}$ The hypothesis that the slope coefficients $a_2$ to $a_{14}$ are jointly equal to zero is rejected here also at the one percent level of significance.

$^{12}$ The parameter estimates for the groups $Q2$ and $Q4$ are similar to those reported for the other groups.

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 8

Evidence of Predictable Behavior of Security Returns 887

coefficients in the other groups. The hypothesis that all slope coefficients are jointly equal to zero can be rejected at the one percent level of significance in every size-based group.

Furthermore, the serial correlation in security returns is not confined to any isolated subperiod within the sample. Analysis of the regression estimates within four roughly equal subperiods revealed a similar pattern of serial correlation in every sample period. $^{13}$ Thus, there seems to be reliable evidence that the serial correlation in stock returns is a general phenomenon, observed over a fairly long period and also across the entire cross-section of stocks.

## II. Prediction of Security Returns

### A. Portfolio Formation Procedure

A total of over a half million observations were used in fitting the regressions reported in the last section. With such a large number of observations, the regression estimates are obtained with high precision, and hence even small deviations, possibly of little economic consequence, could lead to statistical rejection of the null hypothesis. The objective of this section is to evaluate the economic significance of the observed serial correlation.

Three different trading strategies are considered in order to investigate the significance of different aspects of the predictability reported. The first strategy, labeled $S0$ , uses the out-of-sample return forecasts obtained from the following model:

$$
\hat{R}_{it} = \hat{a}_{0t} + \sum_{j=1}^{12} \hat{a}_{jt} R_{it-j} + \hat{a}_{13t} R_{it-24} + \hat{a}_{14t} R_{it-36}
$$

where $\hat{a}_{jt}$ ’s are estimated from a regression model similar to the regression model (2), with the raw return $\hat{R}_{it}$ as the dependent variable in the place of $\hat{R}_{it} - \bar{R}_{it}$ , $^{14}$ over the period $t - 60$ to $t - 1$ , and these estimates are updated every month. $^{15}$ The securities are ranked in descending order on the basis of predicted returns, and ten predictive portfolios are formed. Specifically, the securities in the top decile are assigned to portfolio $P1$ , the securities in the next decile are assigned to portfolio $P2$ , and so on, and each security in a portfolio is assigned equal weight. The same procedure is used every month to revise the predictive portfolios. Since data over five years are needed to estimate the parameters in the forecasting model, the starting period for portfolio formation is January 1934, and the ending period is 1987 since ex post returns data are not required in the model used here to form the predictive portfolios.

The next two strategies examine the predictive ability based on one- and twelve-month lagged returns. The absolute value of the slope coefficient at lag one is by far the biggest among all the slope coefficients, and hence it is of

---

$^{13}$ The subperiod results are not separately reported here in order to avoid repetition but are available from the author.

$^{14}$ In regression (2) the ex post returns data are used to estimate $\bar{R}_{it}$ . The raw return is used as the dependent variable here in order to avoid the use of ex post data in the forecasting model.

$^{15}$ The $\hat{a}_{jt}$ ’s for the month of January are estimated from the January regressions in the previous five years.

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 9

888

The Journal of Finance

interest to examine the extent to which the security returns can be predicted based solely on the one-month lagged returns. Therefore, under the second trading strategy, labeled $ S1 $ , the securities are ranked in ascending order on the basis of the one-month lagged returns, and the portfolios $ P1 $ to $ P10 $ are formed as outlined above. The next strategy is aimed at examining the importance of the observed serial correlation at the longer lags, which are statistically significant but appear small in magnitude. Specifically, to assess the significance of $ a_{12} $ , the third strategy labeled $ S12 $ is considered. Under this strategy the securities are ranked in descending order on the basis of twelve-month lagged returns, and the portfolios $ P1 $ to $ P10 $ are formed as before.

The abnormal returns earned by the portfolios formed above are estimated under the market model using the following time series regression:

$$
\tilde{R}_{pt} - R_{ft} = \alpha_p + \beta_p (R_{mt} - R_{ft}) + \tilde{u}_{pt},
$$

where $ R_{pt} $ and $ R_{ft} $ are the return on portfolio $ p $ in month $ t $ and the risk-free rate of return, respectively. The interest rate on the one-month T-bills is used as the risk-free rate, and the interest rate data are obtained from the dataset maintained by CRSP. $ R_{mt} $ is the return on the market portfolio, and the CRSP equal-weighted index is used as the market proxy here. $^{16}$ The intercept in the above regression provides the estimate of abnormal return under the market model. Under the null hypothesis, the abnormal returns on all the predictive portfolios are jointly equal to zero, i.e., $ \alpha_p = 0 \forall p $ .

B. Portfolio Performance

The estimates of abnormal returns on the portfolios formed under the three strategies formulated above for the period 1934–1987 are presented in Table II. First consider the strategy $ S0 $ . The abnormal portfolio returns under this strategy, which are plotted in Figure 1, clearly highlight the pattern of excess returns. The order of ranking of excess returns across portfolios exactly matches the order predicted. Portfolios $ P1 $ to $ P5 $ experience positive abnormal returns, while the abnormal returns on the rest of the portfolios are negative. The abnormal return ( $ t $ -statistic) $^{17}$ on portfolio $ P1 $ is 1.11 (12.25) percent per month, and that on $ P10 $ is –1.38 (–16.90) percent per month. Portfolio $ P1 $ earns positive abnormal returns in 71 percent of the months in the sample period, while portfolio $ P10 $ earns positive abnormal returns in only 20 percent of the months (see Table III). Both of these proportions are significantly different from the 50 percent positive realizations that can be expected by pure chance. The difference between the abnormal returns on these portfolios is 2.49 percent per month, or, equivalently, the compounded rate of abnormal return is 34.33 percent per year. The abnormal portfolio returns are also separately examined within and outside January by fitting regression (3) separately within each of these sample periods.

$^{16}$ The use of the CRSP value-weighted index as the market proxy also yielded results that were qualitatively similar to those reported here.

$^{17}$ The heteroskedasticity-consistent estimates of the standard errors suggested by White (1980) are used to compute the $ t $ -statistics.

This content downloaded from 147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC All use subject to https://about.jstor.org/terms

---

# Page 10

# Evidence of Predictable Behavior of Security Returns

The patterns of abnormal returns across the predictive portfolios, both within and outside January, are qualitatively similar to the results discussed above. However, the absolute magnitudes of the abnormal returns are generally higher in January. The difference between the abnormal returns on the extreme decile portfolios is 2.20 percent per month ( $t$ -statistic of 15.63) outside January and 4.37 percent per month (5.42) in January. The $F$ -statistic under the hypothesis that the abnormal returns across the portfolios are jointly equal to zero is 24.89. The $F$ -statistics within and outside January are 2.77 and 24.97, respectively, and the null hypothesis can be rejected at the one percent level of significance.

The patterns of the abnormal portfolio returns under the strategies $S1$ and $S12$ also closely match the pattern implied by the signs of the observed serial correlation at these lags. The differences between the abnormal returns on the extreme decile portfolios under the strategies $S1$ and $S12$ are 1.99 percent and 0.93 percent per month, respectively. The $F$ -statistics under the hypothesis that the abnormal returns on the portfolio $P1$ to $P10$ are jointly equal to zero are 17.94 and 4.99 under the strategies $S1$ and $S12$ , respectively, both significant at the one percent level.

To a large extent, the ranking of the securities under the strategy $S0$ is determined by the one-month lagged returns. However, the improvement in the predictive ability that is achieved due to the use of information in the returns at longer lags is nontrivial. For example, the compounded abnormal return on the predictive portfolio $P1$ – $P10$ under $S0$ is about 7.6 percent per year higher than that under $S1$ , which is statistically significant. Furthermore, the abnormal returns on portfolio $P1$ – $P10$ are positive more often under $S0$ than under $S1$ . Some descriptive measures of the pair-wise relation between the different trading strategies considered here are presented in Table IV. On average, fifty-two percent of the securities in the predictive portfolio $P1$ – $P10$ under the strategy $S0$ are also included in that portfolio under $S1$ .

It is also of interest to evaluate the extent of abnormal returns earned by the predictive portfolios after accounting for transaction costs. Consider the zero net investment portfolio $P1$ – $P10$ . On average, about 91 percent of the securities held in this portfolio were revised each month, and this proportion was about the same under all these strategies. Assuming a two-way transaction cost of 0.5 percent, $^{18}$ the total cost of periodically revising the portfolios amounts to about 0.9 percent of the aggregate value of the long or short position. After accounting for transaction costs, the average abnormal returns under the trading strategies $S0$ and $S1$ are 20.8 percent and 13.9 percent per year (in terms of the value of the long position), respectively. The profits attributable to the trading strategy $S12$ would be swamped by the transaction costs. However, this strategy was considered primarily to assess the importance of the serial correlation estimate and is unlikely to be of interest for the purpose of actual implementation. The net profits on the zero investment portfolios under the strategies $S0$ and $S1$ appear fairly large, and it seems reasonable to conclude that they are economically significant.

---

$^{18}$ Berkowitz et al. (1988) report that the average round-trip cost for securities transaction is less than 0.5 percent.

---

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 11

890

The Journal of Finance

Table II

**Abnormal Returns on the Predictive Portfolios**

Predictive portfolios are formed under three different strategies: S0, S1, and S12. Under S0, ten portfolios are formed on the basis of one-step-ahead return forecasts obtained using ex ante regression estimates. P1 is the equally weighted portfolio of securities in the top decile when ranked in descending order on the basis of return forecasts, P2 is the equally weighted portfolio of securities in the next decile, and so on. Under S1 the securities are ranked in ascending order on the basis of one-month lagged returns, and under S12 the securities are ranked in descending order on the basis of twelve-month lagged returns and ten portfolios are formed as described above. The abnormal returns are estimated using the market model with monthly returns. The sample period is 1934–1987.

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="2">S0</th>
      <th colspan="2">S1</th>
      <th colspan="2">S12</th>
    </tr>
    <tr>
      <th>Jan–Dec</th>
      <th>Feb–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Feb–Dec</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>P1</td>
      <td>0.0111<br>(12.25)</td>
      <td>0.0241<br>(5.46)</td>
      <td>0.0092<br>(10.96)</td>
      <td>0.0096<br>(10.21)</td>
      <td>0.0181<br>(3.86)</td>
      <td>0.0084<br>(9.48)</td>
      <td>0.0041<br>(5.20)</td>
      <td>0.0092<br>(2.92)</td>
      <td>0.0029<br>(3.82)</td>
    </tr>
    <tr>
      <td>P2</td>
      <td>0.0062<br>(10.39)</td>
      <td>0.0069<br>(1.77)</td>
      <td>0.0057<br>(9.37)</td>
      <td>0.0042<br>(6.66)</td>
      <td>0.0085<br>(3.47)</td>
      <td>0.0039<br>(5.90)</td>
      <td>0.0029<br>(5.29)</td>
      <td>0.0030<br>(1.16)</td>
      <td>0.0028<br>(4.96)</td>
    </tr>
    <tr>
      <td>P3</td>
      <td>0.0037<br>(7.31)</td>
      <td>0.0065<br>(2.63)</td>
      <td>0.0034<br>(6.71)</td>
      <td>0.0020<br>(4.34)</td>
      <td>0.0051<br>(3.16)</td>
      <td>0.0019<br>(3.78)</td>
      <td>0.0016<br>(3.31)</td>
      <td>−0.0006<br>(−0.35)</td>
      <td>0.0017<br>(3.38)</td>
    </tr>
    <tr>
      <td>P4</td>
      <td>0.0028<br>(6.62)</td>
      <td>0.0041<br>(2.03)</td>
      <td>0.0026<br>(6.13)</td>
      <td>0.0014<br>(3.09)</td>
      <td>0.0040<br>(1.73)</td>
      <td>0.0014<br>(2.96)</td>
      <td>0.0017<br>(3.84)</td>
      <td>0.0020<br>(0.95)</td>
      <td>0.0018<br>(4.16)</td>
    </tr>
    <tr>
      <td>P5</td>
      <td>0.0013<br>(3.32)</td>
      <td>−0.0015<br>(−0.99)</td>
      <td>0.0016<br>(3.81)</td>
      <td>0.0013<br>(3.15)</td>
      <td>0.0012<br>(0.73)</td>
      <td>0.0015<br>(3.51)</td>
      <td>0.0007<br>(1.77)</td>
      <td>0.0000<br>(0.01)</td>
      <td>0.0009<br>(2.08)</td>
    </tr>
  </tbody>
</table>

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 12

# Evidence of Predictable Behavior of Security Returns

891

<table>
  <thead>
    <tr>
      <th rowspan="2">Table II—Continued</th>
      <th colspan="3">S0</th>
      <th colspan="3">S1</th>
      <th colspan="3">S12</th>
    </tr>
    <tr>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>P6</td>
      <td>-0.0002<br>(-0.38)</td>
      <td>-0.0019<br>(-1.00)</td>
      <td>0.0002<br>(0.49)</td>
      <td>0.0003<br>(0.76)</td>
      <td>-0.0005<br>(-0.27)</td>
      <td>0.0006<br>(1.48)</td>
      <td>0.0006<br>(1.52)</td>
      <td>-0.0013<br>(-0.80)</td>
      <td>0.0009<br>(2.25)</td>
    </tr>
    <tr>
      <td>P7</td>
      <td>-0.0016<br>(-3.38)</td>
      <td>-0.0063<br>(-2.59)</td>
      <td>-0.0009<br>(-1.92)</td>
      <td>-0.0013<br>(-2.76)</td>
      <td>-0.0029<br>(-1.28)</td>
      <td>-0.0010<br>(-2.07)</td>
      <td>-0.0005<br>(-1.12)</td>
      <td>-0.0040<br>(-2.04)</td>
      <td>0.0000<br>(0.07)</td>
    </tr>
    <tr>
      <td>P8</td>
      <td>-0.0027<br>(-4.86)</td>
      <td>-0.0088<br>(-2.92)</td>
      <td>-0.0018<br>(-3.36)</td>
      <td>-0.0019<br>(-3.60)</td>
      <td>-0.0090<br>(-4.35)</td>
      <td>-0.0012<br>(-2.25)</td>
      <td>-0.0012<br>(-2.39)</td>
      <td>-0.0054<br>(-1.98)</td>
      <td>-0.0007<br>(-1.48)</td>
    </tr>
    <tr>
      <td>P9</td>
      <td>-0.0062<br>(-9.63)</td>
      <td>-0.0140<br>(-4.72)</td>
      <td>-0.0051<br>(-8.04)</td>
      <td>-0.0046<br>(-7.01)</td>
      <td>-0.0132<br>(-4.35)</td>
      <td>-0.0037<br>(-5.87)</td>
      <td>-0.0027<br>(-4.46)</td>
      <td>-0.0045<br>(-1.78)</td>
      <td>-0.0020<br>(-3.34)</td>
    </tr>
    <tr>
      <td>P10</td>
      <td>-0.0138<br>(-16.90)</td>
      <td>-0.0196<br>(-4.38)</td>
      <td>-0.0127<br>(-15.51)</td>
      <td>-0.0102<br>(-11.98)</td>
      <td>-0.0208<br>(-5.98)</td>
      <td>-0.0091<br>(-10.64)</td>
      <td>-0.0052<br>(-6.82)</td>
      <td>-0.0081<br>(-2.09)</td>
      <td>-0.0044<br>(-5.55)</td>
    </tr>
    <tr>
      <td>P1–P10</td>
      <td>0.0249<br>(16.82)</td>
      <td>0.0437<br>(5.42)</td>
      <td>0.0220<br>(15.63)</td>
      <td>0.0199<br>(12.55)</td>
      <td>0.0389<br>(5.23)</td>
      <td>0.0175<br>(11.60)</td>
      <td>0.0093<br>(6.94)</td>
      <td>0.0173<br>(2.83)</td>
      <td>0.0073<br>(5.48)</td>
    </tr>
    <tr>
      <td>F-statistic</td>
      <td>24.89<br>(0.00)</td>
      <td>2.77<br>(0.01)</td>
      <td>24.97<br>(0.00)</td>
      <td>17.94<br>(0.00)</td>
      <td>4.10<br>(0.00)</td>
      <td>16.31<br>(0.00)</td>
      <td>4.99<br>(0.00)</td>
      <td>0.68<br>(0.74)</td>
      <td>4.42<br>(0.00)</td>
    </tr>
    <tr>
      <td>p-Value</td>
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

The White $t$-statistics are presented within parentheses. The $F$-statistics are obtained under the hypothesis that the abnormal returns on all portfolios are jointly equal to zero. Note that the abnormal return when all calendar months are simultaneously considered is not a weighted average of the abnormal returns in January and outside January since the estimates of systematic risk and the average excess market returns in the two subperiods are different.

This content downloaded from 147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 13

892

The Journal of Finance

![image](image_1.png)

Figure 1. Abnormal returns on predictive portfolios (1934–1987). The predictive portfolios are formed under the trading strategy S0. See Table II for a description of this trading strategy.

Table III

Proportion of Positive Abnormal Returns on the Predictive Portfolios

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="3">S0</th>
      <th colspan="3">S1</th>
      <th colspan="3">S12</th>
    </tr>
    <tr>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>P1</td><td>.705</td><td>.741</td><td>.704</td><td>.651</td><td>.611</td><td>.665</td><td>.605</td><td>.648</td><td>.591</td></tr>
    <tr><td>P2</td><td>.707</td><td>.685</td><td>.704</td><td>.623</td><td>.759</td><td>.614</td><td>.603</td><td>.574</td><td>.611</td></tr>
    <tr><td>P3</td><td>.651</td><td>.648</td><td>.648</td><td>.603</td><td>.722</td><td>.593</td><td>.574</td><td>.444</td><td>.579</td></tr>
    <tr><td>P4</td><td>.630</td><td>.667</td><td>.628</td><td>.588</td><td>.704</td><td>.577</td><td>.588</td><td>.667</td><td>.591</td></tr>
    <tr><td>P5</td><td>.571</td><td>.463</td><td>.594</td><td>.566</td><td>.611</td><td>.581</td><td>.552</td><td>.574</td><td>.557</td></tr>
    <tr><td>P6</td><td>.517</td><td>.519</td><td>.532</td><td>.543</td><td>.519</td><td>.552</td><td>.520</td><td>.426</td><td>.539</td></tr>
    <tr><td>P7</td><td>.443</td><td>.333</td><td>.480</td><td>.466</td><td>.370</td><td>.465</td><td>.502</td><td>.407</td><td>.515</td></tr>
    <tr><td>P8</td><td>.418</td><td>.333</td><td>.419</td><td>.451</td><td>.333</td><td>.466</td><td>.461</td><td>.407</td><td>.470</td></tr>
    <tr><td>P9</td><td>.332</td><td>.241</td><td>.342</td><td>.394</td><td>.315</td><td>.397</td><td>.406</td><td>.463</td><td>.404</td></tr>
    <tr><td>P10</td><td>.204</td><td>.185</td><td>.197</td><td>.278</td><td>.185</td><td>.283</td><td>.349</td><td>.352</td><td>.347</td></tr>
    <tr><td>P1–P10</td><td>.796</td><td>.741</td><td>.788</td><td>.716</td><td>.741</td><td>.712</td><td>.657</td><td>.685</td><td>.636</td></tr>
  </tbody>
</table>

See Table II for the description of trading strategies. The entries indicate the proportion of the months in the sample period in which the respective portfolios earned positive abnormal returns. Note that the proportion of positive abnormal returns when all calendar months are simultaneously considered is not a weighted average of the corresponding proportions in January and outside January since the estimates of systematic risk and the average excess market returns in the two subperiods are different.

## III. Possible Explanations

### A. Size-Based Risk Adjustment

It is possible that the market model used for risk adjustment is inadequate. For instance, the size effect documented by Banz (1981) suggests that the market model does not adequately adjust for certain size-related risk. To investigate whether alternate procedures for risk adjustment could explain the observed

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 14

# Evidence of Predictable Behavior of Security Returns

## Table IV

### Relation between Trading Strategies

<table>
  <thead>
    <tr>
      <th colspan="3">I. Proportion of securities in the predictive portfolio $P1–P10$ under one strategy which are also included in the predictive portfolio under another trading strategy</th>
    </tr>
    <tr>
      <th></th>
      <th>S0</th>
      <th>S1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>S1</td>
      <td>.516</td>
      <td></td>
    </tr>
    <tr>
      <td>S12</td>
      <td>.220</td>
      <td>.128</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th colspan="3">II. Spearman rank correlation coefficient</th>
    </tr>
    <tr>
      <th></th>
      <th>S0</th>
      <th>S1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>S1</td>
      <td>.664</td>
      <td></td>
    </tr>
    <tr>
      <td>S12</td>
      <td>.202</td>
      <td>–.012</td>
    </tr>
  </tbody>
</table>

empirical regularity, the abnormal returns on the predictive portfolios are estimated under the following size-based model: $^{19}$

$$
\tilde{R}_{pt} = \alpha_0 + b_{pS} R_{St} + b_{pM} R_{Mt} + b_{pL} R_{Lt} + \tilde{u}_{pt},
\quad (4)
$$

where $R_{St}$ , $R_{Mt}$ , and $R_{Lt}$ are the returns on the small-, medium-, and large-firm size-quintile portfolios in month $t$ , respectively.

The estimates of the abnormal returns on the extreme decile portfolios under the size-based returns model are presented in Table V. The estimate of the abnormal return in (4) on the portfolio $P1–P10$ is 2.46 percent (in terms of the value of the long or short position) per month, which is close to the estimate of 2.49 percent under the market model. However, when the month of January is considered separately, the estimate of the abnormal return under the size-based model is 2.37 percent, which is substantially less than the market model estimate of 4.37 percent. Thus, the size-based returns model may account for a part of the empirical anomaly in the month of January, but even here a bulk of the empirical regularity is left unexplained. Similar results are also observed with the predictive portfolios under the strategies $S1$ and $S12$ .

## B. Time-Varying Market Risk

The composition of the predictive portfolios formed in the last section varied from month to month, and therefore their “true” betas could be expected to vary across months. Statistical inference using unconditional estimates from the market model is asymptotically valid if intertemporal changes in portfolio betas are purely random. However, if the betas vary in a systematic fashion, then the estimates of $\alpha_p$ ’s from the market model could be biased. For instance, if $\beta_{P1}$ were high in the periods when the expected market return was high and low in the other periods, and if $\beta_{P10}$ behaved in the opposite manner, then the consequent

$^{19}$ A size-based returns model was first formally proposed by Huberman and Kandel (1985). The size-based returns model used here can be viewed as a specialized empirical specification of a three-factor model.

---

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 15

894

The Journal of Finance

Table V

Predictive Portfolio Abnormal Returns under a Size-Based Model (1934–1987)

The abnormal returns are estimated using the following size-based returns model:

$$
\hat{R}_{pt} = \alpha_0 + \beta_{pS} R_{St} + \beta_{pM} R_{Mt} + \beta_{pL} R_{Lt} + \tilde{\varepsilon}_{pt},
$$

where $R_{St}$ , $R_{Mt}$ , and $R_{Lt}$ are the returns on the small-, medium-, and large-firm size-quintile portfolios in month $t$ .

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="2">S0</th>
      <th colspan="2">S1</th>
      <th colspan="2">S12</th>
    </tr>
    <tr>
      <th>Jan–Dec</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Feb–Dec</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>P1</td>
      <td>0.0103<br>(11.75)</td>
      <td>0.0095<br>(1.85)</td>
      <td>0.0086<br>(9.61)</td>
      <td>0.0032<br>(0.81)</td>
      <td>0.0080<br>(8.91)</td>
      <td>0.0033<br>(4.28)</td>
      <td>0.0009<br>(0.27)</td>
      <td>0.0022<br>(2.80)</td>
    </tr>
    <tr>
      <td>P10</td>
      <td>−0.0143<br>(−17.21)</td>
      <td>−0.0142<br>(−2.51)</td>
      <td>−0.0128<br>(−15.13)</td>
      <td>−0.0105<br>(−12.30)</td>
      <td>−0.0149<br>(−3.49)</td>
      <td>−0.0095<br>(−10.48)</td>
      <td>−0.0058<br>(−7.77)</td>
      <td>−0.0070<br>(−1.12)</td>
      <td>−0.0046<br>(−5.93)</td>
    </tr>
    <tr>
      <td>P1–P10</td>
      <td>0.0246<br>(16.84)</td>
      <td>0.0237<br>(2.42)</td>
      <td>0.0213<br>(14.55)</td>
      <td>0.0191<br>(12.76)</td>
      <td>0.0181<br>(2.03)</td>
      <td>0.0175<br>(11.14)</td>
      <td>0.0091<br>(6.92)</td>
      <td>0.0079<br>(0.92)</td>
      <td>0.0068<br>(5.08)</td>
    </tr>
  </tbody>
</table>

See Table II for the description of strategies S0, S1, and S12. The White $t$ -statistics are presented in parentheses. The estimate of the abnormal return when all calendar months are simultaneously considered is not a weighted average of the corresponding estimates in January and outside January since the slope coefficients in the time series regressions and the mean returns on the size-based portfolios are different in the two subperiods.

This content downloaded from 147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 16

Evidence of Predictable Behavior of Security Returns

bias in estimated $\alpha_p$ 's would be in the direction of the results obtained in the last section. Chan (1988), for instance, argues that the abnormal returns to long-term “winners” and “losers” documented by DeBondt and Thaler (1985) can be explained by such systematic relation between portfolio betas and expected market returns. Chan hypothesizes that the expected market returns are different over the different three-year holding periods of the contrarian portfolios formed based on the DeBondt and Thaler strategy and hence estimates the betas separately over each holding period. Following Chan, the abnormal returns on the predictive portfolios were estimated by fitting the market model within eighteen three-year subperiods. Under this procedure, the differences between the average abnormal returns on the extreme decile portfolios were 2.41 percent, 2.09 percent, and 0.84 percent per months under the strategies $S0$ , $S1$ , and $S12$ , respectively. These estimates are close to the earlier estimates obtained by fitting the market model over the entire sample period. Furthermore, the estimates of the abnormal returns were all positive in each of the eighteen three-year subperiods. These results suggest that time-varying market risk cannot explain the abnormal returns on the predictive portfolios. $^{20}$

C. Bid-Ask Spread and Thin Trading

The security returns are computed using traded prices. The transactions on the stock exchanges occur at the bid or the ask prices, and hence the recorded prices contain a measurement error to the extent of the bid-ask spreads. Since the prices fluctuate between the bid and ask prices, the security returns measured over adjacent intervals will exhibit negative serial correlation (see Roll (1984) for a formal analysis). Additionally, infrequent trading of securities also induces negative serial correlation in measured returns. Intuitively, when securities are thinly traded, the trading intervals do not always coincide with the observation intervals. Therefore, on average, longer trading intervals are followed by shorter trading intervals, and hence, to the extent that the security prices tend to drift upward, high measured returns will on average be followed by low measured returns. This phenomenon induces negative first-order serial correlation in measured returns (see Scholes and Williams (1977)). The measurement error in the recorded prices due to the bid-ask spread and thin trading could potentially bias the estimate of the first-order serial correlation and also overstate the profits from the trading strategies. Though the extent of bias due to these sources is

$^{20}$ I also estimated the abnormal returns using an alternate procedure to account for possible systematic variation in market risk. I specified a stylized model for estimating the one-month-ahead conditionally expected market returns. In this specification, a January dummy, the one-month lagged market return, and the squared one-month lagged market return were used as the predictor variables to determine the expected return on the market the following month. These predetermined variables explained about ten percent of the variance of monthly EWI returns. I estimated the abnormal returns after allowing for the portfolio betas to vary linearly with the changes in conditionally expected market returns. The estimates of the abnormal returns on the predictive portfolios under this procedure were virtually the same as the estimates reported in Section II.

This content downloaded from 147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC All use subject to https://about.jstor.org/terms

---

# Page 17

896

The Journal of Finance

likely to be small when monthly returns are used, $^{21}$ some additional tests, which virtually eliminate the potential bias, are carried out here. These tests are conservative, and the results of these tests provide an upper limit on the extent of bias in the earlier tests.

The thin trading phenomenon and the presence of bid-ask spread bias the estimates only when $R_{it-1}$ and $R_{it}$ are measured over adjacent intervals. Therefore, in order to avoid measurement error-induced biases, $R_{it-1}$ is measured excluding the last trading day in month $t - 1$ . As an added precaution, the securities which did not trade on the last trading day of the month $t - 1$ were deleted from the sample for the month $t$ . $^{22}$ This procedure, while eliminating the bias, also discards potentially useful information contained in the returns on the last trading day. Therefore, the results are likely to overstate the extent of the measurement error-induced bias. The cross-sectional regression (2) is fitted using one-month lagged returns, which excludes the return on the last trading day, over the sample period 1963–1982. $^{23}$ The estimate of $a_1$ ( $t$ -statistic) in the modified regression is $-0.0612$ ( $-8.74$ ), while the corresponding estimate obtained earlier over this sample period was $-0.077$ ( $-10.78$ ). The other slope coefficients remain virtually the same as before.

The abnormal returns on the predictive portfolios formed using the returns in month $t - 1$ excluding the last trading day under the strategies $S0$ and $S1$ are presented in Table VI. In the sample period 1963–1987, the abnormal return on the portfolio $P1$ – $P10$ under the strategy $S0$ , when the return in the entire month $t - 1$ is used for prediction, is 2.07 percent per month, and the corresponding return when the prediction is based on the returns in month $t - 1$ , excluding the last trading day, is 1.77 percent. The corresponding abnormal returns under the strategy $S1$ are 1.53 and 1.08 percent per month, respectively. As can be expected, the elimination of the returns on the last trading day for the purpose of prediction has a greater impact on the strategy $S1$ than on $S0$ . However, even after conservatively controlling for potential bias, the abnormal returns earned by the predictive portfolios appear fairly large.

## IV. Concluding Remarks

This paper documents strong evidence of predictable behavior of security returns. The results here show that the monthly returns on individual stocks exhibit

$^{21}$ For instance, using the results of Roll, it can be shown that the order of bias in the estimate of $a_1$ due to the bid-ask spread is $-E\{spread^2/4 \text{ var}(\hat{R}_t)\}$ , where $spread^2$ is the cross-sectional average of the squared percentage bid-ask spread and $\text{var}(\hat{R}_t)$ is the cross-sectional variance of the percentage security returns at time $t$ . While $E\{spread^2\}$ is independent of the measurement interval, $\text{var}(\hat{R}_t)$ increases with length of the measurement interval. Therefore, the extent of bias reduces as the length of the measurement interval is increased.

$^{22}$ These securities can be identified from the CRSP Daily Master File, where the daily closing prices are reported. In this data set, the transaction-based closing prices are recorded with a positive sign, and the prices based on the average of the bid and the ask prices are recorded with a negative sign.

This selection criterion, on average, results in the exclusion of 0.65 percent of the securities previously included in the sample.

$^{23}$ The daily returns data are obtained from the CRSP daily returns file. The first full calendar year of data available in this data set is 1963.

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 18

# Evidence of Predictable Behavior of Security Returns

## Table VI

### Abnormal Returns on the Predictive Portfolios (1963–1987)

The abnormal returns on the extreme decile portfolios under the strategies S0 and S1 described in Table II are presented in Panel I. Panel II contains the abnormal returns on the predictive portfolios formed under these strategies but using the returns in the month $t - 1$ excluding the last trading day for the purpose of prediction. The returns on the last trading day are not used for prediction in order to avoid potential bias due to the bid-ask spread and due to thin trading.

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="3">S0</th>
      <th colspan="3">S1</th>
    </tr>
    <tr>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
      <th>Jan–Dec</th>
      <th>Jan</th>
      <th>Feb–Dec</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>I</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>P1</td>
      <td>0.0087</td>
      <td>0.0135</td>
      <td>0.0074</td>
      <td>0.0074</td>
      <td>0.0081</td>
      <td>0.0066</td>
    </tr>
    <tr>
      <td></td>
      <td>(7.23)</td>
      <td>(2.06)</td>
      <td>(6.34)</td>
      <td>(6.23)</td>
      <td>(1.37)</td>
      <td>(5.69)</td>
    </tr>
    <tr>
      <td>P10</td>
      <td>−0.0120</td>
      <td>−0.0068</td>
      <td>−0.0114</td>
      <td>−0.0080</td>
      <td>−0.0100</td>
      <td>−0.0072</td>
    </tr>
    <tr>
      <td></td>
      <td>(−10.70)</td>
      <td>(−1.05)</td>
      <td>(−10.63)</td>
      <td>(−6.63)</td>
      <td>(−2.11)</td>
      <td>(−5.98)</td>
    </tr>
    <tr>
      <td>P1–P10</td>
      <td>0.0207</td>
      <td>0.0203</td>
      <td>0.0187</td>
      <td>0.0153</td>
      <td>0.0181</td>
      <td>0.0138</td>
    </tr>
    <tr>
      <td></td>
      <td>(10.30)</td>
      <td>(1.71)</td>
      <td>(9.94)</td>
      <td>(7.41)</td>
      <td>(1.85)</td>
      <td>(6.84)</td>
    </tr>
    <tr>
      <td>II</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>P1</td>
      <td>0.0072</td>
      <td>0.0110</td>
      <td>0.0060</td>
      <td>0.0044</td>
      <td>0.0072</td>
      <td>0.0036</td>
    </tr>
    <tr>
      <td></td>
      <td>(5.90)</td>
      <td>(1.77)</td>
      <td>(4.99)</td>
      <td>(3.86)</td>
      <td>(1.21)</td>
      <td>(3.22)</td>
    </tr>
    <tr>
      <td>P10</td>
      <td>−0.0106</td>
      <td>−0.0056</td>
      <td>−0.0099</td>
      <td>−0.0064</td>
      <td>−0.0072</td>
      <td>−0.0057</td>
    </tr>
    <tr>
      <td></td>
      <td>(−9.38)</td>
      <td>(−0.88)</td>
      <td>(−9.25)</td>
      <td>(−5.33)</td>
      <td>(−1.35)</td>
      <td>(−4.71)</td>
    </tr>
    <tr>
      <td>P1–P10</td>
      <td>0.0177</td>
      <td>0.0166</td>
      <td>0.0158</td>
      <td>0.0108</td>
      <td>0.0144</td>
      <td>0.0092</td>
    </tr>
    <tr>
      <td></td>
      <td>(8.78)</td>
      <td>(1.47)</td>
      <td>(8.28)</td>
      <td>(5.37)</td>
      <td>(1.43)</td>
      <td>(4.72)</td>
    </tr>
  </tbody>
</table>

The White $t$-statistics are presented in parentheses.

significantly negative first-order serial correlation and significantly positive higher-order serial correlation. The pattern of serial correlation exhibits seasonality, with the pattern in January significantly different from that in the other months. Ten portfolios were formed based on the predicted returns using ex ante estimates of the regression parameters. The difference between the abnormal returns on the extreme decile portfolios thus formed was 2.49 percent per month over the period 1934–1987, 2.20 percent per month excluding January, and 4.37 percent per month when the month of January was considered separately. The differences between the abnormal returns on the extreme decile portfolios formed on the basis of the one- and twelve-month lagged returns were 1.99 percent and 0.93 percent per month, respectively.

The results documented here reliably reject the hypothesis that the stock prices follow random walks. Predictability of stock returns can be attributed either to market inefficiency or to systematic changes in expected stock returns. The models of time-varying expected returns considered here were not able to satisfactorily explain the empirical regularity. However, it is possible that the results can be explained by alternate asset pricing model specifications that allow for more general variation in security risk premia. The search for economic models that account for the short-term stock return predictability is left for the future.

## REFERENCES

Banz, Rolfo, 1981, The relationship between return and market value of common stocks, *Journal of Financial Economics* 9, 3–18.

This content downloaded from  
147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC  
All use subject to https://about.jstor.org/terms

---

# Page 19

898

The Journal of Finance

Berkowitz, Stephen A., Dennis E. Logue, and Eugene A. Noser, Jr., 1988, The total cost of transactions on the NYSE, Journal of Finance 43, 97–112.

Branch, Ben, 1977, A tax loss trading rule, Journal of Business 50, 198–207.

Chan, K. C., 1988, On the contrarian investment strategy, Journal of Business 61, 147–163.

DeBondt, Werner, F. M. and Richard Thaler, 1985, Does the stock market overreact?, Journal of Finance 40, 793–805.

—— and Richard Thaler, 1987, Further evidence of investor overreaction and stock market seasonality, Journal of Finance 42, 557–581.

Fama, Eugene F., 1965, The behavior of stock market prices, Journal of Business 38, 34–105.

——, 1970, Efficient capital markets: A review of theory and empirical work, Journal of Finance 25, 383–417.

—— and Kenneth R. French, 1988, Permanent and temporary components of stock prices, Journal of Political Economy 98, 247–273.

—— and J. D. MacBeth, 1973, Risk return and equilibrium: Empirical test, Journal of Political Economy 81, 607–636.

French, Kenneth R. and Richard Roll, 1986, Stock return variances: The arrival of information and reaction of traders, Journal of Financial Economics 17, 5–26.

Huberman, Gur and Shmuel Kandel, 1985, A size-based returns model, Working Paper, University of Chicago.

Jegadeesh, Narasimhan, 1987, Predictable behavior of security returns and tests of asset pricing models, Ph.D. dissertation, Columbia University.

——, 1989, Seasonality in stock price mean reversion: Evidence from the U.S. and the U.K., Working Paper, 13-89, UCLA.

Lehmann, Bruce N., 1988, Fads, martingales, and market efficiency, Working Paper, Columbia University.

Lo, Andrew W. and A. Craig MacKinlay, 1988, Stock market prices do not follow random walks: Evidence from a simple specification test, Review of Financial Studies 1, 41–66.

Reinganum, Marc R., 1983, The anomalous stock market behavior of small firms in January: Empirical tests for tax-loss selling effects, Journal of Financial Economics 12, 89–104.

Roll, Richard, 1984, A simple implicit measure of the effective bid-ask spread in an efficient market, Journal of Finance 39, 1127–1139.

Rosenberg, Barr and Andrew Rudd, 1982, Factor-related and specific returns of common stocks: Serial correlation and market inefficiency, Journal of Finance 37, 543–554.

Scholes, Myron and Joseph Williams, 1977, Estimating betas from nonsynchronous data, Journal of Financial Economics 5, 309–327.

White, Hal, 1980, A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity, Econometrica 48, 817–838.

This content downloaded from 147.8.204.164 on Wed, 05 Aug 2026 07:56:43 UTC All use subject to https://about.jstor.org/terms