# Page 1

Journal of Financial Economics 111 (2014) 1–25

Contents lists available at ScienceDirect

Journal of Financial Economics

journal homepage: www.elsevier.com/locate/jfec

ELSEVIER

# Betting against beta $^\star$

Andrea Frazzini $^{a}$ , Lasse Heje Pedersen $^{a,b,c,d,e,*}$

$^{a}$ AQR Capital Management, CT 06830, USA  
$^{b}$ Stern School of Business, New York University, 44 West Fourth Street, Suite 9-190, NY 10012, USA  
$^{c}$ Copenhagen Business School, 2000 Frederiksberg, Denmark  
$^{d}$ Center for Economic Policy Research (CEPR), London, UK  
$^{e}$ National Bureau of Economic Research (NBER), MA, USA

---

## A R T I C L E I N F O

Article history:  
Received 16 December 2010  
Received in revised form  
10 April 2013  
Accepted 19 April 2013  
Available online 17 October 2013

JEL classification:  
G01  
G11  
G12  
G14  
G15

Keywords:  
Asset prices  
Leverage constraints  
Margin requirements  
Liquidity  
Beta  
CAPM

---

## A B S T R A C T

We present a model with leverage and margin constraints that vary across investors and time. We find evidence consistent with each of the model’s five central predictions: (1) Because constrained investors bid up high-beta assets, high beta is associated with low alpha, as we find empirically for US equities, 20 international equity markets, Treasury bonds, corporate bonds, and futures. (2) A betting against beta (BAB) factor, which is long leveraged low-beta assets and short high-beta assets, produces significant positive risk-adjusted returns. (3) When funding constraints tighten, the return of the BAB factor is low. (4) Increased funding liquidity risk compresses betas toward one. (5) More constrained investors hold riskier assets.

© 2013 Elsevier B.V. All rights reserved.

---

## 1. Introduction

A basic premise of the capital asset pricing model (CAPM) is that all agents invest in the portfolio with the highest expected excess return per unit of risk (Sharpe ratio) and leverage or de-leverage this portfolio to suit their risk preferences. However, many investors, such as individuals, pension funds, and mutual funds, are constrained in the leverage that they can take, and they therefore overweight risky securities instead of using

---

$^\star$ We thank Cliff Asness, Aaron Brown, John Campbell, Josh Coval (discussant), Kent Daniel, Gene Fama, Nicolae Garleanu, John Heaton (discussant), Michael Katz, Owen Lamont, Juhani Linnainmaa (discussant), Michael Mendelson, Mark Mitchell, Lubos Pastor (discussant), Matt Richardson, William Schwert (editor), Tuomo Vuolteenaho, Robert Whitelaw and two anonymous referees for helpful comments and discussions as well as seminar participants at AQR Capital Management, Columbia University, New York University, Yale University, Emory University, University of Chicago Booth School of Business, Northwestern University Kellogg School of Management, Harvard University, Boston University, Vienna University of Economics and Business, University of Mannheim, Goethe University Frankfurt, the American Finance Association meeting, NBER conference, Utah Winter Finance Conference, Annual Management Conference at University of Chicago Booth School of Business, Bank of America and Merrill Lynch Quant Conference, and Nomura Global Quantitative Investment Strategies Conference. Lasse Heje Pedersen gratefully acknowledges support from the European Research Council (ERC Grant no. 312417) and the FRIC Center for Financial Frictions (Grant no. DNRF102).

$^*$ Corresponding author at: Stern School of Business, New York University, 44 West Fourth Street, Suite 9-190, NY 10012, USA.  
E-mail address: lpederse@stern.nyu.edu (L.H. Pedersen).

0304-405X/$ – see front matter © 2013 Elsevier B.V. All rights reserved.  
http://dx.doi.org/10.1016/j.jfineco.2013.10.005

---

# Page 2

2 A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

leverage. For instance, many mutual fund families offer balanced funds in which the “normal” fund may invest around 40% in long-term bonds and 60% in stocks, whereas the “aggressive” fund invests 10% in bonds and 90% in stocks. If the “normal” fund is efficient, then an investor could leverage it and achieve a better trade-off between risk and expected return than the aggressive portfolio with a large tilt toward stocks. The demand for exchange-traded funds (ETFs) with embedded leverage provides further evidence that many investors cannot use leverage directly.

This behavior of tilting toward high-beta assets suggests that risky high-beta assets require lower risk-adjusted returns than low-beta assets, which require leverage. Indeed, the security market line for US stocks is too flat relative to the CAPM (Black, Jensen, and Scholes, 1972) and is better explained by the CAPM with restricted borrowing than the standard CAPM [see Black (1972, 1993), Brennan (1971), and Mehrling (2005) for an excellent historical perspective].

Several questions arise: How can an unconstrained arbitrageur exploit this effect, i.e., how do you bet against beta? What is the magnitude of this anomaly relative to the size, value, and momentum effects? Is betting against beta rewarded in other countries and asset classes? How does the return premium vary over time and in the cross section? Who bets against beta?

We address these questions by considering a dynamic model of leverage constraints and by presenting consistent empirical evidence from 20 international stock markets, Treasury bond markets, credit markets, and futures markets.

Our model features several types of agents. Some agents cannot use leverage and, therefore, overweight high-beta assets, causing those assets to offer lower returns. Other agents can use leverage but face margin constraints. Unconstrained agents underweight (or short-sell) high-beta assets and buy low-beta assets that they lever up. The model implies a flatter security market line (as in Black (1972)), where the slope depends on the tightness (i.e., Lagrange multiplier) of the funding constraints on average across agents (Proposition 1).

One way to illustrate the asset pricing effect of the funding friction is to consider the returns on market-neutral betting against beta (BAB) factors. A BAB factor is a portfolio that holds low-beta assets, leveraged to a beta of one, and that shorts high-beta assets, de-leveraged to a beta of one. For instance, the BAB factor for US stocks achieves a zero beta by holding $1.4 of low-beta stocks and shortselling $0.7 of high-beta stocks, with offsetting positions in the risk-free asset to make it self-financing.$^{1}$ Our model predicts that BAB factors have a positive average return and that the return is increasing in the ex ante tightness of constraints and in the spread in betas between high- and low-beta securities (Proposition 2).

$^{1}$ While we consider a variety of BAB factors within a number of markets, one notable example is the zero-covariance portfolio introduced by Black (1972) and studied for US stocks by Black, Jensen, and Scholes (1972), Kandel (1984), Shanken (1985), Polk, Thompson, and Vuolteenaho (2006), and others.

When the leveraged agents hit their margin constraint, they must de-leverage. Therefore, the model predicts that, during times of tightening funding liquidity constraints, the BAB factor realizes negative returns as its expected future return rises (Proposition 3). Furthermore, the model predicts that the betas of securities in the cross section are compressed toward one when funding liquidity risk is high (Proposition 4). Finally, the model implies that more-constrained investors overweight high-beta assets in their portfolios and less-constrained investors overweight low-beta assets and possibly apply leverage (Proposition 5).

Our model thus extends the Black (1972) insight by considering a broader set of constraints and deriving the dynamic time series and cross-sectional properties arising from the equilibrium interaction between agents with different constraints.

We find consistent evidence for each of the model’s central predictions. To test Proposition 1, we first consider portfolios sorted by beta within each asset class. We find that alphas and Sharpe ratios are almost monotonically declining in beta in each asset class. This finding provides broad evidence that the relative flatness of the security market line is not isolated to the US stock market but that it is a pervasive global phenomenon. Hence, this pattern of required returns is likely driven by a common economic cause, and our funding constraint model provides one such unified explanation.

To test Proposition 2, we construct BAB factors within the US stock market and within each of the 19 other developed MSCI stock markets. The US BAB factor realizes a Sharpe ratio of 0.78 between 1926 and March 2012. To put this BAB factor return in perspective, note that its Sharpe ratio is about twice that of the value effect and 40% higher than that of momentum over the same time period. The BAB factor has highly significant risk-adjusted returns, accounting for its realized exposure to market, value, size, momentum, and liquidity factors (i.e., significant one-, three-, four-, and five-factor alphas), and it realizes a significant positive return in each of the four 20-year subperiods between 1926 and 2012.

We find similar results in our sample of international equities. Combining stocks in each of the non-US countries produces a BAB factor with returns about as strong as the US BAB factor.

We show that BAB returns are consistent across countries, time, within deciles sorted by size, and within deciles sorted by idiosyncratic risk and are robust to a number of specifications. These consistent results suggest that coincidence or data mining are unlikely explanations. However, if leverage constraints are the underlying drivers as in our model, then the effect should also exist in other markets.

Hence, we examine BAB factors in other major asset classes. For US Treasuries, the BAB factor is a portfolio that holds leveraged low-beta (i.e., short-maturity) bonds and shortsells de-leveraged high-beta (i.e., long-term) bonds. This portfolio produces highly significant risk-adjusted returns with a Sharpe ratio of 0.81. This profitability of shortselling long-term bonds could seem to contradict the well-known “term premium” in fixed income markets. There is no paradox, however. The term premium means

---

# Page 3

that investors are compensated on average for holding long-term bonds instead of T-bills because of the need for maturity transformation. The term premium exists at all horizons, however. Just as investors are compensated for holding ten-year bonds over T-bills, they are also compensated for holding one-year bonds. Our finding is that the compensation per unit of risk is in fact larger for the one-year bond than for the ten-year bond. Hence, a portfolio that has a leveraged long position in one-year (and other short-term) bonds and a short position in long-term bonds produces positive returns. This result is consistent with our model in which some investors are leverage-constrained in their bond exposure and, therefore, require lower risk-adjusted returns for long-term bonds that give more “bang for the buck”. Indeed, short-term bonds require tremendous leverage to achieve similar risk or return as long-term bonds. These results complement those of Fama (1984, 1986) and Duffee (2010), who also consider Sharpe ratios across maturities implied by standard term structure models.

We find similar evidence in credit markets: A leveraged portfolio of highly rated corporate bonds outperforms a de-leveraged portfolio of low-rated bonds. Similarly, using a BAB factor based on corporate bond indices by maturity produces high risk-adjusted returns.

We test the time series predictions of Proposition 3 using the TED spread as a measure of funding conditions. Consistent with the model, a higher TED spread is associated with low contemporaneous BAB returns. The lagged TED spread predicts returns negatively, which is inconsistent with the model if a high TED spread means a high tightness of investors’ funding constraints. This result could be explained if higher TED spreads meant that investors’ funding constraints would be tightening as their banks reduce credit availability over time, though this is speculation.

To test the prediction of Proposition 4, we use the volatility of the TED spread as an empirical proxy for funding liquidity risk. Consistent with the model’s beta-compression prediction, we find that the dispersion of betas is significantly lower when funding liquidity risk is high.

Lastly, we find evidence consistent with the model’s portfolio prediction that more-constrained investors hold higher-beta securities than less-constrained investors (Proposition 5). We study the equity portfolios of mutual funds and individual investors, which are likely to be constrained. Consistent with the model, we find that these investors hold portfolios with average betas above one. On the other side of the market, we find that leveraged buyout (LBO) funds acquire firms with average betas below 1 and apply leverage. Similarly, looking at the holdings of Warren Buffett’s firm Berkshire Hathaway, we see that Buffett bets against beta by buying low-beta stocks and applying leverage (analyzed further in Frazzini, Kabiller, and Pedersen (2012)).

Our results shed new light on the relation between risk and expected returns. This central issue in financial economics has naturally received much attention. The standard CAPM beta cannot explain the cross section of unconditional stock returns (Fama and French, 1992) or conditional stock returns (Lewellen and Nagel, 2006). Stocks with high beta have been found to deliver low risk-adjusted returns (Black, Jensen, and Scholes, 1972; Baker, Bradley, and Wurgler, 2011); thus, the constrained-borrowing CAPM has a better fit (Gibbons, 1982; Kandel, 1984; Shanken, 1985). Stocks with high idiosyncratic volatility have realized low returns (Falkenstein, 1994; Ang, Hodrick, Xing, Zhang, 2006, 2009), but we find that the beta effect holds even when controlling for idiosyncratic risk. $^{2}$ Theoretically, asset pricing models with benchmarked managers (Brennan, 1993) or constraints imply more general CAPM-like relations (Hindy, 1995; Cuoco, 1997). In particular, the margin-CAPM implies that high-margin assets have higher required returns, especially during times of funding illiquidity (Garleanu and Pedersen, 2011; Ashcraft, Garleanu, and Pedersen, 2010). Garleanu and Pedersen (2011) show empirically that deviations of the law of one price arises when high-margin assets become cheaper than low-margin assets, and Ashcraft, Garleanu, and Pedersen (2010) find that prices increase when central bank lending facilities reduce margins. Furthermore, funding liquidity risk is linked to market liquidity risk (Gromb and Vayanos, 2002; Brunnermeier and Pedersen, 2009), which also affects required returns (Acharya and Pedersen, 2005). We complement the literature by deriving new cross-sectional and time series predictions in a simple dynamic model that captures leverage and margin constraints and by testing its implications across a broad cross section of securities across all the major asset classes. Finally, Asness, Frazzini, and Pedersen (2012) report evidence of a low-beta effect across asset classes consistent with our theory.

The rest of the paper is organized as follows. Section 2 lays out the theory, Section 3 describes our data and empirical methodology, Sections 4–7 test Propositions 1–5, and Section 8 concludes. Appendix A contains all proofs, Appendix B provides a number of additional empirical results and robustness tests, and Appendix C provides a calibration of the model. The calibration shows that, to match the strong BAB performance in the data, a large fraction of agents must face severe constraints. An interesting topic for future research is to empirically estimate agents’ leverage constraints and risk preferences and study whether the magnitude of the BAB returns is consistent with the model or should be viewed as a puzzle.

## 2. Theory

We consider an overlapping-generations (OLG) economy in which agents $i = 1, \ldots, I$ are born each time period $t$ with wealth $W_t^i$ and live for two periods. Agents trade securities $s = 1, \ldots, S$ , where security $s$ pays dividends $\delta_t^s$ and has $x^{*s}$ shares outstanding. $^{3}$ Each time period $t$ , young

---

$^{2}$ This effect disappears when controlling for the maximum daily return over the past month (Bali, Cakici, and Whitelaw, 2011) and when using other measures of idiosyncratic volatility (Fu, 2009).

$^{3}$ The dividends and shares outstanding are taken as exogenous. Our modified CAPM has implications for a corporation’s optimal capital structure, which suggests an interesting avenue of future research beyond the scope of this paper.

---

# Page 4

4

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

agents choose a portfolio of shares $x = (x^1, \ldots, x^S)$ , investing the rest of their wealth at the risk-free return $r^f$ , to maximize their utility:

$$
\max x'(E_t(P_{t+1} + \delta_{t+1}) - (1 + r^f)P_t) - \frac{\gamma^i}{2}x'\Omega_t x,
\quad (1)
$$

where $P_t$ is the vector of prices at time $t$ , $\Omega_t$ is the variance–covariance matrix of $P_{t+1} + \delta_{t+1}$ , and $\gamma^i$ is agent $i$ ’s risk aversion. Agent $i$ is subject to the portfolio constraint

$$
m_t^i \sum_s x^s P_t^s \leq W_t^i
\quad (2)
$$

This constraint requires that some multiple $m_t^i$ of the total dollars invested, the sum of the number of shares $x^s$ times their prices $P^s$ , must be less than the agent’s wealth.

The investment constraint depends on the agent $i$ . For instance, some agents simply cannot use leverage, which is captured by $m^i = 1$ [as Black (1972) assumes]. Other agents not only could be precluded from using leverage but also must have some of their wealth in cash, which is captured by $m^i$ greater than one. For instance, $m^i = 1/(1 - 0.20) = 1.25$ represents an agent who must hold 20% of her wealth in cash. For instance, a mutual fund could need some ready cash to be able to meet daily redemptions, an insurance company needs to pay claims, and individual investors may need cash for unforeseen expenses.

Other agents could be able to use leverage but could face margin constraints. For instance, if an agent faces a margin requirement of 50%, then his $m^i$ is 0.50. With this margin requirement, the agent can invest in assets worth twice his wealth at most. A smaller margin requirement $m^i$ naturally means that the agent can take greater positions. Our formulation assumes for simplicity that all securities have the same margin requirement, which may be true when comparing securities within the same asset class (e.g., stocks), as we do empirically. Garleanu and Pedersen (2011) and Ashcraft, Garleanu, and Pedersen (2010) consider assets with different margin requirements and show theoretically and empirically that higher margin requirements are associated with higher required returns (Margin CAPM).

We are interested in the properties of the competitive equilibrium in which the total demand equals the supply:

$$
\sum_i x^i = x^*
\quad (3)
$$

To derive equilibrium, consider the first order condition for agent $i$ :

$$
0 = E_t(P_{t+1} + \delta_{t+1}) - (1 + r^f)P_t - \gamma^i \Omega x^i - \psi_t^i P_t,
\quad (4)
$$

where $\psi^i$ is the Lagrange multiplier of the portfolio constraint. Solving for $x^i$ gives the optimal position:

$$
x^i = \frac{1}{\gamma^i} \Omega^{-1} (E_t(P_{t+1} + \delta_{t+1}) - (1 + r^f + \psi_t^i)P_t).
\quad (5)
$$

The equilibrium condition now follows from summing over these positions:

$$
x^* = \frac{1}{\gamma} \Omega^{-1} (E_t(P_{t+1} + \delta_{t+1}) - (1 + r^f + \psi_t)P_t),
\quad (6)
$$

where the aggregate risk aversion $\gamma$ is defined by $1/\gamma = \Sigma_i 1/\gamma^i$ and $\psi_t = \sum_i (\gamma/\gamma^i) \psi_t^i$ is the weighted average Lagrange multiplier. (The coefficients $\gamma/\gamma^i$ sum to one by definition of the aggregate risk aversion $\gamma$ .) The equilibrium price can then be computed:

$$
P_t = \frac{E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*}{1 + r^f + \psi_t},
\quad (7)
$$

Translating this into the return of any security $r_{t+1}^i = (P_{t+1}^i + \delta_{t+1}^i)/P_t^i - 1$ , the return on the market $r_{t+1}^M$ , and using the usual expression for beta, $\beta_t^s = \text{cov}_t(r_{t+1}^s, r_{t+1}^M)/\text{var}_t(r_{t+1}^M)$ , we obtain the following results. (All proofs are in Appendix A, which also illustrates the portfolio choice with leverage constraints in a mean-standard deviation diagram.)

**Proposition 1 (high beta is low alpha).**

(i) The equilibrium required return for any security $s$ is

$$
E_t(r_{t+1}^s) = r^f + \psi_t + \beta_t^s \lambda_t
\quad (8)
$$

