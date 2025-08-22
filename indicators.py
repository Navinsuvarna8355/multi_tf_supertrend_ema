import pandas as pd
import numpy as np

def ema(series, period):
    return series.ewm(span=period, adjust=False).mean()

def compute_supertrend(df, atr_period=10, atr_mult=3):
    high = df["High"]
    low = df["Low"]
    close = df["Close"]
    tr = pd.concat([
        high - low,
        (high - close.shift()).abs(),
        (low - close.shift()).abs()
    ], axis=1).max(axis=1)
    atr = tr.rolling(atr_period).mean()
    hl2 = (high + low) / 2
    upperband = hl2 + atr_mult * atr
    lowerband = hl2 - atr_mult * atr
    supertrend = pd.Series(index=df.index)
    in_uptrend = pd.Series(True, index=df.index)

    for i in range(1, len(df)):
        if close[i] > lowerband[i - 1]:
            in_uptrend[i] = True
        elif close[i] < upperband[i - 1]:
            in_uptrend[i] = False
        supertrend[i] = lowerband[i] if in_uptrend[i] else upperband[i]

    return supertrend, in_uptrend
