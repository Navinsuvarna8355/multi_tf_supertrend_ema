import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import pytz
import numpy as np

IST = pytz.timezone("Asia/Kolkata")

def fetch_option_chain(symbol="NIFTY"):
    url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Referer": "https://www.nseindia.com/option-chain"
    }
    session = requests.Session()
    try:
        session.get("https://www.nseindia.com/option-chain", headers=headers, timeout=5)
        response = session.get(url, headers=headers, timeout=5)
        data = json.loads(response.text)
        return data
    except Exception as e:
        print(f"⚠️ NSE scrape failed: {e}")
        return None

def parse_option_metrics(data):
    if not data:
        return {"PCR": None, "IV": None, "Delta": None, "Gamma": None, "Vega": None}

    expiry_dates = data["records"]["expiryDates"]
    current_expiry = expiry_dates[0]
    total_ce_oi = 0
    total_pe_oi = 0
    atm_iv = None
    atm_delta = None
    atm_gamma = None
    atm_vega = None

    underlying = data["records"]["underlyingValue"]
    strikes = sorted({item["strikePrice"] for item in data["records"]["data"]})
    atm_strike = min(strikes, key=lambda x: abs(x - underlying))

    for item in data["records"]["data"]:
        if item["expiryDate"] != current_expiry:
            continue
        strike = item["strikePrice"]
        ce = item.get("CE", {})
        pe = item.get("PE", {})
        total_ce_oi += ce.get("openInterest", 0)
        total_pe_oi += pe.get("openInterest", 0)

        if strike == atm_strike:
            atm_iv = (ce.get("impliedVolatility", 0) + pe.get("impliedVolatility", 0)) / 2
            atm_delta = ce.get("delta", None)
            atm_gamma = ce.get("gamma", None)
            atm_vega = ce.get("vega", None)

    pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi else None
    return {
        "PCR": pcr,
        "IV": atm_iv,
        "Delta": atm_delta,
        "Gamma": atm_gamma,
        "Vega": atm_vega
    }

def fetch_option_metrics(symbol="NIFTY"):
    data = fetch_option_chain(symbol)
    return parse_option_metrics(data)

def fetch_dummy_candles(symbol="NIFTY", tf="5m"):
    now = datetime.now(IST)
    periods = 50
    freq_map = {"5m": 5, "15m": 15, "60m": 60}
    delta = timedelta(minutes=freq_map.get(tf, 5))
    rng = [now - i * delta for i in reversed(range(periods))]

    base_price = 20000 if symbol == "NIFTY" else 45000
    df = pd.DataFrame(index=rng)
    df["Open"] = base_price + np.random.normal(0, 50, size=periods).cumsum()
    df["High"] = df["Open"] + np.random.uniform(5, 15, size=periods)
    df["Low"] = df["Open"] - np.random.uniform(5, 15, size=periods)
    df["Close"] = df["Open"] + np.random.normal(0, 10, size=periods)
    return df
