# Page 1

Review of Accounting Studies (2019) 24:34–112  
https://doi.org/10.1007/s11142-018-9470-2

---

<div style="display: flex; align-items: center; gap: 10px;">
  ![image](image_1.png)
  <span>CrossMark</span>
</div>

# Quality minus junk

**Clifford S. Asness$^{1}$ · Andrea Frazzini$^{1,2}$ · Lasse Heje Pedersen$^{1,2,3,4}$**

Published online: 5 November 2018  
© The Author(s) 2018, corrected publication 2018

## Abstract

We define *quality* as characteristics that investors should be willing to pay a higher price for. Theoretically, we provide a tractable valuation model that shows how stock prices should increase in their quality characteristics: profitability, growth, and safety. Empirically, we find that high-quality stocks do have higher prices on average but not by a large margin. Perhaps because of this puzzlingly modest impact of quality on price, high-quality stocks have high risk-adjusted returns. Indeed, a quality-minus-junk (QMJ) factor that goes long high-quality stocks and shorts low-quality stocks earns significant risk-adjusted returns in the United States and across 24 countries. The price of quality varies over time, reaching a low during the internet bubble, and a low price of quality predicts a high future return of QMJ. Analysts’ price targets and earnings forecasts imply systematic quality-related errors in return and earnings expectations.

## Keywords

Quality · Valuation · Accounting variables · Profitability · Growth · Safety · Analyst forecasts

## JEL classification

D84 · G12 · G14 · G4 · M4

> When did our field stop being “asset pricing” and become “asset expected returning?” ... Market-to-book ratios should be our left-hand variable, the thing we are trying to explain, not a sorting characteristic for expected returns.
>
> — John Cochrane, Presidential Address, American Finance Association, 2011

---

**Electronic supplementary material** The online version of this article (https://doi.org/10.1007/s11142-018-9470-2) contains supplementary material, which is available to authorized users.

✉ Andrea Frazzini  
andrea.frazzini@aqr.com

Lasse Heje Pedersen  
http://www.lhpedersen.com/

1. AQR Capital Management, Two Greenwich Plaza, Greenwich, CT 06830, USA  
2. NYU, New York, NY, USA  
3. Copenhagen Business School, Frederiksberg, Denmark  
4. CEPR, London, UK

<div style="display: flex; align-items: center; gap: 5px;">
  ![image](image_2.png)
  <span>Springer</span>
</div>

---

# Page 2

Quality minus junk

35

## 1 Introduction

The asset pricing literature in accounting and financial economics studies the drivers of returns, but, while linked, the economic consequences of market efficiency ultimately depend on prices, not returns, as emphasized by Summer (1986) and Cochrane (2011). Do the highest quality firms command the highest price so that these firms can finance their operations and invest?

To address this question, we define *quality* as characteristics that investors should be willing to pay a higher price for, everything else equal, and study the price of quality, theoretically and empirically. We show that investors pay more for firms with higher quality characteristics. However, the explanatory power of quality for prices is limited, presenting a puzzle for asset pricing. This puzzle for asset *prices* is analogous to the old puzzle of the low $R^2$ of asset *returns* presented by Roll (1984, 1988). Consistent with the limited pricing of quality, high-quality stocks have delivered high risk-adjusted returns while low-quality *junk* stocks have delivered negative risk-adjusted returns. Hence, a *quality-minus-junk* (QMJ) portfolio that invests long quality stocks and shorts junk stocks produces high risk-adjusted returns. Further, we find that the price of quality (the marginal amount extra investors pay for higher quality characteristics) has varied over time, as the market has sometimes put a larger or smaller price premium on quality stocks versus junk stocks. For instance, the price of quality was particularly low during the internet bubble. Since prices and returns are linked, the price of quality predicts the future return to the QMJ factor. Lastly, we consider analyst forecast and broader asset pricing applications.

To apply our general definition of quality, we must identify stock characteristics that should command a higher price. For this, we derive a dynamic asset pricing model with time-varying growth, profitability, and risk. We show closed form how price-to-book ratios increase linearly in each of these quality characteristics. To get some intuition before we present the general model, we can rewrite Gordon’s growth model to express a stock’s price-to-book value ( $P/B$ ) as follows $^1$ :

$$
\frac{P}{B} = \frac{\text{profitability} \times \text{payout-ratio}}{\text{required-return-growth}}.
\quad (1)
$$

We scale prices by book values to make them more stationary over time and in the cross section. For instance, a food company with 10,000 restaurants likely has a price and book value that are 10 times that of another food company with only 1000 restaurants, but it is more interesting to consider which firm has the larger price-to-book (or, in this example, price per restaurant).

The three key right-hand side variables form the basis for our definition of quality. $^2$

---

$^1$ We rewrite the Gordon model simply as $\frac{P}{B} = \frac{1}{B} \frac{\text{dividend}}{\text{required-return-growth}} = \frac{\text{profit}/B \times \text{dividend}/\text{profit}}{\text{required-return-growth}}$ .

$^2$ In our more sophisticated dynamic model, payout only comes in implicitly through its effect on residual income, and, based on that model, we focus on residual income (rather than net income) and not explicitly on payout (as we did in an earlier version of this paper). Of course, the timing of dividend payouts does not matter in a frictionless economy in which Modigliani-Miller holds, but a company is more valuable if it can achieve the same stream of profits over its lifetime with a larger payout (since the present value of dividends is higher). Further, the payout (fraction of profits paid out to shareholders) can be seen as a measure of shareholder friendliness if management’s agency problems are diminished when free cash flows are reduced through higher dividends (Jensen (1986)).

$\copyright$ Springer

---

# Page 3

36

C. S. Asness et al.

i. Profitability. Profitability is the profits per unit of book value. All else equal, more profitable companies should command a higher stock price. We measure profits in several ways, including gross profits, margins, earnings, accruals, and cash flows and focus on each stock’s average rank across these metrics.

ii. Growth. Investors should also pay a higher price for stocks with growing profits. We measure growth as the prior five-year growth in each of our profitability measures.

iii. Safety. Investors should also pay, all-else-equal, a higher price for a stock with a lower required return, that is, a safer stock. What should enter into required return is still a very contentious part of the literature. We do not attempt to resolve those issues here, but rather consider both return-based measures of safety (e.g., market beta) and fundamental-based measures of safety (low volatility of profitability, low leverage, and low credit risk).

While Gordon’s growth model assumes that all variables are constant over time, it is central to our empirical analysis that price-to-book ratios and quality characteristics vary across stocks and across time. Our general model allows such time variation, showing how prices increase with quality in a dynamic setting.

For the market to rationally put a price on these quality characteristics, they need to be measured in advance and predict future quality characteristics, that is, they need to be persistent. We show that this is indeed the case; profitable, growing, and safe stocks continue on average to display these characteristics over the following 5 or 10 yrs.

We test the pricing of quality over a long sample of U.S. stocks from 1957 to 2016 and a broad sample of stocks from 24 developed markets from 1989 to 2016. To evaluate the pricing of quality, we first run cross-sectional regressions of price-to-book on each stock’s overall quality score. Both in the long and broad sample, we find that higher quality is significantly associated with higher prices. However, the explanatory power of quality on price is limited, as the average $R^2$ is only about 10% in both samples. When we also control for the firm’s size, the past 12-month stock returns, controls suggested by Pástor and Veronesi (2003), and include industry-, country-, and firm-fixed effects, the cross-sectional $R^2$ increases to a maximum of, respectively, 49 and 43%, still leaving unexplained a large fraction of the cross-sectional distribution of prices. Interestingly, larger firms are more expensive, controlling for quality, the analogue of the size effect on returns (Banz 1981; Asness et al. 2018).

We also regress the price-to-book on the three quality measures separately and in a multivariate regression. Each of the quality components has a positive marginal price, accounting for all the control variables, and having all quality measures separately modestly increases the $R^2$. Lastly, we consider the price of quality in different subsamples, finding a positive price of quality across industries and size deciles, with a somewhat larger price of quality for large stocks relative to small ones.

There could be several reasons for the limited explanatory power of quality on prices. (a) Market prices are based on superior quality characteristics than the ones we consider (e.g., an omitted variable). (b) The quality characteristics are correlated with risk factors not captured in our risk adjustments (so while the quality measure alone might command a higher price-to-book, the risk increase we fail to capture could imply an offsetting lower one). Or (c) market prices fail to fully reflect these characteristics for reasons linked to behavioral finance or constraints.

$\copyright$ Springer

---

# Page 4

Quality minus junk

37

These three hypotheses have different implications for the return of quality sorted stocks. The first does not necessarily predict that the stocks that we classify as high quality have high risk-adjusted returns. The second predicts that high-quality stocks should have low returns during distress periods or other times of high marginal utility. And the third predicts that high-quality stocks do have high risk-adjusted returns.

To examine these potential explanations, we first consider the returns of high- versus low-quality stocks. We sort stocks into 10 deciles based on their quality scores and consider the value-weighted return in each portfolio. We find that high-quality stocks have significantly higher excess returns than junk stocks. The difference in their risk-adjusted returns (i.e., four-factor alphas) is even larger since high-quality stocks tend to have lower market, size, value and momentum exposures than junk stocks.

We then construct a QMJ factor with a methodology that follows that of Fama and French (1993) and Asness and Frazzini (2013). The factor is long the top 30% high-quality stocks and short the bottom 30% junk stocks within the universe of large stocks and similarly within the universe of small stocks. This QMJ factor (as well as its large-cap only and small-cap only components) delivers positive returns in 23 out of 24 countries that we study and highly significant risk-adjusted returns in our long and broad samples. QMJ portfolios have negative market, value, and size exposures, positive alpha, relatively small residual risk, and QMJ returns are high during market downturns, presenting a challenge to risk-based explanations relying on covariance with market crises. Rather than exhibiting crash risk, if anything, QMJ exhibits a mild positive convexity, that is, it benefits from *flight to quality* during crises. In other words, the evidence challenges hypotheses (a) and (b) above, while appearing more consistent with (c).

To test (c) more directly, we examine equity analysts’ forecasts as reflected in their “target prices,” that is, the expected stock price 1 yr into the future using the methodology of Brav et al. (2005). Analysts’ target prices (scaled by book value) are higher for high-quality stocks, consistent with a positive price of quality. However, analysts’ implied return expectations (target price divided by current actual price) are lower for high-quality stocks than junk stocks, presenting a systematic error, relative to the realized returns. In other words, analysts appear to have higher target prices for high-quality stocks but not high enough on average, consistent with (c). Looking at earnings forecast errors, we find consistent results: analysts are indeed too optimistic about junk stocks (i.e., forecasted earnings are above realized earnings, on average) and much more so than about quality stocks.

To further test the link between the price and return to quality, it is interesting to exploit the time-variation in the price of quality. In particular, each month, we estimate the current price of quality as the cross-sectional regression coefficient of price-to-book on quality. The time series of these cross-sectional regression coefficients reflects how the pricing of quality varies over time. Intuitively, the price of quality reached its lowest level in February 2000, during the height of the internet bubble. The price of quality was also relatively low leading into the 1987 crash and leading into the global financial crisis of 2007–2009. Following each of these three dramatic events, the price of quality increased, reaching highs in late 1990 (first gulf war), in late 2002 (after the Enron and WorldCom scandals), and in early 2009 (at the height of the banking crisis). Prices and returns are naturally connected, and we show that the price of quality negatively predicts the future return on QMJ. Said differently, a higher price of quality is

$\mathcal{S}$ Springer

---

# Page 5

38

C. S. Asness et al.

associated with a lower return on high-quality stocks, consistent with the theory (c) that a low price of quality means that the market is inefficient in incorporating quality into prices.

We note that the QMJ strategy of buying profitable, safe, growing stocks while shorting unprofitable, risky, shrinking stocks is very different from the standard value strategy, high minus low (HML) – in fact, the two are negatively correlated. QMJ is buying and selling based on quality characteristics, *irrespective* of stock prices, while HML is buying based on stock prices, *irrespective* of quality. Naturally, the two concepts can be combined, which we call quality at a reasonable price (QARP).$^{3}$ This concept goes back at least to Graham and Dodd (1934), who stated that “investment must always consider the price as well as the quality of the security.” Naturally, value investing is improved by QARP, consistent with the finding in the accounting literature that information from financial statements can improve value investing (e.g., Frankel and Lee 1998; Piotroski 2000).

Our paper relates to a large literature. A number of papers study return-based anomalies. It has been documented that stocks with high profitability outperform (Novy-Marx 2012, 2013), stocks that repurchase tend to do well (Baker and Wurgler 2002; Pontiff and Woodgate 2008; McLean et al. 2009), low beta is associated with high alpha for stocks, bonds, credit, and futures (Black et al. 1972; Frazzini and Pedersen 2014), firms with low leverage have high alpha (George and Hwang 2010; Penman et al. 2007), firms with high credit risk tend to underperform (Altman 1968; Ohlson 1980; Campbell et al. 2008), growing firms outperform firms with poor growth (Mohanram 2005), and firms with high accruals are more likely to suffer subsequent earnings disappointments and their stocks tend to underperform peers with low accruals (Sloan 1996; Richardson et al. 2005). While these papers are very different and appear disconnected, our framework illustrates a unifying theme, namely that all these effects are about the outperformance of high-quality stocks, and we link returns and prices.

Our paper also relates to the literature that considers how the price-to-book predicts future returns and future fundamentals, based on the present-value relationship. Campbell and Shiller (1988) consider the overall market, and their dividend growth variable can be interpreted an as aggregate quality variable. Vuolteenaho (2002); Cohen et al. (2003, 2009); and Fama and French (2006) consider individual stocks. Cohen et al. (2003) decompose the cross-sectional variance of firms’ book-to-market ratios across book-to-market portfolios, and Cohen et al. (2009) consider how cash-flow betas affect price levels and long-run returns. See also the overview by Cochrane (2011) and references therein.

In summary, we complement the literature by showing (i) the theoretical price of quality in a dynamic model; (ii) how quality affects price multiples and how much of the cross-sectional variation of price multiples can be explained by quality; (iii) that the price of quality varies over time and predicts the future return on quality factors; (iv) that quality stocks earn higher returns and yet appear safer, not riskier, than junk stocks, benefiting from flight to quality; and (v) that analysts’ target prices and earnings forecast errors imply systematic quality-related errors in return and earnings expectations.

The rest of the paper is organized as follows. Section 1 presents our model. Section 2 presents our data and quality measures, showing that ex ante quality forecasts future quality (i.e., quality is sticky, as would be necessary for it to affect prices). Section 3

$^{3}$ Our definition of QARP is a generalization of the so-called growth at a reasonable price (GARP) strategy.

$\copyright$ Springer

---

# Page 6

Quality minus junk

39

analyzes the price of quality. Section 4 tests different potential explanations for the limited explanatory power of quality for price. Section 5 further asset pricing applications. Section 6 concludes. The Appendix contains a number of additional results and robustness checks.

## 2 The price of quality: dynamic model

### 2.1 A dynamic model of firm quality: time-varying profits, growth, and risk

We consider a firm in an economy with pricing kernel $M_t$ . The pricing kernel is given by $\frac{M_{t+1}}{M_t} = \frac{1}{1+r^f} \left(1 + e_{t+1}^M\right)$ , where $r^f$ is the risk-free rate and $e_{t+1}^M$ is the zero-mean innovation to the pricing kernel. For example, if the Capital Asset Pricing Model (CAPM) holds then $\varepsilon_{t+1}^M$ is linked to the return on the market portfolio, $r_{t+1}^{MKT}$ . More specifically, the CAPM pricing kernel is $e_{t+1}^M = -\lambda_t \left( \frac{r_{t+1}^{MKT} - E_t(r_{t+1}^{MKT})}{\sigma_t^2(r_{t+1}^{MKT})} \right)$ , where $\lambda_t = E_t(r_{t+1}^{MKT}) - r^f$ is the market risk premium.

The value of the firm is the present value of all future dividends, $d_t$ :

$$
V_t = \sum_{s=1}^{\infty} E_t \left( \frac{M_{t+s} d_{t+s}}{M_t} \right).
$$

We rewrite the valuation equation in terms of the book value $B_t$ and earnings (or net income) $NI_t$ by using the clean surplus relation, $B_t = B_{t-1} + NI_t - d_t$ :

$$
V_t = B_t + \sum_{s=1}^{\infty} E_t \left( \frac{M_{t+s} RI_{t+s}}{M_t} \right),
$$

where the so-called residual income, $RI_{t+s} = NI_{t+s} - r^f B_{t+s-1}$ , is the net income in excess of the cost of book capital. $^4$ We assume that the firm keeps all financial assets in risk-free securities, which implies that dividend policy and capital structure do not affect residual income. $^5$ Therefore we can specify an exogenous process for the residual income (which depends on the firm’s free cash flows from operations). Residual income consists of two components:

$$
RI_t = e_t + a_t,
$$

---

$^4$ Residual income is often defined as $NI_t - kB_{t-1}$ where $k$ is the required return on equity, but one should use the risk-free rate $r^f$ when the valuation equation is written with a pricing kernel $M_t$ (rather than a required return in the denominator). This can be seen using a simple calculation based on inserting the clean surplus relation into the valuation equation, or see the derivation in appendix and Feltham and Ohlson (1999).

$^5$ To see this result, suppose first that the firm lowers dividends by 1 at time $t$ , puts the money in risk-free securities, and increases the dividend by $(1 + r^f)^\tau$ at time $t + \tau$ . Then, at any time $t + s < t + \tau$ , the net income $NI_{t+s}$ increases by the interest income $r^f(1 + r^f)^{s-1}$ , and the book value $B_{t+s-1}$ increases by $(1 + r^f)^{s-1}$ , leaving the residual income unchanged. Second, suppose that the firm takes a loan of and invests the money in the risk-free asset at time $t$ . Then, at any time $t + s$ , the income from the risk-free asset cancels the interest payment on the loan, again leaving residual income unchanged. Other changes of dividend policy and capital structure can be seen as combinations of such actions.

$\copyright$ Springer

---

# Page 7

40

C. S. Asness et al.

where $e_t$ captures “sustainable residual income” (that is, “sustainable earnings” adjusted for the cost of book capital) and $a_t$ captures “transitory residual income shocks.” As defined precisely below, sustainable residual income is characterized by the fact that it predicts future residual income and may grow over time, whereas transitory shocks are temporary profits or losses that do not affect the long-term earnings of the firm. Specifically, sustainable residual income $e_t$ is expected to grow by $g_t$ such that

$$
e_{t+1} = e_t + g_t + \varepsilon_{t+1}^e.
$$

The zero-mean income innovation $\varepsilon_t^e$ has a risk premium $\pi_t$ due to covariation with the pricing kernel, $\pi_t = -cov_t(\varepsilon_{t+1}^e, \varepsilon_{t+1}^M)$ . We use the negative covariation such that a high risk premium corresponds to a higher required return. Under the CAPM, the risk premium is the cash flow’s standard market beta multiplied by the market risk premium $\lambda_t$ , that is,

$$
\pi_t = \lambda_t \frac{cov_t(\varepsilon_{t+1}^e, r_{t+1}^M)}{\sigma_t^2(r_{t+1}^{MKT})} = \lambda_t \beta_t^e.
$$

The growth $g_t$ and risk premium $\pi_t$ are time-varying:

$$
g_{t+1} = \varphi_g g_t + \left(1 - \varphi_g\right) \overline{g} + \varepsilon_{t+1}^g
$$

$$
\pi_{t+1} = \varphi_\pi \pi_t + (1 - \varphi_\pi) \overline{\pi} + \varepsilon_{t+1}^\pi,
$$

where $\overline{g}$ and $\overline{\pi}$ are the long-run means, $\varphi_g$ and $\varphi_\pi$ indicate the persistence of the processes, and $\varepsilon_{t+1}^g$ and $\varepsilon_{t+1}^\pi$ are zero-mean shocks that are uncorrelated to $\varepsilon_{t+1}^M$ .

The transitory residual income shock follows a moving average process and for simplicity we only consider a single lag:

$$
a_t = \varepsilon_t^a - \theta \varepsilon_{t-1}^a.
$$

We see that $\varepsilon_t^a$ captures zero-mean random shocks to residual income, and $\theta$ measures dependence on past shocks. The transitory income does not grow over time, and a positive shock is even expected to be partly reversed in the next period if $\theta > 0$ . For example, aggressive accounting accruals can lead to such reversals in earnings. $^6$

## 2.2 Valuation: the price of quality

To compute the fundamental value, we first compute the conditional expectation of the sustainable residual income $e_{t+1}$ for the next period:

$$
E_t\left(\frac{M_{t+1}}{M_t} e_{t+1}\right) = E_t\left(\frac{1}{1 + r^f} \left(1 + \varepsilon_{t+1}^M\right) \left(e_t + g_t + \varepsilon_{t+1}^e\right)\right) = \frac{1}{1 + r^f} \left(e_t + g_t - \pi_t\right).
$$

---

$^6$ Accrual accounting is a method to measure profits at the time when an economic activity happens, rather than when cash is paid or received. Accruals can be used to make reported earnings capture true profits better than pure cash-based measures, but accruals can also be used to artificially boost earnings. For example, see Richardson et al. (2005), who find that “less reliable accruals lead to lower earnings persistence.”

$\copyright$ Springer

---

# Page 8

Quality minus junk

41

We can iterate this result to show that the value of sustainable income $\tau$ periods into the future is

$$
E_t \left( \frac{M_{t+\tau}}{M_t} e_{t+\tau} \right) = \frac{1}{(1 + r^f)^\tau} \left( e_t + \sum_{n=1}^\tau E_t (g_{t+n} - \pi_{t+n}) \right)
$$

$$
= \frac{1}{(1 + r^f)^\tau} \left( e_t + \sum_{n=1}^\tau \left( \varphi_g^n g_t + \left(1 - \varphi_g^n\right) \bar{g} - \varphi_\pi^n \pi_t - \left(1 - \varphi_\pi^n\right) \bar{\pi} \right) \right)
$$

$$
= \frac{1}{(1 + r^f)^\tau} \left( e_t + \frac{\varphi_g - \varphi_g^{\tau+1}}{1 - \varphi_g} (g_t - \bar{g}) + \tau \bar{g} - \frac{\varphi_\pi - \varphi_\pi^{\tau+1}}{1 - \varphi_\pi} (\pi_t - \bar{\pi}) - \tau \bar{\pi} \right).
$$

Based on this result, we can next compute the fundamental value as the sum of the book value and all future discounted residual incomes $^7$ :

$$
V_t = B_t + v^e e_t + v - v^a \varepsilon_t^a + v^g \left( g_t - \bar{g} \right) - v^\pi \left( \pi_t - \bar{\pi} \right),
$$

where the valuation coefficients are $v = \frac{1 + r_f}{r_f} (\bar{g} - \bar{\pi})$ , $v^e = \frac{1}{r_f}$ , $v^g = \frac{\varphi_g (1 + r_f)}{r_f (1 + r_f - \varphi_g)}$ , $v^\pi = \frac{\varphi_\pi (1 + r_f)}{r_f (1 + r_f - \varphi_\pi)}$ , and $v^a = \frac{\theta}{1 + r_f}$ . The fundamental value can be written as a fraction of book value $B_t$ :

$$
\frac{V_t}{B_t} = 1 + \underbrace{\frac{v^e e_t + v - v^a \varepsilon_t^a}{B_t}}_{\text{scaled value}} + \underbrace{v^g \frac{g_t - \bar{g}}{B_t}}_{\text{profitability (adjusted for accruals)}} + \underbrace{-v^\pi \frac{\pi_t - \bar{\pi}}{B_t}}_{\text{growth}}.
\quad (2)
$$

This specification motivates our empirical work. In particular, we see that the ratio of fundamental value to book value increases in the current residual earnings adjusted for accruals divided by book (which we call profitability), $^8$ it increases in the growth of sustainable profits, and it increases in safety (i.e., it decreases in market risk $\pi_t$ ). Further, we see that the valuation is linear in these values.

## 3 Data, quality measures, and preliminary analysis

### 3.1 Data sources

The data is collected from a variety of sources. Our sample consists of 54,616 stocks covering 24 countries between June 1957 and December 2016. The 24 markets in our

---

$^7$ We are using the standard results that $\sum_{\tau=1}^\infty z^\tau = \frac{1}{1-z}$ and $\sum_{\tau=1}^\infty \tau z^\tau = \frac{z}{(1-z)^3}$ .

$^8$ Note that there may be two reasons to adjust for transitory earnings shocks. First, if $\theta > 0$ , then $v^a > 0$ , leading to the adjustment shown in the valuation equation. Second, if we start with net income $NI_t$ , then sustainable earnings $e_t$ is net income adjusted transitory shocks (and cost of capital), $e_t = NI_t - a_t - r^f B_{t-1}$ .

$\copyright$ Springer

---

# Page 9

42

C. S. Asness et al.

sample correspond to union of all countries belonging to the MSCI World Developed Index over our sample period. We report summary statistics in Table 10 in the Appendix. Stock returns and accounting data are from the union of the Center for Research on Security Prices (CRSP) pricing database, the Compustat North America Fundamentals Annual, Fundamentals Quarterly and Security Daily databases, the Compustat Global Fundamentals Annual, Fundamentals Quarterly, and Security Daily databases. All returns are in U.S. dollars. They do not include any currency hedging, and they are measured as excess returns above the U.S. Treasury bill rate.$^{9}$ We follow the standard convention (Fama and French (1992) and align accounting variables at the end of the firm’s fiscal year ending anywhere in calendar year $t-1$ to June of calendar year $t$. We focus on a *long sample* of U.S. stocks and a *broad sample* of global stocks.

Our *long sample* of U.S. data includes all available common stocks on the merged CRSP/Compustat North America data.$^{10}$ Our default primary source for pricing information is Compustat, supplemented with CRSP over the earlier period when Compustat pricing data is not available. Table 10 in the Appendix reports details on the data sources for each period. The first available date for our regressions and return tests is June 1957.$^{11}$

Our *broad sample* includes all available common stocks on the union of the CRSP, the Compustat North America and the Compustat Global database for 24 developed markets. We assign individual issues to the corresponding market based on the location of the primary exchange. For companies traded in multiple markets, we use the primary trading vehicle identified by Compustat. The first available date for our regressions and return test is June 1989. Table 10 reports date coverage of the individual markets.

Target prices are from the Thomson Reuters I/B/E/S global database, which contains the projected price level forecasted by analysts within a specific time horizon. For our analysis, we use the monthly mean and median consensus target prices. I/B/E/S computes consensus prices are over a 12-month time horizon. Earnings forecast errors are also from Thomson Reuters. Every month, we compute the actual EPS earnings for the next fiscal year minus the I/B/E/S consensus forecasts, deflated by the stock price.

## 3.2 Quality score

To avoid data mining, we base our measures on our theoretical model implemented using standard off-the-shelf empirical measures to compute three composite quality measures: *profitability*, *growth*, and *safety*. We then average these three quality components to compute a single overall quality score. Our results are qualitatively robust to the specific choices of factors.

The theory suggests that profitability should be measured as the “sustainable” part of profits in relation to book value, adjusted for accruals, which we implement empirically by averaging several measures of profitability to reduce noise (hopefully leaving the more sustainable part) and avoiding focusing on a particular measure. Our empirical exercise is focused on cross-sectional comparisons of firms sorted by their overall

---

$^{9}$ We include delisting returns when available. If a firm is delisted but the delisting return is missing and the delisting is performance related, we follow Shumway (1997) and assume a $-30\%$ delisting return.

$^{10}$ Common stocks are identified by a CRSP share code (SHRCD) of 10 or 11 or by a Compustat issue code (TPCI) of 0. We also drop stocks traded on over-the-counter (OTC) exchanges.

$^{11}$ Our tests require at least a five-year history as some of our variables are five-year growth measures.

$\copyright$ Springer

---

# Page 10

Quality minus junk

43

quality scores as well as the three quality components. When comparing firms’ profitability, note that there is no difference between comparing their residual-income-to-book versus net-income-to-book, since these only differ by the common risk-free rate, $RI_t/B_{t-1} = NI_t/B_{t-1} - r^f$ .

Second, theory suggests that growth should be the increase in sustainable profits in relation to book values. Since profits are noisy, we use a five-year window to focus on sustainable growth, and, again based on our model, accruals are not included in the growth measure. When computing growth measures, using residual income, rather than net income, does matter. $^{12}$ Further, to account for issuance, we consider all variables on a per-share basis. That is, we compute the value to a buy-and-hold investor who does not participate in issuances. $^{13}$

More specifically, our quality measures are constructed as follows (details are in the Appendix). We measure profitability as gross profits over assets (GPOA), return on equity (ROE), return on assets (ROA), cash flow over assets (CFOA), gross margin (GMAR), and the fraction of earnings composed of cash (i.e., minus accruals, ACC). To put each measure on equal footing and combine them, each month we convert each variable into ranks and standardize to obtain a $z$ -score. More formally, let $x$ be the variable of interest and $r$ be the vector of ranks, $r_i = rank(x_i)$ . Then the $z$ -score of the ranks of $x$ is given by $z(x) = z_x = (r - \mu_r)/\sigma_r$ , where $\mu_r$ and $\sigma_r$ are the cross-sectional mean and standard deviation of $r$ . Our Profitability score is the average of the individual $z$ -scores:

$$
Profitability = z(z_{gpoa} + z_{roe} + z_{roa} + z_{cfoa} + z_{gmar} + z_{acc}).
\quad (3)
$$

Similarly, we measure growth as the five-year growth in residual per-share profitability measures (excluding accruals), averaged across five measures. Letting $\Delta$ denote the five-year change in each measure of residual income per share, divided by the lagged denominator (e.g., assets per share), we have:

$$
Growth = z(z_{\Delta gpoa} + z_{\Delta roe} + z_{\Delta roa} + z_{\Delta cfoa} + z_{\Delta gmar}).
\quad (4)
$$

Further, we define safe securities as companies with low beta (BAB), low leverage (LEV), low bankruptcy risk (O-Score and Z-Score), and low ROE volatility (EVOL):

$$
Safety = z(z_{bab} + z_{lev} + z_o + z_z + z_{evol})
\quad (5)
$$

Finally, we combine the three measures into a single quality score:

$$
Quality = z(Profitability + Growth + Safety).
\quad (6)
$$

---

$^{12}$ Growth in residual income increases in the growth in net income and decreases in asset growth, all else equal:

$$
\frac{RI_t - RI_{t-5}}{B_{t-5}} = \frac{NI_t - NI_{t-5}}{B_{t-5}} - r^f \frac{B_{t-1} - B_{t-6}}{B_{t-5}}.
$$

For example, consider two firms that are equally profitable in terms of $NI_t$ and $NI_{t-5}$ and have the same starting book value $B_{t-5}$ . Further, suppose that firm X pays out all of the profits to shareholders such that its book value stays constant, $B_t = B_{t-5}$ , while firm Y keeps all profits in the firm such that its book value increases $B_t >> B_{t-5}$ . Then it is more impressive that firm X can deliver the same NI today, since firm Y should have generated some net income from the retained earnings.

$^{13}$ The appendix considers a version of QMJ where payout is as a separate factor.

$\copyright$ Springer

---

# Page 11

44

C. S. Asness et al.

To construct our composite quality measure as well as the individual subcomponents, we use all available information: if a particular measure is missing due lack of data availability, we simply average the remaining ones. We also consider a number of robustness tests, for example, using raw values rather than the ranks.

## 3.3 Portfolios

Our portfolio analysis relies on two sets of test factors: quality-sorted portfolios and quality-minus-junk factors (hereafter, QMJ factors). For both, we form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization.

To form quality-sorted portfolios, at the end of each calendar month, we assign stocks in each country to 10 quality-sorted portfolios. U.S. sorts are based on NYSE breakpoints. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights.

The QMJ portfolio construction follows Fama and French (1993) and Asness and Frazzini (2013). QMJ factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, we assign stocks to two size-sorted portfolios, based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. $^{14}$ We use conditional sorts, first sorting on size and then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios:

$$
QMJ = \frac{1}{2} (Small\ Quality + Big\ Quality) - \frac{1}{2} (Small\ Junk + Big\ Junk)
$$

$$
= \frac{1}{2} \underbrace{(Small\ Quality - Small\ Junk)}_{QMJ\ in\ small\ stocks} + \frac{1}{2} \underbrace{(Big\ Quality - Big\ Junk)}_{QMJ\ in\ big\ stocks}.
\quad (7)
$$

Portfolios based on profitability, growth and safety are constructed in a similar manner. We compute alphas with respect to a domestic and a global four-factor model. The explanatory variables are the market (MKT), size (small-minus-big, SMB), book-to-market (high-minus-low, HML), and momentum (up-minus-down, UMD) portfolios. We report a more detailed description in the Appendix. $^{15}$ In some of our tests, we also use the Fama and French (2015) five-factor model, based on the market factor (MKT), size (small-minus-big, SMB), book-to-market (high-minus-low, HML), profitability (robust-minus-weak, RMW), and an investment factor (conservative-minus-aggressive, CMA). $^{16}$

---

$^{14}$ In our sample, the 80th size percentile by country corresponds approximately to NYSE breakpoints.

$^{15}$ The data can be downloaded at https://www.aqr.com/library/data-sets.

$^{16}$ The data can be downloaded at http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

$\copyright$ Springer

---

# Page 12

Quality minus junk

45

## 3.4 Ex ante quality forecasts fundamentals

We start by showing that a stock’s quality is persistent. That is, by selecting companies that were profitable, growing, and safe in the recent past, we succeed in selecting companies that display these characteristics in the future. This step is important when we turn to the central analysis of whether the high-quality firms command higher prices since, in a forward-looking rational market, prices should be related to *future* quality characteristics. Of course, predictability of quality is perfectly consistent with an efficient market—market efficiency says only that, since prices should reflect quality, *stock returns* should be unpredictable (or only predictable due to risk premia), not that quality itself should be unpredictable.

Table 1 analyzes the predictability of quality as follows. Each month, we sort stocks into 10 portfolios by their quality scores (as defined in Section 2). The table reports the value-weighted average of our quality measures across stocks in each of the portfolios. The table shows these average quality scores both at the time of the portfolio formation (time $t$ ) and in the subsequent 10 yrs ( $t + 120$ months). The standard errors are adjusted for heteroskedasticity and autocorrelation with a lag length of 5 yrs (Newey and West (1987)). By construction, the quality scores vary monotonically across portfolios at the time of portfolio formation, so the interesting part of the table is the future quality scores. Table 1 shows that, on average, high-quality firms today remain high-quality firms five and 10 yrs into the future (conditional on survival) and we can reject the null hypothesis of no difference in each of quality characteristics up to 10 yrs. Table 11 in the Appendix reports additional results: we sort firms separately using each component of our quality score (profitability, growth, and safety) and report the spread in each variable up to 10 yrs, yielding similarly consistent results.

To summarize, quality is a persistent characteristic such that high quality today predicts future high quality. For both the U.S. long and global sample, profitability is the most persistent, and, while still surprisingly stable, growth and safety are the least persistent.

## 4 The price of quality

Given that future quality can be forecasted, we now turn to the central question of how quality affects prices: do high-quality stocks command higher prices than low-quality ones?

### 4.1 The price of quality in the United States and globally

To address this question, we run a cross-sectional regression of each stock $i$ ’s log market-to-book ( $MB$ ) ratio on its overall quality score, $Quality_t^i$ (defined in Section 2). Specifically, we let $P_t^i = log(MB)_t^i$ and run the regression:

$$
P_t^i = a + b \, Quality_t^i + controls + \varepsilon_t^i.
\quad (8)
$$

Market-to-book is defined as book equity divided by the current market equity of the firm in June of year $t$ . This regression tests whether high quality is associated with high prices in the cross section. Using ranked $z$ -scores as our explanatory variable limits the effect of outliers and implies that the regression coefficient $b$ has a simple

$\copyright$ Springer

---

# Page 13

46

C. S. Asness et al.

Table 1 Persistence of quality measures

<table>
  <thead>
    <tr>
      <th></th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
      <th>H-L t-stat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Panel A: Long Sample (U.S.), 6/1975–12/2016</td>
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
      <td>Quality</td>
      <td>t</td>
      <td>-1.44</td>
      <td>-0.83</td>
      <td>-0.53</td>
      <td>-0.29</td>
      <td>-0.07</td>
      <td>0.15</td>
      <td>0.38</td>
      <td>0.65</td>
      <td>0.99</td>
      <td>1.64</td>
      <td>3.07</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 12 M</td>
      <td>-0.86</td>
      <td>-0.51</td>
      <td>-0.33</td>
      <td>-0.20</td>
      <td>-0.01</td>
      <td>0.16</td>
      <td>0.36</td>
      <td>0.54</td>
      <td>0.83</td>
      <td>1.46</td>
      <td>2.34</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 36 M</td>
      <td>-0.50</td>
      <td>-0.32</td>
      <td>-0.23</td>
      <td>-0.16</td>
      <td>-0.02</td>
      <td>0.11</td>
      <td>0.23</td>
      <td>0.41</td>
      <td>0.65</td>
      <td>1.22</td>
      <td>1.73</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 60 M</td>
      <td>-0.23</td>
      <td>-0.17</td>
      <td>-0.14</td>
      <td>-0.12</td>
      <td>-0.04</td>
      <td>0.06</td>
      <td>0.18</td>
      <td>0.31</td>
      <td>0.52</td>
      <td>1.07</td>
      <td>1.31</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 120 M</td>
      <td>-0.23</td>
      <td>-0.18</td>
      <td>-0.14</td>
      <td>-0.09</td>
      <td>-0.04</td>
      <td>0.07</td>
      <td>0.16</td>
      <td>0.33</td>
      <td>0.48</td>
      <td>0.91</td>
      <td>1.14</td>
    </tr>
    <tr>
      <td>Profit</td>
      <td>t + 120 M</td>
      <td>-0.37</td>
      <td>-0.23</td>
      <td>-0.12</td>
      <td>-0.02</td>
      <td>0.10</td>
      <td>0.13</td>
      <td>0.26</td>
      <td>0.33</td>
      <td>0.53</td>
      <td>1.08</td>
      <td>1.47</td>
    </tr>
    <tr>
      <td>Growth</td>
      <td>t + 120 M</td>
      <td>-0.15</td>
      <td>-0.11</td>
      <td>-0.13</td>
      <td>-0.11</td>
      <td>-0.13</td>
      <td>-0.08</td>
      <td>-0.05</td>
      <td>0.02</td>
      <td>0.23</td>
      <td>0.41</td>
      <td>0.56</td>
    </tr>
    <tr>
      <td>Safety</td>
      <td>t + 120 M</td>
      <td>-0.43</td>
      <td>-0.27</td>
      <td>-0.14</td>
      <td>-0.04</td>
      <td>0.04</td>
      <td>0.13</td>
      <td>0.23</td>
      <td>0.37</td>
      <td>0.60</td>
      <td>0.75</td>
      <td>1.18</td>
    </tr>
    <tr>
      <td>Panel B: Broad Sample (Global), 6/1989–12/2016</td>
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
      <td>Quality</td>
      <td>t</td>
      <td>-1.63</td>
      <td>-0.91</td>
      <td>-0.57</td>
      <td>-0.31</td>
      <td>-0.08</td>
      <td>0.15</td>
      <td>0.39</td>
      <td>0.66</td>
      <td>1.01</td>
      <td>1.59</td>
      <td>3.22</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 12 M</td>
      <td>-1.16</td>
      <td>-0.60</td>
      <td>-0.38</td>
      <td>-0.20</td>
      <td>-0.03</td>
      <td>0.13</td>
      <td>0.32</td>
      <td>0.52</td>
      <td>0.82</td>
      <td>1.34</td>
      <td>2.50</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 36 M</td>
      <td>-0.81</td>
      <td>-0.43</td>
      <td>-0.28</td>
      <td>-0.17</td>
      <td>-0.04</td>
      <td>0.07</td>
      <td>0.22</td>
      <td>0.39</td>
      <td>0.63</td>
      <td>1.07</td>
      <td>1.88</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 60 M</td>
      <td>-0.53</td>
      <td>-0.24</td>
      <td>-0.17</td>
      <td>-0.12</td>
      <td>-0.03</td>
      <td>0.03</td>
      <td>0.15</td>
      <td>0.29</td>
      <td>0.47</td>
      <td>0.86</td>
      <td>1.39</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>t + 120 M</td>
      <td>-0.41</td>
      <td>-0.22</td>
      <td>-0.13</td>
      <td>-0.05</td>
      <td>0.00</td>
      <td>0.05</td>
      <td>0.13</td>
      <td>0.26</td>
      <td>0.42</td>
      <td>0.65</td>
      <td>1.06</td>
    </tr>
    <tr>
      <td>Profit</td>
      <td>t + 120 M</td>
      <td>-0.29</td>
      <td>-0.14</td>
      <td>-0.03</td>
      <td>0.05</td>
      <td>0.16</td>
      <td>0.18</td>
      <td>0.29</td>
      <td>0.37</td>
      <td>0.52</td>
      <td>0.93</td>
      <td>1.23</td>
    </tr>
    <tr>
      <td>Growth</td>
      <td>t + 120 M</td>
      <td>-0.12</td>
      <td>-0.06</td>
      <td>-0.10</td>
      <td>-0.08</td>
      <td>-0.05</td>
      <td>-0.05</td>
      <td>-0.06</td>
      <td>0.03</td>
      <td>0.15</td>
      <td>0.21</td>
      <td>0.32</td>
    </tr>
    <tr>
      <td>Safety</td>
      <td>t + 120 M</td>
      <td>-0.51</td>
      <td>-0.34</td>
      <td>-0.21</td>
      <td>-0.12</td>
      <td>-0.01</td>
      <td>0.04</td>
      <td>0.15</td>
      <td>0.30</td>
      <td>0.46</td>
      <td>0.57</td>
      <td>1.08</td>
    </tr>
  </tbody>
</table>


This table shows average quality scores. Each calendar month, stocks in each country in are ranked in ascending order on the basis of their quality score. The ranked stocks are assigned to one of 10 portfolios. U.S. sorts are based on NYSE breakpoints. This table reports each portfolio’s quality score at portfolio formation (date t) up to the subsequent 10 years (date t + 120 months). We report the time series average of the value-weighted cross-sectional means. Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1989 to December 2016. Standard errors are adjusted for heteroskedasticity and autocorrelation with a lag length of 5 yrs (Newey and West 1987), and 5% significance is indicated in bold

Springer

---

# Page 14

Quality minus junk

47

interpretation: $b$ measures the percentage increase (log changes) in market-to-book associated to a one standard deviation increase in our quality score.$^{17}$ We include several control variables motivated by theory as discussed below.

Panel A of Table 2 reports results of Fama and MacBeth (1973) regressions of prices on quality. In June of each year, we regress scaled prices on quality measures, and we report time series averages of the cross-sectional slope estimates. Standard errors are adjusted for heteroskedasticity and autocorrelation (Newey and West 1987) with a lag length of 5 yrs. We run the regression with and without industry-, country-, or firm-fixed effects, as indicated.

We see that the price of quality $b$ is generally positive and highly statistically significant: high-quality firms do command higher (scaled) prices. Indeed, the price of quality is positive both in the U.S. and global samples and across specifications with controls and fixed effects. The univariate estimated price of quality in the long domestic (broad global) sample is 0.22 (0.17). This coefficient implied that a one standard deviation change in a stock’s quality score is associated (in the cross section) with a 22% (17%) increase in its price-to-book.

While theory does not provide specific guidance on what the $R^2$ should be, the explanatory power of quality on price appears limited. Quality alone explains only about 9% of the cross-sectional variation in prices in both our U.S. and global sample.

We also include several controls. With the exception of dummy variables, we measure each of these controls as the z-score of their cross-sectional rank for consistency and ease of interpretation of the coefficients. First, we control for size, motivated by the theory that large stocks are more liquid and have less liquidity risk than small firms and thus higher prices and lower required returns (Amihud and Mendelson 1986; Pástor and Stambaugh 2003; Acharya and Pedersen 2005). Consistent with this theory, we see that larger firms do have higher prices, controlling for quality. This result is the analogue of the size effect on returns (Banz 1981; also Berk 1995), expressed in terms of prices. That is, big firms, even for the same quality, are more expensive, possibly leading to the return effect observed by Banz.

Motivated by the theory of learning about profitability by Pástor and Veronesi (2003), we also control for age, profit uncertainty, and a dividend payer dummy, as defined as in their paper. Firm age is the cumulative number of years since the firm’s IPO. Profit uncertainty is the standard deviation of the residuals of an AR(1) model for each firm’s ROE, using the longest continuous series of a firm’s valid annual ROE up to June of each year. Dividend payer is a dummy equal to one if the firm paid any dividends over the prior year. Consistent with Pástor and Veronesi (2003), we find that prices are lower for firms that pay dividends, decrease in age, and increase in profit uncertainly, especially for firms that pay no dividends.

We also control for past stock returns. Including past returns is necessary since our sample include firms with fiscal year-ends up to 11 months apart. (Accounting variables at the end of the firm’s fiscal year ending anywhere in calendar year $t-1$ are aligned to June of calendar year $t$.) A positive coefficient on past returns simply reflects that high recent returns raise current prices while the book value has not had time to adjust. Consistent with this observation, Table 2 shows that, ceteris paribus, stocks with higher stock returns tend to have higher scaled prices.

---

$^{17}$ Using the z-score of the market-to-book on the left hand side as opposed to logs or computing ordinal z-scores by dropping the rank step from the z-score construction does not significantly impact any of the results. For brevity, we do not report these additional results.

$\text{Springer}$

---

# Page 15

48

C. S. Asness et al.

Table 2 The price of quality: cross sectional regressions, results: cross sectional regressions, the price of quality

<table>
  <thead>
    <tr>
      <th>Panel A</th>
      <th>Long Sample (U.S., 6/1975 – 12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>Broad Sample (Global, 6/1989–12/2016)</th>
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
      <td>(1)</td>
      <td>(2)</td>
      <td>(3)</td>
      <td>(4)</td>
      <td>(5)</td>
      <td>(6)</td>
      <td>(7)</td>
      <td>(8)</td>
      <td>(9)</td>
      <td>(10)</td>
      <td>(11)</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>0.22</td>
      <td>0.24</td>
      <td>0.24</td>
      <td>0.22</td>
      <td>0.22</td>
      <td>0.24</td>
      <td>0.17</td>
      <td>0.20</td>
      <td>0.17</td>
      <td>0.17</td>
      <td>0.17</td>
    </tr>
    <tr>
      <td></td>
      <td>(10.07)</td>
      <td>(20.92)</td>
      <td>(10.06)</td>
      <td>(11.78)</td>
      <td>(10.07)</td>
      <td>(20.92)</td>
      <td>(14.06)</td>
      <td>(26.38)</td>
      <td>(13.59)</td>
      <td>(20.67)</td>
      <td>(14.06)</td>
    </tr>
    <tr>
      <td>Firm size</td>
      <td></td>
      <td>0.34</td>
      <td></td>
      <td>0.33</td>
      <td></td>
      <td>0.34</td>
      <td></td>
      <td>0.34</td>
      <td></td>
      <td>0.33</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(20.92)</td>
      <td></td>
      <td>(18.87)</td>
      <td></td>
      <td>(20.92)</td>
      <td></td>
      <td>(12.81)</td>
      <td></td>
      <td>(12.49)</td>
      <td></td>
    </tr>
    <tr>
      <td>1-year return</td>
      <td></td>
      <td>0.21</td>
      <td></td>
      <td>0.21</td>
      <td></td>
      <td>0.21</td>
      <td></td>
      <td>0.26</td>
      <td></td>
      <td>0.26</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(12.59)</td>
      <td></td>
      <td>(12.39)</td>
      <td></td>
      <td>(12.59)</td>
      <td></td>
      <td>(24.04)</td>
      <td></td>
      <td>(27.48)</td>
      <td></td>
    </tr>
    <tr>
      <td>Firm age</td>
      <td></td>
      <td>−0.18</td>
      <td></td>
      <td>−0.17</td>
      <td></td>
      <td>−0.18</td>
      <td></td>
      <td>−0.12</td>
      <td></td>
      <td>−0.11</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−7.60)</td>
      <td></td>
      <td>(−6.81)</td>
      <td></td>
      <td>(−7.60)</td>
      <td></td>
      <td>(−5.23)</td>
      <td></td>
      <td>(−4.92)</td>
      <td></td>
    </tr>
    <tr>
      <td>Profit Uncertainty</td>
      <td></td>
      <td>0.38</td>
      <td></td>
      <td>0.35</td>
      <td></td>
      <td>0.38</td>
      <td></td>
      <td>0.41</td>
      <td></td>
      <td>0.35</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(15.54)</td>
      <td></td>
      <td>(15.15)</td>
      <td></td>
      <td>(15.54)</td>
      <td></td>
      <td>(28.36)</td>
      <td></td>
      <td>(19.92)</td>
      <td></td>
    </tr>
    <tr>
      <td>Dividend payer</td>
      <td></td>
      <td>−0.16</td>
      <td></td>
      <td>−0.07</td>
      <td></td>
      <td>−0.16</td>
      <td></td>
      <td>−0.20</td>
      <td></td>
      <td>−0.10</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−7.68)</td>
      <td></td>
      <td>(−3.50)</td>
      <td></td>
      <td>(−7.68)</td>
      <td></td>
      <td>(−6.64)</td>
      <td></td>
      <td>(−2.93)</td>
      <td></td>
    </tr>
    <tr>
      <td>Profit Uncertainty x Dividend payer</td>
      <td></td>
      <td>−0.20</td>
      <td></td>
      <td>−0.20</td>
      <td></td>
      <td>−0.20</td>
      <td></td>
      <td>−0.22</td>
      <td></td>
      <td>−0.20</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−10.88)</td>
      <td></td>
      <td>(−7.78)</td>
      <td></td>
      <td>(−10.88)</td>
      <td></td>
      <td>(−15.13)</td>
      <td></td>
      <td>(−8.05)</td>
      <td></td>
    </tr>
    <tr>
      <td>Average AdjR2</td>
      <td></td>
      <td>0.09</td>
      <td></td>
      <td>0.26</td>
      <td></td>
      <td>0.09</td>
      <td></td>
      <td>0.41</td>
      <td></td>
      <td>0.20</td>
      <td></td>
    </tr>
    <tr>
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
      <td>Nobs (years)</td>
      <td></td>
      <td>60</td>
      <td></td>
      <td>54</td>
      <td></td>
      <td>60</td>
      <td></td>
      <td>54</td>
      <td></td>
      <td>28</td>
      <td></td>
    </tr>
    <tr>
      <td>Industry FE</td>
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
      <td>Country FE</td>
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
      <td>Firm FE</td>
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
      <td>Panel B</td>
      <td>Long Sample (U.S., 6/1975 – 12/2016)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Broad Sample (Global, 6/1989 – 12/2016)</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(1)</td>
      <td>(2)</td>
      <td>(3)</td>
      <td>(4)</td>
      <td>(5)</td>
      <td>(6)</td>
      <td>(7)</td>
      <td>(8)</td>
      <td>(9)</td>
      <td>(10)</td>
      <td>(11)</td>
    </tr>
    <tr>
      <td>Profitability</td>
      <td>0.19</td>
      <td></td>
      <td></td>
      <td>0.11</td>
      <td>0.14</td>
      <td>0.13</td>
      <td></td>
      <td></td>
      <td>0.06</td>
      <td>0.08</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(10.31)</td>
      <td></td>
      <td></td>
      <td>(6.65)</td>
      <td>(9.67)</td>
      <td>(19.74)</td>
      <td></td>
      <td></td>
      <td>(8.75)</td>
      <td>(11.68)</td>
      <td></td>
    </tr>
    <tr>
      <td>Growth</td>
      <td></td>
      <td>0.18</td>
      <td></td>
      <td>0.12</td>
      <td>0.13</td>
      <td></td>
      <td>0.14</td>
      <td></td>
      <td>0.11</td>
      <td>0.13</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(12.37)</td>
      <td></td>
      <td>(14.73)</td>
      <td>(24.76)</td>
      <td></td>
      <td>(20.23)</td>
      <td></td>
      <td>(13.33)</td>
      <td>(22.76)</td>
      <td></td>
    </tr>
    <tr>
      <td>Safety</td>
      <td></td>
      <td></td>
      <td>0.13</td>
      <td>0.04</td>
      <td>0.02</td>
      <td></td>
      <td></td>
      <td>0.10</td>
      <td>0.04</td>
      <td>0.04</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td>(8.23)</td>
      <td>(3.69)</td>
      <td>(2.17)</td>
      <td></td>
      <td></td>
      <td>(9.89)</td>
      <td>(3.86)</td>
      <td>(3.05)</td>
      <td></td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 16

