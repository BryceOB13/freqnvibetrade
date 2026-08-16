# ADX & Moving Averages: Freqtrade Crypto Strategy That Actually Works!

*Quant Tactics*

<iframe width="560" height="315" src="https://www.youtube.com/embed/S6l3nZ3YkWw" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Transcript

[0:00](https://youtube.com/watch?v=S6l3nZ3YkWw&t=0s)

hey everyone in today's video we're testing a powerful yet straightforward trading strategy that combines the moving average with the adx to spot high probability trade opportunities we'll code the entire strategy in Python optimize it using freck trade and run back tests to evaluate its Effectiveness so let's Dive Right In let's start with the foundation of this strategy moving averages we'll be using a 20 period SMA but with a Twist instead of the usual closing price the 20 High SMA is based on the high price of each candle and the 20 low SMA is based on the low price if the price closes above the 20 High SMA it signals a potential long trade if the price closes below the 20 low SMA it signals a potential short trade now to avoid trading against the trend we add a 100 period SMA as a trend filter

---

[1:00](https://youtube.com/watch?v=S6l3nZ3YkWw&t=60s)

we only go long when the price is above the 100 SMA and we only go short when the price is below the 100 SMA this keeps us trading in the right direction reducing unnecessary losses in choppy markets next we bring in the average directional index adx a key tool for measuring Trend strength unlike moving averages which show price Direction adx tells us whether a trend is strong enough to trade if the adx is above 25 it means the trend is strong and we have a better chance of catching a solid move if it's below 25 the market lacks momentum and we avoid taking trades finally we use the average true range to filter out low volatility periods ATR measures how much the price moves on average over time a high ATR means strong price movements good for trading a low ATR signals a quiet Market

---

[2:03](https://youtube.com/watch?v=S6l3nZ3YkWw&t=123s)

which can lead to false breakouts by avoiding trades during low volatility we increase the chances of catching real momentum based moves now that we've covered the key indicators in our strategy let's put them all together and see how we can apply them to analyze Trends and generate our trading signals to enter a long trade we need to meet all of these conditions one the close price must cross above the 20 High SMA two the close price must also be above the 100 SMA confirming we're in an uptrend three the adx must be above 25 which confirms a strong trending Market no weak Trends allowed since we're working on a 4-Hour time frame we'll also check the 1-day ATR it must be above 3% of the current price which ensures there's enough volatility for a reliable trade once all of these conditions are met we'll enter the long trade on the next

---

[3:04](https://youtube.com/watch?v=S6l3nZ3YkWw&t=184s)

candle to exit the long trade we'll use the following condition we don't exit immediately when the price crosses below the 20 low SMA doing so would be too quick and could lead to unnecessary exits instead we wait for additional confirmation by combining it with the ATR multiplied by 0.7 before closing the position this ensures that we're not reacting to small pullbacks but instead exiting only when the market truly shows signs of reversing locking in our profits to enter a short trade we need to meet these conditions one the close price must cross below the 20 low SMA two the close price must also be below the 100 SMA confirming we're in a downtrend three the adx must be above 25 ensuring a strong Trend the 1day ATR must be above 3% of the current price confirming sufficient volatility for a

---

[4:04](https://youtube.com/watch?v=S6l3nZ3YkWw&t=244s)

reliable trade once all conditions are met we'll enter the short trade on the next candle we don't exit immediately when the price crosses above the 20 High SMA this could result in primature exits instead we wait for additional confirmation by combining it with the ATR multiplied by 0.7 before closing the position this helps us ride strong Trends while avoiding false exit and noise in the market now that we've covered the strategy let's take it a step further and see how to optimize and back test it using fre trade a free open-source crypto trading bot built with python if you want to learn more about fre trade check out the link in the description for a complete fre trade course here's our approach we'll test our strategy on the 4-Hour time frame we're splitting the data into two parts in Sample data 8 months we'll use this data to fine-tune the parameters of our strategy out of sample data 4 months

---

[5:08](https://youtube.com/watch?v=S6l3nZ3YkWw&t=308s)

this data will test our optimized strategy on new unseen data to see how well it holds up in real market conditions we'll focus on optimizing the following important parameters short SMA period adjust the sensitivity of the 20 high and 20 low SMA long SEMA period helps to find the overall trend Direction addex sub period F Tunes how we measure Trend strength addex threshold ensures we're only trading in strong market trends ATR maltt controls how much ATR volatility filtering is applied to exits ATR price threshold ensures the one-day ATR is high enough for a reliable trade setup cross rolling window defines how long the EMA crossover remain remains valid before a signal is confirmed we'll use FR trade's hyper op feature to find the best parameter combination for maximizing profits while minimizing risk once we've

---

[6:10](https://youtube.com/watch?v=S6l3nZ3YkWw&t=370s)

optimized the settings we'll run a back test to check how well the strategy performs with the new parameters all right now let's dive into the back testing results for our strategy we tested it on GRT Perpetual Futures using a 4-Hour time frame over one full year and here's how it performed total profit of a solid 475 return long positions contributed an impressive 234. short positions added another 241 per to the total Market change minus 1% over the same period but what about risk maximum draw down MDD kept to just 11% which is well within a reasonable range for a high performing strategy and here's the cumulative profit graph as you can see it shows a steady upward Trend exactly what we want in a robust trading strategy we used 8 months of insample data to fine-tune our

---

[7:10](https://youtube.com/watch?v=S6l3nZ3YkWw&t=430s)

parameters four months of out of sample data to verify its performance on unseen market conditions if you'd like to explore this strategy further check out the link in the description below I've also developed a pair optimized version of the strategy this version allows multiple Trading pairs to run within a single setup each using its own optimized parameters for better performance it helps diversify risk and reduce maximum draw down if you found this video helpful don't forget to subscribe hit the notification Bell and share it with your friends on WhatsApp Facebook or Twitter to help support the channel thanks so much for watching and I'll see you in the next one