# Defense sheet — Exercise set 1

> Scope note. This set has four exercises. Only **Ex. 1** (implied volatility) and **Ex. 4** (Monte Carlo basket call) are code. **Ex. 2** (risk-neutral pricing / change of numéraire, Black–Scholes recovery) and **Ex. 3** (ratio SDE, change to QS1) are pen-and-paper derivations in the report PDF. This sheet centres on the two `.py` files but flags the analytic exercises where the code depends on them (the QS1 dynamics in Ex. 4 come straight from Ex. 3).
>
> Files referenced:
> - `assignments/exercise-set-1/exercise_1_computational_finance (2).py`
> - `assignments/exercise-set-1/exercise_4_computational_finance (2).py`

---

## The task (in my own words)

**Exercise 1 — Implied volatility.** From a CSV of SPX call/put quotes (expiry 2021-12-01, near-the-money), back out the Black–Scholes implied volatility for each call strike by solving `C_BS(S0,K,r,T,σ) = C_mkt` two ways: (i) bisection, (ii) Newton–Raphson. Plot IV vs strike for each, overlay them, and compare against the CSV's own IV column; discuss why they differ (bid–ask, dividends, rounding, tolerance). Assumptions fixed by the brief: `r = 0.11%`, Act/365, no dividends.

**Exercise 4 — Monte Carlo basket call.** Price a European basket call with payoff `(A_T − K)^+`, `A_T = ½(S1(T)+S2(T))`, on two correlated GBM stocks. Do it two ways: under the risk-neutral measure Q, and under the QS1 measure (S1 as numéraire) whose dynamics were derived analytically in Ex. 3. For a grid of path counts `M ∈ {10k,25k,50k,75k,100k}`, report price and standard error under both measures, check the SE decays like `1/√M`, and explain the variance reduction of QS1. Run it for two parameter scenarios.

**TODO (Bruno):** In one sentence, state the single conceptual link between Ex. 3 and Ex. 4 — i.e. why the QS1 simulation in Ex. 4 is not a separate idea but a direct numerical test of the change of measure you derived by hand.

---

## My approach and why

**TODO (Bruno):** Why bisection *and* Newton, rather than just one? What does each buy you, and what is the standard pedagogical point (robustness vs speed) you are demonstrating?

**TODO (Bruno):** Why solve only on the **call** quotes and not the puts? (The code filters `df['Type'] == 'Call'`.) Could you have used puts via put–call parity? Why didn't you?

**TODO (Bruno):** For Ex. 4, why is pricing under QS1 expected to reduce variance at all? State the mechanism in your own words (drift removal + near-cancellation of the two correlated stocks), and connect it to the effective volatility `σ̃ = √(σ1²+σ2²−2ρσ1σ2)` you quote in the report.

**TODO (Bruno):** Why did you choose the *exact* GBM solution (one-step terminal sampling) rather than an Euler time-stepping scheme for the basket? What property of the payoff makes this legitimate?

**TODO (Bruno):** Why did you fix `np.random.seed(44)` *inside* each simulation function, and what is the consequence for the Q vs QS1 comparison (same Z draws reused)? Is that a feature or a bug for a fair variance comparison?

---

## Key code sections (file + what it does + why I wrote it that way)

### Exercise 1 — `exercise_1_computational_finance (2).py`

- **`C_bs(S0,K,r,T,sigma)` (lines 9–17).** Black–Scholes call price. Line 13–14 guard: if `sigma<=0` or `T<=0` it returns the intrinsic value `max(S0 − K e^{−rT}, 0)` instead of dividing by zero. Lines 15–17 compute `d1`, `d2` and return `S0·Φ(d1) − K e^{−rT}·Φ(d2)`.
- **`implied_volatility_bisection(...)` (lines 19–41).** Bracketing root-finder for `C_bs(σ) − C_mkt = 0`. Lines 24–25 evaluate the residual at the bracket ends; line 28–29 return `NaN` if the root is not bracketed (`f_low·f_high > 0`). Lines 30–40 are the bisection loop: midpoint at line 31, stop test at line 34 (`|f_mid| < tol` **or** interval width `< tol`), and the sub-interval update at lines 37–40. Line 41 returns the midpoint if `max_iter` is exhausted.
- **`Vega(S0,K,r,T,sigma)` (lines 43–49).** Returns `S0·√T·φ(d1)`, the BS vega, used as the Newton derivative.
- **`implied_volatility_Newton_Ralphson(...)` (lines 51–67).** Newton on the same residual. Line 58 sets the initial guess `σ0 = √((1/T)·2|ln(S0/K) + rT|)`. Lines 60–66 iterate `σ ← σ − (C_bs − C_mkt)/vega`, stopping when `|diff| < tol` (line 64).
- **Data pipeline (lines 70–96).** Line 70 reads the CSV; line 74 pulls `S0` from the `'SPX'` row / `'2021-Nov-19'` column; line 75 sets `T = 12/365`; line 76 sets `r = 0.0011`. Line 79 keeps calls only. Lines 82–84 strip commas from `Strike` and `%` from `IV` and cast to float, dropping rows with missing `Strike`/`Midpoint`. Lines 94–96 build the two IV lists by looping over `(Strike, Midpoint)` pairs, using `Midpoint` as `C_mkt`.
- **Plots (lines 102–127).** Three figures: bisection alone, bisection vs Newton, and both vs the CSV `IV` column.

