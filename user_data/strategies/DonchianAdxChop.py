"""DonchianAdxChop — Bucket A benchmark (classic breakout).

Source: Quant Tactics, "Donchian Channel Strategy made 140% Profit!"
(https://www.youtube.com/watch?v=CgYdfwrL1VQ).
Transcript: user_data/research/transcripts/donchian-channel-CgYdfwrL1VQ.md

Rules from the video (1h timeframe):
  Long entry:  close crosses above the Donchian upper band (prior N-high)
               AND ADX > 20
               AND Choppiness Index < 40 (market trending, not sideways)
               AND close > EMA(50)
  Exit:        ATR * 3 trailing stop only (no signal exit).
  Shorts are fully mirrored.

Role in this repo: benchmark. If AdxSmaBreakout can't beat this simpler
strategy out-of-sample, the extra complexity isn't earning its keep.
"""

import numpy as np
import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib

from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    IStrategy,
    stoploss_from_absolute,
)


def choppiness(dataframe: DataFrame, period: int = 14):
    atr1 = ta.ATR(dataframe, timeperiod=1)
    atr_sum = atr1.rolling(period).sum()
    hh = dataframe["high"].rolling(period).max()
    ll = dataframe["low"].rolling(period).min()
    rng = (hh - ll).replace(0, np.nan)
    return 100 * np.log10(atr_sum / rng) / np.log10(period)


class DonchianAdxChop(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "1h"
    can_short = True

    stoploss = -0.30
    use_custom_stoploss = True
    minimal_roi = {}
    trailing_stop = False
    use_exit_signal = True

    startup_candle_count = 120
    process_only_new_candles = True

    donchian_period = IntParameter(10, 40, default=20, space="buy")
    ema_period = IntParameter(30, 100, default=50, space="buy")
    adx_threshold = IntParameter(15, 30, default=20, space="buy")
    chop_threshold = IntParameter(30, 55, default=40, space="buy")
    atr_trail_mult = DecimalParameter(1.5, 5.0, default=3.0, decimals=1, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        for p in self.donchian_period.range:
            dataframe[f"dc_upper_{p}"] = dataframe["high"].rolling(p).max().shift(1)
            dataframe[f"dc_lower_{p}"] = dataframe["low"].rolling(p).min().shift(1)
        for p in self.ema_period.range:
            dataframe[f"ema_{p}"] = ta.EMA(dataframe, timeperiod=p)

        dataframe["adx"] = ta.ADX(dataframe, timeperiod=14)
        dataframe["chop"] = choppiness(dataframe, 14)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        upper = dataframe[f"dc_upper_{self.donchian_period.value}"]
        lower = dataframe[f"dc_lower_{self.donchian_period.value}"]
        ema = dataframe[f"ema_{self.ema_period.value}"]

        filters = (
            (dataframe["adx"] > self.adx_threshold.value)
            & (dataframe["chop"] < self.chop_threshold.value)
            & (dataframe["volume"] > 0)
        )

        dataframe.loc[
            (dataframe["close"] > upper) & (dataframe["close"] > ema) & filters,
            "enter_long",
        ] = 1
        dataframe.loc[
            (dataframe["close"] < lower) & (dataframe["close"] < ema) & filters,
            "enter_short",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe

    def custom_stoploss(self, pair: str, trade: Trade, current_time,
                        current_rate: float, current_profit: float,
                        after_fill: bool, **kwargs):
        df, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if df.empty:
            return None
        atr = df.iloc[-1]["atr"]
        dist = self.atr_trail_mult.value * atr
        stop_price = (
            current_rate + dist if trade.is_short else current_rate - dist
        )
        return stoploss_from_absolute(
            stop_price, current_rate, is_short=trade.is_short, leverage=trade.leverage
        )

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs) -> float:
        return 1.0
