# THEORY cheat-sheet — Computational Finance (WI4151)

One condensed block per lecture: **core idea**, **key results**, **the line of reasoning**.
No derivations — those live in `notes/Lecture<NN>-notes.pdf`. COS (L6, L10) is the centre of gravity.

Notation: `x = ln(S/K)` or `ln S` (log-state); `φ` = characteristic function (cf); `[a,b]` = COS truncation
range; `Σ'` = first term halved; cumulants `c1,c2,c4`; `N(·)` = standard normal CDF.

---

## Cluster 1 — Foundations / lattice / PDE (L1–L3, L5)

### Lecture 01 — Asset classes, no-arbitrage, the Wiener process
- **Core:** the pricing primitives — discounting, no-arbitrage replication, and the stochastic model of `S`.
- **Key results:** bank account `M(t)=e^{rt}`, discount `e^{-r(T-t)}`; covered interest-rate parity `(1+i_s)=(F/S)(1+i_c)`; payoffs `(S_T-K)^+`,`(K-S_T)^+` (kink at `K`); one-step hedge `Δ=ΔV/ΔS`, price `=E^Q[payoff]` (physical `p` irrelevant); put–call parity `C+Ke^{-r(T-t)}=P+S`; bound `C≥(S-Ke^{-r(T-t)})^+` ⇒ American call = European; GBM `S_t=S_0 e^{(μ-½σ²)t+σW_t}`, `ln(S_T/S_0)~N((μ-½σ²)T,σ²T)`; Wiener: `E[dW]=0,(dW)²=dt,[W]_t=t`.
- **Reasoning:** price = cost of the replicating hedge ⇒ risk-neutral expectation; `(dW)²=dt` forces Itô calculus; GBM is the baseline the whole course perturbs.

### Lecture 02 — Itô, the BS PDE, risk-neutral valuation, Feynman–Kac
- **Core:** three equivalent views of the European price — hedging PDE, `Q`-expectation, Feynman–Kac bridge.
- **Key results:** Itô `dg=(g_t+μg_x+½σ²g_xx)dt+σg_x dW`; BS PDE `V_t+rSV_S+½σ²S²V_{SS}-rV=0`; under `Q` drift `μ→r`, `σ` unchanged; discounted price `e^{-rt}V` is a `Q`-martingale; closed form `C=S_0N(d1)-Ke^{-rT}N(d2)`, `d_{1,2}=[ln(S_0/K)+(r±½σ²)T]/(σ√T)`, `N(d2)=Q(S_T>K)`.
- **Reasoning:** delta-hedge removes `dW` ⇒ portfolio earns `r` ⇒ PDE; `μ` cancels in hedging, so the real drift never enters the price.

### Lecture 03 — Implied volatility
- **Core:** invert BS price for the one unknown `σ`; read the market's view off option prices.
- **Key results:** four knowns `(S,K,T,r)`, unknown `σ`; vega `=S√T φ(d1)>0` ⇒ price strictly increasing in `σ` ⇒ **unique** IV; admissible price interval bounds existence; **bisection** (linear, robust) vs **Newton** (quadratic, divide-by-vega blows up deep OTM) ⇒ globalise by seeding at the price-curve inflection point; put and call share one IV (parity); smile/skew in `K`, term structure in `T`.
- **Reasoning:** monotonicity (vega>0) guarantees a unique root; a non-flat IV surface is the empirical proof that constant-σ BS is wrong — motivates Heston/jumps.

### Lecture 05 — Binomial trees & finite differences
- **Core:** two lattice/grid pricers and the fact that a binomial tree *is* an explicit FD scheme.
- **Key results:** CRR `u,d,p` from matching mean+variance of the log-return to BS; risk-neutral backward induction; convergence `O(1/M)`, non-monotone (strike-straddling). FD on the heat equation: FTCS (explicit, stable only if `ν=k/h²≤½`), BTCS (implicit, unconditionally stable), Crank–Nicolson (`O(k²+h²)`); von Neumann amplification `ξ_FTCS=1-4ν sin²(βh/2)`; BS→heat via `x=ln S`, `V=e^{-rτ}W`; binomial = FTCS with the `h²=σ²k` coupling collapsing the centre node.
- **Reasoning:** explicit schemes are cheap but the CFL bound forces `k=O(h²)`; work in `x=ln S` for constant coefficients and to tame the large-`S` diffusion weight (same domain-truncation lesson as the COS `[a,b]`).

