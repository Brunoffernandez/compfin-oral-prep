# Theory question bank

Filled in per cluster as I study. Format: question -> my short answer -> (gap?).

## Cluster 1 — Foundations / lattice / PDE
## Cluster 2 — Monte Carlo
## Cluster 3 — Fourier / COS

> COS-specific drilling lives in `cos-deep-dive.md`. This section holds the
> surrounding Fourier-family theory from Lecture 6 that Fang can ask "around" COS.

### Lecture 6 — the Fourier family (around COS)
1. State the continuous Fourier transform and its inverse. Which scaling/sign convention did the slides use, and why does the convention not matter for the method? -> -> (gap?)
2. Define the characteristic function φ_X(t). In what precise sense is it the "Fourier dual" of the density f_X? Write the inversion formula f_X(x) = (1/2π)∫ e^{-itx} φ_X(t) dt. -> -> (gap?)
3. Why are characteristic-function methods attractive at all? Name four models whose ch.f. is known in closed form but whose density is not. -> -> (gap?)
4. Write the DFT and inverse DFT. What does the FFT change about the cost, from what to what, and by what factorisation idea? Does COS use the FFT? -> -> (gap?)
5. Derive the half-range cosine series from the full Fourier series via the even extension. Why does the even extension kill the sine terms? -> -> (gap?)
6. Carr–Madan: why is the undamped call C_T(k) not square-integrable in log-strike k? What is the role of the damping factor e^{αk}, and what is the cost of having a free parameter α? -> -> (gap?)
7. Carr–Madan: ψ_T(v) = e^{-rT} φ_X(v-(α+1)i) / (α²+α-v²+i(2α+1)v). Why is it a selling point that ψ_T is expressible through the ch.f.? How is the price recovered, and by what numerical tool? -> -> (gap?)
8. Contrast COS and Carr–Madan on: core operation, free parameters, convergence rate for smooth f, and number of terms to reach machine precision. -> -> (gap?)
9. Give the BS log-price characteristic function and state the risk-neutral drift μ = r - ½σ². Where does the martingale condition fix μ? -> -> (gap?)

### Lecture 10 — barrier options (theory around COS)

> Deep COS-for-barrier drilling is in `cos-deep-dive.md` (sets H–K). These are the surrounding theory items.

10. Name the 8 barrier types and explain why exactly 8. State in–out parity and its uses. -> -> (gap?)
11. Write the barrier price as (i) a first-passage expectation and (ii) a localized Feynman–Kac PDE. How does the barrier enter the PDE? -> -> (gap?)
12. State and prove the reflection principle result P(τ_a ≤ T) = 2P(W_T ≥ a). Hence write the density of the running maximum. -> -> (gap?)
13. Derive the joint density of (running max, W_T). Why does the reflection at level 2a−b appear? -> -> (gap?)
14. Method of images: state U(S,t) = S^{2α}V(B²/S,t), α = ½(1−2r/σ²), and the down-and-out call it gives. -> -> (gap?)
15. Sine-series PDE route: what substitution turns the localized BS PDE into the heat equation, and why the sine (not cosine) basis? -> -> (gap?)
16. Why is a discretely-monitored barrier a backward recursion? Where does the Markov property enter, and why does the FFT reappear (vs European COS)? -> -> (gap?)

## Cluster 4 — Models (Heston / jumps)
## Cluster 5 — American options
## Cluster 6 — Exotics