where the risk premium is $\lambda_t = E_t(r_{t+1}^M) - r^f - \psi_t$ and $\psi_t$ is the average Lagrange multiplier, measuring the tightness of funding constraints.

(ii) A security’s alpha with respect to the market is $\alpha_t^s = \psi_t(1 - \beta_t^s)$ . The alpha decreases in the beta, $\beta_t^s$ .

(iii) For an efficient portfolio, the Sharpe ratio is highest for an efficient portfolio with a beta less than one and decreases in $\beta_t^s$ for higher betas and increases for lower betas.

As in Black’s CAPM with restricted borrowing (in which $m^i = 1$ for all agents), the required return is a constant plus beta times a risk premium. Our expression shows explicitly how risk premia are affected by the tightness of agents’ portfolio constraints, as measured by the average Lagrange multiplier $\psi_t$ . Tighter portfolio constraints (i.e., a larger $\psi_t$ ) flatten the security market line by increasing the intercept and decreasing the slope $\lambda_t$ .

Whereas the standard CAPM implies that the intercept of the security market line is $r^f$ , the intercept here is increased by binding funding constraints (through the weighted average of the agents’ Lagrange multipliers). One could wonder why zero-beta assets require returns in excess of the risk-free rate. The answer has two parts. First, constrained agents prefer to invest their limited capital in riskier assets with higher expected return. Second, unconstrained agents do invest considerable amounts in zero-beta assets so, from their perspective, the risk of these assets is not idiosyncratic, as additional exposure to such assets would increase the risk of their portfolio. Hence, in equilibrium, zero-beta risky assets must offer higher returns than the risk-free rate.

Assets that have zero covariance to the Tobin (1958) “tangency portfolio” held by an unconstrained agent do earn the risk-free rate, but the tangency portfolio is not the market portfolio in our equilibrium. The market portfolio is the weighted average of all investors’ portfolios, i.e., an average of the tangency portfolio held by unconstrained investors and riskier portfolios held by constrained investors. Hence, the market portfolio has higher risk and expected return than the tangency portfolio, but a lower Sharpe ratio.

---

# Page 5

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

The portfolio constraints further imply a lower slope $\lambda_t$ of the security market line, i.e., a lower compensation for a marginal increase in systematic risk. The slope is lower because constrained agents need high unleveraged returns and are, therefore, willing to accept less compensation for higher risk. $^4$

We next consider the properties of a factor that goes long low-beta assets and short sells high-beta assets. To construct such a factor, let $w_t$ be the relative portfolio weights for a portfolio of low-beta assets with return $r_{t+1}^L = w_t r_{t+1}$ and consider similarly a portfolio of high-beta assets with return $r_{t+1}^H$ . The betas of these portfolios are denoted $\beta_t^L$ and $\beta_t^H$ , where $\beta_t^L < \beta_t^H$ . We then construct a betting against beta (BAB) factor as

$$
r_{t+1}^{BAB} = \frac{1}{\beta_t^L}(r_{t+1}^L - r^f) - \frac{1}{\beta_t^H}(r_{t+1}^H - r^f)
\quad (9)
$$

this portfolio is market-neutral; that is, it has a beta of zero. The long side has been leveraged to a beta of one, and the short side has been de-leveraged to a beta of one. Furthermore, the BAB factor provides the excess return on a self-financing portfolio, such as HML (high minus low) and SMB (small minus big), because it is a difference between excess returns. The difference is that BAB is not dollar-neutral in terms of only the risky securities because this would not produce a beta of zero. $^5$ The model has several predictions regarding the BAB factor.

**Proposition 2 (positive expected return of BAB).** The expected excess return of the self-financing BAB factor is positive

$$
E_t(r_{t+1}^{BAB}) = \frac{\beta_t^H - \beta_t^L}{\beta_t^L \beta_t^H} \psi_t \geq 0
\quad (10)
$$

and increasing in the ex ante beta spread $(\beta_t^H - \beta_t^L)/(\beta_t^L \beta_t^H)$ and funding tightness $\psi_t$ .

**Proposition 2** shows that a market-neutral BAB portfolio that is long leveraged low-beta securities and short higher-beta securities earns a positive expected return on average. The size of the expected return depends on the spread in the betas and how binding the portfolio constraints are in the market, as captured by the average of the Lagrange multipliers $\psi_t$ .

**Proposition 3** considers the effect of a shock to the portfolio constraints (or margin requirements), $m^k$ , which can be interpreted as a worsening of funding liquidity,

a credit crisis in the extreme. Such a funding liquidity shock results in losses for the BAB factor as its required return increases. This happens because agents may need to de-leverage their bets against beta or stretch even further to buy the high-beta assets. Thus, the BAB factor is exposed to funding liquidity risk, as it loses when portfolio constraints become more binding.

**Proposition 3 (funding shocks and BAB returns).** A tighter portfolio constraint, that is, an increase in $m_t^k$ for some of $k$ , leads to a contemporaneous loss for the BAB factor

$$
\frac{\partial r_t^{BAB}}{\partial m_t^k} \leq 0
\quad (11)
$$

and an increase in its future required return:

$$
\frac{\partial E_t(r_{t+1}^{BAB})}{\partial m_t^k} \geq 0
\quad (12)
$$

Funding shocks have further implications for the cross section of asset returns and the BAB portfolio. Specifically, a funding shock makes all security prices drop together (that is, $(\partial P_t^s / \partial \psi_t)/P_t^s$ is the same for all securities $s$ ). Therefore, an increased funding risk compresses betas toward one. $^6$ If the BAB portfolio construction is based on an information set that does not account for this increased funding risk, then the BAB portfolio’s conditional market beta is affected.

**Proposition 4 (beta compression).** Suppose that all random variables are identically and independently distributed (i.i.d.) over time and $\delta_t$ is independent of the other random variables. Further, at time $t-1$ after the BAB portfolio is formed and prices are set, the conditional variance of the discount factor $1/(1 + r^f + \psi_t)$ rises (falls) due to new information about $m_t$ and $W_t$ . Then,

(i) The conditional return betas $\beta_{t-1}^i$ of all securities are compressed toward one (more dispersed), and

(ii) The conditional beta of the BAB portfolio becomes positive (negative), even though it is market neutral relative to the information set used for portfolio formation.

In addition to the asset-pricing predictions that we derive, funding constraints naturally affect agents’ portfolio choices. In particular, more-constrained investors tilt toward riskier securities in equilibrium and less-constrained agents tilt toward safer securities with higher reward per unit of risk. To state this result, we write next

---

$^4$ While the risk premium implied by our theory is lower than the one implied by the CAPM, it is still positive. It is difficult to empirically estimate a low risk premium and its positivity is not a focus of our empirical tests as it does not distinguish our theory from the standard CAPM. However, the data are generally not inconsistent with our prediction as the estimated risk premium is positive and insignificant for US stocks, negative and insignificant for international stocks, positive and insignificant for Treasuries, positive and significant for credits across maturities, and positive and significant across asset classes.

$^5$ A natural BAB factor is the zero-covariance portfolio of Black (1972) and Black, Jensen, and Scholes (1972). We consider a broader class of BAB portfolios because we empirically consider a variety of BAB portfolios within various asset classes that are subsets of all securities (e.g., stocks in a particular size group). Therefore, our construction achieves market neutrality by leveraging (and de-leveraging) the long and short sides instead of adding the market itself as Black, Jensen, and Scholes (1972) do.

$^6$ Garleanu and Pedersen (2011) find a complementary result, studying securities with identical fundamental risk but different margin requirements. They find theoretically and empirically that such assets have similar betas when liquidity is good, but when funding liquidity risk rises the high-margin securities have larger betas, as their high margins make them more funding sensitive. Here, we study securities with different fundamental risk, but the same margin requirements. In this case, higher funding liquidity risk means that betas are compressed toward one.

---

# Page 6

6

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

**Table 1**

Summary statistics: equities.

This table shows summary statistics as of June of each year. The sample includes all common stocks on the Center for Research in Security Prices daily stock files (shrcd equal to 10 or 11) and Xpressfeed Global security files (tcpi equal to zero). Mean ME is the average market value of equity, in billions of US dollars. Means are pooled averages as of June of each year.

<table>
  <thead>
    <tr>
      <th>Country</th>
      <th>Local market index</th>
      <th>Number of stocks, total</th>
      <th>Number of stocks, mean</th>
      <th>Mean ME (firm, billion of US dollars)</th>
      <th>Mean ME (market, billion of US dollars)</th>
      <th>Start year</th>
      <th>End year</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Australia</td><td>MSCI Australia</td><td>3,047</td><td>894</td><td>0.57</td><td>501</td><td>1989</td><td>2012</td></tr>
    <tr><td>Austria</td><td>MSCI Austria</td><td>211</td><td>81</td><td>0.75</td><td>59</td><td>1989</td><td>2012</td></tr>
    <tr><td>Belgium</td><td>MSCI Belgium</td><td>425</td><td>138</td><td>1.79</td><td>240</td><td>1989</td><td>2012</td></tr>
    <tr><td>Canada</td><td>MSCI Canada</td><td>5,703</td><td>1,180</td><td>0.89</td><td>520</td><td>1984</td><td>2012</td></tr>
    <tr><td>Denmark</td><td>MSCI Denmark</td><td>413</td><td>146</td><td>0.83</td><td>119</td><td>1989</td><td>2012</td></tr>
    <tr><td>Finland</td><td>MSCI Finland</td><td>293</td><td>109</td><td>1.39</td><td>143</td><td>1989</td><td>2012</td></tr>
    <tr><td>France</td><td>MSCI France</td><td>1,815</td><td>589</td><td>2.12</td><td>1,222</td><td>1989</td><td>2012</td></tr>
    <tr><td>Germany</td><td>MSCI Germany</td><td>2,165</td><td>724</td><td>2.48</td><td>1,785</td><td>1989</td><td>2012</td></tr>
    <tr><td>Hong Kong</td><td>MSCI Hong Kong</td><td>1,793</td><td>674</td><td>1.22</td><td>799</td><td>1989</td><td>2012</td></tr>
    <tr><td>Italy</td><td>MSCI Italy</td><td>610</td><td>224</td><td>2.12</td><td>470</td><td>1989</td><td>2012</td></tr>
    <tr><td>Japan</td><td>MSCI Japan</td><td>5,009</td><td>2,907</td><td>1.19</td><td>3,488</td><td>1989</td><td>2012</td></tr>
    <tr><td>Netherlands</td><td>MSCI Netherlands</td><td>413</td><td>168</td><td>3.33</td><td>557</td><td>1989</td><td>2012</td></tr>
    <tr><td>New Zealand</td><td>MSCI New Zealand</td><td>318</td><td>97</td><td>0.87</td><td>81</td><td>1989</td><td>2012</td></tr>
    <tr><td>Norway</td><td>MSCI Norway</td><td>661</td><td>164</td><td>0.76</td><td>121</td><td>1989</td><td>2012</td></tr>
    <tr><td>Singapore</td><td>MSCI Singapore</td><td>1,058</td><td>375</td><td>0.63</td><td>240</td><td>1989</td><td>2012</td></tr>
    <tr><td>Spain</td><td>MSCI Spain</td><td>376</td><td>138</td><td>3.00</td><td>398</td><td>1989</td><td>2012</td></tr>
    <tr><td>Sweden</td><td>MSCI Sweden</td><td>1,060</td><td>264</td><td>1.30</td><td>334</td><td>1989</td><td>2012</td></tr>
    <tr><td>Switzerland</td><td>MSCI Switzerland</td><td>566</td><td>210</td><td>3.06</td><td>633</td><td>1989</td><td>2012</td></tr>
    <tr><td>United Kingdom</td><td>MSCI UK</td><td>6,126</td><td>1,766</td><td>1.22</td><td>2,243</td><td>1989</td><td>2012</td></tr>
    <tr><td>United States</td><td>CRSP value-weighted index</td><td>23,538</td><td>3,182</td><td>0.99</td><td>3,215</td><td>1926</td><td>2012</td></tr>
  </tbody>
</table>

period’s security payoffs as

$$
P_{t+1} + \delta_{t+1} = E_t(P_{t+1} + \delta_{t+1}) + b\left(P_{t+1}^M + \delta_{t+1}^M - E_t(P_{t+1}^M + \delta_{t+1}^M)\right) + e
\quad (13)
$$

where $b$ is a vector of market exposures, and $e$ is a vector of noise that is uncorrelated with the market. We have the following natural result for the agents’ positions.

**Proposition 5 (constrained investors hold high betas).** Unconstrained agents hold a portfolio of risky securities that has a beta less than one; constrained agents hold portfolios of risky securities with higher betas. If securities $s$ and $k$ are identical except that $s$ has a larger market exposure than $k$ , $b^s > b^k$ , then any constrained agent $j$ with greater than average Lagrange multiplier, $\psi_t^j > \psi_t$ , holds more shares of $s$ than $k$ . The reverse is true for any agent with $\psi_t^j < \psi_t$ .

We next provide empirical evidence for Propositions 1–5. Beyond matching the data qualitatively, Appendix C illustrates how well a calibrated model can quantitatively match the magnitude of the estimated BAB returns.

## 3. Data and methodology

The data in this study are collected from several sources. The sample of US and international equities has 55,600 stocks covering 20 countries, and the summary statistics for stocks are reported in Table 1. Stock return data are from the union of the Center for Research in Security Prices (CRSP) tape and the Xpressfeed Global database. Our US equity data include all available common stocks on CRSP between January 1926 and March 2012, and betas are computed with respect to the CRSP value-weighted market index. Excess returns are above the US Treasury bill rate. We consider alphas with respect to the market factor and factor returns based on size (SMB), book-to-market (HML), momentum (up minus down, UMD), and (when available) liquidity risk. $^7$

The international equity data include all available common stocks on the Xpressfeed Global daily security file for 19 markets belonging to the MSCI developed universe between January 1989 and March 2012. We assign each stock to its corresponding market based on the location of the primary exchange. Betas are computed with respect to the corresponding MSCI local market index. $^8$

All returns are in US dollars, and excess returns are above the US Treasury bill rate. We compute alphas with respect to the international market and factor returns based on size (SMB), book-to-market (HML), and momentum (UMD) from Asness and Frazzini (2013) and (when available) liquidity risk. $^9$

We also consider a variety of other assets. Table 2 contains the list of instruments and the corresponding ranges of available data. We obtain US Treasury bond data from the CRSP US Treasury Database, using monthly returns (in excess of the one-month Treasury bill) on the

---

$^7$ SMB, HML, and UMD are from Ken French’s data library, and the liquidity risk factor is from Wharton Research Data Service (WRDS).

$^8$ Our results are robust to the choice of benchmark (local versus global). We report these tests in Appendix B.

$^9$ These factors mimic their U.S counterparts and follow Fama and French (1992, 1993, 1996). See Asness and Frazzini (2013) for a detailed description of their construction. The data can be downloaded at http://www.econ.yale.edu/ af227/data_library.htm.

---

# Page 7

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

7

**Table 2**

Summary statistics: other asset classes.

This table reports the securities included in our data sets and the corresponding date range.

<table>
  <thead>
    <tr>
      <th>Asset class</th>
      <th>Instrument</th>
      <th>Frequency</th>
      <th>Start year</th>
      <th>End year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Equity indices</td>
      <td>Australia</td>
      <td>Daily</td>
      <td>1977</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Germany</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Canada</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Spain</td>
      <td>Daily</td>
      <td>1980</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>France</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Hong Kong</td>
      <td>Daily</td>
      <td>1980</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Italy</td>
      <td>Daily</td>
      <td>1978</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Japan</td>
      <td>Daily</td>
      <td>1976</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Netherlands</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Sweden</td>
      <td>Daily</td>
      <td>1980</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Switzerland</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>United Kingdom</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>United States</td>
      <td>Daily</td>
      <td>1965</td>
      <td>2012</td>
    </tr>
    <tr>
      <td>Country bonds</td>
      <td>Australia</td>
      <td>Daily</td>
      <td>1986</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Germany</td>
      <td>Daily</td>
      <td>1980</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Canada</td>
      <td>Daily</td>
      <td>1985</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Japan</td>
      <td>Daily</td>
      <td>1982</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Norway</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Sweden</td>
      <td>Daily</td>
      <td>1987</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Switzerland</td>
      <td>Daily</td>
      <td>1981</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>United Kingdom</td>
      <td>Daily</td>
      <td>1980</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>United States</td>
      <td>Daily</td>
      <td>1965</td>
      <td>2012</td>
    </tr>
    <tr>
      <td>Foreign exchange</td>
      <td>Australia</td>
      <td>Daily</td>
      <td>1977</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Germany</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Canada</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Japan</td>
      <td>Daily</td>
      <td>1976</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Norway</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>New Zealand</td>
      <td>Daily</td>
      <td>1986</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Sweden</td>
      <td>Daily</td>
      <td>1987</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Switzerland</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>United Kingdom</td>
      <td>Daily</td>
      <td>1975</td>
      <td>2012</td>
    </tr>
    <tr>
      <td>US Treasury bonds</td>
      <td>Zero to one year</td>
      <td>Monthly</td>
      <td>1952</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>One to two years</td>
      <td>Monthly</td>
      <td>1952</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Two to three years</td>
      <td>Monthly</td>
      <td>1952</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Three to four years</td>
      <td>Monthly</td>
      <td>1952</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Four to five years</td>
      <td>Monthly</td>
      <td>1952</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Four to ten years</td>
      <td>Monthly</td>
      <td>1952</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>More than ten years</td>
      <td>Monthly</td>
      <td>1952</td>
      <td>2012</td>
    </tr>
    <tr>
      <td>Credit indices</td>
      <td>One to three years</td>
      <td>Monthly</td>
      <td>1976</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Three to five year</td>
      <td>Monthly</td>
      <td>1976</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Five to ten years</td>
      <td>Monthly</td>
      <td>1991</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Seven to ten years</td>
      <td>Monthly</td>
      <td>1988</td>
      <td>2012</td>
    </tr>
    <tr>
      <td>Corporate bonds</td>
      <td>Aaa</td>
      <td>Monthly</td>
      <td>1973</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Aa</td>
      <td>Monthly</td>
      <td>1973</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>A</td>
      <td>Monthly</td>
      <td>1973</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Baa</td>
      <td>Monthly</td>
      <td>1973</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Ba</td>
      <td>Monthly</td>
      <td>1983</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>B</td>
      <td>Monthly</td>
      <td>1983</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Caa</td>
      <td>Monthly</td>
      <td>1983</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Ca-D</td>
      <td>Monthly</td>
      <td>1993</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Distressed</td>
      <td>Monthly</td>
      <td>1986</td>
      <td>2012</td>
    </tr>
    <tr>
      <td>Commodities</td>
      <td>Aluminum</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Brent oil</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Cattle</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Cocoa</td>
      <td>Daily</td>
      <td>1984</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Coffee</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Copper</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Corn</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Cotton</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Crude</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Gasoil</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Gold</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
    <tr>
      <td></td>
      <td>Heat oil</td>
      <td>Daily</td>
      <td>1989</td>
      <td>2012</td>
    </tr>
  </tbody>
