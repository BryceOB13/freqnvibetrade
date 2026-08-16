# I Tested Supertrend + EMA200 for 6 Years (Long AND Short) — It Made 2,529%

*Quant Tactics*

<iframe width="560" height="315" src="https://www.youtube.com/embed/53yqW60SDPk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Transcript

[0:00](https://youtube.com/watch?v=53yqW60SDPk&t=0s)

Most traders say supertrend is too slow. I tuned the settings, added one filter, backtested eight crypto pairs across six years, and turned $1,000 into $26,000. The strategy is built around two ideas. First, direction. We use the supertrend indicator with a length of eight and a multiplier of 4.0. When price flips above the supertrend line, that's a long signal. When it flips below, that's a short signal. One indicator, both directions. Second, a filter so we don't fight the bigger trend. We only take the long signal if price is above the 200-period EMA. We only take the short signal if price is below it. That's the entire entry logic. A trend flip on tuned settings confirmed by where price sits relative to the macro trend. Now, here's the part most people get wrong with trend following strategies, the exit. There's no take profit target here, no close at 5%. The trade rides until the supertrend flips back against it. If you're long

---

[1:01](https://youtube.com/watch?v=53yqW60SDPk&t=61s)

and the trend turns down, you're out. The only other way out is a safety net, an ATR-based stop loss set at 1.5 times the average true range below entry for longs. That's not the primary exit, it's just there in case price moves hard before the supertrend has a chance to react. I tested this on Freqtrade with the following setup. Exchange, Binance Futures because this strategy needs both long and short access. Pairs, eight of the highest market cap coins, BTC, ETH, SOL, and five others. Time frame, 4-hour candles. Time range, May 2020 to June 2026, just over six years. Max open trades, eight, one slot per pair. Here's what one set of rules and six years of data produced. 783 trades total. Win rate, 34.5%. That number looks low until you see the profit factor, 2.00. Wins are worth roughly twice as much as losses cost.

---

[2:02](https://youtube.com/watch?v=53yqW60SDPk&t=122s)

Max drawdown, 11%. Total return, 2,529%. $1,000 became just over 26,000. Buy and hold across the same eight pairs over the same period returned 1,489%. 358 long trades produced about 1,635% of that profit. 425 short trades produced roughly 894%. Both sides were profitable on their own. Neither one was just along for the ride. If you want to test this yourself, the full strategy code is available in the description below. Before going live with real capital, I'd recommend at least two months of paper trading first. Make sure the behavior matches what you see in the back test on your own setup. If you're serious about building systems like this, I also have a full freqtrade course where I cover everything step-by-step from zero to fully automated strategies running 24 hours a day. If you enjoyed this video, make sure to like it, subscribe to the channel, and turn on the notification

---

[3:02](https://youtube.com/watch?v=53yqW60SDPk&t=182s)

bell so you don't miss the next strategy breakdown. I'll see you in the next one.