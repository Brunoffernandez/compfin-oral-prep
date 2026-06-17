# Defense sheet — Exercise set 2

This set has two problems, each in its own file:
- **Exercise 1 — Least-Squares Monte Carlo (LSM / Longstaff–Schwartz):** `exercise1_def (2).py`
- **Exercise 2 — Finite Difference (FTCS) for European and American puts:** `exercise2_def (2).py`

Line numbers below refer to those two files. Where a "why" requires my own reasoning, it is left as a `TODO (Bruno)` for me to answer out loud.

---

## The task (in my own words)

**Exercise 1 — LSM (Longstaff–Schwartz, 2001).**
- Part (i): reproduce the textbook 8-path numerical example from the paper. Strike `K = 1.10`, `r = 6%`, three yearly exercise dates (`dt = 1`, `T = 3`). Print the cash-flow matrix at each time, the in-the-money regression tables, the fitted `E[Y|X] = a0 + a1 X + a2 X^2`, the optimal early-exercise decisions, the stopping rule, the option cash-flow matrix, and finally the American and European put prices to 5 decimals.
- Part (ii): replace the 8 hard-coded paths with `N = 100,000` simulated GBM paths (50k + 50k antithetic), `K = 40`, `M = 50` exercise dates per year, and replicate the "red box" columns of Table 1 of the paper (Simulated American, s.e., closed-form European, early-exercise value) for the 20 `(S0, sigma, T)` combinations. Here the basis is the first three weighted Laguerre polynomials evaluated at `x = S/K`.

**Exercise 2 — Finite Difference (FTCS).**
- Part (i): adapt a provided `ftcs_bs_put.py` to price European puts via an explicit (forward-time, central-space) scheme in log-price space `m = log S`, for the same 20 parameter combinations, and compare against closed-form Black–Scholes.
- Part (ii): turn the European FTCS solver into an American one by adding the early-exercise (free-boundary) projection `U = max(U, intrinsic)` after each time step. Compare FD-American against the LSM-American of Exercise 1 as a correctness check.
- Part (iii): assemble the full "outside the red box" columns of Table 1 (FD American, closed-form European, FD early-exercise value, and the FD-minus-LSM difference in early-exercise value).

**TODO (Bruno):** In one sentence, why does the American put price exceed the European put price here, and why is that *not* true for an American call on a non-dividend stock?

---

## My approach and why

**Exercise 1 — LSM.**
- Backward induction over exercise dates. At each date, regress discounted realized future cash flows `Y` on a basis in the current spot `X`, but **only over in-the-money paths**, then compare immediate exercise against the fitted continuation value.
- Part (i) uses a degree-2 monomial basis `{1, X, X^2}` via an sklearn pipeline (`exercise1_def (2).py:107`).
- Part (ii) uses the first three weighted Laguerre polynomials in `x = S/K` (`exercise1_def (2).py:185-191`).
- Variance reduction by antithetic paths (`exercise1_def (2).py:177-178`).

**TODO (Bruno):** Why regress only on in-the-money paths rather than all paths? (Out-of-the-money continuation values are irrelevant to the exercise decision — but say *why* in your own words and tie it to the paper.)

**TODO (Bruno):** Why monomials `{1, X, X^2}` in Part (i) but weighted Laguerre in Part (ii)? Was this just "match the paper," or numerical conditioning? Be ready to defend both.

**TODO (Bruno):** Antithetic variates: why does pairing `Z` with `-Z` reduce variance for this payoff, and what property of the estimator makes the variance reduction work? State the covariance argument.

**Exercise 2 — FTCS.**
- Work in log-price `m = log S` so the Black–Scholes PDE has constant coefficients, build the explicit evolution matrix `F` once per parameter set, and march forward in transformed time (time-to-maturity).
- American: project onto the payoff after each step (`exercise2_def (2).py:105`).

**TODO (Bruno):** Why transform to log-price `m = log S` before discretizing instead of working directly in `S`? (Constant coefficients / uniform grid — but explain the consequence for the matrices `T1`, `T2`.)

**TODO (Bruno):** FTCS is *explicit*. Why is that an acceptable choice here, and what stability condition are you implicitly relying on with `Nt = 40000*T`? (See "hardest question" below — this is the danger zone.)

---

## Key code sections (file + what it does + why I wrote it that way)

### Exercise 1 — `exercise1_def (2).py`