Quality minus junk

49

Table 2 (continued)

<table>
  <thead>
    <tr>
      <th>Firm size</th>
      <th>0.34</th>
      <th>0.33</th>
      <th>0.38</th>
      <th>0.33</th>
      <th>0.32</th>
      <th>0.33</th>
      <th>0.33</th>
      <th>0.36</th>
      <th>0.33</th>
      <th>0.31</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>(17.42)</td>
      <td>(19.28)</td>
      <td>(22.79)</td>
      <td>(18.36)</td>
      <td>(18.56)</td>
      <td>(11.82)</td>
      <td>(12.56)</td>
      <td>(14.23)</td>
      <td>(11.90)</td>
      <td>(9.94)</td>
    </tr>
    <tr>
      <td>1-year return</td>
      <td>0.22</td>
      <td>0.22</td>
      <td>0.23</td>
      <td>0.21</td>
      <td>0.21</td>
      <td>0.27</td>
      <td>0.27</td>
      <td>0.27</td>
      <td>0.26</td>
      <td>0.26</td>
    </tr>
    <tr>
      <td></td>
      <td>(12.42)</td>
      <td>(11.89)</td>
      <td>(13.58)</td>
      <td>(11.87)</td>
      <td>(11.99)</td>
      <td>(26.44)</td>
      <td>(26.13)</td>
      <td>(28.28)</td>
      <td>(28.17)</td>
      <td>(24.70)</td>
    </tr>
    <tr>
      <td>Firm age</td>
      <td>-0.18</td>
      <td>-0.16</td>
      <td>-0.20</td>
      <td>-0.17</td>
      <td>-0.18</td>
      <td>-0.12</td>
      <td>-0.11</td>
      <td>-0.12</td>
      <td>-0.11</td>
      <td>-0.14</td>
    </tr>
    <tr>
      <td></td>
      <td>(-6.79)</td>
      <td>(-6.30)</td>
      <td>(-7.07)</td>
      <td>(-7.04)</td>
      <td>(-7.41)</td>
      <td>(-4.84)</td>
      <td>(-4.30)</td>
      <td>(-5.14)</td>
      <td>(-4.96)</td>
      <td>(-6.77)</td>
    </tr>
    <tr>
      <td>Profit Uncertainty</td>
      <td>0.31</td>
      <td>0.31</td>
      <td>0.36</td>
      <td>0.33</td>
      <td>0.35</td>
      <td>0.32</td>
      <td>0.31</td>
      <td>0.35</td>
      <td>0.34</td>
      <td>0.39</td>
    </tr>
    <tr>
      <td></td>
      <td>(11.48)</td>
      <td>(13.33)</td>
      <td>(12.68)</td>
      <td>(14.27)</td>
      <td>(13.53)</td>
      <td>(17.53)</td>
      <td>(16.24)</td>
      <td>(23.77)</td>
      <td>(23.32)</td>
      <td>(36.38)</td>
    </tr>
    <tr>
      <td>Dividend payer</td>
      <td>-0.08</td>
      <td>-0.01</td>
      <td>-0.06</td>
      <td>-0.06</td>
      <td>-0.13</td>
      <td>-0.10</td>
      <td>-0.05</td>
      <td>-0.09</td>
      <td>-0.08</td>
      <td>-0.17</td>
    </tr>
    <tr>
      <td></td>
      <td>(-3.77)</td>
      <td>(-0.55)</td>
      <td>(-2.80)</td>
      <td>(-3.18)</td>
      <td>(-6.31)</td>
      <td>(-3.08)</td>
      <td>(-1.61)</td>
      <td>(-2.76)</td>
      <td>(-2.64)</td>
      <td>(-4.30)</td>
    </tr>
    <tr>
      <td>Profit Uncertainty x Dividend payer</td>
      <td>-0.19</td>
      <td>-0.21</td>
      <td>-0.20</td>
      <td>-0.21</td>
      <td>-0.20</td>
      <td>-0.20</td>
      <td>-0.20</td>
      <td>-0.20</td>
      <td>-0.20</td>
      <td>-0.23</td>
    </tr>
    <tr>
      <td></td>
      <td>(-6.52)</td>
      <td>(-8.02)</td>
      <td>(-6.27)</td>
      <td>(-8.13)</td>
      <td>(-10.93)</td>
      <td>(-8.03)</td>
      <td>(-7.40)</td>
      <td>(-8.10)</td>
      <td>(-8.31)</td>
      <td>(-13.63)</td>
    </tr>
    <tr>
      <td>Average AdjR2</td>
      <td>0.48</td>
      <td>0.48</td>
      <td>0.45</td>
      <td>0.50</td>
      <td>0.43</td>
      <td>0.42</td>
      <td>0.43</td>
      <td>0.42</td>
      <td>0.44</td>
      <td>0.35</td>
    </tr>
    <tr>
      <td>Nobs (years)</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>28</td>
      <td>28</td>
      <td>28</td>
      <td>28</td>
      <td>28</td>
    </tr>
    <tr>
      <td>Industry FE</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>X</td>
      <td></td>
    </tr>
    <tr>
      <td>Country FE</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>X</td>
      <td></td>
    </tr>
    <tr>
      <td>Firm FE</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>X</td>
      <td>X</td>
    </tr>
  </tbody>
</table>


This table reports results from annual Fama-Macbeth regressions. The dependent variable is the log of a firm’s market-to-book ratio in June of each calendar year (date t). The explanatory variables are the quality scores on date t and a series of controls. “Firm size” is the log of the firm’s market capitalization; “one-year return” is the firm’s stock return over the prior year. “Firm age” is the cumulative number of years since the firm’s IPO. “Uncertainty about mean profitability” (Pástor and Veronesi 2003) is the standard deviation of the residuals of an AR(1) model for each firm’s ROE, using the longest continuous series of a firm’s valid annual ROE up to date t. We require a minimum of 5 yrs of nonmissing ROEs. “Dividend payer” is a dummy equal to one if the firm paid any dividends over the prior year. With the exception of the “Dividend payer” dummy, all explanatory variables at time t are ranked cross-sectionally and rescaled to have a zero cross-sectional mean and a cross-sectional standard deviation of one. Industry, country, or firm fixed effects are included when indicated (“Industry FE,” “Country FE,” “Firm FE”). “Average AdjR2” is the time series average of the adjusted R-squared of the cross-sectional regression. Standard errors are adjusted for heteroskedasticity and autocorrelation (Newey and West 1987) with a lag length of 5 yrs. T-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold

Springer

---

# Page 17

50

C. S. Asness et al.

Finally, we also consider industry-, country-, and firm-fixed effects. We see that the $R^2$ increases markedly with these controls. Nevertheless, the coefficient on quality is relatively immune to the inclusion of these controls, and its statistical significance actually increases. The maximum $R^2$ across all these specifications is 49%, leaving the majority of cross-sectional variation on prices unexplained.

## 4.2 The price of quality sub-components

Panel B of Table 2 considers cross-sectional regressions on each separate quality score, univariately and multivariately:

$$
P_t^i = a + b^1 bProfitability_t^i + b^2 Growth_t^i + b^3 Safety_t^i + controls + e_t^i. \quad (9)
$$

We see that prices of profitability, growth and safety are positive throughout, controlling for each other and our other control variables and fixed effects. In other words, high-quality stocks tend to have relatively higher prices than low-quality stocks. The maximum $R^2$ reaches 48% in the United States and 42% in the global sample, still leaving a large part of the cross section of prices unexplained.

## 4.3 The price of quality across subsets of stocks

The Appendix contains further robustness tests. Table 12 reports results from monthly regressions, where market-to-book follows the convention of Asness and Frazzini (2013), defined as book equity divided by the current market equity of the firm each month. Figure 6 report results by industry. This figure plots t-statistics of the quality coefficients from annual Fama-Macbeth regressions within 71 GICS industries, using our full set of controls. All the results tell a consistent story: high-quality firms tend to command higher prices.

Table 12 also reports the price of quality by size decile. In particular, we run regression (8) for each subsample of stocks sorted by size. We see that the results are consistent across size groups, both in the United States and globally. Also note that the average $R^2$ rises across decile size, reaching 72% (56%) for U.S. (global) firms in the top size deciles. Although for the median firm the vast majority of cross-sectional variation on prices remains unexplained, over the largest firms, quality does explain a significant amount of cross-sectional dispersion in (scaled) prices.

To summarize, our results are consistent with the hypothesis that high-quality firms command higher (scaled) prices. However, the explanatory power of quality is limited, leaving a large amount of variation in prices unexplained. Our results appear robust to specification and not driven by effects related to small stocks or by a particular industry or geography.

## 5 Understanding the price of quality: the return of quality stocks

We would like to shed light on our finding that quality explains prices only to a limited extent: is this finding because (a) the market uses superior quality measures (and, if we observed these measures, they would strongly relate to prices) or, in some cases, reverse causality; (b) quality is linked to risk in a way not captured by our safety

$\copyright$ Springer

---

# Page 18

Quality minus junk

51

measure; or (c) limited market efficiency. Explanation (c) implies that high-quality stocks have higher risk-adjusted returns than low-quality stocks, as market prices fail to fully reflect the quality characteristics. Explanation (b) implies a univariate relation between quality and future returns, which is reduced or eliminated by an effective risk model. And explanation (a) means that the relation between our measured quality and ex post returns is attenuated, noisy, or potentially biased—in the simplest form, this explanation means that quality should be unrelated to risk-adjusted returns. Hence, to try to explain the limited relation between price and quality, we need to analyze the future returns of quality stocks. $^{18}$

## 5.1 The returns of quality-sorted portfolios

Table 3 reports the returns of stocks sorted into 10 deciles based on their quality score. The table reports both excess returns over T-bills and alphas with respect to the CAPM one-factor model; the Fama and French (1993) three-factor model, which includes the size factor SMB and the value factor HML, in addition to the market factor MKT; and the four-factor model, which includes the momentum factor UMD (Jegadeesh and Titman 1993; Asness 1994; Carhart 1997). Specifically, these alphas are the intercepts from the following regression with the first one, three, or four right-hand-side variables included:

$$
r_t = \alpha + \beta^{MKT} MKT_t + \beta^{SMB} SMB_t + \beta^{HML} HML_t + \beta^{UMD} UMD_t + \varepsilon_t. \quad (10)
$$

We see that excess returns increase almost monotonically in quality such that high-quality stocks outperform low-quality stocks. The right-most column reports the return difference between the highest and lowest deciles and the associated $t$ -statistic, showing that high-quality stocks earn higher average returns than low quality stocks (42 and 52 basis points per month depending on the sample), and we can reject the null hypothesis of no difference in average returns ( $t$ -statistics of 2.56 and 2.49).

When we control for market risk and other factor exposures, the outperformance in the alpha of high-quality stocks and their statistical significance is in fact even larger. This higher outperformance arises because high-quality stocks actually have lower market exposures and lower exposures to other factors than low-quality stocks. In other words, as measured by the CAPM or a three- and four-factor model, high-quality stocks are safer (have lower factor loadings) than low-quality stocks. Adjusting by the CAPM alone materially strengthens our results, as higher-quality stocks are, partly by construction, lower beta stocks. Across our three risk models in our long U.S. sample, a portfolio that is long high-quality stocks and short low-quality stocks earns average abnormal returns ranging from 64 to 105 basis points per month with associated $t$ -statistics ranging between 4.26 and 9.31. In our broad global sample, we obtain similar results with abnormal returns between 71 to 99 basis points and $t$ -statistics between 4.05 and 6.67.

Our results are thus consistent with explanation (c) discussed above but do not appear to support the simplest versions of explanations (a) and (b). Indeed, a simple risk

---

$^{18}$ Table A2 Panel C shows the results of regressing future quality on the current price-to-book as well as a number of control variables. The small positive coefficient shows that market prices do have some predictive power for future quality, consistent with a rational explanation. However, we still need to consider future risk-adjusted returns to fully test the rational theory.

$\copyright$ Springer

---

# Page 19

52

C. S. Asness et al.

Table 3 Quality-sorted portfolios

<table>
  <thead>
    <tr>
      <th></th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Panel A: Long Sample U.S., 7/1957 – 12/2016**</td>
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
      <td>Excess return</td>
      <td>0.28 (1.09)</td>
      <td>0.43 (2.10)</td>
      <td>0.43 (2.29)</td>
      <td>0.51 (2.88)</td>
      <td>0.55 (3.14)</td>
      <td>0.53 (3.18)</td>
      <td>0.48 (2.94)</td>
      <td>0.62 (3.71)</td>
      <td>0.52 (3.11)</td>
      <td>0.70 (4.11)</td>
      <td>0.42 (2.56)</td>
    </tr>
    <tr>
      <td>CAPM alpha</td>
      <td>−0.44 (−3.72)</td>
      <td>−0.17 (−2.29)</td>
      <td>−0.13 (−1.94)</td>
      <td>−0.02 (−0.29)</td>
      <td>0.03 (0.55)</td>
      <td>0.03 (0.60)</td>
      <td>−0.01 (−0.19)</td>
      <td>0.12 (2.36)</td>
      <td>0.01 (0.28)</td>
      <td>0.20 (3.11)</td>
      <td>0.64 (4.26)</td>
    </tr>
    <tr>
      <td>3-factor alpha</td>
      <td>−0.57 (−6.52)</td>
      <td>−0.28 (−4.45)</td>
      <td>−0.21 (−3.68)</td>
      <td>−0.10 (−1.89)</td>
      <td>−0.03 (−0.60)</td>
      <td>−0.02 (−0.41)</td>
      <td>−0.02 (−0.39)</td>
      <td>0.10 (1.99)</td>
      <td>0.05 (1.01)</td>
      <td>0.31 (5.90)</td>
      <td>0.88 (8.23)</td>
    </tr>
    <tr>
      <td>4-factor alpha</td>
      <td>−0.59 (−6.30)</td>
      <td>−0.39 (−5.90)</td>
      <td>−0.28 (−4.56)</td>
      <td>−0.19 (−3.58)</td>
      <td>−0.11 (−1.91)</td>
      <td>−0.12 (−2.41)</td>
      <td>−0.10 (−1.79)</td>
      <td>0.11 (2.10)</td>
      <td>0.07 (1.55)</td>
      <td>0.46 (8.59)</td>
      <td>1.05 (9.31)</td>
    </tr>
    <tr>
      <td>Beta</td>
      <td>1.28</td>
      <td>1.16</td>
      <td>1.10</td>
      <td>1.06</td>
      <td>1.04</td>
      <td>1.00</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.92</td>
      <td>−0.36</td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.14</td>
      <td>0.27</td>
      <td>0.30</td>
      <td>0.37</td>
      <td>0.41</td>
      <td>0.41</td>
      <td>0.38</td>
      <td>0.48</td>
      <td>0.40</td>
      <td>0.53</td>
      <td>0.33</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>−0.88</td>
      <td>−0.83</td>
      <td>−0.64</td>
      <td>−0.50</td>
      <td>−0.27</td>
      <td>−0.34</td>
      <td>−0.25</td>
      <td>0.29</td>
      <td>0.22</td>
      <td>1.20</td>
      <td>1.31</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>0.88</td>
      <td>0.91</td>
      <td>0.92</td>
      <td>0.90</td>
      <td>0.92</td>
      <td>0.91</td>
      <td>0.91</td>
      <td>0.93</td>
      <td>0.91</td>
      <td>0.59</td>
      <td>0.59</td>
    </tr>
    <tr>
      <td>**Panel B: Broad Sample Global, 7/1998 – 12/2016**</td>
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
      <td>Excess return</td>
      <td>0.11 (0.32)</td>
      <td>0.33 (1.11)</td>
      <td>0.39 (1.43)</td>
      <td>0.46 (1.81)</td>
      <td>0.46 (1.88)</td>
      <td>0.46 (1.99)</td>
      <td>0.57 (2.52)</td>
      <td>0.59 (2.65)</td>
      <td>0.55 (2.45)</td>
      <td>0.63 (2.80)</td>
      <td>0.52 (2.49)</td>
    </tr>
    <tr>
      <td>CAPM alpha</td>
      <td>−0.41 (−2.50)</td>
      <td>−0.13 (−1.01)</td>
      <td>−0.03 (−0.31)</td>
      <td>0.06 (0.64)</td>
      <td>0.08 (0.84)</td>
      <td>0.10 (1.11)</td>
      <td>0.21 (2.57)</td>
      <td>0.25 (2.76)</td>
      <td>0.20 (2.21)</td>
      <td>0.29 (2.76)</td>
      <td>0.71 (4.05)</td>
    </tr>
    <tr>
      <td>3-factor alpha</td>
      <td>−0.51 (−3.40)</td>
      <td>−0.21 (−1.84)</td>
      <td>−0.11 (−1.06)</td>
      <td>0.01 (0.10)</td>
      <td>0.01 (0.07)</td>
      <td>0.04 (0.45)</td>
      <td>0.19 (2.34)</td>
      <td>0.23 (2.56)</td>
      <td>0.25 (2.72)</td>
      <td>0.40 (4.20)</td>
      <td>0.91 (6.66)</td>
    </tr>
    <tr>
      <td>4-factor alpha</td>
      <td>−0.43</td>
      <td>−0.27</td>
      <td>−0.17</td>
      <td>−0.06</td>
      <td>−0.05</td>
      <td>−0.04</td>
      <td>0.11</td>
      <td>0.19</td>
      <td>0.27</td>
      <td>0.56</td>
      <td>0.99</td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 20

