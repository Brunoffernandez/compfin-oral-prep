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

## Cluster 4 — Models (Heston / jumps)
## Cluster 5 — American options
## Cluster 6 — Exotics