</table>

---

# Page 8

8

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

Table 2 (continued)

<table>
  <thead>
    <tr>
      <th>Asset class</th>
      <th>Instrument</th>
      <th>Frequency</th>
      <th>Start year</th>
      <th>End year</th>
    </tr>
  </thead>
  <tbody>
    <tr><td></td><td>Hogs</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Lead</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Nat gas</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Nickel</td><td>Daily</td><td>1984</td><td>2012</td></tr>
    <tr><td></td><td>Platinum</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Silver</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Soymeal</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Soy oil</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Sugar</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Tin</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Unleaded</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Wheat</td><td>Daily</td><td>1989</td><td>2012</td></tr>
    <tr><td></td><td>Zinc</td><td>Daily</td><td>1989</td><td>2012</td></tr>
  </tbody>
</table>

Fama Bond portfolios for maturities ranging from one to ten years between January 1952 and March 2012. Each portfolio return is an equal-weighted average of the unadjusted holding period return for each bond in the portfolio. Only non-callable, non-flower notes and bonds are included in the portfolios. Betas are computed with respect to an equally weighted portfolio of all bonds in the database.

We collect aggregate corporate bond index returns from Barclays Capital’s Bond.Hub database. $^{10}$ Our analysis focuses on the monthly returns (in excess of the one-month Treasury bill) of four aggregate US credit indices with maturity ranging from one to ten years and nine investment-grade and high-yield corporate bond portfolios with credit risk ranging from AAA to Ca-D and Distressed. $^{11}$ The data cover the period between January 1973 and March 2012, although the data availability varies depending on the individual bond series. Betas are computed with respect to an equally weighted portfolio of all bonds in the database.

We also study futures and forwards on country equity indexes, country bond indexes, foreign exchange, and commodities. Return data are drawn from the internal pricing data maintained by AQR Capital Management LLC. The data are collected from a variety of sources and contain daily return on futures, forwards, or swap contracts in excess of the relevant financing rate. The type of contract for each asset depends on availability or the relative liquidity of different instruments. Prior to expiration, positions are rolled over into the next most-liquid contract. The rolling date’s convention differs across contracts and depends on the relative liquidity of different maturities. The data cover the period between January 1963 and March 2012, with varying data availability depending on the asset class. For more details on the computation of returns and data sources, see Moskowitz, Ooi, and Pedersen (2012), Appendix A. For equity indexes, country bonds, and currencies, the betas are computed with respect to a gross domestic product (GDP)-weighted portfolio, and for commodities, the betas are computed

with respect to a diversified portfolio that gives equal risk weight across commodities.

Finally, we use the TED spread as a proxy for time periods when credit constraints are more likely to be binding [as in Garleanu and Pedersen (2011) and others]. The TED spread is defined as the difference between the three-month Eurodollar LIBOR and the three-month US Treasuries rate. Our TED data run from December 1984 to March 2012.

### 3.1. Estimating ex ante betas

We estimate pre-ranking betas from rolling regressions of excess returns on market excess returns. Whenever possible, we use daily data, rather than monthly data, as the accuracy of covariance estimation improves with the sample frequency (Merton, 1980). $^{12}$ Our estimated beta for security $i$ is given by

$$
\hat{\beta}_i^{ts} = \hat{\rho} \frac{\hat{\sigma}_i}{\hat{\sigma}_m},
\quad \text{(14)}
$$

where $\hat{\sigma}_i$ and $\hat{\sigma}_m$ are the estimated volatilities for the stock and the market and $\hat{\rho}$ is their correlation. We estimate volatilities and correlations separately for two reasons. First, we use a one-year rolling standard deviation for volatilities and a five-year horizon for the correlation to account for the fact that correlations appear to move more slowly than volatilities. $^{13}$ Second, we use one-day log returns to estimate volatilities and overlapping three-day log returns, $r_{i,t}^{3d} = \sum_{k=0}^{2} \ln(1 + r_{t+k}^i)$ , for correlation to control for nonsynchronous trading (which affects only correlations). We require at least six months (120 trading days) of non-missing data to estimate volatilities and at least three years (750 trading days) of non-missing return data for correlations. If we have access only to monthly data, we use rolling one and five-year windows and require at least 12 and 36 observations.

Finally, to reduce the influence of outliers, we follow Vasicek (1973) and Elton, Gruber, Brown, and Goetzmann (2003) and shrink the time series estimate of beta ( $\beta_i^{TS}$ )

---

$^{10}$ The data can be downloaded at https://live.barcap.com.

$^{11}$ The distress index was provided to us by Credit Suisse.

$^{12}$ Daily returns are not available for our sample of US Treasury bonds, US corporate bonds, and US credit indices.

$^{13}$ See, for example, De Santis and Gerard (1997).

---

# Page 9

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

9

toward the cross-sectional mean ( $\beta^{XS}$ ):

$$
\hat{\beta}_i = w_i \hat{\beta}_i^{TS} + (1 - w_i) \hat{\beta}^{XS}
\quad \text{(15)}
$$

for simplicity, instead of having asset-specific and time-varying shrinkage factors as in Vasicek (1973), we set $w = 0.6$ and $\beta^{XS} = 1$ for all periods and across all assets. However, our results are very similar either way. $^{14}$

Our choice of the shrinkage factor does not affect how securities are sorted into portfolios because the common shrinkage does not change the ranks of the security betas. However, the amount of shrinkage affects the construction of the BAB portfolios because the estimated betas are used to scale the long and short sides of portfolio as seen in Eq. (9).

To account for the fact that noise in the ex ante betas affects the construction of the BAB factors, our inference is focused on realized abnormal returns so that any mismatch between ex ante and (ex post) realized betas is picked up by the realized loadings in the factor regression. When we regress our portfolios on standard risk factors, the realized factor loadings are not shrunk as above because only the ex ante betas are subject to selection bias. Our results are robust to alternative beta estimation procedures as we report in Appendix B.

We compute betas with respect to a market portfolio, which is either specific to an asset class or the overall world market portfolio of all assets. While our results hold both ways, we focus on betas with respect to asset class-specific market portfolios because these betas are less noisy for several reasons. First, this approach allows us to use daily data over a long time period for most asset classes, as opposed to using the most diversified market portfolio for which we only have monthly data and only over a limited time period. Second, this approach is applicable even if markets are segmented.

As a robustness test, Table B8 in Appendix B reports results when we compute betas with respect to a proxy for a world market portfolio consisting of many asset classes. We use the world market portfolio from Asness, Frazzini, and Pedersen (2012). $^{15}$ The results are consistent with our main tests as the BAB factors earn large and significant abnormal returns in each of the asset classes in our sample.

### 3.2. Constructing betting against beta factors

We construct simple portfolios that are long low-beta securities and that shortsell high-beta securities (BAB factors). To construct each BAB factor, all securities in an asset class are ranked in ascending order on the basis of their estimated beta. The ranked securities are assigned to one of two portfolios: low-beta and high-beta. The low- (high-) beta

---

$^{14}$ The Vasicek (1973) Bayesian shrinkage factor is given by $w_i = 1 - \sigma_{i,TS}^2 / (\sigma_{i,TS}^2 + \sigma_{XS}^2)$ where $\sigma_{i,TS}^2$ is the variance of the estimated beta for security $i$ and $\sigma_{XS}^2$ is the cross-sectional variance of betas. This estimator places more weight on the historical times series estimate when the estimate has a lower variance or when there is large dispersion of betas in the cross section. Pooling across all stocks in our US equity data, the shrinkage factor $w$ has a mean of 0.61.

$^{15}$ See Asness, Frazzini, and Pedersen (2012) for a detailed description of this market portfolio. The market series is monthly and ranges from 1973 to 2009.

portfolio is composed of all stocks with a beta below (above) its asset class median (or country median for international equities). In each portfolio, securities are weighted by the ranked betas (i.e., lower-beta securities have larger weights in the low-beta portfolio and higher-beta securities have larger weights in the high-beta portfolio). The portfolios are rebalanced every calendar month.

More formally, let $z$ be the $n \times 1$ vector of beta ranks $z_i = rank(\beta_{it})$ at portfolio formation, and let $\bar{z} = 1_n z / n$ be the average rank, where $n$ is the number of securities and $1_n$ is an $n \times 1$ vector of ones. The portfolio weights of the low-beta and high-beta portfolios are given by

$$
w_H = k(z - \bar{z})^+
\quad \text{(16)}
$$

$$
w_L = k(z - \bar{z})^-
$$

where $k$ is a normalizing constant $k = 2 / 1_n |z - \bar{z}|$ and $x^+$ and $x^-$ indicate the positive and negative elements of a vector $x$ . By construction, we have $1_n^+ w_H = 1$ and $1_n^+ w_L = 1$ . To construct the BAB factor, both portfolios are rescaled to have a beta of one at portfolio formation. The BAB is the self-financing zero-beta portfolio (8) that is long the low-beta portfolio and that shortsells the high-beta portfolio.

$$
r_{t+1}^{BAB} = \frac{1}{\beta_t^L} (r_{t+1}^L - r^f) - \frac{1}{\beta_t^H} (r_{t+1}^H - r^f),
\quad \text{(17)}
$$

where $r_{t+1}^L = r_{t+1}^+ w_L$ , $r_{t+1}^H = r_{t+1}^+ w_H$ , $\beta_t^L = \beta_t^+ w_L$ , and $\beta_t^H = \beta_t^+ w_H$ .

For example, on average, the US stock BAB factor is long $1.4 of low-beta stocks (financed by shortselling $ 1.4 of risk-free securities) and shortsells $0.7 of high-beta stocks (with $ 0.7 earning the risk-free rate).

### 3.3. Data used to test the theory’s portfolio predictions

We collect mutual fund holdings from the union of the CRSP Mutual Fund Database and Thomson Financial CDA/Spectrum holdings database, which includes all registered domestic mutual funds filing with the Securities and Exchange Commission. The holdings data run from March 1980 to March 2012. We focus our analysis on open-end, actively managed, domestic equity mutual funds. Our sample selection procedure follows that of Kacperczyk, Sialm, and Zheng (2008), and we refer to their Appendix for details about the screens that were used and summary statistics of the data.

Our individual investors’ holdings data are collected from a nationwide discount brokerage house and contain trades made by about 78 thousand households in the period from January 1991 to November 1996. This data set has been used extensively in the existing literature on individual investors. For a detailed description of the brokerage data set, see Barber and Odean (2000).

Our sample of buyouts is drawn from the mergers and acquisitions and corporate events database maintained by AQR/CNH Partners. $^{16}$ The data contain various items, including initial and subsequent announcement dates, and (if applicable) completion or termination date for all takeover deals in which the target is a US publicly traded

---

$^{16}$ We would like to thank Mark Mitchell for providing us with these data.

---

# Page 10

10

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

firm and where the acquirer is a private company. For some (but not all) deals, the acquirer descriptor also contains information on whether the deal is a leveraged buyout (LBO) or management buyout (MBO). The data run from January 1963 to March 2012.

Finally, we download holdings data for Berkshire Hathaway from Thomson-Reuters Financial Institutional (13f) Holding Database. The data run from March 1980 to March 2012.

## 4. Betting against beta in each asset class

We now test how the required return varies in the cross-section of beta-sorted securities (Proposition 1) and the hypothesis that the BAB factors have positive average returns (Proposition 2). As an overview of these results, the alphas of all the beta-sorted portfolios considered in this paper are plotted in Fig. 1. We see that declining alphas across beta-sorted portfolios are general phenomena across asset classes. (Fig. B1 in Appendix B plots the Sharpe ratios of beta-sorted portfolios and also shows a consistently declining pattern.)

Fig. 2 plots the annualized Sharpe ratios of the BAB portfolios in the various asset classes. All the BAB portfolios deliver positive returns, except for a small insignificantly negative return in Austrian stocks. The BAB portfolios based on large numbers of securities (US stocks, international stocks, Treasuries, credits) deliver high risk-adjusted returns relative to the standard risk factors considered in the literature.

### 4.1. Stocks

Table 3 reports our tests for US stocks. We consider ten beta-sorted portfolios and report their average returns, alphas, market betas, volatilities, and Sharpe ratios. The average returns of the different beta portfolios are similar, which is the well-known relatively flat security market line. Hence, consistent with Proposition 1 and with Black (1972), the alphas decline almost monotonically from the low-beta to high-beta portfolios. The alphas decline when estimated relative to a one-, three-, four-, and five-factor model. Moreover, Sharpe ratios decline monotonically from low-beta to high-beta portfolios.

The rightmost column of Table 3 reports returns of the betting against beta factor, i.e., a portfolio that is long leveraged low-beta stocks and that shortsells de-leveraged high-beta stocks, thus maintaining a beta-neutral portfolio. Consistent with Proposition 2, the BAB factor delivers a high average return and a high alpha. Specifically, the BAB factor has Fama and French (1993) abnormal returns of 0.73% per month (t-statistic=7.39). Further adjusting returns for the Carhart (1997) momentum factor, the BAB portfolio earns abnormal returns of 0.55% per month (t-statistic=5.59). Last, we adjust returns using a five-factor model by adding the traded liquidity factor by Pastor and Stambaugh (2003), yielding an abnormal BAB return of 0.55% per month (t-statistic=4.09, which is lower in part because the liquidity factor is available during only half of our sample). While the alpha of the long-short portfolio is consistent across regressions, the

choice of risk adjustment influences the relative alpha contribution of the long and short sides of the portfolio.

Our results for US equities show how the security market line has continued to be too flat for another four decades after Black, Jensen, and Scholes (1972). Further, our results extend internationally. We consider beta-sorted portfolios for international equities and later turn to altogether different asset classes. We use all 19 MSCI developed countries except the US (to keep the results separate from the US results above), and we do this in two ways: We consider international portfolios in which all international stocks are pooled together (Table 4), and we consider results separately for each country (Table 5). The international portfolio is country-neutral, i.e., the low-(high-) beta portfolio is composed of all stocks with a beta below (above) its country median.$^{17}$

The results for our pooled sample of international equities in Table 4 mimic the US results. The alpha and Sharpe ratios of the beta-sorted portfolios decline (although not perfectly monotonically) with the betas, and the BAB factor earns risk-adjusted returns between 0.28% and 0.64% per month depending on the choice of risk adjustment, with t-statistics ranging from 2.09 to 4.81.

Table 5 shows the performance of the BAB factor within each individual country. The BAB delivers positive Sharpe ratios in 18 of the 19 MSCI developed countries and positive four-factor alphas in 13 out of 19, displaying a strikingly consistent pattern across equity markets. The BAB returns are statistically significantly positive in six countries, while none of the negative alphas is significant. Of course, the small number of stocks in our sample in many of the countries makes it difficult to reject the null hypothesis of zero return in each individual country.

Table B1 in Appendix B reports factor loadings. On average, the US BAB factor goes long $1.40 ($1.40 for international BAB) and shortsells $0.70 ($0.89 for international BAB). The larger long investment is meant to make the BAB factor market-neutral because the stocks that are held long have lower betas. The BAB factor’s realized market loading is not exactly zero, reflecting the fact that our ex ante betas are measured with noise. The other factor loadings indicate that, relative to high-beta stocks, low-beta stocks are likely to be larger, have higher book-to-market ratios, and have higher return over the prior 12 months, although none of the loadings can explain the large and significant abnormal returns. The BAB portfolio’s positive HML loading is natural since our theory predicts that low-beta stocks are cheap and high-beta stocks are expensive.

Appendix B reports further tests and additional robustness checks. In Table B2, we report results using different window lengths to estimate betas and different benchmarks (local, global). We split the sample by size (Table B3) and time periods (Table B4), we control for idiosyncratic volatility (Table B5), and we report results for alternative

$^{17}$ We keep the international portfolio country neutral because we report the result of betting against beta across equity indices BAB separately in Table 8.

---

# Page 11

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

11

![image](image_1.png)

Fig. 1. Alphas of beta-sorted portfolios. This figure shows monthly alphas. The test assets are beta-sorted portfolios. At the beginning of each calendar month, securities are ranked in ascending order on the basis of their estimated beta at the end of the previous month. The ranked securities are assigned to beta-sorted portfolios. This figure plots alphas from low beta (left) to high beta (right). Alpha is the intercept in a regression of monthly excess return. For equity portfolios, the explanatory variables are the monthly returns from Fama and French (1993), Asness and Frazzini (2013), and Carhart (1997) portfolios. For all other portfolios, the explanatory variables are the monthly returns of the market factor. Alphas are in monthly percent.

definitions of the risk-free rate (Table B6). Finally, in Table B7 and Fig. B2 we report an out-of-sample test. We collect pricing data from DataStream and for each country in Table 1 we compute a BAB portfolio over sample period not covered by the Xpressfeed Global database.$^{18}$ All of the results are consistent: Equity portfolios that bet against betas earn significant risk-adjusted returns.

## 4.2. Treasury bonds

Table 6 reports results for US Treasury bonds. As before, we report average excess returns of bond portfolios formed by sorting on beta in the previous month. In the cross section of Treasury bonds, ranking on betas with

$^{18}$ DataStream international pricing data start in 1969, and Xpressfeed Global coverage starts in 1984.

respect to an aggregate Treasury bond index is empirically equivalent to ranking on duration or maturity. Therefore, in Table 6, one can think of the term “beta,” “duration,” or “maturity” in an interchangeable fashion. The right-most column reports returns of the BAB factor. Abnormal returns are computed with respect to a one-factor model in which alpha is the intercept in a regression of monthly excess return on an equally weighted Treasury bond excess market return.

The results show that the phenomenon of a flatter security market line than predicted by the standard CAPM is not limited to the cross section of stock returns. Consistent with Proposition 1, the alphas decline monotonically with beta. Likewise, Sharpe ratios decline monotonically from 0.73 for low-beta (short-maturity) bonds to 0.31 for high-beta (long-maturity) bonds. Furthermore, the bond BAB portfolio delivers abnormal returns of 0.17% per month ($t$-statistic=6.26) with a large annual Sharpe ratio of 0.81.

---

# Page 12

12

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

![image](image_1.png)

Fig. 2. Betting against beta (BAB) Sharpe ratios by asset class. This figures shows annualized Sharpe ratios of BAB factors across asset classes. To construct the BAB factor, all securities are assigned to one of two portfolios: low beta and high beta. Securities are weighted by the ranked betas and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of one at portfolio formation. The BAB factor is a self-financing portfolio that is long the low-beta portfolio and shorts the high-beta portfolio. Sharpe ratios are annualized.