Quality minus junk

53

Table 3 (continued)

<table>
  <thead>
    <tr>
      <th></th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Beta</td>
      <td>(−2.63)</td>
      <td>(−2.16)</td>
      <td>(−1.60)</td>
      <td>(−0.62)</td>
      <td>(−0.57)</td>
      <td>(−0.43)</td>
      <td>(1.20)</td>
      <td>(1.93)</td>
      <td>(2.73)</td>
      <td>(5.57)</td>
      <td>(6.67)</td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>1.20</td>
      <td>1.08</td>
      <td>1.02</td>
      <td>0.97</td>
      <td>0.92</td>
      <td>0.89</td>
      <td>0.87</td>
      <td>0.85</td>
      <td>0.83</td>
      <td>0.79</td>
      <td>−0.41</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>0.06</td>
      <td>0.21</td>
      <td>0.27</td>
      <td>0.34</td>
      <td>0.36</td>
      <td>0.38</td>
      <td>0.48</td>
      <td>0.51</td>
      <td>0.47</td>
      <td>0.53</td>
      <td>0.47</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>−0.55</td>
      <td>−0.45</td>
      <td>−0.34</td>
      <td>−0.13</td>
      <td>−0.12</td>
      <td>−0.09</td>
      <td>0.25</td>
      <td>0.40</td>
      <td>0.57</td>
      <td>1.17</td>
      <td>1.40</td>
    </tr>
    <tr>
      <td></td>
      <td>0.82</td>
      <td>0.85</td>
      <td>0.87</td>
      <td>0.86</td>
      <td>0.88</td>
      <td>0.87</td>
      <td>0.87</td>
      <td>0.84</td>
      <td>0.84</td>
      <td>0.84</td>
      <td>0.58</td>
    </tr>
  </tbody>
</table>


This table shows calendar-time portfolio returns. Each calendar month, stocks in each country in are ranked in ascending order on the basis of their quality score. The ranked stocks are assigned to one of 10 portfolios. U.S. sorts are based on NYSE breakpoints. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. The rightmost column reports returns of a self-financing portfolio that is long the high quality portfolio and short the low quality portfolio. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage. t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Beta” is the realized loading on the market portfolio. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized

Springer

---

# Page 21

54

C. S. Asness et al.

explanation (b) is inconsistent with our finding that high-quality stocks have lower factor exposures than junk stocks, but we study risk in more detail by considering the performance of the QMJ factor.

## 5.2 Quality minus junk

In this section, we examine the returns of our QMJ factors. As described in Section 2 (Eq. 7), QMJ is long the average of the *Small Quality* and *Big Quality* portfolios and short the average of the *Small Junk* and *Big Junk* portfolios. We also construct long/short factors based on each separate quality component using the same method. Hence, in addition to QMJ, we have quality factors based on profitability, safety, and growth.

Table 13 reports the correlations between the different quality components. The table reports the correlation both for the excess returns and for the abnormal returns relative to a four-factor model (i.e., the correlations of the regression residuals). We see that all of the pairwise correlations among the quality components are positive. The average pairwise correlation among the quality components is 0.67 in the United States and 0.64 in the global sample and 0.59 and 0.57 for abnormal returns in the two samples. Hence, while the quality components measure different firm characteristics that investors should be willing to pay for, firms that are high quality in one respect tend to also be high quality in others. This did not have to be. Each of these variables, we argue, is a quality measure investors should pay for at the margin, but the measures did not have to be related to one another. While theory is no guide here, we think these significant positive correlations lend support to our practical decision to combine these three thematic sets of measures as one quality variable.

Table 4 reports the performance of each of our quality factors in the United States (panel A) and globally (panel B). Specifically, the table reports the average excess returns and the alphas with respect to the CAPM, three-, and four-factor models. We see that each quality factor delivers a statistically significant positive excess return and alpha with respect to the CAPM, three-, and four-factor models in the U.S. sample and significant four-factor alphas in the global sample as well (the three- and four-factor results are quite similar as momentum, or UMD, does not change much). The overall QMJ factor tends to be the strongest of the three, with highly significant alphas in the United States and global samples. The abnormal returns are large in magnitude and highly statistically significant. In our U.S. long sample, a QMJ portfolio that is long high-quality stocks and short junk stocks delivers CAPM, three-, and four-factor abnormal returns of 39, 51, and 60 basis points per month (with corresponding $t$-statistics of 5.43, 8.90, and 9.95). Similarly, in our global broad sample, the QMJ factor earns abnormal returns of 51, 61 and 61 basis points per month (with corresponding $t$-statistics of 5.76, 8.75, and 8.07).

Panels A and B of Table 4 also report the risk-factor loadings for the four-factor model. We see that the QMJ factor (with the exception of the UMD loading in the global sample) has significant negative factor exposures, that is, according to four-factor model, quality stocks are in general safer than junk stocks yet surprisingly earn higher (not lower) average returns. QMJ has a significantly negative market and size exposures. That is, QMJ is long low-beta and large stocks, while being short high-beta small ones. As would be expected, the safety factor has the most negative market exposure, though only growth attains a zero

$\copyright$ Springer

---

# Page 22

Quality minus junk

55

Table 4 Quality minus junk: returns

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="4">Panel A: Long Sample<br>(U.S., 7/1957 – 12/2016)</th>
      <th colspan="4">Panel B: Broad Sample<br>(Global, 7/1998 – 12/2016)</th>
    </tr>
    <tr>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess Returns</td>
      <td>0.29<br>(3.62)</td>
      <td>0.25<br>(3.69)</td>
      <td>0.23<br>(2.44)</td>
      <td>0.17<br>(2.46)</td>
      <td>0.38<br>(3.33)</td>
      <td>0.39<br>(4.34)</td>
      <td>0.23<br>(1.72)</td>
      <td>0.15<br>(1.96)</td>
    </tr>
    <tr>
      <td>CAPM-alpha</td>
      <td>0.39<br>(5.43)</td>
      <td>0.32<br>(4.75)</td>
      <td>0.40<br>(5.52)</td>
      <td>0.16<br>(2.28)</td>
      <td>0.51<br>(5.76)</td>
      <td>0.48<br>(6.88)</td>
      <td>0.40<br>(4.49)</td>
      <td>0.16<br>(2.05)</td>
    </tr>
    <tr>
      <td>3-factor alpha</td>
      <td>0.51<br>(8.90)</td>
      <td>0.40<br>(6.97)</td>
      <td>0.52<br>(9.06)</td>
      <td>0.28<br>(5.17)</td>
      <td>0.61<br>(8.75)</td>
      <td>0.51<br>(8.11)</td>
      <td>0.51<br>(7.91)</td>
      <td>0.24<br>(3.63)</td>
    </tr>
    <tr>
      <td>4-factor alpha</td>
      <td>0.60<br>(9.95)</td>
      <td>0.50<br>(8.32)</td>
      <td>0.51<br>(8.39)</td>
      <td>0.46<br>(8.29)</td>
      <td>0.61<br>(8.07)</td>
      <td>0.47<br>(6.89)</td>
      <td>0.39<br>(5.73)</td>
      <td>0.40<br>(5.78)</td>
    </tr>
    <tr>
      <td>MKT</td>
      <td>−0.20<br>(−14.35)</td>
      <td>−0.12<br>(−8.47)</td>
      <td>−0.32<br>(−22.30)</td>
      <td>−0.04<br>(−2.81)</td>
      <td>−0.27<br>(−15.78)</td>
      <td>−0.19<br>(−12.73)</td>
      <td>−0.35<br>(−22.74)</td>
      <td>−0.03<br>(−2.06)</td>
    </tr>
    <tr>
      <td>SMB</td>
      <td>−0.26<br>(−11.92)</td>
      <td>−0.22<br>(−10.01)</td>
      <td>−0.30<br>(−13.55)</td>
      <td>−0.04<br>(−1.76)</td>
      <td>−0.32<br>(−8.71)</td>
      <td>−0.28<br>(−8.32)</td>
      <td>−0.23<br>(−6.79)</td>
      <td>−0.12<br>(−3.56)</td>
    </tr>
    <tr>
      <td>HML</td>
      <td>−0.37<br>(−15.85)</td>
      <td>−0.29<br>(−12.57)</td>
      <td>−0.28<br>(−11.91)</td>
      <td>−0.49<br>(−23.09)</td>
      <td>−0.30<br>(−8.59)</td>
      <td>−0.06<br>(−1.83)</td>
      <td>−0.25<br>(−7.98)</td>
      <td>−0.38<br>(−12.17)</td>
    </tr>
    <tr>
      <td>UMD</td>
      <td>−0.09<br>(−4.34)</td>
      <td>−0.10<br>(−4.87)</td>
      <td>0.01<br>(0.32)</td>
      <td>−0.16<br>(−9.17)</td>
      <td>0.00<br>(−0.02)</td>
      <td>0.04<br>(1.56)</td>
      <td>0.11<br>(4.63)</td>
      <td>−0.14<br>(−5.86)</td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.47</td>
      <td>0.48</td>
      <td>0.32</td>
      <td>0.32</td>
      <td>0.64</td>
      <td>0.83</td>
      <td>0.33</td>
      <td>0.37</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>1.40</td>
      <td>1.17</td>
      <td>1.18</td>
      <td>1.16</td>
      <td>1.70</td>
      <td>1.45</td>
      <td>1.21</td>
      <td>1.22</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>0.50</td>
      <td>0.34</td>
      <td>0.62</td>
      <td>0.46</td>
      <td>0.65</td>
      <td>0.52</td>
      <td>0.78</td>
      <td>0.34</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized

or small positive market beta. The other quality composites also show negative beta. The value exposure of QMJ is negative in the United States and globally. This negative value loading is expected since high-quality stocks have high prices while the value factor HML is long cheap stocks. The loadings on UMD

Springer

---

# Page 23

56

C. S. Asness et al.

tend to be smaller in magnitude and statistically insignificant in some the specifications. The loadings are consistent across quality sub-components, with profitability, safety, and growth all having negative market, SMB, and HML loadings in the U.S. and global samples.

Figure 1 and Table 16 report the performance of the QMJ factor across countries. Remarkably, the QMJ factor delivers positive returns and alphas in all but one of the 24 countries that we study, displaying a strikingly consistent pattern (with the only small negative in our sample being in New Zealand, one of the smallest countries in market capitalization and number of stocks). Furthermore four-factors alphas are statistically significant in 18 out of 24 countries, despite the fact that many individual countries have a small cross section of securities and a short time series.

Fig. 2 shows the performance of the QMJ factor over time in the U.S. and global samples. Specifically, Fig. 2 shows the cumulative sum of QMJ’s four-factor risk-adjusted returns (the sum of the monthly in-sample regression alpha plus the regression error), illustrating that QMJ factor has consistently delivered positive risk-adjusted returns over time with no particular subsample driving our results. Figs. 7 and 8 in the Appendix plot, respectively, the raw excess returns over time (i.e., without risk adjustments) and the four-factor alphas by year.

![image](image_1.png)

Fig. 1 QMJ: 4-Factor Adjusted Information Ratios. This figure plots four-factor adjusted information ratios of quality minus junk (QMJ) factors. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Information ratios are equal to the intercept of a time-series regression of monthly excess return divided by the standard deviation of the estimated residuals. The explanatory variables are the monthly returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Information ratios are annualized

Springer

---

# Page 24

Quality minus junk

57

## A: Long Sample (U.S., 1957 - 2016)

![image](image_1.png)

## B: Broad Sample (Global, 1986 - 2012)

![image](image_2.png)

**Fig. 2** QMJ: Cumulative Four-Factor Alphas. This figure shows four-factor adjusted cumulative returns of quality minus junk (QMJ) factors. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1989 to December 2016. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the monthly returns of the market, (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. We plot the cumulative abnormal returns (alpha plus regression residual) from the time-series regression

$\text{Springer}$

---

# Page 25

58

C. S. Asness et al.

## 5.3 Robustness of QMJ performance

Table 5 reports the performance of our quality factors using alternative risk-adjustments. Specifically, we report alphas relative to the five-factor model of Fama and French (2015) and the six-factor model augmented with the (UMD) momentum portfolio.$^{19}$ While using this six-factor adjustment reduces the magnitude of the abnormal returns, the results are consistent with prior ones: QMJ portfolios earn significant returns, controlling for the five- or six-factor models. We note that QMJ portfolios have large positive loading on the RMW factor based on gross profit over assets (GPOA), which is not surprising given that GPOA is a component out our profitability composite. Nevertheless, alphas are positive, ranging from 16 to 38 basis points per month, and most of them are significant. Said differently, RMW is a quality factor, so we are measuring the return of quality broadly defined, controlling for a narrow quality measure and other factors.

Furthermore, factor loadings to the market, size, and value remain negative, indicating that high-quality stocks are safer than junk stocks in terms of these risk exposures (while CMA, RMW, and UMD have less clear interpretations as risk).

We report a series of additional results and robustness checks in the Appendix. Table 14 reports returns for the individual components (small quality, big quality, small junk, big junk) of the QMJ factors. In Table 15, we split the sample in 20-year subsamples and report QMJ returns by size (10 size-sorted based on NYSE-breakpoints). Figure 9 report results for large- and small-cap stocks within each country. Table 17 reports QMJ abnormal returns controlling for the four-factor model augmented with the betting against beta (BAB) factor of Frazzini and Pedersen (2014). Table 18 reports QMJ abnormal returns controlling for the six-factor model plus BAB. Finally, Fig. 10 reports results by industry using 71 global GICS industries. We form a QMJ portfolio within each industry and report four-factor adjusted information ratios.

All the results point in the same direction with consistency across size, time periods, countries, and construction methodology: QMJ portfolios that are long high-quality stocks and short junk stocks earn large and significant abnormal returns, relative to variety of factor models, ranging from one- to seven-factor models. Furthermore, quality stocks do not appear riskier (as defined by model loadings); if anything, they appear safer than junk stocks and, as a result, earn abnormal returns that are larger than their excess returns.

The return evidence on the QMJ factors could be consistent with both mispricing (quality stocks are underpriced and junk stocks are overpriced) or risk (quality stocks underperform junk stocks in bad states of the world) that is not fully captured by the factor models considered above. Although a full explanation of the driver of quality returns is beyond the scope of this paper, we can nonetheless provide some stylized facts that either explanation should generate to fit the available evidence.

---

$^{19}$ The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), profitability (RMW), and investment (CMA) portfolios from Fama and French (2015) and the momentum (UMD) portfolio. All the portfolios are from Ken’s French data library. The shorter sample period (July 1963 to December 2016 for the U.S. sample and November 1990 to December 2016 for the global sample) is due to the slightly shorter availability of the data on Ken’s French data library, relative to our sample.

$\copyright$ Springer

---

# Page 26

Quality minus junk

59

Table 5 Quality minus junk: six-factor adjusted returns

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="4">Panel A: Long Sample<br>(U.S.,7/1963–12/2016)</th>
      <th colspan="4">Panel B: Broad Sample<br>(Global, 11/1990–12/2016)</th>
    </tr>
    <tr>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess Returns</td>
      <td>0.29<br>(3.30)</td>
      <td>0.29<br>(3.92)</td>
      <td>0.20<br>(2.04)</td>
      <td>0.15<br>(2.02)</td>
      <td>0.32<br>(2.70)</td>
      <td>0.37<br>(4.07)</td>
      <td>0.19<br>(1.36)</td>
      <td>0.12<br>(1.51)</td>
    </tr>
    <tr>
      <td>5-factor alpha</td>
      <td>0.38<br>(7.71)</td>
      <td>0.29<br>(6.85)</td>
      <td>0.38<br>(5.75)</td>
      <td>0.30<br>(6.60)</td>
      <td>0.33<br>(5.06)</td>
      <td>0.29<br>(5.83)</td>
      <td>0.27<br>(3.48)</td>
      <td>0.19<br>(3.34)</td>
    </tr>
    <tr>
      <td>6-factor alpha</td>
      <td>0.33<br>(6.81)</td>
      <td>0.28<br>(6.54)</td>
      <td>0.29<br>(4.49)</td>
      <td>0.27<br>(5.85)</td>
      <td>0.28<br>(4.46)</td>
      <td>0.28<br>(5.58)</td>
      <td>0.16<br>(2.42)</td>
      <td>0.18<br>(3.12)</td>
    </tr>
    <tr>
      <td>MKT</td>
      <td>−0.17<br>(−14.07)</td>
      <td>−0.08<br>(−7.72)</td>
      <td>−0.28<br>(−17.60)</td>
      <td>−0.05<br>(−4.47)</td>
      <td>−0.24<br>(−13.92)</td>
      <td>−0.15<br>(−10.84)</td>
      <td>−0.32<br>(−17.79)</td>
      <td>−0.06<br>(−3.84)</td>
    </tr>
    <tr>
      <td>SMB</td>
      <td>−0.11<br>(−6.51)</td>
      <td>−0.07<br>(−4.57)</td>
      <td>−0.19<br>(−8.89)</td>
      <td>0.03<br>(1.83)</td>
      <td>−0.17<br>(−5.41)</td>
      <td>−0.17<br>(−6.84)</td>
      <td>−0.17<br>(−5.03)</td>
      <td>−0.08<br>(−2.61)</td>
    </tr>
    <tr>
      <td>HML</td>
      <td>−0.26<br>(−10.85)</td>
      <td>−0.29<br>(−13.80)</td>
      <td>−0.19<br>(−6.26)</td>
      <td>−0.26<br>(−11.88)</td>
      <td>−0.25<br>(−6.42)</td>
      <td>−0.10<br>(−3.05)</td>
      <td>−0.25<br>(−6.10)</td>
      <td>−0.11<br>(−2.93)</td>
    </tr>
    <tr>
      <td>CMA</td>
      <td>−0.05<br>(−1.39)</td>
      <td>0.09<br>(3.04)</td>
      <td>0.04<br>(0.97)</td>
      <td>−0.36<br>(−11.46)</td>
      <td>0.05<br>(0.99)</td>
      <td>0.06<br>(1.57)</td>
      <td>0.13<br>(2.54)</td>
      <td>−0.41<br>(−9.10)</td>
    </tr>
    <tr>
      <td>RMW</td>
      <td>0.55<br>(24.07)</td>
      <td>0.58<br>(28.37)</td>
      <td>0.32<br>(10.67)</td>
      <td>0.33<br>(15.70)</td>
      <td>0.65<br>(13.63)</td>
      <td>0.59<br>(15.49)</td>
      <td>0.46<br>(9.28)</td>
      <td>0.32<br>(7.24)</td>
    </tr>
    <tr>
      <td>UMD</td>
      <td>0.07<br>(5.68)</td>
      <td>0.01<br>(1.25)</td>
      <td>0.13<br>(8.87)</td>
      <td>0.05<br>(4.37)</td>
      <td>0.08<br>(4.92)</td>
      <td>0.02<br>(1.32)</td>
      <td>0.19<br>(11.30)</td>
      <td>0.02<br>(1.29)</td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.45</td>
      <td>0.54</td>
      <td>0.28</td>
      <td>0.28</td>
      <td>0.53</td>
      <td>0.80</td>
      <td>0.27</td>
      <td>0.30</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>1.00</td>
      <td>0.96</td>
      <td>0.66</td>
      <td>0.86</td>
      <td>0.97</td>
      <td>1.21</td>
      <td>0.52</td>
      <td>0.68</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>0.72</td>
      <td>0.70</td>
      <td>0.63</td>
      <td>0.67</td>
      <td>0.77</td>
      <td>0.75</td>
      <td>0.81</td>
      <td>0.54</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), profitability (RMW), and investment (CMA) portfolios from Fama and French (2015) and the momentum (UMD) portfolios from Ken’s French data library. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from July 1963 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from November 1990 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized

Springer

---

# Page 27

60

C. S. Asness et al.

Table 6 QMJ: recessions, severe bear and bull markets and volatility environment

<table>
  <thead>
    <tr>
      <th rowspan="2">Return</th>
      <th colspan="4">t-statistics</th>
      <th rowspan="2">Number of months</th>
    </tr>
    <tr>
      <th>Excess Return</th>
      <th>CAPM Alpha</th>
      <th>3-Factor Alpha</th>
      <th>4-Factor Alpha</th>
      <th>Excess Return</th>
      <th>CAPM Alpha</th>
      <th>3-Factor Alpha</th>
      <th>4-Factor Alpha</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="10">Panel A: Long Sample U.S., 7/1957 – 12/2016</td>
    </tr>
    <tr>
      <td>All Periods</td>
      <td>0.29</td>
      <td>0.39</td>
      <td>0.51</td>
      <td>0.60</td>
      <td>3.62</td>
      <td>5.43</td>
      <td>8.90</td>
      <td>9.95</td>
      <td>714</td>
    </tr>
    <tr>
      <td>Recession</td>
      <td>0.50</td>
      <td>0.48</td>
      <td>0.74</td>
      <td>0.82</td>
      <td>2.00</td>
      <td>2.16</td>
      <td>4.47</td>
      <td>4.96</td>
      <td>110</td>
    </tr>
    <tr>
      <td>Expansion</td>
      <td>0.25</td>
      <td>0.38</td>
      <td>0.49</td>
      <td>0.56</td>
      <td>3.03</td>
      <td>4.99</td>
      <td>8.26</td>
      <td>8.69</td>
      <td>604</td>
    </tr>
    <tr>
      <td>Severe bear market</td>
      <td>0.03</td>
      <td>0.30</td>
      <td>0.82</td>
      <td>0.78</td>
      <td>0.03</td>
      <td>0.40</td>
      <td>1.69</td>
      <td>1.50</td>
      <td>21</td>
    </tr>
    <tr>
      <td>Severe bull Market</td>
      <td>0.18</td>
      <td>0.18</td>
      <td>0.32</td>
      <td>0.50</td>
      <td>1.14</td>
      <td>1.21</td>
      <td>2.46</td>
      <td>3.56</td>
      <td>144</td>
    </tr>
    <tr>
      <td>Low volatility</td>
      <td>0.43</td>
      <td>0.63</td>
      <td>0.71</td>
      <td>0.77</td>
      <td>2.41</td>
      <td>4.21</td>
      <td>5.78</td>
      <td>6.16</td>
      <td>245</td>
    </tr>
    <tr>
      <td>High volatility</td>
      <td>0.13</td>
      <td>0.21</td>
      <td>0.41</td>
      <td>0.56</td>
      <td>1.24</td>
      <td>1.92</td>
      <td>5.70</td>
      <td>7.16</td>
      <td>227</td>
    </tr>
    <tr>
      <td>Spike up in volatility</td>
      <td>0.48</td>
      <td>0.56</td>
      <td>0.58</td>
      <td>0.72</td>
      <td>3.20</td>
      <td>4.15</td>
      <td>5.18</td>
      <td>6.32</td>
      <td>240</td>
    </tr>
    <tr>
      <td>Spike down in volatility</td>
      <td>0.00</td>
      <td>0.23</td>
      <td>0.48</td>
      <td>0.47</td>
      <td>−0.04</td>
      <td>1.80</td>
      <td>5.06</td>
      <td>4.58</td>
      <td>238</td>
    </tr>
    <tr>
      <td colspan="10">Panel B: Broad Sample Global, 7/1989 – 12/2016</td>
    </tr>
    <tr>
      <td>All Periods</td>
      <td>0.38</td>
      <td>0.51</td>
      <td>0.61</td>
      <td>0.61</td>
      <td>3.33</td>
      <td>5.76</td>
      <td>8.75</td>
      <td>8.07</td>
      <td>330</td>
    </tr>
    <tr>
      <td>Recession</td>
      <td>0.91</td>
      <td>0.59</td>
      <td>1.22</td>
      <td>1.23</td>
      <td>1.84</td>
      <td>1.70</td>
      <td>5.18</td>
      <td>5.15</td>
      <td>37</td>
    </tr>
    <tr>
      <td>Expansion</td>
      <td>0.32</td>
      <td>0.50</td>
      <td>0.59</td>
      <td>0.56</td>
      <td>2.80</td>
      <td>5.56</td>
      <td>8.44</td>
      <td>7.24</td>
      <td>293</td>
    </tr>
    <tr>
      <td>Severe bear market</td>
      <td>0.57</td>
      <td>0.93</td>
      <td>1.23</td>
      <td>1.30</td>
      <td>0.53</td>
      <td>1.78</td>
      <td>5.33</td>
      <td>4.64</td>
      <td>15</td>
    </tr>
    <tr>
      <td>Severe bull Market</td>
      <td>0.65</td>
      <td>0.59</td>
      <td>0.71</td>
      <td>0.89</td>
      <td>2.38</td>
      <td>2.38</td>
      <td>3.98</td>
      <td>3.97</td>
      <td>38</td>
    </tr>
    <tr>
      <td>Low volatility</td>
      <td>0.53</td>
      <td>0.65</td>
      <td>0.81</td>
      <td>0.79</td>
      <td>2.31</td>
      <td>4.09</td>
      <td>6.65</td>
      <td>6.29</td>
      <td>139</td>
    </tr>
    <tr>
      <td>High volatility</td>
      <td>0.10</td>
      <td>0.19</td>
      <td>0.38</td>
      <td>0.50</td>
      <td>0.67</td>
      <td>1.48</td>
      <td>3.22</td>
      <td>3.72</td>
      <td>92</td>
    </tr>
    <tr>
      <td>Spike up in volatility</td>
      <td>0.53</td>
      <td>0.64</td>
      <td>0.61</td>
      <td>0.64</td>
      <td>2.40</td>
      <td>3.86</td>
      <td>4.79</td>
      <td>4.81</td>
      <td>115</td>
    </tr>
    <tr>
      <td>Spike down in volatility</td>
      <td>0.17</td>
      <td>0.39</td>
      <td>0.65</td>
      <td>0.61</td>
      <td>0.88</td>
      <td>2.47</td>
      <td>5.02</td>
      <td>4.27</td>
      <td>116</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time portfolio returns. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Recession” indicates NBER recessions. “Expansion” indicates all other months. “Severe bear (bull) market” is defined as a total market return in the past 12-month below (above) -25% (25%). “Low (high) volatility” indicates periods of low (high) market volatility. We measure volatility as the one-month standard deviation of daily returns of the CRSP-value weighted index (U.S.) or the MSCI-World index (global) and split the sample in the top and bottom 30% high and low periods. “Spike Up (down) in Volatility” indicates periods of large increases or drops in market volatility. We measure volatility changes as the one-month change in market volatility and split the sample into top and bottom 30% Spike Up and Down periods

Springer

---

# Page 28

Quality minus junk

61

## 5.4 The risk of quality stocks

We have already noted that the evidence does not point toward compensation for risk measured by the host of factor models considered above. The evidence also does not point toward compensation for tail risk as seen in Table 6. We compute the return of the QMJ factors during recessions and expansions, during severe bear and bull markets (defined as total market returns in the past 12 months below $-25\%$ or above $+25\%$), during periods of high and low market volatility (measured as the one-month standard deviation of daily returns of the CRSP-value weighted index or the MSCI-World index and splitting the sample in the 30% top and bottom periods), and during periods of a large increase or drop in aggregate volatility (again splitting the sample into the 30% top and bottom periods in terms of the one-month change in volatility). We find no evidence of compensation for tail risk. If anything, the evidence again points toward high-quality stocks being safer than junk stocks: quality appears to hedge (as opposed being correlated to) periods of market distress.

To study further the risk of QMJ, Fig. 3 plots the performance of QMJ against the return on the market. The negative beta of QMJ is clearly visible by the downward sloping relation of the excess return of QMJ and the market. Further, the relatively tight fit around the curve shows the limited residual risk, implying a strong and consistent historical performance of QMJ during down periods for the market. QMJ also performs well in extreme down markets; in fact, the estimated second-order polynomial shown in the graph has a positive (but insignificant) quadratic term, meaning that the fitted curve bends upward in the extreme. This mild concavity is mostly driven by the returns to the profitability subcomponent of quality. The quadratic term is marginally significant ($t$-statistic of 2.4) for the profitability factor in our long sample. The strong return in extreme down markets is consistent with a *flight to quality* (or at least to profitability). That is, in down markets, investors may exhibit flight to quality in the sense that prices of unprofitable stocks drop more than the prices of profitable stocks, even adjusting for their betas. The strong performance of QMJ in down markets is robust to considering longer periods such as down-market quarters or down-market years (not shown for brevity).

The alphas also reveal a similar pattern of mild flight to quality. At the very least, quality stocks, even after adjustment for their factor loadings, do not appear to perform poorly in periods of extreme market distress; if anything, they tend to deliver higher returns at those times.

Overall, our findings present serious challenges for the risk-based theories (explanation (b) above). Using a variety of factor models ranging from the CAPM to a seven-factor model as our risk adjustment, we show that QMJ factors earn significant abnormal returns. Looking at factor exposures and performance during distressed market conditions, quality stocks appear safer, not riskier, than junk stocks. Of course, alternative risk-based explanations are always possible; such explanations will have to generate these patterns to match the empirical evidence.

## 5.5 Market (in)efficiency: analysts’ expectations of the price of quality

To test whether the limited explanatory power of quality on price could be driven at least partly by limited efficiency (theory (c) above), we consider the expectations of equity analysts using the methodology of Brav et al. (2005). We consider each analyst’s target price, that is, the expected price 1 yr into the future. As seen in

$\copyright$ Springer

---

# Page 29

62

C. S. Asness et al.

Table 7, target prices scaled by book values are higher for high-quality stocks. In other words, analyst forecasts appear consistent with the idea that high-quality stocks deserve higher prices.

Next, Table 7 and Fig. 4 consider the implied return expectations, computed as the ratio of the target price to the current price minus 1. We see that analysts have lower return expectations for higher-quality stocks than junk stocks. In other words, analyst expectations are inconsistent with the high ex-post realized returns of high-quality stocks.

Analysts’ implied return expectations could reflect that the *required* return of high-quality stocks is lower than that of junk stocks (because quality stocks are viewed as safer). If so, quality stocks should realize lower returns than junk stocks, or, said differently, quality stocks should have a larger price premium. However, since quality stocks actually realize high risk-adjusted returns, our findings reflect erroneous analyst expectations consistent with theory (c) for our finding that the price of quality is too limited. $^{20}$

Table 7 presents further evidence of analyst bias, which could help explain our results on the price of quality. In particular, we find that analysts are too optimistic about junk stocks on average and much more so than about quality stocks. Further, the dispersion of analyst forecasts is much larger for junk stocks.

As further evidence consistent with the idea of mispricing and limited arbitrage, we show in Table 19 in the Appendix that short-sellers more frequently short junk stocks, relative to quality stocks, and shorting costs are higher for junk stocks. $^{21}$

If the limited price of quality is partly driven by limited market efficiency, then how far off the mark are market prices? This is an important question, but a precise answer is beyond the scope of this paper. To get a sense of magnitudes, we can consider the event-time cumulative five-year abnormal return of QMJ. $^{22}$ Buying quality and shorting junk for 5 yrs earns a cumulative four-factor alpha of 20.85% on average in our U.S. sample (22.04% in the global sample). The cumulative abnormal return can be interpreted as an average underpricing of 10.72% among high-quality stocks and overpricing of 10.72% of junk stocks across the two samples. Of course, this could reflect that some quality stocks are more underpriced while others are less underpriced or even overpriced.

---

$^{20}$ Analysts tend to self-select to cover stocks for which they have relatively optimistic expectations (McNichols and O’Brien 1997) and this overrepresentation of optimistic analysts leads to an upward bias of their forecasts, which could be especially strong for junk stocks that have greater fundamental uncertainty (and hence greater potential dispersion in analyst beliefs). For further analysis of errors in analysts’ target prices and associated mispricing of stocks, see Dechow and You (2017).

$^{21}$ Shleifer and Vishny (1997) consider a model of limited arbitrage, and Duffie et al. (2002) model short-sellers and shorting costs (that is, securities lending fees).