- **`:11-24`** — Part (i) parameters and the 8 hard-coded paths from the paper. `C` (cash-flow matrix) initialized to zeros at `:27`, shape `(8, 3)`.
- **`:32-86`** — three printing helpers (`print_formatted_table`, `print_regression_table`, `optimal_table`) that produce the per-time tables shown in the report. Pure presentation, no pricing logic.
- **`:89` `LSQM(S,C,dt,T,K,r)`** — the Part (i) LSM engine.
  - `:91` terminal payoff `C[:,T-1] = max(K - S[:,T], 0)`.
  - `:93` `C_european` keeps a copy of the terminal payoff for the European price later.
  - `:96` backward loop `i = T-2 ... 0`.
  - `:98` regressor `X = S[:,i+1]` masked by `<K` (so OTM entries are zeroed before the ITM filter), reshaped to 2D.
  - `:99-101` builds `Y` = sum of *all* future cash flows discounted back to time `i+1` using `discount_factors = exp(-r*dt*(u-i))` with `u = arange(i+1, ncols)`.
  - `:102-104` ITM mask `S[:,i+1] < K`; restrict `X`, `Y` to ITM.
  - `:107-108` degree-2 polynomial + linear regression pipeline, fit on ITM data.
  - `:111-112` extracts intercept `a0` and coefficients `a1, a2`.
  - `:117-120` continuation = model prediction on ITM paths; exercise = `K - S` on ITM paths.
  - `:122-127` exercise rule: if `exercise > continuation`, set `C[j,i]` to exercise value and **zero out all later cash flows** `C[j,i+1:] = 0`; else `C[j,i] = 0`.
  - `:131` stopping matrix from `C != 0`.
  - `:147-152` American price: discount each path's cash flows by `exp(-r*dt*t)` for `t=1..T`, sum per path, average.
  - `:156` European price: `mean(C_european * exp(-r*dt*T))`.
- **`:167-173`** — Part (ii) parameters (`K=40`, `M=50`, `N=100000`).
- **`:175-183` `simulate_paths`** — GBM exact-step simulation; `:177` draws `N//2` normals, `:178` stacks `-Z` for antithetics; `:181-182` exact log-Euler update `S[:,i+1] = S[:,i]*exp((r-0.5 sigma^2)dt + sigma sqrt(dt) Z)`.
- **`:185-191` `laguerre_basis`** — `x=S/K`; `L0=exp(-x/2)`, `L1=exp(-x/2)(1-x)`, `L2=exp(-x/2)(1-2x+x^2/2)`; stacked column-wise.
- **`:193-196` `black_scholes_put`** — closed-form European put.
- **`:198-235` `LSM_pricing`** — Part (ii) LSM engine; same backward structure as `LSQM` but basis is `laguerre_basis` (`:212`) and `LinearRegression()` with default intercept (`:215`). Returns per-path discounted cash flows.
- **`:237-267`** — loop over the 20 `(S0, sigma, T)` combos: `M_total = M*T`, `dt = 1/M`, simulate, price, compute `american = mean(cashflow)`, `european = black_scholes_put(...)`, `ee = |american - european|` (`:257`), `se = std(cashflow)/sqrt(N)` (`:258`).

**TODO (Bruno):** `:91` and `:203` index `S[:, T]` / `S[:, M_total]` for the terminal payoff while the cash-flow matrix `C` has only `T` (resp. `M_total`) columns indexed `0..T-1`. Explain the off-by-one convention: `S` has one more column (the `t=0` spot) than `C`. Be ready to point at exactly which column of `S` is "today" and which is maturity.

**TODO (Bruno):** `:257` uses `ee = np.abs(american - european)` (absolute value) in the Part (ii) block of `exercise1_def`, but the copy in `exercise2_def (2).py:223` uses the *signed* `ee = american_value - european_value`. Which one matches the paper's "early exercise value" column, and is the absolute value ever wrong (can LSM-American dip below European by noise)?

**TODO (Bruno):** Standard error `se = std(cashflow)/sqrt(N)` at `:258`. With antithetic sampling the `N` draws are **not independent** (each path is paired with its antithetic). Is dividing by `sqrt(N)` the correct s.e., or does it understate/overstate it? Defend your formula.

### Exercise 2 — `exercise2_def (2).py`

