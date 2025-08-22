import pandas as pd

def calculate_supertrend(df, period=7, multiplier=3):
    df['ATR'] = df['high'].rolling(period).max() - df['low'].rolling(period).min()
    hl2 = (df['high'] + df['low']) / 2
    df['UpperBand'] = hl2 + (multiplier * df['ATR'])
    df['LowerBand'] = hl2 - (multiplier * df['ATR'])
    df['Supertrend'] = df['close'] < df['LowerBand']
    return df

def calculate_ema(df, period=21):
    df['EMA'] = df['close'].ewm(span=period, adjust=False).mean()
    return df
