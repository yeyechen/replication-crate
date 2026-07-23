# Page 1

JOURNAL OF FINANCIAL AND QUANTITATIVE ANALYSIS Vol. 45, No. 5, Oct. 2010, pp. 1133–1160 COPYRIGHT 2010, MICHAEL G. FOSTER SCHOOL OF BUSINESS, UNIVERSITY OF WASHINGTON, SEATTLE, WA 98195 doi:10.1017/S0022109010000451

# Seasonality in the Cross Section of Stock Returns: The International Evidence

Steven L. Heston and Ronnie Sadka*

## Abstract

This paper studies seasonal predictability in the cross section of international stock returns. Stocks that outperform the domestic market in a particular month continue to outperform the domestic market in that same calendar month for up to 5 years. The pattern appears in Canada, Japan, and 12 European countries. Global trading strategies based on seasonal predictability outperform similar nonseasonal strategies by over 1% per month. Abnormal seasonal returns remain after controlling for size, beta, and value, using global or local risk factors. In addition, the strategies are not highly correlated across countries. This suggests they do not reflect return premiums for systematic global risk.

## I. Introduction

This paper studies predictability in the cross section of international stock returns. It documents a new pattern of annual return continuation in Canada, Japan, and 12 European countries. One reason for examining international markets is to corroborate anomalies that have appeared in U.S. markets. International markets are particularly useful in addressing this issue because they provide out-of-sample evidence. When patterns across many different countries replicate U.S. results, we are reassured that they are not artifacts of collective academic snooping through a particular data set (Lo and MacKinlay (1990a)). In addition to confirming the existence of a return premium, international data can also narrow the statistical uncertainty about its magnitude.

A second reason for studying this predictability is to examine whether the returns can be explained by risk factors. For example, Griffin, Ji, and Martin (2003) emphasize that macroeconomic risk does not explain international stock momentum. If abnormal returns are not correlated with risk factors, and if they are not correlated across countries, then they do not support risk-based explanations. Instead, similar return patterns that are uncorrelated across countries may need to be explained by behavioral theories.

*Heston, sheston@rhsmith.umd.edu, University of Maryland, Smith School of Business, 4447 Van Munching Hall, College Park, MD 20742; Sadka, sadka@bc.edu, Boston College, Carroll School of Management, 140 Commonwealth Ave., Chestnut Hill, MA 02467. We thank Stephen Brown (the editor), Andrea Frazzini, G. Andrew Karolyi (the referee), Tobias Moskowitz, and Christopher Polk.

1133

---

# Page 2

1134 Journal of Financial and Quantitative Analysis

The main contribution of this paper is to explore a new pattern of annual return continuation that describes the cross section of stock returns in Canada, Japan, and 12 European countries. This challenges previous findings that Japan is different because it displays no momentum within 12 months (Liu and Lee (2001), Chui, Titman, and Wei (2001)). Our pattern is different from the uniform long-term reversal of Griffin et al. (2003). Instead, we find that stocks display positive continuation at annual intervals of exactly 12 months while displaying negative reversal in between.

To measure the economic size of this cross-sectional predictability, we form decile portfolio spreads that buy the top 10% of stocks and sell the bottom 10% based on historical returns. We show that decile spreads based on historical returns at annual lags earn positive returns exceeding 30 basis points (bp) per month, while decile spreads based on nonannual lags (historical returns at lags that are not a multiple of 12 months) lose over 100 bp per month. The difference between these strategies is statistically significant and lasts for 5 years. One potential explanation for the common pattern across countries is that international stocks respond similarly to global return factors (Karolyi, Lee, and Van Dijk (2007)). This might be due to integrated capital markets that respond to international risk factors with seasonally time-varying prices of risk (Harvey (1991)). However, abnormal returns of our decile strategies remain after adjusting for the risk of global size, $\beta$ , and value factors. They also persist after adjusting for country-specific risk factors. Finally, the decile strategies are not highly correlated across countries. These results do not support a risk-based explanation.

The remainder of this paper is organized as follows. Section II uncovers a new pattern in international stock returns using the cross-sectional regression approach of Jegadeesh (1990). Section III demonstrates the profitability of this pattern using decile spreads. Section IV shows that this effect is similar across many countries and is not easily explained by global or local risk factors. Section V concludes.

## II. Predictability in International Stock Returns

We begin this study by exploring linear predictability at all lags in the cross section of international stock returns. This search allows us to find predictable return patterns that are common across countries. By including many different lags at a monthly frequency, this encompasses the 1-year “momentum” effect of Jegadeesh (1990) and Jegadeesh and Titman (1993), (2001) as well as the 3–5 year “reversal” effect of DeBondt and Thaler (1985), (1987). In particular this methodology has the power to separately detect intermixed combinations of continuation and reversal at adjacent lags.

Our international data set is from FactSet Research Systems (www.factset.com). FactSet is used extensively in the financial services industry, by the top 10 global investment banks, and by 95 of the top 100 asset managers. The data are free of survivorship bias and consist of monthly stock returns (including dividends) and market capitalizations on firms in 14 non-U.S. countries from January

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 3

Heston and Sadka 1135

1985 through June 2006. We measure returns in U.S. dollars but present results only for excess returns, which are robust to choice of numeraire. $^{1}$

Table 1 describes the distribution of firms across countries and shows that every country has at least 60 firms with more than 15 years of data. The countries include Canada, Japan, and 12 European countries comparable to those used by Rouwenhorst (1998), Chui, Titman, and Wei (2010), and Griffin et al. (2003).

---

**TABLE 1**

**Summary Statistics**

Table 1 reports some diagnostics of each country included in the sample: the number of unique firms, the number of firm-month observations, and the distribution of the number of months that firms exist in the sample. The sample includes stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom for the time period January 1985–June 2006 (258 months).

<table>
  <thead>
    <tr>
      <th>Country</th>
      <th>No. of Firms</th>
      <th>1 &lt; Months &lt; 60</th>
      <th>60 &lt; Months &lt; 120</th>
      <th>120 &lt; Months &lt; 180</th>
      <th>Months &gt; 180</th>
      <th>Firm-Month Obs.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Austria</td><td>192</td><td>36</td><td>55</td><td>40</td><td>61</td><td>25,291</td></tr>
    <tr><td>Belgium</td><td>229</td><td>37</td><td>73</td><td>29</td><td>90</td><td>33,362</td></tr>
    <tr><td>Canada</td><td>2,714</td><td>893</td><td>866</td><td>586</td><td>369</td><td>263,264</td></tr>
    <tr><td>Finland</td><td>292</td><td>49</td><td>107</td><td>80</td><td>56</td><td>35,340</td></tr>
    <tr><td>France</td><td>1,512</td><td>216</td><td>562</td><td>322</td><td>412</td><td>200,138</td></tr>
    <tr><td>Germany</td><td>1,471</td><td>115</td><td>548</td><td>232</td><td>576</td><td>219,082</td></tr>
    <tr><td>Italy</td><td>558</td><td>86</td><td>193</td><td>94</td><td>185</td><td>75,846</td></tr>
    <tr><td>Japan</td><td>4,452</td><td>755</td><td>773</td><td>788</td><td>2,136</td><td>710,858</td></tr>
    <tr><td>Netherlands</td><td>497</td><td>52</td><td>119</td><td>95</td><td>231</td><td>80,984</td></tr>
    <tr><td>Norway</td><td>493</td><td>153</td><td>187</td><td>78</td><td>75</td><td>48,046</td></tr>
    <tr><td>Spain</td><td>396</td><td>51</td><td>98</td><td>73</td><td>174</td><td>61,809</td></tr>
    <tr><td>Sweden</td><td>773</td><td>213</td><td>306</td><td>159</td><td>95</td><td>79,101</td></tr>
    <tr><td>Switzerland</td><td>600</td><td>56</td><td>184</td><td>121</td><td>239</td><td>92,296</td></tr>
    <tr><td>United Kingdom</td><td>3,938</td><td>912</td><td>1,087</td><td>759</td><td>1,180</td><td>515,264</td></tr>
    <tr><td>Total</td><td>18,117</td><td>3,624</td><td>5,158</td><td>3,456</td><td>5,879</td><td>2,440,681</td></tr>
  </tbody>
</table>

In this section we analyze monthly stock returns using the cross-sectional regression methodology of Jegadeesh (1990). The next section uses a different methodology of decile spreads to quantify the magnitudes and demonstrate that results are robust to methodology. For each month in our data set we run cross-sectional regressions of returns on 14 country dummy variables and lagged returns,

$$
(1) \quad r_{it} = \sum_{j=0}^{14} \alpha_j I_{ij} + \gamma_{tk} r_{i,t-k} + e_{it},
$$

where $r_{it}$ is the return on stock $i$ in month $t$ , and the country variable $I_{ij}$ is 1 if firm $i$ belongs to country $j$ , and 0 otherwise. The coefficients $\alpha_j$ represent pure country effects because they are returns to a unit investment in “momentum-neutral” country portfolios. But we are not focused on country effects. Instead, we are interested in the effect of past stock returns on future returns. The coefficients $\gamma_{tk}$ represent the response of returns at time $t$ to previous returns lagged by $k$ months. Therefore, we call them “return responses.”

---

$^{1}$ While we follow the literature in using simple monthly returns, they are a close approximation for continuously compounded returns, which are literally independent of the numeraire currency.

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 4

1136 Journal of Financial and Quantitative Analysis

Following Fama (1976), the return responses have the interpretation of (excess) returns on costless portfolios that had historical (excess) returns of 100%. Note that this regression uses all firms with returns available in month $t$ and month $t-k$ . Therefore, the estimated return responses represent a feasible portfolio strategy that does not suffer from hindsight bias. By including country dummy variables in the cross-sectional regression (1), we ensure that the returns responses are country-neutral in the sense of having 0 net investment in any country. However, stocks in some countries are more volatile and may disproportionately affect the results. For example, the average estimated standard error from the simple regression (1) in Belgium is only 10.6%, whereas it is 25.9% in Canada. Other countries are more similar, with estimated standard errors between 12% and 19%. To adjust for this heteroskedasticity, we estimate return responses with a weighted least squares regression (1), determining weights by the (reciprocal) of estimated variances in each country.

Table 2 presents the average impulse responses for different lags. The average lag 1 response estimated over all countries is negative, representing return reversal. This is consistent with bid-ask spreads and other microstructure effects discussed by Lehmann (1990) and Lo and MacKinlay (1990b). However, the responses at other reported lags are uniformly positive. This matches the U.S. results of Jegadeesh and Titman (1993) for lags of less than 1 year and matches the results of Jegadeesh (1990) for lags of 24 and 36 months. But it also indicates

---

TABLE 2

Cross-Sectional Regressions of Returns

In Table 2, monthly univariate cross-sectional regressions of the form $r_{i,t} = \alpha_{k,t} + \gamma_{k,t} r_{i,t-k} + u_{i,t}$ are calculated for each month $t$ and lag $k$ , and where $r_{i,t}$ is the return of stock $i$ in month $t$ . The lagged variable $r_{i,t-k}$ is the return of stock $i$ in month $t-k$ . The regression is calculated for every month $t$ from February 1985 through June 2006 (257 months), and for lag $k$ values 1–12, and each 12th lag thereafter through 60. Regression results (using country dummy variables for intercept) are reported separately for different samples: all countries, European countries only, Canada, and Japan. The time-series averages of $\gamma_{k,t}$ as well as $t$ -statistics are reported. Heteroskedasticity-adjusted regressions for all countries and European countries are computed by weighting each firm observation by the pooled cross-sectional and time-series variance of firm returns in its country. The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th rowspan="3">Lag</th>
      <th colspan="2">Simple Regressions</th>
      <th colspan="2">Heteroskedasticity-Adjusted Regressions</th>
    </tr>
    <tr>
      <th colspan="2">All</th>
      <th colspan="2">Europe</th>
      <th colspan="2">Canada</th>
      <th colspan="2">Japan</th>
      <th colspan="2">All</th>
      <th colspan="2">Europe</th>
    </tr>
    <tr>
      <th>Estimate</th>
      <th>t-Stat.</th>
      <th>Estimate</th>
      <th>t-Stat.</th>
      <th>Estimate</th>
      <th>t-Stat.</th>
      <th>Estimate</th>
      <th>t-Stat.</th>
      <th>Estimate</th>
      <th>t-Stat.</th>
      <th>Estimate</th>
      <th>t-Stat.</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>1</td><td>-0.0293</td><td>-6.22</td><td>-0.0200</td><td>-3.26</td><td>-0.0325</td><td>-4.09</td><td>-0.0513</td><td>-5.72</td><td>-0.0307</td><td>-5.91</td><td>-0.0210</td><td>-3.35</td></tr>
    <tr><td>2</td><td>0.0030</td><td>0.68</td><td>0.0018</td><td>0.23</td><td>-0.0005</td><td>-0.05</td><td>-0.0165</td><td>-1.84</td><td>0.0014</td><td>0.31</td><td>0.0024</td><td>0.30</td></tr>
    <tr><td>3</td><td>0.0110</td><td>2.03</td><td>0.0042</td><td>0.39</td><td>0.0132</td><td>1.31</td><td>0.0060</td><td>0.73</td><td>0.0094</td><td>1.65</td><td>0.0047</td><td>0.45</td></tr>
    <tr><td>4</td><td>0.0092</td><td>2.52</td><td>0.0078</td><td>0.85</td><td>0.0151</td><td>2.14</td><td>-0.0087</td><td>-1.17</td><td>0.0085</td><td>2.14</td><td>0.0082</td><td>0.90</td></tr>
    <tr><td>5</td><td>0.0095</td><td>2.52</td><td>0.0122</td><td>2.59</td><td>0.0018</td><td>0.21</td><td>0.0000</td><td>-0.01</td><td>0.0101</td><td>2.64</td><td>0.0125</td><td>2.60</td></tr>
    <tr><td>6</td><td>0.0103</td><td>2.74</td><td>0.0202</td><td>3.88</td><td>0.0019</td><td>0.23</td><td>-0.0134</td><td>-1.78</td><td>0.0098</td><td>2.50</td><td>0.0197</td><td>3.75</td></tr>
    <tr><td>7</td><td>0.0083</td><td>2.14</td><td>0.0123</td><td>1.53</td><td>0.0104</td><td>1.21</td><td>-0.0077</td><td>-1.30</td><td>0.0084</td><td>1.84</td><td>0.0133</td><td>1.59</td></tr>
    <tr><td>8</td><td>0.0068</td><td>2.24</td><td>-0.0007</td><td>-0.08</td><td>0.0162</td><td>2.02</td><td>-0.0061</td><td>-0.99</td><td>0.0051</td><td>1.60</td><td>-0.0006</td><td>-0.06</td></tr>
    <tr><td>9</td><td>0.0113</td><td>3.31</td><td>0.0112</td><td>1.13</td><td>0.0137</td><td>1.67</td><td>0.0031</td><td>0.49</td><td>0.0104</td><td>3.08</td><td>0.0118</td><td>1.19</td></tr>
    <tr><td>10</td><td>0.0057</td><td>1.59</td><td>0.0100</td><td>0.96</td><td>0.0095</td><td>1.05</td><td>-0.0063</td><td>-0.92</td><td>0.0047</td><td>1.21</td><td>0.0101</td><td>0.97</td></tr>
    <tr><td>11</td><td>0.0087</td><td>2.63</td><td>0.0014</td><td>0.16</td><td>0.0113</td><td>1.46</td><td>-0.0031</td><td>-0.56</td><td>0.0075</td><td>2.27</td><td>0.0016</td><td>0.19</td></tr>
    <tr><td>12</td><td>0.0151</td><td>4.25</td><td>0.0102</td><td>1.49</td><td>0.0160</td><td>2.19</td><td>0.0131</td><td>2.05</td><td>0.0158</td><td>4.48</td><td>0.0102</td><td>1.50</td></tr>
    <tr><td>24</td><td>0.0064</td><td>2.57</td><td>0.0185</td><td>2.33</td><td>0.0035</td><td>0.44</td><td>0.0046</td><td>0.83</td><td>0.0084</td><td>3.13</td><td>0.0188</td><td>2.36</td></tr>
    <tr><td>36</td><td>0.0080</td><td>2.43</td><td>0.0100</td><td>0.84</td><td>-0.0052</td><td>-0.50</td><td>0.0079</td><td>1.72</td><td>0.0080</td><td>2.42</td><td>0.0098</td><td>0.83</td></tr>
    <tr><td>48</td><td>0.0071</td><td>2.62</td><td>0.0110</td><td>1.03</td><td>0.0069</td><td>0.64</td><td>0.0078</td><td>1.44</td><td>0.0070</td><td>2.36</td><td>0.0103</td><td>0.96</td></tr>
    <tr><td>60</td><td>0.0091</td><td>3.27</td><td>0.0063</td><td>1.55</td><td>0.0186</td><td>1.97</td><td>0.0048</td><td>0.89</td><td>0.0083</td><td>2.94</td><td>0.0055</td><td>1.29</td></tr>
  </tbody>
