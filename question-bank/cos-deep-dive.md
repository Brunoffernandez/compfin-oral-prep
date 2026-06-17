# COS deep-dive — the priority file

Fang invented COS. If she asks one hard question, it is probably here. Goal: I can do everything on the checklist **closed-book, on paper, out loud**.

## Mastery checklist (tick when you can do it cold)

- [ ] Derive the COS pricing formula for a European option from the Fourier-cosine expansion of the density.
- [ ] State where the characteristic function enters and why COS only needs the cf, not the density.
- [ ] Explain why a **cosine** expansion (even extension, real coefficients) rather than a full complex Fourier series.
- [ ] Write the payoff coefficients V_k for a call/put and explain the closed form.
- [ ] Choose the truncation range [a, b] from cumulants: a, b = c1 ± L·sqrt(c2 + sqrt(c4)). Explain each term.
- [ ] Explain the convergence rate: exponential for smooth densities, algebraic otherwise — and what kills it.
- [ ] **My Assignment 2 bug:** why a small c2 (short maturity) makes [a, b] too narrow to cover the spot grid, and exactly how I fixed it.
- [ ] COS for Heston: plug in the Heston cf; state the Feller condition.
- [ ] COS for Barrier options (Lecture 10) — how the method adapts.
- [ ] COS for American options (Lecture 9) — the approach used.
- [ ] COS vs Carr–Madan FFT: when and why COS wins.

## High-probability questions (have Claude Code grill me on these)

1. Derive the COS European call price. Where does the cf enter?

   **A.** Start from the discounted-expectation price in the log-state `y` (e.g. `y = ln(S_T/K)`):
   ```
   P(x0,T) = e^{-rT} ∫_R V(y,T) f(y|x0) dy.
   ```
   I do not know `f`, but I know its characteristic function `φ_{X_T}(t;x0) = E[e^{i t X_T}|x0] = ∫ e^{ity} f(y) dy`, i.e. `φ` is the Fourier transform of `f`.

   **Step 1 — truncate.** Pick `[a,b]` (cumulant rule, Q2) containing essentially all the mass and restrict the integral to `[a,b]`.

   **Step 2 — cosine-expand the density.** On `[a,b]` write the half-range cosine series (prime halves `k=0`):
   ```
   f(y) ≈ Σ'_{k≥0} A_k cos(kπ (y-a)/(b-a)),   A_k = (2/(b-a)) ∫_a^b f(y) cos(kπ(y-a)/(b-a)) dy.
   ```

   **Step 3 — A_k from φ (the engine).** Write `cos = Re{exp}`, pull out the phase `e^{-ikπa/(b-a)}`, and extend the integral to `R` (the *only* approximation — range truncation):
   ```
   A_k ≈ F_k = (2/(b-a)) Re{ φ(kπ/(b-a); x0) · exp(-ikπ a/(b-a)) }.
   ```
   The remaining `∫_R f(y) e^{i(kπ/(b-a))y} dy = φ(kπ/(b-a))` exactly. No integral survives.

   **Step 4 — payoff coefficients.** Define `V_k = (2/(b-a)) ∫_a^b V(y,T) cos(kπ(y-a)/(b-a)) dy`. For the call `V = K(e^y-1)^+` lives on `y≥0`, so
   ```
   V_k^call = (2/(b-a)) K [ χ_k(0,b) − ψ_k(0,b) ].
   ```

   **Step 5 — assemble.** Insert the expansion, swap `Σ`/`∫` (uniform convergence of the cosine series for smooth `f`), and use `V_k`:
   ```
   P ≈ e^{-rT} (b-a)/2 Σ'_{k=0}^{N-1} A_k V_k.
   ```
   Since `(b-a)/2 · A_k = Re{φ(kπ/(b-a);x0) e^{-ikπa/(b-a)}}`, this is
   ```
   P ≈ e^{-rT} Σ'_{k=0}^{N-1} Re{ φ(kπ/(b-a); x0) exp(-ikπ a/(b-a)) } V_k.
   ```

   **Where the cf enters:** in exactly one place — as the cosine coefficients of the density, `Re{φ · e^{-ikπa/(b-a)}}`. The spot dependence sits inside `φ(·;x0)`; for BS/Lévy `φ(u;x0)=φ_lvl(u) e^{iux0}`, so one set of `{V_k}` prices the whole spot/strike grid (only the cheap `e^{iux0}` changes). Cost `O(N)`, no integration, no FFT.

