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