</table>

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 5

Heston and Sadka 1137

positive return continuation at lags of 48 and 60 months. This has not been previously documented in the international literature.

These results hold up across different continents. When estimated using the subsample of 12 European countries, the impulse responses beyond 1 month are positive for all annual lags. Due to the large standard errors associated with smaller sample size, these lags are not individually significant for all maturities. This matches the results of Rouwenhorst (1998) for lags of less than 1 year and extends those results to much longer maturities. Canada shows a similar pattern, with all but one of the estimates positive beyond the 2-month lag. This is not surprising, given published results about the U.S. Japan also shows significant positive responses at the 12-month lag and beyond. While this largely matches the pattern in the North America and Europe, it challenges the conclusion of Liu and Lee (2001) and Chui et al. (2001) that Japan has no momentum within 12 months. $^{2}$ This finding is important because it shows that the developed markets of North America, Europe, and Japan share similar cross-sectional and temporal patterns of returns.

The weighted least squares regression results in the right-hand columns of Table 2 are quite similar to the ordinary least squares results. Adjusting for country heteroskedasticity does very little to change the point estimates across all countries or just the European subsample. This is important because it shows that the results are not driven by a few countries with high variance stocks. It is compatible with a common pattern across countries. $^{3}$

III. Portfolio Strategies

The previous section finds an intriguing new pattern in international stock returns. This section forms portfolio strategies to exploit the pattern and measure its economic importance. By using portfolios we can focus the strategies to measure specific kinds of predictability (e.g., annual vs. nonannual). Then we can interpret results in a simple way as excess returns. Finally, we can segregate firms by risk or characteristics to see whether the effects are limited to particular kinds of firms.

Given our short sample, we do not expect the time series of return responses to be significant for all individual lags. Indeed, forming a portfolio based on a single monthly lag is a very weak strategy. Moreover, cross-sectional regressions do not indicate the magnitude of returns available. Therefore, we adopt the decile spread methodology of Jegadeesh and Titman (1993). Each month we sort stocks into deciles based on their historical returns in excess of equal-weighted local country indices. $^{4}$ These sorts may be formed based on average returns over a contiguous multiperiod historical interval such as lags 1–12, or they may use averages over noncontiguous annual lags such as lags 24 and 36, or lags 48 and 60.

$^{2}$ While momentum is a cross-sectional effect, there are other studies related to Asian market seasonality. Ziemba (1991) and Comolli and Ziemba (2000) document a January effect in Japan, but Koh and Wong (2000) find a January effect in only 2 of 7 Asian markets studied. Hamori (2001) also fails to find non-January seasonality in the average market return on large Japanese stocks.

$^{3}$ Following Jegadeesh (1990), we obtain similar results by estimating return responses jointly with a multiple regression instead of the simple regression (1).

$^{4}$ We obtain similar results using value-weighted indices.

---

# Page 6

1138 Journal of Financial and Quantitative Analysis

After sorting the stocks, we calculate the difference between the returns on the top and bottom deciles. We rebalance these portfolios monthly and calculate average excess returns on these decile portfolio sorts for a holding period of 1 month.

The key distinction is that Jegadeesh and Titman (1993) use contiguous multiperiod formation intervals with subsequent holding periods of 1 month, whereas we sometimes use noncontiguous formation intervals with holding periods of 1 month. This creates high turnover in our strategies based on annual lags, because the top decile of stock returns in 1 calendar month does not correspond to the top decile of returns in the next.

Table 3 presents the average returns on decile portfolios sorted according to their returns over various historical lags. The annual strategies buy stocks based on historical monthly returns that are a multiple of 12. For example, the Year 1 annual strategies represent decile portfolios sorted on a single lag 12-month return. The nonannual strategies buy stocks based on historical returns at lags that are not a multiple of 12. For example, the Year 1 nonannual strategies choose stocks based on the most recent 11 months of returns. Both of these Year 1 strategies show the conventional momentum effect, where stocks with high returns continue to outperform stocks with low returns for up to 1 year. When sorting stocks based on all 12 of the past Year 1 returns in excess of country returns, the highest decile outperforms the lowest decile by 131 bp per month. This is comparable to Jegadeesh and Titman’s (1993) momentum results with U.S. stocks. It is also consistent with Rouwenhorst (1998), who finds that a decile spread strategy based on 6 months of past returns earns an excess return of 128 bp per month in European countries, and Griffin et al. (2003), who find profits on different continents ranging from 32 bp to 163 bp per month.

Table 3 also indicates significant returns at longer lags. The Years 2–3 nonannual decile spread strategy loses 143 bp per month. This is broadly consistent with Griffin et al. (2003), who find momentum strategies over a similar period lose 36 bp–122 bp, depending on the continent. In contrast, the Years 2–3 annual decile spread, which chooses stocks based on historical returns at lags 24 and 36, earns a positive 37 bp per month. These positive annual and negative nonannual results are both statistically significant at high levels, albeit in opposite directions.

The results are qualitatively similar, but slightly weaker, for strategies based on 4- to 5-year lags. The Years 4–5 nonannual decile spread loses 56 bp per month, while the Years 4–5 annual decile spread earns 44 bp per month. As with shorter lags, these Years 4–5 results are statistically significant in opposite directions. It is striking that decile spreads based on nonannual lags (longer than 1 year) give negative reversal results, while return strategies based on the intermediate annual lags exhibit positive continuation. The difference between these decile spreads is economically large, over 1% per month.

The lower panels of Table 3 report profitability of value-weighted decile spread strategies instead of equal-weighted strategies. The holding period returns on both equal- and value-weighted decile spreads compare the top 10% of stocks to the bottom 10% of stocks, not to an equal- or value-weighted index. The distinction is that value-weighted deciles put more weight on the performance of large stocks in the top 10% compared to large stocks in the bottom 10%. The value-weighted strategies based on total return provide weaker evidence of annual

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 7

Heston and Sadka 1139

continuation than the equal-weighted strategies. The Years 2–3 annual value-weighted strategies outperform the corresponding nonannual strategies by 27 bp, but this difference is not statistically significant. The Years 4–5 value-weighted annual strategy earns 50 bp per month, which is actually higher than the Years 4–5 equal-weighted annual strategy. Despite the higher profitability, the Years 4–5 value-weighted annual strategy is not significantly profitable at the 95% level due to higher variability. The value-weighted strategies are riskier because they are concentrated in a few large firms. Nevertheless, the Years 4–5 value-weighted strategies significantly outperform the corresponding nonannual strategies.

---

TABLE 3

Inter- and Intracountry Relative Strength Returns of Decile Spreads

Each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on past performance. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns during the historical lags 48 and 60. For each strategy, Table 3 reports the portfolio return spread of the top-minus-bottom decile. The difference strategy is the annual strategy minus the nonannual strategy. A stock’s past return performance is measured either in excess of its country’s equal-weighted average (Panel A) or as its total (simple) return (Panel B). The monthly holding return of every stock is then decomposed into intra- and intercountry components. The intracountry component is the monthly return of the stock excess of its country’s equal-weighted average return, and the intercountry component is the average monthly return of the country itself. The average monthly returns (equal- and value-weighted) of the various trading strategies (for both intra- and interindustry components) for the period February 1985–June 2006 (257 months) are reported, as well as the corresponding t-statistics (2-decimal-place numbers). The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

Equal-Weighted Portfolio Returns

<table>
  <thead>
    <tr>
      <th rowspan="2">Strategy</th>
      <th colspan="3">Panel A. Sorting by Historical Return Excess of Country</th>
      <th colspan="3">Panel B. Sorting by Historical Total Return</th>
    </tr>
    <tr>
      <th>Total Return</th>
      <th>Intra-country Return</th>
      <th>Inter-country Return</th>
      <th>Total Return</th>
      <th>Intra-country Return</th>
      <th>Inter-country Return</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Year 1</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0121<br>4.17</td>
      <td>0.0117<br>4.03</td>
      <td>0.0004<br>1.06</td>
      <td>0.0136<br>3.75</td>
      <td>0.0107<br>3.90</td>
      <td>0.0029<br>1.68</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0081<br>4.28</td>
      <td>0.0085<br>4.49</td>
      <td>−0.0004<br>−1.33</td>
      <td>0.0076<br>2.60</td>
      <td>0.0078<br>4.28</td>
      <td>−0.0002<br>−0.12</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>−0.0040<br>−1.32</td>
      <td>−0.0032<br>−1.06</td>
      <td>−0.0008<br>−2.18</td>
      <td>−0.0060<br>−1.53</td>
      <td>−0.0029<br>−1.00</td>
      <td>−0.0031<br>−1.53</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0131<br>4.53</td>
      <td>0.0127<br>4.39</td>
      <td>0.0004<br>0.96</td>
      <td>0.0149<br>4.07</td>
      <td>0.0119<br>4.37</td>
      <td>0.0029<br>1.65</td>
    </tr>
    <tr>
      <td>Years 2–3</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>−0.0143<br>−7.05</td>
      <td>−0.0138<br>−6.79</td>
      <td>−0.0005<br>−1.73</td>
      <td>−0.0156<br>−5.90</td>
      <td>−0.0130<br>−6.80</td>
      <td>−0.0026<br>−1.71</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0037<br>2.72</td>
      <td>0.0037<br>2.87</td>
      <td>−0.0001<br>−0.24</td>
      <td>0.0042<br>1.76</td>
      <td>0.0037<br>2.82</td>
      <td>0.0005<br>0.29</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0180<br>8.25</td>
      <td>0.0175<br>8.00</td>
      <td>0.0005<br>1.27</td>
      <td>0.0198<br>6.06</td>
      <td>0.0167<br>7.96</td>
      <td>0.0031<br>1.44</td>
    </tr>
    <tr>
      <td>All</td>
      <td>−0.0127<br>−6.42</td>
      <td>−0.0123<br>−6.18</td>
      <td>−0.0004<br>−1.36</td>
      <td>−0.0143<br>−5.55</td>
      <td>−0.0120<br>−6.41</td>
      <td>−0.0024<br>−1.55</td>
    </tr>
    <tr>
      <td>Years 4–5</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>−0.0056<br>−3.95</td>
      <td>−0.0052<br>−3.69</td>
      <td>−0.0005<br>−1.21</td>
      <td>−0.0043<br>−1.96</td>
      <td>−0.0047<br>−3.60</td>
      <td>0.0004<br>0.24</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0044<br>3.51</td>
      <td>0.0048<br>3.96</td>
      <td>−0.0004<br>−1.27</td>
      <td>0.0045<br>1.86</td>
      <td>0.0042<br>3.54</td>
      <td>0.0003<br>0.17</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0101<br>5.54</td>
      <td>0.0100<br>5.52</td>
      <td>0.0001<br>0.22</td>
      <td>0.0088<br>2.87</td>
      <td>0.0089<br>5.13</td>
      <td>−0.0001<br>−0.03</td>
    </tr>
    <tr>
      <td>All</td>
      <td>−0.0042<br>−2.88</td>
      <td>−0.0040<br>−2.76</td>
      <td>−0.0002<br>−0.55</td>
      <td>−0.0032<br>−1.46</td>
      <td>−0.0037<br>−2.74</td>
      <td>0.0005<br>0.31</td>
    </tr>
  </tbody>
</table>

(continued on next page)

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 8

1140 Journal of Financial and Quantitative Analysis

TABLE 3 (continued)

Inter- and Intracountry Relative Strength Returns of Decile Spreads

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th>Value-Weighted Portfolio Returns</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>Panel A. Sorting by Historical Return Excess of Country</td>
      <td></td>
      <td></td>
      <td>Panel B. Sorting by Historical Total Return</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Total Return</td>
      <td>Intra-country Return</td>
      <td>Inter-country Return</td>
      <td>Total Return</td>
      <td>Intra-country Return</td>
      <td>Inter-country Return</td>
    </tr>
    <tr>
      <td>Year 1</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0077</td>
      <td>0.0082</td>
      <td>-0.0005</td>
      <td>0.0032</td>
      <td>0.0022</td>
      <td>0.0010</td>
    </tr>
    <tr>
      <td></td>
      <td>1.35</td>
      <td>1.41</td>
      <td>-0.33</td>
      <td>0.51</td>
      <td>0.42</td>
      <td>0.38</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0123</td>
      <td>0.0130</td>
      <td>-0.0007</td>
      <td>0.0100</td>
      <td>0.0100</td>
      <td>0.0000</td>
    </tr>
    <tr>
      <td></td>
      <td>3.40</td>
      <td>3.88</td>
      <td>-0.57</td>
      <td>2.42</td>
      <td>3.14</td>
      <td>0.02</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0045</td>
      <td>0.0047</td>
      <td>-0.0002</td>
      <td>0.0068</td>
      <td>0.0078</td>
      <td>-0.0010</td>
    </tr>
    <tr>
      <td></td>
      <td>0.73</td>
      <td>0.75</td>
      <td>-0.09</td>
      <td>1.02</td>
      <td>1.37</td>
      <td>-0.30</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0093</td>
      <td>0.0101</td>
      <td>-0.0008</td>
      <td>0.0072</td>
      <td>0.0072</td>
      <td>0.0000</td>
    </tr>
    <tr>
      <td></td>
      <td>1.68</td>
      <td>1.81</td>
      <td>-0.54</td>
      <td>1.16</td>
      <td>1.37</td>
      <td>0.01</td>
    </tr>
    <tr>
      <td>Years 2–3</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>-0.0033</td>
      <td>-0.0057</td>
      <td>0.0024</td>
      <td>-0.0095</td>
      <td>-0.0097</td>
      <td>0.0002</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.96</td>
      <td>-1.70</td>
      <td>1.71</td>
      <td>-2.43</td>
      <td>-3.01</td>
      <td>0.08</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>-0.0008</td>
      <td>0.0011</td>
      <td>-0.0020</td>
      <td>0.0017</td>
      <td>0.0023</td>
      <td>-0.0006</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.27</td>
      <td>0.39</td>
      <td>-1.71</td>
      <td>0.44</td>
      <td>0.72</td>
      <td>-0.25</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0027</td>
      <td>0.0073</td>
      <td>-0.0045</td>
      <td>0.0113</td>
      <td>0.0122</td>
      <td>-0.0009</td>
    </tr>
    <tr>
      <td></td>
      <td>0.60</td>
      <td>1.66</td>
      <td>-2.35</td>
      <td>2.22</td>
      <td>2.88</td>
      <td>-0.28</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0031</td>
      <td>-0.0044</td>
      <td>0.0013</td>
      <td>-0.0076</td>
      <td>-0.0073</td>
      <td>-0.0003</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.93</td>
      <td>-1.34</td>
      <td>0.90</td>
      <td>-1.89</td>
      <td>-2.29</td>
      <td>-0.15</td>
    </tr>
    <tr>
      <td>Years 4–5</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>-0.0044</td>
      <td>-0.0045</td>
      <td>0.0001</td>
      <td>-0.0024</td>
      <td>-0.0030</td>
      <td>0.0006</td>
    </tr>
    <tr>
      <td></td>
      <td>-1.63</td>
      <td>-1.69</td>
      <td>0.05</td>
      <td>-0.70</td>
      <td>-1.06</td>
      <td>0.28</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0050</td>
      <td>0.0073</td>
      <td>-0.0023</td>
      <td>0.0048</td>
      <td>0.0062</td>
      <td>-0.0014</td>
    </tr>
    <tr>
      <td></td>
      <td>1.84</td>
      <td>2.96</td>
      <td>-1.71</td>
      <td>1.50</td>
      <td>2.81</td>
      <td>-0.57</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0092</td>
      <td>0.0115</td>
      <td>-0.0023</td>
      <td>0.0070</td>
      <td>0.0090</td>
      <td>-0.0020</td>
    </tr>
    <tr>
      <td></td>
      <td>2.55</td>
      <td>3.27</td>
      <td>-1.25</td>
      <td>1.52</td>
      <td>2.62</td>
      <td>-0.62</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0046</td>
      <td>-0.0053</td>
      <td>0.0007</td>
      <td>-0.0017</td>
      <td>-0.0019</td>
      <td>0.0002</td>
    </tr>
    <tr>
      <td></td>
      <td>-1.72</td>
      <td>-1.99</td>
      <td>0.49</td>
      <td>-0.47</td>
      <td>-0.67</td>
      <td>0.10</td>
    </tr>
  </tbody>