Because the idea that funding constraints have a significant effect on the term structure of interest could be surprising, let us illustrate the economic mechanism that could be at work. Suppose an agent, e.g., a pension fund, has $1 to allocate to Treasuries with a target excess return of 2.9% per year. One way to achieve this return target is to invest $ 1 in a portfolio of Treasuries with maturity above ten years as seen in Table 6, P7. If the agent invests in one-year Treasuries (P1) instead, then he would need to invest $11 if all maturities had the same Sharpe ratio. This higher leverage is needed because the long-term Treasuries are 11 times more volatile than the short-term Treasuries. Hence, the agent would need to borrow an additional $ 10 to lever his investment in one-year bonds. If the agent has leverage limits (or prefers lower leverage), then he would strictly prefer the ten-year Treasuries in this case.

According to our theory, the one-year Treasuries therefore must offer higher returns and higher Sharpe ratios, flattening the security market line for bonds. Empirically, short-term Treasuries do offer higher risk-adjusted returns so the return target can be achieved by investing about $5 in one-year bonds. While a constrained investor could still prefer an un-leveraged investment in ten-year bonds, unconstrained investors now prefer the leveraged low-beta bonds, and the market can clear.

While the severity of leverage constraints varies across market participants, it appears plausible that a five-to-one leverage (on this part of the portfolio) makes a difference for some large investors such as pension funds.

## 4.3. Credit

We next test our model using several credit portfolios and report results in Table 7. In Panel A, columns 1 to 5, the test assets are monthly excess returns of corporate bond indexes by maturity. We see that the credit BAB portfolio delivers abnormal returns of 0.11% per month (t-statistic = 5.14) with a large annual Sharpe ratio of 0.82. Furthermore, alphas and Sharpe ratios decline monotonically.

In columns 6 to 10, we attempt to isolate the credit component by hedging away the interest rate risk. Given the results on Treasuries in Table 6, we are interested in testing a pure credit version of the BAB portfolio. Each calendar month, we run one-year rolling regressions of excess bond returns on the excess return on Barclay’s US government bond index. We construct test assets by going long the corporate bond index and hedging this position by shortselling the appropriate amount of the government bond index: $ r_t^{CDS} - r_t^f = (r_t - r_t^f) - \hat{\theta}_{t-1}(r_t^{USGOV} - r_t^f) $, where $ \hat{\theta}_{t-1}$ is the slope coefficient estimated in an expanding

---

# Page 13

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

13

**Table 3**

US equities: returns, 1926–2012.

This table shows beta-sorted calendar-time portfolio returns. At the beginning of each calendar month, stocks are ranked in ascending order on the basis of their estimated beta at the end of the previous month. The ranked stocks are assigned to one of ten deciles portfolios based on NYSE breakpoints. All stocks are equally weighted within a given portfolio, and the portfolios are rebalanced every month to maintain equal weights. The right-most column reports returns of the zero-beta betting against beta (BAB) factor. To construct the BAB factor, all stocks are assigned to one of two portfolios: low beta and high beta. Stocks are weighted by the ranked betas (lower beta security have larger weight in the low-beta portfolio and higher beta securities have larger weights in the high-beta portfolio), and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of one at portfolio formation. The betting against beta factor is a self-financing portfolio that is long the low-beta portfolio and short the high-beta portfolio. This table includes all available common stocks on the Center for Research in Security Prices database between January 1926 and March 2012. Alpha is the intercept in a regression of monthly excess return. The explanatory variables are the monthly returns from Fama and French (1993) mimicking portfolios, Carhart (1997) momentum factor and Pastor and Stambaugh (2003) liquidity factor. CAPM = Capital Asset Pricing Model. Regarding the five-factor alphas the Pastor and Stambaugh (2003) liquidity factor is available only between 1968 and 2011. Returns and alphas are in monthly percent, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. Beta (ex ante) is the average estimated beta at portfolio formation. Beta (realized) is the realized loading on the market portfolio. Volatilities and Sharpe ratios are annualized.

<table>
  <thead>
    <tr>
      <th>Portfolio</th>
      <th>P1<br>(low beta)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10<br>(high beta)</th>
      <th>BAB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess return</td>
      <td>0.91<br>(6.37)</td>
      <td>0.98<br>(5.73)</td>
      <td>1.00<br>(5.16)</td>
      <td>1.03<br>(4.88)</td>
      <td>1.05<br>(4.49)</td>
      <td>1.10<br>(4.37)</td>
      <td>1.05<br>(3.84)</td>
      <td>1.08<br>(3.74)</td>
      <td>1.06<br>(3.27)</td>
      <td>0.97<br>(2.55)</td>
      <td>0.70<br>(7.12)</td>
    </tr>
    <tr>
      <td>CAPM alpha</td>
      <td>0.52<br>(6.30)</td>
      <td>0.48<br>(5.99)</td>
      <td>0.42<br>(4.91)</td>
      <td>0.39<br>(4.43)</td>
      <td>0.34<br>(3.51)</td>
      <td>0.34<br>(3.20)</td>
      <td>0.22<br>(1.94)</td>
      <td>0.21<br>(1.72)</td>
      <td>0.10<br>(0.67)</td>
      <td>−0.10<br>(−0.48)</td>
      <td>0.73<br>(7.44)</td>
    </tr>
    <tr>
      <td>Three-factor alpha</td>
      <td>0.40<br>(6.25)</td>
      <td>0.35<br>(5.95)</td>
      <td>0.26<br>(4.76)</td>
      <td>0.21<br>(4.13)</td>
      <td>0.13<br>(2.49)</td>
      <td>0.11<br>(1.94)</td>
      <td>−0.03<br>(−0.59)</td>
      <td>−0.06<br>(−1.02)</td>
      <td>−0.22<br>(−2.81)</td>
      <td>−0.49<br>(−3.68)</td>
      <td>0.73<br>(7.39)</td>
    </tr>
    <tr>
      <td>Four-factor alpha</td>
      <td>0.40<br>(6.05)</td>
      <td>0.37<br>(6.13)</td>
      <td>0.30<br>(5.36)</td>
      <td>0.25<br>(4.92)</td>
      <td>0.18<br>(3.27)</td>
      <td>0.20<br>(3.63)</td>
      <td>0.09<br>(1.63)</td>
      <td>0.11<br>(1.94)</td>
      <td>0.01<br>(0.12)</td>
      <td>−0.13<br>(−1.01)</td>
      <td>0.55<br>(5.59)</td>
    </tr>
    <tr>
      <td>Five-factor alpha</td>
      <td>0.37<br>(4.54)</td>
      <td>0.37<br>(4.66)</td>
      <td>0.33<br>(4.50)</td>
      <td>0.30<br>(4.40)</td>
      <td>0.17<br>(2.44)</td>
      <td>0.20<br>(2.71)</td>
      <td>0.11<br>(1.40)</td>
      <td>0.14<br>(1.65)</td>
      <td>0.02<br>(0.21)</td>
      <td>0.00<br>(−0.01)</td>
      <td>0.55<br>(4.09)</td>
    </tr>
    <tr>
      <td>Beta (ex ante)</td>
      <td>0.64</td>
      <td>0.79</td>
      <td>0.88</td>
      <td>0.97</td>
      <td>1.05</td>
      <td>1.12</td>
      <td>1.21</td>
      <td>1.31</td>
      <td>1.44</td>
      <td>1.70</td>
      <td>0.00</td>
    </tr>
    <tr>
      <td>Beta (realized)</td>
      <td>0.67</td>
      <td>0.87</td>
      <td>1.00</td>
      <td>1.10</td>
      <td>1.22</td>
      <td>1.32</td>
      <td>1.42</td>
      <td>1.51</td>
      <td>1.66</td>
      <td>1.85</td>
      <td>−0.06</td>
    </tr>
    <tr>
      <td>Volatility</td>
      <td>15.70</td>
      <td>18.70</td>
      <td>21.11</td>
      <td>23.10</td>
      <td>25.56</td>
      <td>27.58</td>
      <td>29.81</td>
      <td>31.58</td>
      <td>35.52</td>
      <td>41.68</td>
      <td>10.75</td>
    </tr>
    <tr>
      <td>Sharpe ratio</td>
      <td>0.70</td>
      <td>0.63</td>
      <td>0.57</td>
      <td>0.54</td>
      <td>0.49</td>
      <td>0.48</td>
      <td>0.42</td>
      <td>0.41</td>
      <td>0.36</td>
      <td>0.28</td>
      <td>0.78</td>
    </tr>
  </tbody>
</table>

**Table 4**

International equities: returns, 1984–2012.

This table shows beta-sorted calendar-time portfolio returns. At the beginning of each calendar month, stocks are ranked in ascending order on the basis of their estimated beta at the end of the previous month. The ranked stocks are assigned to one of ten deciles portfolios. All stocks are equally weighted within a given portfolio, and the portfolios are rebalanced every month to maintain equal weights. The rightmost column reports returns of the zero-beta betting against beta (BAB) factor. To construct the BAB factor, all stocks are assigned to one of two portfolios: low beta and high beta. The low- (high-) beta portfolio is composed of all stocks with a beta below (above) its country median. Stocks are weighted by the ranked betas (lower beta security have larger weight in the low-beta portfolio and higher beta securities have larger weights in the high-beta portfolio), and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of one at portfolio formation. The betting against beta factor is a self-financing portfolio that is long the low-beta portfolio and short the high-beta portfolio. This table includes all available common stocks on the Xpressfeed Global database for the 19 markets listed in Table 1. The sample period runs from January 1984 to March 2012. Alpha is the intercept in a regression of monthly excess return. The explanatory variables are the monthly returns of Asness and Frazzini (2013) mimicking portfolios and Pastor and Stambaugh (2003) liquidity factor. CAPM = Capital Asset Pricing Model. Regarding the five-factor alphas the Pastor and Stambaugh (2003) liquidity factor is available only between 1968 and 2011. Returns are in US dollars and do not include any currency hedging. Returns and alphas are in monthly percent, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. Beta (ex-ante) is the average estimated beta at portfolio formation. Beta (realized) is the realized loading on the market portfolio. Volatilities and Sharpe ratios are annualized.

<table>
  <thead>
    <tr>
      <th>Portfolio</th>
      <th>P1<br>(low beta)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7</th>
      <th>P8</th>
      <th>P9</th>
      <th>P10<br>(high beta)</th>
      <th>BAB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess return</td>
      <td>0.63<br>(2.48)</td>
      <td>0.67<br>(2.44)</td>
      <td>0.69<br>(2.39)</td>
      <td>0.58<br>(1.96)</td>
      <td>0.67<br>(2.19)</td>
      <td>0.63<br>(1.93)</td>
      <td>0.54<br>(1.57)</td>
      <td>0.59<br>(1.58)</td>
      <td>0.44<br>(1.10)</td>
      <td>0.30<br>(0.66)</td>
      <td>0.64<br>(4.66)</td>
    </tr>
    <tr>
      <td>CAPM alpha</td>
      <td>0.45<br>(2.91)</td>
      <td>0.47<br>(3.03)</td>
      <td>0.48<br>(2.96)</td>
      <td>0.36<br>(2.38)</td>
      <td>0.44<br>(2.86)</td>
      <td>0.39<br>(2.26)</td>
      <td>0.28<br>(1.60)</td>
      <td>0.32<br>(1.55)</td>
      <td>0.15<br>(0.67)</td>
      <td>0.00<br>(−0.01)</td>
      <td>0.64<br>(4.68)</td>
    </tr>
    <tr>
      <td>Three-factor alpha</td>
      <td>0.28<br>(2.19)</td>
      <td>0.30<br>(2.22)</td>
      <td>0.29<br>(2.15)</td>
      <td>0.16<br>(1.29)</td>
      <td>0.22<br>(1.71)</td>
      <td>0.11<br>(0.78)</td>
      <td>0.01<br>(0.06)</td>
      <td>−0.03<br>(−0.17)</td>
      <td>−0.23<br>(−1.20)</td>
      <td>−0.50<br>(−1.94)</td>
      <td>0.65<br>(4.81)</td>
    </tr>
    <tr>
      <td>Four-factor alpha</td>
      <td>0.20<br>(1.42)</td>
      <td>0.24<br>(1.64)</td>
      <td>0.20<br>(1.39)</td>
      <td>0.10<br>(0.74)</td>
      <td>0.19<br>(1.36)</td>
      <td>0.08<br>(0.53)</td>
      <td>0.04<br>(0.27)</td>
      <td>0.06<br>(0.35)</td>
      <td>−0.16<br>(−0.79)</td>
      <td>−0.16<br>(−0.59)</td>
      <td>0.30<br>(2.20)</td>
    </tr>
    <tr>
      <td>Five-factor alpha</td>
      <td>0.19<br>(1.38)</td>
      <td>0.23<br>(1.59)</td>
      <td>0.19<br>(1.30)</td>
      <td>0.09<br>(0.65)</td>
      <td>0.20<br>(1.40)</td>
      <td>0.07<br>(0.42)</td>
      <td>0.05<br>(0.33)</td>
      <td>0.05<br>(0.30)</td>
      <td>−0.19<br>(−0.92)</td>
      <td>−0.18<br>(−0.65)</td>
      <td>0.28<br>(2.09)</td>
    </tr>
    <tr>
      <td>Beta (ex ante)</td>
      <td>0.61</td>
      <td>0.70</td>
      <td>0.77</td>
      <td>0.83</td>
      <td>0.88</td>
      <td>0.93</td>
      <td>0.99</td>
      <td>1.06</td>
      <td>1.15</td>
      <td>1.35</td>
      <td>0.00</td>
    </tr>
    <tr>
      <td>Beta (realized)</td>
      <td>0.66</td>
      <td>0.75</td>
      <td>0.78</td>
      <td>0.85</td>
      <td>0.87</td>
      <td>0.92</td>
      <td>0.98</td>
      <td>1.03</td>
      <td>1.0

---

# Page 14

14

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

**Table 5**

International equities: returns by country, 1984–2012.

This table shows calendar-time portfolio returns. At the beginning of each calendar month, all stocks are assigned to one of two portfolios: low beta and high beta. The low- (high-) beta portfolio is composed of all stocks with a beta below (above) its country median. Stocks are weighted by the ranked betas, and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of one at portfolio formation. The zero-beta betting against beta (BAB) factor is a self-financing portfolio that is long the low-beta portfolio and short the high-beta portfolio. This table includes all available common stocks on the Xpressfeed Global database for the 19 markets listed in Table 1. The sample period runs from January 1984 to March 2012. Alpha is the intercept in a regression of monthly excess return. The explanatory variables are the monthly returns of Asness and Frazzini (2013) mimicking portfolios. Returns are in US dollars and do not include any currency hedging. Returns and alphas are in monthly percent, and 5% statistical significance is indicated in bold. $Short (Long) is the average dollar value of the short (long) position. Volatilities and Sharpe ratios are annualized.

<table>
  <thead>
    <tr>
      <th>Country</th>
      <th>Excess return</th>
      <th>t-Statistics Excess return</th>
      <th>Four-factor alpha</th>
      <th>t-Statistics alpha</th>
      <th>$Short</th>
      <th>$Long</th>
      <th>Volatility</th>
      <th>Sharpe ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Australia</td><td>0.11</td><td>0.36</td><td>0.03</td><td>0.10</td><td>0.80</td><td>1.26</td><td>16.7</td><td>0.08</td></tr>
    <tr><td>Austria</td><td>−0.03</td><td>−0.09</td><td>−0.28</td><td>−0.72</td><td>0.90</td><td>1.44</td><td>19.9</td><td>−0.02</td></tr>
    <tr><td>Belgium</td><td>0.71</td><td>2.39</td><td>0.72</td><td>2.28</td><td>0.94</td><td>1.46</td><td>16.9</td><td>0.51</td></tr>
    <tr><td>Canada</td><td>1.23</td><td>5.17</td><td>0.67</td><td>2.71</td><td>0.85</td><td>1.45</td><td>14.1</td><td>1.05</td></tr>
    <tr><td>Switzerland</td><td>0.75</td><td>2.91</td><td>0.54</td><td>2.07</td><td>0.93</td><td>1.47</td><td>14.6</td><td>0.61</td></tr>
    <tr><td>Germany</td><td>0.40</td><td>1.30</td><td>−0.07</td><td>−0.22</td><td>0.94</td><td>1.58</td><td>17.3</td><td>0.27</td></tr>
    <tr><td>Denmark</td><td>0.41</td><td>1.47</td><td>−0.02</td><td>−0.07</td><td>0.91</td><td>1.40</td><td>15.7</td><td>0.31</td></tr>
    <tr><td>Spain</td><td>0.59</td><td>2.12</td><td>0.23</td><td>0.80</td><td>0.92</td><td>1.44</td><td>15.6</td><td>0.45</td></tr>
    <tr><td>Finland</td><td>0.65</td><td>1.51</td><td>−0.10</td><td>−0.22</td><td>1.08</td><td>1.64</td><td>24.0</td><td>0.33</td></tr>
    <tr><td>France</td><td>0.26</td><td>0.63</td><td>−0.37</td><td>−0.82</td><td>0.92</td><td>1.57</td><td>23.7</td><td>0.13</td></tr>
    <tr><td>United Kingdom</td><td>0.49</td><td>1.99</td><td>−0.01</td><td>−0.05</td><td>0.91</td><td>1.53</td><td>13.9</td><td>0.42</td></tr>
    <tr><td>Hong Kong</td><td>0.85</td><td>2.50</td><td>1.01</td><td>2.79</td><td>0.83</td><td>1.38</td><td>19.1</td><td>0.54</td></tr>
    <tr><td>Italy</td><td>0.29</td><td>1.41</td><td>0.04</td><td>0.17</td><td>0.91</td><td>1.35</td><td>11.8</td><td>0.30</td></tr>
    <tr><td>Japan</td><td>0.21</td><td>0.90</td><td>0.01</td><td>0.06</td><td>0.87</td><td>1.39</td><td>13.3</td><td>0.19</td></tr>
    <tr><td>Netherlands</td><td>0.98</td><td>3.62</td><td>0.79</td><td>2.75</td><td>0.91</td><td>1.45</td><td>15.4</td><td>0.77</td></tr>
    <tr><td>Norway</td><td>0.44</td><td>1.15</td><td>0.34</td><td>0.81</td><td>0.85</td><td>1.33</td><td>21.3</td><td>0.25</td></tr>
    <tr><td>New Zealand</td><td>0.74</td><td>2.28</td><td>0.62</td><td>1.72</td><td>0.94</td><td>1.36</td><td>18.1</td><td>0.49</td></tr>
    <tr><td>Singapore</td><td>0.66</td><td>3.37</td><td>0.52</td><td>2.36</td><td>0.79</td><td>1.24</td><td>11.0</td><td>0.72</td></tr>
    <tr><td>Sweden</td><td>0.77</td><td>2.29</td><td>0.22</td><td>0.64</td><td>0.89</td><td>1.34</td><td>19.0</td><td>0.48</td></tr>
  </tbody>
