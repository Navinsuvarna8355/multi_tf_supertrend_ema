import streamlit as st
from datetime import datetime
import pytz
from utils import fetch_index_data, add_indicators, generate_signals, fetch_option_metrics

IST = pytz.timezone("Asia/Kolkata")
st.set_page_config(page_title="Multi-TF Supertrend+EMA Dashboard", layout="wide")

indices = ["NIFTY", "BANKNIFTY"]
timeframes = [("5m", "5-Min"), ("15m", "15-Min"), ("60m", "1-Hour")]

st.title("📊 Multi-Timeframe Supertrend + EMA Dashboard")
st.caption("Live signals with PCR, IV, Delta, Gamma, Vega and reasoning")

for idx in indices:
    st.header(f"⚡ {idx}")
    cols = st.columns(len(timeframes))
    for i, (tf_code, tf_name) in enumerate(timeframes):
        df = fetch_index_data(idx, tf_code, 5)
        if df.empty:
            cols[i].warning(f"No data for {tf_name}")
            continue
        df = add_indicators(df)
        sig = generate_signals(df).iloc[-1]["signal"]

        reason = []
        if "BUY" in sig: reason.append("EMA bullish + Price > Supertrend")
        if "SELL" in sig: reason.append("EMA bearish + Price < Supertrend")

        pcr, iv, delta, gamma, vega = fetch_option_metrics(idx)
        if pcr:
            if pcr > 1 and "BUY" in sig: reason.append(f"PCR {pcr:.2f} supports bullish bias")
            if pcr < 1 and "SELL" in sig: reason.append(f"PCR {pcr:.2f} supports bearish bias")

        signal_color = "🟢" if "BUY" in sig else "🔴"
        with cols[i]:
            st.subheader(tf_name)
            st.markdown(f"**{signal_color} {sig}**")
            st.caption(", ".join(reason) if reason else "No strong confluence")

    st.subheader("📈 Options Metrics (ATM)")
    m1, m2, m3, m4, m5 = st.columns(5)
    pcr, iv, delta, gamma, vega = fetch_option_metrics(idx)
    m1.metric("PCR", f"{pcr:.2f}" if pcr else "—")
    m2.metric("IV %", f"{iv:.2f}" if iv else "—")
    m3.metric("Delta", f"{delta:.2f}" if delta else "—")
    m4.metric("Gamma", f"{gamma:.3f}" if gamma else "—")
    m5.metric("Vega", f"{vega:.2f}" if vega else "—")

st.caption(f"Last updated: {datetime.now(IST).strftime('%Y-%m-%d %H:%M:%S')} IST")
