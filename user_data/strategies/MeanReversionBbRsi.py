"""MeanReversionBbRsi — Bucket B (mean-reversion, long-term bag money).

Source: Quant Tactics, "Mean Reversion Trading Strategy Explained &
Backtested" (https://www.youtube.com/watch?v=c9-SIpy3dEw).
Transcript: user_data/research/transcripts/mean-reversion-bb-rsi-adx-c9-SIpy3dEw.md

Rules from the video (1h trading timeframe, 4h informative):
  Long entry:  4h RSI > 55 (trend filter — trade WITH the higher trend)
               AND 1h ADX > 20 AND 4h ADX > 25
               AND close below the lower Bollinger Band (oversold snap-back)
  Long exit:   close above the upper Bollinger Band
  Stoploss:    signal-candle close minus 4.5 * ATR (volatility buffer)
  Shorts are fully mirrored (4h RSI < 45, entry above upper band).

Design decisions not in the video (documented for other agents):
  - The ATR stop is implemented via custom_stoploss anchored to the ATR at
    trade entry; fallback hard stop is -30% (should never be the binding
    constraint at 1x leverage).
  - Leverage fixed at 1x.
"""

import talib.abstract as ta
from pandas import DataFrame
from technical import qtpylib

from freqtrade.persistence import Trade
from freqtrade.strategy import (
    DecimalParameter,
    IntParameter,
    IStrategy,
    merge_informative_pair,
    stoploss_from_absolute,
)


class MeanReversionBbRsi(IStrategy):
    INTERFACE_VERSION = 3

    timeframe = "1h"
    informative_timeframe = "4h"
    can_short = True

    stoploss = -0.30
    use_custom_stoploss = True
    minimal_roi = {}
    trailing_stop = False
    use_exit_signal = True

    startup_candle_count = 120
    process_only_new_candles = True

    # --- Hyperopt space (params named in the video) ---
    bb_period = IntParameter(15, 30, default=20, space="buy")
    bb_std = DecimalParameter(1.5, 3.0, default=2.0, decimals=1, space="buy")
    htf_rsi_long = IntParameter(50, 65, default=55, space="buy")
    htf_rsi_short = IntParameter(35, 50, default=45, space="buy")
    adx_threshold = IntParameter(15, 30, default=20, space="buy")
    htf_adx_threshold = IntParameter(20, 35, default=25, space="buy")
    atr_stop_mult = DecimalParameter(2.0, 6.0, default=4.5, decimals=1, space="sell")

    def informative_pairs(self):
        return [(pair, self.informative_timeframe) for pair in self.dp.current_whitelist()]

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        inf = self.dp.get_pair_dataframe(
            pair=metadata["pair"], timeframe=self.informative_timeframe
        )
        inf["rsi"] = ta.RSI(inf, timeperiod=14)
        inf["adx"] = ta.ADX(inf, timeperiod=14)
        dataframe = merge_informative_pair(
            dataframe, inf[["date", "rsi", "adx"]],
            self.timeframe, self.informative_timeframe, ffill=True,
        )

        dataframe["adx"] = ta.ADX(dataframe, timeperiod=14)
        dataframe["atr"] = ta.ATR(dataframe, timeperiod=14)

        for p in self.bb_period.range:
            mid = dataframe["close"].rolling(p).mean()
            std = dataframe["close"].rolling(p).std()
            dataframe[f"bb_mid_{p}"] = mid
            dataframe[f"bb_std_{p}"] = std
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        mid = dataframe[f"bb_mid_{self.bb_period.value}"]
        std = dataframe[f"bb_std_{self.bb_period.value}"]
        lower = mid - self.bb_std.value * std
        upper = mid + self.bb_std.value * std

        trend_ok = (
            (dataframe["adx"] > self.adx_threshold.value)
            & (dataframe["adx_4h"] > self.htf_adx_threshold.value)
            & (dataframe["volume"] > 0)
        )

        dataframe.loc[
            (dataframe["rsi_4h"] > self.htf_rsi_long.value)
            & (dataframe["close"] < lower)
            & trend_ok,
            "enter_long",
        ] = 1

        dataframe.loc[
            (dataframe["rsi_4h"] < self.htf_rsi_short.value)
            & (dataframe["close"] > upper)
            & trend_ok,
            "enter_short",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        mid = dataframe[f"bb_mid_{self.bb_period.value}"]
        std = dataframe[f"bb_std_{self.bb_period.value}"]
        lower = mid - self.bb_std.value * std
        upper = mid + self.bb_std.value * std

        dataframe.loc[(dataframe["close"] > upper), "exit_long"] = 1
        dataframe.loc[(dataframe["close"] < lower), "exit_short"] = 1
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
