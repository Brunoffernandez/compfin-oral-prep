#!/usr/bin/env python3
"""
Compare four methods for pricing a European call option
under the Black-Scholes model:

1. Standard Monte Carlo (MC)
2. Monte Carlo with antithetic variates (AV)
3. Randomized Quasi-Monte Carlo (RQMC) using Sobol sequences
4. Importance sampling via change to the stock numeraire (Q^S)

Usage:
    python qmc_bs_call_compare.py

Optional:
    python qmc_bs_call_compare.py --spot 100 --strike 100 --rate 0.05 \
        --vol 0.2 --maturity 1.0 --n 8192 --replications 20
"""

from __future__ import annotations

import argparse
import math
from statistics import mean, pstdev

import numpy as np
from scipy.stats import norm, qmc


def bs_call_price(spot: float, strike: float, rate: float, vol: float, maturity: float) -> float:
    """Closed-form Black-Scholes price of a European call."""
    if maturity <= 0:
        return max(spot - strike, 0.0)
    if vol <= 0:
        payoff = max(spot * math.exp(rate * maturity) - strike, 0.0)
        return math.exp(-rate * maturity) * payoff

    sqrt_t = math.sqrt(maturity)
    d1 = (math.log(spot / strike) + (rate + 0.5 * vol * vol) * maturity) / (vol * sqrt_t)
    d2 = d1 - vol * sqrt_t
    return spot * norm.cdf(d1) - strike * math.exp(-rate * maturity) * norm.cdf(d2)


def simulate_terminal_stock_q(
    normals: np.ndarray,
    spot: float,
    rate: float,
    vol: float,
    maturity: float,
) -> np.ndarray:
    """Simulate terminal stock prices under the risk-neutral measure Q."""
    drift = (rate - 0.5 * vol * vol) * maturity
    diffusion = vol * math.sqrt(maturity) * normals
    return spot * np.exp(drift + diffusion)


def simulate_terminal_stock_qs(
    normals: np.ndarray,
    spot: float,
    rate: float,
    vol: float,
    maturity: float,
) -> np.ndarray:
    """Simulate terminal stock prices under the stock-numeraire measure Q^S."""
    drift = (rate + 0.5 * vol * vol) * maturity
    diffusion = vol * math.sqrt(maturity) * normals
    return spot * np.exp(drift + diffusion)


def discounted_call_payoff(
    terminal_stock: np.ndarray,
    strike: float,
    rate: float,
    maturity: float,
) -> np.ndarray:
    """Discounted payoff of a European call."""
    return math.exp(-rate * maturity) * np.maximum(terminal_stock - strike, 0.0)


def mc_price(
    n_paths: int,
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    seed: int | None = None,
) -> tuple[float, float]:
    """Standard Monte Carlo price and standard error."""
    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n_paths)
    st = simulate_terminal_stock_q(z, spot, rate, vol, maturity)
    payoffs = discounted_call_payoff(st, strike, rate, maturity)

    estimate = float(np.mean(payoffs))
    std_error = float(np.std(payoffs, ddof=1) / math.sqrt(n_paths))
    return estimate, std_error


def antithetic_mc_price(
    n_paths: int,
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    seed: int | None = None,
) -> tuple[float, float]:
    """
    Monte Carlo with antithetic variates.

    If n_paths is odd, one path is dropped so that paths can be paired.
    Each pair uses Z and -Z, and the pair payoff average is treated
    as one observation for standard error estimation.
    """
    n_pairs = n_paths // 2
    if n_pairs < 1:
        raise ValueError("n_paths must be at least 2 for antithetic variates.")

    rng = np.random.default_rng(seed)
    z = rng.standard_normal(n_pairs)

    st_plus = simulate_terminal_stock_q(z, spot, rate, vol, maturity)
    st_minus = simulate_terminal_stock_q(-z, spot, rate, vol, maturity)

    payoff_plus = discounted_call_payoff(st_plus, strike, rate, maturity)
    payoff_minus = discounted_call_payoff(st_minus, strike, rate, maturity)

    pair_payoffs = 0.5 * (payoff_plus + payoff_minus)

    estimate = float(np.mean(pair_payoffs))
    std_error = float(np.std(pair_payoffs, ddof=1) / math.sqrt(n_pairs))
    return estimate, std_error