$^{22}$ We compute the $k$ -month event-time abnormal return $\alpha^k$ as the intercept in a regression:

$$
r_t^k = \alpha^k + \beta^{MKT} MKT_t + \beta^{SMB} SMB_t + \beta^{HML} HML_t + \beta^{UMD} UMD_t + \varepsilon_t,
$$

where $r_t^k = \sum_i w_{i,t-k} r_{i,t}$ is excess return in month $t$ of a calendar-time portfolio formed in month $t-k$ . The event-time cumulative abnormal return $CAR$ is given by $CAR = \sum_k \alpha^k$ .

$\copyright$ Springer

---

# Page 30

Quality minus junk

63

A: Long Sample (U.S., 1957 - 2016)

![image](image_1.png)

B: Broad Sample (Global, 1989 - 2016)

![image](image_2.png)

Fig. 3 QMJ: Flight to Quality. This figure shows monthly returns and four-factor alpha of quality minus junk (QMJ) factors. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the monthly returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. Returns are in U.S. doolars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. We plot monthly excess returns and alphas on the y-axes and market excess returns on the x-axes. Market returns indices are either the CRSP-value weighted index (U.S.) or the MSCI-World index (global)

## 5.6 Linking prices and returns: the price of quality predicts QMJ

We next consider more directly the link between the price of quality and the future returns of QMJ. The theory of limited market efficiency (explanation (c) above) implies that a higher price of quality predicts lower future returns to quality. In other words, when market prices incorporate quality to a larger extent, then the expected return to buying quality is lower. In contrast, theories (a) and (b) do not have clear predictions for the time-variation of risk-adjusted returns.

Springer

---

# Page 31

64

C. S. Asness et al.

Table 7 Quality-sorted portfolios: target prices and forecast errors

<table>
  <thead>
    <tr>
      <th></th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
      <th>H-L t-statistics</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>**Panel A: United States**</td>
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
      <td>Price (scaled by book)</td>
      <td>2.69</td>
      <td>2.29</td>
      <td>2.46</td>
      <td>2.80</td>
      <td>3.10</td>
      <td>3.02</td>
      <td>3.30</td>
      <td>3.81</td>
      <td>4.58</td>
      <td>7.05</td>
      <td>4.36</td>
      <td>4.20</td>
    </tr>
    <tr>
      <td>Mean price target (scaled by book)</td>
      <td>3.45</td>
      <td>2.79</td>
      <td>2.94</td>
      <td>3.31</td>
      <td>3.64</td>
      <td>3.50</td>
      <td>3.85</td>
      <td>4.43</td>
      <td>5.28</td>
      <td>8.26</td>
      <td>4.82</td>
      <td>3.83</td>
    </tr>
    <tr>
      <td>Median price target (scaled by book)</td>
      <td>3.43</td>
      <td>2.78</td>
      <td>2.93</td>
      <td>3.31</td>
      <td>3.63</td>
      <td>3.49</td>
      <td>3.85</td>
      <td>4.42</td>
      <td>5.28</td>
      <td>8.28</td>
      <td>4.85</td>
      <td>3.85</td>
    </tr>
    <tr>
      <td>Mean Implied Expected Return</td>
      <td>0.26</td>
      <td>0.20</td>
      <td>0.19</td>
      <td>0.17</td>
      <td>0.17</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.15</td>
      <td>0.15</td>
      <td>-0.11</td>
      <td>-3.71</td>
    </tr>
    <tr>
      <td>Median Implied Expected Return</td>
      <td>0.25</td>
      <td>0.19</td>
      <td>0.19</td>
      <td>0.17</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>-0.10</td>
      <td>-3.80</td>
    </tr>
    <tr>
      <td>Dispersion</td>
      <td>0.83</td>
      <td>0.90</td>
      <td>0.95</td>
      <td>0.96</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.95</td>
      <td>0.13</td>
      <td>6.06</td>
    </tr>
    <tr>
      <td>Number of estimates</td>
      <td>9.10</td>
      <td>10.67</td>
      <td>12.08</td>
      <td>12.04</td>
      <td>12.41</td>
      <td>13.12</td>
      <td>14.31</td>
      <td>13.37</td>
      <td>14.47</td>
      <td>17.43</td>
      <td>8.33</td>
      <td>8.48</td>
    </tr>
    <tr>
      <td>Mean Forecast Error</td>
      <td>-0.030</td>
      <td>-0.019</td>
      <td>-0.015</td>
      <td>-0.011</td>
      <td>-0.011</td>
      <td>-0.010</td>
      <td>-0.008</td>
      <td>-0.008</td>
      <td>-0.007</td>
      <td>-0.005</td>
      <td>0.03</td>
      <td>3.46</td>
    </tr>
    <tr>
      <td>Dispersion (EPS)</td>
      <td>0.551</td>
      <td>0.328</td>
      <td>0.224</td>
      <td>0.141</td>
      <td>0.109</td>
      <td>0.091</td>
      <td>0.084</td>
      <td>0.059</td>
      <td>0.053</td>
      <td>0.034</td>
      <td>-0.52</td>
      <td>-8.07</td>
    </tr>
    <tr>
      <td>Number of estimates (EPS)</td>
      <td>15.36</td>
      <td>18.05</td>
      <td>19.30</td>
      <td>20.22</td>
      <td>20.78</td>
      <td>20.88</td>
      <td>22.04</td>
      <td>23.06</td>
      <td>21.79</td>
      <td>25.56</td>
      <td>10.20</td>
      <td>10.28</td>
    </tr>
    <tr>
      <td>Realized future 12-month return</td>
      <td>0.024</td>
      <td>0.059</td>
      <td>0.067</td>
      <td>0.067</td>
      <td>0.071</td>
      <td>0.097</td>
      <td>0.065</td>
      <td>0.093</td>
      <td>0.079</td>
      <td>0.068</td>
      <td>0.054</td>
      <td>1.82</td>
    </tr>
    <tr>
      <td>**Panel B: Global**</td>
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
      <td>Price (scaled by book)</td>
      <td>2.74</td>
      <td>2.37</td>
      <td>2.47</td>
      <td>2.78</td>
      <td>3.06</td>
      <td>2.98</td>
      <td>3.26</td>
      <td>3.75</td>
      <td>4.48</td>
      <td>6.85</td>
      <td>4.11</td>
      <td>4.08</td>
    </tr>
    <tr>
      <td>Mean price target (scaled by book)</td>
      <td>3.56</td>
      <td>2.92</td>
      <td>2.97</td>
      <td>3.29</td>
      <td>3.59</td>
      <td>3.45</td>
      <td>3.80</td>
      <td>4.36</td>
      <td>5.16</td>
      <td>8.03</td>
      <td>4.46</td>
      <td>3.63</td>
    </tr>
    <tr>
      <td>Median price target (scaled by book)</td>
      <td>3.54</td>
      <td>2.91</td>
      <td>2.96</td>
      <td>3.29</td>
      <td>3.58</td>
      <td>3.44</td>
      <td>3.80</td>
      <td>4.35</td>
      <td>5.16</td>
      <td>8.04</td>
      <td>4.50</td>
      <td>3.65</td>
    </tr>
    <tr>
      <td>Mean Implied Expected Return</td>
      <td>0.28</td>
      <td>0.22</td>
      <td>0.20</td>
      <td>0.17</td>
      <td>0.17</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.15</td>
      <td>0.15</td>
      <td>-0.13</td>
      <td>-5.02</td>
    </tr>
    <tr>
      <td>Median Implied Expected Return</td>
      <td>0.27</td>
      <td>0.21</td>
      <td>0.19</td>
      <td>0.17</td>
      <td>0.16</td>
      <td>0.15</td>
      <td>0.16</td>
      <td>0.16</td>
      <td>0.15</td>
      <td>0.16</td>
      <td>-0.11</td>
      <td>-5.22</td>
    </tr>
    <tr>
      <td>Dispersion</td>
      <td>0.82</td>
      <td>0.90</td>
      <td>0.95</td>
      <td>0.96</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.98</td>
      <td>0.97</td>
      <td>0.97</td>
      <td>0.95</td>
      <td>0.13</td>
      <td>6.75</td>
    </tr>
    <tr>
      <td>Number of estimates</td>
      <td>8.72</td>
      <td>10.41</td>
      <td>11.84</td>
      <td>11.86</td>
      <td>12.26</td>
      <td>12.98</td>
      <td>14.12</td>
      <td>13.32</td>
      <td>14.34</td>
      <td>16.85</td>
      <td>8.13</td>
      <td>8.76</td>
    </tr>
    <tr>
      <td>Mean Forecast Error</td>
      <td>-0.030</td>
      <td>-0.019</td>
      <td>-0.016</td>
      <td>-0.011</td>
      <td>-0.011</td>
      <td>-0.008</td>
      <td>-0.006</td>
      <td>-0.007</td>
      <td>-0.007</td>
      <td>-0.005</td>
      <td>0.02</td>
      <td>3.34</td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 32

Quality minus junk

65

Table 7 (continued)

<table>
  <thead>
    <tr>
      <th></th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
      <th>H-L t-statistics</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Dispersion (EPS)</td>
      <td>0.548</td>
      <td>0.338</td>
      <td>0.305</td>
      <td>0.348</td>
      <td>0.172</td>
      <td>0.121</td>
      <td>0.104</td>
      <td>0.101</td>
      <td>0.063</td>
      <td>0.045</td>
      <td>−0.50</td>
      <td>−7.31</td>
    </tr>
    <tr>
      <td>Number of estimates (EPS)</td>
      <td>15.18</td>
      <td>16.95</td>
      <td>18.33</td>
      <td>19.27</td>
      <td>19.86</td>
      <td>20.21</td>
      <td>21.25</td>
      <td>22.21</td>
      <td>20.85</td>
      <td>23.40</td>
      <td>8.23</td>
      <td>7.55</td>
    </tr>
    <tr>
      <td>Realized future 12-month return</td>
      <td>0.025</td>
      <td>0.055</td>
      <td>0.065</td>
      <td>0.067</td>
      <td>0.074</td>
      <td>0.098</td>
      <td>0.069</td>
      <td>0.094</td>
      <td>0.083</td>
      <td>0.070</td>
      <td>0.058</td>
      <td>2.00</td>
    </tr>
  </tbody>
</table>


This table shows evidence on analysts’ one-year-ahead target prices and earnings forecasts for quality-sorted portfolios. Each calendar month, stocks in each country are ranked in ascending order on the basis of their quality score. The ranked stocks are assigned to one of 10 portfolios, where U.S. sorts are based on NYSE breakpoints. For each portfolio, each month we compute the weighted-average target price (scaled by book equity), using the I/B/E/S mean and median consensus for each stock. For each portfolio, we also compute the weighted-average forecast error, defined as actual I/B/E/S EPS earnings for the next fiscal year minus the current mean or median analyst earnings forecast, deflated by the stock price. We report time-series averages of each variable. “Dispersion” is the cross-sectional standard deviation of the consensus estimate divided by the absolute value of the mean estimate. The rightmost columns report the difference between portfolios 10 and 1 and the corresponding t-statistic. Standard errors are adjusted for heteroskedasticity and autocorrelation (Newey and West 1987) with a lag length of 5 yrs, and 5% statistical significance is indicated in bold. Stocks in each portfolio are value-weighted and refreshed every calendar month. For the global sample, we form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. The sample period of our I/B/E/S target price data runs from March 1999 to December 2016. The sample period of our I/B/E/S EPS data runs from January 1982 (U.S.) and December 1985 (global) to December 2016

Springer

---

# Page 33

66

C. S. Asness et al.

A: United States, 1999 – 2016

![image](image_1.png)

B: Global, 1999 – 2016

![image](image_2.png)

Fig. 4 Expected Returns versus Return Expectations. This figure plots realized returns and return expectations based on I/B/E/S target prices for quality-sorted portfolios. Portfolio P1 contains the stocks with the lowest quality scores, and P10 those with the highest quality scores. Each calendar month, stocks in each country are ranked in ascending order on the basis of their quality score. The ranked stocks are assigned to one of 10 portfolios, where U.S. sorts are based on NYSE breakpoints. For each portfolio, each month we compute the weighted-average target price (scaled by book equity) using the I/B/E/S mean and median consensus for each stock. We report time-series averages of each variable. The implied expected return is given by the ratio of target prices to current prices minus 1. For the global sample, we form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. The sample period of our I/B/E/S target price data runs from March 1999 to December 2016

Springer

---

# Page 34

Quality minus junk

67

We first consider how the price of quality varies over time. To study this, Fig. 5 shows the time series of the price of quality, that is, the time series of the Fama-MacBeth regression coefficients that we estimate above in Eq. 8. Specifically, we plot the monthly coefficients from Table 12, columns (1) and (7). We see that the price of quality varies significantly over time. As one might expect, the price of quality is low during the height of the internet bubble in early 2000 and has other large swings during periods consistent with the economics intuition as discussed in the introduction. Figure 11 in the Appendix plots the time series of cross-sectional coefficients for the quality sub-components.

The intuitive pattern of the price of quality suggests that the variation is not just driven by noise. To explore further the variation in the price of quality, it is interesting to link prices and subsequent returns in the time series. Specifically, if this time variation is not due to mis-measurement noise, then a high price of quality should predict low subsequent returns of QMJ. Table 8 provides evidence of such predictability. This table reports the regression coefficients of time-series regressions of future QMJ returns on the ex ante price of quality:

$$
QMJ_{t \to t+k} = \beta^0 + \beta^{lagged\ FMB} b_{t-1} + \beta^{lagged\ QMJ} QMJ_{t-12,t-1} + \varepsilon_t.
\quad (11)
$$

Said simply, $QMJ_{t \to t+k}$ is the return of QMJ over the future $k$ months, $b_{t-1}$ is the lagged price of quality (the variable of interest), and $QMJ_{t-12,t-1}$ controls for past returns. Let us describe each of these variables in detail.

We run the regression in two ways: using the excess returns of the QMJ factor on the left-hand side (“Ret-Rf”) and using the alpha of the QMJ factor on the left-hand side (“Alpha”). The future excess return on the raw QMJ factor is computed simply by cumulating returns, $QMJ_{t \to t+k} = \prod_{j=0}^{k} \left(1 + QMJ_{t+j} + r_{t+j}^f\right) - \prod_t \left(1 + r_{t+j}^f\right)$ . To compute the alphas, we regress QMJ on the contemporaneous returns of the market, size, value, and momentum factors and compute the alpha as the regression residual plus the intercept (i.e., as the return of QMJ with its factor exposures hedged out). We then cumulate these alphas $QMJ_{t \to t+k} = \prod_{j=0}^{k} \left(1 + \alpha_{t+j} + r_{t+j}^f\right) - \prod_t \left(1 + r_{t+j}^f\right)$ and use them on the left-hand side of (11). We consider alphas to ensure that the predictability of the price of quality on QMJ is not driven by any potential predictability of other factors.

The price of quality, $b_{t-1}$ , is the lagged Fama-MacBeth regression coefficient from Eq. (8) that gives the connection between price and quality at each time. Specifically, the price of quality is estimated from the monthly regressions reported in Table 14, columns (1) and (7). We are interested in testing the hypothesis that a high lagged price of quality predicts lower subsequent returns, that is, $b_{t-1} < 0$ .

Last, $QMJ_{t-12,t-1}$ is defined as the portfolio-weighted average of the past one-year returns of the stocks in the QMJ portfolio. This captures standard momentum effects, again to ensure that the predictability of the price of quality is a novel finding.

Table 8 reports only the regression coefficient for the variable of interest, $b_{t-1}$ , the ex ante price of quality. We run overlapping forecasting regressions predicting returns from 1 mo up to 5 yrs. We adjust standard errors for heteroskedasticity and autocorrelation (Newey and West 1987) with a lag length of 5 yrs.

$\copyright$ Springer

---

# Page 35

68

C. S. Asness et al.

Table 8 shows that a high price of quality indeed predicts lower future returns on QMJ. In our U.S. long sample shown in Panel A, all the coefficients have the expected negative sign, and we can reject the null hypothesis of no predictability in all but one specification. Predictability rises with the forecasting horizon, indicating slowly changing expected returns. The results for our shorter global sample in Panel B are noisier, but we see that all of the statistically significant coefficients are negative as expected. The bottom rows of Table 8 similarly test whether the price of the separate quality characteristics predict the returns of the corresponding long/short factors. While these results are noisier, the estimates tend to be negative, as conjectured.

To summarize, the results in Table 8 are consistent with the hypothesis that the variation of the price of quality is not pure noise but rather reflects changes in the market pricing of quality characteristics, generating variation in QMJ returns.

## 6 Further asset pricing applications

### 6.1 Quality at a reasonable price

It is interesting to consider what is the fair price of quality? That is, if we suppose that a stock’s fundamental value $V$ is a multiple of its quality, $V = m \, Quality$ , then what is the fair value of $m$ ? Relatedly, if the market pays a price for quality different from $m$ , then what is the best way to buy cheap quality stocks?

To answer these questions, we construct a long-short portfolio that we call *quality at a reasonable price* (QARP) as follows. Using the same factor construction as for QMJ, we construct a long-short portfolio based on the signal $n \, Quality_t^i - z(P_t^i)$ for various choices of $n$ . That is, QARP is based on a stock’s quality times $n$ , minus its price-to-book (normalized as a z-score). We should get the highest risk-

![image](image_1.png)

Fig. 5 Cross-Sectional Regressions Coefficient, the Price of Quality. This figure plots coefficients from monthly cross-sectional regressions. The dependent variable is the log of a firm’s market-to-book ratio in month $t$ . The explanatory variable is the quality score in month $t$ . We plot the time series of the cross-sectional coefficients

Springer

---

# Page 36

Quality minus junk

69

Table 8 Time variation of the price of quality: high price of quality predicts low QMJ returns

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1957 – 12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th>Panel B: Broad Sample (Global, 7/1989 – 12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>Return (t)</td>
      <td>Return (t, t + 12)</td>
      <td>Return (t, t + 36)</td>
      <td>Return (t, t + 60)</td>
      <td>Return (t)</td>
      <td>Return (t, t + 12)</td>
      <td>Return (t, t + 36)</td>
      <td>Return (t, t + 60)</td>
    </tr>
    <tr>
      <td></td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
    </tr>
    <tr>
      <td>QMJ</td>
      <td>-0.03</td>
      <td>-0.01</td>
      <td>-0.46</td>
      <td>-0.27</td>
      <td>-1.52</td>
      <td>-1.03</td>
      <td>-2.35</td>
      <td>-2.87</td>
    </tr>
    <tr>
      <td></td>
      <td>(-3.18)</td>
      <td>(-1.76)</td>
      <td>(-2.82)</td>
      <td>(-2.50)</td>
      <td>(-3.60)</td>
      <td>(-2.78)</td>
      <td>(-3.59)</td>
      <td>(-4.32)</td>
    </tr>
    <tr>
      <td>Profitability</td>
      <td>-0.04</td>
      <td>-0.02</td>
      <td>-0.49</td>
      <td>-0.34</td>
      <td>-1.51</td>
      <td>-1.19</td>
      <td>-2.27</td>
      <td>-2.69</td>
    </tr>
    <tr>
      <td></td>
      <td>(-3.28)</td>
      <td>(-2.14)</td>
      <td>(-2.95)</td>
      <td>(-2.41)</td>
      <td>(-3.61)</td>
      <td>(-2.84)</td>
      <td>(-3.18)</td>
      <td>(-4.16)</td>
    </tr>
    <tr>
      <td>Growth</td>
      <td>-0.03</td>
      <td>-0.01</td>
      <td>-0.33</td>
      <td>-0.08</td>
      <td>-0.99</td>
      <td>-0.11</td>
      <td>-0.41</td>
      <td>-1.70</td>
    </tr>
    <tr>
      <td></td>
      <td>(-3.42)</td>
      <td>(-0.81)</td>
      <td>(-2.26)</td>
      <td>(-0.70)</td>
      <td>(-1.76)</td>
      <td>(-0.34)</td>
      <td>(-0.61)</td>
      <td>(-1.80)</td>
    </tr>
    <tr>
      <td>Safety</td>
      <td>-0.01</td>
      <td>0.00</td>
      <td>-0.11</td>
      <td>-0.07</td>
      <td>-0.97</td>
      <td>-0.73</td>
      <td>-2.28</td>
      <td>-2.52</td>
    </tr>
    <tr>
      <td></td>
      <td>(-0.63)</td>
      <td>(-0.12)</td>
      <td>(-0.61)</td>
      <td>(-0.48)</td>
      <td>(-1.99)</td>
      <td>(-1.65)</td>
      <td>(-2.39)</td>
      <td>(-3.41)</td>
    </tr>
    <tr>
      <td>Average Adj R2</td>
      <td>0.06</td>
      <td>0.04</td>
      <td>0.07</td>
      <td>0.04</td>
      <td>0.17</td>
      <td>0.08</td>
      <td>0.16</td>
      <td>0.31</td>
    </tr>
  </tbody>
</table>


<table>
  <thead>
    <tr>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <td>Return (t)</td>
      <td>Return (t, t + 12)</td>
      <td>Return (t, t + 36)</td>
      <td>Return (t, t + 60)</td>
      <td>Return (t)</td>
      <td>Return (t, t + 12)</td>
      <td>Return (t, t + 36)</td>
      <td>Return (t, t + 60)</td>
    </tr>
    <tr>
      <td></td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
      <td>Ret-Rf</td>
      <td>Alpha</td>
    </tr>
    <tr>
      <td>QMJ</td>
      <td>-0.03</td>
      <td>0.02</td>
      <td>-0.82</td>
      <td>0.10</td>
      <td>-1.91</td>
      <td>0.17</td>
      <td>-1.40</td>
      <td>-3.57</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.38)</td>
      <td>(1.49)</td>
      <td>(-2.65)</td>
      <td>(0.56)</td>
      <td>(-2.99)</td>
      <td>(0.30)</td>
      <td>(-4.09)</td>
      <td>(-6.32)</td>
    </tr>
    <tr>
      <td>Profitability</td>
      <td>-0.04</td>
      <td>0.02</td>
      <td>-1.08</td>
      <td>-0.14</td>
      <td>-2.14</td>
      <td>-0.59</td>
      <td>-2.88</td>
      <td>-4.64</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.58)</td>
      <td>(1.13)</td>
      <td>(-4.55)</td>
      <td>(-0.95)</td>
      <td>(-3.60)</td>
      <td>(-1.37)</td>
      <td>(-4.93)</td>
      <td>(-6.16)</td>
    </tr>
    <tr>
      <td>Growth</td>
      <td>-0.03</td>
      <td>0.01</td>
      <td>-0.65</td>
      <td>-0.06</td>
      <td>-2.35</td>
      <td>-0.74</td>
      <td>-2.68</td>
      <td>-2.59</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.70)</td>
      <td>(0.51)</td>
      <td>(-3.78)</td>
      <td>(-0.31)</td>
      <td>(-4.05)</td>
      <td>(-1.09)</td>
      <td>(-2.20)</td>
      <td>(-3.86)</td>
    </tr>
    <tr>
      <td>Safety</td>
      <td>-0.02</td>
      <td>0.00</td>
      <td>-0.34</td>
      <td>0.04</td>
      <td>-0.61</td>
      <td>0.64</td>
      <td>0.69</td>
      <td>-1.33</td>
    </tr>
    <tr>
      <td></td>
      <td>(-1.07)</td>
      <td>(0.11)</td>
      <td>(-1.22)</td>
      <td>(0.27)</td>
      <td>(-1.42)</td>
      <td>(4.06)</td>
      <td>(3.17)</td>
      <td>(-2.79)</td>
    </tr>
    <tr>
      <td>Average Adj R2</td>
      <td>0.05</td>
      <td>0.02</td>
      <td>0.09</td>
      <td>0.01</td>
      <td>0.20</td>
      <td>0.07</td>
      <td>0.19</td>
      <td>0.36</td>
    </tr>
  </tbody>
</table>


This table shows results of monthly time-series regressions of future quality factor returns on the lagged price of quality. The left-hand side is the cumulative excess return (labeled “Ret-Rf”) and the cumulative abnormal return (labeled “Alpha”) of the QMJ factor (or profitability, growth, and safety) over the subsequent one, 12, 36, or 60 months. Abnormal returns are constructed from of a time-series regression of monthly excess returns on the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. Regression coefficients are estimated using all available data, and abnormal returns are cumulated over the subsequent t + k period. The right-hand side variables are the lagged price of quality and prior quality returns. The lagged price of quality at time t is the regression coefficient of a cross sectional regression of log market-to-book ratios in month t-1 on quality score in month t-1. The prior quality return is defined as the portfolio-weighted average of the past one-year returns of the stocks in the portfolio. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Each line and each column reports results from a separate regression. We report only the coefficient on the variable of interest, the lagged price of quality. An intercept and prior quality returns are included in all regressions but not reported. Standard errors are adjusted for heteroskedasticity and autocorrelation (Newey and West 1987) with lag length of 5 yrs, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Average Adj R2” is the average adjusted R-squared across all the regressions above

Springer

---

# Page 37

70

C. S. Asness et al.

Table 9 Asset pricing tests: HML, SMB, and UMD

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1957–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>Panel B: Broad Sample (Global, 7/1989–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>SMB</td>
      <td>SMB</td>
      <td>HML</td>
      <td>HML</td>
      <td>UMD</td>
      <td>SMB</td>
      <td>SMB</td>
      <td>HML</td>
      <td>HML</td>
      <td>UMD</td>
    </tr>
    <tr>
      <td>Excess Returns</td>
      <td>0.15</td>
      <td>0.16</td>
      <td>0.30</td>
      <td>0.30</td>
      <td>0.71</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.35</td>
      <td>0.35</td>
      <td>0.66</td>
    </tr>
    <tr>
      <td></td>
      <td>(1.55)</td>
      <td>(1.55)</td>
      <td>(2.39)</td>
      <td>(2.39)</td>
      <td>(4.77)</td>
      <td>(0.23)</td>
      <td>(0.23)</td>
      <td>(2.19)</td>
      <td>(2.19)</td>
      <td>(3.05)</td>
    </tr>
    <tr>
      <td>Alpha</td>
      <td>0.13</td>
      <td>0.49</td>
      <td>0.79</td>
      <td>1.01</td>
      <td>1.22</td>
      <td>0.08</td>
      <td>0.43</td>
      <td>0.76</td>
      <td>1.00</td>
      <td>1.08</td>
    </tr>
    <tr>
      <td></td>
      <td>(1.26)</td>
      <td>(4.97)</td>
      <td>(8.52)</td>
      <td>(12.47)</td>
      <td>(10.75)</td>
      <td>(0.71)</td>
      <td>(3.87)</td>
      <td>(6.82)</td>
      <td>(9.51)</td>
      <td>(7.57)</td>
    </tr>
    <tr>
      <td>MKT</td>
      <td>0.17</td>
      <td>0.01</td>
      <td>−0.16</td>
      <td>−0.26</td>
      <td>−0.25</td>
      <td>0.06</td>
      <td>−0.11</td>
      <td>−0.10</td>
      <td>−0.25</td>
      <td>−0.22</td>
    </tr>
    <tr>
      <td></td>
      <td>(7.15)</td>
      <td>(0.38)</td>
      <td>(−7.18)</td>
      <td>(−13.03)</td>
      <td>(−8.76)</td>
      <td>(2.57)</td>
      <td>(−3.51)</td>
      <td>(−3.83)</td>
      <td>(−8.44)</td>
      <td>(−6.87)</td>
    </tr>
    <tr>
      <td>SMB</td>
      <td></td>
      <td></td>
      <td>−0.04</td>
      <td>−0.22</td>
      <td>−0.16</td>
      <td></td>
      <td></td>
      <td>−0.13</td>
      <td>−0.30</td>
      <td>−0.12</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td>(−1.26)</td>
      <td>(−6.76)</td>
      <td>(−3.50)</td>
      <td></td>
      <td></td>
      <td>(−2.16)</td>
      <td>(−5.33)</td>
      <td>(−1.64)</td>
    </tr>
    <tr>
      <td>HML</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−0.81</td>
      <td></td>
      <td></td>
      <td>−0.27</td>
      <td></td>
      <td>−0.94</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−24.87)</td>
      <td></td>
      <td></td>
      <td>(−5.33)</td>
      <td></td>
      <td>(−19.14)</td>
    </tr>
    <tr>
      <td>UMD</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−0.56</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−19.14)</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>QMJ</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>−0.59</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>(−8.71)</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.20</td>
      <td>0.20</td>
      <td>0.31</td>
      <td>0.31</td>
      <td>0.62</td>
      <td>0.04</td>
      <td>0.04</td>
      <td>0.42</td>
      <td>0.42</td>
      <td>0.58</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td></td>
      <td>(−11.92)</td>
      <td>(−15.85)</td>
      <td>(−4.34)</td>
      <td></td>
      <td></td>
      <td>(−8.59)</td>
      <td></td>
      <td>(−0.02)</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>0.18</td>
      <td>0.73</td>
      <td>1.14</td>
      <td>1.69</td>
      <td>1.28</td>
      <td>0.15</td>
      <td>0.87</td>
      <td>1.34</td>
      <td>1.94</td>
      <td>1.47</td>
    </tr>
    <tr>
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
      <td>Adjusted R2</td>
      <td>0.09</td>
      <td>0.24</td>
      <td>0.47</td>
      <td>0.61</td>
      <td>0.48</td>
      <td>0.04</td>
      <td>0.22</td>
      <td>0.53</td>
      <td>0.62</td>
      <td>0.57</td>
    </tr>
  </tbody>
</table>


This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The test portfolios are the quality minus junk (QMJ) portfolio, the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Appendix 2. We run a regression of each of SMB, HML, and UMD on the remaining factors excluding and including the QMJ factor as explanatory variable. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to regression intercept, divided by the standard deviation of the estimated residuals. Sharpe ratios and information ratios are annualized

Springer

---

# Page 38

Quality minus junk

71

adjusted return if we let $n = m$ , that is, if we base the signal on the quality multiple that corresponds to the true fundamental value. Indeed, in this case, the portfolio is long the highest-alpha securities and short the lowest-alpha securities. $^{23}$

While $m$ is generally unobservable, as we do not know true fundamental values, we can proceed by relying on the fact that we have normalized quality and prices based on the cross-section. Specifically, if the highest-quality stocks were the most expensive, then the quality and price ranks would line up, corresponding to $m = 1$ . When we construct QARP empirically, we do find that the alpha is highest for $n$ close to 1 both in the United States and globally (as seen in Fig. 12 in the Appendix, which plots the monthly alpha of QARP as function of $n$ ).

Another way to consider QARP is to simply form a portfolio of quality (QMJ) and value (HML). The combination of QMJ and HML that has the highest Sharpe ratio puts a weight of about 63% on QMJ (and hence the remaining 37% on HML) in the United States and about 62% weight on QMJ globally.

The Sharpe ratio of QARP (whether constructed based on combining signals or combining factor returns) is naturally higher than either quality or value alone, about 0.7 in the United States and 0.9 globally. QARP performs well, as quality strategies complement value by helping an investor avoid the “value trap,” that is, buying securities that look cheap but deserve to be cheap. Instead, QARP buys securities that are cheap, relative to their quality. Our evidence suggests that the return to QARP is above the equity risk premium, which seems to challenge rational risk-based models.

## 6.2 QMJ on the right-hand-side of a factor model

We have seen that QMJ is an intuitive and powerful factor that has significant alpha, relative to a series of standard factor models. It is also interesting to switch things around and put QMJ on the right-hand-side to see how it affects the alphas and interpretation of the standard factors. More broadly, QMJ is a useful factor to add to the toolbox of global factors, for example, when researchers need to test whether new phenomena are driven by quality.

Table 9 reports the results of regressing each of the SMB, HML, and UMD on the other standard factors, with and without QMJ on the right-hand-side. Let us first consider SMB, that is, the size effect. SMB has a modest, but significant, excess return in our U.S. and global samples. In both, SMB has a small and insignificant alpha when controlling for the other standard factors (the market, HML, and UMD). The size effect is not present in our sample, but controlling for QMJ completely changes this conclusion. SMB has a very large negative exposure to QMJ. Clearly, small stocks are junky. This finding is intuitive, as small stocks could, for instance, be young firms that are yet to be profitable and are

---

$^{23}$ For simplicity consider a two-period model so that the fundamental value is the expected payoff at time 2 discounted at the required return, $V = \frac{E(P_2)}{1+k}$ , where $k$ is the required return. The alpha of the security, that is, the expected excess return above the required return is then

$$
\alpha = E\left(\frac{P_2}{P_1}\right) - 1 - k = \frac{V - P_1}{P_1}(1 + k).
$$

Naturally, the alpha depends on the difference between the fundamental value $V$ and the price $P_1$ . Since our measures of quality and price are based on z-scores, we simply subtract the two (rather than dividing by price as above).

$\copyright$ Springer

---

# Page 39

72

C. S. Asness et al.

more volatile. Moreover, controlling for QMJ, the size effect becomes large and highly significant in both samples. The size effect is alive and well when we account for quality as small stocks outperform large stocks when we compare firms of similar quality (and market beta, value, and momentum exposures). This finding in return space is the analog of the strong size effect for prices that we documented in Table 2. Asness et al. (2018) further analyze the size effect when controlling for quality.

Table 9 further shows that HML has a negative loading on QMJ. This is also intuitive, as cheap stocks (with high book-to-market) are naturally lower quality than expensive stocks. This negative loading implies that controlling for QMJ increases the alpha of HML, strengthening the value effect.

The Appendix contains further tests. Indeed, Tables 20, 21, and 22 analyze different combinations of size (SMB), value (HML), momentum (UMD), investments (CMA), profitability (RMW), and betting against beta (BAB). The results show, for instance, that controlling for quality eliminates the alpha of RMW.

