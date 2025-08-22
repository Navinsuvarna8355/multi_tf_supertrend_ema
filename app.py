import streamlit as st
from utils import fetch_option_metrics, fetch_dummy_candles
from indicators import ema, compute_supertrend
from datetime import datetime
import pytz

IST = pytz.timezone("Asia/Kolkata")
st.set_page_config(layout="wide")
st.title("📊 NIFTY & BANKNIFTY Multi-Timeframe Dashboard")

symbols = ["NIFTY", "BANKNIFTY"]
timeframes = [("5m", "5-Min"), ("15m", "15-Min"), ("60m", "1-Hour")]

for symbol in symbols:
    st.header(f"⚡ {symbol}")
    cols = st.columns(len(timeframes))
    for i, (tf_code, tf_name) in enumerate(timeframes):
        df = fetch_dummy_candles(symbol, tf_code)
        df["EMA"] = ema(df["Close"], 20)
        df["Supertrend"], df["Trend"] = compute_supertrend(df)

        last = df.iloc[-1]
        signal = "BUY" if last["Close"] > last["EMA"] and last["Trend"] else "SELL"
        with cols[i]:
            st.subheader(tf_name)
            st.metric("Signal", signal)
            st.caption(f"Close: {last['Close']:.2f}, EMA: {last['EMA']:.2f}")

    st.subheader("📈 Options Metrics")
    metrics = fetch_option_metrics(symbol)
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("PCR", metrics["PCR"] or "—")
    m2.metric("IV %", f"{metrics['IV']:.2f}" if metrics["IV"] else "—")
    m3.metric("Delta", metrics["Delta"] or "—")
    m4.metric("Gamma", metrics["Gamma"] or "—")
    m5.metric("Vega", metrics["Vega"] or "—")

st.caption(f"Last updated: {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')} IST")
