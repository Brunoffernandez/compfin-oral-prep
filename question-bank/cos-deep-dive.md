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
2. How do you pick [a, b]? What breaks at short maturity, and how did you fix it in your assignment?
3. Why cosine series instead of a complex Fourier series?
4. What sets the convergence rate? Give a case where it is only algebraic.
5. Write the Heston characteristic function you used as ground truth. State the Feller condition.
6. How does COS extend to Barrier options? To American options?
7. Compare COS with Carr–Madan. Advantages and limitations.

## My answers (fill in / refine with Claude Code, then test yourself against them)

> Write your worked answers below as you master each one. Re-derive, don't paste.

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
> Key: F_k=(2/(b-a))Re{e^{-½(kπ/(b-a))²} e^{-ikπa/(b-a)}}; a=Φ^{-1}(1e-8), b=-a clips each tail at probability 1e-8.

## B. Why cosine

**B1.** Three reasons COS uses a cosine series, not a complex Fourier series. Be specific about each.
> Key: (i) even extension ⇒ real coefficients, real arithmetic, half the storage; (ii) A_k is literally Re{φ at grid frequency} — direct sampling from ch.f.; (iii) payoff coefficients V_k reduce to elementary χ_k, ψ_k (exp/poly × cos integrate in closed form).

## C. Pricing formula

**C1.** *(Core derivation.)* From P = e^{-rT}∫ V f dy, derive P ≈ e^{-rT} Σ'_{k=0}^{N-1} Re{φ(kπ/(b-a);x0) e^{-ikπa/(b-a)}} V_k. State the V_k definition and the sum–integral swap justification.
> Key: insert cosine expansion of f, swap Σ/∫ (uniform convergence, smooth f), define V_k=(2/(b-a))∫_a^b V cos(...)dy ⇒ P≈e^{-rT}(b-a)/2 Σ' A_k V_k; sub (b-a)/2·A_k = Re{φ e^{-ikπa/(b-a)}}; truncate at N.

**C2.** Where exactly does the ch.f. enter, and where does the spot x0 dependence live? Why does one set of {V_k} price the whole strike/spot grid?
> Key: φ enters only as the cosine coefficients of the density. x0 sits inside φ(·;x0); for Lévy/BS φ(u;x0)=φ_lvl(u)e^{iux0}, so only the cheap e^{iux0} factor changes across the grid — V_k computed once.

**C3.** What is the per-price computational cost of the COS sum? Does it call an FFT?
> Key: O(N) — a single cosine sum, no integration, no FFT.

## D. Payoff coefficients V_k

**D1.** *(Derive.)* Define χ_k(c,d)=∫_c^d e^y cos(ω_k(y-a))dy, ω_k=kπ/(b-a). Derive the closed form.
> Key: χ_k=Re{e^{-iω_k a}/(1+iω_k) [e^{(1+iω_k)y}]_c^d}; rationalise by (1-iω_k)/(1+ω_k²); χ_k = 1/(1+ω_k²)[cos(ω_k(d-a))e^d - cos(ω_k(c-a))e^c + ω_k sin(ω_k(d-a))e^d - ω_k sin(ω_k(c-a))e^c].

**D2.** Write ψ_k(c,d) including the k=0 case. Why must k=0 be special-cased?
> Key: k≠0: ψ_k=(b-a)/(kπ)[sin(ω_k(d-a))-sin(ω_k(c-a))]; k=0: ψ_0=d-c (ω_0=0 ⇒ integrand=1, and the 1/ω_k form is 0/0).

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
> Key: MC is O(N^{-1/2}); COS exponential ⇒ N~160 reaches ~1e-10 on Heston, vs thousands of FFT nodes for worse error.

## G. Greeks

**G1.** Why are Delta and Vega "free" in COS? Write the Delta sum.
> Key: S0/params enter only analytically via φ(·;x0); differentiate the finite sum termwise — no re-integration. Δ≈e^{-rT}Σ' Re{φ(kπ/(b-a)) e^{ikπ(x-a)/(b-a)} · ikπ/(b-a)} V_k/S0.

---

# Lecture 10 drill set (COS for barrier options)

Companion to `notes/Lecture10-notes.pdf`. Same cover-and-answer format.

## H. The pricing problem

**H1.** Define up-and-out vs up-and-in call. Why are there exactly 8 barrier types?
> Key: out = pays vanilla UNLESS barrier crossed (then 0); in = pays 0 UNLESS crossed (then vanilla). 8 = up/down × in/out × call/put.

**H2.** State in–out parity and give its two practical uses.
> Key: C_in + C_out = e^{-r(T-t)}E[(S_T-K)^+] (vanilla). Uses: (i) price the easier leg + vanilla, subtract for the other; (ii) free correctness check on a numerical barrier price.

**H3.** Write the two equivalent formulations (expectation and PDE). Where does the barrier enter the PDE?
> Key: V=e^{-r(T-t)}E_x[(α(e^{X_T}-K))^+ 1_{τ_B>T}]; or localized Feynman–Kac BS PDE on [a,b] with terminal payoff and ABSORBING boundary V(a,t)=V(b,t)=0. Barrier enters via the homogeneous Dirichlet BC, not the equation.

## I. Reflection principle (derive)

**I1.** *(Core.)* Derive P(τ_a ≤ T) = 2P(W_T ≥ a) and hence the density of the running maximum Ξ.
> Key: split P(τ_a≤T) by {W_T>a},{W_T≤a}; reflection ⇒ both halves equal ⇒ =2P(τ_a≤T,W_T≥a)=2P(W_T≥a) (since {W_T≥a}⊆{τ_a≤T}). So Ξ ~ |W_T|, P(Ξ≤a)=erf-type, p_Ξ(a)=√(2/πT) e^{-a²/2T} 1_{a≥0}.

**I2.** *(Core.)* Derive the joint density of (Ξ_0^T, W_T).
> Key: for b≤a, reflect after τ_a: P(Ξ≥a,W_T<b)=P(Ξ≥a,W_T>2a-b)=P(W_T>2a-b) (since 2a-b≥a). Differentiate -∂²/∂a∂b ⇒ p(a,b)=√(2/π)(2a-b)/T^{3/2} e^{-(2a-b)²/2T} 1_{a≥max(b,0)}.

**I3.** How do you get from standard BM to drifted BM (GBM log-price) results?
> Key: Girsanov change of measure — the drift appears as a Radon–Nikodym weight e^{θW_T-½θ²T}; reflect under the equivalent driftless measure then reweight.

## J. PDE routes

**J1.** State the method-of-images identity and the down-and-out call it produces. What is α?
> Key: if LV=0 then U(S,t)=S^{2α}V(B²/S,t) also solves it, α=½(1-2r/σ²). Subtract the weighted image to kill V on S=B: C_down-out=C_van(S,K) - (S/B)^{2α} C_van(B²/S,K).

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
> Key: Heston ⇒ 2-D state (log-stock, variance): 1-D COS in log-stock + numerical integration over variance, OR full 2-D COS for the joint density; cf is Heston's, Feller 2κv̄≥η². Continuous = M→∞ limit; extrapolate in Δt using the known O(√Δt) discrete-continuous bias.
