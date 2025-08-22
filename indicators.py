import pandas as pd
import ta

def add_indicators(df):
    df["EMA"] = ta.trend.ema_indicator(df["close"], window=20)
    df["Supertrend"] = ta.trend.stc(df["close"], fillna=True)
    return df

def generate_signals(df):
    df["Signal"] = "Hold"
    df.loc[(df["close"] > df["EMA"]) & (df["Supertrend"] > df["close"]), "Signal"] = "Buy"
    df.loc[(df["close"] < df["EMA"]) & (df["Supertrend"] < df["close"]), "Signal"] = "Sell"
    return df