</table>

**Table 6**

US Treasury bonds: returns, 1952–2012.

This table shows calendar-time portfolio returns. The test assets are the Center for Research in Security Prices Treasury Fama bond portfolios. Only non callable, non flower notes and bonds are included in the portfolios. The portfolio returns are an equal-weighted average of the unadjusted holding period return for each bond in the portfolios in excess of the risk-free rate. To construct the zero-beta betting against beta (BAB) factor, all bonds are assigned to one of two portfolios: low beta and high beta. Bonds are weighted by the ranked betas (lower beta bonds have larger weight in the low-beta portfolio and higher beta bonds have larger weights in the high-beta portfolio) and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of one at portfolio formation. The BAB factor is a self-financing portfolio that is long the low-beta portfolio and shorts the high-beta portfolio. Alpha is the intercept in a regression of monthly excess return. The explanatory variable is the monthly return of an equally weighted bond market portfolio. The sample period runs from January 1952 to March 2012. Returns and alphas are in monthly percent, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. Volatilities and Sharpe ratios are annualized. For P7, returns are missing from August 1962 to December 1971.

<table>
  <thead>
    <tr>
      <th>Portfolio</th>
      <th>P1 (low beta)</th>
      <th>P2</th>
      <th>P3</th>
      <th>P4</th>
      <th>P5</th>
      <th>P6</th>
      <th>P7 (high beta)</th>
      <th>BAB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Maturity (months)</td>
      <td>one to 12</td>
      <td>13–24</td>
      <td>25–36</td>
      <td>37–48</td>
      <td>49–60</td>
      <td>61–120</td>
      <td>&gt; 120</td>
      <td></td>
    </tr>
    <tr>
      <td>Excess return</td>
      <td>0.05</td>
      <td>0.09</td>
      <td>0.11</td>
      <td>0.13</td>
      <td>0.13</td>
      <td>0.16</td>
      <td>0.24</td>
      <td>0.17</td>
    </tr>
    <tr>
      <td></td>
      <td>(5.66)</td>
      <td>(3.91)</td>
      <td>(3.37)</td>
      <td>(3.09)</td>
      <td>(2.62)</td>
      <td>(2.52)</td>
      <td>(2.20)</td>
      <td>(6.26)</td>
    </tr>
    <tr>
      <td>Alpha</td>
      <td>0.03</td>
      <td>0.03</td>
      <td>0.02</td>
      <td>0.01</td>
      <td>−0.01</td>
      <td>−0.02</td>
      <td>−0.07</td>
      <td>0.16</td>
    </tr>
    <tr>
      <td></td>
      <td>(5.50)</td>
      <td>(3.00)</td>
      <td>(1.87)</td>
      <td>(0.99)</td>
      <td>(−1.35)</td>
      <td>(−2.28)</td>
      <td>(−1.85)</td>
      <td>(6.18)</td>
    </tr>
    <tr>
      <td>Beta (ex ante)</td>
      <td>0.14</td>
      <td>0.45</td>
      <td>0.74</td>
      <td>0.98</td>
      <td>1.21</td>
      <td>1.44</td>
      <td>2.24</td>
      <td>0.00</td>
    </tr>
    <tr>
      <td>Beta (realized)</td>
      <td>0.16</td>
      <td>0.48</td>
      <td>0.76</td>
      <td>0.98</td>
      <td>1.17</td>
      <td>1.44</td>
      <td>2.10</td>
      <td>0.01</td>
    </tr>
    <tr>
      <td>Volatility</td>
      <td>0.81</td>
      <td>2.07</td>
      <td>3.18</td>
      <td>3.99</td>
      <td>4.72</td>
      <td>5.80</td>
      <td>9.26</td>
      <td>2.43</td>
    </tr>
    <tr>
      <td>Sharpe ratio</td>
      <td>0.73</td>
      <td>0.50</td>
      <td>0.43</td>
      <td>0.40</td>
      <td>0.34</td>
      <td>0.32</td>
      <td>0.31</td>
      <td>0.81</td>
    </tr>
  </tbody>
</table>

returns are computed with respect to a two-factor model in which alpha is the intercept in a regression of monthly excess return on the equally weighted average pseudo-CDS excess return and the monthly return on the Treasury BAB factor. The addition of the Treasury BAB factor on the right-hand side is an extra check to test a pure credit version of the BAB portfolio.

The results in Panel A of Table 7 columns 6 to 10 tell the same story as columns 1 to 5: The BAB portfolio delivers significant abnormal returns of 0.17% per month (t-statistics=4.44) and Sharpe ratios decline monotonically from low-beta to high-beta assets.

Last, in Panel B of Table 7, we report results in which the test assets are credit indexes sorted by rating, ranging from AAA to Ca-D and Distressed. Consistent with all our previous results, we find large abnormal returns of the BAB portfolios (0.57% per month with a t-statistics=3.72) and declining alphas and Sharpe ratios across beta-sorted portfolios.

---

# Page 15

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

15

**Table 7**

US credit: returns, 1973–2012.

This table shows calendar-time portfolio returns. Panel A shows results for US credit indices by maturity. The test assets are monthly returns on corporate bond indices with maturity ranging from one to ten years, in excess of the risk-free rate. The sample period runs from January 1976–March 2012. Unhedged indicates excess returns and Hedged indicates excess returns after hedging the index’s interest rate exposure. To construct hedged excess returns, each calendar month we run one-year rolling regressions of excess bond returns on the excess return on Barclay’s US government bond index. We construct test assets by going long the corporate bond index and hedging this position by shorting the appropriate amount of the government bond index. We compute market excess returns by taking an equal weighted average of the hedged excess returns. Panel B shows results for US corporate bond index returns by rating. The sample period runs from January 1973 to March 2012. To construct the zero-beta betting against beta (BAB) factor, all bonds are assigned to one of two portfolios: low beta and high beta. Bonds are weighted by the ranked betas (lower beta security have larger weight in the low-beta portfolio and higher beta securities have larger weights in the high-beta portfolio) and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of 1 at portfolio formation. The zero-beta BAB factor is a self-financing portfolio that is long the low-beta portfolio and short the high-beta portfolio. Alpha is the intercept in a regression of monthly excess return. The explanatory variable is the monthly excess return of the corresponding market portfolio and, for the hedged portfolios in Panel A, the Treasury BAB factor. Distressed in Panel B indicates the Credit Suisse First Boston distressed index. Returns and alphas are in monthly percent, $t$-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. Volatilities and Sharpe ratios are annualized.

*Panel A: Credit indices, 1976–2012*

<table>
  <thead>
    <tr>
      <th rowspan="2">Portfolios</th>
      <th colspan="5">Unhedged</th>
      <th colspan="5">Hedged</th>
    </tr>
    <tr>
      <th>One to<br>three years</th>
      <th>Three to<br>five years</th>
      <th>Five to<br>ten years</th>
      <th>Seven to<br>ten years</th>
      <th>BAB</th>
      <th>One to<br>three years</th>
      <th>Three to<br>five years</th>
      <th>Five to<br>ten years</th>
      <th>Seven to<br>ten years</th>
      <th>BAB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess return</td>
      <td>0.18<br>(4.97)</td>
      <td>0.22<br>(4.35)</td>
      <td>0.36<br>(3.35)</td>
      <td>0.36<br>(3.51)</td>
      <td>0.10<br>(4.85)</td>
      <td>0.11<br>(3.39)</td>
      <td>0.10<br>(2.56)</td>
      <td>0.11<br>(1.55)</td>
      <td>0.10<br>(1.34)</td>
      <td>0.16<br>(4.35)</td>
    </tr>
    <tr>
      <td>Alpha</td>
      <td>0.03<br>(2.49)</td>
      <td>0.01<br>(0.69)</td>
      <td>−0.04<br>(−3.80)</td>
      <td>−0.07<br>(−4.28)</td>
      <td>0.11<br>(5.14)</td>
      <td>0.05<br>(3.89)</td>
      <td>0.03<br>(2.43)</td>
      <td>−0.03<br>(−3.22)</td>
      <td>−0.05<br>(−3.20)</td>
      <td>0.17<br>(4.44)</td>
    </tr>
    <tr>
      <td>Beta (ex ante)</td>
      <td>0.71</td>
      <td>1.02</td>
      <td>1.59</td>
      <td>1.75</td>
      <td>0.00</td>
      <td>0.54</td>
      <td>0.76</td>
      <td>1.48</td>
      <td>1.57</td>
      <td>0.00</td>
    </tr>
    <tr>
      <td>Beta (realized)</td>
      <td>0.61</td>
      <td>0.85</td>
      <td>1.38</td>
      <td>1.49</td>
      <td>−0.03</td>
      <td>0.53</td>
      <td>0.70</td>
      <td>1.35</td>
      <td>1.42</td>
      <td>−0.02</td>
    </tr>
    <tr>
      <td>Volatility</td>
      <td>2.67</td>
      <td>3.59</td>
      <td>5.82</td>
      <td>6.06</td>
      <td>1.45</td>
      <td>1.68</td>
      <td>2.11</td>
      <td>3.90</td>
      <td>4.15</td>
      <td>1.87</td>
    </tr>
    <tr>
      <td>Sharpe ratio</td>
      <td>0.83</td>
      <td>0.72</td>
      <td>0.74</td>
      <td>0.72</td>
      <td>0.82</td>
      <td>0.77</td>
      <td>0.58</td>
      <td>0.35</td>
      <td>0.30</td>
      <td>1.02</td>
    </tr>
  </tbody>
</table>

*Panel B: Corporate bonds, 1973–2012*

<table>
  <thead>
    <tr>
      <th>Portfolios</th>
      <th>Aaa</th>
      <th>Aa</th>
      <th>A</th>
      <th>Baa</th>
      <th>Ba</th>
      <th>B</th>
      <th>Caa</th>
      <th>Ca-D</th>
      <th>Distressed</th>
      <th>BAB</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Excess return</td>
      <td>0.28<br>(3.85)</td>
      <td>0.31<br>(3.87)</td>
      <td>0.32<br>(3.47)</td>
      <td>0.37<br>(3.93)</td>
      <td>0.47<br>(4.20)</td>
      <td>0.38<br>(2.56)</td>
      <td>0.35<br>(1.47)</td>
      <td>0.77<br>(1.42)</td>
      <td>−0.41<br>(−1.06)</td>
      <td>0.44<br>(2.64)</td>
    </tr>
    <tr>
      <td>Alpha</td>
      <td>0.23<br>(3.31)</td>
      <td>0.23<br>(3.20)</td>
      <td>0.20<br>(2.70)</td>
      <td>0.23<br>(3.37)</td>
      <td>0.27<br>(4.39)</td>
      <td>0.10<br>(1.39)</td>
      <td>−0.06<br>(−0.40)</td>
      <td>−0.04<br>(−0.15)</td>
      <td>−1.11<br>(−5.47)</td>
      <td>0.57<br>(3.72)</td>
    </tr>
    <tr>
      <td>Beta (ex ante)</td>
      <td>0.67</td>
      <td>0.72</td>
      <td>0.79</td>
      <td>0.88</td>
      <td>0.99</td>
      <td>1.11</td>
      <td>1.57</td>
      <td>2.22</td>
      <td>2.24</td>
      <td>0.00</td>
    </tr>
    <tr>
      <td>Beta (realized)</td>
      <td>0.17</td>
      <td>0.29</td>
      <td>0.41</td>
      <td>0.48</td>
      <td>0.67</td>
      <td>0.91</td>
      <td>1.34</td>
      <td>2.69</td>
      <td>2.32</td>
      <td>−0.47</td>
    </tr>
    <tr>
      <td>Volatility</td>
      <td>4.50</td>
      <td>4.99</td>
      <td>5.63</td>
      <td>5.78</td>
      <td>6.84</td>
      <td>9.04</td>
      <td>14.48</td>
      <td>28.58</td>
      <td>23.50</td>
      <td>9.98</td>
    </tr>
    <tr>
      <td>Sharpe ratio</td>
      <td>0.75</td>
      <td>0.75</td>
      <td>0.68</td>
      <td>0.77</td>
      <td>0.82</td>
      <td>0.50</td>
      <td>0.29</td>
      <td>0.32</td>
      <td>−0.21</td>
      <td>0.53</td>
    </tr>
  </tbody>
</table>

4.4. Equity indexes, country bond indexes, currencies, and commodities

Table 8 reports results for equity indexes, country bond indexes, foreign exchange, and commodities. The BAB portfolio delivers positive returns in each of the four asset classes, with an annualized Sharpe ratio ranging from 0.11 to 0.51. We are able to reject the null hypothesis of zero average return only for equity indexes, but we can reject the null hypothesis of zero returns for combination portfolios that include all or some combination of the four asset classes, taking advantage of diversification. We construct a simple equally weighted BAB portfolio. To account for different volatility across the four asset classes, in month $t$ we rescale each return series to 10% annualized volatility using rolling three-year estimates up to month $t−1$ and then we equally weight the return series and their respective market benchmark. This portfolio construction generates a simple implementable portfolio that targets 10% BAB volatility in each of the asset classes. We report results for an all futures combo including all four asset classes and a country selection combo including only equity indices, country bonds and foreign exchange. The BAB all futures and country selection deliver abnormal return of 0.25% and 0.26% per month ($t$-statistics=2.53 and 2.42).

4.5. Betting against all of the betas

To summarize, the results in Tables 3–8 strongly support the predictions that alphas decline with beta and BAB factors earn positive excess returns in each asset class. Fig. 1 illustrates the remarkably consistent pattern of declining alphas in each asset class, and Fig. 2 shows the consistent return to the BAB factors. Clearly, the relatively flat security market line, shown by Black, Jensen, and Scholes (1972) for US stocks, is a pervasive phenomenon that we find across markets and asset classes. Averaging all of the BAB factors produces a diversified BAB factor with a large and significant abnormal return of 0.54% per month ($t$-statistics of 6.98) as seen in Table 8, Panel B.

5. Time series tests

In this section, we test Proposition 3’s predictions for the time series of BAB returns: When funding constraints

---

# Page 16

16

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

**Table 8**

Equity indices, country bonds, foreign exchange and commodities: returns, 1965–2012.

This table shows calendar-time portfolio returns. The test assets are futures, forwards or swap returns in excess of the relevant financing rate. To construct the betting against beta (BAB) factor, all securities are assigned to one of two portfolios: low beta and high beta. Securities are weighted by the ranked betas (lower beta security have larger weight in the low-beta portfolio and higher beta securities have larger weights in the high-beta portfolio), and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of one at portfolio formation. The BAB factor is a self-financing portfolio that is long the low-beta portfolio and short the high-beta portfolio. Alpha is the intercept in a regression of monthly excess return. The explanatory variable is the monthly return of the relevant market portfolio. Panel A reports results for equity indices, country bonds, foreign exchange and commodities. All futures and Country selection are combo portfolios with equal risk in each individual BAB and 10% ex ante volatility. To construct combo portfolios, at the beginning of each calendar month, we rescale each return series to 10% annualized volatility using rolling three-year estimate up to month $t-1$ and then equally weight the return series and their respective market benchmark. Panel B reports results for all the assets listed in Tables 1 and 2. All bonds and credit includes US Treasury bonds, US corporate bonds, US credit indices (hedged and unhedged) and country bonds indices. All equities includes US equities, all individual BAB country portfolios, the international stock BAB, and the equity index BAB. All assets includes all the assets listed in Tables 1 and 2. All portfolios in Panel B have equal risk in each individual BAB and 10% ex ante volatility. Returns and alphas are in monthly percent, t-statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. $Short (Long)$ is the average dollar value of the short (long) position. Volatilities and Sharpe ratios are annualized. *Denotes equal risk, 10% ex ante volatility.

<table>
  <thead>
    <tr>
      <th>BAB portfolios</th>
      <th>Excess return</th>
      <th>t-Statistics excess return</th>
      <th>Alpha</th>
      <th>t-Statistics alpha</th>
      <th> $Short</th>
      <th>$ Long</th>
      <th>Volatility</th>
      <th>Sharpe ratio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="9">Panel A: Equity indices, country bonds, foreign exchange and commodities</td>
    </tr>
    <tr>
      <td>Equity indices (EI)</td>
      <td>0.55</td>
      <td>2.93</td>
      <td>0.48</td>
      <td>2.58</td>
      <td>0.86</td>
      <td>1.29</td>
      <td>13.08</td>
      <td>0.51</td>
    </tr>
    <tr>
      <td>Country bonds (CB)</td>
      <td>0.03</td>
      <td>0.67</td>
      <td>0.05</td>
      <td>0.95</td>
      <td>0.88</td>
      <td>1.48</td>
      <td>2.93</td>
      <td>0.14</td>
    </tr>
    <tr>
      <td>Foreign exchange (FX)</td>
      <td>0.17</td>
      <td>1.23</td>
      <td>0.19</td>
      <td>1.42</td>
      <td>0.89</td>
      <td>1.59</td>
      <td>9.59</td>
      <td>0.22</td>
    </tr>
    <tr>
      <td>Commodities (COM)</td>
      <td>0.18</td>
      <td>0.72</td>
      <td>0.21</td>
      <td>0.83</td>
      <td>0.71</td>
      <td>1.48</td>
      <td>19.67</td>
      <td>0.11</td>
    </tr>
    <tr>
      <td>All futures (EI+CB+FX+COM)*</td>
      <td>0.26</td>
      <td>2.62</td>
      <td>0.25</td>
      <td>2.52</td>
      <td></td>
      <td></td>
      <td>7.73</td>
      <td>0.40</td>
    </tr>
    <tr>
      <td>Country selection (EI+CB+FX)*</td>
      <td>0.26</td>
      <td>2.38</td>
      <td>0.26</td>
      <td>2.42</td>
      <td></td>
      <td></td>
      <td>7.47</td>
      <td>0.41</td>
    </tr>
    <tr>
      <td colspan="9">Panel B: All assets</td>
    </tr>
    <tr>
      <td>All bonds and credit*</td>
      <td>0.74</td>
      <td>6.94</td>
      <td>0.71</td>
      <td>6.74</td>
      <td></td>
      <td></td>
      <td>9.78</td>
      <td>0.90</td>
    </tr>
    <tr>
      <td>All equities*</td>
      <td>0.63</td>
      <td>6.68</td>
      <td>0.64</td>
      <td>6.73</td>
      <td></td>
      <td></td>
      <td>10.36</td>
      <td>0.73</td>
    </tr>
    <tr>
      <td>All assets*</td>
      <td>0.53</td>
      <td>6.89</td>
      <td>0.54</td>
      <td>6.98</td>
      <td></td>
      <td></td>
      <td>8.39</td>
      <td>0.76</td>
    </tr>
  </tbody>