- **`:5-14`** — parameters `K=40`, `r=0.06`, and the 20 `(S0, sigma, T)` combos.
- **`:18-64`** — **Part (i) European FTCS** loop:
  - `:24-26` closed-form BS put for reference.
  - `:29` domain length `L = 2*log(K) + 2`; `:30` `Nx = 1000`; `:31` `Nt = 40000*T`; `:32-33` steps `h = L/Nx`, `k = T/Nt`.
  - `:35-36` central-difference matrices: `T1` (first derivative, `+1/-1` off-diagonals), `T2` (second derivative, `-2` on diagonal, `1` off-diagonals), size `(Nx-1)`.
  - `:38-40` explicit evolution matrix `F = (1 - r k) I + 0.5 k sigma^2 / h^2 * T2 + k (r - 0.5 sigma^2)/(2h) * T1`.
  - `:42-43` grid `mvec`, centered and shifted by `+log(K)`.
  - `:45-46` initial condition `U[:,0] = max(K - exp(mvec), 0)` (payoff as the time-0 condition in time-to-maturity).
  - `:48-52` forward march; `:51` boundary correction term `p[0]` injected at the low-`m` (deep ITM) boundary node, scaled by `K*exp(-r*time2mat)`.
  - `:54` `np.interp` to read off the price at `log(S0)`.
- **`:66-118`** — **Part (ii) American FTCS** loop: identical to Part (i) except `intrinsic = max(K - exp(mvec), 0)` (`:95`) and the single added projection line `:105` `U[:,i+1] = np.maximum(U[:,i+1], intrinsic)`. `ee = ftcs_american - bs_put` (`:108`).
- **`:120-204`** — re-imports and re-runs the **Exercise 1 Part (ii) LSM** code (paths, Laguerre basis, BS put, `LSM_pricing`) to regenerate `results_lsmc` for the cross-check.
- **`:235-248`** — correctness test table: `|FD American - LSM American|` per row.
- **`:250-261`** — full "outside the red box" table including the signed `FD EE - LSM EE` difference.

**TODO (Bruno):** `:29` `L = 2*log(K) + 2`. Why this width, and why center the grid at `log(K)` (`:43`)? What goes wrong at short maturity / high vol if the domain is too narrow — and what is the analogy with the COS truncation-range `[a,b]` issue I hit in Assignment 2?

**TODO (Bruno):** `:51` the boundary term `p[0]`. Explain in words what Dirichlet boundary condition this enforces at the deep-in-the-money edge, why it carries the factor `K*exp(-r*time2mat)`, and what happens at the *other* (high-`S`) boundary where no correction is added.

**TODO (Bruno):** `:105` is described in the report as "the single line that changes." Explain why projecting `U = max(U, intrinsic)` after each explicit step is a valid (operator-splitting / explicit-penalty) treatment of the American free boundary, and what its accuracy cost is versus a proper LCP/PSOR solve.

---

## Design decisions I must justify

1. **ITM-only regression** (`:103-104`, `:211-213`). Factual: the mask is `S[:,i+1] < K`. **TODO (Bruno):** justify why this is the Longstaff–Schwartz prescription and not a shortcut.
2. **Basis choice:** monomials degree 2 in Part (i) (`:107`) vs weighted Laguerre in Part (ii) (`:185-191`). Factual: the report says normalization `x=S/K` avoids underflow in `exp(-x/2)` for `S in [36,44]`. **TODO (Bruno):** confirm you can derive the underflow argument and say why monomials were fine for the small `K=1.10` example.
3. **Antithetic variates** (`:177-178`). **TODO (Bruno):** justify and quantify expected variance reduction.
4. **Exact GBM step** (`:182`) rather than Euler. **TODO (Bruno):** why is the log update exact for GBM, and does discretization bias still enter the American price through the discrete exercise dates regardless?
5. **`M = 50` exercise dates/year as a proxy for continuous American exercise** (`:172`, `:251`). **TODO (Bruno):** why is a Bermudan with 50/100 dates a good stand-in for the true American, and which direction is the bias?
6. **Explicit FTCS with `Nt = 40000*T`** (`exercise2_def (2).py:31`). **TODO (Bruno):** show that this choice keeps the scheme inside the explicit stability region (compute the CFL-type bound; see hardest question).
7. **`np.interp` to extract the price at `log(S0)`** (`:54`, `:107`). Factual: linear interpolation between grid nodes. **TODO (Bruno):** is linear interpolation accurate enough given `h`, or should it be higher order?

---

## Results and what they mean

**Exercise 1, Part (i)** (from the report): American put price **0.11443**, European put price **0.05638** on the same 8 paths. The fitted regressions match the paper: at `t=2`, `E[Y|X] = -1.06999 + 2.98341 X - 1.81358 X^2`; at `t=1`, `E[Y|X] = 2.03751 - 3.33544 X + 1.35646 X^2`. Stopping rule and option cash-flow matrix reproduce the paper's table.

**Exercise 1, Part (ii)** (report Fig. 13): the 20-row replication of the red-box columns; e.g. `S=36, sigma=0.2, T=1` gives Simulated American **4.4714 (s.e. 0.0094)**, closed-form European **3.8443**, early-exercise value **0.6271**. s.e. all in the 0.006–0.023 range.