def qmc_price_rqmc(
    n_paths: int,
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    replications: int = 16,
    seed: int | None = None,
) -> tuple[float, float, int]:
    """
    Randomized Quasi-Monte Carlo using scrambled Sobol points.

    Returns:
        (estimate, standard_error, actual_n_used)
    """
    if n_paths <= 0:
        raise ValueError("n_paths must be positive")
    if replications <= 1:
        raise ValueError("replications must be at least 2 for an error estimate")

    m = math.ceil(math.log2(n_paths))
    n_qmc = 2**m

    estimates: list[float] = []
    base_seed = 12345 if seed is None else seed

    for r in range(replications):
        sampler = qmc.Sobol(d=1, scramble=True, seed=base_seed + r)
        u = sampler.random_base2(m=m).reshape(-1)

        eps = np.finfo(float).eps
        u = np.clip(u, eps, 1.0 - eps)

        z = norm.ppf(u)
        st = simulate_terminal_stock_q(z, spot, rate, vol, maturity)
        payoffs = discounted_call_payoff(st, strike, rate, maturity)
        estimates.append(float(np.mean(payoffs)))

    estimate = mean(estimates)
    std_error = pstdev(estimates) / math.sqrt(replications)
    return estimate, std_error, n_qmc


def stock_numeraire_is_price(
    n_paths: int,
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    seed: int | None = None,
) -> tuple[float, float]:
    """
    Importance sampling via change to the stock numeraire.

    Uses:
        C0 = S0 * Q^S(ST > K) - K exp(-rT) * Q(ST > K)

    We estimate the two probabilities by independent Monte Carlo under
    Q^S and Q, respectively, then combine them.

    Returns:
        (estimate, standard_error)
    """
    rng_qs = np.random.default_rng(seed)
    rng_q = np.random.default_rng(None if seed is None else seed + 10_000)

    z_qs = rng_qs.standard_normal(n_paths)
    z_q = rng_q.standard_normal(n_paths)

    st_qs = simulate_terminal_stock_qs(z_qs, spot, rate, vol, maturity)
    st_q = simulate_terminal_stock_q(z_q, spot, rate, vol, maturity)

    ind_qs = (st_qs > strike).astype(float)
    ind_q = (st_q > strike).astype(float)

    a = spot * ind_qs
    b = strike * math.exp(-rate * maturity) * ind_q
    estimator_samples = a - b

    estimate = float(np.mean(estimator_samples))
    std_error = float(np.std(estimator_samples, ddof=1) / math.sqrt(n_paths))
    return estimate, std_error



def optimal_drift_shift_mu(
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
) -> float:
    """
    Drift shift that moves the mean of the normal shock to the boundary
    of the in-the-money region S_T > K.
    """
    if maturity <= 0:
        return 0.0
    if vol <= 0:
        return 0.0

    return (
        math.log(strike / spot) - (rate - 0.5 * vol * vol) * maturity
    ) / (vol * math.sqrt(maturity))



def drift_shift_is_price(
    n_paths: int,
    spot: float,
    strike: float,
    rate: float,
    vol: float,
    maturity: float,
    mu: float | None = None,
    seed: int | None = None,
) -> tuple[float, float, float]:
    """
    Importance sampling with drift shift.

    Simulate Z ~ N(mu, 1) instead of N(0, 1), and correct using the
    likelihood ratio. If mu is not provided, use the standard
    strike-hitting choice.
    """
    if mu is None:
        mu = optimal_drift_shift_mu(
            spot=spot,
            strike=strike,
            rate=rate,
            vol=vol,
            maturity=maturity,
        )

    rng = np.random.default_rng(seed)

    # Sample under shifted measure: Z* ~ N(mu, 1)
    z_shifted = rng.standard_normal(n_paths) + mu

    st = simulate_terminal_stock_q(z_shifted, spot, rate, vol, maturity)
    payoff = discounted_call_payoff(st, strike, rate, maturity)

    # Likelihood ratio dP/dP_mu evaluated at z_shifted
    likelihood = np.exp(-mu * z_shifted + 0.5 * mu * mu)

    estimator = payoff * likelihood

    estimate = float(np.mean(estimator))
    std_error = float(np.std(estimator, ddof=1) / math.sqrt(n_paths))

    return estimate, std_error, mu




