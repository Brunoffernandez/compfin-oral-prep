# Assignment-defense questions

Code-level questions for each assignment. Expect "open your file and explain line X."
Open the actual file when answering and give the line number back.

## Exercise set 1

Files:
- `assignments/exercise-set-1/exercise_1_computational_finance (2).py`
- `assignments/exercise-set-1/exercise_4_computational_finance (2).py`

### Exercise 1 — implied volatility

1. Open `exercise_1_computational_finance (2).py` and explain lines 13–14 of `C_bs`: what does the guard `if sigma <= 0 or T <= 0` return, and why is `max(S0 − K·e^{−rT}, 0)` the right fallback value rather than `0`?
2. In `implied_volatility_bisection` (lines 19–41), what does the function return on line 29, and under what condition? Explain in terms of the sign of `f_low·f_high`.
3. Line 34 has a compound stopping test `abs(f_mid) < tol or (sigma_high - sigma_low) < tol`. Which of the two conditions is in *price* units and which is in *vol* units? Why can the loop exit on either?
4. `Vega` (lines 43–49) returns `S0*np.sqrt(T)*norm.pdf(d1)`. Why is this exactly `∂C_BS/∂σ`, and why does it appear in the Newton denominator on line 66?
5. Explain line 58: `sigma_initial = np.sqrt((1/T)*(2*np.abs(np.log(S0/K)+ r*T)))`. What is this initial guess and what does the report claim it guarantees? Where in the lectures does it come from?
6. On line 66, `sigma -= diff/vega`. If `vega` were ~0 (deep OTM, short T), what would happen numerically, and which method (bisection vs Newton) is safe against this? Which line shows the safe behaviour?
7. Lines 94–96 build `IV_bisection` and `IV_Newton`. What column is passed as `C_mkt`, and why does that choice (mid vs bid/ask) directly feed your Exercise 1.3 discrepancy discussion?
8. Roughly how many bisection iterations are needed to shrink the bracket `[1e-6, 5.0]` below `tol = 1e-6`? Why is `max_iter = 200` (line 90) more than enough?

### Exercise 4 — Monte Carlo basket call

9. Open `exercise_4_computational_finance (2).py`. Explain lines 25–26: how do `W1 = Z1` and `W2 = rho*Z1 + np.sqrt(1-rho**2)*Z2` produce two Brownians with `dW1 dW2 = ρ dt`? Why is this the Cholesky factor of a 2×2 correlation matrix?
10. Compare line 29 (`drift r − 0.5σ²`, under Q) with line 65 (`drift r + 0.5σ1²`, under QS1). Why does the sign in front of the `½σ1²` term flip, and which result from Exercise 3(c) does that come from?
11. Line 71 returns `V = S0[0]*np.maximum(AT-K,0)/S1` with **no** `e^{−rT}` factor, whereas line 35 (under Q) **does** discount. Derive why the discount factor is absent under QS1.
12. What exactly do lines 38–39 (and 74–75) return, and why is `ddof=1` used in `np.std`? What would change if you used `ddof=0`?
13. Lines 118–122 construct the `1/√M` reference curves. What is the constant `c_Q = SEQ[0]*np.sqrt(values_M[0])` doing, and why does plotting `c_Q/np.sqrt(M)` test the CLT rate rather than assume it?
14. `np.random.seed(44)` is set on line 14 (Q) and line 50 (QS1). What is the consequence of reseeding identically in both functions for the *fairness* of the Q-vs-QS1 SE comparison? Is the convergence `O(1/√M)` either way?
15. Using Scenario-1 numbers (`σ1=σ2=0.2`, `ρ=0.9999`), compute `σ̃ = √(σ1²+σ2²−2ρσ1σ2)` and explain why this near-zero value is the reason the QS1 SE on line 75 is so small.

## Assignment set 1

Open the named file and answer at the line/function level. Point to the exact line, don't paraphrase the report.

