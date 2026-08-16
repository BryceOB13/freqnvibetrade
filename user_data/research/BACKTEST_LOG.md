# Backtest Log

Append-only. Every backtest/hyperopt run gets logged: date, strategy, window, params, result.
Conventions: IS (in-sample, tune here) = `20250801-20260401` · OOS (out-of-sample, validate ONLY) = `20260401-20260816`.
All runs: OKX futures data, 1x leverage, 1000 USDT paper wallet, `max_open_trades=1`, pair = GRT/USDT:USDT unless noted.

---

## 2026-08-16 — Initial strategy lab: 4 transcript-derived strategies (Claude/Zo)

Setup: freqtrade 2026.8-dev (repo venv), data OKX 20250501-20260816 (1h/4h/1d).
Hyperopt: SharpeHyperOptLoss, spaces buy+sell, 400 epochs, random-state 42, IS window only.

### Scoreboard (GRT/USDT:USDT perps)

| Strategy | TF | Defaults IS | Defaults OOS | Tuned IS | **Tuned OOS** |
|---|---|---|---|---|---|
| AdxSmaBreakout | 4h | -27.4% | — | +72.7% (15 tr, PF 3.90) | **+14.6%** (8 tr, PF 1.86) |
| SupertrendEma200 | 4h | +36.1% | -3.7% | +21.0% (12 tr, PF 1.60) | **+29.3%** (4 tr, PF 4.14) |
| DonchianAdxChop | 1h | -59.2% | -33.5% | +0.5% (16 tr, PF 1.03) | **-13.4%** (8 tr) |
| MeanReversionBbRsi | 1h | -3.9% | +18.0% | degenerate (2 tr) — discarded | — |

### AdxSmaBreakout — tuned params (saved in AdxSmaBreakout.json, auto-loaded)
`short_sma=11, long_sma=132, adx_period=13, adx_threshold=27, atr_pct_threshold=0.03, cross_window=5, atr_mult=1.1`

### Overfit checks on AdxSmaBreakout
1. **IS/OOS split:** +72.7% IS → +14.6% OOS. Degrades (expected) but stays positive
   with PF 1.86. PASS, with caveat: only 8 OOS trades — small sample.
2. **Parameter sensitivity (OOS, one-at-a-time):** 7 of 9 neighboring settings
   profitable. `long_sma` 120/132/145 → identical (+14.6% each). `adx_threshold`
   25/27/29 → +20.1/+14.6/+0.3%. `short_sma` 9/11/13 → **-3.8**/+14.6/+7.0%.
   Not a knife-edge optimum. PARTIAL PASS — fragile around short_sma.
3. **Cross-pair (GRT-tuned params, untouched):** ETH +19.4% IS / +15.6% OOS (edge
   generalizes to volatile alts). BTC -4.4% IS / -12.2% OOS (3% daily-ATR gate is
   wrong for majors; strategy is alt-volatility-shaped). PARTIAL PASS.

### Other findings
- **SupertrendEma200** is the robustness champion: profitable with DEFAULTS in-sample,
  profitable tuned OOS, fewest parameters. Trades rarely (4 OOS trades). Tuned:
  `st_period=12, st_mult=5.0, ema_period=157, atr_stop_mult=1.4`.
- **DonchianAdxChop fails on GRT** even tuned → AdxSmaBreakout's complexity beats the
  simpler benchmark; keeping it as the bar to clear in future re-tunes.
- **MeanReversionBbRsi (Bucket B): no validated edge on majors.** Defaults on
  BTC +6.0% IS / -7.6% OOS; ETH -21.7% IS / -4.2% OOS. Hyperopt on GRT went
  degenerate (Sharpe-maxing via 2 trades; params json deleted). **Do not deploy.**
  Ideas for next pass: tune on BTC+ETH jointly, try 4h TF, walk-forward, wider BB.

### Cross-pair addendum
- SupertrendEma200 tuned params on ETH (untuned pair): +68.8% IS / -2.0% OOS. Flat
  on unseen ETH data — acceptable for paper A/B, watch it.

### Deployed to dry-run (2026-08-16)
- `ft-dry-adxsma` — AdxSmaBreakout tuned, pairs GRT+ETH, port 8080
- `ft-dry-supertrend` — SupertrendEma200 tuned, pairs GRT+ETH, port 8081
Both: 1000 USDT paper wallet, 1x leverage, OKX futures, `max_open_trades=2`.

### Honest caveats (read before trusting any number above)
- 12.5 months of data, one alt (GRT) as the tuning pair; 8-16 trades per window is
  a small statistical sample. These results justify a dry-run, not live capital.
- OKX funding-rate history only covers ~last 3 months; funding fees under-counted
  in older windows (small effect at these trade durations).
- The videos' headline numbers (475%, 2529%, 179%, 140%) did not reproduce on our
  window/exchange with defaults. Expected: different data, different regime, and
  their numbers come from tuned params on their own window (and leverage).
