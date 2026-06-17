# Theory question bank

Filled in per cluster as I study. Format: question -> my short answer -> (gap?).

## Cluster 1 — Foundations / lattice / PDE

### Lecture 02
1. Derive Ito's lemma heuristically: why does the second-order term in g(t,X) survive while the others vanish? -> -> (gap?)
2. Apply Ito to g = ln S under dS = mu S dt + sigma S dW. Where does the -sigma^2/2 come from, and what is its sign relation to Jensen? -> -> (gap?)
3. Walk through the delta-hedging derivation of the Black-Scholes PDE. At which exact step is Delta = V_S forced, and why? -> -> (gap?)
4. In that derivation, mu appears in dV but not in the final PDE. Show precisely the cancellation that removes it. -> -> (gap?)
5. State the BS PDE, its order/type, and its terminal condition. Why is it solved backward in time? -> -> (gap?)
6. Define a risk-neutral measure Q. Starting from dS = mu' S dt + sigma S dW^Q, prove that the martingale property of e^{-rt}S_t forces mu' = r. -> -> (gap?)
7. Under the change from P to Q, the drift goes mu -> r but sigma is unchanged. Why must sigma be preserved (think equivalence / quadratic variation)? -> -> (gap?)
8. State Feynman-Kac and sketch its proof. What is the role of the discounted process Y_s and where is the PDE used? -> -> (gap?)
9. Explain how Feynman-Kac shows the PDE approach and the martingale approach give the same price. State the equivalence "drift = 0 <=> discounted price is a Q-martingale". -> -> (gap?)
10. Derive C_0 = e^{-rT} E^Q[(S_T - K)^+] down to S_0 N(d1) - K e^{-rT} N(d2). What measure-change / square-completion produces the shift from d2 to d1? -> -> (gap?)
11. Interpret N(d2) and N(d1) probabilistically. Which one equals Q(S_T > K)? -> -> (gap?)
12. Derive put-call parity from a static replication argument (not from the BS formula). Why is parity model-free? -> -> (gap?)
13. Greeks: define Delta, Gamma, Theta. Show the BS PDE as an algebraic identity linking them, and give the closed-form call Delta and Gamma. -> -> (gap?)
14. List the five parameters the BS call price depends on and explain why mu (the real-world drift) is not among them. -> -> (gap?)

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

### Lecture 08
1. Define the Poisson process N_t with intensity lambda. State its three defining properties and give P(N_t=k). What are its mean and variance? -> -> (gap?)
2. Show that mean = variance = lambda for the Poisson law. Do the E[X] sum by hand. -> -> (gap?)
3. What is the compensated Poisson process, and why is it (not N_t itself) a martingale? Verify the martingale property explicitly. -> -> (gap?)
4. Distinguish homogeneous, inhomogeneous (time-dependent lambda(t)), and Cox/doubly-stochastic Poisson processes. What is the compensator in each case? -> -> (gap?)
5. Derive the characteristic function of a compound Poisson process Q_t = sum_{k=1}^{N_t} Y_k by conditioning on N_t. You should reach exp(t*lambda*(nu_hat(u)-1)). -> -> (gap?)
6. Identify the characteristic exponent of the compound Poisson process and connect it to the Levy-Khintchine representation. Why does the "-1" appear, and what condition does nu_hat(0)=1 enforce? -> -> (gap?)
7. Write the Merton jump-diffusion SDE for S_t and derive the log-price SDE via Ito-for-jumps. Why is there no (1/2)g''J^2 term in the jump part, and why does ln S_t - ln S_{t^-} = ln(1+J_t)? -> -> (gap?)
8. Derive the risk-neutral drift correction mu = r - lambda*E[J_t] from the requirement that e^{-rt}S_t is a Q-martingale. What is the "jump compensator" here? -> -> (gap?)
9. Common trap: in the Merton drift correction, is it E[J] or E[ln(1+J)] that gets compensated? If ln(1+J)~N(mu_J,sigma_J^2), what is kappa = E[J]? -> -> (gap?)
10. Write Merton's lognormal-jump cf of ln S_T and Kou's double-exponential cf. State Kou's nu_hat(u) and explain the roles of p,q,eta_1,eta_2 and why eta_1>1 is required. -> -> (gap?)
11. Compare Merton vs Kou: tail shape, symmetry, and the decay rate of the cf in u. Why does the cf decay rate matter for COS? -> -> (gap?)
12. How does the jump-diffusion cf enter the COS formula? At which arguments is phi evaluated, and what is the ONLY model-specific input COS needs? -> -> (gap?)
13. Short-maturity COS trap: write c_1, c_2, c_4 for Merton's log-price. Why can a range [a,b] built from c_2 alone be too narrow at small tau, and how does the jump c_4 fix it? (Connect to the Assignment 2 bug.) -> -> (gap?)
14. State the PIDE for a jump-diffusion option value. Which term is non-local, and why does this motivate Fourier methods over a PIDE grid solve? -> -> (gap?)
15. Define an affine process and write the AJD SDE with all four affine conditions (mu, sigma sigma^T, lambda(x), R(x)). What is the jump transform theta(c)? -> -> (gap?)
16. State the AJD result phi = exp(alpha + beta.x) and the Riccati ODEs for (alpha,beta) with boundary conditions. Which term is quadratic, and where does (theta(beta)-1) come from? -> -> (gap?)
17. Recover the Black-Scholes log-price cf by solving the AJD ODEs with no jumps (X=ln S). Show beta=iu and the alpha you obtain. -> -> (gap?)
18. The (theta-1) / compensator motif appears at three scales in this lecture (compensated Poisson, drift correction, AJD ODE). State all three and explain why they are "the same idea". -> -> (gap?)