</table>


The decile spreads based on total returns are not necessarily country-neutral. It is possible that the largest winners come from 1 country, while the largest losers come from another. For example, if Canada has a disproportionate number of stocks with a comparatively large return in a particular month, then Canadian stocks will be overrepresented among the winner decile for that month. For this reason portfolio strategies based on total return do not completely distinguish intracountry effects from return effects across countries. Heston and Rouwenhorst (1994) and Griffin and Karolyi (1998) show the influence of strong country-specific risks on stock returns. Variations in volatility across countries can reduce the international diversification of our return strategies. One possible explanation of our results is a distinct country effect that masks the average returns of stocks within countries.$^{5}$

To reduce the influence of country risks, Table 3 compares strategies that sort stocks on total return with strategies that sort based on return in excess of local

$^{5}$For example, Asness, Liew, and Stevens (1995) and Richards (1996) provide evidence of persistence in country returns.

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 9

Heston and Sadka 1141

equal-weighted indices. The first column reports decile spreads based on excess return over local equal-weighted country indices. The next 2 columns decompose the decile spreads into the intracountry component—returns in excess of local indices—and the remaining intercountry component. In all cases, the intracountry component accounts for the results. The intercountry component is always small and statistically insignificant. The equal-weighted intracountry excess returns on annual strategies are significantly positive, while the corresponding nonannual returns are significantly negative for the equal-weighted Years 2–3 and Years 4–5 strategies. The value-weighted returns are similar to the equal-weighted returns in sign and magnitude but are not always statistically significant. Panel B reports corresponding results with strategies that sort stocks on historical total returns instead of returns in excess of country. The results are very similar to those in Panel A, often with slightly reduced $t$ -statistics. In sum, sorting on historical intracountry returns and measuring intracountry holding returns is the best way to capture the seasonal return premium. The entire pattern is due to the intracountry component of stock returns, not to country effects.

In statistical terms, the empirical results indicate that, on average, across firms, excess returns tend to be followed at annual intervals by excess returns of the same sign:

(2)

$$
\mathrm{E}\left[\left(r_{i,t}-\bar{r}_{t}\right)\left(r_{i,t+k}-\bar{r}_{t+k}\right)\right] > 0,
$$

where $k$ is a multiple of 12 and where we denote the equal-weighted index return at time $t$ by $\bar{r}_{t}$ . This involves both the mean excess returns and the autocovariance of excess returns:

(3)

$$
\begin{aligned}
\mathrm{E}\left[\left(r_{i,t}-\bar{r}_{t}\right)\left(r_{i,t+k}-\bar{r}_{t+k}\right)\right] = & \mathrm{E}\left[r_{i,t}-\bar{r}_{t}\right] \mathrm{E}\left[r_{i,t+k}-\bar{r}_{t+k}\right] \\
& + \operatorname{Cov}\left[r_{i,t}-\bar{r}_{t}, r_{i,t+k}-\bar{r}_{t+k}\right].
\end{aligned}
$$

According to a seasonal version of the explanation of Conrad and Kaul (1998), the periodic annual pattern can be caused by the first term on the right-hand side of equation (3) if stocks have particularly high or low returns in specific calendar months. Indeed, the annual pattern in cross-sectional returns resembles calendar anomalies such as the well-known January effect documented by Rozeff and Kinney (1976) or the small-firm January effects of Keim (1983) and Reinganum (1983).

To investigate calendar explanations, Table 4 reports results by calendar month. Since any given calendar month has only 1/12th of the observations of the whole data set, we do not expect statistical significance in every calendar month. But all the annual strategies produce positive returns in almost every calendar month, while the Years 2–3 and Years 4–5 nonannual strategies produce negative returns in most calendar months.

The results are quite large in January. For example, the Years 2–3 annual decile spread earns 78 bp per month, while the corresponding nonannual strategy loses 370 bp in January, which is statistically significant at the 95% level. Similarly the Years 4–5 annual decile spread earns a statistically significant 173 bp per month in January, and the corresponding nonannual strategy loses a significant

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 10

1142 Journal of Financial and Quantitative Analysis

---

TABLE 4

Relative Strength Strategies across Calendar Months

In Table 4, each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The difference strategy is the annual strategy minus the nonannual strategy. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. The average monthly returns of the various trading strategies are reported separately for every calendar month during the period February 1985–June 2006 (257 months). The corresponding $t$-statistics are also reported (2-decimal-place numbers). In a separate column, returns are computed using all non-January months. The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th>Jan.</th>
      <th>Feb.</th>
      <th>Mar.</th>
      <th>Apr.</th>
      <th>May</th>
      <th>June</th>
      <th>July</th>
      <th>Aug.</th>
      <th>Sept.</th>
      <th>Oct.</th>
      <th>Nov.</th>
      <th>Dec.</th>
      <th>Feb.–Dec.</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Panel A. Year 1</td>
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
      <td>Nonannual</td>
      <td>−0.0101<br>−0.89</td>
      <td>0.0222<br>1.73</td>
      <td>0.0102<br>1.02</td>
      <td>0.0058<br>0.56</td>
      <td>0.0041<br>0.44</td>
      <td>0.0246<br>2.73</td>
      <td>0.0256<br>4.09</td>
      <td>0.0207<br>3.25</td>
      <td>0.0157<br>2.20</td>
      <td>−0.0005<br>−0.04</td>
      <td>0.0063<br>0.45</td>
      <td>0.0208<br>2.92</td>
      <td>0.0142<br>4.78</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0077<br>1.47</td>
      <td>−0.0028<br>−0.30</td>
      <td>0.0099<br>1.99</td>
      <td>0.0065<br>1.74</td>
      <td>0.0043<br>0.78</td>
      <td>0.0180<br>3.46</td>
      <td>0.0054<br>0.83</td>
      <td>0.0002<br>0.04</td>
      <td>0.0138<br>2.39</td>
      <td>0.0034<br>0.52</td>
      <td>0.0016<br>0.15</td>
      <td>0.0282<br>4.08</td>
      <td>0.0081<br>4.04</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0178<br>1.44</td>
      <td>−0.0250<br>−1.52</td>
      <td>−0.0003<br>−0.03</td>
      <td>0.0007<br>0.07</td>
      <td>0.0002<br>0.03</td>
      <td>−0.0066<br>−0.92</td>
      <td>−0.0202<br>−2.94</td>
      <td>−0.0206<br>−2.52</td>
      <td>−0.0019<br>−0.29</td>
      <td>0.0039<br>0.32</td>
      <td>−0.0048<br>−0.31</td>
      <td>0.0074<br>0.93</td>
      <td>−0.0060<br>−1.94</td>
    </tr>
    <tr>
      <td>All</td>
      <td>−0.0054<br>−0.52</td>
      <td>0.0197<br>1.56</td>
      <td>0.0094<br>0.92</td>
      <td>0.0063<br>0.62</td>
      <td>0.0033<br>0.33</td>
      <td>0.0263<br>2.87</td>
      <td>0.0253<br>3.44</td>
      <td>0.0187<br>3.17</td>
      <td>0.0197<br>2.65</td>
      <td>0.0015<br>0.13</td>
      <td>0.0068<br>0.48</td>
      <td>0.0259<br>3.65</td>
      <td>0.0148<br>4.95</td>
    </tr>
  </tbody>
</table>

(continued on next page)

Published online by Cambridge University Press https://doi.org/10.1017/S002210000515400001060122005/710101/0101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101

---

# Page 11

TABLE 4 (continued)

Relative Strength Strategies across Calendar Months

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Strategy</th>
      <th>Jan.</th>
      <th>Feb.</th>
      <th>Mar.</th>
      <th>Apr.</th>
      <th>May</th>
      <th>June</th>
      <th>July</th>
      <th>Aug.</th>
      <th>Sept.</th>
      <th>Oct.</th>
      <th>Nov.</th>
      <th>Dec.</th>
      <th>Feb–Dec.</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Panel B. Years 2–3</td>
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
      <td>Nonannual</td>
      <td>-0.0370</td>
      <td>-0.0192</td>
      <td>-0.0123</td>
      <td>-0.0150</td>
      <td>-0.0218</td>
      <td>-0.0165</td>
      <td>-0.0178</td>
      <td>-0.0112</td>
      <td>-0.0107</td>
      <td>-0.0007</td>
      <td>-0.0092</td>
      <td>0.0007</td>
      <td>-0.0122</td>
    </tr>
    <tr>
      <td></td>
      <td>-3.91</td>
      <td>-2.27</td>
      <td>-1.93</td>
      <td>-2.62</td>
      <td>-3.13</td>
      <td>-2.55</td>
      <td>-2.95</td>
      <td>-1.89</td>
      <td>-1.56</td>
      <td>-0.07</td>
      <td>-2.20</td>
      <td>0.22</td>
      <td>-6.15</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0078</td>
      <td>-0.0070</td>
      <td>0.0079</td>
      <td>0.0022</td>
      <td>0.0035</td>
      <td>0.0055</td>
      <td>0.0029</td>
      <td>-0.0024</td>
      <td>0.0023</td>
      <td>0.0029</td>
      <td>0.0099</td>
      <td>0.0082</td>
      <td>0.0033</td>
    </tr>
    <tr>
      <td></td>
      <td>1.28</td>
      <td>-1.45</td>
      <td>2.13</td>
      <td>0.75</td>
      <td>0.76</td>
      <td>1.39</td>
      <td>0.58</td>
      <td>-1.04</td>
      <td>0.67</td>
      <td>0.54</td>
      <td>1.95</td>
      <td>1.27</td>
      <td>2.41</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0448</td>
      <td>0.0122</td>
      <td>0.0202</td>
      <td>0.0172</td>
      <td>0.0253</td>
      <td>0.0221</td>
      <td>0.0207</td>
      <td>0.0089</td>
      <td>0.0131</td>
      <td>0.0035</td>
      <td>0.0191</td>
      <td>0.0075</td>
      <td>0.0155</td>
    </tr>
    <tr>
      <td></td>
      <td>5.25</td>
      <td>1.16</td>
      <td>3.07</td>
      <td>2.32</td>
      <td>3.95</td>
      <td>3.84</td>
      <td>3.82</td>
      <td>1.40</td>
      <td>1.61</td>
      <td>0.41</td>
      <td>3.08</td>
      <td>1.14</td>
      <td>7.12</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0326</td>
      <td>-0.0189</td>
      <td>-0.0104</td>
      <td>-0.0137</td>
      <td>-0.0200</td>
      <td>-0.0154</td>
      <td>-0.0172</td>
      <td>-0.0082</td>
      <td>-0.0092</td>
      <td>0.0009</td>
      <td>-0.0071</td>
      <td>0.0005</td>
      <td>-0.0109</td>
    </tr>
    <tr>
      <td></td>
      <td>-3.50</td>
      <td>-2.36</td>
      <td>-1.66</td>
      <td>-2.59</td>
      <td>-2.83</td>
      <td>-2.35</td>
      <td>-2.92</td>
      <td>-1.46</td>
      <td>-1.44</td>
      <td>0.10</td>
      <td>-1.61</td>
      <td>0.14</td>
      <td>-5.58</td>
    </tr>
    <tr>
      <td>Panel C. Years 4–5</td>
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
      <td>Nonannual</td>
      <td>-0.0197</td>
      <td>-0.0133</td>
      <td>-0.0017</td>
      <td>-0.0007</td>
      <td>-0.0009</td>
      <td>-0.0063</td>
      <td>-0.0025</td>
      <td>-0.0115</td>
      <td>-0.0069</td>
      <td>0.0034</td>
      <td>-0.0008</td>
      <td>-0.0062</td>
      <td>-0.0043</td>
    </tr>
    <tr>
      <td></td>
      <td>-3.19</td>
      <td>-2.40</td>
      <td>-0.63</td>
      <td>-0.15</td>
      <td>-0.15</td>
      <td>-1.75</td>
      <td>-0.79</td>
      <td>-2.32</td>
      <td>-1.36</td>
      <td>0.78</td>
      <td>-0.15</td>
      <td>-1.14</td>
      <td>-3.05</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0173</td>
      <td>0.0046</td>
      <td>0.0013</td>
      <td>-0.0027</td>
      <td>0.0022</td>
      <td>0.0086</td>
      <td>0.0028</td>
      <td>-0.0003</td>
      <td>0.0033</td>
      <td>0.0000</td>
      <td>0.0039</td>
      <td>0.0113</td>
      <td>0.0032</td>
    </tr>
    <tr>
      <td></td>
      <td>2.35</td>
      <td>1.23</td>
      <td>0.26</td>
      <td>-0.83</td>
      <td>0.46</td>
      <td>2.61</td>
      <td>0.72</td>
      <td>-0.07</td>
      <td>1.21</td>
      <td>0.01</td>
      <td>0.80</td>
      <td>3.61</td>
      <td>2.75</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0370</td>
      <td>0.0179</td>
      <td>0.0030</td>
      <td>-0.0020</td>
      <td>0.0031</td>
      <td>0.0149</td>
      <td>0.0053</td>
      <td>0.0112</td>
      <td>0.0103</td>
      <td>-0.0034</td>
      <td>0.0047</td>
      <td>0.0175</td>
      <td>0.0075</td>
    </tr>
    <tr>
      <td></td>
      <td>4.53</td>
      <td>2.91</td>
      <td>0.59</td>
      <td>-0.48</td>
      <td>0.46</td>
      <td>3.61</td>
      <td>1.08</td>
      <td>2.10</td>
      <td>1.75</td>
      <td>-0.60</td>
      <td>0.69</td>
      <td>2.69</td>
      <td>4.36</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0169</td>
      <td>-0.0132</td>
      <td>-0.0011</td>
      <td>-0.0008</td>
      <td>-0.0005</td>
      <td>-0.0050</td>
      <td>-0.0017</td>
      <td>-0.0097</td>
      <td>-0.0041</td>
      <td>0.0064</td>
      <td>0.0010</td>
      <td>-0.0040</td>
      <td>-0.0030</td>
    </tr>
    <tr>
      <td></td>
      <td>-2.67</td>
      <td>-2.35</td>
      <td>-0.39</td>
      <td>-0.16</td>
      <td>-0.08</td>
      <td>-1.34</td>
      <td>-0.65</td>
      <td>-1.90</td>
      <td>-0.86</td>
      <td>1.39</td>
      <td>0.17</td>
      <td>-0.77</td>
      <td>-2.06</td>
    </tr>
  </tbody>
</table>

Heston and Sacka 1143

Published online by Cambridge University Press https://doi.org/10.1017/S002210005451

---

# Page 12

1144 Journal of Financial and Quantitative Analysis

197 bp in this same calendar month. But other months have large returns too: The Years 2–3 annual decile spread earns its highest returns in March, November, and December. An essential point is that while annual strategies outperform the nonannual strategies in January, this month is not responsible for results across the entire data set. In addition, these strategies are all statistically significant in the combined February–December holding periods. This annual pattern is not limited to any single month.