To summarize, quality stocks, despite earning on average higher returns, appear safer, not riskier, than junk stocks in terms of their market, size, and value exposures. As a result, these factors’ alphas increase when we control for quality, since they, too, load negative on QMJ. At the same time, quality can explain other factors, such as RMW, and possibly other factors related to quality or mispricing.

## 6.3 QMJ: alternative definition based on profitability, growth, safety and payout

Table 23 in the Appendix reports returns of QMJ factors that include an explicit payout component. All our results are robust to this alternative specification. The relevance of payout for asset prices is discussed in footnotes 2 and 12.

## 7 Conclusion

We define a quality security as one that has characteristics that should command a higher (scaled) price. We present a dynamic valuation model, which shows how stock prices should increase in their quality characteristics, profitability, growth, and safety. We create empirical counterparts of each quality sub-component and quality in general, which are robust and inclusive from across the literature, testing the hypothesis that high-quality firms have higher scaled prices.

Consistent with the theory, we find that high-quality firms do exhibit higher prices, on average. However, the explanatory power of quality on prices is low, leaving the majority of cross-sectional dispersion in scaled prices unexplained. As a result, high quality firms exhibit high risk-adjusted returns. A quality-minus-junk (QMJ) factor that goes long high-quality stocks and shorts low-quality stocks earns significant risk-adjusted returns with an information ratio above 1 (i.e., a Sharpe ratio above 1 after hedging its other factor exposures) in the United States and globally across 24 countries.

Our results are consistent with quality stocks being underpriced and junk stocks overpriced or, alternatively, with quality stocks being riskier than junk stocks. However, while one can never rule out a risk explanation for the high return of quality stocks, we are unable to identify this risk; in anything, we find evidence of the opposite. We show that quality stocks are low beta, and, rather than exhibiting crash risk, they, if anything, benefit from flight

$\copyright$ Springer

---

# Page 40

Quality minus junk

73

to quality, that is, they have a tendency to perform well during periods of extreme market distress. These findings present a challenge for risk-based explanations. To test the mispricing hypothesis, we consider analysts’ expectations. Analysts’ expectations are consistent with the idea that high-quality stocks deserve higher prices. However, analysts expect high-quality stocks to deliver lower returns than junk stocks, contrary to the ex post realized returns. Analysts’ earnings forecasts also suggest errors in expectations that vary systematically with quality. This evidence of systematic analyst errors is consistent with the mispricing hypothesis that the price of quality is too low.

Finally, we show that the price of quality varies over time, generating a time-varying expected return on quality-minus-junk portfolios: a low price of quality predicts a high future return of quality stocks relative to junk stocks.

In summary, we document strong and consistent abnormal returns to quality and do so in a far more inclusive and complete setting than prior papers simultaneously using all quality components implied by our theoretical model. We also tie these results to the cross section and time series of the pricing of quality in novel ways. Our results present an important puzzle for asset pricing: we cannot tie the returns of quality to risk or, in a highly related finding, demonstrate that prices cross-sectionally vary “enough” with quality measures. At this point the returns to quality must be either an anomaly, data mining (incredibly robust data mining, including across countries, size, and periods, and out-of-sample, relative to the first draft of the paper) or the results of a still-to-be-identified risk factor.

**Acknowledgements** We thank Richard Sloan (the editor), Peter Ove Christensen, Antti Ilmanen, Ronen Israel, Johnny Kang, Charles Lee, John Liew, Toby Moskowitz, Per Olsson, Thomas Plenborg, Scott Richardson, Richard Thaler, and Tuomo Vuolteenaho for helpful comments as well as seminar participants at Harvard University, Harvard Business School; University of Bocconi; and conference participants in the NBER Asset Pricing Meeting 2013, the NBER Behavioral Economics Meeting 2013, and the SIFR Institute of Financial Research Conference on Re-Thinking Beta. AQR Capital Management is a global investment management firm, which may or may not apply similar investment techniques or methods of analysis as described herein. The views expressed here are those of the authors and not necessarily those of AQR.

## Appendix 1

### Variable definitions

In this section, we report details of each variable used on our quality score. Our variables’ definitions are based on Altman (1968); Ohlson (1980); Ang et al. (2006); Daniel and Titman (2006); Penman et al. (2007); Campbell et al. (2008); Novy-Marx (2012); Frazzini and Pedersen (2014); and Asness and Frazzini (2013). Variable names correspond to CRSP and Compustat data items, and we omit the time subscript $t$ for contemporaneous variables. Finally, unless specified, Compustat data items refer to annual items, and time subscripts refer to years. To compute the z-score of a variable $x$ at time $t$ , we rank $x$ cross-sectionally in ascending order

$$
r_x = \text{rank}(x)
$$

The cross-sectional ranks are rescaled to have a zero cross-sectional mean and a cross-sectional standard deviation of one:

$$
z(x) = z_x = \left[ r_x - \bar{r}_x \right] / \sigma(r_x).
$$

$\text{Springer}$

---

# Page 41

74

C. S. Asness et al.

**Profitability** We compute a profitability z-score by averaging z-scores of various measures of profitability. For cross-sectional comparisons, we get the same result whether we use our measures of profitability or residual profitability since these measures only differ by the common risk-free rate (but this is not true when we consider growth below).

Specifically, we consider gross profits over assets (GPOA), return on equity (ROE), return on assets (ROA), cash flow over assets (CFOA), gross margin (GMAR), and low accruals (ACC):

$$
Profitability = z(z_{gpoa} + z_{roe} + z_{roa} + z_{cfoa} + z_{gmar} + z_{acc}).
$$

GPOA is equal to revenue minus costs of goods sold divided by total assets ( $REVT - COGS)/AT$ . ROE is net income divided by book-equity $IB/BE$ . ROA is net income divided by total assets $IB/AT$ . CFOA is net income plus depreciation minus changes in working capital and capital expenditures divided by total assets: $(NB + DP - \Delta WC - CAPX)/AT$ . GMAR is revenue minus costs of goods sold divided by total sales: $(REVT - COGS)/SALE$ . ACC is depreciation minus changes in working capital $-(\Delta WC - DP)/AT$ . Working capital $WC$ is defined as current assets minus current liabilities minus cash and short-term instruments plus short-term debt and income taxes payable $ACT - LCT - CHE + DLC + TXP$ . Book equity $BE$ is defined as shareholders’ equity minus preferred stock. To obtain shareholders’ equity, we use stockholders’ equity ( $SEQ$ ), but if it is not available, we use the sum of common equity ( $CEQ$ ) and preferred stock ( $PSTK$ ). If both $SEQ$ and $CEQ$ are unavailable, we proxy shareholders’ equity by total assets ( $AT$ ) minus the sum of total liability ( $LT$ ) and minority interest ( $MIB$ ). To obtain book equity ( $BE$ ), we subtract from shareholders’ equity the preferred stock value ( $PSTKRV$ , $PSTKL$ , or $PSTK$ depending on availability).

**Growth** We compute a growth z-score by averaging z-scores of various measures of five-year growth in residual profits:

$$
Growth = z(z_{\Delta gpoa} + z_{\Delta roe} + z_{\Delta roa} + z_{\Delta cfoa} + z_{\Delta gmar}).
$$

First, we compute growth in residual gross profits over assets $[(gp_t - r^f at_{t-1}) - (gp_{t-5} - r^f at_{t-6})]/at_{t-5}$ , where $GP = REVT - COGS$ and lowercase indicates quantities per share. For example, for any accounting measure $X$ , we let $x \equiv X/S$ , using the split-adjusted number of shares outstanding $S$ . Similarly, we compute five-year growth in residual return on equity $[(ib_t - r^f be_{t-1}) - (ib_{t-5} - r^f be_{t-6})]/be_{t-5}$ , five-year growth in residual return over assets $[(ib_t - r^f a_{t-1}) - (ib_{t-5} - r^f a_{t-6})]/a_{t-5}$ , five-year growth in residual cash flow over assets $[(cf_t - r^f a_{t-1}) - (cf_{t-5} - r^f a_{t-6})]/at_{t-5}$ where $CF = IB + DP - \Delta WC - CAPX$ , and five-year growth in gross margin $(gp_t - gp_{t-5})/sale_{t-5}$ .

**Safety** We compute a safety z-score by averaging z-scores of low beta (BAB), low leverage (LEV), low bankruptcy risk (Ohlson’s O and Altman’s Z), and low earnings volatility (EVOL):

$$
Safety = z(z_{bab} + z_{lev} + z_o + z_z + z_{evol}).
$$

$BAB$ is equal to minus market beta $-\beta$ . Betas are estimated as in Frazzini and Pedersen (2014) based on the product of the rolling one-year daily standard deviation and the

$\copyright$ Springer

---

# Page 42

Quality minus junk

75

rolling five-year three-day correlations. For correlations, we use three-day returns to account for nonsynchronous trading and a longer horizon because correlations are more stable than volatilities. $LEV$ is minus total debt (the sum of long-term debt, short-term debt, minority interest, and preferred stock) over total assets $-(DLTT + DLC + MIBT + PSTK)/AT$ . We compute Ohlson’s O-Score as

$$
O = -\left( -1.32 - 0.407 \cdot \log\left( \frac{ADJASSET}{CPI} \right) + 6.03 \cdot TLTA - 1.43 \cdot WCTA \right. \\
\left. + 0.076 \cdot CLCA - 1.72 \cdot OENEG - 2.37 \cdot NITA - 1.83 \cdot FUTL \right. \\
\left. + 0.285 \cdot INTWO - 0.521 \cdot CHIN \right),
$$

where $ADJASSET$ is adjusted total assets equal to total assets plus 10% of the difference between book equity and market equity $AT + .1 * (ME - BE)$ . $CPI$ is the consumer price index. $TLTA$ is equal to book value of debt $(DLC + DLTT)$ divided by $ADJASSET$ . $WCTA$ is current assets minus current liabilities scaled by adjusted assets $(ACT - LCT)/ADJASSET$ . $CLCA$ is current liabilities divided by current assets $LCT/ACT$ . $OENEG$ is a dummy equal to 1 if total liabilities exceed total assets $1(LT > AT)$ . $NITA$ is net income over assets $IB/AT$ . $FUTL$ is pre-tax income over total liabilities $PT/LT$ . $INTWO$ is a dummy equal to one if net income is negative for the current and prior fiscal year $1(MAX\{IB_t, IB_{t-1}\} < 0)$ . $CHIN$ is changes in net income, defined as $(IB_t - IB_{t-1})/(|IB|_t + |IB_{t-1}|)$ . Altman’s Z-Score is a weighted average of working capital, retained earnings, earnings before interest and taxes, market equity, and sales, all over total assets:

$$
Z = (1.2 \cdot WC + 1.4 \cdot RE + 3.3 \cdot EBIT + 0.6 \cdot ME + SALE)/AT.
$$

$EVOL$ is the standard deviation of quarterly $ROE$ over the past 60 quarters. We require at least 12 nonmissing quarters. If quarterly data is unavailable we use the standard deviation of annual $ROE$ over the past 5 yrs, and we require five nonmissing fiscal years. $^{24}$

**Quality** We combine the three measures into a single quality score:

$$
Quality = z(Profitability + Growth + Safety).
$$

**Payout** We also compute QMJ factors that include an explicit payout component. We compute a payout z-score by averaging z-scores of net equity issuance ( $EISS$ ), net debt issuance ( $DISS$ ), and total net payout over profits ( $NPOP$ ):

$$
Payout = z(z_{eiss} + z_{diss} + z_{npop}).
$$

$EISS$ is minus one-year percentage change in split-adjusted number of shares $-\log(SHROUT\_ADJ_t/SHROUT\_ADJ_{t-1})$ , where $SHROUT\_ADJ$ is split-adjusted shares outstanding. $DISS$ is minus one-year percentage change in total debt $-\log(TOTD_t/TOTD_{t-1})$ , where $TOTD$ is the sum of long-term debt, short-term debt, minority interest, and preferred stock, $DLTT + DLC + MIBT + PSTK$ . $NPOP$ is equal the sum of total net payout (net income minus changes in book equity $IB - \Delta BE$ ) over the past 5 yrs divided by total profits ( $RETV - COGS$ ) over the past 5 yrs.

---

$^{24}$ Quarterly data is unavailable for countries in our global sample.

$\copyright$ Springer

---

# Page 43

76

C. S. Asness et al.

---

**Quality (alternative definition including payout)** We combine the four measures into a single quality score:

$$
Quality_{alt\ def} = z(Profitability + Growth + Safety + Payout).
$$

---

### Global factor returns

In this section, we report details of the construction of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios used on the analysis. The data can be downloaded at https://www.aqr.com/library/data-sets/quality-minus-junk-factors-monthly. The portfolio construction follows Fama and French (1993) and Asness and Frazzini (2013). We form one set of portfolios in each country and compute global factor portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. The market factor MKT is the value-weighted return on all available stocks minus the one-month Treasury bill rate. The size, value, and momentum factors are constructed using six value-weighted portfolios formed on size (market value of equity ME) and book-to-market (book equity divided by the most recent market equity $BE/ME$ ) and one-year return (return over the prior 12 months, skipping the most recent month). At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For our international sample, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on the second variable. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The size factor SMB is the average return on the three small portfolios minus the average return on the three big portfolios:

$$
SMB = 1/3(Small\ Value + Small\ Neutral + Small\ Growth.) \\
- \frac{1}{3}(Big\ Value + Big\ Neutral + Big\ Growth).
$$

The value factors HML is the average return on the two value portfolios minus the average return on the two growth portfolios:

$$
HML = 1/2(Small\ Value + Big\ Value) - 1/2(Small\ Growth + Big\ Growth).
$$

The momentum factor UMD is the average return on the two high return portfolios minus the average return on the two low return portfolios:

$$
UMD = 1/2(Small\ High + Big\ High) - 1/2(Small\ Low + Big\ Low).
$$

Portfolio returns are in U.S. dollars and do not include any currency hedging. Excess returns are over the U.S. Treasury bill rate.

---

Springer

---

# Page 44

Quality minus junk

77

Table 10 Summary statistics and data sources

<table>
  <thead>
    <tr>
      <th>Panel A. Summary Statistics</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Code</td>
      <td>Country</td>
      <td>Total number of stocks</td>
      <td>Average number of stocks</td>
      <td>Average Firm size (Billion-USD)</td>
      <td>Average Global Market Weight</td>
      <td>Start Date</td>
      <td>End Date</td>
    </tr>
    <tr>
      <td>AUS</td>
      <td>Australia</td>
      <td>2822</td>
      <td>1265</td>
      <td>0.69</td>
      <td>0.027</td>
      <td>199606</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>AUT</td>
      <td>Austria</td>
      <td>166</td>
      <td>82</td>
      <td>1.05</td>
      <td>0.003</td>
      <td>199606</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>BEL</td>
      <td>Belgium</td>
      <td>282</td>
      <td>136</td>
      <td>1.90</td>
      <td>0.008</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>CAN</td>
      <td>Canada</td>
      <td>5242</td>
      <td>1703</td>
      <td>0.62</td>
      <td>0.040</td>
      <td>198906</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>CHE</td>
      <td>Switzerland</td>
      <td>427</td>
      <td>225</td>
      <td>3.57</td>
      <td>0.024</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>DEU</td>
      <td>Germany</td>
      <td>1564</td>
      <td>748</td>
      <td>1.72</td>
      <td>0.037</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>DNK</td>
      <td>Denmark</td>
      <td>324</td>
      <td>160</td>
      <td>1.03</td>
      <td>0.005</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>ESP</td>
      <td>Spain</td>
      <td>310</td>
      <td>145</td>
      <td>4.17</td>
      <td>0.018</td>
      <td>199706</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>FIN</td>
      <td>Finland</td>
      <td>213</td>
      <td>114</td>
      <td>1.58</td>
      <td>0.005</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>FRA</td>
      <td>France</td>
      <td>1591</td>
      <td>694</td>
      <td>2.38</td>
      <td>0.049</td>
      <td>199306</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>GBR</td>
      <td>United Kingdom</td>
      <td>4899</td>
      <td>1820</td>
      <td>1.54</td>
      <td>0.080</td>
      <td>200206</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>GRC</td>
      <td>Greece</td>
      <td>368</td>
      <td>251</td>
      <td>0.39</td>
      <td>0.003</td>
      <td>199606</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>HKG</td>
      <td>Hong Kong</td>
      <td>1980</td>
      <td>1024</td>
      <td>1.30</td>
      <td>0.042</td>
      <td>199706</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>IRL</td>
      <td>Ireland</td>
      <td>99</td>
      <td>46</td>
      <td>2.17</td>
      <td>0.003</td>
      <td>200206</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>ISR</td>
      <td>Israel</td>
      <td>611</td>
      <td>312</td>
      <td>0.45</td>
      <td>0.004</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>ITA</td>
      <td>Italy</td>
      <td>560</td>
      <td>250</td>
      <td>2.36</td>
      <td>0.018</td>
      <td>199306</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>JPN</td>
      <td>Japan</td>
      <td>5136</td>
      <td>3234</td>
      <td>1.16</td>
      <td>0.107</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>NLD</td>
      <td>Netherlands</td>
      <td>341</td>
      <td>168</td>
      <td>3.23</td>
      <td>0.014</td>
      <td>199506</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>NOR</td>
      <td>Norway</td>
      <td>526</td>
      <td>191</td>
      <td>1.00</td>
      <td>0.006</td>
      <td>199806</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>NZL</td>
      <td>New Zealand</td>
      <td>250</td>
      <td>116</td>
      <td>0.33</td>
      <td>0.001</td>
      <td>200006</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>PRT</td>
      <td>Portugal</td>
      <td>96</td>
      <td>54</td>
      <td>1.46</td>
      <td>0.002</td>
      <td>199606</td>
      <td>201612</td>
    </tr>
    <tr>
      <td>SGP</td>
      <td>Singapore</td>
      <td>1037</td>
      <td>545</td>
      <td>0.65</td>
      <td>0.011</td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 45

78

C. S. Asness et al.

<table>
  <thead>
    <tr>
      <th colspan="2">Table 10 (continued)</th>
      <th rowspan="2">333</th>
      <th rowspan="2">1.20</th>
      <th rowspan="2">0.012</th>
      <th rowspan="2">199606</th>
      <th rowspan="2">201612</th>
    </tr>
    <tr>
      <th>SWE</th>
      <th>Sweden</th>
    </tr>
    <tr>
      <th>USA</th>
      <th>United States</th>
      <td>4585</td>
      <td>1.58</td>
      <td>0.483</td>
      <td>195706</td>
      <td>201612</td>
    </tr>
    <tr>
      <th>Data Type</th>
      <th>Universe</th>
      <td></td>
      <td></td>
      <td></td>
      <td>Source</td>
      <td></td>
    </tr>
    <tr>
      <th>Pricing data</th>
      <th>Domestic</th>
      <td></td>
      <td>Date Range</td>
      <td>192601–196706</td>
      <td>CRSP</td>
      <td></td>
    </tr>
    <tr>
      <th colspan="7">Panel B. Pricing and Accounting Data Sources</th>
    </tr>
    <tr>
      <th>Pricing data</th>
      <th>Domestic</th>
      <td></td>
      <td></td>
      <td></td>
      <td>Merged CRSP/Compustat</td>
      <td></td>
    </tr>
    <tr>
      <th>Pricing data</th>
      <th>Domestic</th>
      <td></td>
      <td></td>
      <td></td>
      <td>Compustat</td>
      <td></td>
    </tr>
    <tr>
      <th>Pricing data</th>
      <th>International</th>
      <td></td>
      <td></td>
      <td></td>
      <td>Compustat</td>
      <td></td>
    </tr>
    <tr>
      <th>Accounting data</th>
      <th>Global</th>
      <td></td>
      <td></td>
      <td></td>
      <td>Compustat</td>
      <td></td>
    </tr>
    <tr>
      <th>Risk free rate</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>CRSP</td>
      <td></td>
    </tr>
    <tr>
      <th>Risk free rate</th>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Compustat</td>
      <td></td>
    </tr>
  </thead>
</table>

Panel A of this table shows summary statistics, and Panel B shows pricing and accounting data sources by period. Our sample consists of all common stocks traded in 24 developed markets between June 1957 and December 2016. The 24 markets in our sample correspond to union of all countries belonging to the MSCI World Developed Index over our sample period. Stock returns and accounting data are from the union of the Center for Research on Security Prices (CRSP) pricing database, the Compustat North America Fundamentals Annual, Fundamentals Quarterly and Security Daily databases, and the Compustat Global Fundamentals Annual, Fundamentals Quarterly and Security Daily databases. We assign individual issues to the corresponding market based on the location of the primary exchange. For companies traded in multiple markets, we use the primary trading vehicle identified by Compustat. We restrict the sample to common stocks (identified by a CRSP share code “shrcd” of 10 or 11 or a Compustat share code “tcp” of 0) and exclude securities trading on over-the-counter exchanges

Springer

---

# Page 46

Quality minus junk

79

Table 11 Future quality measures: persistence and predictive regressions

Panel A: Long Sample (U.S.) 6/1957–12/2016

<table>
  <thead>
    <tr>
      <th></th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
      <th>H-L t-stat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Profit (t)</td>
      <td>-1.43</td>
      <td>-0.81</td>
      <td>-0.49</td>
      <td>-0.23</td>
      <td>0.01</td>
      <td>0.24</td>
      <td>0.47</td>
      <td>0.74</td>
      <td>1.10</td>
      <td>1.74</td>
      <td>3.17</td>
      <td>63.53</td>
    </tr>
    <tr>
      <td>Profit (t + 12 M)</td>
      <td>-0.93</td>
      <td>-0.51</td>
      <td>-0.29</td>
      <td>-0.08</td>
      <td>0.09</td>
      <td>0.26</td>
      <td>0.43</td>
      <td>0.65</td>
      <td>0.96</td>
      <td>1.51</td>
      <td>2.43</td>
      <td>38.29</td>
    </tr>
    <tr>
      <td>Profit (t + 36 M)</td>
      <td>-0.66</td>
      <td>-0.38</td>
      <td>-0.23</td>
      <td>-0.04</td>
      <td>0.08</td>
      <td>0.21</td>
      <td>0.38</td>
      <td>0.53</td>
      <td>0.78</td>
      <td>1.37</td>
      <td>2.04</td>
      <td>25.97</td>
    </tr>
    <tr>
      <td>Profit (t + 60 M)</td>
      <td>-0.54</td>
      <td>-0.31</td>
      <td>-0.17</td>
      <td>-0.05</td>
      <td>0.09</td>
      <td>0.17</td>
      <td>0.31</td>
      <td>0.48</td>
      <td>0.66</td>
      <td>1.30</td>
      <td>1.83</td>
      <td>20.17</td>
    </tr>
    <tr>
      <td>Profit (t + 120 M)</td>
      <td>-0.38</td>
      <td>-0.23</td>
      <td>-0.11</td>
      <td>0.00</td>
      <td>0.10</td>
      <td>0.17</td>
      <td>0.30</td>
      <td>0.38</td>
      <td>0.60</td>
      <td>1.13</td>
      <td>1.54</td>
      <td>25.39</td>
    </tr>
    <tr>
      <td>Growth (t)</td>
      <td>-1.50</td>
      <td>-0.99</td>
      <td>-0.67</td>
      <td>-0.41</td>
      <td>-0.16</td>
      <td>0.08</td>
      <td>0.34</td>
      <td>0.62</td>
      <td>0.98</td>
      <td>1.57</td>
      <td>3.07</td>
      <td>99.03</td>
    </tr>
    <tr>
      <td>Growth (t + 12 M)</td>
      <td>-0.73</td>
      <td>-0.54</td>
      <td>-0.41</td>
      <td>-0.23</td>
      <td>-0.07</td>
      <td>0.05</td>
      <td>0.17</td>
      <td>0.42</td>
      <td>0.78</td>
      <td>1.22</td>
      <td>1.96</td>
      <td>30.11</td>
    </tr>
    <tr>
      <td>Growth (t + 36 M)</td>
      <td>-0.30</td>
      <td>-0.29</td>
      <td>-0.24</td>
      <td>-0.17</td>
      <td>-0.08</td>
      <td>-0.07</td>
      <td>0.05</td>
      <td>0.19</td>
      <td>0.46</td>
      <td>0.85</td>
      <td>1.15</td>
      <td>14.42</td>
    </tr>
    <tr>
      <td>Growth (t + 60 M)</td>
      <td>0.11</td>
      <td>-0.03</td>
      <td>-0.10</td>
      <td>-0.12</td>
      <td>-0.13</td>
      <td>-0.13</td>
      <td>-0.06</td>
      <td>0.03</td>
      <td>0.21</td>
      <td>0.50</td>
      <td>0.39</td>
      <td>4.23</td>
    </tr>
    <tr>
      <td>Growth (t + 120 M)</td>
      <td>-0.16</td>
      <td>-0.13</td>
      <td>-0.11</td>
      <td>-0.11</td>
      <td>-0.12</td>
      <td>-0.10</td>
      <td>-0.05</td>
      <td>0.01</td>
      <td>0.22</td>
      <td>0.40</td>
      <td>0.57</td>
      <td>6.12</td>
    </tr>
    <tr>
      <td>Safety (t)</td>
      <td>-1.52</td>
      <td>-0.90</td>
      <td>-0.55</td>
      <td>-0.28</td>
      <td>-0.05</td>
      <td>0.17</td>
      <td>0.39</td>
      <td>0.64</td>
      <td>0.94</td>
      <td>1.44</td>
      <td>2.96</td>
      <td>51.53</td>
    </tr>
    <tr>
      <td>Safety (t + 12 M)</td>
      <td>-1.20</td>
      <td>-0.72</td>
      <td>-0.45</td>
      <td>-0.22</td>
      <td>-0.03</td>
      <td>0.19</td>
      <td>0.36</td>
      <td>0.58</td>
      <td>0.87</td>
      <td>1.28</td>
      <td>2.49</td>
      <td>36.46</td>
    </tr>
    <tr>
      <td>Safety (t + 36 M)</td>
      <td>-0.87</td>
      <td>-0.55</td>
      <td>-0.33</td>
      <td>-0.17</td>
      <td>-0.01</td>
      <td>0.15</td>
      <td>0.30</td>
      <td>0.50</td>
      <td>0.74</td>
      <td>1.05</td>
      <td>1.95</td>
      <td>26.07</td>
    </tr>
    <tr>
      <td>Safety (t + 60 M)</td>
      <td>-0.67</td>
      <td>-0.41</td>
      <td>-0.24</td>
      <td>-0.12</td>
      <td>0.00</td>
      <td>0.14</td>
      <td>0.28</td>
      <td>0.45</td>
      <td>0.66</td>
      <td>0.93</td>
      <td>1.64</td>
      <td>18.45</td>
    </tr>
    <tr>
      <td>Safety (t + 120 M)</td>
      <td>-0.44</td>
      <td>-0.28</td>
      <td>-0.15</td>
      <td>-0.04</td>
      <td>0.06</td>
      <td>0.15</td>
      <td>0.24</td>
      <td>0.38</td>
      <td>0.59</td>
      <td>0.73</td>
      <td>1.17</td>
      <td>12.94</td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 47

80

C. S. Asness et al.

Table 11 (continued)

Panel B: Broad Sample (Global) 6/1989-12/2016

<table>
  <thead>
    <tr>
      <th></th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
      <th>H-L t-stat</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Profit (t)</td>
      <td>-1.49</td>
      <td>-0.87</td>
      <td>-0.53</td>
      <td>-0.25</td>
      <td>0.00</td>
      <td>0.24</td>
      <td>0.49</td>
      <td>0.77</td>
      <td>1.12</td>
      <td>1.70</td>
      <td>3.19</td>
      <td>103.27</td>
    </tr>
    <tr>
      <td>Profit (t + 12 M)</td>
      <td>-0.86</td>
      <td>-0.48</td>
      <td>-0.26</td>
      <td>-0.08</td>
      <td>0.08</td>
      <td>0.26</td>
      <td>0.44</td>
      <td>0.64</td>
      <td>0.95</td>
      <td>1.44</td>
      <td>2.30</td>
      <td>84.74</td>
    </tr>
    <tr>
      <td>Profit (t + 36 M)</td>
      <td>-0.57</td>
      <td>-0.34</td>
      <td>-0.17</td>
      <td>-0.04</td>
      <td>0.08</td>
      <td>0.23</td>
      <td>0.39</td>
      <td>0.55</td>
      <td>0.80</td>
      <td>1.29</td>
      <td>1.86</td>
      <td>30.52</td>
    </tr>
    <tr>
      <td>Profit (t + 60 M)</td>
      <td>-0.43</td>
      <td>-0.25</td>
      <td>-0.11</td>
      <td>0.01</td>
      <td>0.10</td>
      <td>0.23</td>
      <td>0.36</td>
      <td>0.50</td>
      <td>0.70</td>
      <td>1.19</td>
      <td>1.62</td>
      <td>26.82</td>
    </tr>
    <tr>
      <td>Profit (t + 120 M)</td>
      <td>-0.30</td>
      <td>-0.13</td>
      <td>-0.01</td>
      <td>0.06</td>
      <td>0.15</td>
      <td>0.23</td>
      <td>0.32</td>
      <td>0.43</td>
      <td>0.60</td>
      <td>0.98</td>
      <td>1.28</td>
      <td>19.33</td>
    </tr>
    <tr>
      <td>Growth (t)</td>
      <td>-1.55</td>
      <td>-1.03</td>
      <td>-0.70</td>
      <td>-0.42</td>
      <td>-0.16</td>
      <td>0.09</td>
      <td>0.36</td>
      <td>0.65</td>
      <td>1.01</td>
      <td>1.61</td>
      <td>3.15</td>
      <td>73.50</td>
    </tr>
    <tr>
      <td>Growth (t + 12 M)</td>
      <td>-0.72</td>
      <td>-0.49</td>
      <td>-0.37</td>
      <td>-0.21</td>
      <td>-0.06</td>
      <td>0.05</td>
      <td>0.19</td>
      <td>0.43</td>
      <td>0.72</td>
      <td>1.12</td>
      <td>1.83</td>
      <td>34.47</td>
    </tr>
    <tr>
      <td>Growth (t + 36 M)</td>
      <td>-0.26</td>
      <td>-0.19</td>
      <td>-0.17</td>
      <td>-0.15</td>
      <td>-0.06</td>
      <td>-0.02</td>
      <td>0.09</td>
      <td>0.21</td>
      <td>0.40</td>
      <td>0.73</td>
      <td>0.99</td>
      <td>15.64</td>
    </tr>
    <tr>
      <td>Growth (t + 60 M)</td>
      <td>0.27</td>
      <td>0.13</td>
      <td>-0.01</td>
      <td>-0.06</td>
      <td>-0.06</td>
      <td>-0.09</td>
      <td>-0.02</td>
      <td>0.03</td>
      <td>0.12</td>
      <td>0.33</td>
      <td>0.06</td>
      <td>0.74</td>
    </tr>
    <tr>
      <td>Growth (t + 120 M)</td>
      <td>-0.14</td>
      <td>-0.08</td>
      <td>-0.07</td>
      <td>-0.08</td>
      <td>-0.07</td>
      <td>-0.04</td>
      <td>-0.08</td>
      <td>0.02</td>
      <td>0.14</td>
      <td>0.20</td>
      <td>0.34</td>
      <td>6.34</td>
    </tr>
    <tr>
      <td>Safety (t)</td>
      <td>-1.65</td>
      <td>-0.99</td>
      <td>-0.63</td>
      <td>-0.34</td>
      <td>-0.08</td>
      <td>0.15</td>
      <td>0.39</td>
      <td>0.65</td>
      <td>0.96</td>
      <td>1.46</td>
      <td>3.12</td>
      <td>54.00</td>
    </tr>
    <tr>
      <td>Safety (t + 12 M)</td>
      <td>-1.35</td>
      <td>-0.84</td>
      <td>-0.54</td>
      <td>-0.29</td>
      <td>-0.09</td>
      <td>0.12</td>
      <td>0.32</td>
      <td>0.56</td>
      <td>0.83</td>
      <td>1.19</td>
      <td>2.54</td>
      <td>40.98</td>
    </tr>
    <tr>
      <td>Safety (t + 36 M)</td>
      <td>-1.05</td>
      <td>-0.69</td>
      <td>-0.46</td>
      <td>-0.26</td>
      <td>-0.08</td>
      <td>0.07</td>
      <td>0.22</td>
      <td>0.46</td>
      <td>0.68</td>
      <td>0.88</td>
      <td>1.93</td>
      <td>24.56</td>
    </tr>
    <tr>
      <td>Safety (t + 60 M)</td>
      <td>-0.84</td>
      <td>-0.56</td>
      <td>-0.37</td>
      <td>-0.20</td>
      <td>-0.07</td>
      <td>0.04</td>
      <td>0.20</td>
      <td>0.40</td>
      <td>0.58</td>
      <td>0.73</td>
      <td>1.58</td>
      <td>18.52</td>
    </tr>
    <tr>
      <td>Safety (t + 120 M)</td>
      <td>-0.52</td>
      <td>-0.35</td>
      <td>-0.23</td>
      <td>-0.10</td>
      <td>0.00</td>
      <td>0.05</td>
      <td>0.16</td>
      <td>0.30</td>
      <td>0.45</td>
      <td>0.54</td>
      <td>1.06</td>
      <td>10.80</td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 48

Quality minus junk

81

Table 11 (continued)

