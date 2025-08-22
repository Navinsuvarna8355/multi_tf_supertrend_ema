import pandas as pd
import yfinance as yf
import requests
import pytz
from datetime import datetime

IST = pytz.timezone("Asia/Kolkata")

def _ticker(index_choice):
    return "^NSEI" if index_choice == "NIFTY" else "^NSEBANK"

def fetch_index_data(index_choice, interval, lookback_days):
    try:
        df = yf.download(_ticker(index_choice), period=f"{lookback_days}d", interval=interval, progress=False)
        df = df.tz_localize("UTC").tz_convert(IST)
        return df.dropna()
    except:
        return pd.DataFrame()

def add_indicators(df, atr_period=10, atr_mult=3, fast_ema=8, slow_ema=21):
    df["ema_fast"] = df["Close"].ewm(span=fast_ema).mean()
    df["ema_slow"] = df["Close"].ewm(span=slow_ema).mean()
    high, low, close = df["High"], df["Low"], df["Close"]
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    atr = tr.ewm(alpha=1/atr_period).mean()
    hl2 = (high + low) / 2
    basic_upper = hl2 + atr_mult * atr
    basic_lower = hl2 - atr_mult * atr
    final_upper, final_lower = basic_upper.copy(), basic_lower.copy()
    for i in range(1, len(df)):
        final_upper.iat[i] = basic_upper.iat[i] if (basic_upper.iat[i] < final_upper.iat[i-1]) or (close.iat[i-1] > final_upper.iat[i-1]) else final_upper.iat[i-1]
        final_lower.iat[i] = basic_lower.iat[i] if (basic_lower.iat[i] > final_lower.iat[i-1]) or (close.iat[i-1] < final_lower.iat[i-1]) else final_lower.iat[i-1]
    in_uptrend = pd.Series(True, index=df.index)
    for i in range(1, len(df)):
        if close.iat[i] > final_lower.iat[i]:
            in_uptrend.iat[i] = True
        elif close.iat[i] < final_upper.iat[i]:
            in_uptrend.iat[i] = False
    df["supertrend"] = [final_lower[i] if in_uptrend[i] else final_upper[i] for i in range(len(df))]
    df["in_uptrend"] = in_uptrend
    return df

def generate_signals(df):
    sig = pd.DataFrame(index=df.index)
    sig["signal"] = "FLAT"
    bull = (df["Close"] > df["supertrend"]) & (df["ema_fast"] > df["ema_slow"]) & (df["ema_fast"].shift() <= df["ema_slow"].shift())
    bear = (df["Close"] < df["supertrend"]) & (df["ema_fast"] < df["ema_slow"]) & (df["ema_fast"].shift() >= df["ema_slow"].shift())
    sig.loc[bull, "signal"] = "BUY_CE"
    sig.loc[bear, "signal"] = "BUY_PE"
    sell_ce = (df["Close"] < df["supertrend"]) & (df["ema_fast"] < df["ema_slow"]) & (~bear)
    sell_pe = (df["Close"] > df["supertrend"]) & (df["ema_fast"] > df["ema_slow"]) & (~bull)
    sig.loc[sell_ce, "signal"] = "SELL_CE"
    sig.loc[sell_pe, "signal"] = "SELL_PE"
    return sig

def fetch_option_metrics(index_choice):
    base = "https://www.nseindia.com"
    url = f"{base}/api/option-chain-indices?symbol={index_choice}"
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        session.get(base, headers=headers, timeout=5)
        r = session.get(url, headers=headers, timeout=5)
        data = r.json()
        rec = data.get("records", {})
        under = rec.get("underlyingValue")
        oi_data = rec.get("data", [])
        total_put_oi = sum([x.get("PE", {}).get("openInterest", 0) for x in oi_data])
        total_call_oi = sum([x.get("CE", {}).get("openInterest", 0) for x in oi_data])
        pcr = total_put_oi / total_call_oi if total_call_oi else None
        strikes = sorted({row["strikePrice"] for row in oi_data if "strikePrice" in row})
        atm = min(strikes, key=lambda x: abs(x - under))
        atm_row = next((row for row in oi_data if row.get("strikePrice") == atm), {})
        ce = atm_row.get("CE", {})
        pe = atm_row.get("PE", {})
        iv = (ce.get("impliedVolatility") + pe.get("impliedVolatility")) / 2 if ce.get("impliedVolatility") and pe.get("impliedVolatility") else None
        delta = ce.get("delta")
        gamma = ce.get("gamma")
        vega = ce.get("vega")
        return pcr, iv, delta, gamma, vega
    except:
        return None, None, None, None, None
