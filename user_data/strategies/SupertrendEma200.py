"""SupertrendEma200 — Bucket A benchmark (robust low-knob trend follower).

Source: Quant Tactics, "I Tested Supertrend + EMA200 for 6 Years (Long AND
Short) — It Made 2,529%" (https://www.youtube.com/watch?v=53yqW60SDPk).
Transcript: user_data/research/transcripts/supertrend-ema200-53yqW60SDPk.md

Rules from the video (4h timeframe):
  Long entry:  Supertrend(length 8, multiplier 4.0) flips bullish
               AND close > EMA(200)
  Long exit:   Supertrend flips bearish (ride until the flip; no take-profit)
  Safety net:  ATR * 1.5 initial stoploss below entry.
  Shorts are fully mirrored.

Role in this repo: benchmark. Two effective knobs — hardest of the four
strategies to overfit.
"""

import numpy as np
import talib.abstract as ta
from pandas import DataFrame

from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    IStrategy,
    stoploss_from_absolute,
)


def supertrend(dataframe: DataFrame, period: int, multiplier: float):
    hl2 = (dataframe["high"] + dataframe["low"]) / 2
    atr = ta.ATR(dataframe, timeperiod=period)
    upper = (hl2 + multiplier * atr).to_numpy()
    lower = (hl2 - multiplier * atr).to_numpy()
    close = dataframe["close"].to_numpy()

    n = len(close)
    st = np.full(n, np.nan)
    direction = np.ones(n, dtype=np.int64)
    fu = upper.copy()
    fl = lower.copy()

    for i in range(1, n):
        if np.isnan(upper[i]):
            continue
        if np.isnan(fu[i - 1]) or np.isnan(fl[i - 1]):
            fu[i] = upper[i]
            fl[i] = lower[i]
            st[i] = fl[i]
            continue
        fu[i] = (
            upper[i]
            if (upper[i] < fu[i - 1]) or (close[i - 1] > fu[i - 1])
            else fu[i - 1]
        )
        fl[i] = (
            lower[i]
            if (lower[i] > fl[i - 1]) or (close[i - 1] < fl[i - 1])
            else fl[i - 1]
        )
        if close[i] > fu[i]:
            direction[i] = 1
        elif close[i] < fl[i]:
            direction[i] = -1
        else:
            direction[i] = direction[i - 1]
        st[i] = fl[i] if direction[i] == 1 else fu[i]

    return st, direction


class SupertrendEma200(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "4h"
    can_short = True

    stoploss = -0.30
    use_custom_stoploss = True
    minimal_roi = {}
    trailing_stop = False
    use_exit_signal = True

    startup_candle_count = 400
    process_only_new_candles = True

    st_period = IntParameter(6, 14, default=8, space="buy")
    st_mult = DecimalParameter(2.0, 5.0, default=4.0, decimals=1, space="buy")
    ema_period = IntParameter(150, 250, default=200, space="buy")
    atr_stop_mult = DecimalParameter(1.0, 3.0, default=1.5, decimals=1, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        st, direction = supertrend(
            dataframe, self.st_period.value, self.st_mult.value
        )
        dataframe["st_dir"] = direction
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=self.ema_period.value)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        flipped_up = (dataframe["st_dir"] == 1) & (dataframe["st_dir"].shift(1) == -1)
        flipped_dn = (dataframe["st_dir"] == -1) & (dataframe["st_dir"].shift(1) == 1)

        dataframe.loc[
            flipped_up
            & (dataframe["close"] > dataframe["ema200"])
            & (dataframe["volume"] > 0),
            "enter_long",
        ] = 1
        dataframe.loc[
            flipped_dn
            & (dataframe["close"] < dataframe["ema200"])
            & (dataframe["volume"] > 0),
            "enter_short",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        flipped_up = (dataframe["st_dir"] == 1) & (dataframe["st_dir"].shift(1) == -1)
        flipped_dn = (dataframe["st_dir"] == -1) & (dataframe["st_dir"].shift(1) == 1)

        dataframe.loc[flipped_dn, "exit_long"] = 1
        dataframe.loc[flipped_up, "exit_short"] = 1
        return dataframe

    def custom_stoploss(self, pair: str, trade: Trade, current_time,
                        current_rate: float, current_profit: float,
                        after_fill: bool, **kwargs):
        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        signal = df.loc[df["date"] <= trade.open_date_utc]
        if signal.empty:
            return None
        atr = signal.iloc[-1]["atr"]
        dist = self.atr_stop_mult.value * atr
        stop_price = (
            trade.open_rate + dist if trade.is_short else trade.open_rate - dist
        )
        return stoploss_from_absolute(
            stop_price, current_rate, is_short=trade.is_short, leverage=trade.leverage
        )

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs) -> float:
        return 1.0
