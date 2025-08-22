import streamlit as st
from utils import get_greeks

st.title("📊 Local Greeks Calculator")

spot = st.number_input("Spot Price", value=20350)
expiry = st.text_input("Expiry Date (e.g. 29-Aug-2025)", value="29-Aug-2025")
option_type = st.selectbox("Option Type", ["call", "put"])

# Simulated option chain for demo
option_chain = {
    20300: {"IV": 8.5},
    20350: {"IV": 8.86},
    20400: {"IV": 9.1}
}

if st.button("Calculate Greeks"):
    greeks = get_greeks(option_chain, spot, expiry, option_type)
    if "error" in greeks:
        st.error(f"Calculation failed: {greeks['error']}")
    else:
        st.subheader("Greeks (ATM Option)")
        for k, v in greeks.items():
            st.write(f"**{k}**: {v}")