<table>
  <thead>
    <tr>
      <th>Panel C</th>
      <th>Long Sample (U.S., 6/1957–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th>Broad Sample (Global, 6/1989–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>t + 12 M</td>
      <td>t + 36 M</td>
      <td>t + 60 M</td>
      <td>t + 120 M</td>
      <td>t + 12 M</td>
      <td>t + 36 M</td>
      <td>t + 60 M</td>
      <td>t + 120 M</td>
    </tr>
    <tr>
      <td>Log (PB)</td>
      <td>0.14</td>
      <td>0.18</td>
      <td>0.08</td>
      <td>0.35</td>
      <td>0.10</td>
      <td>0.18</td>
      <td>0.04</td>
      <td>0.12</td>
    </tr>
    <tr>
      <td></td>
      <td>(8.40)</td>
      <td>(15.77)</td>
      <td>(3.57)</td>
      <td>(8.29)</td>
      <td>(2.21)</td>
      <td>(5.57)</td>
      <td>(2.53)</td>
      <td>(5.49)</td>
    </tr>
    <tr>
      <td>Quality</td>
      <td>0.68</td>
      <td>0.59</td>
      <td>0.48</td>
      <td></td>
      <td>0.30</td>
      <td>0.20</td>
      <td>0.32</td>
      <td>0.25</td>
    </tr>
    <tr>
      <td></td>
      <td>(99.04)</td>
      <td>(76.69)</td>
      <td>(36.75)</td>
      <td></td>
      <td>(15.33)</td>
      <td>(13.41)</td>
      <td>(34.25)</td>
      <td>(20.35)</td>
    </tr>
    <tr>
      <td>Firm size</td>
      <td></td>
      <td>−0.03</td>
      <td></td>
      <td>−0.05</td>
      <td></td>
      <td>−0.06</td>
      <td></td>
      <td>−0.03</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−4.06)</td>
      <td></td>
      <td>(−4.20)</td>
      <td></td>
      <td>(−4.36)</td>
      <td></td>
      <td>(−5.06)</td>
    </tr>
    <tr>
      <td>1-year return</td>
      <td></td>
      <td>0.15</td>
      <td></td>
      <td>0.09</td>
      <td></td>
      <td>0.03</td>
      <td></td>
      <td>−0.01</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(20.47)</td>
      <td></td>
      <td>(7.84)</td>
      <td></td>
      <td>(3.34)</td>
      <td></td>
      <td>(−1.69)</td>
    </tr>
    <tr>
      <td>Firm age</td>
      <td></td>
      <td>0.03</td>
      <td></td>
      <td>0.04</td>
      <td></td>
      <td>0.04</td>
      <td></td>
      <td>0.01</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(6.65)</td>
      <td></td>
      <td>(5.14)</td>
      <td></td>
      <td>(7.36)</td>
      <td></td>
      <td>(1.21)</td>
    </tr>
    <tr>
      <td>Profit Uncertainty</td>
      <td></td>
      <td>−0.08</td>
      <td></td>
      <td>−0.23</td>
      <td></td>
      <td>−0.13</td>
      <td></td>
      <td>−0.13</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−4.73)</td>
      <td></td>
      <td>(−10.01)</td>
      <td></td>
      <td>(−5.68)</td>
      <td></td>
      <td>(−9.43)</td>
    </tr>
    <tr>
      <td>Dividend payer</td>
      <td></td>
      <td>0.10</td>
      <td></td>
      <td>0.23</td>
      <td></td>
      <td>0.16</td>
      <td></td>
      <td>0.10</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(7.80)</td>
      <td></td>
      <td>(10.35)</td>
      <td></td>
      <td>(7.36)</td>
      <td></td>
      <td>(16.94)</td>
    </tr>
    <tr>
      <td>Profit Uncertainty x Dividend payer</td>
      <td></td>
      <td>0.00</td>
      <td></td>
      <td>0.02</td>
      <td></td>
      <td>−0.01</td>
      <td></td>
      <td>0.03</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−0.17)</td>
      <td></td>
      <td>(0.93)</td>
      <td></td>
      <td>(−0.52)</td>
      <td></td>
      <td>(0.97)</td>
    </tr>
    <tr>
      <td>Average AdjR2</td>
      <td>0.53</td>
      <td>0.61</td>
      <td>0.27</td>
      <td>0.29</td>
      <td>0.14</td>
      <td>0.27</td>
      <td>0.13</td>
      <td>0.26</td>
    </tr>
    <tr>
      <td>Nobs (years)</td>
      <td>59</td>
      <td>53</td>
      <td>57</td>
      <td>51</td>
      <td>54</td>
      <td>49</td>
      <td>45</td>
      <td>44</td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 49

82

C. S. Asness et al.

<table>
  <tr>
    <th>Table II (continued)</th>
    <th></th>
    <th></th>
    <th></th>
    <th></th>
    <th></th>
    <th></th>
    <th></th>
    <th></th>
    <th></th>
  </tr>
  <tr>
    <td>Industry FE</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
  </tr>
  <tr>
    <td>Country FE</td>
    <td></td>
    <td></td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
    <td>X</td>
  </tr>
  <tr>
    <td>Panels A and B: Persistence of Quality Measures</td>
    <td colspan="9">Panel A (U.S.) and Panel B (global) show the average quality scores over time. Each calendar month, stocks in each country in are ranked in ascending order on the basis of their quality score. The ranked stocks are assigned to one of 10 portfolios. U.S. sorts are based on NYSE breakpoints. This table reports each portfolio’s quality score at portfolio formation (date $t$) up to the subsequent 10 yrs (date $t+120$ months). We report the time-series average of the value-weighted cross sectional means. Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1989 to December 2016. Standard errors are adjusted for heteroskedasticity and autocorrelation with a lag length of 5 yrs (Newey and West 1987), and 5% significance is indicated in bold</td>
  </tr>
  <tr>
    <td>Panel C: Predicting Future Quality with Lagged Price-to-Book.</td>
    <td colspan="9">Panel C This table reports results from annual Fama-Macbeth regressions. The dependent variable is a firm quality score at month $t+k$ months. The explanatory variables are the log of firm’s market-to-book ratio in June of each calendar year (date $t$), the quality scores on date $t$, and a series of controls. “Firm size” is the log of the firm’s market capitalization; “one-year return” is the firm’s stock return over the prior year. “Firm age” is the cumulative number of years since the firm’s IPO. “Uncertainty about mean profitability” (Pastor and Veronesi 2003) is the standard deviation of the residuals of an AR(1) model for each firm’s ROE, using the longest continuous series of a firm’s valid annual ROE up to date $t$. We require a minimum of 5 yrs of nonmissing ROEs. “Dividend payer” is a dummy equal to one if the firm paid any dividends over the prior year. With the exception of the “Dividend payer” dummy, all explanatory variables at time $t$ are ranked cross-sectionally and rescaled to have a zero cross-sectional mean and a cross-sectional standard deviation of one. Industry, country, or firm fixed effects are included when indicated (“Industry FE,” “Country FE,” “Firm FE”), “Average AdjR2” is the time-series average of the adjusted R-squared of the cross-sectional regression. Standard errors are adjusted for heteroskedasticity and autocorrelation (Newey and West 1987) with a lag length of 5 yrs. T-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold</td>
  </tr>
</table>

Springer

---

# Page 50

Quality minus junk

83

Table 12 The price of quality: alternative specifications

<table>
  <thead>
    <tr>
      <th rowspan="2">Panel A: Long Sample (U.S., 6/1957–12/2016)</th>
      <th colspan="12">Panel B: Broad Sample (Global, 6/1989–12/2016)</th>
      <th colspan="12">Broad Sample (Global, 6/1989–12/2016)</th>
    </tr>
    <tr>
      <th>(1)</th>
      <th>(2)</th>
      <th>(3)</th>
      <th>(4)</th>
      <th>(5)</th>
      <th>(6)</th>
      <th>(7)</th>
      <th>(8)</th>
      <th>(9)</th>
      <th>(10)</th>
      <th>(11)</th>
      <th>(12)</th>
      <th>(1)</th>
      <th>(2)</th>
      <th>(3)</th>
      <th>(4)</th>
      <th>(5)</th>
      <th>(6)</th>
      <th>(7)</th>
      <th>(8)</th>
      <th>(9)</th>
      <th>(10)</th>
      <th>(11)</th>
      <th>(12)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Quality</td>
      <td>0.24</td>
      <td>0.26</td>
      <td>0.26</td>
      <td>0.24</td>
      <td>0.23</td>
      <td>0.10</td>
      <td>0.19</td>
      <td>0.22</td>
      <td>0.19</td>
      <td>0.19</td>
      <td>0.20</td>
      <td>0.07</td>
      <td>0.19</td>
      <td>0.20</td>
      <td>0.24</td>
      <td>0.23</td>
      <td>0.23</td>
      <td>0.23</td>
      <td>0.23</td>
      <td>0.23</td>
      <td>0.23</td>
      <td>0.23</td>
      <td>0.23</td>
    </tr>
    <tr>
      <td></td>
      <td>(13.09)</td>
      <td>(26.17)</td>
      <td>(12.93)</td>
      <td>(15.06)</td>
      <td>(14.15)</td>
      <td>(10.97)</td>
      <td>(13.36)</td>
      <td>(21.68)</td>
      <td>(14.10)</td>
      <td>(20.23)</td>
      <td>(8.84)</td>
      <td>(12.59)</td>
      <td>(13.36)</td>
      <td>(21.68)</td>
      <td>(14.10)</td>
      <td>(20.23)</td>
      <td>(8.84)</td>
      <td>(12.59)</td>
      <td>(13.36)</td>
      <td>(21.68)</td>
      <td>(14.10)</td>
      <td>(20.23)</td>
      <td>(8.84)</td>
    </tr>
    <tr>
      <td>Firm size</td>
      <td></td>
      <td>0.37</td>
      <td></td>
      <td>0.36</td>
      <td></td>
      <td>0.80</td>
      <td></td>
      <td>0.38</td>
      <td></td>
      <td>0.37</td>
      <td></td>
      <td>0.79</td>
      <td></td>
      <td>0.38</td>
      <td></td>
      <td>0.37</td>
      <td></td>
      <td>0.37</td>
      <td></td>
      <td>0.38</td>
      <td></td>
      <td>0.37</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(20.17)</td>
      <td></td>
      <td>(19.37)</td>
      <td></td>
      <td>(21.55)</td>
      <td></td>
      <td>(12.57)</td>
      <td></td>
      <td>(12.83)</td>
      <td></td>
      <td>(17.10)</td>
      <td></td>
      <td>(12.57)</td>
      <td></td>
      <td>(12.83)</td>
      <td></td>
      <td>(17.10)</td>
      <td></td>
      <td>(12.57)</td>
      <td></td>
      <td>(12.83)</td>
      <td></td>
    </tr>
    <tr>
      <td>1-year return</td>
      <td></td>
      <td>0.24</td>
      <td></td>
      <td>0.24</td>
      <td></td>
      <td>0.20</td>
      <td></td>
      <td>0.30</td>
      <td></td>
      <td>0.30</td>
      <td></td>
      <td>0.24</td>
      <td></td>
      <td>0.30</td>
      <td></td>
      <td>0.30</td>
      <td></td>
      <td>0.30</td>
      <td></td>
      <td>0.30</td>
      <td></td>
      <td>0.30</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(13.80)</td>
      <td></td>
      <td>(13.62)</td>
      <td></td>
      <td>(15.28)</td>
      <td></td>
      <td>(21.81)</td>
      <td></td>
      <td>(23.02)</td>
      <td></td>
      <td>(39.89)</td>
      <td></td>
      <td>(21.81)</td>
      <td></td>
      <td>(23.02)</td>
      <td></td>
      <td>(39.89)</td>
      <td></td>
      <td>(21.81)</td>
      <td></td>
      <td>(23.02)</td>
      <td></td>
    </tr>
    <tr>
      <td>Firm age</td>
      <td></td>
      <td>-0.19</td>
      <td></td>
      <td>-0.18</td>
      <td></td>
      <td>-0.17</td>
      <td></td>
      <td>-0.14</td>
      <td></td>
      <td>-0.12</td>
      <td></td>
      <td>-0.16</td>
      <td></td>
      <td>-0.14</td>
      <td></td>
      <td>-0.12</td>
      <td></td>
      <td>-0.16</td>
      <td></td>
      <td>-0.14</td>
      <td></td>
      <td>-0.12</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(-8.32)</td>
      <td></td>
      <td>(-7.41)</td>
      <td></td>
      <td>(-6.07)</td>
      <td></td>
      <td>(-5.61)</td>
      <td></td>
      <td>(-5.25)</td>
      <td></td>
      <td>(-5.46)</td>
      <td></td>
      <td>(-5.61)</td>
      <td></td>
      <td>(-5.25)</td>
      <td></td>
      <td>(-5.46)</td>
      <td></td>
      <td>(-5.61)</td>
      <td></td>
      <td>(-5.25)</td>
      <td></td>
    </tr>
    <tr>
      <td>Profit</td>
      <td></td>
      <td>0.38</td>
      <td></td>
      <td>0.36</td>
      <td></td>
      <td>0.38</td>
      <td></td>
      <td>0.42</td>
      <td></td>
      <td>0.36</td>
      <td></td>
      <td>0.46</td>
      <td></td>
      <td>0.42</td>
      <td></td>
      <td>0.36</td>
      <td></td>
      <td>0.46</td>
      <td></td>
      <td>0.42</td>
      <td></td>
      <td>0.36</td>
      <td></td>
    </tr>
    <tr>
      <td>Uncertainty</td>
      <td></td>
      <td>(15.83)</td>
      <td></td>
      <td>(14.34)</td>
      <td></td>
      <td>(10.39)</td>
      <td></td>
      <td>(29.61)</td>
      <td></td>
      <td>(20.41)</td>
      <td></td>
      <td>(33.69)</td>
      <td></td>
      <td>(29.61)</td>
      <td></td>
      <td>(20.41)</td>
      <td></td>
      <td>(33.69)</td>
      <td></td>
      <td>(29.61)</td>
      <td></td>
      <td>(20.41)</td>
      <td></td>
    </tr>
    <tr>
      <td>Dividend payer</td>
      <td></td>
      <td>(-0.16)</td>
      <td></td>
      <td>(-0.09)</td>
      <td></td>
      <td>(-0.01)</td>
      <td></td>
      <td>(-0.21)</td>
      <td></td>
      <td>(-0.12)</td>
      <td></td>
      <td>(0.07)</td>
      <td></td>
      <td>(-0.21)</td>
      <td></td>
      <td>(-0.12)</td>
      <td></td>
      <td>(0.07)</td>
      <td></td>
      <td>(-0.21)</td>
      <td></td>
      <td>(-0.12)</td>
      <td></td>
    </tr>
    <tr>
      <td>Profit Uncertainty</td>
      <td></td>
      <td>(-7.32)</td>
      <td></td>
      <td>(-3.85)</td>
      <td></td>
      <td>(-0.38)</td>
      <td></td>
      <td>(-6.68)</td>
      <td></td>
      <td>(-3.42)</td>
      <td></td>
      <td>(2.17)</td>
      <td></td>
      <td>(-6.68)</td>
      <td></td>
      <td>(-3.42)</td>
      <td></td>
      <td>(2.17)</td>
      <td></td>
      <td>(-6.68)</td>
      <td></td>
      <td>(-3.42)</td>
      <td></td>
    </tr>
    <tr>
      <td>x Dividend payer</td>
      <td></td>
      <td>-0.20</td>
      <td></td>
      <td>-0.20</td>
      <td></td>
      <td>-0.15</td>
      <td></td>
      <td>-0.23</td>
      <td></td>
      <td>-0.20</td>
      <td></td>
      <td>-0.19</td>
      <td></td>
      <td>-0.23</td>
      <td></td>
      <td>-0.20</td>
      <td></td>
      <td>-0.19</td>
      <td></td>
      <td>-0.23</td>
      <td></td>
      <td>-0.20</td>
      <td></td>
    </tr>
    <tr>
      <td>Average AdjR2</td>
      <td></td>
      <td>(-10.51)</td>
      <td></td>
      <td>(-7.41)</td>
      <td></td>
      <td>(-6.72)</td>
      <td></td>
      <td>(-16.64)</td>
      <td></td>
      <td>(-8.58)</td>
      <td></td>
      <td>(-9.94)</td>
      <td></td>
      <td>(-16.64)</td>
      <td></td>
      <td>(-8.58)</td>
      <td></td>
      <td>(-9.94)</td>
      <td></td>
      <td>(-16.64)</td>
      <td></td>
      <td>(-8.58)</td>
      <td></td>
    </tr>
    <tr>
      <td>Nobs (months)</td>
      <td>0.09</td>
      <td>0.43</td>
      <td>0.25</td>
      <td>0.50</td>
      <td>0.06</td>
      <td>0.46</td>
      <td>0.10</td>
      <td>0.39</td>
      <td>0.20</td>
      <td>0.45</td>
      <td>0.04</td>
      <td>0.42</td>
      <td>0.10</td>
      <td>0.39</td>
      <td>0.20</td>
      <td>0.45</td>
      <td>0.04</td>
      <td>0.42</td>
      <td>0.10</td>
      <td>0.39</td>
      <td>0.20</td>
      <td>0.45</td>
      <td>0.04</td>
    </tr>
    <tr>
      <td>Industry FE</td>
      <td>715</td>
      <td>648</td>
      <td>715</td>
      <td>648</td>
      <td>715</td>
      <td>648</td>
      <td>331</td>
      <td>331</td>
      <td>331</td>
      <td>331</td>
      <td>331</td>
      <td>331</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
    </tr>
    <tr>
      <td>Country FE</td>
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
      <td></td>
      <td></td>
     

---

# Page 51

84

C. S. Asness et al.

Table 12 (continued)

<table>
  <thead>
    <tr>
      <th></th>
      <th>0.31</th>
      <th>0.29</th>
      <th>0.31</th>
      <th>0.17</th>
      <th>0.20</th>
      <th>0.38</th>
      <th>0.17</th>
      <th>0.42</th>
      <th>0.34</th>
      <th>0.27</th>
      <th>0.27</th>
      <th>0.18</th>
      <th>0.18</th>
      <th>0.12</th>
      <th>0.03</th>
      <th>0.13</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Profit Uncertainty</td>
      <td>(4.27)</td>
      <td>(5.29)</td>
      <td>(7.08)</td>
      <td>(-0.70)</td>
      <td>(3.22)</td>
      <td>(2.91)</td>
      <td>(-0.60)</td>
      <td>(3.40)</td>
      <td>(2.06)</td>
      <td>(0.57)</td>
      <td>(27.55)</td>
      <td>(28.43)</td>
      <td>(15.93)</td>
      <td>(15.08)</td>
      <td>(10.52)</td>
      <td>(7.71)</td>
    </tr>
    <tr>
      <td>Dividend payer</td>
      <td>-0.09</td>
      <td>-0.04</td>
      <td>-0.04</td>
      <td>-1.33</td>
      <td>0.09</td>
      <td>-0.07</td>
      <td>-0.52</td>
      <td>0.00</td>
      <td>0.16</td>
      <td>-0.01</td>
      <td>-0.08</td>
      <td>-0.09</td>
      <td>-0.14</td>
      <td>-0.12</td>
      <td>-0.09</td>
      <td>-0.13</td>
    </tr>
    <tr>
      <td></td>
      <td>(-2.23)</td>
      <td>(-0.64)</td>
      <td>(-0.52)</td>
      <td>(-1.12)</td>
      <td>(0.72)</td>
      <td>(-1.23)</td>
      <td>(-2.10)</td>
      <td>(-0.05)</td>
      <td>(0.64)</td>
      <td>(-0.03)</td>
      <td>(-1.48)</td>
      <td>(-3.08)</td>
      <td>(-3.59)</td>
      <td>(-2.55)</td>
      <td>(-2.18)</td>
      <td>(-3.21)</td>
    </tr>
    <tr>
      <td>Profit Uncertainty</td>
      <td>-0.11</td>
      <td>-0.16</td>
      <td>-0.13</td>
      <td>0.72</td>
      <td>-0.17</td>
      <td>-0.05</td>
      <td>0.21</td>
      <td>-0.10</td>
      <td>-0.29</td>
      <td>-0.06</td>
      <td>-0.17</td>
      <td>-0.15</td>
      <td>-0.11</td>
      <td>-0.10</td>
      <td>-0.09</td>
      <td>-0.06</td>
    </tr>
    <tr>
      <td>x Dividend payer</td>
      <td>(-1.62)</td>
      <td>(-2.93)</td>
      <td>(-3.09)</td>
      <td>(0.89)</td>
      <td>(-1.98)</td>
      <td>(-0.85)</td>
      <td>(1.21)</td>
      <td>(-1.81)</td>
      <td>(-1.63)</td>
      <td>(-0.22)</td>
      <td>(-9.82)</td>
      <td>(-9.65)</td>
      <td>(-4.95)</td>
      <td>(-3.54)</td>
      <td>(-7.18)</td>
      <td>(-5.59)</td>
    </tr>
    <tr>
      <td>Average R2</td>
      <td>0.42</td>
      <td>0.43</td>
      <td>0.43</td>
      <td>0.50</td>
      <td>0.49</td>
      <td>0.51</td>
      <td>0.60</td>
      <td>0.61</td>
      <td>0.65</td>
      <td>0.72</td>
      <td>0.39</td>
      <td>0.43</td>
      <td>0.42</td>
      <td>0.44</td>
      <td>0.43</td>
      <td>0.46</td>
    </tr>
    <tr>
      <td>Industry FE</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>54</td>
      <td>28</td>
      <td>28</td>
      <td>28</td>
      <td>28</td>
      <td>28</td>
      <td>28</td>
    </tr>
    <tr>
      <td>Country FE</td>
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
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
      <td>X</td>
    </tr>
  </tbody>
</table>


Panels A and B of this table report results from monthly Fama-Macbeth regressions. Panel C estimates the annual price of quality within each size decline. The dependent variable is the log of a firm’s market-to-book ratio in month t. The explanatory variables are the quality scores on month t and a series of controls. “Firm size” is the log of the firm’s market capitalization; “one-year return” is the firm’s stock return over the prior year. “Firm age” is the cumulative number of years since the firm’s IPO. “Uncertainty about mean profitability” (Pastor and Veronesi 2003) is the standard deviation of the residuals of an AR(1) model for each firm’s ROE, using the longest continuous series of a firm’s valid annual ROE up to date t. We require a minimum of 5 yrs of nonmissing ROEs. “Dividend payer” is a dummy equal to one if the firm paid any dividends over the prior year. With the exception of the “Dividend payer” dummy, all explanatory variables at time t are ranked cross-sectionally and rescaled to have a zero cross-sectional mean and a cross-sectional standard deviation of one. Industry, country, or firm fixed effects are included when indicated (“Industry FE,” “Country FE,” “Firm FE”). “Average AdjR2” is the time-series average of the adjusted R-squared of the cross-sectional regression. Standard errors are adjusted for heteroskedasticity and autocorrelation (Newey and West 1987) with a lag length of 5 yrs. T-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold

Springer

---

# Page 52

Quality minus junk

85

Table 13 Quality minus junk: correlations

<table>
  <thead>
    <tr>
      <th rowspan="2">Panel A: Long Sample (U.S., 7/1957–12/2016)</th>
      <th colspan="4">Returns</th>
      <th colspan="4">Abnormal Returns (4-factor)</th>
    </tr>
    <tr>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>QMJ</td>
      <td>1.00</td>
      <td>0.90</td>
      <td>0.85</td>
      <td>0.65</td>
      <td>1.00</td>
      <td>0.86</td>
      <td>0.73</td>
      <td>0.67</td>
    </tr>
    <tr>
      <td>Profitability</td>
      <td>0.90</td>
      <td>1.00</td>
      <td>0.65</td>
      <td>0.60</td>
      <td>0.86</td>
      <td>1.00</td>
      <td>0.47</td>
      <td>0.54</td>
    </tr>
    <tr>
      <td>Safety</td>
      <td>0.85</td>
      <td>0.65</td>
      <td>1.00</td>
      <td>0.35</td>
      <td>0.73</td>
      <td>0.47</td>
      <td>1.00</td>
      <td>0.30</td>
    </tr>
    <tr>
      <td>Growth</td>
      <td>0.65</td>
      <td>0.60</td>
      <td>0.35</td>
      <td>1.00</td>
      <td>0.67</td>
      <td>0.54</td>
      <td>0.30</td>
      <td>1.00</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th rowspan="2">Panel B: Broad Sample (Global, 7/1989–12/2016)</th>
      <th colspan="4">Returns</th>
      <th colspan="4">Abnormal Returns (4-factor)</th>
    </tr>
    <tr>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>QMJ</td>
      <td>1.00</td>
      <td>0.86</td>
      <td>0.89</td>
      <td>0.55</td>
      <td>1.00</td>
      <td>0.76</td>
      <td>0.70</td>
      <td>0.57</td>
    </tr>
    <tr>
      <td>Profitability</td>
      <td>0.86</td>
      <td>1.00</td>
      <td>0.80</td>
      <td>0.42</td>
      <td>0.76</td>
      <td>1.00</td>
      <td>0.62</td>
      <td>0.51</td>
    </tr>
    <tr>
      <td>Safety</td>
      <td>0.89</td>
      <td>0.80</td>
      <td>1.00</td>
      <td>0.34</td>
      <td>0.70</td>
      <td>0.62</td>
      <td>1.00</td>
      <td>0.25</td>
    </tr>
    <tr>
      <td>Growth</td>
      <td>0.55</td>
      <td>0.42</td>
      <td>0.34</td>
      <td>1.00</td>
      <td>0.57</td>
      <td>0.51</td>
      <td>0.25</td>
      <td>1.00</td>
    </tr>
  </tbody>
</table>

This table shows correlation of monthly returns. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Abnormal returns are constructed as the intercept plus the residual of a time-series regression of monthly excess returns. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7. Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate

Springer

---

# Page 53

86

C. S. Asness et al.

Table 14 Quality minus junk components

