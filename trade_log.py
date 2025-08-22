import pandas as pd
from datetime import datetime

class TradeLogger:
    def __init__(self, symbol, lot_size):
        self.symbol = symbol
        self.lot_size = lot_size
        self.trades = []

    def log_trade(self, signal_type, entry_price, exit_price, timeframe, reason=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pnl_per_lot = (exit_price - entry_price) * self.lot_size if signal_type == "BUY" else (entry_price - exit_price) * self.lot_size
        trade = {
            "Symbol": self.symbol,
            "Signal": signal_type,
            "Entry": entry_price,
            "Exit": exit_price,
            "PnL (₹)": round(pnl_per_lot, 2),
            "Timeframe": timeframe,
            "Timestamp": timestamp,
            "Reason": reason
        }
        self.trades.append(trade)

    def get_trade_df(self):
        return pd.DataFrame(self.trades)

    def export_csv(self, filename="trade_log.csv"):
        df = self.get_trade_df()
        df.to_csv(filename, index=False)
        return filename

    def cumulative_pnl(self):
        df = self.get_trade_df()
        return round(df["PnL (₹)"].sum(), 2)

    def reset_log(self):
        self.trades = []