def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare MC, antithetic variates, RQMC, and stock-numeraire importance sampling."
    )
    parser.add_argument("--spot", type=float, default=100.0, help="Initial stock price S0")
    parser.add_argument("--strike", type=float, default=100.0, help="Strike K")
    parser.add_argument("--rate", type=float, default=0.05, help="Risk-free rate r")
    parser.add_argument("--vol", type=float, default=0.20, help="Volatility sigma")
    parser.add_argument("--maturity", type=float, default=1.0, help="Maturity T")
    parser.add_argument("--n", type=int, default=8192, help="Number of paths/samples")
    parser.add_argument("--replications", type=int, default=20, help="Number of RQMC replications")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    exact = bs_call_price(args.spot, args.strike, args.rate, args.vol, args.maturity)

    mc_est, mc_se = mc_price(
        n_paths=args.n,
        spot=args.spot,
        strike=args.strike,
        rate=args.rate,
        vol=args.vol,
        maturity=args.maturity,
        seed=args.seed,
    )

    av_est, av_se = antithetic_mc_price(
        n_paths=args.n,
        spot=args.spot,
        strike=args.strike,
        rate=args.rate,
        vol=args.vol,
        maturity=args.maturity,
        seed=args.seed,
    )

    qmc_est, qmc_se, qmc_n = qmc_price_rqmc(
        n_paths=args.n,
        spot=args.spot,
        strike=args.strike,
        rate=args.rate,
        vol=args.vol,
        maturity=args.maturity,
        replications=args.replications,
        seed=args.seed,
    )

    is_est, is_se = stock_numeraire_is_price(
        n_paths=args.n,
        spot=args.spot,
        strike=args.strike,
        rate=args.rate,
        vol=args.vol,
        maturity=args.maturity,
        seed=args.seed,
    )

    is_drift_est, is_drift_se, is_mu = drift_shift_is_price(
        n_paths=args.n,
        spot=args.spot,
        strike=args.strike,
        rate=args.rate,
        vol=args.vol,
        maturity=args.maturity,
        mu=1,   # use optimal mu automatically if None
        seed=args.seed,
    )

    print("European Call under Black-Scholes")
    print("-" * 72)
    print(f"S0             = {args.spot:.6f}")
    print(f"K              = {args.strike:.6f}")
    print(f"r              = {args.rate:.6f}")
    print(f"sigma          = {args.vol:.6f}")
    print(f"T              = {args.maturity:.6f}")
    print(f"Requested N    = {args.n}")
    print(f"RQMC N used    = {qmc_n}")
    print(f"Replications   = {args.replications}")
    print(f"Drift-shift IS mu            : {is_mu:.8f}")
    print("-" * 72)
    print(f"Black-Scholes exact           : {exact:.8f}")
    print(f"MC estimate                   : {mc_est:.8f}   SE ~ {mc_se:.8f}   abs err = {abs(mc_est - exact):.8f}")
    print(f"Antithetic MC estimate        : {av_est:.8f}   SE ~ {av_se:.8f}   abs err = {abs(av_est - exact):.8f}")
    print(f"RQMC estimate                 : {qmc_est:.8f}   SE ~ {qmc_se:.8f}   abs err = {abs(qmc_est - exact):.8f}")
    print(f"Stock-numeraire IS estimate   : {is_est:.8f}   SE ~ {is_se:.8f}   abs err = {abs(is_est - exact):.8f}")
    print(f"Drift-shift IS estimate       : {is_drift_est:.8f}   SE ~ {is_drift_se:.8f}   abs err = {abs(is_drift_est - exact):.8f}")
    print("-" * 72)

    if av_se > 0:
        print(f"SE reduction (MC / AV)        : {mc_se / av_se:.2f}x")
    if qmc_se > 0:
        print(f"SE reduction (MC / RQMC)      : {mc_se / qmc_se:.2f}x")
    if is_se > 0:
        print(f"SE reduction (MC / Numeraire) : {mc_se / is_se:.2f}x")
    if is_drift_se > 0:
        print(f"SE reduction (MC / Drift IS)  : {mc_se / is_drift_se:.2f}x")

if __name__ == "__main__":
    main()