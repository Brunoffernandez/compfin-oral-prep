# Defense sheet — Assignment set 2

> Scope: pricing a European basket call `V(0) = e^{-rT} E^Q[max(w1 S1(T) + w2 S2(T) - K, 0)]`
> with `w1 = w2 = 0.5`, `T = 1`, `r = 0.02`, `K = 100`, by three methods:
> Q1 Monte Carlo, Q2 moment matching, Q3 the 2D COS method.
> Two market setups recur in every question:
> **(a)** both underlyings log-normal (GBM), `S10=S20=100`, `sigma1=0.20`, `sigma2=0.30`, `rho=0.30`;
> **(b)** `S1` log-normal, `S2` a CIR / square-root process `dS2 = r S2 dt + sigma2 sqrt(S2) dW2`,
> `sigma1=0.25`, `sigma2=1.5`, `rho=0.10` in Q1 / `rho=0` in Q2 and Q3.
>
> NOTE: the assignment PDF could not be rendered in this environment (no `poppler`/`pypdf`),
> so the "task in my own words" below is reconstructed from the in-code comments and parameters.
> **TODO (Bruno):** open `Computational_Finance_Assignment_2 (2) (1).pdf` and confirm the exact
> wording of each sub-question (especially what convergence behaviour Q1 and Q3 ask you to demonstrate).

## The task (in my own words)

Price a two-asset European **basket call** under the risk-neutral measure Q. The basket is
`B_T = w1 S1(T) + w2 S2(T)`; the payoff is `max(B_T - K, 0)`, discounted at `e^{-rT}`.

- **Q1 — Monte Carlo.** Simulate the basket and report the price with a standard error / 95% CI.
  (a) both assets GBM, correlated, exact terminal simulation. (b) `S1` GBM, `S2` a CIR square-root
  process under the Q-drift `r S2`; demonstrate (i) the weak / time-discretization convergence of
  the Euler scheme and (ii) the statistical `O(1/sqrt(M))` convergence.
- **Q2 — Moment matching.** Compute the raw moments of `B_T` in closed form, then approximate the
  basket distribution by matching 2, 3, 4 moments (log-normal, shifted log-normal, Johnson SU) and
  price the call from each. Benchmark against a high-precision Monte Carlo price.
- **Q3 — 2D COS.** Price the basket with the two-dimensional COS method (Ruijter & Oosterlee 2012),
  expanding the joint density of the two state variables on `[a1,b1] x [a2,b2]`, exploiting `rho=0`
  so the 2D density coefficients factorise into a product of 1D coefficients. Show convergence in `N`.

**TODO (Bruno):** confirm whether the PDF asks for these specific deliverables or also for, e.g., a
comparison table across the three methods.

## My approach and why

- **Q1:** exact GBM simulation at maturity where possible (no time grid needed); Euler–Maruyama with
  full truncation for the CIR leg because exact joint simulation is unavailable when `rho != 0`.
- **Q2:** derive `E[B_T^k]` analytically from the binomial expansion of `(w1 S1 + w2 S2)^k` and the
  cross moments of correlated log-normals (and the non-central chi-square moments for the CIR leg),
  then fit successively richer distributions to more moments.
- **Q3:** 1D characteristic functions per marginal, cumulant-rule truncation range per marginal,
  payoff coefficients by 2D trapezoidal quadrature, assembled as `chi1^T V chi2`.

**TODO (Bruno):** for each method, state in one sentence *why* it is the right tool and what each
buys you (MC = unbiased baseline, moment matching = cheap closed-form approximation, COS = spectral
accuracy). Do not let the examiner hear a generic answer.

## Key code sections (file + what it does + why I wrote it that way)

### Q1 — basket Monte Carlo (`Q1_basket_MC (1).py`)

- **`simulate_basket_lognormal(M)` — lines 17–42.** Q1(a). Draws two standard normals
  (`Z1`, `Zc`, lines 27–28) and correlates them by Cholesky: `Z2 = rho*Z1 + sqrt(1-rho^2)*Zc`
  (line 29). Simulates terminal prices with the **exact GBM solution** at `T` (lines 32–33), forms
  the basket and discounted payoff (lines 36–37), and returns the MC mean and standard error
  `std(ddof=1)/sqrt(M)` (lines 40–41).
- **Convergence loop — lines 48–63.** Prices over `M = 2000 … 1e6` (line 48), then estimates the
  convergence rate as the OLS slope of `log(SE)` vs `log(M)` (line 62), expected `-0.5`.
- **`simulate_basket_cir(M, n_steps)` — lines 93–125.** Q1(b). Time-steps with `h = T/n_steps`
  (line 107). `S1` exact GBM step (line 118); `S2` **Euler–Maruyama** step with **full truncation**
  `S2p = max(S2,0)` inside drift and diffusion (lines 120–121), so the square root is always defined.
