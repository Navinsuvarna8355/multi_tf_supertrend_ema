import streamlit as st
import pandas as pd
from utils import get_live_price
from indicators import generate_signals
from trade_log import log_trade, load_trade_log, save_trade_log
from greeks import calculate_greeks  # Optional: if implemented

st.set_page_config(layout="wide")
st.title("📊 NIFTY & BANKNIFTY Trading Dashboard")

# ------------------ Settings ------------------
symbols = ["NIFTY", "BANKNIFTY"]
timeframes = ["5m", "15m", "1h"]
auto_refresh = st.sidebar.checkbox("🔁 Auto-refresh every 30s", value=False)

# ------------------ Dashboard ------------------
for symbol in symbols:
    col = st.columns(2)[symbols.index(symbol)]
    with col:
        st.subheader(f"{symbol} Signals")
        trade_log = []
        cumulative_pnl = 0

        for tf in timeframes:
            live_price = get_live_price(symbol)
            close_series = [live_price + i for i in range(-10, 10)]
            signal, reason, ema = generate_signals(close_series)
            entry = live_price
            exit = entry - 40 if signal == "SELL" else entry + 40
            pnl = abs(entry - exit)

            st.write(f"**{tf} Signal:** {signal} | Entry: {entry} | Exit: {exit} | Reason: {reason}")
            trade = log_trade(symbol, signal, entry, exit, pnl, tf, reason)
            trade_log.append(trade)
            cumulative_pnl += pnl

        df = pd.DataFrame(trade_log)
        st.dataframe(df, use_container_width=True)
        st.success(f"Cumulative PnL: ₹{int(cumulative_pnl)}")

        # Save log
        save_trade_log(df, symbol)

        # Optional: Greeks Panel
        st.markdown("### Greeks (ATM Option)")
        greeks = calculate_greeks(symbol, live_price)
        st.json(greeks)

# ------------------ CSV Export ------------------
st.sidebar.markdown("### 📥 Export Trade Logs")
for symbol in symbols:
    df = load_trade_log(symbol)
    st.sidebar.download_button(
        label=f"Download {symbol} Log",
        data=df.to_csv(index=False),
        file_name=f"{symbol.lower()}_trade_log.csv",
        mime="text/csv"
    )

# ------------------ Auto Refresh ------------------
if auto_refresh:
    st.experimental_rerun()
