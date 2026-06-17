# Theory question bank

Filled in per cluster as I study. Format: question -> my short answer -> (gap?).

## Cluster 1 — Foundations / lattice / PDE

### Lecture 01
1. Why does a course built around the COS method open with equity options, given that equities are a tiny fraction of total notional outstanding? -> -> (gap?)
2. Derive the continuously-compounded bank-account value M(t) from the differential argument dM = rM dt, and state the discount factor for one euro at time T. -> -> (gap?)
3. State covered interest-rate parity (1+i_s) = (F_t/S_t)(1+i_c) and prove it by a static no-arbitrage replication. What is the "FX basis" and why is it needed in practice? -> -> (gap?)
4. Write the terminal payoffs of a European call and put. Where are they non-smooth, and why does that kink cause numerical trouble for Fourier/COS methods? -> -> (gap?)
5. In the one-step binomial hedge of a short call, derive Delta = 20/(S_up - S_dn) and then the premium V_{c,0}. Compute both for {120,80} and {120,75}. Why is case B more expensive? -> -> (gap?)
6. Show that the one-step replication price equals E^Q[payoff] under the risk-neutral measure, and that the real-world probabilities p=0.7, p=0.4 never enter. Define q explicitly. -> -> (gap?)
7. At the fair price, does a perfectly hedged writer make money? Explain Pi_up = Pi_dn = 0 and where real-world profit actually comes from. -> -> (gap?)
8. Derive put-call parity from two portfolios held to maturity. Which assumptions about the dynamics of S did you use? -> -> (gap?)
9. Prove the lower bound C(t) >= max(S(t) - K e^{-r(T-t)}, 0) and use it to argue an American call on a non-dividend stock is never exercised early. Why does the argument fail for puts? -> -> (gap?)
10. Apply Ito's lemma to g = ln S under GBM and obtain d(ln S) = (mu - sigma^2/2) dt + sigma dW. Where does the -1/2 sigma^2 come from, and what goes wrong if you forget it? -> -> (gap?)
11. From the log-price ABM, write the closed-form S(t) and verify E[S(t)] = S_0 e^{mu t} using the Gaussian MGF. State the distribution of ln(S(T)/S_0) under Q. -> -> (gap?)
12. State the four defining properties of a Wiener process. What are E[dW], E[(dW)^2], and the quadratic variation [W]_t, and why does that force Ito calculus instead of ordinary calculus? -> -> (gap?)
13. Define the Markov property via P(S_{t+1} <= s | S_t) = P(S_{t+1} <= s | S_t, S_{t-1}, ...). How does it relate to the weak-form EMH, and why does i.i.d. returns imply weak-form EMH but not conversely? -> -> (gap?)
14. Contrast ABM, GBM and OU: which can go negative, which is multiplicative, which mean-reverts, and what single property do all three share? Which one is the template for the Heston variance process? -> -> (gap?)
15. What stylised fact does the SPX QQ-plot reveal (sample quantiles [-3,3] vs theoretical [-2.3,2.3]), and which later models in the course are introduced to fix it? -> -> (gap?)

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

### Lecture 05
1. Derive the CRR up/down/probability parameters by matching the mean and variance of the tree log-return to Black-Scholes. Show every step. -> -> (gap?)
2. Why does the Itô-corrected drift r-½σ² (not r) appear inside u and d? What exactly is being matched -- the price or the log-price? -> -> (gap?)
3. The moment equations give two equations in three unknowns (p,u,d). Which free choice does the deck make, and how does that differ from the classical d=1/u CRR tree? Do both match the first two moments? -> -> (gap?)
4. State and justify the convergence rate of the binomial method. Why is the convergence non-monotone (sign-oscillating in M)? What is the mechanism? -> -> (gap?)
5. Write the FTCS stencil for u_t=u_xx, the explicit update, and the matrix form U^{i+1}=F U^i+p^i. Why do boundary terms appear only in the first and last entries of p^i? -> -> (gap?)
6. Carry out the von Neumann analysis for FTCS. Derive ξ(β)=1-4ν sin²(βh/2) and show the stability condition reduces to ν=k/h²≤½. Which mode is worst? -> -> (gap?)
7. Do the same for BTCS: derive ξ=1/(1+4ν sin²(βh/2)) and explain why BTCS is unconditionally stable. -> -> (gap?)
8. What is the CFL-type cost of FTCS's explicitness in terms of how k must scale with h? Why is this expensive when refining the grid? -> -> (gap?)
9. Give the local truncation errors of FTCS, BTCS and Crank-Nicolson. Why does CN gain an order in time while costing the same per step as BTCS? -> -> (gap?)
10. State the Lax equivalence theorem and explain its role: consistency + stability ⇒ convergence. Why isn't consistency alone enough? -> -> (gap?)
11. Transform the reverse-time BS PDE to a constant-coefficient equation via X=ln S, then remove the reaction term via V=e^{-rτ}W. Show the coefficient algebra (S²∂_SS=∂_XX-∂_X). -> -> (gap?)
12. Show that applying BTCS to the log-transformed advection-diffusion equation with the coupling h²=σ²k makes the centre node drop out, yielding V^i_j=e^{-rk}(p*V^{i+1}_{j+1}+(1-p*)V^{i+1}_{j-1}). Derive p*. -> -> (gap?)
13. In what precise sense is the binomial method "an explicit FD scheme customised to a single time-zero value"? What does a general FD scheme give that the tree throws away? -> -> (gap?)
14. On the raw S-grid the FTCS diffusion weight is ½kσ²j². What does this do to stability near S=L, and how does working in x=ln S fix it? Connect this to domain-truncation pitfalls (cf. the COS [a,b] range at small c_2). -> -> (gap?)
15. The deck's Slide 57 prints a garbled p* formula. Why is it wrong, and what is the correct dimensionless form p*=½(1+(r-σ²/2)√k/σ)? Check the k→0 limit. -> -> (gap?)