2. How do you pick [a, b]? What breaks at short maturity, and how did you fix it in your assignment?

   **A.** **Cumulant rule (Fang–Oosterlee):**
   ```
   [a,b] = [ c1 − L√(c2+√c4),  c1 + L√(c2+√c4) ],   L ∈ [8,12] (typ. 10),
   ```
   where `c1` = mean (centres the box), `c2` = variance (`√c2` is the natural width scale, so `L√c2` is an "L-sigma" box), `√c4` (fourth cumulant) fattens the box for heavy tails / kurtosis (zero for Gaussian), and `L` is the safety multiplier — larger `L` lowers the truncation floor but needs more terms.

   **BS cumulants** of `ln(S_T/K)`:
   ```
   c1 = ln(S0/K) + (r − ½σ²)T,   c2 = σ²T,   c3 = c4 = 0   ⇒   [a,b] = c1 ± Lσ√T.
   ```

   **What breaks as T→0:** `c2 = σ²T → 0`, so the half-width `L√(c2+√c4) → 0` and the box collapses toward the single point `c1`. With `c4=0` (Gaussian) there is no `√c4` floor to keep it open. Two failure modes: (i) the box gets too narrow to cover where `V·f` has mass; (ii) when pricing a whole grid of spots/strikes, a range centred by `c1` for one `(S0,K)` is centred away from other grid points, so the cosine reconstruction is evaluated where it is meaningless — large, erratic errors at short maturity.

   **Diagnostic signature** (this is the tell): the error *grows* as `T→0` and does *not* improve when `N` increases. That distinguishes a *range* error (a fixed accuracy floor) from a *series* error (curable by more terms).

   **Assignment-2 fix:** the truncation range was too narrow at short maturities because `c2` was tiny. I (i) raised `L` at short `T`, (ii) imposed a minimum half-width floor so `b−a` cannot collapse (equivalently kept a `√c4`-type term), and (iii) made sure the range was computed to cover the entire spot/strike grid actually being priced, not a single point. After that the error stopped growing as `T→0` and reverted to exponential decay in `N`.

3. Why cosine series instead of a complex Fourier series?

   **A.** Three reasons:
   - **(i) Real coefficients / real arithmetic.** The even extension of `f` on `[a,b]` kills every sine term, so the surviving `A_k` are real (`F_k` is literally a `Re{·}`). A full complex series carries twice the coefficients and complex bookkeeping for no gain.
   - **(ii) Direct sampling from φ.** The cosine coefficient *is* the real part of `φ` evaluated at the grid frequency `kπ/(b-a)`: `A_k = (2/(b-a)) Re{φ(kπ/(b-a)) e^{-ikπa/(b-a)}}`. The cosine basis is exactly the one whose coefficients are read off the cf in one line — no inversion integral.
   - **(iii) Payoff side closes in elementary functions.** `V_k` are integrals of (polynomial/exponential)×cos, which integrate to the closed forms `χ_k, ψ_k`. With a complex-exponential basis the call coefficients are not as clean. The whole method pairs the cosine coefficients of `f` (from `φ`) against those of `V` (closed form).

4. What sets the convergence rate? Give a case where it is only algebraic.

   **A.** Three error sources: (1) **range truncation** `[a,b]` — *fixed* once chosen, it sets the accuracy *floor* at which convergence saturates (exponentially small in the half-width for exponentially-decaying tails); (2) **series truncation** at `N` — governed by the decay of the cosine coefficients `A_k`; (3) **cf/model error** — feeds straight through.

   The rate in `N` is set by the **smoothness of `f`**:
   - `f` analytic in a strip / `f∈C^∞` with integrable derivatives ⇒ `A_k` decay **exponentially** ⇒ **exponential** convergence in `N` (machine precision in dozens–low hundreds of terms).
   - `f` with only `β` integrable derivatives ⇒ `A_k = O(k^{-(β+1)})` ⇒ only **algebraic** convergence. *Lack of smoothness is what kills the exponential rate.*

   **Algebraic case:** a low-regularity density — e.g. Variance-Gamma with small `ν` (the density develops a non-smooth peak / cusp), or a short-dated density approaching a Dirac, or near a jump/kink. There `A_k` decay only polynomially and you need many more terms.

