import pandas as pd

def generate_signals(close_series):
    ema = pd.Series(close_series).ewm(span=10).mean().iloc[-1]
    signal = "BUY" if close_series[-1] > ema else "SELL"
    reason = "Close > EMA (bullish)" if signal == "BUY" else "Close < EMA or bearish trend"
    return signal, reason, ema