1. **`2bCF (2).py:26`** — `fk = (2/(b-a)) * Im{ char(wk) * exp(-i wk a) }`. Explain term by term where this comes from. Why the imaginary part? Why the `2/(b-a)` prefactor (and not `1/(b-a)`)? Why does `k` start at 1 (`:22`) with no `k=0` term?
2. **`2bCF (2).py:30-31`** — the reconstruction loop. Write out the sum being evaluated and say why it approximates `f(x)` on `[a,b]`. What sets the accuracy: `N`, or the range `[a,b]=[-10,10]` (`:4-5`)?
3. **`2dCF (2).py` — function `phi_BS`** — it returns `exp(i w mu_y - 0.5 var_y w^2)` with `mu_y = x + (r - 0.5 sigma^2) T`. Why is this the characteristic function of `y = ln(S_T/K)` and not of `ln(S_T)`? Where does `x = x0 = log(S0/K)` enter?
4. **`2dCF (2).py` — cumulant range block** — `a = c1 - L*sqrt(c2 + sqrt(c4))` with `c1 = x0 + mu*T`, `c2 = T sigma^2`, `c4 = 0`, `L = 10`. Derive `c1` and `c2` as the first and second cumulants of the log-price. Why is `c4 = 0` legitimate for Black–Scholes? What breaks if `L` is too small?
5. **`2dCF (2).py` — functions `phi_k` and `chi_k`** — note the naming clash: the function called `phi_k` is the report's `psi_k` (integral of `sin`), and `chi_k` matches the report's `chi_k` (integral of `e^y sin`). Reconcile the code with your 2c derivation and confirm `V_k_put` pairs them correctly. Why does the function name `phi_k` collide awkwardly with the characteristic function `phi`?
6. **`2dCF (2).py` — `V_k_put`** — returns `(2K/(b-a)) * (-chi_k(...,a,0) + phi_k(...,a,0))`. Why are the integration limits `(a, 0)` and not `(a, b)`? Tie this to the put payoff being zero for `y > 0`.
7. **`2dCF (2).py` — `sin_put_price`** — final line is `exp(-rT) * dot(cf_part, Vk)`. Why `e^{-rT}` and not `e^{-r Delta t}` with a different `Delta t`? Why is the price a dot product of the CF part with the payoff coefficients (what theorem makes the product of two functions become a product of their sine coefficients)?
8. **`2eCF (2).py:46`** — `return (2/pi) * (im/ks) @ (1 - cosine).T`. Derive this from integrating the sine density term by term. Where do the `1/k` factor and the `2/pi` prefactor come from, and why is the integrated `sin` term `(1 - cos(...))`?
9. **`2eCF (2).py:14-15`** — fixed range `a=-2, b=2`. For `ln(S_T/S_0) ~ N(mu, sigma_aux^2)` with `mu ≈ -0.015`, `sigma_aux = 0.3`, how many standard deviations is `[-2,2]`? Is that wide enough? Why does the 2e error plateau at `3.67e-11` rather than reaching `1e-16` as 2d does?
10. **`3aCF (2).py:26`** — `S_T = S_0 * exp(drift*T + sigma1*Wt[:,None] + sigma2*Bi)` with `drift = r - 0.5*(sigma1^2 + sigma2^2)`. Derive this exact terminal law from the SDE (your 3a Ito derivation). Why is `0.5*(sigma1^2 + sigma2^2)` the right convexity correction, and why is no time-stepping needed?
11. **`3aCF (2).py:42`** — `q = np.quantile(L_T, 1 - alpha)` with `alpha = 1 - 0.95`. Given the assignment's definition `P(L_T >= q_alpha) <= alpha`, justify taking the `0.95` empirical quantile. What interpolation does `np.quantile` use, and could that matter for a discrete `L_T`?
12. **`3bCF (2).py:53`** — `ratio = exp(-(mu_shift/T)*W_q + mu_shiftsq)` with `mu_shiftsq = mu_shift^2/(2T)`. Derive this `p/q` from two Gaussians `p~N(0,T)`, `q~N(1.5,T)` and confirm it equals `exp(-1.5 w + 1.125)` at `T=1`. Why is only `W` reweighted and not the `B_i` (`:44`)?
13. **`3cCF (2).py:54`** — `ratio = sqrt(2)*exp((-W_q^2 - 3 W_q + 2.25)/(4T))`. Derive this from `p~N(0,T)`, `q~N(1.5,2T)`. Where does the `sqrt(2)` prefactor come from? Explain why this mean+var shift is *less* efficient for the 95% quantile than the pure mean shift in 3b.
14. **`3bCF (2).py:20-34` / `3cCF (2).py:20-34`** — `weighted_quantile`: `cumsum(w_sorted)/sum(w_sorted)` then `searchsorted(cdf, q)`. Why must you sort by `values` first and carry the weights along? Why does 3a use `np.quantile` but 3b/3c need this custom weighted version — and does that estimator mismatch bias the efficiency comparison against 3a?