5. Write the Heston characteristic function you used as ground truth. State the Feller condition.

   **A.** Heston: `dS = rS dt + √v S dW1`, `dv = κ(v̄ − v)dt + η√v dW2`, `d⟨W1,W2⟩ = ρ dt`, with `κ` mean-reversion speed, `v̄` long-run variance, `η` vol-of-vol, `ρ` correlation, `v0` initial variance. The characteristic function of the log-price `x_T = ln(S_T/S0)` (or `ln S_T`) is affine-exponential:
   ```
   φ(u;T) = exp( i u (ln S0 + rT)
               + (v0/η²) · ( (1 − e^{-DT})/(1 − G e^{-DT}) ) · (κ − iρηu − D)
               + (κ v̄/η²) · ( (κ − iρηu − D)T − 2 ln( (1 − G e^{-DT})/(1 − G) ) ) ),
   ```
   with
   ```
   D = √( (κ − iρηu)² + (u² + iu) η² ),
   G = (κ − iρηu − D) / (κ − iρηu + D).
   ```
   `D` and `G` come from solving the Riccati ODE for the variance factor of the affine system. (Equivalent "little-trap" form uses `G` rather than `g=1/G` to keep the complex log on the principal branch and avoid branch-cut discontinuities — the cf must be evaluated continuously or COS picks up `φ`-error that feeds straight through.)

   **Feller condition:** `2κv̄ ≥ η²`. It guarantees the CIR variance process stays strictly positive (never hits 0), which keeps the density well-behaved and `φ` clean; if violated, `v` can touch zero and the simulation/quadrature near `v=0` needs care.

6. How does COS extend to Barrier options? To American options?

   **A. Barrier (Lecture 10), discretely monitored on `t_1<…<t_M=T`.** Knock-out survival is a product of indicators `∏_m 1_{x_m<h}` (`h = ln(H/K)`). By the **Markov property** the joint density factorises into one-step transitions, so the `M`-dimensional integral nests into a **backward recursion**. Define continuation and option value at each date:
   ```
   c(x,t_{m-1}) = e^{-rΔt} ∫ v(y,t_m) f(y|x) dy,
   v(x,t_{m-1}) = R (knocked out) for x ≥ h,   = c(x,t_{m-1}) (alive) for x < h.
   ```
   Each continuation integral is *exactly* the European COS sum:
   ```
   ĉ(x,t_{m-1}) = e^{-rΔt} Σ'_k F_k(x) V_k(t_m),   F_k(x)=Re{φ(kπ/(b-a);x) e^{-ikπa/(b-a)}}.
   ```
   The new ingredient: the "payoff" `v(y,t_m)` is produced by the previous step, so its coefficients `V_k` are **propagated by backward induction**. Because `v` is piecewise at `h`, `V_k` splits at the barrier:
   ```
   V̂_k(t_m) = Ĉ_k(a,h,t_m) + e^{-r(T-t_{m-1})} (2R/(b-a)) Ψ_k(h,b),
   ```
   and `Ĉ_k` (inserting the COS continuation) becomes `Σ_j φ_lvl(jπ/(b-a)) V_j M_{k,j}` with an analytic coupling `M_{k,j}`. `M_{k,j}` splits into a **Hankel** part (`j+k`) and a **Toeplitz** part (`j−k`); Toeplitz/Hankel×vector = convolution = 3 FFTs by circulant embedding ⇒ `O(N log N)` per step, total `O((M−1)N log₂N)`. So — unlike European COS — the barrier method *does* use the FFT, because it must move the whole coefficient vector at every step. "In" barriers come from in–out parity. Continuous monitoring is the `M→∞` limit, recovered by Richardson extrapolation in `Δt` using the known `O(√Δt)` discrete-vs-continuous bias. Heston ⇒ 2-D state (log-stock, variance): 1-D COS in log-stock + numerical integration over variance, or full 2-D COS; Feller `2κv̄≥η²`.

   **B. American (Lecture 9).** Same backward-recursion idea but the decision is *early exercise* rather than a barrier knock-out. On a time grid, at each step the option value is `v(x,t_m) = max( g(x), c(x,t_m) )` — the larger of immediate exercise payoff `g` and the COS continuation value `c(x,t_m)=e^{-rΔt}Σ'_k F_k(x)V_k(t_{m+1})`. The early-exercise boundary `x*_m` is the point where `g = c`; below/above it (call vs put) the option is exercised. So each step (i) finds `x*_m` (a 1-D root-find on `g − c = 0`), (ii) splits the cosine coefficients of `v` at `x*_m` into a continuation region (cosine coeffs of `c`, computed from the previous `V_k` via the same analytic coupling integrals) and an exercise region (cosine coeffs of `g`, closed-form `χ_k/ψ_k`). This is the COS Bermudan pricer; the American price is obtained by Richardson extrapolation in the number of exercise dates. Structurally identical to the barrier recursion, with the moving boundary `x*_m` playing the role the fixed barrier `h` plays there.