In the context of our annual and nonannual strategies, the resemblance of January to other calendar months contrasts with previous studies of anomalies. For example, Jegadeesh and Titman (1993) use U.S. data to show that their short-term momentum strategies do not work in January. Griffin et al. (2003) confirm the U.S. results and also show that these strategies may have unusual returns when tested in January with international data. Heston and Sadka (2008) show that annual continuation strategies in the U.S. have abnormally strong returns in January. In either case, the absence of a return effect or the magnification of this effect in January threatens to confound the basic pattern with a turn-of-year effect. Our evidence shows that January does not seem peculiar for the performance of annual and nonannual strategies with international stock returns.

Unreported statistical diagnostics do not reject the hypothesis that our strategies earn equal expected returns across all 12 calendar months. Nevertheless, the comparison of our strategies across calendar months is potentially useful for addressing theoretical explanations of the annual effect. For example, Carhart, Kaniel, Musto, and Reed (2002) provide evidence of “window dressing” by mutual funds. According to this theory, mutual funds increase their holdings near the end of fiscal year-end or quarter-end, effectively using price pressure to influence stock prices and manipulate their returns. To the extent that mutual funds hold certain subsets of stocks, this is consistent with an annual cross-sectional effect. However, examination of Table 4 shows that our effect is not especially limited to calendar months at year-end or quarter-end. The effect is somewhat strong in December. The Years 2–3 annual strategy earns 82 bp in December, while the Years 4–5 annual strategy earns 113 bp in that month. Yet it is strong in other calendar months too. The Years 2–3 annual strategy earns 99 bp in November, and the Years 4–5 annual strategy earns 173 bp in January. These months are not the end of the fiscal year for most mutual funds. There are economically and statistically significant returns to the annual strategies in a variety of months. In particular these returns are not confined to specific months at the turn-of-year or turn-of-quarter.

Other potential explanations link the annual pattern in the cross section to seasonality in market returns. For example, Kamstra, Kramer, and Levi (2003) provide international evidence of seasonality in global equities premiums. While their analysis focuses on seasonal affective disorder (SAD), their methodology is compatible with any smoothly varying seasonal pattern. In contrast, the annual cross-sectional effect documented in this paper is abruptly discontinuous. The annual strategies earn positive decile spreads, but the returns are often negative in adjacent months. This is inconsistent with SAD or any smooth seasonal variable.

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 13

Heston and Sadka 1145

IV. Comparisons across Size, Liquidity, Countries, and Risk

The previous section establishes an annual return pattern in the cross section of international stock returns. This pattern is not a country effect because it occurs within countries. And it occurs throughout the calendar year. There are different potential explanations. First, it may be a liquidity effect. If market activity is seasonal, then thin trading or bid-ask spreads may create an artificial appearance of autocorrelation. Alternatively, the effect may be real, but limited to a few large countries that dominate the data set. Finally, the returns may be associated with annual exposure to systematic international risk factors.

A. Comparisons across Size and Liquidity

If the return patterns are related to liquidity then they may not be exploitable. Particularly in countries with less liquid markets, small firms may not be actively traded at all times of the year. In this case stale price quotes at one time of year might be followed by similar stale quotes the next year, giving the appearance of autocorrelation in returns. Table 5 diagnoses this possibility by testing our strategies on separate subsamples of small-, medium-, and large-capitalization stocks. Small stocks are less liquid, while large stocks are more actively traded. If the results are due to illiquidity then the effect should disappear or shrink in large stocks.

We can categorize the size of a firm in domestic terms relative to the market capitalization of other stocks in the same country, or instead in global terms compared to firms in all countries. The top 30% of firms at the end of the month prior to holding period are considered “large,” the bottom 30% are “small,” and the remainder are “medium.” The advantage of the domestic definition of size is that our portfolio strategies within a domestic size category tend to be diversified across all countries, leading to lower risk and higher statistical power. In contrast, the global definition compares firms of similar size and potentially similar liquidity across countries.

By both domestic and global definitions of size, the Years 2–3 annual and nonannual strategies give slightly weaker results in large stocks than in small or medium stocks. Yet the Years 4–5 annual strategy is actually slightly more profitable among large stocks than it is among small stocks. All the nonannual strategies lose money in every size group, while the annual strategies earn money in every size group. Since the effect is not limited to small firms, it might be possible to capture some of these returns by trading large stocks in well-diversified international portfolios.

Other measures of liquidity include share price and volume. Table 6 limits the strategies to those stocks selling for more than the equivalent of $5 USD per share, and to the top 75% of stocks in each country based on share price prior to the holding period. It also uses only those stocks with above-median trading volume within their countries. The magnitudes are slightly diminished relative to using the full universe in Table 3. But in all cases the long-term annual strategies are significantly more profitable than the nonannual strategies.

---

# Page 14

1146 Journal of Financial and Quantitative Analysis

TABLE 5

Relative Strength Strategies across Different Size Groups

Each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The difference strategy is the annual strategy minus the nonannual strategy. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. The average monthly return difference between the highest past-performing decile and the lowest past-performing decile is then calculated for the period February 1985–June 2006 (257 months). Table 5 reports the results of this procedure, performed separately for 3 different size groups (measured by market capitalization in U.S. dollars), within each country and across all countries. Small firms are defined as the bottom 30%, large firms are the top 30%, and the remaining 40% are medium-size firms. The size categorization is reevaluated in the beginning of every month. The corresponding t-statistics are also reported (2-decimal-place numbers). The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th rowspan="2">Strategy</th>
      <th colspan="3">Intracountry Size Breakpoints</th>
      <th colspan="3">Intercountry Size Breakpoints</th>
    </tr>
    <tr>
      <th>Small</th>
      <th>Medium</th>
      <th>Large</th>
      <th>Small</th>
      <th>Medium</th>
      <th>Large</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="7">Panel A. Year 1</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0043<br>1.47</td>
      <td>0.0133<br>4.28</td>
      <td>0.0088<br>2.29</td>
      <td>0.0087<br>2.97</td>
      <td>0.0103<br>3.20</td>
      <td>0.0071<br>1.77</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0064<br>3.10</td>
      <td>0.0111<br>5.24</td>
      <td>0.0088<br>3.39</td>
      <td>0.0069<br>3.42</td>
      <td>0.0112<br>5.42</td>
      <td>0.0085<br>3.14</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0020<br>0.58</td>
      <td>–0.0022<br>–0.65</td>
      <td>0.0000<br>0.00</td>
      <td>–0.0018<br>–0.53</td>
      <td>0.0010<br>0.29</td>
      <td>0.0014<br>0.33</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0061<br>2.11</td>
      <td>0.0153<br>4.91</td>
      <td>0.0107<br>2.76</td>
      <td>0.0105<br>3.68</td>
      <td>0.0127<br>4.00</td>
      <td>0.0094<br>2.36</td>
    </tr>
    <tr>
      <td colspan="7">Panel B. Years 2–3</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>–0.0129<br>–5.50</td>
      <td>–0.0117<br>–6.13</td>
      <td>–0.0071<br>–2.51</td>
      <td>–0.0123<br>–5.74</td>
      <td>–0.0122<br>–6.23</td>
      <td>–0.0068<br>–2.40</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0041<br>2.12</td>
      <td>0.0047<br>2.98</td>
      <td>0.0017<br>0.80</td>
      <td>0.0043<br>2.32</td>
      <td>0.0048<br>3.09</td>
      <td>0.0012<br>0.53</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0170<br>6.21</td>
      <td>0.0164<br>6.81</td>
      <td>0.0087<br>2.61</td>
      <td>0.0167<br>6.07</td>
      <td>0.0170<br>7.08</td>
      <td>0.0079<br>2.32</td>
    </tr>
    <tr>
      <td>All</td>
      <td>–0.0109<br>–4.73</td>
      <td>–0.0097<br>–5.07</td>
      <td>–0.0066<br>–2.42</td>
      <td>–0.0100<br>–4.59</td>
      <td>–0.0107<br>–5.44</td>
      <td>–0.0063<br>–2.24</td>
    </tr>
    <tr>
      <td colspan="7">Panel C. Years 4–5</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>–0.0043<br>–2.05</td>
      <td>–0.0041<br>–2.74</td>
      <td>–0.0052<br>–2.78</td>
      <td>–0.0043<br>–2.27</td>
      <td>–0.0036<br>–2.58</td>
      <td>–0.0058<br>–3.00</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0009<br>0.41</td>
      <td>0.0039<br>2.73</td>
      <td>0.0027<br>1.51</td>
      <td>0.0025<br>1.29</td>
      <td>0.0036<br>2.43</td>
      <td>0.0031<br>1.73</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0051<br>1.77</td>
      <td>0.0080<br>3.63</td>
      <td>0.0079<br>3.28</td>
      <td>0.0068<br>2.55</td>
      <td>0.0072<br>3.33</td>
      <td>0.0089<br>3.53</td>
    </tr>
    <tr>
      <td>All</td>
      <td>–0.0042<br>–2.05</td>
      <td>–0.0027<br>–1.85</td>
      <td>–0.0034<br>–1.75</td>
      <td>–0.0045<br>–2.38</td>
      <td>–0.0022<br>–1.56</td>
      <td>–0.0041<br>–2.08</td>
    </tr>
  </tbody>
</table>

B. Comparisons across Countries

It is important to determine whether the annual strategies are profitable in all countries or only in a special subset. If the annual return patterns are limited to a particular country, then they may be compensation for country-specific risk or liquidity conditions. But if the return effect exists across all countries, then it may provide evidence of a seasonal premium for international stock risk.

Table 7 presents the performance of our annual and nonannual strategies in each country separately. The Year 1 nonannual strategies are profitable in every country except Japan, confirming the previous studies of Rouwenhorst (1998) and Griffin et al. (2003). In this respect it appears that Japan is somehow different and lacks any positive momentum effect within 1 year (Liu and Lee (2001), Chui et al. (2001)). Yet, the Year 1 annual strategies indicate otherwise. With the exception

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 15

Heston and Sadka 1147

TABLE 6

Controlling for Liquidity

In Table 6, each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The difference strategy is the annual strategy minus the nonannual strategy. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. The average monthly returns of the various trading strategies for the period February 1985–June 2006 (257 months) are reported, as well as the corresponding t-statistics (2-decimal-place numbers). Each panel uses a different subset of stocks in the portfolios: stocks whose price is at least $5 USD at the end of the previous month, stocks that are in the top 75% of price in each country, and stocks whose trading volume during the previous month is in the top 50% of volume in each country. The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th>Stocks Above $5 USD</th>
      <th>Stocks at Top 75% of Price in Each Country</th>
      <th>Stocks at Top 50% of Volume in Each Country</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Panel A. Year 1</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0170<br>5.24</td>
      <td>0.0173<br>5.88</td>
      <td>0.0153<br>4.22</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0103<br>5.04</td>
      <td>0.0103<br>5.33</td>
      <td>0.0082<br>3.25</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>–0.0067<br>–2.01</td>
      <td>–0.0070<br>–2.28</td>
      <td>–0.0071<br>–1.80</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0182<br>5.62</td>
      <td>0.0176<br>6.03</td>
      <td>0.0152<br>4.19</td>
    </tr>
    <tr>
      <td>Panel B. Years 2–3</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>–0.0070<br>–3.18</td>
      <td>–0.0084<br>–4.05</td>
      <td>–0.0139<br>–6.03</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0041<br>2.72</td>
      <td>0.0035<br>2.73</td>
      <td>0.0022<br>1.34</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0112<br>4.38</td>
      <td>0.0119<br>5.26</td>
      <td>0.0161<br>6.61</td>
    </tr>
    <tr>
      <td>All</td>
      <td>–0.0058<br>–2.66</td>
      <td>–0.0068<br>–3.29</td>
      <td>–0.0123<br>–5.20</td>
    </tr>
    <tr>
      <td>Panel C. Years 4–5</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>–0.0041<br>–2.71</td>
      <td>–0.0035<br>–2.69</td>
      <td>–0.0032<br>–1.73</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0030<br>2.44</td>
      <td>0.0036<br>3.31</td>
      <td>0.0044<br>2.84</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0071<br>4.10</td>
      <td>0.0071<br>4.35</td>
      <td>0.0076<br>3.19</td>
    </tr>
    <tr>
      <td>All</td>
      <td>–0.0030<br>–1.91</td>
      <td>–0.0023<br>–1.74</td>
      <td>–0.0016<br>–0.90</td>
    </tr>
  </tbody>
</table>

of Austria, the Year 1 annual strategies are profitable in every country. The decile spread of 85 bp in Japan is actually higher than the return in Canada (50 bp), Finland (38 bp), France (70 bp), Italy (52 bp), or the Netherlands (80 bp).

The longer-term nonannual strategies resemble the DeBondt and Thaler (1985), (1987) strategies. They lose money in every country, except that the Years 4–5 nonannual strategy earns a statistically insignificant 6 bp in Belgium and 78 bp in Finland. This appears to confirm the reversal effect in Griffin et al. (2003) that tests strategies with global stocks using formation lags beyond 12 months. But the Years 2–3 and Years 4–5 annual strategies are profitable in almost every county, including Japan. This finding of positive annual continuation is new in this international context. The positive annual return continuation and intermediate nonannual return reversal appear to describe the cross section of returns in many countries.

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 16

1148 Journal of Financial and Quantitative Analysis

---

TABLE 7

Relative Strength Strategies across Different Countries

In Table 7, each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The difference strategy is the annual strategy minus the nonannual strategy. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. The average monthly returns of the various trading strategies are reported separately for each country in the sample for the period February 1985–June 2006 (257 months). The corresponding $t$-statistics are also reported (2-decimal-place numbers). The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th>Austria</th>
      <th>Belgium</th>
      <th>Canada</th>
      <th>Finland</th>
      <th>France</th>
      <th>Germany</th>
      <th>Italy</th>
      <th>Japan</th>
      <th>Netherlands</th>
      <th>Norway</th>
      <th>Spain</th>
      <th>Sweden</th>
      <th>Switzerland</th>
      <th>United Kingdom</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Panel A. Year 1</td>
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
      <td>Nonannual</td>
      <td>0.0089<br>0.95</td>
      <td>0.0241<br>5.37</td>
      <td>0.0198<br>3.45</td>
      <td>0.0042<br>0.51</td>
      <td>0.0187<br>3.81</td>
      <td>0.0105<br>2.33</td>
      <td>0.0173<br>3.29</td>
      <td>−0.0027<br>−0.66</td>
      <td>0.0203<br>3.25</td>
      <td>0.0203<br>2.33</td>
      <td>0.0115<br>2.29</td>
      <td>0.0112<br>1.69</td>
      <td>0.0170<br>3.39</td>
      <td>0.0173<br>4.29</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>−0.0042<br>−0.56</td>
      <td>0.0087<br>2.27</td>
      <td>0.0050<br>0.98</td>
      <td>0.0038<br>0.66</td>
      <td>0.0070<br>2.12</td>
      <td>0.0117<br>3.23</td>
      <td>0.0052<br>1.51</td>
      <td>0.0085<br>3.39</td>
      <td>0.0080<br>1.90</td>
      <td>0.0104<br>1.48</td>
      <td>0.0089<br>2.39</td>
      <td>0.0211<br>4.07</td>
      <td>0.0093<br>2.41</td>
      <td>0.0062<br>2.63</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>−0.0131<br>−0.91</td>
      <td>−0.0154<br>−2.75</td>
      <td>−0.0148<br>−1.95</td>
      <td>−0.0003<br>−0.04</td>
      <td>−0.0118<br>−2.04</td>
      <td>0.0011<br>0.20</td>
      <td>−0.0121<br>−2.05</td>
      <td>0.0111<br>2.61</td>
      <td>−0.0123<br>−2.03</td>
      <td>−0.0099<br>−0.88</td>
      <td>−0.0026<br>−0.43</td>
      <td>0.0099<br>1.35</td>
      <td>−0.0077<br>−1.27</td>
      <td>−0.0112<br>−2.72</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0118<br>1.45</td>
      <td>0.0250<br>5.33</td>
      <td>0.0204<br>3.45</td>
      <td>0.0089<br>1.11</td>
      <td>0.0167<br>3.41</td>
      <td>0.0125<br>2.91</td>
      <td>0.0158<br>3.08</td>
      <td>0.0006<br>0.15</td>
      <td>0.0195<br>2.98</td>
      <td>0.0210<br>2.43</td>
      <td>0.0152<br>2.94</td>
      <td>0.0140<br>2.10</td>
      <td>0.0170<br>3.42</td>
      <td>0.0171<br>4.09</td>
    </tr>
  </tbody>
