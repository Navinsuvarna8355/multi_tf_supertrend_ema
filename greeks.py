import math
from scipy.stats import norm

def black_scholes_greeks(S, K, T, iv, r=0.06, option_type="call"):
    sigma = iv / 100
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    delta = norm.cdf(d1) if option_type == "call" else -norm.cdf(-d1)
    gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
    vega = S * norm.pdf(d1) * math.sqrt(T) / 100

    return {
        "Delta": round(delta, 4),
        "Gamma": round(gamma, 4),
        "Vega": round(vega, 4)
    }
