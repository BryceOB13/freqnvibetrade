"""AdxSmaBreakout — Bucket A (trend/breakout, "gambling money").

Source: Quant Tactics, "ADX & Moving Averages: Freqtrade Crypto Strategy
That Actually Works!" (https://www.youtube.com/watch?v=S6l3nZ3YkWw).
Transcript: user_data/research/transcripts/adx-moving-averages-S6l3nZ3YkWw.md

Rules from the video:
  Long entry:  close crosses above SMA(high, 20)  [within a rolling window]
               AND close > SMA(close, 100)
               AND ADX > 25
               AND daily ATR > 3% of price
  Long exit:   close < SMA(low, 20) - 0.7 * ATR   (buffered, not immediate)
  Shorts are fully mirrored.

Design decisions not specified in the video (documented for other agents):
  - Exit buffer uses the 4h ATR(14); the daily ATR is only the volatility
    entry filter, matching the video's phrasing.
  - Fixed stoploss -15% as a disaster stop; the video never states one.
    Kept fixed (not hyperopted) to limit overfitting surface.
  - Leverage fixed at 1x. The video trades GRT perps with leverage; we
    validate the edge unlevered first.
"""

import numpy as np
import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib

from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    IStrategy,
    merge_informative_pair,
)


class AdxSmaBreakout(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "4h"
    can_short = True

    # Disaster stop only — exits are signal-driven.
    stoploss = -0.15
    minimal_roi = {}
    trailing_stop = False
    use_exit_signal = True
    exit_profit_only = False

    startup_candle_count = 220
    process_only_new_candles = True

    # --- Hyperopt space (the 7 knobs named in the video) ---
    short_sma = IntParameter(10, 30, default=20, space="buy")
    long_sma = IntParameter(60, 150, default=100, space="buy")
    adx_period = IntParameter(10, 20, default=14, space="buy")
    adx_threshold = IntParameter(20, 32, default=25, space="buy")
    atr_pct_threshold = DecimalParameter(0.02, 0.05, default=0.03, decimals=3, space="buy")
    cross_window = IntParameter(1, 5, default=1, space="buy")
    atr_mult = DecimalParameter(0.3, 1.5, default=0.7, decimals=1, space="sell")

    def informative_pairs(self):
        return [(pair, "1d") for pair in self.dp.current_whitelist()]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Daily ATR for the volatility filter
        inf = self.dp.get_pair_dataframe(pair=metadata["pair"], timeframe="1d")
        inf["atr_1d"] = ta.ATR(inf, timeperiod=14)
        dataframe = merge_informative_pair(
            dataframe, inf[["date", "atr_1d"]], self.timeframe, "1d", ffill=True
        )

        for p in self.short_sma.range:
            dataframe[f"sma_high_{p}"] = ta.SMA(dataframe["high"], timeperiod=p)
            dataframe[f"sma_low_{p}"] = ta.SMA(dataframe["low"], timeperiod=p)
        for p in self.long_sma.range:
            dataframe[f"sma_long_{p}"] = ta.SMA(dataframe["close"], timeperiod=p)
        for p in self.adx_period.range:
            dataframe[f"adx_{p}"] = ta.ADX(dataframe, timeperiod=p)

        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        sma_high = dataframe[f"sma_high_{self.short_sma.value}"]
        sma_low = dataframe[f"sma_low_{self.short_sma.value}"]
        sma_long = dataframe[f"sma_long_{self.long_sma.value}"]
        adx = dataframe[f"adx_{self.adx_period.value}"]
        w = self.cross_window.value

        crossed_up = qtpylib.crossed_above(dataframe["close"], sma_high)
        crossed_dn = qtpylib.crossed_below(dataframe["close"], sma_low)
        recent_cross_up = crossed_up.rolling(w).max() > 0
        recent_cross_dn = crossed_dn.rolling(w).max() > 0

        vol_ok = dataframe["atr_1d_1d"] > (
            self.atr_pct_threshold.value * dataframe["close"]
        )

        dataframe.loc[
            recent_cross_up
            & (dataframe["close"] > sma_high)
            & (dataframe["close"] > sma_long)
            & (adx > self.adx_threshold.value)
            & vol_ok
            & (dataframe["volume"] > 0),
            "enter_long",
        ] = 1

        dataframe.loc[
            recent_cross_dn
            & (dataframe["close"] < sma_low)
            & (dataframe["close"] < sma_long)
            & (adx > self.adx_threshold.value)
            & vol_ok
            & (dataframe["volume"] > 0),
            "enter_short",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        sma_high = dataframe[f"sma_high_{self.short_sma.value}"]
        sma_low = dataframe[f"sma_low_{self.short_sma.value}"]
        buffer = self.atr_mult.value * dataframe["atr"]

        dataframe.loc[
            (dataframe["close"] < (sma_low - buffer)) & (dataframe["volume"] > 0),
            "exit_long",
        ] = 1
        dataframe.loc[
            (dataframe["close"] > (sma_high + buffer)) & (dataframe["volume"] > 0),
            "exit_short",
        ] = 1
        return dataframe

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs) -> float:
        return 1.0