<table>
  <thead>
    <tr>
      <th></th>
      <th>Panel A: Long Sample (U.S., 7/1957–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th>Panel B: Broad Sample (Global, 7/1989–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>High Quality</td>
      <td></td>
      <td>Low Quality</td>
      <td></td>
      <td>High Quality</td>
      <td></td>
      <td>Low Quality</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>Small</td>
      <td>Big</td>
      <td>Small</td>
      <td>Big</td>
      <td>Small</td>
      <td>Big</td>
      <td>Small</td>
      <td>Big</td>
    </tr>
    <tr>
      <td>Excess Returns</td>
      <td>0.88</td>
      <td>0.60</td>
      <td>0.46</td>
      <td>0.44</td>
      <td>0.72</td>
      <td>0.59</td>
      <td>0.19</td>
      <td>0.36</td>
    </tr>
    <tr>
      <td></td>
      <td>(4.31)</td>
      <td>(3.64)</td>
      <td>(1.76)</td>
      <td>(2.31)</td>
      <td>(2.99)</td>
      <td>(2.62)</td>
      <td>(0.54)</td>
      <td>(1.24)</td>
    </tr>
    <tr>
      <td>CAPM-alpha</td>
      <td>0.30</td>
      <td>0.10</td>
      <td>−0.25</td>
      <td>−0.14</td>
      <td>0.38</td>
      <td>0.24</td>
      <td>−0.31</td>
      <td>−0.09</td>
    </tr>
    <tr>
      <td></td>
      <td>(3.31)</td>
      <td>(2.26)</td>
      <td>(−1.90)</td>
      <td>(−2.49)</td>
      <td>(2.95)</td>
      <td>(2.62)</td>
      <td>(−1.65)</td>
      <td>(−0.83)</td>
    </tr>
    <tr>
      <td>3-factor alpha</td>
      <td>0.23</td>
      <td>0.18</td>
      <td>−0.41</td>
      <td>−0.22</td>
      <td>0.34</td>
      <td>0.31</td>
      <td>−0.38</td>
      <td>−0.18</td>
    </tr>
    <tr>
      <td></td>
      <td>(5.97)</td>
      <td>(5.14)</td>
      <td>(−7.50)</td>
      <td>(−4.61)</td>
      <td>(3.37)</td>
      <td>(3.61)</td>
      <td>(−2.91)</td>
      <td>(−1.72)</td>
    </tr>
    <tr>
      <td>4-factor alpha</td>
      <td>0.23</td>
      <td>0.28</td>
      <td>−0.39</td>
      <td>−0.30</td>
      <td>0.33</td>
      <td>0.40</td>
      <td>−0.26</td>
      <td>−0.23</td>
    </tr>
    <tr>
      <td></td>
      <td>(5.74)</td>
      <td>(8.22)</td>
      <td>(−6.73)</td>
      <td>(−6.18)</td>
      <td>(3.04)</td>
      <td>(4.31)</td>
      <td>(−1.80)</td>
      <td>(−2.00)</td>
    </tr>
    <tr>
      <td>MKT</td>
      <td>0.96</td>
      <td>0.95</td>
      <td>1.18</td>
      <td>1.13</td>
      <td>0.78</td>
      <td>0.84</td>
      <td>1.06</td>
      <td>1.08</td>
    </tr>
    <tr>
      <td></td>
      <td>(102.79)</td>
      <td>(118.78)</td>
      <td>(87.63)</td>
      <td>(100.40)</td>
      <td>(31.99)</td>
      <td>(40.41)</td>
      <td>(33.26)</td>
      <td>(42.44)</td>
    </tr>
    <tr>
      <td>SMB</td>
      <td>0.86</td>
      <td>−0.12</td>
      <td>1.21</td>
      <td>0.05</td>
      <td>0.76</td>
      <td>−0.16</td>
      <td>1.24</td>
      <td>0.00</td>
    </tr>
    <tr>
      <td></td>
      <td>(58.45)</td>
      <td>(−9.63)</td>
      <td>(57.53)</td>
      <td>(2.81)</td>
      <td>(14.33)</td>
      <td>(−3.49)</td>
      <td>(17.81)</td>
      <td>(0.00)</td>
    </tr>
    <tr>
      <td>HML</td>
      <td>0.06</td>
      <td>−0.29</td>
      <td>0.22</td>
      <td>0.29</td>
      <td>0.14</td>
      <td>−0.29</td>
      <td>0.15</td>
      <td>0.31</td>
    </tr>
    <tr>
      <td></td>
      <td>(3.93)</td>
      <td>(−21.65)</td>
      <td>(9.93)</td>
      <td>(15.56)</td>
      <td>(2.85)</td>
      <td>(−6.72)</td>
      <td>(2.22)</td>
      <td>(5.81)</td>
    </tr>
    <tr>
      <td>UMD</td>
      <td>−0.01</td>
      <td>−0.10</td>
      <td>−0.02</td>
      <td>0.08</td>
      <td>0.01</td>
      <td>−0.08</td>
      <td>−0.12</td>
      <td>0.04</td>
    </tr>
    <tr>
      <td></td>
      <td>(−0.38)</td>
      <td>(−9.09)</td>
      <td>(−0.93)</td>
      <td>(5.17)</td>
      <td>(0.17)</td>
      <td>(−2.47)</td>
      <td>(−2.32)</td>
      <td>(1.08)</td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 54

Quality minus junk

87

Table 14 (continued)

<table>
  <thead>
    <tr>
      <th rowspan="3">Panel A: Long Sample (U.S., 7/1957–12/2016)</th>
      <th colspan="2">High Quality</th>
      <th colspan="2">Low Quality</th>
      <th rowspan="3">QMJ</th>
    </tr>
    <tr>
      <th rowspan="2">Small</th>
      <th rowspan="2">Big</th>
      <th rowspan="2">Small</th>
      <th rowspan="2">Big</th>
    </tr>
    <tr>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.56</td>
      <td>0.47</td>
      <td>0.23</td>
      <td>0.30</td>
      <td>0.47</td>
    </tr>
    <tr>
      <td>Information ratio</td>
      <td>0.80</td>
      <td>1.15</td>
      <td>-0.94</td>
      <td>-0.87</td>
      <td>1.40</td>
    </tr>
    <tr>
      <td>R2</td>
      <td>0.97</td>
      <td>0.96</td>
      <td>0.96</td>
      <td>0.94</td>
      <td>0.50</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th rowspan="3">Panel B: Broad Sample (Global, 7/1989–12/2016)</th>
      <th colspan="2">High Quality</th>
      <th colspan="2">Low Quality</th>
      <th rowspan="3">QMJ</th>
    </tr>
    <tr>
      <th rowspan="2">Small</th>
      <th rowspan="2">Big</th>
      <th rowspan="2">Small</th>
      <th rowspan="2">Big</th>
    </tr>
    <tr>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.57</td>
      <td>0.50</td>
      <td>0.10</td>
      <td>0.24</td>
      <td>0.64</td>
    </tr>
    <tr>
      <td>Information ratio</td>
      <td>0.64</td>
      <td>0.91</td>
      <td>-0.38</td>
      <td>-0.42</td>
      <td>1.70</td>
    </tr>
    <tr>
      <td>R2</td>
      <td>0.83</td>
      <td>0.86</td>
      <td>0.86</td>
      <td>0.87</td>
      <td>0.65</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time monthly portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7. Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage. t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized.

Springer

---

# Page 55

88

C. S. Asness et al.

Table 15 Robustness checks: QMJ by time period and size

<table>
  <thead>
    <tr>
      <th>Sample</th>
      <th>Universe</th>
      <th>Sample Period</th>
      <th>Excess return</th>
      <th>T-stat Excess return</th>
      <th>4-factor alpha</th>
      <th>T-stat Alpha</th>
      <th>Sharpe Ratio</th>
      <th>Information Ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Long Sample</td>
      <td>United States</td>
      <td>1957–1988</td>
      <td>0.21</td>
      <td>2.29</td>
      <td>0.60</td>
      <td>8.37</td>
      <td>0.41</td>
      <td>1.67</td>
    </tr>
    <tr>
      <td>Long Sample</td>
      <td>United States</td>
      <td>1989–2005</td>
      <td>0.42</td>
      <td>2.57</td>
      <td>0.79</td>
      <td>6.21</td>
      <td>0.62</td>
      <td>1.68</td>
    </tr>
    <tr>
      <td>Long Sample</td>
      <td>United States</td>
      <td>2006–2016</td>
      <td>0.32</td>
      <td>1.35</td>
      <td>0.54</td>
      <td>4.05</td>
      <td>0.41</td>
      <td>1.25</td>
    </tr>
    <tr>
      <td>Broad Sample</td>
      <td>Global</td>
      <td>1989–2005</td>
      <td>0.35</td>
      <td>2.52</td>
      <td>0.58</td>
      <td>5.10</td>
      <td>0.62</td>
      <td>1.43</td>
    </tr>
    <tr>
      <td>Broad Sample</td>
      <td>Global</td>
      <td>2006–2016</td>
      <td>0.43</td>
      <td>2.18</td>
      <td>0.65</td>
      <td>7.33</td>
      <td>0.66</td>
      <td>2.40</td>
    </tr>
    <tr>
      <td>P1 (small)</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.67</td>
      <td>4.47</td>
      <td>0.74</td>
      <td>5.60</td>
      <td>0.58</td>
      <td>0.78</td>
    </tr>
    <tr>
      <td>P2</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.47</td>
      <td>3.83</td>
      <td>0.62</td>
      <td>5.65</td>
      <td>0.50</td>
      <td>0.79</td>
    </tr>
    <tr>
      <td>P3</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.36</td>
      <td>3.16</td>
      <td>0.56</td>
      <td>5.09</td>
      <td>0.41</td>
      <td>0.71</td>
    </tr>
    <tr>
      <td>P4</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.38</td>
      <td>3.56</td>
      <td>0.60</td>
      <td>5.92</td>
      <td>0.46</td>
      <td>0.83</td>
    </tr>
    <tr>
      <td>P5</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.17</td>
      <td>1.70</td>
      <td>0.42</td>
      <td>4.22</td>
      <td>0.22</td>
      <td>0.59</td>
    </tr>
    <tr>
      <td>P6</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.14</td>
      <td>1.53</td>
      <td>0.40</td>
      <td>4.46</td>
      <td>0.20</td>
      <td>0.62</td>
    </tr>
    <tr>
      <td>P7</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.16</td>
      <td>1.77</td>
      <td>0.44</td>
      <td>4.99</td>
      <td>0.23</td>
      <td>0.70</td>
    </tr>
    <tr>
      <td>P8</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.25</td>
      <td>2.64</td>
      <td>0.57</td>
      <td>6.45</td>
      <td>0.34</td>
      <td>0.90</td>
    </tr>
    <tr>
      <td>P9</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.16</td>
      <td>1.75</td>
      <td>0.45</td>
      <td>5.45</td>
      <td>0.23</td>
      <td>0.76</td>
    </tr>
    <tr>
      <td>P10 (large)</td>
      <td>United States</td>
      <td>1957–2016</td>
      <td>0.23</td>
      <td>2.15</td>
      <td>0.66</td>
      <td>7.23</td>
      <td>0.28</td>
      <td>1.01</td>
    </tr>
    <tr>
      <td>P1 (small)</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.45</td>
      <td>2.24</td>
      <td>0.27</td>
      <td>1.81</td>
      <td>0.43</td>
      <td>0.38</td>
    </tr>
    <tr>
      <td>P2</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.54</td>
      <td>3.33</td>
      <td>0.45</td>
      <td>3.81</td>
      <td>0.63</td>
      <td>0.80</td>
    </tr>
    <tr>
      <td>P3</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.52</td>
      <td>3.55</td>
      <td>0.51</td>
      <td>4.50</td>
      <td>0.68</td>
      <td>0.95</td>
    </tr>
    <tr>
      <td>P4</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.52</td>
      <td>3.93</td>
      <td>0.59</td>
      <td>5.79</td>
      <td>0.75</td>
      <td>1.22</td>
    </tr>
    <tr>
      <td>P5</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.36</td>
      <td>2.83</td>
      <td>0.49</td>
      <td>4.54</td>
      <td>0.54</td>
      <td>0.96</td>
    </tr>
    <tr>
      <td>P6</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.30</td>
      <td>2.76</td>
      <td>0.46</td>
      <td>4.78</td>
      <td>0.53</td>
      <td>1.00</td>
    </tr>
    <tr>
      <td>P7</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.38</td>
      <td>3.70</td>
      <td>0.58</td>
      <td>6.76</td>
      <td>0.70</td>
      <td>1.42</td>
    </tr>
    <tr>
      <td>P8</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.40</td>
      <td>3.71</td>
      <td>0.72</td>
      <td>7.98</td>
      <td>0.71</td>
      <td>1.68</td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 56

Quality minus junk

89

<table>
  <thead>
    <tr>
      <th>Sample</th>
      <th>Universe</th>
      <th>Sample Period</th>
      <th>Excess return</th>
      <th>T-stat Excess return</th>
      <th>4-factor alpha</th>
      <th>T-stat Alpha</th>
      <th>Sharpe Ratio</th>
      <th>Information Ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>P9</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.25</td>
      <td>2.40</td>
      <td>0.56</td>
      <td>6.56</td>
      <td>0.46</td>
      <td>1.38</td>
    </tr>
    <tr>
      <td>P10 (large)</td>
      <td>Global</td>
      <td>1989–2016</td>
      <td>0.26</td>
      <td>1.76</td>
      <td>0.66</td>
      <td>5.73</td>
      <td>0.33</td>
      <td>1.21</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time monthly portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7. The table report results from our *Long Sample* of domestic stocks (sample period running from June 1957 to December 2016) and from our *Broad Sample* of global stocks (sample period running from June 1989 to December 2016). Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized.

$\text{Springer}$

---

# Page 57

90

C. S. Asness et al.

Table 16 Robustness checks: QMJ by country

<table>
  <thead>
    <tr>
      <th>Panel A. QMJ by Country</th>
      <th>Excess return</th>
      <th>T-stat excess return</th>
      <th>4-factor alpha</th>
      <th>T-s-alpha</th>
      <th>Factor loadings</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>MKT</td>
      <td>SMB</td>
      <td>HML</td>
      <td>UMD</td>
      <td>Sharpe ratio</td>
      <td>Information ratio</td>
      <td>Number of months</td>
      <td>Return date range</td>
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
      <td>Australia</td>
      <td>0.24</td>
      <td>1.38</td>
      <td>0.41</td>
      <td>2.57</td>
      <td>-0.17</td>
      <td>-0.28</td>
      <td>-0.18</td>
      <td>-0.02</td>
      <td>0.31</td>
      <td>0.65</td>
      <td>246</td>
      <td>199607–201612</td>
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
      <td>Austria</td>
      <td>0.03</td>
      <td>0.10</td>
      <td>0.16</td>
      <td>0.66</td>
      <td>-0.38</td>
      <td>0.01</td>
      <td>-0.14</td>
      <td>0.21</td>
      <td>0.02</td>
      <td>0.15</td>
      <td>246</td>
      <td>199607–201612</td>
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
      <td>Belgium</td>
      <td>0.46</td>
      <td>1.64</td>
      <td>0.44</td>
      <td>2.26</td>
      <td>-0.27</td>
      <td>-0.40</td>
      <td>-0.39</td>
      <td>0.21</td>
      <td>0.35</td>
      <td>0.52</td>
      <td>258</td>
      <td>199507–201612</td>
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
      <td>0.64</td>
      <td>3.08</td>
      <td>0.62</td>
      <td>3.22</td>
      <td>-0.19</td>
      <td>-0.31</td>
      <td>-0.21</td>
      <td>0.10</td>
      <td>0.59</td>
      <td>0.66</td>
      <td>330</td>
      <td>198907–201612</td>
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
      <td>Switzerland</td>
      <td>0.30</td>
      <td>1.20</td>
      <td>0.39</td>
      <td>2.08</td>
      <td>-0.41</td>
      <td>-0.19</td>
      <td>-0.27</td>
      <td>0.19</td>
      <td>0.26</td>
      <td>0.47</td>
      <td>258</td>
      <td>199507–201612</td>
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
      <td>0.56</td>
      <td>2.84</td>
      <td>0.63</td>
      <td>4.08</td>
      <td>-0.24</td>
      <td>-0.15</td>
      <td>-0.28</td>
      <td>0.07</td>
      <td>0.61</td>
      <td>0.97</td>
      <td>258</td>
      <td>199507–201612</td>
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
      <td>Denmark</td>
      <td>0.40</td>
      <td>1.61</td>
      <td>0.14</td>
      <td>0.68</td>
      <td>-0.19</td>
      <td>-0.30</td>
      <td>-0.32</td>
      <td>0.24</td>
      <td>0.35</td>
      <td>0.16</td>
      <td>258</td>
      <td>199507–201612</td>
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
      <td>Spain</td>
      <td>0.01</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.10</td>
      <td>-0.34</td>
      <td>-0.09</td>
      <td>-0.28</td>
      <td>0.22</td>
      <td>0.00</td>
      <td>0.02</td>
      <td>234</td>
      <td>199707–201612</td>
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
      <td>-0.08</td>
      <td>-0.27</td>
      <td>0.11</td>
      <td>0.44</td>
      <td>-0.02</td>
      <td>-0.01</td>
      <td>-0.43</td>
      <td>-0.04</td>
      <td>-0.06</td>
      <td>0.10</td>
      <td>258</td>
      <td>199507–201612</td>
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
      <td>0.32</td>
      <td>1.43</td>
      <td>0.52</td>
      <td>3.35</td>
      <td>-0.30</td>
      <td>-0.19</td>
      <td>-0.37</td>
      <td>0.09</td>
      <td>0.31</td>
      <td>0.77</td>
      <td>258</td>
      <td>199507–201612</td>
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
      <td>United Kingdom</td>
      <td>0.22</td>
      <td>1.34</td>
      <td>0.20</td>
      <td>1.54</td>
      <td>-0.23</td>
      <td>-0.10</td>
      <td>-0.16</td>
      <td>0.15</td>
      <td>0.28</td>
      <td>0.35</td>
      <td>282</td>
      <td>199307–201612</td>
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
      <td>Greece</td>
      <td>1.98</td>
      <td>3.40</td>
      <td>1.32</td>
      <td>3.92</td>
      <td>-0.26</td>
      <td>-0.29</td>
      <td>-0.09</td>
      <td>0.49</td>
      <td>0.89</td>
      <td>1.06</td>
      <td>174</td>
      <td>200207–201612</td>
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
      <td>Hong Kong</td>
      <td>0.14</td>
      <td>0.36</td>
      <td>0.76</td>
      <td>3.12</td>
      <td>-0.36</td>
      <td>-0.38</td>
      <td>-0.52</td>
      <td>0.05</td>
      <td>0.08</td>
      <td>0.72</td>
      <td>246</td>
      <td>199607–201612</td>
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
      <td>Ireland</td>
      <td>1.03</td>
      <td>1.51</td>
      <td>1.08</td>
      <td>2.17</td>
      <td>-0.68</td>
      <td>-0.04</td>
      <td>-0.02</td>
      <td>0.21</td>
      <td>0.34</td>
      <td>0.50</td>
      <td>234</td>
      <td>199707–201612</td>
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
      <td>Israel</td>
      <td>0.48</td>
      <td>1.47</td>
      <td>0.50</td>
      <td>2.21</td>
      <td>-0.30</td>
      <td>-0.32</td>
      <td>-0.25</td>
      <td>0.28</td>
      <td>0.39</td>
      <td>0.64</td>
      <td>174</td>
      <td>200207–201612</td>
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
      <td>Italy</td>
      <td>0.62</td>
      <td>2.16</td>
      <td>0.58</td>
      <td>3.38</td>
      <td>-0.30</td>
      <td>-0.15</td>
      <td>-0.37</td>
      <td>0.22</td>
      <td>0.47</td>
      <td>0.75</td>
      <td>258</td>
      <td>199507–201612</td>
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
      <td>Japan</td>
      <td>0.24</td>
      <td>1.16</td>
      <td>0.56</td>
      <td>3.66</td>
      <td>-0.34</td>
      <td>-0.27</td>
      <td>-0.43</td>
      <td>0.08</td>
      <td>0.24</td>
      <td>0.82</td>
      <td>282</td>
      <td>199307–201612</td>
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
      <td>Netherlands</td>
      <td>0.14</td>
      <td>0.48</td>
      <td>0.47</td>
      <td>2.16</td>
      <td>-0.38</td>
      <td>-0.20</td>
      <td>-0.25</td>
      <td>0.04</td>
      <td>0.10</td>
      <td>0.48</td>
      <td>258</td>
      <td>199507–201612

---

# Page 58

Quality minus junk

91

Table 16 (continued)

<table>
  <thead>
    <tr>
      <th></th>
      <th>Large Cap</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>Small Cap</th>
      <th></th>
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
      <td>Excess return</td>
      <td>T-stat Excess return</td>
      <td>4-factor Alpha</td>
      <td>T-stat Alpha</td>
      <td>Sharpe Ratio</td>
      <td>Information Ratio</td>
      <td>Excess return</td>
      <td>T-stat Excess return</td>
      <td>4-factor Alpha</td>
      <td>T-stat Alpha</td>
      <td>Sharpe Ratio</td>
      <td>Information Ratio</td>
      <td></td>
    </tr>
    <tr>
      <td>United States</td>
      <td>0.29</td>
      <td>3.62</td>
      <td>0.60</td>
      <td>9.95</td>
      <td>-0.20</td>
      <td>-0.26</td>
      <td>-0.37</td>
      <td>-0.08</td>
      <td>0.47</td>
      <td>1.40</td>
      <td>714</td>
      <td>195707–201612</td>
      <td></td>
    </tr>
    <tr>
      <td>Global</td>
      <td>0.38</td>
      <td>3.33</td>
      <td>0.61</td>
      <td>8.07</td>
      <td>-0.27</td>
      <td>-0.32</td>
      <td>-0.30</td>
      <td>0.00</td>
      <td>0.64</td>
      <td>1.70</td>
      <td>330</td>
      <td>198907–201612</td>
      <td></td>
    </tr>
    <tr>
      <td>Panel B. QMJ by Country: Large and Small Stocks</td>
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
      <td>Australia</td>
      <td>-0.16</td>
      <td>-0.68</td>
      <td>0.14</td>
      <td>0.57</td>
      <td>-0.15</td>
      <td>0.15</td>
      <td>0.65</td>
      <td>2.47</td>
      <td>0.68</td>
      <td>2.84</td>
      <td>0.54</td>
      <td>0.72</td>
      <td></td>
    </tr>
    <tr>
      <td>Austria</td>
      <td>0.16</td>
      <td>0.36</td>
      <td>0.10</td>
      <td>0.25</td>
      <td>0.08</td>
      <td>0.06</td>
      <td>-0.10</td>
      <td>-0.31</td>
      <td>0.22</td>
      <td>0.78</td>
      <td>-0.07</td>
      <td>0.18</td>
      <td></td>
    </tr>
    <tr>
      <td>Belgium</td>
      <td>0.37</td>
      <td>0.96</td>
      <td>0.26</td>
      <td>0.88</td>
      <td>0.21</td>
      <td>0.20</td>
      <td>0.55</td>
      <td>1.90</td>
      <td>0.61</td>
      <td>2.44</td>
      <td>0.41</td>
      <td>0.56</td>
      <td></td>
    </tr>
    <tr>
      <td>Canada</td>
      <td>0.53</td>
      <td>2.17</td>
      <td>0.60</td>
      <td>2.55</td>
      <td>0.41</td>
      <td>0.53</td>
      <td>0.75</td>
      <td>3.00</td>
      <td>0.64</td>
      <td>2.86</td>
      <td>0.57</td>
      <td>0.59</td>
      <td></td>
    </tr>
    <tr>
      <td>Switzerland</td>
      <td>0.35</td>
      <td>0.93</td>
      <td>0.49</td>
      <td>1.56</td>
      <td>0.20</td>
      <td>0.35</td>
      <td>0.25</td>
      <td>1.16</td>
      <td>0.29</td>
      <td>1.54</td>
      <td>0.25</td>
      <td>0.35</td>
      <td></td>
    </tr>
    <tr>
      <td>Germany</td>
      <td>-0.03</td>
      <td>-0.11</td>
      <td>0.49</td>
      <td>1.92</td>
      <td>-0.02</td>
      <td>0.45</td>
      <td>1.16</td>
      <td>4.75</td>
      <td>0.77</td>
      <td>3.76</td>
      <td>1.02</td>
      <td>0.89</td>
      <td></td>
    </tr>
    <tr>
      <td>Denmark</td>
      <td>0.24</td>
      <td>0.59</td>
      <td>-0.21</td>
      <td>-0.58</td>
      <td>0.13</td>
      <td>-0.13</td>
      <td>0.57</td>
      <td>2.15</td>
      <td>0.49</td>
      <td>1.92</td>
      <td>0.46</td>
      <td>0.44</td>
      <td></td>
    </tr>
    <tr>
      <td>Spain</td>
      <td>0.03</td>
      <td>0.07</td>
      <td>0.03</td>
      <td>0.08</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>-0.02</td>
      <td>-0.05</td>
      <td>0.02</td>
      <td>0.07</td>
      <td>-0.01</td>
      <td>0.02</td>
      <td></td>
    </tr>
    <tr>
      <td>Finland</td>
      <td>-0.36</td>
      <td>-0.71</td>
      <td>-0.05</td>
      <td>-0.13</td>
      <td>-0.15</td>
      <td>-0.03</td>
      <td>0.20</td>
      <td>0.74</td>
      <td>0.26</td>
      <td>0.99</td>
      <td>0.16</td>
      <td>0.22</td>
      <td></td>
    </tr>
    <tr>
      <td>France</td>
      <td>0.13</td>
      <td>0.45</td>
      <td>0.40</td>
      <td>1.68</td>
      <td>0.10</td>
      <td>0.39</td>
      <td>0.51</td>
      <td>2.20</td>
      <td>0.64</td>
      <td>3.62</td>
      <td>0.47</td>
      <td>0.83</td>
      <td></td>
    </tr>
    <tr>
      <td>United Kingdom</td>
      <td>-0.02</td>
      <td>-0.07</td>
      <td>-0.07</td>
      <td>-0.34</td>
      <td>-0.01</td>
      <td>-0.08</td>
      <td>0.46</td>
      <td>3.06</td>
      <td>0.47</td>
      <td>3.62</td>
      <td>0.63</td>
      <td>0.82</td>
      <td></td>
    </tr>
    <tr>
      <td>Greece</td>
      <td>2.80</td>
      <td>3.10</td>
      <td>1.71</td>
      <td>2.65</td>
      <td>0.81</td>
      <td>0.72</td>
      <td>1.17</td>
      <td>2.40</td>
      <td>0.92</td>
      <td>2.58</td>
      <td>0.63</td>
      <td>0.70</td>
      <td></td>
    </tr>
    <tr>
      <td>Hong Kong</td>
      <td>0.31</td>
      <td>0.73</td>
      <td>1.02</td>
      <td>3.23</td>
      <td>0.16</td>
      <td>0.74</td>
      <td>-0.04</td>
      <td>-0.09</td>
      <td>0.50</td>
      <td>1.56</td>
      <td>-0.02</td>
      <td>0.36</td>
      <td></td>
    </tr>
    <tr>
      <td>Ireland</td>
      <td>0.84</td>
      <td>0.93</td>
      <td>1.10</td>
      <td>1.79</td>
      <td>0.21</td>
      <td>0.41</td>
      <td>1.23</td>
      <td>1.54</td>
      <td>1.07</td>
      <td>1.47</td>
      <td>0.35</td>
      <td>0.34</td>
      <td></td>
    </tr>
    <tr>
      <td>Israel</td>
      <td>0.30</td>
      <td>0.65</td>
      <td>0.49</td>
      <td>1.28</td>
      <td>0.17</td>
      <td>0.37</td>
      <td>0.65</td>
      <td>1.99</td>
      <td>0.50</td>
      <td>1.84</td>
      <td>0.52</td>
      <td>0.53</td>
      <td></td>
    </tr>
    <tr>
      <td>Italy</td>
      <td>0.44</td>
      <td>1.14</td>
      <td>0.42</td>
      <td>1.48</td>
      <td>0.25</td>
      <td>0.33</td>
      <td>0.79</td>
      <td>2.78</td>
      <td>0.74</td>
      <td>3.59</td>
      <td>0.60</td>
      <td>0.80</td>
      <td></td>
    </tr>
    <tr>
      <td>Japan</td>
      <td>0.32</td>
      <td>1.29</td>
      <td>0.68</td>
      <td>3.15</td>
      <td>0.27</td>
      <td>0.70</td>
      <td>0.16</td>
      <td>0.73</td>
      <td>0.44</td>
      <td>2.63</td>
      <td>0.15</td>
      <td>0.59</td>
      <td></td>
    </tr>
    <tr>
      <td>Netherlands</td>
      <td>-0.04</td>
      <td>-0.11</td>
      <td>0.37</td>
      <td>1.10</td>
      <td>-0.02</td>
      <td>0.25</td>
      <td>0.32</td>
      <td>1.12</td>
      <td>0.56</td>
      <td>2.33</td>
      <td>0.24</td>
      <td>0.52</td>
      <td></td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 59

92

C. S. Asness et al.

<table>
  <thead>
    <tr>
      <th rowspan="2">Table 16 (continued)</th>
      <th colspan="6">Norway</th>
    </tr>
    <tr>
      <th>0.26</th>
      <th>0.71</th>
      <th>0.35</th>
      <th>0.97</th>
      <th>0.15</th>
      <th>0.22</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>New Zealand</td>
      <td>0.12</td>
      <td>0.41</td>
      <td>0.30</td>
      <td>1.03</td>
      <td>0.10</td>
      <td>0.26</td>
    </tr>
    <tr>
      <td>Portugal</td>
      <td>1.50</td>
      <td>2.69</td>
      <td>1.20</td>
      <td>2.48</td>
      <td>0.66</td>
      <td>0.65</td>
    </tr>
    <tr>
      <td>Singapore</td>
      <td>-0.01</td>
      <td>-0.02</td>
      <td>0.51</td>
      <td>1.90</td>
      <td>0.00</td>
      <td>0.44</td>
    </tr>
    <tr>
      <td>Sweden</td>
      <td>0.02</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>0.26</td>
      <td>0.02</td>
      <td>0.06</td>
    </tr>
    <tr>
      <td>United States</td>
      <td>0.16</td>
      <td>1.75</td>
      <td>0.58</td>
      <td>8.17</td>
      <td>0.23</td>
      <td>1.14</td>
    </tr>
    <tr>
      <td>Global</td>
      <td>0.23</td>
      <td>1.75</td>
      <td>0.63</td>
      <td>6.48</td>
      <td>0.33</td>
      <td>1.36</td>
    </tr>
  </tbody>
</table>

<table>
  <thead>
    <tr>
      <th rowspan="2">0.88</th>
      <th colspan="6">2.45</th>
    </tr>
    <tr>
      <th>-0.29</th>
      <th>-0.95</th>
      <th>0.84</th>
      <th>2.41</th>
      <th>3.86</th>
      <th>4.32</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>0.81</td>
      <td>-0.31</td>
      <td>-0.93</td>
      <td>0.66</td>
      <td>3.88</td>
      <td>2.88</td>
      <td>7.54</td>
    </tr>
    <tr>
      <td>2.57</td>
      <td>-0.22</td>
      <td>0.21</td>
      <td>0.53</td>
      <td>0.85</td>
      <td>0.56</td>
      <td>0.76</td>
    </tr>
    <tr>
      <td>0.53</td>
      <td>-0.24</td>
      <td>0.17</td>
      <td>0.89</td>
      <td>0.67</td>
      <td>1.06</td>
      <td>1.33</td>
    </tr>
    <tr>
      <td>0.59</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
  </tbody>
</table>

This table shows calendar-time monthly portfolio returns and factor loadings by country (Panel A) and by country separately for small and large (Panel B). Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities the size breakpoint is the median NYSE market equity. For other markets the size breakpoint is the 80th percentile by country. We use conditional sorts first sorting on size then on quality. Portfolios are value-weighted refreshed every calendar month and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability growth and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT) size (SMB) book-to-market (HML) and momentum (UMD) portfolios from Fig. 7. The table report results from our *Long Sample* of domestic stocks (sample period running from June 1957 to December 2016) and from our *Broad Sample* of global stocks (sample period running from June 1989 to December 2016). Returns are in U.S. dollars do not include currency hedging and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage t-statistics are shown below the coefficient estimates and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized.

Springer

---

# Page 60

Quality minus junk

93

Table 17 Quality minus junk: alpha to four-factor model plus BAB

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="4">Panel A: Long Sample<br>(U.S., 7/1957–12/2016)</th>
      <th colspan="4">Panel B: Broad Sample<br>(Global, 7/1989–12/2016)</th>
    </tr>
    <tr>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess Returns</td>
      <td>0.29<br>(3.62)</td>
      <td>0.25<br>(3.69)</td>
      <td>0.23<br>(2.44)</td>
      <td>0.17<br>(2.46)</td>
      <td>0.38<br>(3.33)</td>
      <td>0.39<br>(4.34)</td>
      <td>0.23<br>(1.72)</td>
      <td>0.15<br>(1.96)</td>
    </tr>
    <tr>
      <td>5-factor alpha</td>
      <td>0.55<br>(9.29)</td>
      <td>0.48<br>(7.86)</td>
      <td>0.45<br>(7.59)</td>
      <td>0.45<br>(8.07)</td>
      <td>0.57<br>(7.88)</td>
      <td>0.45<br>(6.66)</td>
      <td>0.35<br>(5.48)</td>
      <td>0.39<br>(5.65)</td>
    </tr>
    <tr>
      <td>MKT</td>
      <td>−0.20<br>(−14.88)</td>
      <td>−0.12<br>(−8.63)</td>
      <td>−0.32<br>(−23.59)</td>
      <td>−0.04<br>(−2.84)</td>
      <td>−0.26<br>(−16.14)</td>
      <td>−0.19<br>(−12.74)</td>
      <td>−0.34<br>(−24.14)</td>
      <td>−0.03<br>(−1.99)</td>
    </tr>
    <tr>
      <td>SMB</td>
      <td>−0.27<br>(−12.35)</td>
      <td>−0.22<br>(−10.16)</td>
      <td>−0.31<br>(−14.39)</td>
      <td>−0.04<br>(−1.79)</td>
      <td>−0.36<br>(−10.08)</td>
      <td>−0.30<br>(−9.07)</td>
      <td>−0.28<br>(−8.84)</td>
      <td>−0.13<br>(−3.71)</td>
    </tr>
    <tr>
      <td>HML</td>
      <td>−0.41<br>(−17.28)</td>
      <td>−0.32<br>(−13.04)</td>
      <td>−0.34<br>(−14.45)</td>
      <td>−0.50<br>(−22.25)</td>
      <td>−0.39<br>(−10.47)</td>
      <td>−0.11<br>(−3.31)</td>
      <td>−0.36<br>(−11.10)</td>
      <td>−0.40<br>(−11.32)</td>
    </tr>
    <tr>
      <td>UMD</td>
      <td>−0.13<br>(−6.28)</td>
      <td>−0.12<br>(−5.75)</td>
      <td>−0.05<br>(−2.66)</td>
      <td>−0.17<br>(−8.96)</td>
      <td>−0.09<br>(−2.84)</td>
      <td>−0.01<br>(−0.51)</td>
      <td>0.01<br>(0.42)</td>
      <td>−0.16<br>(−5.57)</td>
    </tr>
    <tr>
      <td>BAB</td>
      <td>0.11<br>(5.94)</td>
      <td>0.06<br>(3.28)</td>
      <td>0.16<br>(8.29)</td>
      <td>0.02<br>(1.11)</td>
      <td>0.15<br>(5.46)</td>
      <td>0.09<br>(3.63)</td>
      <td>0.19<br>(7.49)</td>
      <td>0.03<br>(1.07)</td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.47</td>
      <td>0.48</td>
      <td>0.32</td>
      <td>0.32</td>
      <td>0.64</td>
      <td>0.83</td>
      <td>0.33</td>
      <td>0.37</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>1.32</td>
      <td>1.11</td>
      <td>1.07</td>
      <td>1.14</td>
      <td>1.67</td>
      <td>1.41</td>
      <td>1.16</td>
      <td>1.20</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>0.53</td>
      <td>0.35</td>
      <td>0.66</td>
      <td>0.46</td>
      <td>0.68</td>
      <td>0.53</td>
      <td>0.81</td>
      <td>0.34</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), momentum (UMD) portfolios all from Fig. 7 and the low beta (BAB) factor (Frazzini and Pedersen 2014). Panel A reports results from our Long Sample of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our Broad Sample of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized.

Springer

---

# Page 61

94

C. S. Asness et al.

Table 18 Quality minus junk: alphas to five-factor model plus UMD and BAB

<table>
  <thead>
    <tr>
      <th rowspan="2"></th>
      <th colspan="4">Panel A: Long Sample<br>(U.S., 7/1963–12/2016)</th>
      <th colspan="4">Panel B: Broad Sample<br>(Global, 7/1990–12/2016)</th>
    </tr>
    <tr>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess Returns</td>
      <td>0.29<br>(3.30)</td>
      <td>0.29<br>(3.92)</td>
      <td>0.20<br>(2.04)</td>
      <td>0.15<br>(2.02)</td>
      <td>0.35<br>(2.95)</td>
      <td>0.37<br>(4.20)</td>
      <td>0.20<br>(1.48)</td>
      <td>0.12<br>(1.54)</td>
    </tr>
    <tr>
      <td>7-factor alpha</td>
      <td>0.33<br>(6.75)</td>
      <td>0.30<br>(6.87)</td>
      <td>0.26<br>(4.13)</td>
      <td>0.27<br>(5.96)</td>
      <td>0.26<br>(4.20)</td>
      <td>0.25<br>(5.10)</td>
      <td>0.12<br>(1.93)</td>
      <td>0.17<br>(2.86)</td>
    </tr>
    <tr>
      <td>MKT</td>
      <td>−0.17<br>(−13.88)</td>
      <td>−0.08<br>(−7.22)</td>
      <td>−0.28<br>(−17.95)</td>
      <td>−0.05<br>(−4.23)</td>
      <td>−0.22<br>(−13.62)</td>
      <td>−0.14<br>(−10.12)</td>
      <td>−0.32<br>(−19.09)</td>
      <td>−0.05<br>(−3.02)</td>
    </tr>
    <tr>
      <td>SMB</td>
      <td>−0.11<br>(−6.47)</td>
      <td>−0.06<br>(−4.22)</td>
      <td>−0.20<br>(−9.26)</td>
      <td>0.03<br>(1.97)</td>
      <td>−0.19<br>(−5.71)</td>
      <td>−0.16<br>(−6.01)</td>
      <td>−0.18<br>(−5.43)</td>
      <td>−0.07<br>(−2.12)</td>
    </tr>
    <tr>
      <td>HML</td>
      <td>−0.26<br>(−10.65)</td>
      <td>−0.28<br>(−13.15)</td>
      <td>−0.21<br>(−6.71)</td>
      <td>−0.26<br>(−11.51)</td>
      <td>−0.29<br>(−7.38)</td>
      <td>−0.09<br>(−2.70)</td>
      <td>−0.29<br>(−7.26)</td>
      <td>−0.11<br>(−2.88)</td>
    </tr>
    <tr>
      <td>CMA</td>
      <td>−0.05<br>(−0.00)</td>
      <td>0.11<br>(−0.05)</td>
      <td>0.02<br>(0.07)</td>
      <td>−0.35<br>(−0.02)</td>
      <td>0.05<br>(0.04)</td>
      <td>0.06<br>(−0.01)</td>
      <td>0.06<br>(0.12)</td>
      <td>−0.40<br>(−0.02)</td>
    </tr>
    <tr>
      <td>RMW</td>
      <td>−1.33<br>(0.55)</td>
      <td>3.66<br>(0.60)</td>
      <td>0.35<br>(0.29)</td>
      <td>−10.94<br>(0.34)</td>
      <td>1.00<br>(0.63)</td>
      <td>1.54<br>(0.60)</td>
      <td>1.15<br>(0.35)</td>
      <td>−8.94<br>(0.34)</td>
    </tr>
    <tr>
      <td>UMD</td>
      <td>22.75<br>(0.07)</td>
      <td>28.15<br>(0.02)</td>
      <td>9.07<br>(0.13)</td>
      <td>15.29<br>(0.05)</td>
      <td>12.48<br>(0.09)</td>
      <td>14.81<br>(0.04)</td>
      <td>6.81<br>(0.18)</td>
      <td>7.13<br>(0.04)</td>
    </tr>
    <tr>
      <td>BAB</td>
      <td>5.54<br>(−0.23)</td>
      <td>2.00<br>(−3.42)</td>
      <td>8.01<br>(3.00)</td>
      <td>4.37<br>(−1.50)</td>
      <td>5.40<br>(1.53)</td>
      <td>2.68<br>(−0.60)</td>
      <td>10.65<br>(4.28)</td>
      <td>2.38<br>(−0.69)</td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.45</td>
      <td>0.54</td>
      <td>0.28</td>
      <td>0.28</td>
      <td>0.57</td>
      <td>0.82</td>
      <td>0.29</td>
      <td>0.30</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>0.99</td>
      <td>1.01</td>
      <td>0.61</td>
      <td>0.88</td>
      <td>0.90</td>
      <td>1.10</td>
      <td>0.42</td>
      <td>0.62</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>0.72</td>
      <td>0.71</td>
      <td>0.64</td>
      <td>0.67</td>
      <td>0.78</td>
      <td>0.75</td>
      <td>0.83</td>
      <td>0.54</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), profitability (RMW), and investment (CMA) portfolios from Fama and French (2015) and the momentum (UMD) portfolios from Ken’s French data library and the low beta (BAB) factor (Frazzini and Pedersen 2014). Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from July 1963 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1990 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized

Springer

---

# Page 62

Quality minus junk

95

Table 19 Shortselling of quality versus junk stocks

