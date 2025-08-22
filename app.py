import streamlit as st
import pandas as pd
from indicators import calculate_supertrend, calculate_ema
from trade_log import load_trade_log, save_trade_log

st.set_page_config(layout="wide")
st.title("📊 NIFTY & BANKNIFTY Trading Dashboard")

def load_csv(symbol, tf):
    try:
        return pd.read_csv(f"data/{symbol}_{tf}.csv")
    except FileNotFoundError:
        st.error(f"{symbol} {tf} data error: CSV file not found: {symbol}_{tf}.csv")
        return pd.DataFrame()

def show_signals(symbol):
    st.subheader(f"{symbol} Signals")
    pnl_total = 0
    for tf in ['5m', '15m', '1h']:
        df = load_csv(symbol, tf)
        if df.empty:
            continue
        df = calculate_supertrend(df)
        df = calculate_ema(df)
        latest = df.iloc[-1]
        signal = "BUY" if latest['close'] > latest['EMA'] and latest['Supertrend'] else "SELL"
        st.write(f"{symbol} {tf} Signal: **{signal}**")

    trade_log = load_trade_log(symbol)
    if not trade_log.empty:
        pnl_total = trade_log['PnL'].sum()
        st.dataframe(trade_log)
        st.download_button("📥 Export Trade Logs", trade_log.to_csv(index=False), file_name=f"{symbol}_trade_log.csv")

    st.write(f"Cumulative PnL: ₹{pnl_total}")

def show_greeks():
    st.subheader("Greeks (ATM Option)")
    greeks = {
        "Delta": 0.52,
        "Gamma": 0.03,
        "Vega": 12.5,
        "Theta": -4.2,
        "IV": 18.7
    }
    st.json(greeks)

col1, col2 = st.columns(2)
with col1:
    show_signals("NIFTY")
    show_greeks()
with col2:
    show_signals("BANKNIFTY")
    show_greeks()
