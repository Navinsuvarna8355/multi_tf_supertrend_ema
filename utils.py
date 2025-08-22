import pandas as pd

def get_live_price(symbol):
    # Dummy live price — replace with API
    return 24870.25 if symbol == "NIFTY" else 55151.75

def get_ohlc(symbol, timeframe):
    filename = f"{symbol}_{timeframe}.csv"
    try:
        df = pd.read_csv(filename)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        raise Exception(f"CSV file not found: {filename}")
