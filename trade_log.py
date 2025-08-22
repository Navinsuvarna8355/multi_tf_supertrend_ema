import pandas as pd
from datetime import datetime

def log_trade(symbol, signal, entry, exit, pnl, timeframe, reason):
    return {
        "Symbol": symbol,
        "Signal": signal,
        "Entry": entry,
        "Exit": exit,
        "PnL (₹)": pnl,
        "Timeframe": timeframe,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Reason": reason
    }

def save_trade_log(df, symbol):
    try:
        df.to_csv(f"{symbol.lower()}_trade_log.csv", index=False)
    except Exception:
        pass

def load_trade_log(symbol):
    try:
        return pd.read_csv(f"{symbol.lower()}_trade_log.csv")
    except:
        return pd.DataFrame()
