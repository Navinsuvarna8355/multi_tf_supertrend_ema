import ta

def generate_signals(close_series):
    ema = ta.trend.ema_indicator(close_series, window=21).iloc[-1]
    stc = ta.trend.STCIndicator(close=close_series, fillna=True).stc().iloc[-1]

    signal = "BUY" if close_series.iloc[-1] > ema and stc > ema else "SELL"
    reason = "Close > EMA and Supertrend bullish" if signal == "BUY" else "Close < EMA or Supertrend bearish"
    return signal, reason, ema