**Exercise 2, Part (i)** (report Fig. 14): FD-European vs BS-European agree to ~1e-4 across all 20 rows (largest `|Difference| = 0.0008` at `S=40, sigma=0.2, T=1`).

**Exercise 2, Part (ii)** (report Fig. 16): FD-American prices, all above the corresponding European, with early-exercise values matching the LSM ones in sign and magnitude.

**Exercise 2 cross-check** (report Fig. 17): `|FD American - LSM American|` is below 0.05 for all 20 rows (max ~0.016), and the Part (iii) `FD EE - LSM EE` differences are small and alternate in sign.

**TODO (Bruno):** The FD-European prices are *systematically slightly below* BS (every `Difference` is negative, ~ -1e-4 to -8e-4). Is that a bias of the explicit scheme, the truncated domain, or the interpolation? Pick one and defend it — Fang will ask why the sign is consistent.

**TODO (Bruno):** The FD-American vs LSM-American differences are ~0.005–0.016, an order of magnitude larger than the FD-European vs BS error (~1e-4). Why is the American comparison so much looser? (Hint: LSM bias + 50-date Bermudan + regression noise vs a near-exact PDE.)

---

## The hardest question Fang could ask here — and my answer

**Likely hardest: "Your FTCS scheme is explicit. Is it stable for `Nx = 1000`, `Nt = 40000*T`? Derive the condition and check it for your worst-case `sigma = 0.4`."**

Factual setup from the code: in log-space the diffusion coefficient is `0.5*sigma^2`, `h = L/Nx` with `L = 2 log K + 2 = 2 log 40 + 2 ≈ 9.376`, so `h ≈ 0.00938`; `k = T/Nt = 1/40000 = 2.5e-5` per unit time.

The explicit-scheme stability constraint for the diffusion part is roughly `0.5*sigma^2 * k / h^2 <= 1/2`, i.e. `k <= h^2 / sigma^2`.

**TODO (Bruno):** Plug in the numbers: `h^2 / sigma^2 = (0.00938)^2 / 0.16 ≈ 5.5e-4`, and `k = 2.5e-5 << 5.5e-4`, so the diffusion number `≈ 0.045 << 0.5`. State this out loud, confirm the scheme is comfortably stable, and explain *why the author picked Nt so large* (was it stability, or matching the paper's accuracy?). Also be ready to say what the `(1 - r k)` reaction term and the `T1` advection term contribute to the stability bound — and whether the advection (first-derivative) term can cause spurious oscillations even when the diffusion bound is met.

**Backup hardest (LSM): "Is your LSM price biased high or low, and why?"**
**TODO (Bruno):** Standard result — using the *same* paths to estimate the continuation regression and to value the option introduces a look-ahead/in-sample bias in the continuation estimate, so the exercise decision uses noisy information. State the direction of the resulting price bias and how an out-of-sample / two-pass scheme would fix it.

---

## "Show me in your code where you do X" — anticipated spots

- **"...filter to in-the-money paths before regressing."** `exercise1_def (2).py:102-104` (`itm_indexes = S[:,i+1] < K`), and `:211-213` for Part (ii).
- **"...build the discounted continuation target Y."** `:99-101` (Part i) and `:207-209` / `:182-184` (Part ii).
- **"...fit the continuation-value regression and read off the coefficients."** `:107-112` (monomial pipeline) and `:215-217` (Laguerre).
- **"...make the exercise-vs-continue decision and zero out future cash flows."** `:122-127` (Part i), `:224-229` / `:194-199` (Part ii).
- **"...compute the American and European prices."** `:147-157` (Part i American + European).
- **"...generate antithetic paths."** `:177-178`.
- **"...evaluate the weighted Laguerre basis."** `:185-191`.
- **"...the closed-form Black–Scholes put."** `:193-196` (Ex.1), `exercise2_def (2).py:24-26` and `:74-76`.
- **"...assemble the explicit FTCS evolution matrix F."** `exercise2_def (2).py:35-40` (and `:85-90`).
- **"...set the initial/boundary conditions of the PDE."** initial: `:45-46`; boundary term: `:51` (and `:103`).
- **"...the one line that makes it American."** `exercise2_def (2).py:105` (`U = np.maximum(U, intrinsic)`).
- **"...read the price off the grid at S0."** `:54` and `:107` (`np.interp(np.log(S0), mvec, U[:, Nt])`).
- **"...cross-check FD against LSM."** `:235-248` (`|FD American - LSM American|`).