- **Weak-error test — lines 134–185.** Reuses the **same fine Brownian increments** across all
  coarse grids (`basket_on_grid`, lines 144–159; increments summed into blocks at lines 151–152) to
  isolate the discretization bias from MC noise. Fits the weak order as the slope of `log|bias|` vs
  `log h` on the coarse grids (line 184), expected `1.0`.
- **Statistical-error test — lines 198–210.** Fixes the grid, varies `M`, fits the SE slope (line 209).

**TODO (Bruno):** justify (i) full truncation vs reflection / other CIR fixes; (ii) why you reuse the
same increments across grids for the weak-error test; (iii) the Q-drift argument at lines 86–91
(physical CIR drift `kappa(theta - S2)` replaced by `r S2` because the discounted price is a Q-martingale).

### Q2 — moment matching (`Q2_moment_matching (1).py`)

- **`lognormal_cross(j, m, ...)` — lines 20–29.** Cross raw moment `E[S1^j S2^m]` for two correlated
  log-normals, from `E[exp(N)] = exp(mean + 0.5 var)` with the combined log-return mean/variance/cov
  at lines 26–29.
- **`basket_moments_LN(...)` — lines 31–37.** Raw basket moments `E[B_T^k]` via the binomial
  expansion `sum_j C(k,j) w1^j w2^(k-j) E[S1^j S2^(k-j)]`.
- **`cir_S2_rawmoments(...)` — lines 39–53.** Raw moments of `S2(T) = c·Z`, `Z ~ chi'^2_0(lambda)`
  (zero-dof non-central chi-square), using cumulants `kappa_n = 2^(n-1) n! lambda` (line 49) and the
  raw-from-cumulant recursion (lines 50–52). `c` and `lambda` from the technical hint at lines 46–48.
- **`basket_moments_CIR(...)` — lines 55–64.** Combines the LN-`S1` and CIR-`S2` marginal moments
  under independence (`rho=0`), so joint moments factorise (line 63).
- **`central_from_raw(mom)` — lines 66–75.** Converts raw moments to mean, variance, skewness, kurtosis.
- **`price_2moments` — lines 78–89.** Fits a log-normal matching `m1`, `m2`; Black's formula with
  `F = m1`, total variance `s^2 = log(m2/m1^2)`.
- **`price_3moments` — lines 91–107.** Shifted log-normal `B = gamma + L`; inverts the log-normal
  skewness `(w+2)sqrt(w-1) = g1` for `w` by `brentq` (line 99), recovers shift and shifted strike.
- **`price_4moments` — lines 109–139.** Johnson SU; solves the 2×2 system for `(delta, gamma)` from
  skewness and kurtosis by `least_squares` with Gauss–Hermite moments of `sinh` (`U_moments`,
  lines 120–125; residual lines 127–132; solve line 134), then prices by Gauss–Hermite quadrature
  (line 139). GH nodes/weights set at lines 16–17.
- **MC benchmarks — `mc_benchmark_LN` lines 144–159, `mc_benchmark_CIR` lines 161–180.** Exact
  simulation with antithetic variates; the CIR benchmark samples the zero-dof non-central chi-square
  via a Poisson mixture of Gammas (lines 171–173).

**TODO (Bruno):** be ready to (i) derive the cross-moment formula at line 29 by hand; (ii) derive the
non-central chi-square cumulants `kappa_n = 2^(n-1) n! lambda`; (iii) explain *why* more matched
moments need not monotonically reduce the pricing error.

### Q3 — basket COS (`Q3_basket_COS (1).py`)

- **`chi_coeffs(phi, a, b, N)` — lines 22–32.** 1D density cosine coefficients
  `chi_k = Re{ phi(omega_k) exp(-i omega_k a) }`, `omega_k = k pi/(b-a)` (lines 29–30), with the
  `k=0` term halved (line 31) to realise the primed summation.
- **`payoff_coeffs_2d(...)` — lines 34–54.** Payoff cosine coefficients `V_{k1,k2}`: builds the
  payoff matrix `P = max(w1 g1(y1) + w2 g2(y2) - K, 0)` on a dense grid (line 49) and contracts it
  with cosine/trapezoidal-weight matrices `C1, C2` (lines 52–53) as `C1^T P C2` (line 54). Trapezoidal
  weights at lines 45–46; normalisation `(2/(b1-a1))(2/(b2-a2))` at line 54.