7. Compare COS with Carr–Madan. Advantages and limitations.

   **A.** Both need only the characteristic function. Carr–Madan damps the call (`c_T(k)=e^{αk}C_T(k)`, `α>0`, to make it `L¹∩L²`), Fourier-transforms it in closed form in terms of `φ`, and recovers the price by an **inverse FFT** — i.e. a trapezoidal-type quadrature of an oscillatory integrand, `O(N log N)`.

   | | COS | Carr–Madan / FFT |
   |---|---|---|
   | Core op | one `O(N)` cosine sum, no integration | FFT quadrature, `O(N log N)` |
   | Free params | none (range from cumulants) | damping `α` must be tuned |
   | Convergence (smooth `f`) | exponential in `N` | algebraic (quadrature-limited) |
   | Terms for ~machine prec. | dozens–hundreds | thousands of nodes |
   | Greeks | analytic, same sum | extra transforms / finite differences |

   **COS wins** for smooth/piecewise-smooth densities with known `φ` and exponentially-decaying tails — essentially all European pricing under BS, Heston, and standard Lévy/AJD models — because it converges exponentially, needs no free parameter, and gives Greeks for free.

   **Limitations / be careful:** genuinely low-regularity densities (slow algebraic `A_k` decay), very short maturities, or fat tails, where `[a,b]` must be chosen carefully (Q2) and `N` raised; and any error in `φ` (e.g. a mis-evaluated Heston cf across the branch cut) feeds straight through. Carr–Madan's FFT also naturally returns a *whole strip of strikes* in one transform, which COS matches only because its `{V_k}` are strike-independent in log-moneyness.

## My answers (concise board versions — re-derive these out loud, don't read)

Compressed versions of the full answers above; expand any of them on demand.

1. **COS call price.** `P = e^{-rT}∫V f dy`; I don't know `f` but know its cf `φ`. Truncate to `[a,b]`, cosine-expand `f`, and the coefficients come straight off `φ`: `A_k ≈ (2/(b-a))Re{φ(kπ/(b-a))e^{-ikπa/(b-a)}}` (extend the coefficient integral to `R` — the only approximation). Pair against payoff coeffs `V_k=(2/(b-a))∫_a^b V cos(...)dy`; the integral of the product is `(b-a)/2 Σ'A_kV_k`, giving `P ≈ e^{-rT} Σ'_{k=0}^{N-1} Re{φ(kπ/(b-a);x0)e^{-ikπa/(b-a)}} V_k`. The cf enters only as the cosine coefficients of the density; `x0` lives inside `φ`, so one `{V_k}` prices the whole grid.

2. **`[a,b]`.** `c1 ± L√(c2+√c4)`, `L≈10`: `c1` centres, `√c2` is the width scale, `√c4` fattens for fat tails, `L` is the safety margin. BS: `c1=ln(S0/K)+(r-½σ²)T`, `c2=σ²T`, `c4=0`, so `[a,b]=c1±Lσ√T`. As `T→0`, `c2→0` so the box collapses (no `√c4` floor in the Gaussian case) → error *grows* as `T→0` and is *not* cured by more `N` (that signature = range, not series, error). Assignment-2 fix: raise `L` at short `T`, impose a minimum half-width floor, and size the range to the whole spot/strike grid, not one point.

3. **Why cosine.** Even extension ⇒ real `A_k`, real arithmetic, half the storage; `A_k` is literally `Re{φ}` at the grid frequency (direct cf sampling); payoff coeffs reduce to elementary `χ_k, ψ_k`. A complex series gives none of these cleanly.

4. **Convergence.** Three errors: range (fixed floor), series (decay of `A_k`), cf/model (passes through). Rate set by smoothness of `f`: analytic ⇒ exponential `A_k` decay ⇒ exponential in `N`; only `β` integrable derivatives ⇒ `A_k=O(k^{-(β+1)})` ⇒ algebraic. Algebraic case: VG with small `ν`, or short-dated density near a Dirac/kink.

