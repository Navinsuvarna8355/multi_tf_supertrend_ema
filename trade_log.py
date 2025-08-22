import pandas as pd

def load_trade_log(symbol):
    try:
        df = pd.read_csv(f"data/{symbol.lower()}_trade_log.csv")
        if df.empty or df.columns.size == 0:
            return pd.DataFrame()
        return df
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return pd.DataFrame()

def save_trade_log(symbol, df):
    df.to_csv(f"data/{symbol.lower()}_trade_log.csv", index=False)
