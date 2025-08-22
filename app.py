import streamlit as st
from utils import fetch_index_data, fetch_option_metrics, load_trade_log
from indicators import add_indicators, generate_signals

st.set_page_config(layout="wide")
st.title("📊 NIFTY & BANKNIFTY Dashboard")

cols = st.columns(2)
symbols = ["NIFTY", "BANKNIFTY"]

for i, symbol in enumerate(symbols):
    with cols[i]:
        st.header(f"{symbol} Overview")
        index_data = fetch_index_data(symbol)
        st.metric("Last Price", index_data["last_price"], delta=index_data["percent_change"])

        option_metrics = fetch_option_metrics(symbol)
        st.subheader("Options Metrics")
        for key, val in option_metrics.items():
            st.write(f"{key}: {val}")

        st.subheader("Trade Log")
        trade_log = load_trade_log()
        st.dataframe(trade_log[trade_log["Symbol"] == symbol])

        # Placeholder for chart
        st.subheader("Signal Chart")
        st.write("📈 Chart placeholder — integrate candles + signals here")

st.sidebar.title("Settings")
st.sidebar.write("Configure strategy parameters here (coming soon)")
