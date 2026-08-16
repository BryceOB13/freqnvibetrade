# Donchian Channel Strategy made 140% Profit! (Full Tutorial)

*Quant Tactics*

<iframe width="560" height="315" src="https://www.youtube.com/embed/CgYdfwrL1VQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Transcript

[0:00](https://youtube.com/watch?v=CgYdfwrL1VQ&t=0s)

Hey everyone. In today's video, we're exploring the Donian channel strategy. We'll go through the entire process from explaining how the strategy works to optimizing it with Freck Trade, an open-source trading bot, and finally running back tests to see how it performs. If you're looking for a complete beginnerfriendly Freck Trade tutorial, check out the link in the description below. Before we dive into the strategy, let's start by breaking down the key indicators we'll be using. One, Donian channel. The Donian channel is a trend following indicator that highlights the highest high and lowest low over a set period. By defining these upper and lower bands, it helps traders identify potential breakout points in the market. When the closing price crosses above the upper band, it indicates a potential upward breakout and we consider entering a long position. When the closing price crosses below the lower band, it signals a potential downward breakout and we consider

---

[1:01](https://youtube.com/watch?v=CgYdfwrL1VQ&t=61s)

entering a short position. While the Donian channel can be very effective in identifying trends, it is not perfect in markets that are moving sideways or experiencing low volatility, the price may cross the bands frequently, generating false signals. These false signals can lead to losing trades if used in isolation. To improve accuracy, the Donian channel is often combined with other indicators such as the average directional index, ADX, to confirm the strength of a trend. 2 ADX. The average directional index or ADX is a powerful technical indicator that helps us determine whether the market is trending or moving sideways. It's important to note that ADX does not indicate the direction of the trend. It only measures the strength of the trend. The ADX value ranges from 0 to 100. A value below 20 suggests a weak trend or a sideways market. A value above 20

---

[2:03](https://youtube.com/watch?v=CgYdfwrL1VQ&t=123s)

indicates a strong trend, whether it's moving upward or downward. By checking the ADX before entering trades, we can confirm that the market is in a meaningful trend. Three, choppiness index. The choppiness index or chop is an indicator that helps us identify whether the market is trending or ranging. It's particularly useful for avoiding trades during periods of low momentum or sideways price movement. The chop value typically ranges from 0 to 100. A chop value above 40 indicates a choppy or sideways market where trends are weak and trading signals are less reliable. A chop value below 40 suggests that the market is trending either upward or downward, making it a better environment for trend following strategies like the Donian channel. By using the choppiness index in combination with the Donian channel and ADX, we can filter out trades in indecisive or sideways markets. Now that we understand how each

---

[3:03](https://youtube.com/watch?v=CgYdfwrL1VQ&t=183s)

indicator works, let's walk through how we combine them to identify trade setups and generate signals. To enter a long position, we wait for all of the following conditions to be met. Price crosses above the Donian channel upper band. This indicates a potential breakout to the upside, signaling the start of a new upward trend. A DX is above 20. This confirms that the market is in a strong trend, helping us avoid false breakouts in sideways or weak markets. Choppiness index is below 40. This shows that the market is trending rather than moving sideways, which increases the reliability of our trade. Price is above the 50 period EMA. This confirms that the overall market momentum is bullish and aligns with our long position. Once all of these conditions are met, we enter the long trade on the next candle. After entering the trade, we manage risk using an ATRbased trailing stop-loss. In this

---

[4:04](https://youtube.com/watch?v=CgYdfwrL1VQ&t=244s)

strategy, we use ATR multiplied by three. This means that the stop loss is dynamically adjusted based on market volatility, allowing the trade to ride the trend while protecting our capital. When the price hits the trailing stop-loss, we exit the trade, securing profits or limiting losses. Entering a short position works similarly to a long trade, but with the conditions flipped. Price crosses below the Donian channel lower band. This indicates a potential downward breakout and the start of a new downtrend. A DX is above 20 confirms that the market is in a strong trend, avoiding weak or sideways moves. Choppiness index is below 40 shows that the market is trending, not moving sideways, making the signal more reliable. Prices below the 50 period EMA confirms that overall market momentum is bearish and aligns with our short trade. Once all conditions are met, we enter the short trade on the next candle. We also use

---

[5:05](https://youtube.com/watch?v=CgYdfwrL1VQ&t=305s)

the ATR trailing stop-loss to manage risk. This allows the trade to follow the trend while protecting our capital. When the price hits the trailing stop-loss, we exit the trade. Now that we understand the strategy, let's move on to optimization using f trade. We'll test on the 1 hour time frame and split the data into in sample 8 months for tuning the strategy out of sample 4 months for testing on unseen data. The key parameters we'll focus on optimizing include donian period, number of periods for the donian channel, EMA period, length of the EMA to confirm trend direction, a DX threshold, minimum ADX to confirm a strong trend and avoid weak markets. Chop threshold, maximum choppiness index to identify trending markets and skip sideways conditions. ATR multiplier sets the ATR based

---

[6:06](https://youtube.com/watch?v=CgYdfwrL1VQ&t=366s)

trailing stop distance. We'll use Freck Trade's hyperopt feature to find the best combination of these parameters. Once optimization is done, we'll run a full back test to see how the strategy performs with the best parameters in place. All right, let's take a closer look at the back testing results. We tested the strategy on ETH perpetual futures using a 1-hour time frame over the past year with the optimized settings. Here's what we observed. The strategy achieved a total return of 140%. By comparison, the market itself saw a return of around minus 32% during the same period. The maximum draw down was 10.42%. Which shows that while the strategy did experience some retracements, it effectively managed risk and maintained overall profitability. Next, we'll review a visual summary of these results. The strategy was optimized with eight months of insample data and then tested on four months of outof sample data ensuring it performs

---

[7:09](https://youtube.com/watch?v=CgYdfwrL1VQ&t=429s)

reliably on unseen market conditions and isn't just curve fitted to historical data. If you'd like access to the full strategy file along with the complete step-by-step fra tutorial, it's available to supporters through the link in the description. It's a great way to support the channel and in return you get everything you need to build, run, and customize this strategy on your own. There's also a pair optimized version which allows you to apply the strategy across multiple trading pairs, each with its own optimized parameters for improved performance. If you found this video useful, remember to subscribe, enable notifications, and share it with others who might benefit from it. Thanks for tuning in. See you in the next video.