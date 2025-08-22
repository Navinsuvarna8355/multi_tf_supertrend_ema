import requests
import json
import numpy as np
import streamlit as st

def get_live_price(symbol="NIFTY"):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com"
        }
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)
        url = f"https://www.nseindia.com/api/option-chain-indices?symbol={symbol}"
        response = session.get(url, headers=headers, timeout=5)
        data = json.loads(response.text)
        return float(data["records"]["underlyingValue"])
    except Exception as e:
        st.warning(f"Fallback triggered for {symbol}: {e}")
        return np.random.randint(19500, 20000)