</table>

(continued on next page)

Published online by Cambridge University Press https://doi.org/10.1017/S002210000515400001060122005/ZL1010190101715400001060122005/ZL1010190101715400001060122005

1148 Journal of Financial and Quantitative Analysis

---

# Page 17

TABLE 7 (continued)

Relative Strength Strategies across Different Countries

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th>Austria</th>
      <th>Belgium</th>
      <th>Canada</th>
      <th>Finland</th>
      <th>France</th>
      <th>Germany</th>
      <th>Italy</th>
      <th>Japan</th>
      <th>Netherlands</th>
      <th>Norway</th>
      <th>Spain</th>
      <th>Sweden</th>
      <th>Switzerland</th>
      <th>United Kingdom</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>*Panel B. Years 2–3*</td>
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
      <td>Nonannual</td>
      <td>–0.0038<br>–0.58</td>
      <td>–0.0030<br>–0.70</td>
      <td>–0.0200<br>–4.06</td>
      <td>–0.0117<br>–1.82</td>
      <td>–0.0115<br>–3.44</td>
      <td>–0.0138<br>–3.38</td>
      <td>–0.0044<br>–0.99</td>
      <td>–0.0129<br>–4.92</td>
      <td>–0.0063<br>–1.22</td>
      <td>–0.0222<br>–3.20</td>
      <td>–0.0146<br>–3.30</td>
      <td>–0.0113<br>–1.94</td>
      <td>–0.0009<br>–0.22</td>
      <td>–0.0145<br>–4.69</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0188<br>2.30</td>
      <td>0.0080<br>2.05</td>
      <td>–0.0003<br>–0.05</td>
      <td>0.0076<br>1.13</td>
      <td>0.0043<br>1.69</td>
      <td>0.0031<br>1.11</td>
      <td>0.0072<br>2.66</td>
      <td>0.0027<br>1.33</td>
      <td>0.0040<br>1.01</td>
      <td>0.0059<br>0.89</td>
      <td>0.0071<br>1.84</td>
      <td>0.0117<br>2.96</td>
      <td>0.0061<br>1.76</td>
      <td>0.0013<br>0.58</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0226<br>2.26</td>
      <td>0.0110<br>1.93</td>
      <td>0.0198<br>2.80</td>
      <td>0.0194<br>2.08</td>
      <td>0.0158<br>4.08</td>
      <td>0.0169<br>3.97</td>
      <td>0.0116<br>2.41</td>
      <td>0.0156<br>4.51</td>
      <td>0.0103<br>1.97</td>
      <td>0.0281<br>3.08</td>
      <td>0.0217<br>3.86</td>
      <td>0.0230<br>3.55</td>
      <td>0.0070<br>1.37</td>
      <td>0.0158<br>4.89</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0048<br>0.59</td>
      <td>–0.0014<br>–0.32</td>
      <td>–0.0203<br>–4.16</td>
      <td>–0.0107<br>–1.71</td>
      <td>–0.0093<br>–2.86</td>
      <td>–0.0127<br>–3.08</td>
      <td>–0.0053<br>–1.17</td>
      <td>–0.0118<br>–4.64</td>
      <td>–0.0051<br>–0.92</td>
      <td>–0.0187<br>–2.80</td>
      <td>–0.0100<br>–2.09</td>
      <td>–0.0108<br>–1.85</td>
      <td>0.0011<br>0.30</td>
      <td>–0.0128<br>–4.11</td>
    </tr>
    <tr>
      <td>*Panel C. Years 4–5*</td>
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
      <td>Nonannual</td>
      <td>–0.0033<br>–0.57</td>
      <td>0.0006<br>0.14</td>
      <td>–0.0097<br>–1.92</td>
      <td>0.0064<br>0.88</td>
      <td>–0.0066<br>–1.88</td>
      <td>–0.0038<br>–1.14</td>
      <td>–0.0015<br>–0.33</td>
      <td>–0.0055<br>–3.13</td>
      <td>–0.0022<br>–0.52</td>
      <td>–0.0162<br>–2.24</td>
      <td>–0.0137<br>–3.21</td>
      <td>–0.0079<br>–1.44</td>
      <td>–0.0026<br>–0.58</td>
      <td>–0.0070<br>–2.66</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0010<br>0.12</td>
      <td>–0.0007<br>–0.18</td>
      <td>0.0070<br>1.20</td>
      <td>0.0030<br>0.48</td>
      <td>0.0043<br>1.44</td>
      <td>0.0030<br>1.17</td>
      <td>0.0018<br>0.41</td>
      <td>0.0036<br>1.66</td>
      <td>0.0047<br>1.26</td>
      <td>0.0090<br>1.38</td>
      <td>0.0039<br>0.90</td>
      <td>0.0133<br>2.69</td>
      <td>–0.0001<br>–0.03</td>
      <td>0.0032<br>1.62</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0043<br>0.42</td>
      <td>–0.0013<br>–0.28</td>
      <td>0.0167<br>2.12</td>
      <td>–0.0034<br>–0.32</td>
      <td>0.0109<br>2.29</td>
      <td>0.0068<br>1.68</td>
      <td>0.0033<br>0.55</td>
      <td>0.0091<br>3.22</td>
      <td>0.0070<br>1.43</td>
      <td>0.0252<br>2.80</td>
      <td>0.0176<br>2.99</td>
      <td>0.0212<br>2.95</td>
      <td>0.0025<br>0.41</td>
      <td>0.0102<br>3.21</td>
    </tr>
    <tr>
      <td>All</td>
      <td>–0.0121<br>–1.53</td>
      <td>0.0003<br>0.06</td>
      <td>–0.0045<br>–0.92</td>
      <td>0.0041<br>0.61</td>
      <td>–0.0056<br>–1.55</td>
      <td>–0.0024<br>–0.73</td>
      <td>0.0007<br>0.15</td>
      <td>–0.0035<br>–1.97</td>
      <td>0.0026<br>0.61</td>
      <td>–0.0170<br>–2.28</td>
      <td>–0.0123<br>–2.79</td>
      <td>–0.0042<br>–0.76</td>
      <td>–0.0046<br>–0.99</td>
      <td>–0.0047<br>–1.78</td>
    </tr>
  </tbody>
</table>


Heston and Sacka 1149

Published online by Cambridge University Press https://doi.org/10.1017/S0022100057001019

---

# Page 18

1150 Journal of Financial and Quantitative Analysis

C. Controlling for Risk

Although our annual strategies are profitable within size categories, they may be exposed to other common international risk factors. Hou, Karolyi, and Kho (2008) show that international stocks have significant return premiums associated with risk characteristics such as book-to-market (BM) and cash-earning-to-price (CEP) ratios. If stocks have seasonal exposure to pervasive factors, or if these risk factors have a time-varying price of risk over the calendar year, then our annual patterns might emerge as a consequence.

To analyze risk we construct a market index factor as the return on a value-weighted combination of stocks in our sample in excess of the risk-free return on a 1-month U.S. T-bill. We construct an international analog of the Fama and French (1993) size risk factor following Fama and French (1998) and Rouwenhorst (1998). This “small-minus-big” (SMB) factor is a value-weighted return on the smallest 50% of market capitalization stocks within each country in excess of the largest 50% of firms within each country. We also use additional international factors from Ken French to control for the risk of BM, earnings-to-price (EP), CEP, and dividend yield (DP) ratios. These portfolio risk factors are available for all the countries in our sample, as well as an internationally diversified combination. $^{6}$

To adjust the average returns for risk, we regress the decile spreads of our portfolio strategies (from Table 3) on the international risk factors. The intercepts or $\alpha$ s represent risk-adjusted excess returns. Specifically, they represent rewards to the component of our portfolio returns that is not correlated with international market or other risk factors.

Table 8 presents the risk-adjusted returns using diversified international risk factors. In general, the risk exposures are not large. The market $\beta$ s are less than 0.16 for all strategies, and the SMB exposures are less than 0.2. The Year 1 nonannual strategy has strong negative exposure to BM with a $\beta$ of –0.85. But the Years 4–5 strategy has slight positive exposure to this factor. Exposures to the remaining risk factors are small and almost always statistically insignificant. It appears these strategies do not have much systematic risk. Overall, the magnitude and statistical significance of risk-adjusted returns are quite similar to the raw returns in Table 3. In particular, the risk-adjusted returns for the annual strategies remain positive and significant at the 95% level for the Year 1, Years 2–3, and Years 4–5 annual strategies.

Table 9 presents internationally risk-adjusted $\alpha$ s of the intra- and intercountry decile spreads. The results are quite similar to the unadjusted returns from Table 3. Like the unadjusted returns, the intercountry $\alpha$ s are all insignificantly different from 0. The risk adjustment does little to affect the unadjusted returns. In particular, the $\alpha$ s of all intracountry strategies retain the same sign and statistical significance as the unadjusted returns from Table 3. This holds for both equal-weighted returns (top panel) and value-weighted returns (bottom panel).

---