5. **Heston cf + Feller.** Affine-exponential cf in `u` with `D=√((κ-iρηu)²+(u²+iu)η²)`, `G=(κ-iρηu-D)/(κ-iρηu+D)`, variance term `(v0/η²)((1-e^{-DT})/(1-Ge^{-DT}))(κ-iρηu-D)` plus the `(κv̄/η²)` drift term; use the "little-trap" form for a continuous branch. Feller: `2κv̄ ≥ η²` keeps `v>0` and `φ` clean.

6. **Barrier / American.** Both = backward recursion via Markov factorisation; each step is European COS `ĉ=e^{-rΔt}Σ'F_k(x)V_k(t_m)` with `V_k` propagated. Barrier: knock out by overwriting `v=R` above `h`, `V_k` splits at `h`, the coupling `M_{k,j}` is Hankel+Toeplitz ⇒ FFT, `O((M-1)N log₂N)`. American: `v=max(g,c)`, split `V_k` at the early-exercise boundary `x*_m` (root of `g-c`); Bermudan + Richardson in #exercise dates. The moving boundary `x*` plays the role of the fixed barrier `h`.

7. **COS vs Carr–Madan.** Both need only `φ`. CM damps the call (param `α`) and inverts by FFT quadrature — algebraic, `O(N log N)`, tunable `α`. COS is a single `O(N)` cosine sum, no integration, no free parameter, exponential convergence, free Greeks. COS wins for smooth densities with decaying tails; be careful for low-regularity / very short `T` / fat tails (set `[a,b]`, raise `N`), and any `φ` error feeds straight through.

---

# Lecture 6 drill set (European COS)

Companion to `notes/Lecture06-notes.pdf`. Each question has a terse answer key in the
collapsible note — cover it and answer out loud first. "Derive" means on paper, no notes.

## A. Density recovery

**A1.** Write the half-range cosine expansion of a density f on [a,b], with the prime convention. What does the prime mean and why is A0/2 the mean of f over [a,b]?
> Key: f(x)=Σ' A_k cos(kπ(x-a)/(b-a)), A_k=(2/(b-a))∫_a^b f cos(kπ(x-a)/(b-a))dx. Prime halves k=0. A0 = (2/(b-a))∫f = (2/(b-a))·(mass), and A0/2 over the constant basis function is the average height.

**A2.** *(Core derivation.)* Derive A_k ≈ (2/(b-a)) Re{ φ(kπ/(b-a)) exp(-ikπa/(b-a)) } starting from the coefficient integral. Identify the single approximation you make and where.
> Key: cos = Re of exp; pull out e^{-ikπa/(b-a)}; the remaining ∫_a^b f e^{i(kπ/(b-a))x}dx is extended to ℝ (THE approximation — range truncation) = φ(kπ/(b-a)). Everything else exact.

**A3.** Standard normal: φ(t)=e^{-t²/2}. Write F_k for a=-b symmetric. What range do the slides suggest and why (10^{-8} clip)?
> Key: substitute φ(t)=e^{-t²/2} at t=kπ/(b-a) into F_k, giving F_k=(2/(b-a))Re{e^{-½(kπ/(b-a))²} e^{-ikπa/(b-a)}}. The slides set a=Φ^{-1}(1e-8), b=-a, i.e. clip each tail at probability 1e-8 — symmetric because the standard normal is symmetric about 0. The Gaussian factor e^{-½(kπ/(b-a))²} makes F_k decay super-exponentially in k, which is the canonical exponential-convergence picture.

## B. Why cosine

**B1.** Three reasons COS uses a cosine series, not a complex Fourier series. Be specific about each.
> Key: (i) even extension ⇒ real coefficients, real arithmetic, half the storage; (ii) A_k is literally Re{φ at grid frequency} — direct sampling from ch.f.; (iii) payoff coefficients V_k reduce to elementary χ_k, ψ_k (exp/poly × cos integrate in closed form).

## C. Pricing formula

**C1.** *(Core derivation.)* From P = e^{-rT}∫ V f dy, derive P ≈ e^{-rT} Σ'_{k=0}^{N-1} Re{φ(kπ/(b-a);x0) e^{-ikπa/(b-a)}} V_k. State the V_k definition and the sum–integral swap justification.
> Key: insert cosine expansion of f, swap Σ/∫ (uniform convergence, smooth f), define V_k=(2/(b-a))∫_a^b V cos(...)dy ⇒ P≈e^{-rT}(b-a)/2 Σ' A_k V_k; sub (b-a)/2·A_k = Re{φ e^{-ikπa/(b-a)}}; truncate at N.