## Cluster 5 — American options
## Cluster 6 — Exotics

### Lecture 11
1. Give the precise payoff of an arithmetic-average Asian call and a geometric-average Asian call. -> -> (gap?)
2. What economic need does an Asian option serve that a vanilla cannot, and why is the premium lower? (airline fuel hedge; average exposure; effective variance reduced) -> -> (gap?)
3. Derive the geometric-Asian closed form: why is G lognormal, and what are mu_G and sigma_G^2 for equally spaced dates? Show sigma_G^2 -> sigma^2 T/3 in the continuous limit. -> -> (gap?)
4. Why does the arithmetic Asian have NO closed form / no closed-form CF, and what does that imply for method choice? (sum of lognormals not lognormal) -> -> (gap?)
5. List the four numerical methods for arithmetic Asians and the one-line reason for each; what is the standard control variate for the MC? (geometric Asian) -> -> (gap?)
6. State the Fouque-Han 3D Asian PDE and identify the four blocks. Then explain Vecer's reduction: what does q(t) replicate, and how does it collapse the path-dependent state I_t? -> -> (gap?)
7. Give both digital payoffs (cash-or-nothing, asset-or-nothing). Derive the cash-or-nothing call price = e^{-rT} N(d2) from Q(S_T > K). -> -> (gap?)
8. A digital has a clean closed form. Why is it nonetheless considered a hard/dangerous product? (delta spike, gamma sign-flip, pin risk; call-spread notional 1/eps -> infinity near K at expiry) -> -> (gap?)
9. State the Breeden-Litzenberger link dC/dK = -e^{-rT} Q(S_T > K) and explain the centred call-spread static replication (and why centring gives 2nd-order accuracy). -> -> (gap?)
10. Which numerical method is most natural for a digital and why? (COS: indicator payoff has closed-form cosine coefficients; it's the European COS method as a special case) -> -> (gap?)
11. Give the basket and worst-of payoffs. Show Var(B_T) = sum_i sum_j w_i w_j Cov(S_i,S_j) and explain why correlation is the dominant risk. -> -> (gap?)
12. Why is Monte Carlo (not PDE or COS) the method for a >=4-asset worst-of? State the COS availability honestly. (curse of dimensionality; Ruijter-Oosterlee 2D only, no dedicated COS for n>=4) -> -> (gap?)
13. In a worst-of autocallable, is the embedded option a call-on-min or a worst-of put? Explain who is short what. -> -> (gap?)
14. Give the cliquet payoff with local cap C and floor F. Why is it forward-skew / forward-volatility sensitive, and why is MC with local/stochastic vol the practical method? -> -> (gap?)
15. Pre-2008 vs post-2008: which exotics grew, which shrank, and what is the unifying post-crisis preference? (hedgeable, modellable, explainable, liquid; basket/worst-of and autocallables grew; bespoke/long-dated/aggressive cliquets shrank) -> -> (gap?)
