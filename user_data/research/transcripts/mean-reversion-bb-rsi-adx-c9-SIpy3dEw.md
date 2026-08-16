# Mean Reversion Trading Strategy Explained & Backtested – 179% Profit

*Quant Tactics*

<iframe width="560" height="315" src="https://www.youtube.com/embed/c9-SIpy3dEw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Transcript

[0:00](https://youtube.com/watch?v=c9-SIpy3dEw&t=0s)

Hey everyone. In today's video, we're testing a mean reversion strategy. We'll walk through the entire process from explaining how the strategy works to optimizing it using Freck Trade, an open-source trading bot, and finally running back tests to see how it performs. If you're looking for a complete beginnerfriendly Freck Trade tutorial, check out the link in the description below. Before we dive into the strategy, let's first break down the key indicators we'll be using. One, Ballinger bands. Ballinger bands are one of the most popular technical indicators used by traders to analyze volatility and price movement. They were developed by John Ballinger and are composed of three lines. Middle band. This is usually a 20 period simple moving average. It shows the average price over the past 20 candles. Upper band, this is the middle band plus two standard deviations. Lower band, this is the middle band

---

[1:00](https://youtube.com/watch?v=c9-SIpy3dEw&t=60s)

minus two standard deviations. Ballinger bands are often used for mean reversion strategies. When the closing price falls below the lower band, it may indicate the asset is oversold. So, we consider entering a long position. When the price crosses above the upper band, it may suggest the asset is overbought. So, we consider entering a short position. However, we can't rely on Ballinger bands alone. We need to combine them with other indicators to avoid false signals. Two, RSI, the relative strength index, helps us measure the strength and momentum of price movements. While RSI is often used to identify overbought and oversold conditions, in this strategy, we use it as a trend filter instead. Since we're trading on the 1 hour time frame, the 1 hour RSI can be noisy and less reliable due to short-term fluctuations. That's why we use the RSI on a higher time frame, 4hour, to identify the

---

[2:02](https://youtube.com/watch?v=c9-SIpy3dEw&t=122s)

broader trend. If the 4hour RSI is above 55, we only look for long positions. If the 4hour RSI is below 45, we only look for short positions. This approach helps us stay aligned with the overall market direction and avoid trading against the trend. 3. Ax. The average directional index is a powerful indicator that tells us whether the market is trending or ranging, but it doesn't indicate the direction of the trend. It ranges from 0 to 100. An ADX value below 20 suggests a weak trend or sideways choppy market. An ADX value above 20 indicates a strong trend, whether it's upward or downward. We apply ADX to both the 4hour time frame and the 1 hour trading time frame. To confirm a valid trend, we want the ADX to be above 20. This helps us avoid trading in sideways or choppy markets.

---

[3:03](https://youtube.com/watch?v=c9-SIpy3dEw&t=183s)

Now that we understand how each indicator works, let's walk through how we combine them to identify trade setups and generate signals. To enter a long position, we wait for all of the following conditions to be met. 4hour RSI is above 55. This indicates the overall market trend is bullish and we should only consider long trades. The ADX must be above 20 on the 1 hour time frame and above 25 on the 4hour time frame. This confirms there is enough trend strength and momentum across both short and medium-term charts. The closing price must fall below the lower Ballinger band on the 1-hour chart. This suggests the market is oversold and a potential reversal to the mean may occur. Once all of these conditions are met, we enter the long trade on the next candle. This approach allows us to combine momentum, volatility, and trend confirmation, increasing the probability of a high quality setup. After entering the trade, we set the stop loss just

---

[4:03](https://youtube.com/watch?v=c9-SIpy3dEw&t=243s)

below the low of the signal candle to give the trade enough breathing room and avoid being stopped out by small fluctuations. We further subtract 4.5 times the ATR, average true range, from the closing price of the signal candle. We exit the trade when the price closes above the upper Ballinger band. This typically indicates the price has become overbought and a pullback may follow. By exiting at this point, we lock in profits before the market reverses. To enter a short position, all of the following conditions must be met. 4hour RSI is below 45. Indicates a bearish trend. ADX is above 20 on the 1 hour chart and above 25 on the 4hour chart. Confirms trend strength. Price closes above the upper Ballinger band. Suggests overbought condition. We enter the short trade on the next candle. Stop loss is set just above the high of the signal candle plus 4.5 times

---

[5:05](https://youtube.com/watch?v=c9-SIpy3dEw&t=305s)

ATR for volatility buffer. Take profit when price closes below the lower Ballinger band indicates a potential reversal. Now that we understand the strategy, let's move on to optimization using fret trade. We'll test on the 1 hour time frame and split the data into in sample 8 months. For tuning the strategy, out of sample 4 months for testing on unseen data, key parameters to optimize include BB period and BBSTDS control the length and width of the Ballinger bands, HTF RSI threshold helps define the RSI level used to filter trade direction. HTFA DX threshold and a DX threshold ensure sufficient trend strength on both time frames. ATR multiplier determines how far the stop loss is placed from the signal candle. We'll use Freck Trade's hyper opt feature to find the best combination of these parameters. Once optimization is

---

[6:07](https://youtube.com/watch?v=c9-SIpy3dEw&t=367s)

done, we'll run a full back test to see how the strategy performs with the best parameters in place. All right, let's take a closer look at the back testing results. We ran the back test on near perpetual futures using the 1-hour time frame over the past year with the optimized settings. Here's what we found. The strategy delivered a total profit of 179%. For comparison, the market itself returned around -66% during the same period. The maximum draw down was 19.318%. which means the strategy did experience some pullbacks, but overall it managed risk well and stayed profitable. Now, let's take a look at the visual summary of these results. This strategy was optimized using 8 months of insample data, then tested on 4 months of outof sample data that helps ensure it's not just curve fitted to the past, but also performs well in new unseen market

---

[7:09](https://youtube.com/watch?v=c9-SIpy3dEw&t=429s)

conditions. If you'd like access to the full strategy file along with the complete step-by-step fract tutorial, it's available to supporters through the link in the description. It's a great way to support the channel, and in return, you get everything you need to build, run, and customize this strategy on your own. There's also a pair optimized version available, so you can run it across multiple trading pairs, each with its own fine-tuned parameters for better performance. If you found this video helpful, don't forget to subscribe, turn on notifications, and share it with your friends who might find it useful, too. Thanks for watching, and I'll catch you in the next one.