</table>

become more binding (e.g., because margin requirements rise), the required future BAB premium increases, and the contemporaneous realized BAB returns become negative.

We take this prediction to the data using the TED spread as a proxy of funding conditions. The sample runs from December 1984 (the first available date for the TED spread) to March 2012.

Table 9 reports regression-based tests of our hypotheses for the BAB factors across asset classes. The first column simply regresses the US BAB factor on the lagged level of the TED spread and the contemporaneous change in the TED spread. $^{19}$ We see that both the lagged level and the contemporaneous change in the TED spread are negatively related to the BAB returns. If the TED spread measures the tightness of funding constraints (given by $\psi$ in the model), then the model predicts a negative coefficient for the contemporaneous change in TED [Eq. (11)] and a positive coefficient for the lagged level [Eq. (12)]. Hence, the coefficient for change is consistent with the model, but the coefficient for the lagged level is not, under this interpretation of the TED spread. If, instead, a high TED spread indicates that agents’ funding constraints are worsening, then the results would be easier to understand. Under this interpretation, a high TED spread could indicate that banks are credit-constrained and that banks tighten other investors’ credit constraints over time, leading to a deterioration of BAB returns over time (if investors do not foresee this).

$^{19}$ We are viewing the TED spread simply as a measure of credit conditions, not as a return. Hence, the TED spread at the end of the return period is a measure of the credit conditions at that time (even if the TED spread is a difference in interest rates that would be earned over the following time period).

However, the model’s prediction as a partial derivative assumes that the current funding conditions change while everything else remains unchanged, but, empirically, other things do change. Hence, our test relies on an assumption that such variation of other variables does not lead to an omitted variables bias. To partially address this issue, column 2 provides a similar result when controlling for a number of other variables. The control variables are the market return (to account for possible noise in the ex ante betas used for making the BAB portfolio market neutral), the one-month lagged BAB return (to account for possible momentum in BAB), the ex ante beta spread, the short volatility returns, and the lagged inflation. The beta spread is equal to $(\beta_S - \beta_L)/(\beta_S \beta_L)$ and measures the ex ante beta difference between the long and short side of the BAB portfolios, which should positively predict the BAB return as seen in Proposition 2. Consistent with the model, Table 9 shows that the estimated coefficient for the beta spread is positive in all specifications, but not statistically significant. The short volatility returns is the return on a portfolio that shortsells closest-to-the-money, next-to-expire straddles on the S&P500 index, capturing potential sensitivity to volatility risk. Lagged inflation is equal to the one-year US CPI inflation rate, lagged one month, which is included to account for potential effects of money illusion as studied by Cohen, Polk, and Vuolteenaho (2005), although we do not find evidence of this effect.

Columns 3–4 of Table 9 report panel regressions for international stock BAB factors and columns 5–6 for all the BAB factors. These regressions include fixed effects and standard errors are clustered by date. We consistently find a negative relation between BAB returns and the TED spread.

---

# Page 17

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

17

**Table 9**

Regression results.

This table shows results from (pooled) time series regressions. The left-hand side is the month $t$ return of the betting against beta (BAB) factors. To construct the BAB portfolios, all securities are assigned to one of two portfolios: low beta and high beta. Securities are weighted by the ranked betas (lower beta security have larger weight in the low-beta portfolio and higher beta securities have larger weights in the high-beta portfolio), and the portfolios are rebalanced every calendar month. Both portfolios are rescaled to have a beta of one at portfolio formation. The BAB factor is a self-financing portfolio that is long the low-beta portfolio and short the high-beta portfolio. The explanatory variables include the TED spread and a series of controls. Lagged TED spread is the TED spread at the end of month $t-1$ . Change in TED spread is equal to TED spread at the end of month $t$ minus Ted spread at the end of month $t-1$ . Short volatility return is the month $t$ return on a portfolio that shorts at-the-money straddles on the S&P 500 index. To construct the short volatility portfolio, on index options expiration dates we write the next-to-expire closest-to-maturity straddle on the S&P 500 index and hold it to maturity. Beta spread is defined as $(\text{HBeta} - \text{LBeta})/(\text{HBeta}^* \text{LBeta})$ where HBeta (LBeta) are the betas of the short (long) leg of the BAB portfolio at portfolio formation. Market return is the monthly return of the relevant market portfolio. Lagged inflation is equal to the one-year US Consumer Price Index inflation rate, lagged one month. The data run from December 1984 (first available date for the TED spread) to March 2012. Columns 1 and 2 report results for US equities. Columns 3 and 4 report results for international equities. In these regressions we use each individual country BAB factors as well as an international equity BAB factor. Columns 5 and 6 report results for all assets in our data. Asset fixed effects are included where indicated, $t$ -statistics are shown below the coefficient estimates and all standard errors are adjusted for heteroskedasticity (White, 1980). When multiple assets are included in the regression, standard errors are clustered by date and 5% statistical significance is indicated in bold.

<table>
  <thead>
    <tr>
      <th rowspan="2">Left-hand side: BAB return</th>
      <th colspan="2">US equities</th>
      <th colspan="2">International equities, pooled</th>
      <th colspan="2">All assets, pooled</th>
    </tr>
    <tr>
      <th>(1)</th>
      <th>(2)</th>
      <th>(3)</th>
      <th>(4)</th>
      <th>(5)</th>
      <th>(6)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Lagged TED spread</td>
      <td>−0.025</td>
      <td>−0.038</td>
      <td>−0.009</td>
      <td>−0.015</td>
      <td>−0.013</td>
      <td>−0.018</td>
    </tr>
    <tr>
      <td></td>
      <td>(−5.24)</td>
      <td>(−4.78)</td>
      <td>(−3.87)</td>
      <td>(−4.07)</td>
      <td>(−4.87)</td>
      <td>(−4.65)</td>
    </tr>
    <tr>
      <td>Change in TED spread</td>
      <td>−0.019</td>
      <td>−0.035</td>
      <td>−0.006</td>
      <td>−0.010</td>
      <td>−0.007</td>
      <td>−0.011</td>
    </tr>
    <tr>
      <td></td>
      <td>(−2.58)</td>
      <td>(−4.28)</td>
      <td>(−2.24)</td>
      <td>(−2.73)</td>
      <td>(−2.42)</td>
      <td>(−2.64)</td>
    </tr>
    <tr>
      <td>Beta spread</td>
      <td></td>
      <td>0.011</td>
      <td></td>
      <td>0.001</td>
      <td></td>
      <td>0.001</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(0.76)</td>
      <td></td>
      <td>(0.40)</td>
      <td></td>
      <td>(0.69)</td>
    </tr>
    <tr>
      <td>Lagged BAB return</td>
      <td></td>
      <td>0.011</td>
      <td></td>
      <td>0.035</td>
      <td></td>
      <td>0.044</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(0.13)</td>
      <td></td>
      <td>(1.10)</td>
      <td></td>
      <td>(1.40)</td>
    </tr>
    <tr>
      <td>Lagged inflation</td>
      <td></td>
      <td>−0.177</td>
      <td></td>
      <td>0.003</td>
      <td></td>
      <td>−0.062</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−0.87)</td>
      <td></td>
      <td>(0.03)</td>
      <td></td>
      <td>(−0.58)</td>
    </tr>
    <tr>
      <td>Short volatility return</td>
      <td></td>
      <td>−0.238</td>
      <td></td>
      <td>0.021</td>
      <td></td>
      <td>0.027</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−2.27)</td>
      <td></td>
      <td>(0.44)</td>
      <td></td>
      <td>(0.48)</td>
    </tr>
    <tr>
      <td>Market return</td>
      <td></td>
      <td>−0.372</td>
      <td></td>
      <td>−0.104</td>
      <td></td>
      <td>−0.097</td>
    </tr>
    <tr>
      <td></td>
      <td></td>
      <td>(−4.40)</td>
      <td></td>
      <td>(−2.27)</td>
      <td></td>
      <td>(−2.18)</td>
    </tr>
    <tr>
      <td>Asset fixed effects</td>
      <td>No</td>
      <td>No</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Yes</td>
    </tr>
    <tr>
      <td>Number of observations</td>
      <td>328</td>
      <td>328</td>
      <td>5,725</td>
      <td>5,725</td>
      <td>8,120</td>
      <td>8,120</td>
    </tr>
    <tr>
      <td>Adjusted $R^2$ </td>
      <td>0.070</td>
      <td>0.214</td>
      <td>0.007</td>
      <td>0.027</td>
      <td>0.014</td>
      <td>0.036</td>
    </tr>
  </tbody>
</table>

## 6. Beta compression

We next test Proposition 4 that betas are compressed toward one when funding liquidity risk is high. Table 10 presents tests of this prediction. We use the volatility of the TED spread to proxy for the volatility of margin requirements. Volatility in month $t$ is defined as the standard deviation of daily TED spread innovations, $\sigma_t^{TED} = \sqrt{\sum_{s \in \text{month } t} (\Delta TED_s - \overline{\Delta TED}_t)^2}$ . Because we are computing conditional moments, we use the monthly volatility as of the prior calendar month, which ensures that the conditioning variable is known at the beginning of the measurement period. The sample runs from December 1984–March 2012.

Panel A of Table 10 shows the cross-sectional dispersion in betas in different time periods sorted by the TED volatility for US stocks, Panel B shows the same for international stocks, and Panel C shows this for all asset classes in our sample. Each calendar month, we compute cross-sectional standard deviation, mean absolute deviation, and inter-quintile range of the betas for all assets in the universe. We assign the TED spread volatility into three groups (low, medium, and high) based on full sample breakpoints (top and bottom third) and regress the times series of the cross-sectional dispersion measure on the full set of dummies (without intercept). In Panel C, we compute the monthly dispersion measure in each asset class and average across assets. All standard errors are adjusted for heteroskedasticity and autocorrelation up to 60 months.

Table 10 shows that, consistent with Proposition 4, the cross-sectional dispersion in betas is lower when credit constraints are more volatile. The average cross-sectional standard deviation of US equity betas in periods of low spread volatility is 0.34, and the dispersion shrinks to 0.29 in volatile credit environment. The difference is statistically significant (t-statistics = −2.71). The tests based on the other dispersion measures, the international equities, and the other assets all confirm that the cross-sectional dispersion in beta shrinks at times when credit constraints are more volatile.

Appendix B contains an additional robustness check. Because we are looking at the cross-sectional dispersion of estimated betas, one could worry that our results was driven by higher beta estimation errors, instead of a higher variance of the true betas. To investigate this possibility, we run simulations under the null hypothesis of a constant standard deviation of true betas and test whether the measurement error in betas can account for the compression observed in the data. Fig. B3 shows that the compression observed in the data is much larger than what could be generated by estimation error variance alone. Naturally, while this bootstrap analysis does not indicate that the

---

# Page 18

18

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

**Table 10**

Beta compression.

This table reports results of cross-sectional and time-series tests of beta compression. Panels A, B and C report cross-sectional dispersion of betas in US equities, international equities, and all asset classes in our sample. The data run from December 1984 (first available date for the TED spread) to March 2012. Each calendar month we compute cross sectional standard deviation, mean absolute deviation, and inter quintile range of betas. In Panel C we compute each dispersions measure for each asset class and average across asset classes. The row denoted all reports times series means of the dispersion measures. P1 to P3 report coefficients on a regression of the dispersion measure on a series of TED spread volatility dummies. TED spread volatility is defined as the standard deviation of daily changes in the TED spread in the prior calendar month. We assign the TED spread volatility into three groups (low, neutral, and high) based on full sample breakpoints (top and bottom one third) and regress the times series of the cross-sectional dispersion measure on the full set of dummies (without intercept). *t*-Statistics are shown below the coefficient estimates, and 5% statistical significance is indicated in bold. Panels D, E and F report conditional market betas of the betting against beta (BAB) portfolio based on TED spread volatility as of the prior month. The dependent variable is the monthly return of the BAB portfolios. The explanatory variables are the monthly returns of the market portfolio, Fama and French (1993), Asness and Frazzini (2013), and Carhart (1997) mimicking portfolios, but only the alpha and the market betas are reported. CAPM indicates the Capital Asset Pricing Model. Market betas are allowed to vary across TED spread volatility regimes (low, neutral, and high) using the full set of dummies. Panels D, E and F report loading on the market factor corresponding to different TED spread volatility regimes. All assets report results for the aggregate BAB portfolio of Table 9, Panel B. All standard errors are adjusted for heteroskedasticity and autocorrelation using a Bartlett kernel (Newey and West, 1987) with a lag length of sixty months.

<table>
  <thead>
    <tr>
      <th>Cross-sectional dispersion</th>
      <th>Standard deviation</th>
      <th>Mean absolute deviation</th>
      <th>Interquintile range</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="4">Panel A: US equities</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.32</td>
      <td>0.25</td>
      <td>0.43</td>
    </tr>
    <tr>
      <td>P1 (low TED volatility)</td>
      <td>0.34</td>
      <td>0.27</td>
      <td>0.45</td>
    </tr>
    <tr>
      <td>P2</td>
      <td>0.33</td>
      <td>0.26</td>
      <td>0.44</td>
    </tr>
    <tr>
      <td>P3 (high TED volatility)</td>
      <td>0.29</td>
      <td>0.23</td>
      <td>0.40</td>
    </tr>
    <tr>
      <td>P3 minus P1</td>
      <td>−0.05</td>
      <td>−0.04</td>
      <td>−0.05</td>
    </tr>
    <tr>
      <td>t-Statistics</td>
      <td>(−2.71)</td>
      <td>(−2.43)</td>
      <td>(−1.66)</td>
    </tr>
    <tr>
      <td colspan="4">Panel B: International equities</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.22</td>
      <td>0.17</td>
      <td>0.29</td>
    </tr>
    <tr>
      <td>P1 (low TED volatility)</td>
      <td>0.23</td>
      <td>0.18</td>
      <td>0.30</td>
    </tr>
    <tr>
      <td>P2</td>
      <td>0.22</td>
      <td>0.17</td>
      <td>0.29</td>
    </tr>
    <tr>
      <td>P3 (high TED volatility)</td>
      <td>0.20</td>
      <td>0.16</td>
      <td>0.27</td>
    </tr>
    <tr>
      <td>P3 minus P1</td>
      <td>−0.04</td>
      <td>−0.03</td>
      <td>−0.03</td>
    </tr>
    <tr>
      <td>t-Statistics</td>
      <td>(−2.50)</td>
      <td>(−2.10)</td>
      <td>(−1.46)</td>
    </tr>
    <tr>
      <td colspan="4">Panel C: All assets</td>
    </tr>
    <tr>
      <td>All</td>
      <td>0.45</td>
      <td>0.35</td>
      <td>0.61</td>
    </tr>
    <tr>
      <td>P1 (low TED volatility)</td>
      <td>0.47</td>
      <td>0.37</td>
      <td>0.63</td>
    </tr>
    <tr>
      <td>P2</td>
      <td>0.45</td>
      <td>0.36</td>
      <td>0.62</td>
    </tr>
    <tr>
      <td>P3 (high TED volatility)</td>
      <td>0.43</td>
      <td>0.33</td>
      <td>0.58</td>
    </tr>
    <tr>
      <td>P3 minus P1</td>
      <td>−0.04</td>
      <td>−0.03</td>
      <td>−0.06</td>
    </tr>
    <tr>
      <td>t-Statistics</td>
      <td>(−3.18)</td>
      <td>(−3.77)</td>
      <td>(−2.66)</td>
    </tr>
    <tr>
      <td colspan="4">Conditional market beta</td>
    </tr>
    <tr>
      <td>Alpha</td>
      <td>P1 (low TED volatility)</td>
      <td>P2</td>
      <td>P3 (high TED volatility)</td>
      <td>P3−P1</td>
    </tr>
    <tr>
      <td colspan="5">Panel D: US equities</td>
    </tr>
    <tr>
      <td>CAPM</td>
      <td>1.06</td>
      <td>−0.46</td>
      <td>−0.19</td>
      <td>−0.01</td>
      <td>0.45</td>
    </tr>
    <tr>
      <td></td>
      <td>(3.61)</td>
      <td>(−2.65)</td>
      <td>(−1.29)</td>
      <td>(−0.11)</td>
      <td>(3.01)</td>
    </tr>
    <tr>
      <td>Control for three factors</td>
      <td>0.86</td>
      <td>−0.40</td>
      <td>−0.02</td>
      <td>0.08</td>
      <td>0.49</td>
    </tr>
    <tr>
      <td></td>
      <td>(4.13)</td>
      <td>(−3.95)</td>
      <td>(−0.19)</td>
      <td>(0.69)</td>
      <td>(3.06)</td>
    </tr>
    <tr>
      <td>Control for four factors</td>
      <td>0.66</td>
      <td>−0.28</td>
      <td>0.00</td>
      <td>0.13</td>
      <td>0.40</td>
    </tr>
    <tr>
      <td></td>
      <td>(3.14)</td>
      <td>(−5.95)</td>
      <td>(0.02)</td>
      <td>(1.46)</td>
      <td>(4.56)</td>
    </tr>
    <tr>
      <td colspan="5">Panel E: International equities</td>
    </tr>
    <tr>
      <td>CAPM</td>
      <td>0.60</td>
      <td>−0.09</td>
      <td>0.02</td>
      <td>0.06</td>
      <td>0.16</td>
    </tr>
    <tr>
      <td></td>
      <td>(2.84)</td>
      <td>(−1.30)</td>
      <td>(0.64)</td>
      <td>(1.28)</td>
      <td>(1.87)</td>
    </tr>
    <tr>
      <td>Control for three factors</td>
      <td>0.59</td>
      <td>−0.09</td>
      <td>0.02</td>
      <td>0.05</td>
      <td>0.14</td>
    </tr>
    <tr>
      <td></td>
      <td>(3.23)</td>
      <td>(−1.22)</td>
      <td>(0.74)</td>
      <td>(1.09)</td>
      <td>(1.70)</td>
    </tr>
    <tr>
      <td>Control for four factors</td>
      <td>0.35</td>
      <td>−0.04</td>
      <td>0.05</td>
      <td>0.07</td>
      <td>0.11</td>
    </tr>
    <tr>
      <td></td>
      <td>(2.16)</td>
      <td>(−1.16)</td>
      <td>(1.51)</td>
      <td>(2.03)</td>
      <td>(2.24)</td>
    </tr>
    <tr>
      <td colspan="5">Panel F: All assets</td>
    </tr>
    <tr>
      <td>CAPM</td>
      <td>0.54</td>
      <td>−0.13</td>
      <td>−0.07</td>
      <td>0.01</td>
      <td>0.14</td>
    </tr>
    <tr>
      <td></td>
      <td>(4.96)</td>
      <td>(−2.64)</td>
      <td>(−1.82)</td>
      <td>(0.21)</td>
      <td>(2.34)</td>
    </tr>
  </tbody>