---

## Cluster 2 — Monte Carlo (L4)

### Lecture 04 — MC integration, SDE simulation, variance reduction
- **Core:** unbiased sampling estimator with dimension-independent `O(N^{-1/2})` error, plus how to make it faster.
- **Key results:** `Var(X̄_N)=σ²/N`, SE `=s_N/√N`, CLT confidence interval; QMC reaches `~(log N)^d/N` (Koksma–Hlawka: error ≤ discrepancy × variation); Euler–Maruyama (weak 1, strong ½), Milstein adds `½bb'[(ΔW)²-h]` (strong 1); variance reduction — antithetic (`±Z`), control variate (optimal `c*=Cov/Var`, factor `(1-ρ²)`), importance sampling (drift shift / likelihood ratio).
- **Reasoning:** MC wins in high dimension because the rate is `d`-free; it is the slow benchmark that COS/FFT beat for smooth low-dimensional European problems.

---

## Cluster 3 — Fourier / COS ★ priority (L6, L10)

### Lecture 06 — The Fourier family & the COS method
- **Core:** compute `e^{-rT}E[payoff]` using only the cf, by expanding the density in a cosine series whose coefficients come straight from `φ`.
- **Key results:** cf `φ_X(t)=E[e^{itX}]` is the Fourier dual of the density; density coefficients `A_k=(2/(b-a))Re{φ(kπ/(b-a))e^{-ikπa/(b-a)}}` (only approximation = range truncation); **European COS price** `P≈e^{-rT}Σ'_{k=0}^{N-1} Re{φ(kπ/(b-a);x0) e^{-ikπa/(b-a)}} V_k`; payoff coefficients `V_k` closed-form via `χ_k,ψ_k` (call `(2K/(b-a))[χ_k(0,b)-ψ_k(0,b)]`); **cumulant range** `[a,b]=c1±L√(c2+√c4)`, `L≈8–12`; cost `O(N)`, **no FFT, no quadrature**; exponential convergence for smooth densities (saturates at the range floor).
- **Reasoning:** cosine basis ⇒ real coefficients read off `φ` in one line, and `V_k` closes in elementary functions; the only error you control is `[a,b]` (range) and `N` (series). **Short-maturity trap:** `c2=σ²T→0` collapses `[a,b]`; error then *grows* as `T→0` and is *not* cured by more terms — fix by raising `L` / flooring the half-width / covering the whole grid (the Assignment-2 bug).

### Lecture 10 — Barrier options
- **Core:** payoff × survival indicator; analytic under GBM, and a COS *backward recursion* for discrete monitoring.
- **Key results:** 8 types (up/down × in/out × call/put); in–out parity `C_in+C_out=`vanilla; expectation form with `1_{τ_B>T}` vs localized BS PDE with **absorbing** boundaries `V(a)=V(b)=0`. GBM analytics rest on the **reflection principle** (max density `p_Ξ(a)=√(2/πT)e^{-a²/2T}`, joint density of `(W_T,Ξ)`), giving closed-form barrier prices; PDE routes = method of images `U=S^{2α}V(B²/S)` and a sine-series heat solution. **Discrete COS:** Markov ⇒ the survival product factorises ⇒ backward recursion; at each monitoring date `ĉ=e^{-rΔt}Σ'F_k(x)V_k`, then knock-out splits `V_k` at the barrier `h` into a payoff piece (`Ψ_k`) and a continuation piece (`Ĉ_k`); the coupling `M_{k,j}` is **Hankel + Toeplitz** ⇒ each step is a convolution done by **FFT**; total cost `O((M-1)N log₂N)`.
- **Reasoning:** the barrier enters only through the boundary/indicator, not the dynamics. Key contrast: European COS uses no FFT, but the discrete barrier must propagate all `{V_k}` every step — a structured matrix-vector product — so the FFT returns.

---

## Cluster 4 — Models (L7, L8)