- **`price_2dCOS(...)` — lines 56–63.** Assembles `e^{-rT} chi1^T V chi2` (line 63).
- **`cumulant_range(k1, k2, k4, L=12)` — lines 65–71.** **The truncation range.** Returns
  `[k1 - width, k1 + width]` with `width = L*sqrt(|k2| + sqrt(|k4|))` — **lines 70–71**. This is the
  COS-paper cumulant rule; `L=12` is the default.
- **Q3(a) characteristic functions — lines 79–80.** Normal log-price CFs
  `phi(om) = exp(i om mu - 0.5 sigma^2 T om^2)` for each marginal; means at lines 76–77.
- **Q3(a) ranges — lines 82–83.** `cumulant_range(mu, sigma^2 T, 0)` per marginal (a normal has
  `k1 = mean`, `k2 = variance`, `k4 = 0`).
- **Q3(b) `S2` characteristic function — `phi2_b`, lines 117–119.** CF of `S2(T) = c·Z`,
  `Z ~ chi'^2_0(lambda)`: `exp(lambda i z / (1 - 2i z))` with `z = om·c` (lines 118–119);
  `c_b`, `lam_b` at lines 114–116.
- **Q3(b) cumulants of `S2` — lines 122–124.** `k1 = c·lambda`, `k2 = c^2·4·lambda`,
  `k4 = c^4·192·lambda` (from `kappa_n = 2^(n-1) n! lambda` scaled by `c^n`).
- **Q3(b) ranges — lines 125–127.** `S1` range `cumulant_range(mu1_b, sigma1^2 T, 0)` (line 125);
  `S2` range `cumulant_range(k1_S2, k2_S2, k4_S2, L=12)` (line 126), then **clamped to be
  non-negative** `a2_b = max(a2_b, 0.0)` (line 127) because `S2 >= 0`.
- **Payoff maps — lines 84–85, 128–129.** `g = exp` for log-price state variables; `g2_b = identity`
  in Q3(b) because the `S2` state variable is the *level*, not the log.
- **Convergence loops — lines 88–104 (a), 131–145 (b).** Compare COS prices over
  `N = 8 … 64` against a converged `N = 256` reference.

## Design decisions I must justify

- **Cholesky correlation** (`Z2 = rho Z1 + sqrt(1-rho^2) Zc`) — Q1 lines 29, 116; Q2 line 152.
  **TODO (Bruno):** why this is exactly the 2×2 Cholesky factor.
- **Full truncation** of the CIR scheme — Q1 lines 120–121.
  **TODO (Bruno):** why truncation (not reflection) and what bias it introduces.
- **Reusing fine Brownian increments across grids** for the weak-error test — Q1 lines 144–169.
  **TODO (Bruno):** why this cleanly isolates discretization bias from MC noise.
- **Antithetic variates** in the Q2 benchmarks — Q2 lines 154–158, 176–179.
  **TODO (Bruno):** why antithetics reduce variance here and when they fail.
- **Choice of approximating families** (LN / shifted-LN / Johnson SU) — Q2 lines 78–139.
  **TODO (Bruno):** why each family is the natural one for 2 / 3 / 4 matched moments.
- **`rho = 0` factorisation** of the 2D density coefficients — Q3 lines 13–20, 60–63.
  **TODO (Bruno):** show why independence makes `c_{k1,k2} = chi_{k1} chi_{k2}` and what changes if `rho != 0`.
- **`L = 12` in the cumulant rule** — Q3 line 65, used at lines 82–83, 125–126.
  **TODO (Bruno):** justify `L = 12` (the paper often uses 8–10); relate to the bug below.
- **Trapezoidal quadrature for `V_{k1,k2}`** instead of a closed form — Q3 lines 34–54.
  **TODO (Bruno):** why no analytic `V_k` here (basket payoff couples the two state variables),
  and how `Ngrid` was chosen.

## Results and what they mean

**TODO (Bruno):** run the three scripts and fill in the actual numbers:
- Q1(a) price + 95% CI, and the fitted SE slope (should be ≈ `-0.5`, line 63).
- Q1(b) price + CI, the fitted weak order (≈ `1.0`, line 184), the fitted SE slope (line 209).
- Q2(a) and Q2(b): basket mean/std/skew/kurtosis, MC benchmark, and the 2/3/4-moment prices with
  absolute errors (printed at lines 196–198, 214–216) — explain why error generally falls with more
  moments and any exception.
- Q3(a)/(b): converged COS price and the error/ratio table (lines 98–104, 140–145) — explain whether
  convergence looks spectral (exponential) and how the ratios behave.

## The hardest question Fang could ask here — and my answer

**Most likely deep-dive (highest probability): the COS truncation range `[a,b]`.**
Fang co-invented COS; the cumulant truncation rule is her result, and this assignment had a real bug
there. She will go straight to **`Q3_basket_COS (1).py:65-71`** (`cumulant_range`) and its call
sites **`:82-83` (Q3a)** and **`:125-127` (Q3b)**.