**TODO (Bruno):** Explain line 58 — where does the initial-guess formula `√((1/T)·2|ln(S0/K)+rT|)` come from, and in what sense does it "guarantee global convergence" (the report's claim)? Be ready to name the result / slide it comes from in Lecture 3.

**TODO (Bruno):** Line 34 stops on `|f_mid| < tol` *or* `(sigma_high − sigma_low) < tol` with the **same** `tol = 1e-6`. Why is mixing a price-space tolerance and a vol-space tolerance under one constant acceptable here — or is it something you'd defend differently if pushed?

### Exercise 4 — `exercise_4_computational_finance (2).py`

- **`simulate_underQ(...)` (lines 8–41).** MC under Q. Lines 20–21 draw two independent `N(0,1)` vectors; lines 25–26 correlate them by Cholesky (`W1 = Z1`, `W2 = ρZ1 + √(1−ρ²)Z2`). Lines 29–30 sample terminal `S1,S2` from the **exact** GBM solution with drift `r − ½σ²`. Line 32 forms `A_T = ½(S1+S2)`; line 35 the discounted payoff `e^{−rT}(A_T−K)^+`. Lines 38–39 return the sample mean `V_aprox` and SE `std(ddof=1)/√M`.
- **`simulate_underQS1(...)` (lines 43–77).** MC under QS1 (S1 as numéraire). Same correlated draws (lines 61–62). Line 65: `S1` now carries drift `r + ½σ1²` (sign flip vs Q — this is the numéraire-induced drift from Ex. 3). Line 66: `S2` carries drift `r + ρσ1σ2 − ½σ2²`. Line 71: the estimator weights the payoff by `S0[0]/S1`, i.e. `V = S0[0]·(A_T−K)^+/S1`, and is **not** discounted by `e^{−rT}` (the numéraire change absorbs the discount). Lines 74–75 return mean and SE.
- **`simulate_scenarios(...)` (lines 79–133).** Loops `M` over the grid (line 88), runs both estimators (lines 89–90), unpacks prices/SEs (lines 93–96), prints the summary table (lines 99–103), and makes the dual-axis price/SE plot (lines 106–133). Lines 119–122 build the `1/√M` reference curves by fitting the constant `C = SE(M0)·√M0` from the first point and plotting `C/√M`.
- **Driver (lines 135–153).** Scenario 1: `S0=[100,100]`, `σ=(0.2,0.2)`, `r=0.06`, `ρ=0.9999`, `T=2`, `K=100`. Scenario 2: `S0=[443,73]`, `σ=(0.1,0.2)`, `ρ=0.2`, `K=(443+73)/2 = 258`.

**TODO (Bruno):** Walk through *why* the QS1 estimator on line 71 is `S0[0]·(A_T−K)^+/S1` with no explicit `e^{−rT}`. Derive the change-of-measure identity `e^{−rT}E^Q[(A_T−K)^+] = S0·E^{QS1}[(A_T−K)^+/S1(T)]` and point to exactly where the discount factor went. This is the line most likely to be probed.

**TODO (Bruno):** Line 65 uses `r + ½σ1²` for `S1` and line 66 uses `r + ρσ1σ2 − ½σ2²` for `S2`. Match each of these drifts to the result you derived in Ex. 3(c). Are these the drifts of `S1`,`S2` themselves under QS1, or the drifts that appear once you write the exact-solution exponent? Be precise.

---

## Design decisions I must justify

**TODO (Bruno):** Bisection bracket `[1e-6, 5.0]` (lines 88–89). Why this upper bound of 500% vol — is it comfortably above any IV in this near-the-money SPX data, and what happens to the `NaN`-guard (line 28) if a quote's true IV exceeded it?

**TODO (Bruno):** `tol = 1e-6`, `max_iter = 200` (bisection) / `100` (Newton). Justify these numbers. How many bisection steps does it actually take to shrink `[1e-6,5]` below `1e-6` (≈ `log2(5/1e-6) ≈ 22`), and why is 200 then generous?

**TODO (Bruno):** `T = 12/365` (line 75). Confirm this matches the 12-day Act/365 horizon implied by the data, and be ready to say what the expiry/quote dates are.

**TODO (Bruno):** Using `Midpoint` (mid bid–ask) as `C_mkt` (lines 94–96). Why mid rather than bid or ask, and how does this choice feed directly into your Ex. 1.3 discussion of the discrepancy with the CSV IV column?

**TODO (Bruno):** Seed `44` and the choice to re-seed identically in both Q and QS1 functions. Defend whether the variance-reduction claim is fair given both estimators consume the *same* random numbers.

**TODO (Bruno):** Scenario design. Scenario 1 is the near-degenerate case (`ρ=0.9999`, equal vols) where QS1 nearly annihilates the variance; Scenario 2 (`ρ=0.2`, unequal vols) is the generic case. Why pick these two specifically — what is each meant to *demonstrate* about when change-of-numéraire helps?

---

## Results and what they mean

Reported in the PDF (Figures 4–7), reproduced here as facts the code produces:

- **Scenario 1.** Both estimators converge to ≈ 17.18 (Q) / 17.19 (QS1). SE under Q falls 0.232 → 0.073 as `M: 10k → 100k`; under QS1 0.163 → 0.051. Both ratios ≈ `0.313 ≈ 1/√10`, consistent with the CLT `1/√M` rate. QS1 SE sits below Q SE at every `M`.
- **Scenario 2.** Both estimators converge to ≈ 32.55 (Q) / 32.56 (QS1). SE under Q 0.305 → 0.097; under QS1 0.253 → 0.080; ratios ≈ `1/√10`. QS1 still lower but the gap is smaller than in Scenario 1.
- **Effective vol explanation in the report.** Scenario 1: `σ̃ = √(0.04+0.04−2·0.9999·0.04) ≈ 0`, so `X_T = S2/S1` is nearly constant under QS1 and the payoff `(A_T−K)^+/S1` has tiny variance. Scenario 2: `σ̃ = √(0.01+0.04−2·0.2·0.1·0.2) ≈ √0.042 ≈ 20.5%`, so the ratio keeps real volatility and the variance reduction is modest.

**TODO (Bruno):** The Ex. 1 plots show IV decreasing in strike (a downward "skew" over this narrow near-the-money window). In your own words, what does that shape say about the market's implied distribution vs the lognormal BS assumption — and is the monotone decrease here actually the left wing of a smile? Don't over-claim from 12 strikes.

**TODO (Bruno):** Your report says bisection and Newton "overlap as expected." State the precise reason they must agree (same equation, both converged below `tol`), and give the one situation where Newton could *fail* here while bisection still returns a value.

**TODO (Bruno):** In Scenario 2 you wrote `σ̃ ≈ 20.5%`. Sanity-check: is QS1's variance reduction in Scenario 2 coming from the lowered diffusion of the ratio, or *only* from the removed drift? Reconcile with the fact that `σ̃ (≈20.5%)` is barely below `σ2 = 20%`.

---

## The hardest question Fang could ask here — and my answer

**Likely hardest question (Ex. 4 / change of numéraire):**
> "On line 71 you price under QS1 as `S0[0]*max(A_T−K,0)/S1` with no discount factor. Derive that estimator from `V0 = e^{−rT}E^Q[(A_T−K)^+]`, and tell me exactly why the `e^{−rT}` disappears."

**TODO (Bruno):** Write the full derivation: start from `V0 = e^{−rT}E^Q[(A_T−K)^+]`, use `dQS1/dQ = (S1(T)/BT)/(S1(0)/B0)` from Ex. 3(b) to swap measure, and arrive at `V0 = S1(0)·E^{QS1}[(A_T−K)^+/S1(T)]`. Then say in one line where the discount went (absorbed because the deflator is now the numéraire S1, not the bank account B). Be able to do this on the board cold.

**Runner-up (Ex. 1):**
> "Your Newton initial guess (line 58) — prove it lands you in the region where Newton converges, or at least argue why C_BS(σ) is well-behaved enough that Newton can't overshoot to a negative σ."

**TODO (Bruno):** Prepare the convexity/monotonicity argument: `C_BS` is strictly increasing in σ (vega > 0), and state what the Lecture 3 initial guess guarantees. If you cannot prove global convergence rigorously, say honestly that the formula is a heuristic from the slides and describe the safeguard you'd add (e.g. fall back to bisection).

---

## "Show me in your code where you do X" — anticipated spots

| If Fang says… | Point to |
|---|---|
| "Show me the Black–Scholes price." | `exercise_1_computational_finance (2).py:15–17` |
| "Show your bisection bracketing / failure guard." | lines 28–29 (`NaN` if not bracketed) |
| "Show the bisection stopping criterion." | line 34 |
| "Show the Newton update step." | line 66 |
| "Show your Newton initial guess." | line 58 |
| "Show where you compute vega." | lines 48–49 |
| "Where do you set S0, T, r from the data?" | lines 74–76 |
| "Where do you use the mid price as C_mkt?" | lines 94–96 (`Midpoint`) |
| "Show the exact GBM terminal sampling under Q." | `exercise_4_computational_finance (2).py:29–30` |
| "Show the Cholesky correlation of the two Brownians." | lines 25–26 (Q), 61–62 (QS1) |
| "Show the QS1 drifts." | lines 65–66 |
| "Show the QS1 estimator (no discount, ÷S1)." | line 71 |
| "Show the standard-error formula." | lines 39 / 75 (`std(ddof=1)/√M`) |
| "Show the 1/√M reference-curve construction." | lines 118–122 |
| "Where do you set the two scenarios' parameters?" | lines 136–143 and 146–153 |