## Exercise set 2

Files:
- `assignments/exercise-set-2/exercise1_def (2).py` (LSM / Longstaff–Schwartz)
- `assignments/exercise-set-2/exercise2_def (2).py` (FTCS finite differences)

### Exercise 1 — LSM

1. **`exercise1_def (2).py:96-127`** — walk the backward LSM loop out loud. Which line builds the discounted continuation target `Y`, which applies the ITM mask, which fits the regression, which makes the exercise decision, and which zeroes the later cash flows?
2. **`:99-101`** — `Y` is the sum of all future cash flows discounted by `exp(-r*dt*(u-i))`. Why discount to time `i+1` (not to `0`)? What would change in the comparison at `:117-120` if you discounted to `0` instead?
3. **`:102-104`** — the ITM mask `S[:,i+1] < K`. Why does Longstaff–Schwartz regress *only* on in-the-money paths? What bias appears if you include OTM paths?
4. **`:107-112`** — degree-2 monomial pipeline; you reported `E[Y|X] = -1.06999 + 2.98341 X - 1.81358 X^2` at `t=2`. Reproduce how `a0,a1,a2` are fit and what `X`, `Y` are at that step.
5. **`:122-127`** — the exercise rule sets `C[j,i]` to the intrinsic value and zeroes `C[j,i+1:]`. Why must all later cash flows be zeroed once you exercise? What does the stopping matrix at `:131` then represent?
6. **`:147-156`** — American vs European price. Why does the European price use only the terminal column `C_european` while the American price sums each path's single realized cash flow?
7. **`:177-178`** — antithetic paths (`Z` then `-Z`). State the covariance argument for why this reduces variance for this payoff. Does the s.e. `std(cashflow)/sqrt(N)` at `:258` remain correct when the `N` draws are antithetically paired (not independent)?
8. **`:185-191`** — `laguerre_basis` uses `x = S/K` and weights `exp(-x/2)`. Why normalise by `K`, and what numerical problem (underflow) does `exp(-x/2)` with `x=S/K` avoid that raw monomials in `S` would hit for `S∈[36,44]`?
9. **`:257` vs `exercise2_def (2).py:223`** — one uses `abs(american-european)`, the other the *signed* difference for the early-exercise value. Which matches the paper's "early-exercise value" column, and can LSM-American ever dip below European by Monte-Carlo noise?

### Exercise 2 — FTCS

10. **`exercise2_def (2).py:35-40`** — derive the explicit evolution matrix `F = (1 - r k) I + 0.5 k σ² / h² · T2 + k (r - 0.5 σ²)/(2h) · T1` from the Black–Scholes PDE written in `m = log S`. Identify which term is the reaction, which the diffusion, which the advection.
11. **`:29-33`** — `L = 2 log K + 2`, `Nx = 1000`, `Nt = 40000*T`. Why center the grid at `log K` (`:43`)? What is the analogy between this domain truncation and the COS `[a,b]` range bug you hit in Assignment 2?
12. **`:45-46` and `:51`** — initial condition `max(K - e^m, 0)` and the boundary term `p[0]` scaled by `K·exp(-r·time2mat)`. What Dirichlet boundary condition does `p[0]` enforce at the deep-ITM edge, and why is no correction added at the high-`S` boundary?
13. **`:105`** — `U = np.maximum(U, intrinsic)`, "the single line that makes it American". Why is projecting onto the payoff after each explicit step a valid (operator-splitting / explicit-penalty) treatment of the free boundary, and what accuracy does it cost versus a proper LCP/PSOR solve?
14. **Stability:** with `Nx=1000`, `Nt=40000·T`, worst-case `σ=0.4`, compute the diffusion number `0.5 σ² k / h²` and check it is `≤ 1/2`. Is the scheme stable? Why might the author have picked `Nt` so large (stability vs accuracy)? Can the `T1` advection term cause oscillations even when the diffusion bound holds?
15. **`:54` / `:107`** — `np.interp` reads the price at `log(S0)`. Your FD-European prices are systematically `~1e-4` *below* Black–Scholes (every difference negative). Is the consistent sign due to the explicit scheme, the truncated domain, or the interpolation? Defend your pick.

## Assignment set 2

Files:
- `assignments/assignment-set-2/Q1_basket_MC (1).py`
- `assignments/assignment-set-2/Q2_moment_matching (1).py`
- `assignments/assignment-set-2/Q3_basket_COS (1).py`