**C2.** Where exactly does the ch.f. enter, and where does the spot x0 dependence live? Why does one set of {V_k} price the whole strike/spot grid?
> Key: φ enters only as the cosine coefficients of the density, Re{φ e^{-ikπa/(b-a)}} — nowhere else. The spot x0 sits inside φ(·;x0); for Lévy/BS φ(u;x0)=φ_lvl(u)e^{iux0}, so across a strike/spot grid only the cheap e^{iux0} phase changes while the level cf φ_lvl is reused. The payoff coeffs V_k are strike-independent in the log-moneyness variable, so they are computed once and reused for the whole grid — that is the source of COS's grid efficiency.

**C3.** What is the per-price computational cost of the COS sum? Does it call an FFT?
> Key: O(N) per price — a single finite cosine sum of N terms, no numerical integration and no FFT. Each term is one cf evaluation times a precomputed V_k, so the whole price is essentially a dot product. This is the headline contrast with Carr–Madan (O(N log N) FFT quadrature) and with the discrete-barrier COS (which does need the FFT because it propagates the full coefficient vector at every step).

## D. Payoff coefficients V_k

**D1.** *(Derive.)* Define χ_k(c,d)=∫_c^d e^y cos(ω_k(y-a))dy, ω_k=kπ/(b-a). Derive the closed form.
> Key: χ_k=Re{e^{-iω_k a}/(1+iω_k) [e^{(1+iω_k)y}]_c^d}; rationalise by (1-iω_k)/(1+ω_k²); χ_k = 1/(1+ω_k²)[cos(ω_k(d-a))e^d - cos(ω_k(c-a))e^c + ω_k sin(ω_k(d-a))e^d - ω_k sin(ω_k(c-a))e^c].

**D2.** Write ψ_k(c,d) including the k=0 case. Why must k=0 be special-cased?
> Key: for k≠0, ψ_k(c,d)=(1/ω_k)[sin(ω_k(d-a))-sin(ω_k(c-a))]=(b-a)/(kπ)[sin(ω_k(d-a))-sin(ω_k(c-a))]. For k=0, ω_0=0 so the integrand cos(0)=1 and ψ_0=d-c. The k=0 case must be special-cased because the general 1/ω_k formula is 0/0 there (a removable singularity); in code a naive division by ω_0=0 gives NaN, so the k=0 term — which also carries the ½ from the prime — is set explicitly.

**D3.** In y=ln(S_T/K), give V_k for call and put. Why is the call interval [0,b] and the put interval [a,0]?
> Key: call V_k=(2/(b-a))K[χ_k(0,b)-ψ_k(0,b)] — payoff K(e^y-1)^+ lives on y≥0; put V_k=(2/(b-a))K[ψ_k(a,0)-χ_k(a,0)] — payoff K(1-e^y)^+ lives on y≤0.

## E. Truncation range (THE bug)

**E1.** State [a,b]=[c1 - L√(c2+√c4), c1 + L√(c2+√c4)]. Interpret each of c1, c2, √c4, L.
> Key: c1 mean (centres), c2 variance (√c2 width scale, L-sigma box), √c4 fattens box for heavy tails/kurtosis (0 for Gaussian), L safety multiplier (8–12, typ. 10).

**E2.** Give the BS cumulants of ln(S_T/K) and the resulting box. Which cumulants vanish?
> Key: c1=ln(S0/K)+(r-½σ²)T, c2=σ²T, c4=0 (and c3=0) ⇒ [a,b]=c1 ± Lσ√T.

**E3.** *(High priority.)* As T→0, what happens to [a,b] and why? Give the diagnostic signature distinguishing a range problem from a series problem. How do you fix it?
> Key: c2=σ²T→0 ⇒ half-width→0 ⇒ box collapses to ~c1; with c4=0 no floor keeps it open. Signature: error GROWS as T→0 and does NOT improve when N increases (range error is a floor, not curable by more terms). Fix: raise L at short T; keep √c4 / impose a minimum half-width floor; ensure the range covers the whole spot/strike grid actually priced, not one point.

## F. Convergence

**F1.** List the three error sources in the COS price and say which one sets the accuracy floor.
> Key: (1) range truncation [a,b] — FIXED once chosen, sets the floor; (2) series truncation at N — set by decay of A_k; (3) ch.f./model error feeds straight through. Convergence saturates at the range floor.