### Lecture 07 — Heston stochastic volatility
- **Core:** add a mean-reverting variance with its own Brownian shock; price by plugging the affine cf into COS.
- **Key results:** `dS=rS dt+√v S dW1`, `dv=κ(v̄-v)dt+η√v dW2`, `d⟨W1,W2⟩=ρ dt`; CIR variance ~ noncentral χ²; **Feller** `2κv̄≥η²` keeps `v>0`. Not affine in `(S,v)` but **is** affine in `(ln S,v)` ⇒ cf `φ=exp(α(τ,u)+β(τ,u)v0+iu ln S0)` from **Riccati ODEs** (closed form with `D=√((κ-iρηu)²+η²(u²+iu))`, `G`); the **little-Heston trap** (branch cut of complex `log/√`) fixed by the right grouping. Simulation: Euler can make `v<0` (truncation/reflection/log-`v` fixes); **Broadie–Kaya** exact via noncentral-χ² `v` + cf of integrated variance.
- **Reasoning:** Heston is the headline COS use case — one analytic cf prices the whole smile; `ρ<0` and small `c2` make the short-maturity range trap worse.

### Lecture 08 — Jumps and affine jump-diffusion
- **Core:** add discontinuities; the cf still closes, so COS still works.
- **Key results:** Poisson `P(N=k)=e^{-λt}(λt)^k/k!`, mean=var=`λ`; compensated `N_t-λt` is a martingale; **compound-Poisson cf** `exp(tλ(ν̂(u)-1))` (Lévy–Khintchine exponent); Merton drift correction `μ=r-λE[J]` (compensator); **Merton** (lognormal-jump) and **Kou** (double-exponential, `η1>1`) cfs; non-local **PIDE**; **AJD** (Duffie–Pan–Singleton) cf `=exp(α+β·x)` from Riccati ODEs with the `(θ(β)-1)` jump-transform term; BS recovered as a no-jump AJD.
- **Reasoning:** the `(θ-1)`/compensator motif recurs (compensated Poisson, drift correction, AJD ODE); the only thing COS needs from any of these models is `φ` evaluated at `kπ/(b-a)` — heavy tails (`c4>0`) widen `[a,b]`.

---

## Cluster 5 — American options (L9)

### Lecture 09 — Early exercise
- **Core:** optimal stopping / free boundary; price the Bermudan by backward recursion, extrapolate to American.
- **Key results:** continuation vs stopping region, smooth pasting at `S*(t)`; **American call = European call** (non-dividend; dominating-strategy + parity bound), put breaks it (`Ke^{-r(T-t)}<K`); put as **LCP/obstacle** `(v-Λ)≥0, Lv≤0, (v-Λ)Lv=0`. Methods on the shared `v=max(Λ,c)` recursion: binomial (one `max` line differs from European), FD + **PSOR** (project inside each sweep), **LSM** (regress discounted future CF on a basis over ITM paths; low-biased, foresight bias ⇒ out-of-sample), **COS/Bermudan** (split `V_k` at the early-exercise point `x_n*` found by Newton, `C_k` via FFT, `O(NK log K)`); **Richardson** Bermudan→American.
- **Reasoning:** all four methods compute the same continuation value `E[v(t_{n+1})|x]` differently; the COS range caveat bites *per step* (`c2=σ²Δt`).

---

## Cluster 6 — Exotics overview (L11)

### Lecture 11 — Exotics map
- **Core:** survey of path-dependent / multi-asset payoffs and which numerical method fits each.
- **Key results:** **Asian** (avg) — arithmetic has no closed form (MC + geometric control variate; SV via Fouque–Han 3-D PDE, Vecer numeraire reduction 3D→1D); **digital/binary** = `e^{-rT}N(d2)`, but pin-risk / delta blow-up near `K` at expiry; **basket / worst-of** — correlation-driven, MC or moment-matching / 2-D COS; **cliquet** — forward-starting capped/floored returns (forward-skew sensitive); **barrier** — see L10.
- **Reasoning:** method follows structure — averaging/multi-asset/high-dimension ⇒ MC; smooth low-dimensional with a known cf ⇒ COS; the digital's discontinuous payoff is the recurring hedging-difficulty trap.

---

### The through-line (say it in one breath)
Every price is `e^{-rT}E^Q[payoff]`. If the **density** is known (GBM) → closed form / PDE / trees. If only the **cf** is known (Heston, jumps, AJD) → **COS**: expand the density in a cosine series with coefficients `Re{φ·e^{-ikπa/(b-a)}}`, pair against closed-form payoff coefficients `V_k`, sum `O(N)` terms; pick `[a,b]=c1±L√(c2+√c4)` and watch the short-maturity collapse. Early exercise (L9) and discrete barriers (L10) reuse COS as a **backward recursion**; high-dimensional/averaging payoffs (L11) fall back to **Monte Carlo** (L4).