### Q3 — basket COS (highest-priority: Fang invented COS)

1. **`Q3_basket_COS (1).py:22-32`** — `chi_coeffs`: `chi_k = Re{ phi(omega_k) exp(-i omega_k a) }`, `omega_k = k pi/(b-a)`, with `chi[0] *= 0.5` at `:31`. Explain term by term where this comes from, and why the `k=0` term is halved (the primed sum).
2. **`:34-54`** — `payoff_coeffs_2d` builds `V_{k1,k2}` as `C1^T P C2` by trapezoidal quadrature on a dense payoff grid. Why is there *no* closed-form `V_k` here, unlike the 1D European call/put (where `χ_k, ψ_k` are analytic)? What couples the two state variables?
3. **`:56-63`** — `price_2dCOS` assembles `e^{-rT} · chi1^T V chi2`. What makes the 2D integral collapse to this triple product of coefficient vectors, and where does the `rho=0` independence assumption enter (the density coefficients factorising `c_{k1,k2}=chi_{k1} chi_{k2}`)?
4. **`:65-71`** — `cumulant_range` returns `[k1 - width, k1 + width]` with `width = L*sqrt(|k2| + sqrt(|k4|))`, `L=12`. Interpret each of `k1`, `k2`, `sqrt(k4)`, `L`.
5. **`:82-83`** — Q3(a) calls `cumulant_range(mu, sigma^2 T, 0)` per marginal. For a normal log-price, what are `k1`, `k2`, and why is `k4 = 0`?
6. **THE BUG (over-prepare this).** `:70` — `width = L*sqrt(|k2| + sqrt(|k4|))`. As `T→0`, `k2 = sigma^2 T → 0`, so `width` collapses and `[a,b]` becomes too narrow to contain the density/payoff support. Show me the exact line where this happens. **TODO (Bruno):** what symptom did you see and at which `T`; and exactly what did you change — `L` at `:65`, the width formula at `:70`, or the non-negativity clamp at `:127`? Why is `sqrt(c2 + sqrt(c4))` (not just `sqrt(c2)`) the right safeguard, and why is a fixed wide interval not a free lunch?
7. **`:117-119`** — `phi2_b` is the CIR-leg characteristic function `exp(lambda·i·z/(1-2·i·z))`, `z = om·c`. Where does this come from (the zero-dof non-central chi-square law of `S2(T)=c·Z`)?
8. **`:122-127`** — CIR cumulants `k1 = c·lambda`, `k2 = 4 c^2 lambda`, `k4 = 192 c^4 lambda`, and the range is clamped `a2 = max(a2, 0)` at `:127`. Why is the clamp needed for the square-root process?

### Q1 — basket Monte Carlo

9. **`Q1_basket_MC (1).py:29` and `:116`** — `Z2 = rho*Z1 + sqrt(1-rho^2)*Zc`. Show this is exactly the 2×2 Cholesky factor of the correlation matrix, i.e. that `Corr(Z1,Z2)=rho`.
10. **`:120-121`** — Euler step for the CIR leg with full truncation `S2p = max(S2,0)` inside both drift and diffusion. **TODO (Bruno):** why full truncation rather than reflection, and what bias does it introduce? Why is the Q-drift `r·S2` (not the physical `kappa(theta-S2)`)?
11. **`:144-169`** — the weak-error test reuses the *same* fine Brownian increments across all coarse grids. Why does reusing increments cleanly isolate the discretization bias from the Monte-Carlo noise?

### Q2 — moment matching

12. **`Q2_moment_matching (1).py:20-29`** — `lognormal_cross` returns `E[S1^j S2^m]` via `exp(mean + 0.5 var)`. Derive this cross raw moment for two correlated log-normals by hand.
13. **`:39-53`** — `cir_S2_rawmoments` uses cumulants `kappa_n = 2^{n-1} n! lambda` then a raw-from-cumulant recursion. Derive the non-central chi-square (zero-dof) cumulants `kappa_n`.
14. **`:78-139`** — `price_2moments` (log-normal), `price_3moments` (shifted log-normal via skewness inversion with `brentq`), `price_4moments` (Johnson SU via `least_squares`). **TODO (Bruno):** why is each family the natural choice for 2/3/4 matched moments, and why need not matching more moments monotonically reduce the pricing error?