## Cluster 2 — Monte Carlo

### Lecture 04
1. Construct the MC integral estimator and prove it is unbiased. Derive Var(X̄_N)=σ²/N from independence and state the standard error. -> -> (gap?)
2. Why is the MC error O(N^{-1/2}) independent of dimension, while tensor-product quadrature is O(N^{-k/d})? When does MC win? -> -> (gap?)
3. Write a CLT-based confidence interval for the MC estimate. Why use the sample variance s_N² with (N-1), and what does it cost? -> -> (gap?)
4. State the Koksma-Hlawka inequality (star discrepancy + Hardy-Krause variation). Why can QMC achieve near-O(N^{-1}) = (log N)^d/N? -> -> (gap?)
5. What is "effective dimension" and why can plain QMC degrade in high nominal dimension? What does randomised QMC recover? -> -> (gap?)
6. Write the Euler-Maruyama scheme for dX=a dt+b dW. What iterated Itô integral does it drop? -> -> (gap?)
7. Derive the Milstein correction from the Itô-Taylor expansion: show ∫∫dW dW = ½[(ΔW)²-h] and the resulting ½bb'[(ΔW)²-h] term. -> -> (gap?)
8. Define strong vs weak convergence order. Give the orders for Euler (½,1) and Milstein (1,1). Why does Milstein buy pathwise but not distributional accuracy? -> -> (gap?)
9. Antithetic variates: derive the variance of the antithetic estimator and state the monotonicity/comonotonicity condition for it to help. -> -> (gap?)
10. Control variates: derive the optimal coefficient θ*=Cov(X,Y)/Var(Y) and show the variance is reduced by (1-ρ²). What is a good control for an Asian option? -> -> (gap?)
11. Importance sampling: write the likelihood-ratio estimator and the Gaussian drift-shift. What is the infinite-variance pitfall, and how does Girsanov connect? -> -> (gap?)
12. Why is MC the benchmark that COS and FFT are compared against, and on what axes (rate, dimension, smoothness) does COS dominate for European options? -> -> (gap?)

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

### Lecture 07
1. Write down the Heston SDE system under Q, naming every parameter, and state what dW^S dW^v = rho dt means physically. -> -> (gap?)
2. Derive the log-spot form d ln S_t and show how the Cholesky factor decorrelates the two Brownian motions into independent W^S, W^v. -> -> (gap?)
3. State the conditional law of nu_T given nu_t (noncentral chi-squared): give d, the noncentrality lambda, and the scaling c. -> -> (gap?)
4. State the Feller condition precisely. What exactly does it guarantee, and what happens to nu_t when it is violated? -> -> (gap?)
5. Derive the Feller condition from the noncentral chi-squared density blowing up at zero (use I_nu(y) ~ (y/2)^nu / Gamma(nu+1) as x->0). -> -> (gap?)
6. Is the Heston model affine in (S, nu)? Show why not, then show how moving to ln S restores the affine condition (give K0, K1, H0, H1). -> -> (gap?)
7. Set up the affine ansatz phi = exp(alpha + beta·x) and derive the Riccati ODE system. Where does each ODE come from when you substitute into the Feynman-Kac PDE? -> -> (gap?)
8. Solve the scalar CIR Riccati dot-beta = -kappa beta + (1/2) gamma^2 beta^2 explicitly via g = 1/beta. Then integrate for alpha. -> -> (gap?)
9. Write the closed-form Heston cf of ln S_T: give b, a, s and the formulas for beta(tau,u) and alpha(tau,u). -> -> (gap?)
10. Explain the "little Heston trap": what goes wrong at long maturities, what causes it (branch cut of complex log / sqrt), and which grouping fixes it? -> -> (gap?)
11. How does the Heston cf enter the COS pricing formula? At which frequencies is it evaluated, and why is Heston the ideal use case for COS? -> -> (gap?)
12. Under Heston, how do you choose the COS truncation range [a,b]? Why is the short-maturity (small c2) case dangerous, and how does negative rho make it worse? -> -> (gap?)
13. Why can the Euler scheme produce negative variance? List truncation, reflection, and log-variance fixes and state the drawback of each. -> -> (gap?)
14. State the Broadie-Kaya exact simulation algorithm (4 steps). Which step is hard and how is it solved (cf of integrated variance -> COS inversion -> inverse sampling)? -> -> (gap?)
15. Name the three tools behind the cf of the integrated variance (infinitesimal generator, time change, Girsanov) and say what discrepancy each one fixes relative to the squared Bessel process. -> -> (gap?)
16. Give the qualitative effect on the implied-vol surface of each parameter: gamma, rho, kappa, nu0, nu-bar. -> -> (gap?)

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