$^{6}$ We thank Ken French for making these available on his Web site (http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html#International).

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 19

Heston and Sadka 1151

TABLE 8

Risk-Adjusted Returns Using Global Risk Factors

In Table 8, each month stocks are grouped into 10 deciles (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The difference strategy is the annual strategy minus the nonannual strategy. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. The average monthly returns of the top minus the bottom deciles of the various trading strategies for the period February 1985–June 2006 (257 months) are regressed on 6 global factors: MKT-RF, small-minus-big (SMB), book-to-market (BM), earnings-to-price (EP), cash-earnings-to-price (CEP), and dividend yield (DP). The 1st factor is a weighted average of all stocks in the sample excess of the U.S. risk-free rate. The 2nd factor is the difference portfolio between small and large firms. Small firms are firms below their country’s median market capitalization; the rest are large firms (SMB is value weighted). The last 4 factors provided by Ken French (http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/) represent BM, EP, CEP, and DP. The regression coefficients are reported ( $\alpha$ is the regression intercept), as well as the corresponding $t$ -statistics (2-decimal-place numbers) and the $R^2$ . The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th> $\alpha$ </th>
      <th>MKT-RF</th>
      <th>BM</th>
      <th>EP</th>
      <th>CEP</th>
      <th>DP</th>
      <th>SMB</th>
      <th> $R^2$ </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="9">Panel A. Year 1</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0159</td>
      <td>-0.0022</td>
      <td>-0.8538</td>
      <td>0.2654</td>
      <td>-0.0515</td>
      <td>-0.0266</td>
      <td>0.1146</td>
      <td>0.20</td>
    </tr>
    <tr>
      <td></td>
      <td>5.79</td>
      <td>-0.04</td>
      <td>-5.08</td>
      <td>1.43</td>
      <td>-0.34</td>
      <td>-0.18</td>
      <td>1.32</td>
      <td></td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0102</td>
      <td>-0.0370</td>
      <td>-0.1896</td>
      <td>-0.0301</td>
      <td>-0.0015</td>
      <td>-0.0745</td>
      <td>-0.0786</td>
      <td>0.09</td>
    </tr>
    <tr>
      <td></td>
      <td>5.33</td>
      <td>-0.94</td>
      <td>-1.63</td>
      <td>-0.23</td>
      <td>-0.01</td>
      <td>-0.72</td>
      <td>-1.31</td>
      <td></td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>-0.0058</td>
      <td>-0.0349</td>
      <td>0.6643</td>
      <td>-0.2955</td>
      <td>0.0500</td>
      <td>-0.0479</td>
      <td>-0.1932</td>
      <td>0.08</td>
    </tr>
    <tr>
      <td></td>
      <td>-1.86</td>
      <td>-0.55</td>
      <td>3.51</td>
      <td>-1.42</td>
      <td>0.30</td>
      <td>-0.28</td>
      <td>-1.98</td>
      <td></td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0173</td>
      <td>-0.0131</td>
      <td>-0.8321</td>
      <td>0.2121</td>
      <td>-0.0642</td>
      <td>-0.0325</td>
      <td>0.0737</td>
      <td>0.22</td>
    </tr>
    <tr>
      <td></td>
      <td>6.40</td>
      <td>-0.23</td>
      <td>-5.03</td>
      <td>1.16</td>
      <td>-0.43</td>
      <td>-0.22</td>
      <td>0.87</td>
      <td></td>
    </tr>
    <tr>
      <td colspan="9">Panel B. Years 2–3</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>-0.0125</td>
      <td>0.0691</td>
      <td>-0.0017</td>
      <td>-0.0446</td>
      <td>-0.1750</td>
      <td>-0.0796</td>
      <td>-0.1559</td>
      <td>0.12</td>
    </tr>
    <tr>
      <td></td>
      <td>-6.22</td>
      <td>1.63</td>
      <td>-0.01</td>
      <td>-0.32</td>
      <td>-1.56</td>
      <td>-0.62</td>
      <td>-2.42</td>
      <td></td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0035</td>
      <td>0.0481</td>
      <td>-0.0094</td>
      <td>-0.1118</td>
      <td>0.0515</td>
      <td>0.0663</td>
      <td>-0.0068</td>
      <td>0.02</td>
    </tr>
    <tr>
      <td></td>
      <td>2.48</td>
      <td>1.63</td>
      <td>-0.11</td>
      <td>-1.14</td>
      <td>0.66</td>
      <td>0.75</td>
      <td>-0.15</td>
      <td></td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0159</td>
      <td>-0.0210</td>
      <td>-0.0077</td>
      <td>-0.0672</td>
      <td>0.2264</td>
      <td>0.1459</td>
      <td>0.1491</td>
      <td>0.09</td>
    </tr>
    <tr>
      <td></td>
      <td>7.29</td>
      <td>-0.46</td>
      <td>-0.05</td>
      <td>-0.44</td>
      <td>1.85</td>
      <td>1.05</td>
      <td>2.12</td>
      <td></td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0108</td>
      <td>0.0657</td>
      <td>0.0181</td>
      <td>-0.0902</td>
      <td>-0.1867</td>
      <td>-0.0518</td>
      <td>-0.1393</td>
      <td>0.12</td>
    </tr>
    <tr>
      <td></td>
      <td>-5.54</td>
      <td>1.59</td>
      <td>0.14</td>
      <td>-0.66</td>
      <td>-1.71</td>
      <td>-0.41</td>
      <td>-2.21</td>
      <td></td>
    </tr>
    <tr>
      <td colspan="9">Panel C. Years 4–5</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>-0.0060</td>
      <td>0.1176</td>
      <td>0.3049</td>
      <td>-0.0587</td>
      <td>-0.1600</td>
      <td>-0.1022</td>
      <td>-0.0722</td>
      <td>0.15</td>
    </tr>
    <tr>
      <td></td>
      <td>-4.34</td>
      <td>3.90</td>
      <td>3.01</td>
      <td>-0.57</td>
      <td>-1.81</td>
      <td>-1.08</td>
      <td>-1.61</td>
      <td></td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0043</td>
      <td>0.0565</td>
      <td>-0.1145</td>
      <td>0.0121</td>
      <td>0.0872</td>
      <td>-0.0163</td>
      <td>0.1222</td>
      <td>0.06</td>
    </tr>
    <tr>
      <td></td>
      <td>3.36</td>
      <td>2.01</td>
      <td>-1.21</td>
      <td>0.13</td>
      <td>1.06</td>
      <td>-0.18</td>
      <td>2.92</td>
      <td></td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0103</td>
      <td>-0.0611</td>
      <td>-0.4194</td>
      <td>0.0708</td>
      <td>0.2473</td>
      <td>0.0860</td>
      <td>0.1944</td>
      <td>0.11</td>
    </tr>
    <tr>
      <td></td>
      <td>5.74</td>
      <td>-1.56</td>
      <td>-3.19</td>
      <td>0.53</td>
      <td>2.15</td>
      <td>0.70</td>
      <td>3.34</td>
      <td></td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0044</td>
      <td>0.1217</td>
      <td>0.2910</td>
      <td>-0.0662</td>
      <td>-0.1450</td>
      <td>-0.1206</td>
      <td>-0.0698</td>
      <td>0.15</td>
    </tr>
    <tr>
      <td></td>
      <td>-3.15</td>
      <td>3.96</td>
      <td>2.82</td>
      <td>-0.63</td>
      <td>-1.61</td>
      <td>-1.25</td>
      <td>-1.53</td>
      <td></td>
    </tr>
  </tbody>
</table>

If capital markets are segmented across countries, then the global risk factors may not explain returns to strategies exposed to country risks. Instead, stocks may have return premiums for exposure to local risks. In this case, fluctuating local risk premiums are a potential explanation for the profitability of our strategies. Therefore, we examine the profitability of our strategies separately across countries while controlling for country-specific risk factors.

Table 10 compares the performance of the annual and nonannual portfolio strategies across countries. Following the previous section, we regress decile spreads of our portfolio strategies within each country on local risk factors, including the local market, size (SMB), and the local versions of Ken French’s BM, EP, CEP, and DP factors. The Year 1 nonannual strategy displays positive risk-adjusted returns over our sample in every country. However, the effect is smallest

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 20

1152 Journal of Financial and Quantitative Analysis

and statistically insignificant in Japan. This is consistent with the previous findings of Liu and Lee (2001) and Chui et al. (2001) on the absence of short-term momentum in Japan. In this respect Japanese equity markets appear different from other developed markets.

In contrast to the nonannual strategy, the Year 1 annual strategy that sorts stocks based on a single lagged annual return is profitable in Japan as well as

---

TABLE 9

Inter- and Intracountry Alphas Using Global Risk Factors

In Table 9, each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on past performance. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns during the historical lags 48 and 60. For each strategy, the table reports the portfolio return spread of the top-minus-bottom decile. The difference strategy is the annual strategy minus the nonannual strategy. A stock’s past return performance is measured either in excess of its country’s equal-weighted average (Panel A) or as its total (simple) return (Panel B). The monthly holding return of every stock is then decomposed into intra- and intercountry components. The intracountry component is the monthly return of the stock excess of its country’s equal-weighted average return, and the intercountry component is the average monthly return of the country itself. The average monthly returns (equal- and value-weighted) of the various trading strategies (for both intra- and interindustry components) for the period February 1985–June 2006 (257 months) are regressed on 6 global factors: MKT-RF, small-minus-big (SMB), book-to-market (BM), earnings-to-price (EP), cash-earnings-to-price (CEP), and dividend yield (DP). The 1st factor is a weighted average of all stocks in the sample excess of the U.S. risk-free rate. The 2nd factor is the difference portfolio between small and large firms. Small firms are firms below their country’s median market capitalization; the rest are large firms (SMB is value weighted). The last 4 factors provided by Ken French (http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/) represent BM, EP, CEP, and DP. The regression intercepts ( $\alpha$ s) are reported, as well as the corresponding $t$ -statistics (2-decimal-place numbers). The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

Equal-Weighted Portfolio Returns

<table>
  <thead>
    <tr>
      <th rowspan="2">Strategy</th>
      <th colspan="3">Panel A. Sorting by Historical Return Excess of Country</th>
      <th colspan="3">Panel B. Sorting by Historical Total Return</th>
    </tr>
    <tr>
      <th>Total Return</th>
      <th>Intra-country Return</th>
      <th>Inter-country Return</th>
      <th>Total Return</th>
      <th>Intra-country Return</th>
      <th>Inter-country Return</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Year 1</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0159<br>5.79</td>
      <td>0.0158<br>5.78</td>
      <td>0.0001<br>0.26</td>
      <td>0.0172<br>4.84</td>
      <td>0.0145<br>5.59</td>
      <td>0.0027<br>1.52</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0102<br>5.33</td>
      <td>0.0106<br>5.66</td>
      <td>-0.0005<br>-1.70</td>
      <td>0.0107<br>3.59</td>
      <td>0.0102<br>5.63</td>
      <td>0.0005<br>0.27</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>-0.0058<br>-1.86</td>
      <td>-0.0052<br>-1.66</td>
      <td>-0.0006<br>-1.68</td>
      <td>-0.0065<br>-1.61</td>
      <td>-0.0044<br>-1.45</td>
      <td>-0.0022<br>-1.04</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0173<br>6.40</td>
      <td>0.0173<br>6.41</td>
      <td>0.0001<br>0.16</td>
      <td>0.0190<br>5.35</td>
      <td>0.0161<br>6.33</td>
      <td>0.0029<br>1.59</td>
    </tr>
    <tr>
      <td>Years 2–3</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>-0.0125<br>-6.22</td>
      <td>-0.0118<br>-5.93</td>
      <td>-0.0007<br>-2.22</td>
      <td>-0.0128<br>-5.09</td>
      <td>-0.0110<br>-5.88</td>
      <td>-0.0019<br>-1.23</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0035<br>2.48</td>
      <td>0.0035<br>2.59</td>
      <td>0.0000<br>-0.10</td>
      <td>0.0049<br>2.07</td>
      <td>0.0037<br>2.74</td>
      <td>0.0013<br>0.72</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0159<br>7.29</td>
      <td>0.0153<br>6.99</td>
      <td>0.0007<br>1.75</td>
      <td>0.0178<br>5.36</td>
      <td>0.0147<br>6.95</td>
      <td>0.0031<br>1.42</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0108<br>-5.54</td>
      <td>-0.0103<br>-5.29</td>
      <td>-0.0005<br>-1.68</td>
      <td>-0.0117<br>-4.76</td>
      <td>-0.0101<br>-5.53</td>
      <td>-0.0015<br>-1.02</td>
    </tr>
    <tr>
      <td>Years 4–5</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>-0.0060<br>-4.34</td>
      <td>-0.0055<br>-4.15</td>
      <td>-0.0005<br>-1.30</td>
      <td>-0.0038<br>-1.81</td>
      <td>-0.0050<br>-3.94</td>
      <td>0.0011<br>0.79</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0043<br>3.36</td>
      <td>0.0046<br>3.70</td>
      <td>-0.0003<br>-1.11</td>
      <td>0.0042<br>1.69</td>
      <td>0.0038<br>3.13</td>
      <td>0.0003<br>0.18</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0103<br>5.74</td>
      <td>0.0102<br>5.70</td>
      <td>0.0001<br>0.41</td>
      <td>0.0080<br>2.55</td>
      <td>0.0088<br>5.03</td>
      <td>-0.0008<br>-0.35</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0044<br>-3.15</td>
      <td>-0.0042<br>-3.11</td>
      <td>-0.0002<br>-0.57</td>
      <td>-0.0028<br>-1.35</td>
      <td>-0.0041<br>-3.12</td>
      <td>0.0012<br>0.84</td>
    </tr>
  </tbody>
</table>

(continued on next page)

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 21

Heston and Sadka 1153

TABLE 9 (continued)

Inter- and Intracountry Alphas Using Global Risk Factors

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th>Value-Weighted Portfolio Returns</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>Panel A. Sorting by Historical Return Excess of Country</td>
      <td></td>
      <td></td>
      <td>Panel B. Sorting by Historical Total Return</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Total Return</td>
      <td>Intra-country Return</td>
      <td>Inter-country Return</td>
      <td>Total Return</td>
      <td>Intra-country Return</td>
      <td>Inter-country Return</td>
    </tr>
    <tr>
      <td>Year 1</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0160</td>
      <td>0.0167</td>
      <td>-0.0007</td>
      <td>0.0105</td>
      <td>0.0095</td>
      <td>0.0010</td>
    </tr>
    <tr>
      <td></td>
      <td>3.08</td>
      <td>3.18</td>
      <td>-0.45</td>
      <td>1.76</td>
      <td>1.93</td>
      <td>0.37</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0166</td>
      <td>0.0171</td>
      <td>-0.0006</td>
      <td>0.0149</td>
      <td>0.0139</td>
      <td>0.0010</td>
    </tr>
    <tr>
      <td></td>
      <td>4.56</td>
      <td>5.10</td>
      <td>-0.44</td>
      <td>3.57</td>
      <td>4.34</td>
      <td>0.40</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0006</td>
      <td>0.0004</td>
      <td>0.0001</td>
      <td>0.0044</td>
      <td>0.0044</td>
      <td>0.0000</td>
    </tr>
    <tr>
      <td></td>
      <td>0.09</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>0.66</td>
      <td>0.80</td>
      <td>-0.01</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0178</td>
      <td>0.0189</td>
      <td>-0.0011</td>
      <td>0.0151</td>
      <td>0.0148</td>
      <td>0.0002</td>
    </tr>
    <tr>
      <td></td>
      <td>3.60</td>
      <td>3.82</td>
      <td>-0.73</td>
      <td>2.57</td>
      <td>3.13</td>
      <td>0.08</td>
    </tr>
    <tr>
      <td>Years 2–3</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0015</td>
      <td>-0.0004</td>
      <td>0.0019</td>
      <td>-0.0023</td>
      <td>-0.0045</td>
      <td>0.0022</td>
    </tr>
    <tr>
      <td></td>
      <td>0.46</td>
      <td>-0.13</td>
      <td>1.32</td>
      <td>-0.69</td>
      <td>-1.57</td>
      <td>1.07</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>-0.0001</td>
      <td>0.0024</td>
      <td>-0.0024</td>
      <td>0.0034</td>
      <td>0.0033</td>
      <td>0.0000</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.02</td>
      <td>0.79</td>
      <td>-2.04</td>
      <td>0.84</td>
      <td>1.01</td>
      <td>0.02</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>-0.0016</td>
      <td>0.0028</td>
      <td>-0.0043</td>
      <td>0.0057</td>
      <td>0.0079</td>
      <td>-0.0022</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.34</td>
      <td>0.63</td>
      <td>-2.17</td>
      <td>1.13</td>
      <td>1.87</td>
      <td>-0.64</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0015</td>
      <td>0.0007</td>
      <td>0.0008</td>
      <td>-0.0005</td>
      <td>-0.0024</td>
      <td>0.0019</td>
    </tr>
    <tr>
      <td></td>
      <td>0.46</td>
      <td>0.23</td>
      <td>0.55</td>
      <td>-0.14</td>
      <td>-0.84</td>
      <td>0.94</td>
    </tr>
    <tr>
      <td>Years 4–5</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>-0.0026</td>
      <td>-0.0026</td>
      <td>0.0000</td>
      <td>0.0002</td>
      <td>-0.0013</td>
      <td>0.0015</td>
    </tr>
    <tr>
      <td></td>
      <td>-1.00</td>
      <td>-1.01</td>
      <td>0.03</td>
      <td>0.05</td>
      <td>-0.46</td>
      <td>0.71</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0058</td>
      <td>0.0083</td>
      <td>-0.0025</td>
      <td>0.0054</td>
      <td>0.0071</td>
      <td>-0.0017</td>
    </tr>
    <tr>
      <td></td>
      <td>2.05</td>
      <td>3.27</td>
      <td>-1.85</td>
      <td>1.60</td>
      <td>3.12</td>
      <td>-0.68</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0084</td>
      <td>0.0109</td>
      <td>-0.0026</td>
      <td>0.0052</td>
      <td>0.0084</td>
      <td>-0.0032</td>
    </tr>
    <tr>
      <td></td>
      <td>2.30</td>
      <td>3.06</td>
      <td>-1.36</td>
      <td>1.10</td>
      <td>2.38</td>
      <td>-0.96</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0024</td>
      <td>-0.0027</td>
      <td>0.0003</td>
      <td>0.0007</td>
      <td>-0.0005</td>
      <td>0.0012</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.92</td>
      <td>-1.05</td>
      <td>0.24</td>
      <td>0.20</td>
      <td>-0.16</td>
      <td>0.55</td>
    </tr>
  </tbody>
</table>


almost all the other countries. The average risk-adjusted decile spread is 106 bp per month in Japan, which is greater than the corresponding spread for Canada or the European countries except Germany (130 bp), Norway (136 bp), and Sweden (198 bp). Abnormal returns are positive and statistically significant at the 95% level in most countries.

The longer-term strategies also give similar results across countries. The Years 2–3 nonannual strategy loses money (after risk adjustment) in every country except Belgium and Switzerland, while the Years 4–5 nonannual strategy loses money in every country except Finland. The Years 2–3 annual strategy produces positive abnormal returns in all countries except Canada. Similarly, the Years 4–5 annual strategy earns risk-adjusted returns in 13 of the 14 countries. The difference between the positive Years 2–3 annual and negative Years 2–3 nonannual results is statistically significant at the 95% level in 11 of the countries, and the difference between the positive and negative Years 4–5 strategies is significant in half the countries.

An important reason to examine the pattern of predictability across different countries is to provide independent statistical evidence about the cross section of

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 22

1154 Journal of Financial and Quantitative Analysis

---

TABLE 10

Country Alphas Using Local Risk Factors

In Table 10, each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The difference strategy is the annual strategy minus the nonannual strategy. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. The average monthly returns of the various trading strategies for each country in the sample for the period February 1985–June 2006 (257 months) are regressed on 6 country-specific factors: MKT-RF, small-minus-big (SMB), book-to-market (BM), earnings-to-price (EP), cash-earnings-to-price (CEP), and dividend yield (DP). The 1st factor is a weighted average of all stocks in a country excess of the U.S. risk-free rate. The 2nd factor is the difference portfolio between small and large firms in each country. Small firms are firms below their country’s median market capitalization; the rest are large firms (SMB is value weighted). The last 4 factors provided by Ken French (http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/) represent country-specific BM, EP, CEP, and DP. The regression intercepts ( $\alpha$ s) are reported, as well as the corresponding $t$ -statistics (2-decimal-place numbers). The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th>Strategy</th>
      <th>Austria</th>
      <th>Belgium</th>
      <th>Canada</th>
      <th>Finland</th>
      <th>France</th>
      <th>Germany</th>
      <th>Italy</th>
      <th>Japan</th>
      <th>Netherlands</th>
      <th>Norway</th>
      <th>Spain</th>
      <th>Sweden</th>
      <th>Switzerland</th>
      <th>United Kingdom</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Panel A. Year 1</td>
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
      <td>Nonannual</td>
      <td>0.0068<br>0.66</td>
      <td>0.0278<br>6.38</td>
      <td>0.0280<br>3.06</td>
      <td>0.0078<br>0.95</td>
      <td>0.0206<br>4.31</td>
      <td>0.0128<br>2.96</td>
      <td>0.0192<br>3.75</td>
      <td>0.0029<br>0.76</td>
      <td>0.0226<br>3.71</td>
      <td>0.0182<br>2.05</td>
      <td>0.0133<br>2.54</td>
      <td>0.0101<br>1.48</td>
      <td>0.0183<br>3.69</td>
      <td>0.0197<br>5.23</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>−0.0011<br>−0.14</td>
      <td>0.0105<br>2.70</td>
      <td>−0.0076<br>−0.89</td>
      <td>0.0054<br>0.92</td>
      <td>0.0085<br>2.50</td>
      <td>0.0130<br>3.65</td>
      <td>0.0057<br>1.63</td>
      <td>0.0106<br>4.30</td>
      <td>0.0105<br>2.45</td>
      <td>0.0136<br>1.90</td>
      <td>0.0100<br>2.59</td>
      <td>0.0198<br>3.77</td>
      <td>0.0085<br>2.15</td>
      <td>0.0074<br>3.16</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>−0.0079<br>−0.51</td>
      <td>−0.0173<br>−3.09</td>
      <td>−0.0356<br>−2.97</td>
      <td>−0.0024<br>−0.26</td>
      <td>−0.0121<br>−2.07</td>
      <td>0.0002<br>0.03</td>
      <td>−0.0136<br>−2.30</td>
      <td>0.0077<br>1.84</td>
      <td>−0.0121<br>−1.95</td>
      <td>−0.0047<br>−0.41</td>
      <td>−0.0033<br>−0.53</td>
      <td>0.0097<br>1.28</td>
      <td>−0.0098<br>−1.63</td>
      <td>−0.0123<br>−3.09</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0087<br>1.00</td>
      <td>0.0291<br>6.34</td>
      <td>0.0311<br>3.41</td>
      <td>0.0102<br>1.27</td>
      <td>0.0189<br>4.00</td>
      <td>0.0147<br>3.55</td>
      <td>0.0177<br>3.58</td>
      <td>0.0063<br>1.68</td>
      <td>0.0221<br>3.43</td>
      <td>0.0209<br>2.35</td>
      <td>0.0169<br>3.13</td>
      <td>0.0124<br>1.82</td>
      <td>0.0180<br>3.63</td>
      <td>0.0198<br>5.05</td>
    </tr>
  </tbody>
</table>

(continued on next page)

Published online by Cambridge University Press https://doi.org/10.1017/S00221000515400001060122005/710101/jofq/0000000000000000

---

# Page 23

TABLE 10 (continued)

Country Alphas Using Local Risk Factors

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Strategy</th>
      <th>Austria</th>
      <th>Belgium</th>
      <th>Canada</th>
      <th>Finland</th>
      <th>France</th>
      <th>Germany</th>
      <th>Italy</th>
      <th>Japan</th>
      <th>Netherlands</th>
      <th>Norway</th>
      <th>Spain</th>
      <th>Sweden</th>
      <th>Switzerland</th>
      <th>United Kingdom</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Panel B. Years 2–3</td>
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
      <td>Nonannual</td>
      <td>-0.0057</td>
      <td>0.0003</td>
      <td>-0.0074</td>
      <td>-0.0134</td>
      <td>-0.0105</td>
      <td>-0.0117</td>
      <td>-0.0023</td>
      <td>-0.0075</td>
      <td>-0.0096</td>
      <td>-0.0221</td>
      <td>-0.0118</td>
      <td>-0.0117</td>
      <td>-0.0012</td>
      <td>-0.0131</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.86</td>
      <td>0.06</td>
      <td>-0.95</td>
      <td>-2.23</td>
      <td>-3.17</td>
      <td>-2.95</td>
      <td>-0.55</td>
      <td>-3.20</td>
      <td>-1.84</td>
      <td>-3.12</td>
      <td>-2.64</td>
      <td>-2.00</td>
      <td>-0.31</td>
      <td>-4.48</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0190</td>
      <td>0.0078</td>
      <td>-0.0069</td>
      <td>0.0097</td>
      <td>0.0039</td>
      <td>0.0029</td>
      <td>0.0080</td>
      <td>0.0020</td>
      <td>0.0023</td>
      <td>0.0066</td>
      <td>0.0061</td>
      <td>0.0119</td>
      <td>0.0055</td>
      <td>0.0015</td>
    </tr>
    <tr>
      <td></td>
      <td>2.24</td>
      <td>1.95</td>
      <td>-0.80</td>
      <td>1.45</td>
      <td>1.46</td>
      <td>1.03</td>
      <td>2.95</td>
      <td>0.94</td>
      <td>0.57</td>
      <td>0.96</td>
      <td>1.54</td>
      <td>2.92</td>
      <td>1.55</td>
      <td>0.66</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0248</td>
      <td>0.0076</td>
      <td>0.0005</td>
      <td>0.0232</td>
      <td>0.0144</td>
      <td>0.0146</td>
      <td>0.0103</td>
      <td>0.0094</td>
      <td>0.0119</td>
      <td>0.0286</td>
      <td>0.0179</td>
      <td>0.0235</td>
      <td>0.0067</td>
      <td>0.0146</td>
    </tr>
    <tr>
      <td></td>
      <td>2.39</td>
      <td>1.30</td>
      <td>0.04</td>
      <td>2.54</td>
      <td>3.65</td>
      <td>3.47</td>
      <td>2.18</td>
      <td>2.90</td>
      <td>2.24</td>
      <td>3.09</td>
      <td>3.19</td>
      <td>3.63</td>
      <td>1.33</td>
      <td>4.55</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0028</td>
      <td>0.0010</td>
      <td>-0.0121</td>
      <td>-0.0102</td>
      <td>-0.0083</td>
      <td>-0.0103</td>
      <td>-0.0028</td>
      <td>-0.0068</td>
      <td>-0.0077</td>
      <td>-0.0190</td>
      <td>-0.0078</td>
      <td>-0.0110</td>
      <td>0.0005</td>
      <td>-0.0120</td>
    </tr>
    <tr>
      <td></td>
      <td>0.33</td>
      <td>0.24</td>
      <td>-1.65</td>
      <td>-1.75</td>
      <td>-2.58</td>
      <td>-2.61</td>
      <td>-0.66</td>
      <td>-2.97</td>
      <td>-1.36</td>
      <td>-2.80</td>
      <td>-1.60</td>
      <td>-1.85</td>
      <td>0.12</td>
      <td>-4.03</td>
    </tr>
    <tr>
      <td>Panel C. Years 4–5</td>
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
      <td>Nonannual</td>
      <td>-0.0016</td>
      <td>-0.0009</td>
      <td>-0.0132</td>
      <td>0.0056</td>
      <td>-0.0076</td>
      <td>-0.0035</td>
      <td>-0.0011</td>
      <td>-0.0060</td>
      <td>-0.0055</td>
      <td>-0.0132</td>
      <td>-0.0132</td>
      <td>-0.0093</td>
      <td>-0.0032</td>
      <td>-0.0087</td>
    </tr>
    <tr>
      <td></td>
      <td>-0.26</td>
      <td>-0.20</td>
      <td>-1.28</td>
      <td>0.78</td>
      <td>-2.15</td>
      <td>-1.05</td>
      <td>-0.24</td>
      <td>-3.39</td>
      <td>-1.33</td>
      <td>-1.77</td>
      <td>-3.04</td>
      <td>-1.79</td>
      <td>-0.72</td>
      <td>-3.36</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0000</td>
      <td>-0.0004</td>
      <td>0.0034</td>
      <td>0.0022</td>
      <td>0.0046</td>
      <td>0.0021</td>
      <td>0.0004</td>
      <td>0.0024</td>
      <td>0.0042</td>
      <td>0.0096</td>
      <td>0.0040</td>
      <td>0.0158</td>
      <td>0.0003</td>
      <td>0.0029</td>
    </tr>
    <tr>
      <td></td>
      <td>0.00</td>
      <td>-0.11</td>
      <td>0.28</td>
      <td>0.35</td>
      <td>1.47</td>
      <td>0.79</td>
      <td>0.09</td>
      <td>1.09</td>
      <td>1.05</td>
      <td>1.44</td>
      <td>0.89</td>
      <td>3.29</td>
      <td>0.07</td>
      <td>1.41</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>0.0016</td>
      <td>0.0005</td>
      <td>0.0165</td>
      <td>-0.0034</td>
      <td>0.0121</td>
      <td>0.0055</td>
      <td>0.0015</td>
      <td>0.0084</td>
      <td>0.0097</td>
      <td>0.0228</td>
      <td>0.0172</td>
      <td>0.0252</td>
      <td>0.0035</td>
      <td>0.0116</td>
    </tr>
    <tr>
      <td></td>
      <td>0.15</td>
      <td>0.10</td>
      <td>1.01</td>
      <td>-0.32</td>
      <td>2.46</td>
      <td>1.35</td>
      <td>0.25</td>
      <td>2.91</td>
      <td>1.98</td>
      <td>2.46</td>
      <td>2.81</td>
      <td>3.51</td>
      <td>0.58</td>
      <td>3.65</td>
    </tr>
    <tr>
      <td>All</td>
      <td>-0.0090</td>
      <td>-0.0007</td>
      <td>-0.0071</td>
      <td>0.0041</td>
      <td>-0.0073</td>
      <td>-0.0022</td>
      <td>0.0007</td>
      <td>-0.0045</td>
      <td>-0.0009</td>
      <td>-0.0131</td>
      <td>-0.0113</td>
      <td>-0.0054</td>
      <td>-0.0049</td>
      <td>-0.0065</td>
    </tr>
    <tr>
      <td></td>
      <td>-1.09</td>
      <td>-0.16</td>
      <td>-0.86</td>
      <td>0.61</td>
      <td>-2.04</td>
      <td>-0.68</td>
      <td>0.16</td>
      <td>-2.49</td>
      <td>-0.23</td>
      <td>-1.73</td>
      <td>-2.56</td>
      <td>-1.05</td>
      <td>-1.06</td>
      <td>-2.51</td>
    </tr>
  </tbody>
</table>

Heston and Sacka 1155

Published online by Cambridge University Press https://doi.org/10.1002/15400001060122005/710101/01000001060122005/710101/01000001060122005

---

# Page 24

1156 Journal of Financial and Quantitative Analysis

stock returns. Table 11 addresses this statistical issue by presenting the correlations of annual strategies across countries. The short-term Year 1 annual strategy is positively correlated across almost all pairs of countries. The 95% significance level for these correlations is 0.12. The correlation reaches as high as 43% between France and Germany, and 34% between France and the United Kingdom. But many of the correlations are small and statistically insignificant. The longer-term annual strategies have lower correlations across countries, ranging

---

TABLE 11

Correlation of Annual Strategies across Countries

Each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. Table 11 reports the correlation between the monthly returns of the various trading strategies, formed based on stocks of different countries. The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom, for the period February 1985–June 2006.

<table>
  <thead>
    <tr>
      <th>Country Strategy</th>
      <th>Austria</th>
      <th>Belgium</th>
      <th>Canada</th>
      <th>Finland</th>
      <th>France</th>
      <th>Germany</th>
      <th>Italy</th>
      <th>Japan</th>
      <th>Netherlands</th>
      <th>Norway</th>
      <th>Spain</th>
      <th>Sweden</th>
      <th>Switzerland</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="14">Panel A. Year 1</td>
    </tr>
    <tr>
      <td>Belgium</td>
      <td>0.10</td>
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
      <td>Canada</td>
      <td>0.06</td>
      <td>-0.03</td>
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
      <td>Finland</td>
      <td>0.04</td>
      <td>-0.03</td>
      <td>0.19</td>
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
      <td>France</td>
      <td>0.10</td>
      <td>0.00</td>
      <td>0.20</td>
      <td>0.15</td>
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
      <td>Germany</td>
      <td>0.10</td>
      <td>0.04</td>
      <td>0.25</td>
      <td>0.19</td>
      <td>0.43</td>
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
      <td>Italy</td>
      <td>0.07</td>
      <td>0.02</td>
      <td>0.12</td>
      <td>0.12</td>
      <td>0.17</td>
      <td>0.22</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>0.04</td>
      <td>-0.10</td>
      <td>0.10</td>
      <td>0.04</td>
      <td>0.06</td>
      <td>0.18</td>
      <td>-0.01</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Netherlands</td>
      <td>0.03</td>
      <td>0.05</td>
      <td>0.02</td>
      <td>0.16</td>
      <td>0.24</td>
      <td>0.23</td>
      <td>0.16</td>
      <td>0.01</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Norway</td>
      <td>0.08</td>
      <td>0.00</td>
      <td>0.19</td>
      <td>0.02</td>
      <td>0.21</td>
      <td>0.11</td>
      <td>0.07</td>
      <td>0.09</td>
      <td>0.07</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Spain</td>
      <td>0.10</td>
      <td>0.05</td>
      <td>0.12</td>
      <td>0.23</td>
      <td>0.17</td>
      <td>0.23</td>
      <td>0.13</td>
      <td>0.01</td>
      <td>0.14</td>
      <td>0.00</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Sweden</td>
      <td>0.00</td>
      <td>-0.02</td>
      <td>0.18</td>
      <td>0.15</td>
      <td>0.23</td>
      <td>0.26</td>
      <td>0.16</td>
      <td>0.17</td>
      <td>0.06</td>
      <td>0.24</td>
      <td>0.08</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Switzerland</td>
      <td>-0.06</td>
      <td>-0.10</td>
      <td>0.19</td>
      <td>0.11</td>
      <td>0.29</td>
      <td>0.26</td>
      <td>0.19</td>
      <td>0.11</td>
      <td>0.21</td>
      <td>0.05</td>
      <td>0.26</td>
      <td>0.15</td>
      <td></td>
    </tr>
    <tr>
      <td>United Kingdom</td>
      <td>0.01</td>
      <td>0.02</td>
      <td>0.22</td>
      <td>0.27</td>
      <td>0.34</td>
      <td>0.33</td>
      <td>0.18</td>
      <td>0.08</td>
      <td>0.22</td>
      <td>0.07</td>
      <td>0.16</td>
      <td>0.33</td>
      <td>0.17</td>
    </tr>
    <tr>
      <td colspan="14">Panel B. Years 2–3</td>
    </tr>
    <tr>
      <td>Belgium</td>
      <td>0.10</td>
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
      <td>Canada</td>
      <td>0.09</td>
      <td>0.03</td>
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
      <td>Finland</td>
      <td>0.03</td>
      <td>0.05</td>
      <td>0.05</td>
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
      <td>France</td>
      <td>0.01</td>
      <td>0.09</td>
      <td>0.07</td>
      <td>0.04</td>
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
      <td>Germany</td>
      <td>-0.06</td>
      <td>0.07</td>
      <td>0.03</td>
      <td>0.01</td>
      <td>0.18</td>
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
      <td>Italy</td>
      <td>0.00</td>
      <td>0.12</td>
      <td>-0.09</td>
      <td>0.03</td>
      <td>-0.01</td>
      <td>0.02</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>0.02</td>
      <td>-0.02</td>
      <td>0.10</td>
      <td>-0.01</td>
      <td>0.02</td>
      <td>0.04</td>
      <td>-0.07</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Netherlands</td>
      <td>0.00</td>
      <td>0.17</td>
      <td>-0.03</td>
      <td>0.00</td>
      <td>0.10</td>
      <td>0.17</td>
      <td>0.13</td>
      <td>0.03</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Norway</td>
      <td>-0.03</td>
      <td>0.01</td>
      <td>0.01</td>
      <td>0.00</td>
      <td>0.06</td>
      <td>0.05</td>
      <td>0.05</td>
      <td>0.05</td>
      <td>0.09</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Spain</td>
      <td>0.09</td>
      <td>0.18</td>
      <td>-0.09</td>
      <td>0.01</td>
      <td>-0.02</td>
      <td>0.13</td>
      <td>0.03</td>
      <td>0.09</td>
      <td>0.16</td>
      <td>-0.09</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Sweden</td>
      <td>-0.07</td>
      <td>-0.06</td>
      <td>-0.05</td>
      <td>-0.01</td>
      <td>0.20</td>
      <td>0.17</td>
      <td>-0.01</td>
      <td>0.20</td>
      <td>0.04</td>
      <td>0.16</td>
      <td>0.02</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Switzerland</td>
      <td>0.09</td>
      <td>-0.03</td>
      <td>0.05</td>
      <td>-0.01</td>
      <td>0.18</td>
      <td>0.17</td>
      <td>-0.18</td>
      <td>0.09</td>
      <td>0.04</td>
      <td>-0.03</td>
      <td>0.02</td>
      <td>0.00</td>
      <td></td>
    </tr>
    <tr>
      <td>United Kingdom</td>
      <td>0.07</td>
      <td>0.05</td>
      <td>-0.02</td>
      <td>0.17</td>
      <td>0.17</td>
      <td>0.01</td>
      <td>-0.05</td>
      <td>0.05</td>
      <td>0.04</td>
      <td>0.14</td>
      <td>0.05</td>
      <td>0.08</td>
      <td>0.15</td>
    </tr>
    <tr>
      <td colspan="14">Panel C. Years 4–5</td>
    </tr>
    <tr>
      <td>Belgium</td>
      <td>-0.16</td>
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
      <td>Canada</td>
      <td>-0.01</td>
      <td>-0.03</td>
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
    </tr

---

# Page 25

Heston and Sadka 1157

from $-19\%$ (Years 4–5 annual strategy correlation between Switzerland and Austria) to $20\%$ (Years 2–3 annual strategy correlation between Sweden and France). The preponderance of statistically insignificant correlations indicates that these countries provide independent statistical evidence about the annual return premiums in stock returns. The low correlations across countries also show the potential benefits to international diversification of these annual strategies. It suggests that these strategies are not subject to pervasive international risk.

## D. Sensitivity to Deciles

To address the robustness of the decile methodology, Table 12 reports average returns to quintile and tricile strategies. The quintile and tricile spreads are returns of the top 5th or 3rd of stocks, respectively, in excess of the bottom 5th

---

**TABLE 12**

**Relative Strength Strategies: Quintiles and Triciles**

In Table 12, each month stocks are grouped into 10 portfolios (with equal number of stocks in each portfolio) based on their past performance relative to their country equal-weighted average. For example, the trading strategy that is formed based on past annual returns during Years 4–5 ranks stocks according to their average returns (excess of the country average) during the historical lags 48 and 60. The difference strategy is the annual strategy minus the nonannual strategy. The stocks in each portfolio are assigned equal weight, and the portfolios are rebalanced monthly. The average monthly returns of the various trading strategies for the period February 1985–June 2006 (257 months) are reported, as well as the corresponding $t$-statistics (2-decimal-place numbers). The analysis uses stocks from Austria, Belgium, Canada, Finland, France, Germany, Italy, Japan, Netherlands, Norway, Spain, Sweden, Switzerland, and United Kingdom.

<table>
  <thead>
    <tr>
      <th rowspan="2">Strategy</th>
      <th colspan="6">Quintiles</th>
      <th colspan="4">Triciles</th>
    </tr>
    <tr>
      <th>1 (losers)</th>
      <th>2</th>
      <th>3</th>
      <th>4</th>
      <th>5 (winners)</th>
      <th>5 – 1</th>
      <th>1 (losers)</th>
      <th>2</th>
      <th>3 (winners)</th>
      <th>3 – 1</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="11">Panel A. Year 1</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0090<br>2.44</td>
      <td>0.0096<br>3.26</td>
      <td>0.0099<br>3.62</td>
      <td>0.0115<br>4.17</td>
      <td>0.0184<br>5.41</td>
      <td>0.0094<br>4.12</td>
      <td>0.0092<br>2.75</td>
      <td>0.0099<br>3.61</td>
      <td>0.0159<br>5.13</td>
      <td>0.0067<br>3.92</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0083<br>2.38</td>
      <td>0.0106<br>3.54</td>
      <td>0.0113<br>4.08</td>
      <td>0.0120<br>4.27</td>
      <td>0.0150<br>4.72</td>
      <td>0.0067<br>4.71</td>
      <td>0.0091<br>2.78</td>
      <td>0.0114<br>4.08</td>
      <td>0.0138<br>4.60</td>
      <td>0.0047<br>3.96</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>-0.0007<br>-0.49</td>
      <td>0.0010<br>1.61</td>
      <td>0.0014<br>2.58</td>
      <td>0.0005<br>0.79</td>
      <td>-0.0034<br>-2.55</td>
      <td>-0.0027<br>-1.15</td>
      <td>-0.0001<br>-0.05</td>
      <td>0.0015<br>2.75</td>
      <td>-0.0021<br>-2.16</td>
      <td>-0.0020<br>-1.15</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0082<br>2.24</td>
      <td>0.0091<br>3.08</td>
      <td>0.0098<br>3.53</td>
      <td>0.0124<br>4.49</td>
      <td>0.0189<br>5.60</td>
      <td>0.0107<br>4.72</td>
      <td>0.0084<br>2.54</td>
      <td>0.0101<br>3.65</td>
      <td>0.0165<br>5.32</td>
      <td>0.0080<br>4.63</td>
    </tr>
    <tr>
      <td colspan="11">Panel B. Years 2–3</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0167<br>4.90</td>
      <td>0.0113<br>3.82</td>
      <td>0.0092<br>3.21</td>
      <td>0.0083<br>2.90</td>
      <td>0.0061<br>1.79</td>
      <td>-0.0106<br>-6.70</td>
      <td>0.0146<br>4.61</td>
      <td>0.0094<br>3.30</td>
      <td>0.0069<br>2.18</td>
      <td>-0.0078<br>-6.33</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0098<br>2.90</td>
      <td>0.0096<br>3.23</td>
      <td>0.0104<br>3.66</td>
      <td>0.0110<br>3.81</td>
      <td>0.0131<br>3.88</td>
      <td>0.0032<br>3.23</td>
      <td>0.0097<br>3.02</td>
      <td>0.0103<br>3.62</td>
      <td>0.0123<br>3.91</td>
      <td>0.0027<br>3.49</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>-0.0069<br>-6.82</td>
      <td>-0.0017<br>-2.27</td>
      <td>0.0012<br>2.05</td>
      <td>0.0027<br>4.88</td>
      <td>0.0070<br>5.35</td>
      <td>0.0139<br>8.10</td>
      <td>-0.0050<br>-6.04</td>
      <td>0.0009<br>1.66</td>
      <td>0.0055<br>6.08</td>
      <td>0.0104<br>7.82</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0158<br>4.65</td>
      <td>0.0111<br>3.82</td>
      <td>0.0095<br>3.25</td>
      <td>0.0086<br>3.00</td>
      <td>0.0066<br>1.92</td>
      <td>-0.0092<br>-5.82</td>
      <td>0.0141<br>4.47</td>
      <td>0.0095<br>3.30</td>
      <td>0.0073<br>2.32</td>
      <td>-0.0068<br>-5.60</td>
    </tr>
    <tr>
      <td colspan="11">Panel C. Years 4–5</td>
    </tr>
    <tr>
      <td>Nonannual</td>
      <td>0.0124<br>3.77</td>
      <td>0.0088<br>2.84</td>
      <td>0.0080<br>2.68</td>
      <td>0.0065<br>2.14</td>
      <td>0.0075<br>2.14</td>
      <td>-0.0049<br>-4.37</td>
      <td>0.0110<br>3.49</td>
      <td>0.0076<br>2.53</td>
      <td>0.0073<br>2.22</td>
      <td>-0.0037<br>-4.26</td>
    </tr>
    <tr>
      <td>Annual</td>
      <td>0.0069<br>2.06</td>
      <td>0.0072<br>2.34</td>
      <td>0.0077<br>2.66</td>
      <td>0.0090<br>2.95</td>
      <td>0.0111<br>3.26</td>
      <td>0.0043<br>4.60</td>
      <td>0.0070<br>2.19</td>
      <td>0.0076<br>2.59</td>
      <td>0.0105<br>3.23</td>
      <td>0.0035<br>5.10</td>
    </tr>
    <tr>
      <td>Difference</td>
      <td>-0.0055<br>-5.82</td>
      <td>-0.0016<br>-2.42</td>
      <td>-0.0003<br>-0.53</td>
      <td>0.0025<br>4.35</td>
      <td>0.0036<br>3.56</td>
      <td>0.0091<br>6.31</td>
      <td>-0.0040<br>-6.51</td>
      <td>0.0000<br>-0.10</td>
      <td>0.0032<br>4.44</td>
      <td>0.0072<br>6.81</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.0119<br>3.68</td>
      <td>0.0079<br>2.60</td>
      <td>0.0079<br>2.60</td>
      <td>0.0070<br>2.32</td>
      <td>0.0084<br>2.35</td>
      <td>-0.0036<br>-3.22</td>
      <td>0.0103<br>3.30</td>
      <td>0.0079<br>2.60</td>
      <td>0.0077<br>2.33</td>
      <td>-0.0026<br>-2.98</td>
    </tr>
  </tbody>
</table>

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 26

1158 Journal of Financial and Quantitative Analysis

or 3rd. The results for quintile and tricile spreads are slightly smaller than their decile spread counterparts in Table 3 but remain statistically significant. For example, Table 12 indicates that the Years 2–3 nonannual quintile spread strategy loses 106 bp per month, whereas Table 3 indicates that the Years 2–3 decile spread loses 143 bp. Meanwhile, Table 12 indicates that the corresponding tricile strategy loses only 78 bp. The Years 4–5 nonannual quintile and tricile strategies lose 49 bp and 37 bp, respectively. These Years 4–5 results are smaller than the Years 2–3 results and slightly smaller than their decile spread counterparts in Table 3, but remain statistically significant at the 95% level. The annual quintile and tricile spread strategies are all profitable. For example, the Years 2–3 annual quintile spread earns 32 bp per month, while the associated tricile strategy earns 27 bp per month. The corresponding Years 4–5 annual strategies actually earn a few bp more than the Years 2–3 strategies but are still slightly less profitable than their decile spread counterparts. All of these results are statistically significant. The return effect is not confined to a small subset of stocks and may be implementable using a broader selection of stocks.

## V. Conclusions

Behavioral patterns and empirical anomalies have a special relation to international asset pricing. International stock markets provide critical out-of-sample evidence on patterns developed with U.S. data. This solves the data-snooping problem and greatly enlarges the available data. In addition, empirical patterns can inform asset-pricing theory. If markets are integrated, then different countries should have similar returns for exposure to similar risks. But if markets are segmented, then countries may exhibit distinct patterns of returns. This makes it important to compare the structure of returns across countries.

This paper investigates whether past stock returns can predict future returns across international stocks. It confirms the short-term momentum anomaly in Canada and Europe, and its apparent absence in Japan. But it also uncovers a new long-term pattern: Stocks that outperform the market in 1 month tend to subsequently outperform the market every 12 months, while underperforming in between. This is not a country effect, because it measures country-neutral performance relative to local markets. Unlike the momentum anomaly, this pattern clearly holds in Japan in addition to Canada and 12 European countries. It lasts for up to 5 years, and annual strategies outperform nonannual strategies by over 1% per month.

This new pattern in the cross section of stock returns shows that the return process has a resemblance across different countries. The similarity overcomes data-snooping objections and suggests a common explanation. One potential economic explanation involves time-varying exposure to global risk. If equity markets have seasonal risks, or if the rewards for these risks are seasonal, then international markets may provide return premiums at annual intervals. Yet, the effect is not explained by size, $\beta$ , or value risks, and is not highly correlated across countries. This suggests that it is not due to global risk. Instead, the common pattern in stock return predictability suggests that international stock markets

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press

---

# Page 27

Heston and Sadka 1159

may be affected by similar behavioral or institutional factors across countries. In either case it provides a challenge to the development of international asset pricing theory.

# References

Asness, C. S.; J. M. Liew; and R. L. Stevens. “Parallels between the Cross-Sectional Predictability of Stock Returns and Country Returns.” Working Paper, Goldman Sachs Asset Management (1995).

Carhart, M. M.; R. Kaniel; D. K. Musto; and A. V. Reed. “Leaning for the Tape: Evidence of Gaming Behavior in Equity Mutual Funds.” *Journal of Finance*, 57 (2002), 661–693.

Chui, A. C. W.; S. Titman; and K. C. J. Wei. “Momentum, Legal Systems and Ownership Structure: An Analysis of Asian Stock Markets.” Working Paper, University of Texas (2001).

Chui, A. C. W.; S. Titman; and K. C. J. Wei. “Individualism and Momentum around the World.” *Journal of Finance*, 65 (2010), 361–392.

Comolli, L. R., and W. T. Ziemba. “Japanese Security Market Regularities, 1990–1994.” In *Security Market Imperfections in Worldwide Equity Markets*, D. B. Keim and W. T. Ziemba, eds. Cambridge, UK: Cambridge University Press (2000).

Conrad, J., and G. Kaul. “An Anatomy of Trading Strategies.” *Review of Financial Studies*, 11 (1998), 489–519.

DeBondt, W. F. M., and R. Thaler. “Does the Stock Market Overreact?” *Journal of Finance*, 40 (1985), 793–805.

DeBondt, W. F. M., and R. H. Thaler. “Further Evidence on Investor Overreaction and Stock Market Seasonality.” *Journal of Finance*, 42 (1987), 557–581.

Fama, E. *Foundations of Finance*. New York, NY: Basic Books (1976).

Fama, E. F., and K. R. French. “Common Risk Factors in the Returns on Stocks and Bonds.” *Journal of Financial Economics*, 33 (1993), 3–56.

Fama, E. F., and K. R. French. “Value versus Growth: The International Evidence.” *Journal of Finance*, 53 (1998), 1975–1999.

Griffin, J. M., and A. G. Karolyi. “Another Look at the Role of the Industrial Structure of Markets for International Diversifications Strategies.” *Journal of Financial Economics*, 50 (1998), 351–373.

Griffin, J. M.; X. Ji; and J. S. Martin. “Momentum Investing and Business Cycle Risk: Evidence from Pole to Pole.” *Journal of Finance*, 58 (2003), 2515–2547.

Hamori, S. “Seasonality and Stock Returns: Some Evidence from Japan.” *Japan and the World Economy*, 13 (2001), 463–481.

Harvey, C. R. “The World Price of Covariance Risk.” *Journal of Finance*, 46 (1991), 111–157.

Heston, S. L., and K. G. Rouwenhorst. “Does Industrial Structure Explain the Benefits of International Diversification?” *Journal of Financial Economics*, 36 (1994), 3–27.

Heston, S. L., and R. Sadka. “Seasonality in the Cross-Section of Stock Returns.” *Journal of Financial Economics*, 87 (2008), 418–445.

Hou, K.; G. A. Karolyi; and B. C. Kho. “What Factors Drive Global Stock Returns?” Working Paper, Ohio State University (2008).

Jegadeesh, N. “Evidence of Predictable Behavior of Security Returns.” *Journal of Finance*, 45 (1990), 881–898.

Jegadeesh, N., and S. Titman. “Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency.” *Journal of Finance*, 48 (1993), 65–91.

Jegadeesh, N., and S. Titman. “Profitability of Momentum Strategies: An Evaluation of Alternative Explanations.” *Journal of Finance*, 56 (2001), 699–720.

Kamstra, M. J.; L. A. Kramer; and M. D. Levi. “Winter Blues: A SAD Stock Market Cycle.” *American Economic Review*, 93 (2003), 324–343.

Karolyi, G. A.; K.-H. Lee; and M. A. van Dijk. “Commonality in Returns, Liquidity, and Turnover around the World.” Working Paper, Ohio State University (2007).

Keim, D. B. “Size-Related Anomalies and Stock Return Seasonality: Further Empirical Evidence.” *Journal of Financial Economics*, 12 (1983), 13–32.

Koh, S.-K., and K. A. Wong. “Anomalies in Asian Emerging Stock Markets.” In *Security Market Imperfections in Worldwide Equity Markets*, D. B. Keim and W. T. Ziemba, eds. Cambridge, UK: Cambridge University Press (2000).

Lehmann, B. N. “Fads, Martingales and Market Efficiency.” *Quarterly Journal of Economics*, 105 (1990), 1–28.

Liu, C., and Y. Lee. “Does the Momentum Strategy Work Universally? Evidence from the Japanese Stock Market.” *Asia-Pacific Financial Markets*, 8 (2001), 321–339.

---

# Page 28

1160 Journal of Financial and Quantitative Analysis

Lo, A. W., and A. C. MacKinlay. “Data-Snooping Biases in Tests of Financial Asset Pricing Models.” *Review of Financial Studies*, 3 (1990a), 431–467.

Lo, A. W., and A. C. MacKinlay. “When Are Contrarian Profits Due to Stock Market Overreaction?” *Review of Financial Studies*, 3 (1990b), 175–205.

Reinganum, M. R. “The Anomalous Stock Market Behavior of Small Firms in January: Empirical Tests for Tax-Loss Selling Effects.” *Journal of Financial Economics*, 12 (1983), 89–104.

Richards, A. J. “Winner-Loser Reversals in National Stock Market Indices: Can They Be Explained?” *Journal of Finance*, 52 (1996), 2129–2144.

Rouwenhorst, K. G. “International Momentum Strategies.” *Journal of Finance*, 53 (1998), 267–284.

Rozeff, M. S., and W. R. Kinney, Jr. “Capital Market Seasonality: The Case of Stock Returns.” *Journal of Financial Economics*, 3 (1976), 379–402.

Ziemba, W. T. “Japanese Security Market Regularities: Monthly, Turn-of-the-Month and Year, Holiday and Golden Week Effects.” *Japan and the World Economy*, 3 (1991), 119–146.

https://doi.org/10.1017/S0022109010000451 Published online by Cambridge University Press