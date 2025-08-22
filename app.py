import streamlit as st
import pandas as pd
import numpy as np
from trade_log import TradeLogger

# Dummy signal generator
def generate_signals(df):
    df["EMA"] = df["Close"].ewm(span=10).mean()
    df["Trend"] = df["Close"] > df["EMA"]
    return df

# Dummy data fetcher
def get_data(symbol, timeframe):
    np.random.seed(42)
    data = pd.DataFrame({
        "Close": np.random.randint(19500, 20000, size=100)
    })
    return generate_signals(data)

st.set_page_config(layout="wide")
st.title("📊 NIFTY & BANKNIFTY Trading Dashboard")

symbols = ["NIFTY", "BANKNIFTY"]
timeframes = ["5m", "15m", "1h"]

loggers = {
    "NIFTY": TradeLogger("NIFTY", lot_size=50),
    "BANKNIFTY": TradeLogger("BANKNIFTY", lot_size=15)
}

cols = st.columns(2)

for i, symbol in enumerate(symbols):
    with cols[i]:
        st.header(f"📈 {symbol} Signals")
        for tf in timeframes:
            df = get_data(symbol, tf)
            last = df.iloc[-1]
            signal = "BUY" if last["Close"] > last["EMA"] and last["Trend"] else "SELL"
            entry = last["Close"]
            exit = df["Close"].iloc[-2]
            reason = f"Close > EMA and Supertrend bullish" if signal == "BUY" else "Close < EMA or bearish trend"
            loggers[symbol].log_trade(signal, entry, exit, tf, reason)
            st.write(f"**{tf} Signal:** {signal} | Entry: {entry} | Exit: {exit} | Reason: {reason}")

        st.subheader("📘 Trade Log")
        st.dataframe(loggers[symbol].get_trade_df(), use_container_width=True)
        st.metric("💰 Cumulative PnL", f"₹{loggers[symbol].cumulative_pnl()}")

        if st.button(f"Export {symbol} Log"):
            filename = loggers[symbol].export_csv(f"{symbol.lower()}_trade_log.csv")
            st.success(f"Exported to {filename}")
