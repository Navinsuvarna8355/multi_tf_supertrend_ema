import streamlit as st
import pandas as pd
import time

from utils import get_live_price, get_ohlc
from indicators import generate_signals
from trade_log import log_trade, load_trade_log, save_trade_log
from greeks import calculate_greeks

st.set_page_config(layout="wide")
st.title("📊 NIFTY & BANKNIFTY Trading Dashboard")

symbols = ["NIFTY", "BANKNIFTY"]
timeframes = ["5m", "15m", "1h"]
auto_refresh = st.sidebar.checkbox("🔁 Auto-refresh every 30s", value=False)

def show_signals(symbol):
    st.subheader(f"{symbol} Signals")
    trade_log = []
    cumulative_pnl = 0

    live_price = get_live_price(symbol)

    for tf in timeframes:
        try:
            df = get_ohlc(symbol, tf)
            signal, reason, ema = generate_signals(df['close'])

            entry = df.iloc[-1]['close']
            exit = df.iloc[-2]['close']
            pnl = round(exit - entry, 2) if signal == "BUY" else round(entry - exit, 2)

            st.write(f"**{tf} Signal:** {signal} | Entry: ₹{entry} | Exit: ₹{exit} | PnL: ₹{pnl} | Reason: {reason}")
            trade = log_trade(symbol, signal, entry, exit, pnl, tf, reason)
            trade_log.append(trade)
            cumulative_pnl += pnl

        except Exception as e:
            st.warning(f"{symbol} {tf} data error: {e}")

    df = pd.DataFrame(trade_log)
    st.dataframe(df, use_container_width=True)
    st.success(f"Cumulative PnL: ₹{int(cumulative_pnl)}")
    save_trade_log(df, symbol)

    try:
        st.markdown("### Greeks (ATM Option)")
        greeks = calculate_greeks(symbol, live_price)
        st.json(greeks)
    except Exception as e:
        st.warning(f"Greeks unavailable: {e}")

col1, col2 = st.columns([1, 1])
with col1:
    show_signals("NIFTY")
with col2:
    show_signals("BANKNIFTY")

st.sidebar.markdown("### 📥 Export Trade Logs")
for symbol in symbols:
    df = load_trade_log(symbol)
    st.sidebar.download_button(
        label=f"Download {symbol} Log",
        data=df.to_csv(index=False),
        file_name=f"{symbol.lower()}_trade_log.csv",
        mime="text/csv"
    )

if auto_refresh:
    time.sleep(30)
    st.experimental_rerun()