**F2.** What property of f gives exponential vs only algebraic convergence in N? Give a case where it is only algebraic.
> Key: smoothness/analyticity ⇒ A_k decay exponentially ⇒ exponential in N. Finite smoothness (β integrable derivatives) ⇒ A_k=O(k^{-(β+1)}) ⇒ algebraic. Algebraic case: density with low regularity / near a kink/jump, e.g. VG with small ν, or short-dated densities approaching a Dirac.

**F3.** COS vs MC convergence rate? Roughly how many terms for machine precision on Heston (cf slide 31)?
> Key: MC converges at O(N^{-1/2}) in the number of paths, whereas COS converges exponentially in the number of terms for smooth densities. On Heston (slide 31) N~160 terms reach ~1e-10 error, versus thousands of FFT nodes for worse error and longer CPU time. So COS reaches machine precision with N in the dozens to low hundreds — the gap is the whole selling point of the method.

## G. Greeks

**G1.** Why are Delta and Vega "free" in COS? Write the Delta sum.
> Key: S0 (via x=ln(S0/K)) and the model parameters enter the COS sum only analytically, through φ(·;x0)=φ(·)e^{iux}; so differentiation passes straight through the finite sum with no re-integration. Δ≈e^{-rT}Σ' Re{φ(kπ/(b-a)) e^{ikπ(x-a)/(b-a)} · ikπ/(b-a)} V_k/S0 (chain rule ∂x/∂S0=1/S0). Vega differentiates φ w.r.t. the variance parameter instead. The same {V_k} are reused, so Greeks cost essentially nothing extra — a structural advantage over quadrature/FFT pricers that need finite differences.

---

# Lecture 10 drill set (COS for barrier options)

Companion to `notes/Lecture10-notes.pdf`. Same cover-and-answer format.

## H. The pricing problem

**H1.** Define up-and-out vs up-and-in call. Why are there exactly 8 barrier types?
> Key: up-and-out call pays max(S_T-K,0) UNLESS the asset crosses B>S0 during [0,T], in which case it pays 0 (knocked out); up-and-in call pays 0 UNLESS B is crossed, in which case it becomes a vanilla call (knocked in). The 8 types = up/down × in/out × call/put (2×2×2). Each has a closed-form GBM price.

**H2.** State in–out parity and give its two practical uses.
> Key: holding knock-in and knock-out with the same (K,B,T) reproduces the vanilla, because exactly one of the two is alive at maturity: C_in + C_out = e^{-r(T-t)}E[(S_T-K)^+]. Use (i): price the easier leg (usually the knock-out) plus the vanilla, then back out the other by subtraction — cheaper and more stable than handling the in-condition directly. Use (ii): it gives a free correctness check on any numerical barrier price.

**H3.** Write the two equivalent formulations (expectation and PDE). Where does the barrier enter the PDE?
> Key: V=e^{-r(T-t)}E_x[(α(e^{X_T}-K))^+ 1_{τ_B>T}]; or localized Feynman–Kac BS PDE on [a,b] with terminal payoff and ABSORBING boundary V(a,t)=V(b,t)=0. Barrier enters via the homogeneous Dirichlet BC, not the equation.

## I. Reflection principle (derive)

**I1.** *(Core.)* Derive P(τ_a ≤ T) = 2P(W_T ≥ a) and hence the density of the running maximum Ξ.
> Key: split P(τ_a≤T) by {W_T>a},{W_T≤a}; reflection ⇒ both halves equal ⇒ =2P(τ_a≤T,W_T≥a)=2P(W_T≥a) (since {W_T≥a}⊆{τ_a≤T}). So Ξ ~ |W_T|, P(Ξ≤a)=erf-type, p_Ξ(a)=√(2/πT) e^{-a²/2T} 1_{a≥0}.

**I2.** *(Core.)* Derive the joint density of (Ξ_0^T, W_T).
> Key: for b≤a, reflect after τ_a: P(Ξ≥a,W_T<b)=P(Ξ≥a,W_T>2a-b)=P(W_T>2a-b) (since 2a-b≥a). Differentiate -∂²/∂a∂b ⇒ p(a,b)=√(2/π)(2a-b)/T^{3/2} e^{-(2a-b)²/2T} 1_{a≥max(b,0)}.

**I3.** How do you get from standard BM to drifted BM (GBM log-price) results?
> Key: Girsanov change of measure. A drifted BM W_T+θt under P is a driftless BM under an equivalent measure Q, with Radon–Nikodym derivative dP/dQ = e^{θW_T-½θ²T}. So I compute the reflection-principle result for driftless BM under Q, then reweight by that exponential to recover the drifted (GBM log-price) law. This is exactly what turns the driftless joint density of (Ξ,W_T) into the drifted one used in the closed-form barrier prices.

