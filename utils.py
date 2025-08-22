from datetime import datetime
from greeks import black_scholes_greeks

def days_to_expiry(expiry_date_str):
    try:
        expiry = datetime.strptime(expiry_date_str, "%d-%b-%Y")
        today = datetime.today()
        return max((expiry - today).days / 365, 0.001)
    except:
        return 0.038  # fallback ~14 days

def extract_atm_iv(option_chain, spot_price):
    try:
        strikes = sorted(option_chain.keys())
        atm_strike = min(strikes, key=lambda x: abs(x - spot_price))
        return option_chain[atm_strike]["IV"]
    except:
        return 12.0  # fallback IV

def get_greeks(option_chain, spot_price, expiry_str, option_type="call"):
    K = min(option_chain.keys(), key=lambda x: abs(x - spot_price))
    iv = extract_atm_iv(option_chain, spot_price)
    T = days_to_expiry(expiry_str)
    return black_scholes_greeks(spot_price, K, T, iv, option_type=option_type)
