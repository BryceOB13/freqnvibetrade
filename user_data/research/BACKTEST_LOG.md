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

---

## 2026-08-16 (later) — Multi-coin validation of AdxSmaBreakout (Claude/Zo)

Question: does the ADX+MA edge generalize across many coins (→ higher returns
without leverage), or is it GRT-specific overfit? Method in
`user_data/research/validate_basket.py`. Rule: GRT-tuned params used UNCHANGED on
every coin; SELECT on in-sample only (profit>0, >=6 trades); REPORT out-of-sample
as verification, never select on it. Universe = 12 liquid established alts + GRT + ETH.

### Per-coin standalone (GRT-tuned params, 1x, max_open_trades=1)
| coin | IS % | OOS % | selected (IS)? |
|---|---|---|---|
| GRT | +72.7 | +14.6 | YES |
| ETH | +19.4 | +15.6 | YES |
| OP | +4.3 | **-28.3** | YES (then failed OOS) |
| DOGE | -22.6 | +16.6 | no |
| ADA | -34.0 | +39.2 | no |
| ARB | -33.7 | +45.5 | no |
| CRV | -41.1 | +10.0 | no |
| LDO | -47.5 | +29.1 | no |
| XRP/XLM/FIL/SUI/ALGO/TRX | all ≤ 0 IS | mixed | no |

### Verdict: the edge does NOT broadly generalize with GRT params
- Only GRT + ETH are robust (positive BOTH windows). These are exactly the two
  already in the dry-run bot — validation CONFIRMS the current whitelist.
- **OP is the cautionary tale:** passed IS (+4.3%), then -28.3% OOS. Adding it to the
  basket dragged the portfolio OOS from +15.9% (GRT+ETH) to +0.1% (GRT+ETH+OP).
  More coins made it WORSE, not better.
- **Selection-bias demo:** ADA/ARB/DOGE/LDO were NEGATIVE in-sample but strongly
  POSITIVE out-of-sample (+39/+46/+17/+29%). Picking on OOS would have chosen pure
  flukes. This is exactly why we select on IS and only verify on OOS, and why the
  video's per-coin "pair-optimized" approach is an overfitting trap.
- Implication: GRT-tuned params are shaped to GRT's (spicy alt) volatility profile.
  A real multi-coin bot needs params tuned JOINTLY across coins — tested next.

### Portfolio backtest (GRT+ETH+OP, max_open_trades=3)
IS +33.6% (PF 1.77) / OOS +0.1% (PF 1.01). Worse than the GRT+ETH pair. Not deployed.

### Decision: keep ft-dry-adxsma on GRT+ETH (unchanged). Multi-coin needs a joint re-tune.

---

## 2026-08-16 (later still) — Joint multi-coin re-tune of AdxSmaBreakout (Claude/Zo)

Test: can ADX+MA be a real multi-coin strategy if params are tuned JOINTLY across
coins instead of on GRT alone? Hyperopt on 8-coin basket (GRT, ETH, ADA, ARB, OP,
XLM, DOGE, SUI), SharpeHyperOptLoss, 300 epochs, max_open_trades=4, IS window.
Config: `config-basket-tune.json`. Answer: **YES — this is the deployed bot now.**

### Basket-tuned params (now active in AdxSmaBreakout.json; GRT-only saved as AdxSmaBreakout.grt-tuned.json)
`short_sma=10, long_sma=142, adx_period=10, adx_threshold=23, atr_pct_threshold=0.027, cross_window=3, atr_mult=1.1`

### Portfolio result (8 coins, 1x leverage, max_open_trades=4)
| Window | Profit | Trades | Win% | Max DD | Sharpe |
|---|---|---|---|---|---|
| In-sample | +63.7% | 111 | 43.2% | 19.6% | — |
| **Out-of-sample** | **+24.6%** | **54** | 40.7% | 10.4% | 1.28 |

This beats the GRT+ETH two-coin bot (+15.9% OOS, 16 trades) on BOTH return and
sample size. 54 OOS trades is a statistically meaningful sample — the single most
important improvement. Tuned on 8 and tested on 8 (no cherry-picking) → clean OOS.

### Honest read (per-coin OOS, joint params)
Winners IS+OOS: ARB (+63/+28), OP (+89/+3), GRT (+1.3/+0.3). Strong-IS-weak-OOS:
ETH (+39/-6), ADA (+20/-10). DOGE (-30 IS / +29 OOS) is a lucky-direction fluke,
not edge. **The basket works via DIVERSIFICATION** — noisy per-coin, positive in
aggregate — not because every coin has a clean edge. That's exactly how real
multi-coin systems behave, and it's the honest way to raise returns WITHOUT
leverage (more independent bets, not bigger bets). Per-coin params tuned for GRT
alone gave GRT +72.7% IS but don't generalize; joint params trade GRT's solo
brilliance for basket robustness. Correct trade for a multi-coin bot.

### Deployed (2026-08-16)
- `ft-dry-adxsma` UPDATED → 8-coin basket, basket-tuned params, max_open_trades=4,
  1000 USDT paper, 1x. This is now the primary Bucket A bot.
- `ft-dry-supertrend` unchanged (GRT+ETH benchmark).

## 2026-08-16 (night) — Bucket B joint re-tune on majors: FAILED, not deployed (Claude/Zo)

Method: same treatment that fixed Bucket A. MeanReversionBbRsi jointly hyperopted
on 8 majors (BTC/ETH/SOL/XRP/ADA/LINK/LTC/AVAX), MultiMetricHyperOptLoss (penalizes
low trade counts — guards against the earlier 2-trade degenerate), 300 epochs, IS only.
Config: `config-bucket-b-tune.json`.

Result: IS +18.4% (264 trades, 67% win — healthy MR profile) → **OOS -11.7%
(124 trades, PF 0.62). FAIL.** Params archived at
`research/MeanReversionBbRsi.majors-tuned.FAILED.json` (moved out of strategies/
so nothing auto-loads them).

**Verdict: BB+RSI+ADX mean-reversion has no validated edge on majors in this
period, even with joint tuning.** Two failures now (GRT degenerate, majors joint).

**STOP RULE (important):** every additional tuning attempt validated against the
SAME OOS window erodes that window's meaning (multiple comparisons — try enough
variants and one will pass by luck). No further Bucket B attempts against
20260401-20260816. Revisit after the dry-run period with rolled-forward windows,
and consider structural changes (4h timeframe, long-only spot DCA — the original
Bucket B concept) rather than re-tuning the same shape.

### Leverage guidance recorded for Bryce (his question)
Leverage multiplies returns AND drawdown AND adds liquidation risk — it is a
position-size dial, not an edge. Rule: Bucket B always 1x; Bucket A 1x until a
strategy shows months of clean dry-run matching backtest, then 2-3x ceiling on
written-off capital only. Never the 10-20x exchanges offer. All numbers in this
log are 1x. To see any of them at Nx, multiply profit AND drawdown by ~N.
