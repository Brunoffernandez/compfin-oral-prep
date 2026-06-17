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