What the code factually does: `cumulant_range` returns
`[k1 - L*sqrt(|k2| + sqrt(|k4|)), k1 + L*sqrt(|k2| + sqrt(|k4|))]` (`Q3_basket_COS (1).py:70-71`),
with `L = 12`. For a normal marginal `k4 = 0`, so the half-width is `L*sqrt(variance)`
(`:82-83`). For the CIR leg, the half-width uses the non-central chi-square cumulants
`k2 = 4 c^2 lambda`, `k4 = 192 c^4 lambda` (`:123-124`), and the lower end is clamped to `0`
(`:127`).

**The bug (special focus): a too-small `c2` made `[a,b]` too narrow at short maturities.**
The half-width scales like `sqrt(k2)`, and `k2` is the variance term — for a normal marginal
`k2 = sigma^2 T` (`:82-83`, `:125`), which **shrinks with `T`**. At short maturity `c2` is small, so
`width = L*sqrt(c2 + sqrt(c4))` (`Q3_basket_COS (1).py:70`) collapses and `[a,b]` becomes too narrow
to contain the support of the density / payoff, truncating mass and corrupting the price. The fix
lives at the range construction — the `cumulant_range` formula at **`:70`** and the `L` value at
**`:65`** (and the non-negativity clamp at `:127`).

> **TODO (Bruno): the *reasoning* of the fix — fill this in yourself.** Specifically:
> 1. What symptom did you see (wrong/unstable price, or error not converging) and at which `T`?
> 2. What exactly did you change — raise `L`, add the `sqrt(k4)` term, widen the floor, or change how
>    `c2` is fed in for short `T`? Point to the precise line you edited (`:65` `L=12`, `:70` the
>    width formula, or `:127` the clamp).
> 3. Why `L*sqrt(c2 + sqrt(c4))` (and not just `L*sqrt(c2)`) is the right safeguard when `c2` is tiny
>    but `c4 > 0`, and why a fixed wide interval is *not* a free lunch (more terms `N` needed for the
>    same accuracy, since COS error depends on both truncation and series length).

This is the single question most worth over-preparing.

## "Show me in your code where you do X" — anticipated spots

- **"…where you compute the truncation range `[a,b]`."** `Q3_basket_COS (1).py:65-71` (`cumulant_range`),
  called at `:82-83` (Q3a) and `:125-127` (Q3b, with the `max(a2_b, 0)` clamp at `:127`).
- **"…where a small `c2` makes `[a,b]` too narrow, and how you fixed it."** `Q3_basket_COS (1).py:70`
  (`width = L*sqrt(abs(k2) + sqrt(abs(k4)))`) and `:65` (`L=12`). **TODO (Bruno):** name the line you edited.
- **"…where you define the characteristic function."** Q3(a) `:79-80`; Q3(b) CIR leg `phi2_b` `:117-119`.
- **"…where you build the cosine density coefficients `chi_k`."** `chi_coeffs` `Q3_basket_COS (1).py:22-32`
  (note the `chi[0] *= 0.5` primed-sum term at `:31`).
- **"…where you build the payoff coefficients `V_{k1,k2}`."** `payoff_coeffs_2d` `:34-54` (assembly `:54`).
- **"…where the 2D price is assembled."** `price_2dCOS` `:56-63` (`chi1 @ V @ chi2` at `:63`).
- **"…where the cumulants of the CIR leg come from."** `Q3_basket_COS (1).py:122-124`; same moments in
  `Q2_moment_matching (1).py:39-53`.
- **"…where you correlate the Brownian motions."** `Q1_basket_MC (1).py:29` and `:116`.
- **"…where you do the Euler step for `S2`."** `Q1_basket_MC (1).py:120-121` (full truncation).
- **"…where you isolate the discretization bias."** `Q1_basket_MC (1).py:144-169`.
- **"…where you match 2 / 3 / 4 moments."** `price_2moments :78-89`, `price_3moments :91-107`,
  `price_4moments :109-139` in `Q2_moment_matching (1).py`.
- **"…where the MC benchmark uses antithetics."** `Q2_moment_matching (1).py:154-158` and `:176-179`.

---

## Corrector feedback (from the graded PDF)

> The returned PDF in this folder (`Computational_Finance_Assignment_2 (2) (1).pdf`) contains **no grader
> annotations** — no embedded scores or comments were found, so there is nothing to reconcile here. The
> COS truncation-range discussion above stands on its own. If a separately-graded copy exists, share it and
> I'll fold the comments in the same way as for the other three sets.
