import math
from scipy.stats import norm

def black_scholes_greeks(
    spot_price, strike_price, time_to_expiry, iv, rate=0.06, option_type="call"
):
    S = spot_price
    K = strike_price
    T = time_to_expiry
    r = rate
    sigma = iv / 100  # convert % to decimal

    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    delta = norm.cdf(d1) if option_type == "call" else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * norm.pdf(d1) * math.sqrt(T) / 100  # per 1% change in IV
    theta = (
        (-S * norm.pdf(d1) * sigma / (2 * math.sqrt(T)))
        - r * K * math.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2)
    ) / 365
    rho = (
        K * T * math.exp(-r * T) * norm.cdf(d2 if option_type == "call" else -d2)
    ) / 100

    return {
        "Delta": round(delta, 4),
        "Gamma": round(gamma, 4),
        "Vega": round(vega, 4),
        "Theta": round(theta, 4),
        "Rho": round(rho, 4),
    }
