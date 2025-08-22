import pandas as pd
from nsepython import nse_index_quote, nse_optionchain_scrapper
from indicators import add_indicators, generate_signals

def fetch_index_data(symbol):
    try:
        data = nse_index_quote(symbol)
        return {
            "last_price": data["lastPrice"],
            "change": data["change"],
            "percent_change": data["pChange"]
        }
    except Exception as e:
        print(f"⚠️ Index fetch failed for {symbol}: {e}")
        return {"last_price": None, "change": None, "percent_change": None}

def fetch_option_metrics(symbol):
    try:
        chain = nse_optionchain_scrapper(symbol)
        # Placeholder: parse PCR, IV, Greeks from chain
        return {
            "PCR": "...",
            "IV": "...",
            "Delta": "...",
            "Gamma": "...",
            "Vega": "..."
        }
    except Exception as e:
        print(f"⚠️ Option metrics fetch failed for {symbol}: {e}")
        return {"PCR": None, "IV": None, "Delta": None, "Gamma": None, "Vega": None}

def load_trade_log():
    try:
        return pd.read_csv("trade_log.csv")
    except:
        return pd.DataFrame(columns=["Symbol", "Signal", "Entry", "Exit", "PnL"])