### Lecture 09
1. Define the American early-exercise problem as an optimal-stopping problem. Write v(S,t)=max(Λ, continuation) and v_0 = sup_τ E^Q[e^{-rτ}Λ(S_τ,τ)]. What makes τ* "free"? -> -> (gap?)
2. What is the free boundary S*(t)? Characterise the continuation region (v>Λ, BS PDE holds) vs the stopping region (v=Λ). State the smooth-pasting conditions at S*(t) for the put. -> -> (gap?)
3. PROVE that an American call on a non-dividend stock equals the European call. Give BOTH the slide dominating-strategy argument and the parity lower-bound C^eur = S - Ke^{-r(T-t)} + P^eur > S - K. -> -> (gap?)
4. Why does the same argument FAIL for the put, so early exercise can be optimal? Use parity P^eur = Ke^{-r(T-t)} - S + C^eur and Ke^{-r(T-t)} < K. What is the economic intuition? -> -> (gap?)
5. Why does delta-hedging make the European BS relation an EQUALITY but the American put only an INEQUALITY? Walk through both arbitrage directions and explain why only one survives. -> -> (gap?)
6. Write the LCP for the American put: (v-Λ)≥0, ℒv≤0, (v-Λ)·ℒv=0. Interpret each line, why it equals an obstacle problem, and state terminal/boundary conditions. -> -> (gap?)
7. State the Bermudan backward recursion in log-space: c(x,t_{n-1})=e^{-rΔt}E[v(X(t_n))|x], v=max(Λ,c). What single quantity do all four methods compute differently? -> -> (gap?)
8. Binomial tree: write the backward step with max(intrinsic, discounted continuation). What is the ONLY line that differs from a European tree? How does p=(e^{rΔt}-d)/(u-d) arise? -> -> (gap?)
9. Finite-difference LCP: write the projected update. Why can't you just solve the implicit linear system and clip once? Explain PSOR — projecting INSIDE each SOR sweep. -> -> (gap?)
10. LSM mechanics: explain the backward regression of discounted future cash flows on basis functions. Why regress only on ITM paths? Why is the per-path decision Λ>ĉ (not the fitted value) the cash flow? -> -> (gap?)
11. LSM 8-path example: how is Y constructed (which discount factor, which future date)? Why does the t=1 regression depend on the t=2 exercise decisions? Interpret 0.1144 vs European 0.0564. -> -> (gap?)
12. Is LSM biased? Explain why a suboptimal finite-basis policy gives a LOWER bound, and the competing in-sample foresight upward bias. How do you get a clean out-of-sample estimate? -> -> (gap?)
13. COS Bermudan: derive c(x,t_{n-1}) ≈ e^{-rΔt} Σ' Re{φ(kπ/(b-a)) e^{ikπ(x-a)/(b-a)}} V_k(t_n). What ARE the V_k(t_n) — relate to the Lecture-6 European V_k. -> -> (gap?)
14. COS early-exercise point: define x_n* by c(x_n*,t_n)=Λ(x_n*,t_n). Write the split V_k(t_n)=G_k(a,x_n*)+C_k(x_n*,b,t_n) for a put. Which piece is closed-form (χ_k,ψ_k), which needs the previous coefficients? How is x_n* found? -> -> (gap?)
15. COS algorithm: initialisation, backward loop (Newton for x_n*, FFT for C_k), reconstruction. Why is the cost O(NK log₂K) not O(NK²)? What gives the FFT (Toeplitz/Hankel kernel)? -> -> (gap?)
16. Why does the cumulant range [a,b]=c1±L√(c2+√c4) caveat carry into the Bermudan COS recursion and bite harder per-step? Tie to the Assignment-2 bug: c2=σ²Δt→0, c4=0, no floor; adding K terms does NOT help. -> -> (gap?)
17. Richardson extrapolation Bermudan→American: why does every method here price a Bermudan? Write the 4-point scheme and explain what it cancels. -> -> (gap?)

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