</table>

---

# Page 19

beta compression observed in Table 10 is likely due to measurement error, we cannot rule out all types of measurement error.

Panels D, E, and F report conditional market betas of the BAB portfolio returns based on the volatility of the credit environment for US equities, international equities, and the average BAB factor across all assets, respectively. The dependent variable is the monthly return of the BAB portfolio. The explanatory variables are the monthly returns of the market portfolio, Fama and French (1993) mimicking portfolios, and Carhart (1997) momentum factor. Market betas are allowed to vary across TED volatility regimes (low, neutral, and high) using the full set of TED dummies.

We are interested in testing Proposition 4(ii), studying how the BAB factor’s conditional beta depends on the TED-volatility environment. To understand this test, recall first that the BAB factor is market neutral conditional on the information set used in the estimation of ex ante betas (which determine the ex ante relative position sizes of the long and short sides of the portfolio). Hence, if the TED spread volatility was used in the ex ante beta estimation, then the BAB factor would be market-neutral conditional on this information. However, the BAB factor was constructed using historical betas that do not take into account the effect of the TED spread and, therefore, a high TED spread volatility means that the realized betas will be compressed relative to the ex ante estimated betas used in portfolio construction. Therefore, a high TED spread volatility should increase the conditional market sensitivity of the BAB factor (because the long side of the portfolio is leveraged too much and the short side is deleveraged too much). Indeed, Table 10 shows that when credit constraints are more volatile, the market beta of the BAB factor rises. The right-most column shows that the difference between low- and high-credit volatility environments is statistically significant (t-statistic of 3.01). Controlling for three or four factors yields similar results. The results for our sample of international equities (Panel E) and for the average BAB across all assets (Panel F) are similar, but they are weaker both in terms of magnitude and statistical significance.

Importantly, the alpha of the BAB factor remains large and statistically significant even when we control for the time-varying market exposure. This means that, if we hedge the BAB factor to be market-neutral conditional on the TED spread volatility environment, then this conditionally market-neutral BAB factor continues to earn positive excess returns.

## 7. Testing the model’s portfolio predictions

The theory’s last prediction (Proposition 5) is that more-constrained investors hold higher-beta securities than less-constrained investors. Consistent with this prediction, Table 11 presents evidence that mutual funds and individual investors hold high-beta stocks while LBO firms and Berkshire Hathaway buy low-beta stocks.

Before we delve into the details, let us highlight a challenge in testing Proposition 5. Whether an investor’s constraint is binding depends both on the investor’s ability to apply leverage ($m^i$ in the model) and on its unobservable risk aversion. For example, while a hedge fund could apply some leverage, its leverage constraint could nevertheless be binding if its desired volatility is high (especially if its portfolio is very diversified and hedged).

Given that binding constraints are difficult to observe directly, we seek to identify groups of investors that are

Table 11

Testing the model’s portfolio predictions, 1963–2012.

This table shows average ex ante and realized portfolio betas for different groups of investors. Panel A reports results for our sample of open-end actively-managed domestic equity mutual funds as well as results a sample of individual retail investors. Panel B reports results for a sample of leveraged buyouts (private equity) and for Berkshire Hathaway. We compute both the ex ante beta of their holdings and the realized beta of the time series of their returns. To compute the ex-ante beta, we aggregate all quarterly (monthly) holdings in the mutual fund (individual investor) sample and compute their ex-ante betas (equally weighted and value weighted based on the value of their holdings). We report the time series averages of the portfolio betas. To compute the realized betas, we compute monthly returns of an aggregate portfolio mimicking the holdings, under the assumption of constant weight between reporting dates (quarterly for mutual funds, monthly for individual investors). We compute equally weighted and value-weighted returns based on the value of their holdings. The realized betas are the regression coefficients in a time series regression of these excess returns on the excess returns of the Center for Research in Security Prices value-weighted index. In Panel B we compute ex ante betas as of the month-end prior to the initial takeover announcements date. t-Statistics are shown to right of the betas estimates and test the null hypothesis of beta = 1. All standard errors are adjusted for heteroskedasticity and autocorrelation using a Bartlett kernel (Newey and West, 1987) with a lag length of 60 months. A 5% statistical significance is indicated in bold.

<table>
  <thead>
    <tr>
      <th rowspan="2">Investor, method</th>
      <th rowspan="2">Sample period</th>
      <th colspan="2">Ex ante beta of positions</th>
      <th colspan="2">Realized beta of positions</th>
    </tr>
    <tr>
      <th>Beta</th>
      <th>t-Statistics<br>(H0: beta = 1)</th>
      <th>Beta</th>
      <th>t-Statistics<br>(H0: beta = 1)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="6">Panel A: Investors likely to be constrained</td>
    </tr>
    <tr>
      <td>Mutual funds, value weighted</td>
      <td>1980–2012</td>
      <td>1.08</td>
      <td>2.16</td>
      <td>1.08</td>
      <td>6.44</td>
    </tr>
    <tr>
      <td>Mutual funds, equal weighted</td>
      <td>1980–2012</td>
      <td>1.06</td>
      <td>1.84</td>
      <td>1.12</td>
      <td>3.29</td>
    </tr>
    <tr>
      <td>Individual investors, value weighted</td>
      <td>1991–1996</td>
      <td>1.25</td>
      <td>8.16</td>
      <td>1.09</td>
      <td>3.70</td>
    </tr>
    <tr>
      <td>Individual investors, equal weighted</td>
      <td>1991–1996</td>
      <td>1.25</td>
      <td>7.22</td>
      <td>1.08</td>
      <td>2.13</td>
    </tr>
    <tr>
      <td colspan="6">Panel B: Investors who use leverage</td>
    </tr>
    <tr>
      <td>Private equity (all)</td>
      <td>1963–2012</td>
      <td>0.96</td>
      <td>−1.50</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Private equity (all), equal weighted</td>
      <td>1963–2012</td>
      <td>0.94</td>
      <td>−2.30</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Private equity (LBO, MBO), value weighted</td>
      <td>1963–2012</td>
      <td>0.83</td>
      <td>−3.15</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Private equity (LBO, MBO), equal weighted</td>
      <td>1963–2012</td>
      <td>0.82</td>
      <td>−3.47</td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Berkshire Hathaway, value weighted</td>
      <td>1980–2012</td>
      <td>0.91</td>
      <td>−2.42</td>
      <td>0.77</td>
      <td>−3.65</td>
    </tr>
    <tr>
      <td>Berkshire Hathaway, equal weighted</td>
      <td>1980–2012</td>
      <td>0.90</td>
      <td>−3.81</td>
      <td>0.83</td>
      <td>−2.44</td>
    </tr>
  </tbody>
</table>

---

# Page 20

20 A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

plausibly constrained and unconstrained. One example of an investor that could be constrained is a mutual fund. The 1940 Investment Company Act places some restriction on mutual funds’ use of leverage, and many mutual funds are prohibited by charter from using leverage. A mutual funds’ need to hold cash to meet redemptions ($m^t > 1$ in the model) creates a further incentive to overweight high-beta securities. Overweighting high-beta stocks helps avoid lagging their benchmark in a bull market because of the cash holdings (some funds use futures contracts to “equitize” the cash, but other funds are not allowed to use derivative contracts).

A second class of investors that could face borrowing constraints is individual retail investors. Although we do not have direct evidence of their inability to employ leverage (and some individuals certainly do), we think that (at least in aggregate) it is plausible that they are likely to face borrowing restrictions.

The flipside of this portfolio test is identifying relatively unconstrained investors. Thus, one needs investors that could be allowed to use leverage and are operating below their leverage cap so that their leverage constraints are not binding. We look at the holdings of two groups of investors that could satisfy these criteria as they have access to leverage and focus on long equity investments (requiring less leverage than long/short strategies).

First, we look at the firms that are the target of bids by leveraged buyout (LBO) funds and other forms of private equity. These investors, as the name suggest, employ leverage to acquire a public company. Admittedly, we do not have direct evidence of the maximum leverage available to these LBO firms relative to the leverage they apply, but anecdotal evidence suggests that they achieve a substantial amount of leverage.

Second, we examine the holdings of Berkshire Hathaway, a publicly traded corporation run by Warren Buffett that holds a diversified portfolio of equities and employs leverage (by issuing debt, via insurance float, and other means). The advantage of using the holdings of a public corporation that holds equities such as Berkshire is that we can directly observe its leverage. Over the period from March 1980 to March 2012, its average book leverage, defined as (book equity + total debt) / book equity, was about 1.2, that is, 20% borrowing, and the market leverage including other liabilities such insurance float was about 1.6 (Frazzini, Kabiller, and Pedersen, 2012). It is therefore plausible to assume that Berkshire at the margin could issue more debt but choose not to, making it a likely candidate for an investor whose combination of risk aversion and borrowing constraints made it relatively unconstrained during our sample period.

Table 11 reports the results of our portfolio test. We estimate both the ex ante beta of the various investors’ holdings and the realized beta of the time series of their returns. We first aggregate all holdings for each investor group, compute their ex-ante betas (equal and value weighted, respectively), and take the time series average. To compute the realized betas, we compute monthly returns of an aggregate portfolio mimicking the holdings, under the assumption of constant weight between reporting dates. The realized betas are the regression coefficients

in a time series regression of these excess returns on the excess returns of the CRSP value-weighted index.

Panel A shows evidence consistent with the hypothesis that constrained investors stretch for return by increasing their betas. Mutual funds hold securities with betas above one, and we are able to reject the null hypothesis of betas being equal to one. These findings are consistent with those of Karceski (2002), but our sample is much larger, including all funds over 30-year period. Similar evidence is presented for individual retail investors: Individual investors tend to hold securities with betas that are significantly above one.$^{20}$

Panel B reports results for our sample of private equity. For each target stock in our database, we focus on its ex ante beta as of the month-end prior to the initial announcements date. This focus is to avoid confounding effects that result from changes in betas related to the actual delisting event. We consider both the sample of all private equity deals and the subsample that we are able to positively identify as LBO/MBO events. Since we only have partial information about whether each deal is a LBO/MBO, the broad sample includes all types of deals where a company is taken private. The results are consistent with Proposition 5 in that investors executing leverage buyouts tend to acquire (or attempt to acquire in case of a non-successful bid) firms with low betas, and we are able to reject the null hypothesis of a unit beta.

The results for Berkshire Hathaway show a similar pattern: Warren Buffett bets against beta by buying stocks with betas significantly below one and applying leverage.

## 8. Conclusion

All real-world investors face funding constraints such as leverage constraints and margin requirements, and these constraints influence investors’ required returns across securities and over time. We find empirically that portfolios of high-beta assets have lower alphas and Sharpe ratios than portfolios of low-beta assets. The security market line is not only flatter than predicted by the standard CAPM for US equities (as reported by Black, Jensen, and Scholes (1972)), but we also find this relative flatness in 18 of 19 international equity markets, in Treasury markets, for corporate bonds sorted by maturity and by rating, and in futures markets. We show how this deviation from the standard CAPM can be captured using betting against beta factors, which could also be useful as control variables in future research (Proposition 2). The return of the BAB factor rivals those of all the standard asset pricing factors (e.g., value, momentum, and size) in terms of economic magnitude, statistical significance, and robustness across time periods, subsamples of stocks, and global asset classes.

---

$^{20}$ As further consistent evidence, younger people and people with less financial wealth (who might be more constrained) tend to own portfolios with higher betas (Calvet, Campbell, and Sodini, 2007, Table 5). Further, consistent with the idea that leverage requires certain skills and sophistication, Grinblatt, Keloharju, and Linnainmaa (2011) report that individuals with low intelligence scores hold higher-beta portfolios than individuals with high intelligence scores.

---

# Page 21

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

21

Extending the Black (1972) model, we consider the implications of funding constraints for cross-sectional and time series asset returns. We show that worsening funding liquidity should lead to losses for the BAB factor in the time series (Proposition 3) and that increased funding liquidity risk compresses betas in the cross section of securities toward one (Proposition 4), and we find consistent evidence empirically.

Our model also has implications for agents’ portfolio selection (Proposition 5). To test this, we identify investors that are likely to be relatively constrained and unconstrained. We discuss why mutual funds and individual investors could be leverage constrained, and, consistent with the model’s prediction that constrained investors go for riskier assets, we find that these investor groups hold portfolios with betas above one on average.

Conversely, we show that leveraged buyout funds and Berkshire Hathaway, all of which have access to leverage, buy stocks with betas below one on average, another prediction of the model. Hence, these investors could be taking advantage of the BAB effect by applying leverage to safe assets and being compensated by investors facing borrowing constraints who take the other side. Buffett bets against beta as Fisher Black believed one should.

## Appendix A. Analysis and proofs

Before we prove our propositions, we provide a basic analysis of portfolio selection with constraints. This analysis is based on Fig. A1. The top panel shows the mean-standard deviation frontier for an agent with $m < 1$ , that is, an agent who can use leverage. We see that the agent can leverage the tangency portfolio $T$ to arrive at the portfolio $\overline{T}$ . To achieve a higher expected return, the agent needs to leverage riskier assets, which gives rise to the hyperbola segment to the right of $\overline{T}$ . The agent in the graph is assumed to have risk preferences giving rise to the optimal portfolio $\overline{C}$ . Hence, the agent is leverage constrained so he chooses to apply leverage to portfolio $C$ instead of the tangency portfolio.

The bottom panel of Fig. A1 similarly shows the mean-standard deviation frontier for an agent with $m > 1$ , that is, an agent who must hold some cash. If the agent keeps the minimum amount of money in cash and invests the rest in the tangency portfolio, then he arrives at portfolio $T'$ . To achieve higher expected return, the agent must invest in riskier assets and, in the depicted case, he invests in cash and portfolio $D$ , arriving at portfolio $D'$ .

Unconstrained investors invest in the tangency portfolio and cash. Hence, the market portfolio is a weighted average of $T$ and riskier portfolios such as $C$ and $D$ . Therefore, the market portfolio is riskier than the tangency portfolio.

### A.1. Proof of Proposition 1

Rearranging the equilibrium-price Eq. (7) yields

$$
E_t(r_{t+1}^s) = r^f + \psi_t + \gamma \frac{1}{P_t^s} e_s \Omega x^*
$$