<table>
  <thead>
    <tr>
      <th>Universe</th>
      <th>Time period</th>
      <th>P1 (Low)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10 (High)</th>
      <th>H-L</th>
      <th>H-L t-statistics</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Short Utilization × 100</td>
      <td>2004–2016</td>
      <td>23.13</td>
      <td>14.75</td>
      <td>11.73</td>
      <td>10.42</td>
      <td>9.24</td>
      <td>8.58</td>
      <td>7.76</td>
      <td>8.02</td>
      <td>6.52</td>
      <td>5.78</td>
      <td>−17.35</td>
      <td>−33.53</td>
    </tr>
    <tr>
      <td>Lending Fee (bps)</td>
      <td>2006–2016</td>
      <td>151.04</td>
      <td>69.44</td>
      <td>64.53</td>
      <td>51.36</td>
      <td>46.93</td>
      <td>43.06</td>
      <td>37.09</td>
      <td>42.31</td>
      <td>37.56</td>
      <td>38.09</td>
      <td>−112.95</td>
      <td>−13.13</td>
    </tr>
    <tr>
      <td>Short Utilization × 100</td>
      <td>2004–2016</td>
      <td>17.89</td>
      <td>15.32</td>
      <td>14.13</td>
      <td>12.56</td>
      <td>11.32</td>
      <td>10.60</td>
      <td>9.87</td>
      <td>9.72</td>
      <td>9.23</td>
      <td>9.76</td>
      <td>−8.14</td>
      <td>−29.38</td>
    </tr>
    <tr>
      <td>Lending Fee (bps)</td>
      <td>2006–2016</td>
      <td>127.43</td>
      <td>96.61</td>
      <td>90.06</td>
      <td>78.13</td>
      <td>65.19</td>
      <td>58.08</td>
      <td>53.53</td>
      <td>56.94</td>
      <td>56.73</td>
      <td>62.96</td>
      <td>−64.47</td>
      <td>−16.06</td>
    </tr>
  </tbody>
</table>


This table shows average short selling utilization and fees. Each calendar month, stocks in each country in are ranked in ascending order on the basis of their quality score. The ranked stocks are assigned to one of 10 portfolios. U.S. sorts are based on NYSE breakpoints. This table reports each portfolio’s average utilization and lending fee. The data source is Markit. “Utilization” rates are defined as the value of assets on loan divided by the total lendable assets. Lending fees are equal to the simple average fee over the past 60 days (“SAF”). The data on utilization covers the period 2004–2016, while lending fees are available from 2006 to 2016. We report the time series average of the value-weighted cross sectional means in our U.S. and global samples. Standard errors are adjusted for heteroskedasticity and autocorrelation with a lag length of 5 yrs (Newey and West 1987), and 5% significance is indicated in bold

Springer

---

# Page 63

96

C. S. Asness et al.

Table 20 Asset pricing tests: four-factor model plus BAB

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1963–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <td>SMB</td>
      <td>SMB</td>
      <td>HML</td>
      <td>HML</td>
      <td>UMD</td>
      <td>UMD</td>
      <td>BAB</td>
      <td>BAB</td>
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
      <td>Excess Returns</td>
      <td>0.15</td>
      <td>0.16</td>
      <td>0.30</td>
      <td>0.30</td>
      <td>0.71</td>
      <td>0.71</td>
      <td>0.83</td>
      <td>0.83</td>
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
      <td></td>
      <td>(1.55)</td>
      <td>(1.55)</td>
      <td>(2.39)</td>
      <td>(2.39)</td>
      <td>(4.77)</td>
      <td>(4.77)</td>
      <td>(7.15)</td>
      <td>(7.15)</td>
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
      <td>Alpha</td>
      <td>0.12</td>
      <td>0.47</td>
      <td>0.61</td>
      <td>0.82</td>
      <td>0.79</td>
      <td>0.97</td>
      <td>0.42</td>
      <td>0.17</td>
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
      <td></td>
      <td>(1.15)</td>
      <td>(4.75)</td>
      <td>(6.67)</td>
      <td>(10.67)</td>
      <td>(7.46)</td>
      <td>(9.10)</td>
      <td>(3.63)</td>
      <td>(1.40)</td>
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
      <td>MKT</td>
      <td>0.16</td>
      <td>0.00</td>
      <td>−0.15</td>
      <td>−0.25</td>
      <td>−0.18</td>
      <td>−0.25</td>
      <td>0.02</td>
      <td>0.11</td>
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
      <td></td>
      <td>(7.11)</td>
      <td>(−0.03)</td>
      <td>(−7.07)</td>
      <td>(−13.54)</td>
      <td>(−7.32)</td>
      <td>(−9.53)</td>
      <td>(0.84)</td>
      <td>(3.58)</td>
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
      <td>SMB</td>
      <td>.</td>
      <td>.</td>
      <td>−0.05</td>
      <td>−0.22</td>
      <td>−0.08</td>
      <td>−0.19</td>
      <td>0.03</td>
      <td>0.14</td>
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
      <td></td>
      <td></td>
      <td></td>
      <td>(−1.41)</td>
      <td>(−7.45)</td>
      <td>(−2.03)</td>
      <td>(−4.42)</td>
      <td>(0.68)</td>
      <td>(3.07)</td>
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
      <td>HML</td>
      <td>−0.06</td>
      <td>−0.33</td>
      <td>.</td>
      <td>.</td>
      <td>−0.84</td>
      <td>−0.97</td>
      <td>0.40</td>
      <td>0.55</td>
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
      <td></td>
      <td>(−1.41)</td>
      <td>(−7.45)</td>
      <td></td>
      <td></td>
      <td>(−27.46)</td>
      <td>(−26.91)</td>
      <td>(8.93)</td>
      <td>(10.90)</td>
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
      <td>UMD</td>
      <td>−0.07</td>
      <td>−0.15</td>
      <td>−0.61</td>
      <td>−0.52</td>
      <td>.</td>
      <td>.</td>
      <td>0.38</td>
      <td>0.42</td>
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
      <td></td>
      <td>(−2.03)</td>
      <td>(−4.42)</td>
      <td>(−27.46)</td>
      <td>(−26.91)</td>
      <td></td>
      <td></td>
      <td>(10.23)</td>
      <td>(11.29)</td>
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
      <td>BAB</td>
      <td>0.02</td>
      <td>0.10</td>
      <td>0.25</td>
      <td>0.26</td>
      <td>0.34</td>
      <td>0.37</td>
      <td>.</td>
      <td>.</td>
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
      <td></td>
      <td>(0.68)</td>
      <td>(3.07)</td>
      <td>(8.93)</td>
      <td>(10.90)</td>
      <td>(10.23)</td>
      <td>(11.29)</td>
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
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>QMJ</td>
      <td>.</td>
      <td>−0.67</td>
      <td>.</td>
      <td>−0.72</td>
      <td>.</td>
      <td>−0.41</td>
      <td>.</td>
      <td>0.42</td>
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
      <td></td>
      <td></td>
      <td>(−12.35)</td>
      <td></td>
      <td>(−17.28)</td>
      <td></td>
      <td>(−6.28)</td>
      <td></td>
      <td>(5.94)</td>
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
      <td>Sharpe Ratio</td>
      <td>0.20</td>
      <td>0.20</td>
      <td>0.31</td>
      <td>0.31</td>
      <td>0.62</td>
      <td>0.62</td>
      <td>0.93</td>
      <td>0.93</td>
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


Panel B: Broad Sample (Global, 11/1990–12/2016)

<table>
  <thead>
    <tr>
      <th></th>
      <th>SMB</th>
      <th>SMB</th>
      <th>HML</th>
      <th>HML</th>
      <th>UMD</th>
      <th>UMD</th>
      <th>BAB</th>
      <th>BAB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td></td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.35</td>
      <td>0.35</td>
      <td>0.66</td>
      <td>0.66</td>
      <td>0.81</td>
      <td>0.81</td>
    </tr>
    <tr>
      <td></td>
      <td>(0.23)</td>
      <td>(0.23)</td>
      <td>(2.19)</td>
      <td>(2.19)</td>
      <td>(3.05)</td>
      <td>(3.05)</td>
      <td>(5.17)</td>
      <td>(5.17)</td>
    </tr>
    <tr>
      <td></td>
      <td>0.04</td>
      <td>0.40</td>
      <td>0.52</td>
      <td>0.52</td>
      <td>0.68</td>
      <td>0.68</td>
      <td>0.24</td>
      <td>0.24</td>
    </tr>
    <tr>
      <td></td>
      <td>(0.32)</td>
      <td>(3.86)</td>
      <td>(5.07)</td>
      <td>(5.07)</

---

# Page 64

Quality minus junk

97

Table 20 (continued)

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1963–12/2016)</th>
      <th>Panel B: Broad Sample (Global, 11/1990–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <td>SMB</td>
      <td>HML</td>
      <td>UMD</td>
      <td>BAB</td>
      <td>SMB</td>
      <td>HML</td>
      <td>UMD</td>
      <td>BAB</td>
      <td>SMB</td>
      <td>HML</td>
      <td>UMD</td>
      <td>BAB</td>
      <td>SMB</td>
      <td>HML</td>
    </tr>
    <tr>
      <td>Information Ratio</td>
      <td>0.16</td>
      <td>0.70</td>
      <td>0.92</td>
      <td>1.48</td>
      <td>1.02</td>
      <td>1.29</td>
      <td>0.51</td>
      <td>0.21</td>
      <td>0.07</td>
      <td>0.87</td>
      <td>1.03</td>
      <td>1.73</td>
      <td>1.08</td>
      <td>1.32</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>0.09</td>
      <td>0.25</td>
      <td>0.52</td>
      <td>0.66</td>
      <td>0.54</td>
      <td>0.57</td>
      <td>0.14</td>
      <td>0.18</td>
      <td>0.08</td>
      <td>0.30</td>
      <td>0.63</td>
      <td>0.72</td>
      <td>0.68</td>
      <td>0.69</td>
    </tr>
    <tr>
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
      <td>0.35</td>
    </tr>
    <tr>
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
      <td>0.31</td>
    </tr>
    <tr>
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
      <td>−0.15</td>
    </tr>
    <tr>
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
      <td>0.37</td>
    </tr>
  </tbody>
</table>


This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The test portfolios are the quality minus junk (QMJ) factor, the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7 and the low beta (BAB) factor (Frazzini and Pedersen 2014). We run a regression of each of SMB, HML, UMD, and BAB on the remaining factors excluding and including the QMJ factor as explanatory variable. Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to regression intercept, divided by the standard deviation of the estimated residuals. Sharpe ratios and information ratios are annualized.

Springer

---

# Page 65

98

C. S. Asness et al.

Table 21 Asset pricing tests: five-factor model plus UMD

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1963–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></

---

# Page 66

Quality minus junk

99

Table 21 (continued)

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1963–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
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
      <td>SMB</td>
      <td>SMB</td>
      <td>HML</td>
      <td>HML</td>
      <td>CMA</td>
      <td>CMA</td>
      <td>RMW</td>
      <td>RMW</td>
      <td>UMD</td>
      <td>UMD</td>
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
      <td>Information Ratio</td>
      <td>0.37</td>
      <td>0.61</td>
      <td>0.18</td>
      <td>0.56</td>
      <td>0.52</td>
      <td>0.57</td>
      <td>0.60</td>
      <td>−0.26</td>
      <td>0.63</td>
      <td>0.39</td>
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
      <td>Adjusted R2</td>
      <td>0.16</td>
      <td>0.21</td>
      <td>0.52</td>
      <td>0.60</td>
      <td>0.55</td>
      <td>0.55</td>
      <td>0.19</td>
      <td>0.57</td>
      <td>0.09</td>
      <td>0.13</td>
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
      <td>Panel B: Broad Sample (Global, 11/1990–12/2016)</td>
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
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>SMB</td>
      <td>SMB</td>
      <td>HML</td>
      <td>HML</td>
      <td>CMA</td>
      <td>CMA</td>
      <td>RMW</td>
      <td>RMW</td>
      <td>UMD</td>
      <td>UMD</td>
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
      <td></td>
      <td>0.56</td>
      <td>0.82</td>
      <td>0.07</td>
      <td>0.39</td>
      <td>0.46</td>
      <td>0.40</td>
      <td>1.08</td>
      <td>0.26</td>
      <td>0.56</td>
      <td>0.28</td>
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
      <td></td>
      <td>0.14</td>
      <td>0.21</td>
      <td>0.60</td>
      <td>0.65</td>
      <td>0.61</td>
      <td>0.61</td>
      <td>0.33</td>
      <td>0.58</td>
      <td>0.18</td>
      <td>0.23</td>
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


This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), profitability (RMW), and investment (CMA) portfolios from Fama and French (2015), the momentum (UMD) portfolios from Ken’s French data library, and the low beta (BAB) factor (Frazzini and Pedersen (2014)). Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from July 1963 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from November 1990 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized.

Springer

---

# Page 67

100

C. S. Asness et al.

Table 22 Asset pricing tests: five-factor model plus UMD and BAB

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1963–12/2016)</th>
      <th>Panel B: Broad Sample (Global, 11/1990–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>


---

# Page 68

Quality minus junk

101

Table 22 (continued)

<table>
  <thead>
    <tr>
      <th>Left-hand side</th>
      <th>Panel A: Long Sample (U.S., 7/1963–12/2016)</th>
      <th>Panel B: Broad Sample (Global, 11/1990–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th

---

# Page 69

102

C. S. Asness et al.

Table 23 Quality minus junk (Alternative Definition): returns

<table>
  <thead>
    <tr>
      <th></th>
      <th>Panel A: Long Sample (U.S., 7/1957–12/2016)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th>Panel B: Broad Sample (Global, 7/1989–12/2016)</th>
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
      <td>QMJ</td>
      <td>Profitability</td>
      <td>Safety</td>
      <td>Growth</td>
      <td>Payout</td>
      <td></td>
      <td>QMJ</td>
      <td>Profitability</td>
      <td>Safety</td>
      <td>Growth</td>
      <td>Payout</td>
      <td></td>
    </tr>
    <tr>
      <td>Excess Returns</td>
      <td>0.37</td>
      <td>0.25</td>
      <td>0.23</td>
      <td>0.17</td>
      <td>0.27</td>
      <td></td>
      <td>0.47</td>
      <td>0.39</td>
      <td>0.23</td>
      <td>0.15</td>
      <td>0.31</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(4.47)</td>
      <td>(3.69)</td>
      <td>(2.44)</td>
      <td>(2.46)</td>
      <td>(3.56)</td>
      <td></td>
      <td>(3.97)</td>
      <td>(4.34)</td>
      <td>(1.72)</td>
      <td>(1.96)</td>
      <td>(3.14)</td>
      <td></td>
    </tr>
    <tr>
      <td>CAPM-alpha</td>
      <td>0.50</td>
      <td>0.32</td>
      <td>0.40</td>
      <td>0.16</td>
      <td>0.41</td>
      <td></td>
      <td>0.61</td>
      <td>0.48</td>
      <td>0.40</td>
      <td>0.16</td>
      <td>0.42</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(7.11)</td>
      <td>(4.75)</td>
      <td>(5.52)</td>
      <td>(2.28)</td>
      <td>(6.33)</td>
      <td></td>
      <td>(7.18)</td>
      <td>(6.88)</td>
      <td>(4.49)</td>
      <td>(2.05)</td>
      <td>(5.45)</td>
      <td></td>
    </tr>
    <tr>
      <td>3-factor alpha</td>
      <td>0.59</td>
      <td>0.40</td>
      <td>0.52</td>
      <td>0.28</td>
      <td>0.37</td>
      <td></td>
      <td>0.67</td>
      <td>0.51</td>
      <td>0.51</td>
      <td>0.24</td>
      <td>0.37</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(10.12)</td>
      <td>(6.97)</td>
      <td>(9.06)</td>
      <td>(5.17)</td>
      <td>(6.66)</td>
      <td></td>
      <td>(9.52)</td>
      <td>(8.11)</td>
      <td>(7.91)</td>
      <td>(3.63)</td>
      <td>(5.55)</td>
      <td></td>
    </tr>
    <tr>
      <td>4-factor alpha</td>
      <td>0.62</td>
      <td>0.50</td>
      <td>0.51</td>
      <td>0.46</td>
      <td>0.22</td>
      <td></td>
      <td>0.59</td>
      <td>0.47</td>
      <td>0.39</td>
      <td>0.40</td>
      <td>0.16</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(9.96)</td>
      <td>(8.32)</td>
      <td>(8.39)</td>
      <td>(8.29)</td>
      <td>(3.84)</td>
      <td></td>
      <td>(7.83)</td>
      <td>(6.89)</td>
      <td>(5.73)</td>
      <td>(5.78)</td>
      <td>(2.36)</td>
      <td></td>
    </tr>
    <tr>
      <td>MKT</td>
      <td>−0.23</td>
      <td>−0.12</td>
      <td>−0.32</td>
      <td>−0.04</td>
      <td>−0.17</td>
      <td></td>
      <td>−0.28</td>
      <td>−0.19</td>
      <td>−0.35</td>
      <td>−0.03</td>
      <td>−0.20</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(−15.82)</td>
      <td>(−8.47)</td>
      <td>(−22.30)</td>
      <td>(−2.81)</td>
      <td>(−12.85)</td>
      <td></td>
      <td>(−16.79)</td>
      <td>(−12.73)</td>
      <td>(−22.74)</td>
      <td>(−2.06)</td>
      <td>(−13.27)</td>
      <td></td>
    </tr>
    <tr>
      <td>SMB</td>
      <td>−0.31</td>
      <td>−0.22</td>
      <td>−0.30</td>
      <td>−0.04</td>
      <td>−0.26</td>
      <td></td>
      <td>−0.38</td>
      <td>−0.28</td>
      <td>−0.23</td>
      <td>−0.12</td>
      <td>−0.26</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(−13.85)</td>
      <td>(−10.01)</td>
      <td>(−13.55)</td>
      <td>(−1.76)</td>
      <td>(−12.31)</td>
      <td></td>
      <td>(−10.42)</td>
      <td>(−8.32)</td>
      <td>(−6.79)</td>
      <td>(−3.56)</td>
      <td>(−8.20)</td>
      <td></td>
    </tr>
    <tr>
      <td>HML</td>
      <td>−0.23</td>
      <td>−0.29</td>
      <td>−0.28</td>
      <td>−0.49</td>
      <td>0.26</td>
      <td></td>
      <td>−0.12</td>
      <td>−0.06</td>
      <td>−0.25</td>
      <td>−0.38</td>
      <td>0.31</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(−9.67)</td>
      <td>(−12.57)</td>
      <td>(−11.91)</td>
      <td>(−23.09)</td>
      <td>(11.69)</td>
      <td></td>
      <td>(−3.42)</td>
      <td>(−1.83)</td>
      <td>(−7.98)</td>
      <td>(−12.17)</td>
      <td>(10.33)</td>
      <td></td>
    </tr>
    <tr>
      <td>UMD</td>
      <td>−0.03</td>
      <td>−0.10</td>
      <td>0.01</td>
      <td>−0.16</td>
      <td>0.14</td>
      <td></td>
      <td>0.07</td>
      <td>0.04</td>
      <td>0.11</td>
      <td>−0.14</td>
      <td>0.20</td>
      <td></td>
    </tr>
    <tr>
      <td></td>
      <td>(−1.31)</td>
      <td>(−4.87)</td>
      <td>(0.32)</td>
      <td>(−9.17)</td>
      <td>(7.75)</td>
      <td></td>
      <td>(2.66)</td>
      <td>(1.56)</td>
      <td>(4.63)</td>
      <td>(−5.86)</td>
      <td>(8.51)</td>
      <td></td>
    </tr>
    <tr>
      <td>Sharpe Ratio</td>
      <td>0.58</td>
      <td>0.48</td>
      <td>0.32</td>
      <td>0.32</td>
      <td>0.46</td>
      <td></td>
      <td>0.76</td>
      <td>0.83</td>
      <td>0.33</td>
      <td>0.37</td>
      <td>0.60</td>
      <td></td>
    </tr>
  </tbody>
</table>


Springer

---

# Page 70

Quality minus junk

103

Table 23 (continued)

<table>
  <thead>
    <tr>
      <th rowspan="2">Panel A: Long Sample (U.S., 7/1957–12/2016)</th>
      <th colspan="5">Panel B: Broad Sample (Global, 7/1989–12/2016)</th>
    </tr>
    <tr>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>Payout</th>
      <th>QMJ</th>
      <th>Profitability</th>
      <th>Safety</th>
      <th>Growth</th>
      <th>Payout</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Information Ratio</td>
      <td>1.40</td>
      <td>1.17</td>
      <td>1.18</td>
      <td>1.16</td>
      <td>0.54</td>
      <td>1.65</td>
      <td>1.45</td>
      <td>1.21</td>
      <td>1.22</td>
      <td>0.50</td>
    </tr>
    <tr>
      <td>Adjusted R2</td>
      <td>0.50</td>
      <td>0.34</td>
      <td>0.62</td>
      <td>0.46</td>
      <td>0.51</td>
      <td>0.66</td>
      <td>0.52</td>
      <td>0.78</td>
      <td>0.34</td>
      <td>0.63</td>
    </tr>
  </tbody>
</table>

This table shows calendar-time portfolio returns and factor loadings. Quality minus junk (QMJ) factors are constructed as the intersection of six value-weighted portfolios formed on size and quality. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. Portfolios based on profitability, growth, and safety scores are constructed in a similar manner. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7. Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Returns and alphas are in monthly percentage, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. “Information ratio” is equal to the four-factor alpha divided by the standard deviation of the estimated residuals in the time-series regression. Sharpe ratios and information ratios are annualized.

Springer

---

# Page 71

104

C. S. Asness et al.

![image](image_1.png)

Fig. 6 Cross Sectional Regressions Coefficient t-statistics by Industry. This figure plots coefficients from annual Fama-Macbeth regressions within 71 GICS industries. The dependent variable is the log of a firm’s market-to-book ratio in June of each calendar year (date t). The explanatory variables are the quality scores on date t and a series of controls. “Firm size” is the log of the firm’s market capitalization; “one-year return” is the firm’s stock return over the prior year. “Firm age” is the cumulative number of years since the firm’s IPO. “Uncertainty about mean profitability” (Pástor and Veronesi 2003) is the standard deviation of the residuals of an AR(1) model for each firm’s ROE, using the longest continuous series of a firm’s valid annual ROE up to date t. We require a minimum of 5 yrs of nonmissing ROEs. “Dividend payer” is a dummy equal to one if the firm paid any dividends over the prior year. With the exception of the “Dividend payer” dummy, all explanatory variables at time t are ranked cross-sectionally and rescaled to have a zero cross-sectional mean and a cross-sectional standard deviation of one. We plot t-statistics of the quality regression coefficient

Springer

---

# Page 72

Quality minus junk

105

## Panel A: Long Sample (U.S., 1957 - 2016)

![image](image_1.png)

- **QMJ Cumulative Return, Long Sample (U.S.)**

## Panel B: Broad Sample (Global, 1989 - 2016)

![image](image_2.png)

- **QMJ Cumulative Return, Broad Sample (Global)**

Springer

---

# Page 73

106

C. S. Asness et al.

**Fig. 7** QMJ: Cumulative Returns. This figure shows cumulative returns of quality minus junk (QMJ) factors. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QMJ factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. Panel A reports results from our *Long Sample* of domestic stocks. The sample period runs from June 1957 to December 2016. Panel B reports results from our *Broad Sample* of global stocks. The sample period runs from June 1989 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate

![image](image_1.png)

**Fig. 8** QMJ: 4-Factor Alphas by Year. This figure plots four-factor adjusted information ratios of quality minus junk (QMJ) factors. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. Information ratios are equal to the intercept of a time-series regression of monthly excess return divided by the standard deviation of the estimated residuals. The explanatory variables are the monthly returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. We run a separate regression by year. Alphas are annualized

Springer

---

# Page 74

Quality minus junk

107

![image](image_1.png)

Fig. 9 QMJ: Four-Factor Adjusted Information Ratios by Size. This figure plots four-factor adjusted information ratios of quality minus junk (QMJ) factors. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. Information ratios are equal to the intercept of a time-series regression of monthly excess return divided by the standard deviation of the estimated residuals. The explanatory variables are the monthly returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Information ratios are annualized

Springer

---

# Page 75

108

C. S. Asness et al.

Panel A: Long Sample (U.S., 1957 - 2016)

![image](image_1.png)

Panel B: Broad Sample (Global, 1989 - 2016)

![image](image_2.png)

Fig. 10 QMJ: Four-Factor Adjusted Information Ratios by Industry. This figure plots four-factor adjusted information ratios of quality minus junk (QMJ) factor within 71 GICS industries. Information ratios are equal to the intercept of a time-series regression of monthly excess return divided by the standard deviation of the estimated residuals. The explanatory variables are the monthly returns of the market (MKT), size (SMB), book-to-market (HML), and momentum (UMD) portfolios from Fig. 7. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Information ratios are annualized

Springer

---

# Page 76

Quality minus junk

109

![image](image_1.png)

Fig. 11 Cross-Sectional Regressions Coefficient, the Price of Quality. This figure plots coefficients from monthly cross-sectional regressions. The dependent variable is the log of a firm’s market-to-book ratio in in month t. The explanatory variables are the quality scores in month t. We plot the time series of the cross-sectional coefficients

Springer

---

# Page 77

110

C. S. Asness et al.

![image](image_1.png)

Fig. 12 Quality at a Reasonable Price (QARP). This figure plots monthly returns of quality at a reasonable price (QARP) factors. QARP factors are constructed as the intersection of six value-weighted portfolios formed on size and price adjusted quality $n \, Quality_t^i - z(P_t^i)$ , where $z(P_t^i)$ is the z-score of a firm’s market-to-book and $n$ a constant. At the end of each calendar month, stocks are assigned to two size-sorted portfolios based on their market capitalization. For U.S. securities, the size breakpoint is the median NYSE market equity. For other markets, the size breakpoint is the 80th percentile by country. We use conditional sorts, first sorting on size, then on quality. Portfolios are value-weighted, refreshed every calendar month, and rebalanced every calendar month to maintain value weights. The QARP factor return is the average return on the two high-quality portfolios minus the average return on the two low-quality (junk) portfolios. We form one set of portfolios in each country and compute global portfolios by weighting each country’s portfolio by the country’s total (lagged) market capitalization. The figure reports results from our *Long Sample* of domestic stocks and from our *Broad Sample* of global stocks. The long sample period runs from July 1963 to December 2016. The broad sample period runs from June 1990 to December 2016. Returns are in U.S. dollars, do not include currency hedging, and excess returns are over the U.S. Treasury bill rate. Alpha is the intercept in a time-series regression of monthly excess return. The explanatory variables are the returns of the market (MKT) portfolios from Fig. 7. The figures plot the monthly alpha as function of $n$

Open Access This article is distributed under the terms of the Creative Commons Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/), which permits unrestricted use, distribution, and reproduction in any medium, provided you give appropriate credit to the original author(s) and the source, provide a link to the Creative Commons license, and indicate if changes were made.

## References

Acharya, V., & Pedersen, L. H. (2005). Asset pricing with liquidity risk. *Journal of Financial Economics*, 77, 375–410.

Altman, E. I. (1968). Financial ratios, discriminant analysis and the prediction of corporate bankruptcy. *The Journal of Finance*, 23(4), 589–609.

$\mathcal{S}$ Springer

---

# Page 78

Quality minus junk

111

Amihud, Y., & Mendelson, H. (1986). Asset pricing and the bid-ask spread. *Journal of Financial Economics*, 17(2), 223–249.

Ang, A., Hodrick, R., Xing, Y., & Zhang, X. (2006). The cross-section of volatility and expected returns. *Journal of Finance*, 61, 259–299.

Asness, C., (1994). Variables that explain stock returns. Ph.D. Dissertation, University of Chicago.

Asness, C., & Frazzini, A. (2013). The devil in HML’s detail. *Journal of Portfolio Management*, 39, 49–68.

Asness, C., Frazzini, A., Israel, R., Moskowitz, T. J., & Pedersen, L. H. (2018). Size matters, if you control your junk. *Journal of Financial Economics*, 129(3), 479–509.

Baker, M., & Wurgler, J. (2002). Market timing and capital structure. *Journal of Finance*, 57, 1–32.

Banz, R. W. (1981). The relationship between return and market value of common stocks. *Journal of Financial Economics*, 9, 3–18.

Berk, J. B. (1995). A critique of size-related anomalies. *The Review of Financial Studies*, 8(2), 275–286.

Black, F., Jensen, M. C., & Scholes, M. (1972). The capital asset pricing model: Some empirical tests. In M. C. Jensen (Ed.), *Studies in the theory of capital markets* (pp. 79–121). New York: Praeger.

Brav, A., Lehavy, R., & Michaely, R. (2005). Using expectations to test asset pricing models. *Financial Management*, 34(3), 31–64.

Campbell, J. Y., & Shiller, R. J. (1988). The dividend-price ratio and expectations of future dividends and discount factors. *Review of Financial Studies*, 1, 195–228.

Campbell, J. Y., Hilscher, J., & Szilagyi, J. (2008). In search of distress risk. *Journal of Finance*, 63, 2899–2939.

Carhart, M. M. (1997). On persistence in mutual fund performance. *The Journal of Finance*, 52(1), 57–82.

Cochrane, J. (2011). Presidential address: Discount rates. *The Journal of Finance*, 66(4), 1047–1108.

Cohen, R. B., Polk, C., & Vuolteenaho, T. (2003). The value spread. *The Journal of Finance*, 58, 609–642.

Cohen, R. B., Polk, C., & Vuolteenaho, T. (2009). The price is (almost) right. *The Journal of Finance*, 64, 2739–2782.

Daniel, K., & Titman, S. (2006). Market reaction to tangible and intangible information. *Journal of Finance*, 61, 1605–1643.

Dechow, P., & You, H. (2017). Determinants of errors in analysts’ target price implied returns. Working paper, University of Southern California.

Duffie, D., Garleanu, N., & Pedersen, L. H. (2002). Securities lending, shorting, and pricing. *Journal of Financial Economics*, 66, 307–339.

Fama, E. F., & French, K. R. (1992). The cross-section of expected stock returns. *The Journal of Finance*, 47(2), 427–465.

Fama, E. F., & French, K. R. (1993). Common risk factors in the returns on stocks and bonds. *Journal of Financial Economics*, 33, 3–56.

Fama, E. F., & French, K. R. (2006). Profitability, investment and average returns. *Journal of Financial Economics*, 82, 461–518.

Fama, E. F., & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116, 1–22.

Fama, E. F., & MacBeth, J. D. (1973). Risk, return, and equilibrium: Empirical tests. *The Journal of Political Economy*, 81, 607–636.

Feltham, G. A., & Ohlson, J. A. (1999). Residual earnings valuation with risk and stochastic interest rates. *The Accounting Review*, 74(2), 165–183.

Frankel, R., & Lee, C. (1998). Accounting valuation, market expectation, and cross-sectional stock returns. *Journal of Accounting and Economics*, 25, 283–319.

Frazzini, A., & Pedersen, L. H. (2014). Betting against beta. *Journal of Financial Economics*, 111(1), 1–25.

George, T. J., & Hwang, C. Y. (2010). A resolution of the distress risk and leverage puzzles in the cross section of stock returns. *Journal of Financial Economics*, 96, 56–79.

Graham, B., & Dodd, D. L. (1934). *Security analysis*. New York: McGraw-Hill.

Jegadeesh, N., & Titman, S. (1993). Returns to buying winners and selling losers: Implications for stock market efficiency. *The Journal of Finance*, 48(1), 65–91.

Jensen, M. C. (1986). Agency costs of free cash flow, corporate finance, and takeovers. *The American Economic Review*, 76(2), 323–329.

McLean, D., Pontiff, J., & Watanabe, A. (2009). Share issuance and cross-sectional returns: International evidence. *Journal of Financial Economics*, 94, 1–17.

McNichols, M., & O’Brien, P. C. (1997). Self-selection and analyst coverage. *Journal of Accounting Research*, 35, 167–199.

Mohanram, P. (2005). Separating winners from losers among low book-to-market stocks using financial statement analysis. *Review of Accounting Studies*, 10, 133–170.

$\mathcal{S}$ Springer

---

# Page 79

112

C. S. Asness et al.

Newey, W. K., & West, K. D. (1987). A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. *Econometrica*, 55(3), 703–708.

Novy-Marx, R. (2012). Quality investing. Working paper, Rochester.

Novy-Marx, R. (2013). The other side of value: The gross profitability premium. *Journal of Financial Economics*, 108(1), 1–28.

Ohlson, J. A. (1980). Financial ratios and the probabilistic prediction of bankruptcy. *Journal of Accounting Research*, 18(1), 109–131.

Pástor, L., & Stambaugh, R. F. (2003). Liquidity risk and expected stock returns. *Journal of Political Economy*, 111(3), 642–685.

Pástor, L., & Veronesi, P. (2003). Stock valuation and learning about profitability. *The Journal of Finance*, 58(5), 1749–1790.

Penman, S., Richardson, S., & Tuna, I. (2007). The book-to-price effect in stock returns: Accounting for leverage. *Journal of Accounting Research*, 45(2), 427–467.

Piotroski, J. D. (2000). Value investing: The use of historical financial statement information to separate winners from losers. *Journal of Accounting Research*, 38, 1–41.

Pontiff, J., & Woodgate, W. (2008). Share issuance and cross-sectional returns. *Journal of Finance*, 63, 921–945.

Richardson, S., Sloan, R. G., Soliman, M., & Tuna, I. (2005). Accrual reliability, earnings persistence and stock prices. *Journal of Accounting and Economics*, 39(3), 437–485.

Roll, R. (1984). Orange juice and weather. *American Economic Review*, 74(5), 861–880.

Roll, R. (1988). R2. *Journal of Finance*, 43, 541–566.

Shleifer, A., & Vishny, R. W. (1997). The limits of arbitrage. *The Journal of Finance*, 52(1), 35–55.

Shumway, T. (1997). "The delisting bias in CRSP data." *The Journal of Finance* 52.1, 327–340.

Sloan, R. G. (1996). Do stock prices reflect information in accruals and cash flows about future earnings? *The Accounting Review*, 71, 289–315.

Summer, L. H. (1986). Does the stock market rationally reflect fundamental values? *The Journal of Finance*, 41(3), 591–601.

Vuolteenaho, T. (2002). What drives firm-level stock returns? *The Journal of Finance*, 57(1), 233–264.

Springer