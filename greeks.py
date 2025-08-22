from math import log, sqrt, exp
from scipy.stats import norm

def calculate_greeks(symbol, spot, strike=None, expiry_days=7, rate=0.06, iv=0.18):
    if not strike:
        strike = round(spot / 50) * 50
    T = expiry_days / 365
    d1 = (log(spot / strike) + (rate + iv**2 / 2) * T) / (iv * sqrt(T))
    d2 = d1 - iv * sqrt(T)

    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (spot * iv * sqrt(T))
    vega = spot * norm.pdf(d1) * sqrt(T) / 100
    theta = (-spot * norm.pdf(d1) * iv / (2 * sqrt(T)) - rate * strike * exp(-rate * T) * norm.cdf(d2)) / 365

    return {
        "Spot": spot,
        "Strike": strike,
        "IV": iv,
        "Delta": round(delta, 4),
        "Gamma": round(gamma, 4),
        "Vega": round(vega, 2),
        "Theta": round(theta, 2)
    }