$$
= r^f + \psi_t + \gamma \frac{1}{P_t^s} \text{cov}_t(P_{t+1}^s + \delta_{t+1}^s, [P_{t+1} + \delta_{t+1}]' x^*)
$$

$$
= r^f + \psi_t + \gamma \text{cov}_t(r_{t+1}^s, r_{t+1}^M) P_t x^*
\quad \text{(18)}
$$

where $e_s$ is a vector with a one in row $s$ and zeros elsewhere. Multiplying this equation by the market portfolio weights $w^s = x^{*s} P_t^s / \sum_i x^{*i} P_t^i$ and summing over $s$ gives

$$
E_t(r_{t+1}^M) = r^f + \psi_t + \gamma \text{var}_t(r_{t+1}^M) P_t x^*
\quad \text{(19)}
$$

that is,

$$
\gamma P_t' x^* = \frac{\lambda_t}{\text{var}_t(r_{t+1}^M)}
\quad \text{(20)}
$$

Inserting this into Eq. (18) gives the first result in the proposition. The second result follows from writing the expected return as

$$
E_t(r_{t+1}^s) - r^f = \psi_t (1 - \beta_t^s) + \beta_t^s (E_t(r_{t+1}^M) - r^f)
\quad \text{(21)}
$$

and noting that the first term is (Jensen’s) alpha. Turning to the third result regarding efficient portfolios, the Sharpe ratio increases in beta until the tangency portfolio is reached and decreases thereafter. Hence, the last result follows from the fact that the tangency portfolio has a beta less than one. This is true because the market portfolio is an average of the tangency portfolio (held by unconstrained agents) and riskier portfolios (held by constrained agents) so the market portfolio is riskier than the tangency portfolio. Hence, the tangency portfolio must have a lower expected return and beta (strictly lower if and only if some agents are constrained). □

### A.2. Proof of Propositions 2–3

The expected return of the BAB factor is

$$
E_t(r_{t+1}^{BAB}) = \frac{1}{\beta_t^L} (E_t(r_{t+1}^L) - r^f) - \frac{1}{\beta_t^H} (E_t(r_{t+1}^H) - r^f)
$$

$$
= \frac{1}{\beta_t^L} (\psi_t + \beta_t^L \lambda_t) - \frac{1}{\beta_t^H} (\psi_t + \beta_t^H \lambda_t)
$$

$$
= \frac{\beta_t^H - \beta_t^L}{\beta_t^L \beta_t^H} \psi_t
\quad \text{(22)}
$$

Consider next a change in $m_t^k$ . Such a change in a time $t$ margin requirement does not change the time $t$ betas for two reasons. First, it does not affect the distribution of prices in the following period $t+1$ . Second, prices at time $t$ are scaled (up or down) by the same proportion due to the change in Lagrange multipliers as seen in Eq. (7). Hence, all returns from $t$ to $t+1$ change by the same multiplier, leading to time $t$ betas staying the same.

Given Eq. (22), Eq. (12) in the proposition now follows if we can show that $\psi_t$ increases in $m^k$ because this lead to

$$
\frac{\partial E_t(r_{t+1}^{BAB})}{\partial m_t^k} = \frac{\beta_t^H - \beta_t^L}{\beta_t^L \beta_t^H} \frac{\partial \psi_t}{\partial m_t^k} > 0
\quad \text{(23)}
$$

Further, because prices move opposite required returns, Eq. (11) then follows. To see that an increase in $m_t^k$ increases $\psi_t$ , note that the constrained agents’ asset expenditure decreases with a higher $m_t^k$ . Indeed, summing the portfolio constraint across constrained agents [where

---

# Page 22

22

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

![image](image_1.png)

Fig. A1. Portfolio selection with constraints. The top panel shows the mean-standard deviation frontier for an agent with $m < 1$ who can use leverage, and the bottom panel shows that of an agent with $m > 1$ who needs to hold cash.

Eq. (2) holds with equality] gives

$$
\sum_{i \text{ constrained}} \sum_{s} x^{i,s} P_t^s = \sum_{i \text{ constrained}} \frac{1}{m^i} W_t^i \quad (24)
$$

Because increasing $m^k$ decreases the right-hand side, the left-hand side must also decrease. That is, the total market value of shares owned by constrained agents decreases.

---

# Page 23

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

23

Next, we show that the constrained agents’ expenditure is decreasing in $\psi$ . Hence, because an increase in $m_t^k$ decreases the constrained agents’ expenditure, it must increase $\psi_t$ as we wanted to show.

$$
\frac{\partial}{\partial \psi} \sum_{i \text{ constrained}} P_t^i x^i = \sum_{i \text{ constrained}} \left( \frac{\partial P_t}{\partial \psi} x^i + P_t^i \frac{\partial x^i}{\partial \psi} \right) < 0 \quad (25)
$$

to see the last inequality, note that clearly $(\partial P_t / \partial \psi) x^i < 0$ since all the prices decrease by the same proportion [seen in Eq. (7)] and the initial expenditure is positive. The second term is also negative because

$$
\sum_{i \text{ constrained}} P_t^i \frac{\partial}{\partial \psi} x^i = \sum_{i \text{ constrained}} P_t^i \frac{\partial}{\partial \psi} \frac{1}{\gamma^i} \Omega^{-1}
$$

$$
\times \left( E_t(P_{t+1} + \delta_{t+1}) - (1 + r^f + \psi_t^i) \frac{E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*}{1 + r^f + \psi} \right)
$$

$$
= -P_t^i \frac{\partial}{\partial \psi} \Omega^{-1} \sum_{i \text{ constrained}} \frac{1}{\gamma^i} (1 + r^f + \psi_t^i) \frac{E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*}{1 + r^f + \psi}
$$

$$
= -P_t^i \frac{\partial}{\partial \psi} \Omega^{-1} \frac{1}{\gamma} (q(1 + r^f) + \psi) \frac{E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*}{1 + r^f + \psi}
$$

$$
= -\left( \frac{E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*}{1 + r^f + \psi} \right) \frac{\partial}{\partial \psi} \Omega^{-1} \frac{1}{\gamma} (q(1 + r^f) + \psi) \frac{E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*}{1 + r^f + \psi}
$$

$$
= -\frac{1}{1 + r^f + \psi} \frac{\partial}{\partial \psi} \frac{q(1 + r^f) + \psi}{1 + r^f + \psi} (E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*) \Omega^{-1} (E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*) < 0 \quad (26)
$$

where we have defined $q = \sum_{i \text{ constrained}} (\gamma / \gamma^i) < 1$ and used that $\sum_{i \text{ constrained}} (\gamma / \gamma^i) \psi^i = \sum_i (\gamma / \gamma^i) \psi^i = \psi$ since $\psi^i = 0$ for unconstrained agents. This completes the proof. □

### A.3. Proof of Proposition 4

Using the Eq. (7), the sensitivity of prices with respect to funding shocks can be calculated as

$$
\frac{\partial P_t^s}{P_t^s} / \partial \psi_t = -\frac{1}{1 + r^f + \psi_t} \quad (27)
$$

which is the same for all securities $s$ . Intuitively, shocks that affect all securities the same way compress betas toward one. To see this more rigorously, we write prices as:

$$
P_t^i = \frac{E_t(P_{t+1}^i + \delta_{t+1}^i) - \gamma e_t^i \Omega x^*}{1 + r^f + \psi_t}
$$

$$
= a^i z_t + z_t E_t(P_{t+1}^i)
$$

$$
= a^i (z_t + z_t E(z_{t+1}) + z_t E(z_{t+1}) E(z_{t+2}) + \cdots)
$$

$$
= a^i \pi_t \quad (28)
$$

where we use the following definitions and that random variables are i.i.d. over time:

$$
a^i = E(\delta_{t+1}^i) - \gamma e_t^i \Omega x^*
$$

$$
z_t = \frac{1}{1 + r^f + \psi_t}
$$

$$
\pi_t = z_t + z_t E(z_{t+1}) + z_t E(z_{t+1}) E(z_{t+2}) + \cdots = \frac{z_t}{1 - E(z_{t+1})} \quad (29)
$$

with these definitions, we can write returns as $r_t^i = (P_t^i + \delta_t^i) / P_{t-1}^i = (a^i \pi_t + \delta_t^i) / a^i \pi_{t-1}$ and calculate conditional beta as follows (using that new information about $m_t$ and $W_t$ affect only the conditional distribution of $\pi_t$ ):

$$
\beta_{t-1}^i = \frac{\text{cov}_{t-1}(r_t^i, r_t^M)}{\text{var}_{t-1}(r_t^M)}
$$

$$
= \frac{\text{cov}_{t-1}((a^i \pi_t + \delta_t^i) / a^i \pi_{t-1}, (a^M \pi_t + \delta_t^M) / a^M \pi_{t-1})}{\text{var}_{t-1}(a^M \pi_t + \delta_t^M) / a^M \pi_{t-1}}
$$

$$
= \frac{\text{var}_{t-1}(\pi_t) + (1 / a^i a^M) \text{cov}_{t-1}(\delta_t^i, \delta_t^M)}{\text{var}_{t-1}(\pi_t) + (1 / (a^M)^2) \text{var}_{t-1}(\delta_t^M)} \quad (30)
$$

Here, we use that $\delta_t^s$ and $\pi_t$ are independent since the dividend is paid to the old generation of investors while $\pi_t$ depends on the margin requirements and wealth of the young generation of investors.

We see that the beta depends on the security-specific cash flow covariance, $\text{cov}_{t-1}(\delta_t^i, \delta_t^M)$ , and the market-wide discount rate variance, $\text{var}_{t-1}(\pi_t)$ . For securities with beta below (above) one, the beta is increasing (decreasing) in $\text{var}_{t-1}(\pi_t)$ . Hence, a higher $\text{var}_{t-1}(\pi_t)$ compresses betas, and the reverse is true for a lower $\text{var}_{t-1}(\pi_t)$ .

Further, if betas are compressed toward one after the formation of the BAB portfolio, then BAB will realize a positive beta as its long side is more leveraged than its short side. Specifically, suppose that the BAB portfolio is constructed based on estimated betas $(\hat{\beta}_t^L, \hat{\beta}_t^H)$ using data from a period with less variance of $\psi_t$ so that $\hat{\beta}_t^L < \beta_t^L < \beta_t^H < \hat{\beta}_t^H$ . Then the BAB portfolio will have a beta of

$$
\beta_t^{BAB} = \frac{1}{\text{var}_t(r_{t+1}^M)} \text{cov}_t \left( \frac{1}{\hat{\beta}_t^L} (r_{t+1}^L - r^f) - \frac{1}{\hat{\beta}_t^H} (r_{t+1}^H - r^f), r_{t+1}^M \right)
$$

$$
= \frac{\beta_t^L}{\hat{\beta}_t^L} - \frac{\beta_t^H}{\hat{\beta}_t^H} > 0 \quad \square \quad (31)
$$

### A.4. Proof of Proposition 5

To see the first part of the proposition, note that an unconstrained investor holds the tangency portfolio, which has a beta less than one in the equilibrium with funding constraints, and the constrained investors hold riskier portfolios of risky assets, as discussed in the proof of Proposition 1.

To see the second part of the proposition, note that given the equilibrium prices, the optimal portfolio is

$$
x^i = \frac{1}{\gamma^i} \Omega^{-1} \left( E_t(P_{t+1} + \delta_{t+1}) - (1 + r^f + \psi_t^i) \frac{E_t(P_{t+1} + \delta_{t+1}) - \gamma \Omega x^*}{1 + r^f + \psi_t} \right)
$$

$$
= \frac{\gamma}{\gamma^i} \frac{1 + r^f + \psi_t^i}{1 + r^f + \psi_t} x^* + \frac{\psi_t - \psi_t^i}{1 + r^f + \psi_t} \frac{1}{\gamma^i} \Omega^{-1} E_t(P_{t+1} + \delta_{t+1}) \quad (32)
$$

The first term shows that each agent holds some (positive) weight in the market portfolio $x^*$ and the second term shows how he tilts his portfolio away from the market. The direction of the tilt depends on whether the agent’s Lagrange multiplier $\psi_t^i$ is smaller or larger than the weighted average of all the agents’ Lagrange multipliers $\psi_t$ . A less-constrained agent tilts toward the portfolio $\Omega^{-1} E_t(P_{t+1} + \delta_{t+1})$ (measured in shares), while a more-constrained agent tilts away from this portfolio. Given the

---

# Page 24

24

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

expression (13), we can write the variance-covariance matrix as

$$
\Omega = \sigma_M^2 b b' + \Sigma
\quad \text{(33)}
$$

where $\Sigma = \text{var}(e)$ and $\sigma_M^2 = \text{var}(P_{t+1}^M)$ . Using the Matrix Inversion Lemma (the Sherman-Morrison-Woodbury formula), the tilt portfolio can be written as

$$
\begin{aligned}
&\Omega^{-1} E_t(P_{t+1} + \delta_{t+1}) \\
&= \left( \Sigma^{-1} - \Sigma^{-1} b b' \Sigma^{-1} \frac{1}{\sigma_M^2 + b' \Sigma^{-1} b} \right) E_t(P_{t+1} + \delta_{t+1}) \\
&= \Sigma^{-1} E_t(P_{t+1} + \delta_{t+1}) - \Sigma^{-1} b b' \Sigma^{-1} E_t(P_{t+1} + \delta_{t+1}) \frac{1}{\sigma_M^2 + b' \Sigma^{-1} b} \\
&= \Sigma^{-1} E_t(P_{t+1} + \delta_{t+1}) - y \Sigma^{-1} b
\quad \text{(34)}
\end{aligned}
$$

where $y = b' \Sigma^{-1} E_t(P_{t+1} + \delta_{t+1}) / (\sigma_M^2 + b' \Sigma^{-1} b)$ is a scalar. It holds that $(\Sigma^{-1} b)_s > (\Sigma^{-1} b)_k$ because $b^s > b^k$ and because $s$ and $k$ have the same variances and covariances in $\Sigma$ , implying that $(\Sigma^{-1})_{s,j} = (\Sigma^{-1})_{k,j}$ for $j \ne s,k$ and $(\Sigma^{-1})_{s,s} = (\Sigma^{-1})_{k,k} \ge (\Sigma^{-1})_{s,k} = (\Sigma^{-1})_{k,s}$ . Similarly, it holds that $[\Sigma^{-1} E_t(P_{t+1} + \delta_{t+1})]_s < [\Sigma^{-1} E_t(P_{t+1} + \delta_{t+1})]_k$ since that market exposure leads to a lower price (as seen below). So, everything else equal, a higher $b$ leads to a lower weight in the tilt portfolio.

Finally, security $s$ also has a higher return beta than $k$ because

$$
\beta_t^i = \frac{P_t^M \text{cov}(P_{t+1}^i + \delta_{t+1}^i, P_{t+1}^M + \delta_{t+1}^M)}{P_t^i \text{var}(P_{t+1}^M + \delta_{t+1}^M)} = \frac{P_t^M}{P_t^i} b^i
\quad \text{(35)}
$$

and a higher $b^i$ means a lower price:

$$
\begin{aligned}
P_t^i &= \frac{E_t(P_{t+1}^i + \delta_{t+1}^i) - \gamma (\Omega x^*)_i}{1 + r^f + \psi_t} \\
&= \frac{E_t(P_{t+1}^i + \delta_{t+1}^i) - \gamma (\Sigma x^*)_i - b^i b' x^* \gamma \sigma_M^2}{1 + r^f + \psi_t}
\quad \square
\quad \text{(36)}
\end{aligned}
$$

## Appendix B and C

See the internet appendix at http://jfe.rochester.edu/appendix.htm

## References

Acharya, V.V., Pedersen, L.H., 2005. Asset pricing with liquidity risk. J. Financial Econ. 77, 375–410.

Ang, A., Hodrick, R., Xing, Y., Zhang, X., 2006. The cross-section of volatility and expected returns. J. Finance 61, 259–299.

Ang, A., Hodrick, R., Xing, Y., Zhang, X., 2009. High idiosyncratic volatility and low returns: international and further US evidence. J. Financial Econ. 91, 1–23.

Ashcraft, A., Garleanu, N., Pedersen, L.H., 2010. Two monetary tools: interest rates and hair cuts. NBER Macroeconomics Annu. 25, 143–180.

Asness, C., Frazzini, A., 2013. The devil in HML’s details. J. Portfolio. Manage. 39, 49–68.

Asness, C., Frazzini, A., Pedersen, L.H., 2012. Leverage aversion and risk parity. Financial Anal. J. 68 (1), 47–59.

Baker, M., Bradley, B., Wurgler, J., 2011. Benchmarks as limits to arbitrage: understanding the low volatility anomaly. Financial Anal. J. 67 (1), 40–54.

Bali, T., Cakici, N., Whitelaw, R., 2011. Maxing out: stocks as lotteries and the cross-section of expected returns. J. Financial Econ. 99 (2), 427–446.

Barber, B., Odean, T., 2000. Trading is hazardous to your wealth: the common stock investment performance of individual investors. J. Finance 55, 773–806.

Black, F., 1972. Capital market equilibrium with restricted borrowing. J. Bus. 45 (3), 444–455.

Black, F., 1993. Beta and return. J. Portfolio. Manage. 20, 8–18.

Black, F., Jensen, M.C., Scholes, M., 1972. The capital asset pricing model: some empirical tests. In: Jensen, M.C. (Ed.), Studies in the Theory of Capital Markets, Praeger, New York, NY, pp. 79–121.

Brennan, M.J., 1971. Capital market equilibrium with divergent borrowing and lending rates. J. Financial Quant. Anal. 6, 1197–1205.

Brennan, M.J., 1993. Agency and asset pricing. Unpublished working paper. University of California, Los Angeles, CA.

Brunnermeier, M., Pedersen, L.H., 2009. Market liquidity and funding liquidity. Rev. Financial Stud. 22, 2201–2238.

Calvet, L.E., Campbell, J.Y., Sodini, P., 2007. Down or out: assessing the welfare costs of household investment mistakes. J. Political Econ. 115 (5), 707–747.

Carhart, M., 1997. On persistence in mutual fund performance. J. Finance 52, 57–82.

Cohen, R.B., Polk, C., Vuolteenaho, T., 2005. Money illusion in the stock market: the Modigliani-Cohn hypothesis. Q. J. Econ. 120 (2), 639–668.

Cuoco, D., 1997. Optimal consumption and equilibrium prices with portfolio constraints and stochastic income. J. Econ. Theory. 72 (1), 33–73.

De Santis, G., Gerard, B., 1997. International asset pricing and portfolio diversification with time-varying risk. J. Finance 52, 1881–1912.

Duffee, G., 2010. Sharpe ratios in term structure models. Unpublished working paper. Johns Hopkins University, Baltimore, MD.

Elton, E.G., Gruber, M.J., Brown, S.J., Goetzmann, W., 2003. Modern Portfolio Theory and Investment Analysis. Wiley, Hoboken, NJ.

Falkenstein, E.G., 1994. Mutual Funds, Idiosyncratic Variance, and Asset Returns. Northwestern University, IL (dissertation).

Fama, E.F., 1984. The information in the term structure. J. Financial Econ. 13, 509–528.

Fama, E.F., 1986. Term premiums and default premiums in money markets. J. Financial Econ. 17, 175–196.

Fama, E.F., French, K.R., 1992. The cross-section of expected stock returns. J. Finance 47 (2), 427–465.

Fama, E.F., French, K.R., 1993. Common risk factors in the returns on stocks and bonds. J. Financial Econ. 33, 3–56.

Fama, E.F., French, K.R., 1996. Multifactor explanations of asset pricing anomalies. J. Finance 51, 55–84.

Frazzini, A., Kabiller, D., Pedersen, L.H., 2012. Buffett’s Alpha. Unpublished working paper. AQR Capital Management and New York University, Greenwich, CT and New York, NY.

Fu, F., 2009. Idiosyncratic risk and the cross-section of expected stock returns. J. Financial Econ. 91 (1), 24–37.

Garleanu, N., Pedersen, L.H., 2011. Margin-based asset pricing and deviations from the law of one price. Rev. Financial Stud. 24 (6), 1980–2022.

Gibbons, M., 1982. Multivariate tests of financial models: a new approach. J. Financial Econ. 10, 3–27.

Grinblatt, M., Keloharju, M., Linnainmaa, J., 2011. IQ and stock market participation. J. Finance 66 (6), 2121–2164.

Gromb, D., Vayanos, D., 2002. Equilibrium and welfare in markets with financially constrained arbitrageurs. J. Financial Econ. 66, 361–407.

Hindy, A., 1995. Viable prices in financial markets with solvency constraints. J. Math. Econ. 24 (2), 105–135.

Kacperczyk, M., Sialm, C., Zheng, L., 2008. Unobserved actions of mutual funds. Rev. Financial Stud. 21, 2379–2416.

Kandel, S., 1984. The likelihood ratio test statistic of mean-variance efficiency without a riskless asset. J. Financial Econ. 13, 575–592.

Karczeski, J., 2002. Returns-chasing behavior, mutual funds, and beta’s death. J. Financial Quan. Anal. 37 (4), 559–594.

Lewellen, J., Nagel, S., 2006. The conditional CAPM does not explain asset-pricing anomalies. J. Financial Econ. 82 (2), 289–314.

Mehrling, P., 2005. Fischer Black and the Revolutionary Idea of Finance. Wiley, Hoboken, NJ.

Merton, R.C., 1980. On estimating the expected return on the market: an exploratory investigation. J. Financial Econ. 8, 323–361.

Moskowitz, T., Ooi, Y.H., Pedersen, L.H., 2012. Time series momentum. J. Financial Econ. 104 (2), 228–250.

Newey, W.K., West, K.D., 1987. A simple, positive semi-definite, heteroskedasticity and autocorrelation consistent covariance matrix. Econometrica 55 (3), 703–708.

Pastor, L., Stambaugh, R., 2003. Liquidity risk and expected stock returns. J. Political Econ. 111, 642–685.

---

# Page 25

A. Frazzini, L.H. Pedersen / Journal of Financial Economics 111 (2014) 1–25

25

Polk, C., Thompson, S., Vuolteenaho, T., 2006. Cross-sectional forecasts of the equity premium. J. Financial Econ. 81, 101–141.

Shanken, J., 1985. Multivariate tests of the zero-beta CAPM. J. Financial Econ. 14, 327–348.

Tobin, J., 1958. Liquidity preference as behavior toward risk. R. Econ. Stud. 25, 65–86.

Vasicek, O.A., 1973. A note on using cross-sectional information in Bayesian estimation on security beta’s. J. Finance 28 (5), 1233–1239.

White, H., 1980. A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity. Econometrica 48 (4), 817–838.