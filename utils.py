import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from greeks import black_scholes_greeks

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
    except:
        return None

def parse_option_metrics(data):
    if not data:
        return {"PCR": None, "IV": None, "Delta": None, "Gamma": None, "Vega": None}

    expiry_dates = data["records"]["expiryDates"]
    current_expiry = expiry_dates[0]
    underlying = data["records"]["underlyingValue"]
    strikes = sorted({item["strikePrice"] for item in data["records"]["data"]})
    atm_strike = min(strikes, key=lambda x: abs(x - underlying))

    total_ce_oi = total_pe_oi = 0
    iv = None

    for item in data["records"]["data"]:
        if item["expiryDate"] != current_expiry:
            continue
        ce = item.get("CE", {})
        pe = item.get("PE", {})
        total_ce_oi += ce.get("openInterest", 0)
        total_pe_oi += pe.get("openInterest", 0)
        if item["strikePrice"] == atm_strike:
            iv = (ce.get("impliedVolatility", 0) + pe.get("impliedVolatility", 0)) / 2

    pcr = round(total_pe_oi / total_ce_oi, 2) if total_ce_oi else None
    T = max((datetime.strptime(current_expiry, "%d-%b-%Y") - datetime.today()).days / 365, 0.038)
    greeks = black_scholes_greeks(underlying, atm_strike, T, iv or 12.0)

    return {
        "PCR": pcr,
        "IV": round(iv, 2) if iv else None,
        "Delta": greeks["Delta"],
        "Gamma": greeks["Gamma"],
        "Vega": greeks["Vega"]
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

def generate_trade_log(df, symbol, tf):
    lot_size = 50 if symbol == "NIFTY" else 15
    trades = []
    for i in range(1, len(df) - 1):
        if df["Signal"][i] == "BUY" and df["Signal"][i - 1] != "BUY":
            entry = df["Close"][i]
            exit = df["Close"][i + 1]
            pnl = round((exit - entry) * lot_size, 2)
            trades.append({
                "Trade ID": f"{symbol}_{tf}_{i}",
                "Symbol": symbol,
                "Timeframe": tf,
                "Time": df.index[i].strftime("%Y-%m-%d %H:%M"),
                "Signal": "BUY",
                "Entry": round(entry, 2),
                "Exit": round(exit, 2),
                "Lot Size": lot_size,
                "PnL (₹)": pnl
            })
    return trades