## J. PDE routes

**J1.** State the method-of-images identity and the down-and-out call it produces. What is α?
> Key: for the BS operator LV=V_t+rSV_S+½σ²S²V_SS-rV, if LV=0 then the image U(S,t)=S^{2α}V(B²/S,t) also solves LU=0, with α=½(1-2r/σ²). This is the BS analogue of reflecting a heat-equation solution across a wall. Subtracting the image with the right weight cancels the value on the barrier S=B, giving the down-and-out call C_down-out=C_van(S,K) - (S/B)^{2α} C_van(B²/S,K): the first term is the vanilla, the second removes exactly the paths that would have crossed B, evaluated at the mirror spot B²/S.

**J2.** *(Derive.)* Sine-series PDE route: what change of variables reduces the localized BS PDE to the heat equation, and why does the sine basis appear?
> Key: τ=½σ²(T-t), κ=2r/σ², V=e^{αx+βτ}U with α=-½(κ-1), β=-α²-κ, z=x-a ⇒ U_τ=U_zz on [0,b-a], U(0,τ)=U(b-a,τ)=0. Homogeneous Dirichlet BCs ⇒ sine series. Propagate modes by e^{-(nπ/(b-a))²τ}.

## K. COS for discrete barriers (the main event)

**K1.** *(High priority.)* Why does a discretely-monitored barrier become a BACKWARD RECURSION? Where does the Markov property enter?
> Key: survival = ∏_{m}1_{x_m<h}; Markov ⇒ joint density factorises into one-step transitions ⇒ the M-dim integral nests ⇒ backward recursion: c(x,t_{m-1})=e^{-rΔt}∫v(y,t_m)f(y|x)dy, then knock out: v=R for x≥h, =c for x<h.

**K2.** Write the COS step for the continuation value. How is it the European COS formula?
> Key: ĉ(x,t_{m-1})=e^{-rΔt}Σ'_{k} F_k(x)V_k(t_m), F_k(x)=Re[φ(kπ/(b-a);x)e^{-ikπa/(b-a)}], V_k=cosine coeffs of v(y,t_m). It IS Euro COS with v(·,t_m) playing the role of the payoff — except v's coefficients come from the previous step.

**K3.** *(Core.)* Why must V_k be propagated by backward induction, and how does the knock-out split V_k at h?
> Key: v is piecewise (R above h, ĉ below) ⇒ V̂_k(t_m)=Ĉ_k(a,h,t_m) + e^{-r(T-t_{m-1})}(2R/(b-a))Ψ_k(h,b). Ĉ_k inserts the COS continuation value ⇒ Ĉ_k=e^{-rΔt}Re[Σ'_j φ_Levy(jπ/(b-a))V_j(t_{m+1})M_{k,j}], with M_{k,j} an analytic coupling integral.

**K4.** *(High priority — contrast with Lecture 6.)* Why does the discrete-barrier COS use the FFT when European COS does not? Give the matrix structure and the complexity.
> Key: M_{k,j} splits into a Hankel part (depends on j+k) and Toeplitz part (depends on j-k). Toeplitz/Hankel × vector = convolution = 3 FFTs via circulant embedding ⇒ O(N log N) per step. Euro COS is a single O(N) sum needing no coefficient propagation; the barrier needs all {V_k} at every step. Total: O((M-1)N log₂N).

**K5.** State the truncation range for the barrier problem. What extra constraint beyond Lecture 6?
> Key: [a,b]=(c1+x0) ± L√(c2+√c4), x0=ln(S0/K), cumulants of the one-step increment. Extra: the barrier h=ln(H/K) must sit well INSIDE [a,b] or the split at h is meaningless; and range is fixed once but reused for all M steps.

**K6.** How is Heston handled? Continuous monitoring?
> Key: Heston has a 2-D state (log-stock, variance), so the one-step continuation integral is two-dimensional: either 1-D COS in the log-stock with numerical integration over the variance, or a full 2-D COS recovering the joint density. The characteristic function is Heston's (Lecture 7) and the Feller condition 2κv̄≥η² keeps it well-behaved. Continuous monitoring is the M→∞ (Δt→0) limit; in practice the discrete price converges to it and a Richardson-type extrapolation in Δt — using the known O(√Δt) discrete-vs-continuous barrier bias — recovers the continuous price.
