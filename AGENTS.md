# freqnvibetrade — Agent Guide

Fork of [Freqtrade](https://github.com/freqtrade/freqtrade). Upstream engine code is
untouched — **all of our work lives in `user_data/`**. Keep it that way so upstream
merges stay clean.

## Project intent (Bryce's two-bucket plan)
- **Bucket A — "gambling money":** trend/breakout strategies, low win rate, big
  winners. Isolated capital, prepared to lose it all.
- **Bucket B — "long-term bag":** mean-reversion on majors (BTC/ETH) Bryce is happy
  holding anyway. Many small wins, rare drawdown he can sit through.
- Buckets must stay isolated: separate configs, separate dry-run wallets, separate
  services, eventually separate exchange subaccounts.

## Layout
```
user_data/
  strategies/          # One class per file. Every file's docstring cites its source.
    AdxSmaBreakout.py      # Bucket A PRIMARY. Deployed multi-coin (8-coin basket).
                           #   Active params = basket-tuned (AdxSmaBreakout.json).
                           #   GRT-only params archived: research/AdxSmaBreakout.grt-tuned.json
    SupertrendEma200.py    # Bucket A benchmark (fewest knobs, hardest to overfit)
    DonchianAdxChop.py     # Bucket A benchmark (classic breakout)
    MeanReversionBbRsi.py  # Bucket B primary (BB+RSI+ADX) — NO validated edge yet, not deployed
  configs/
    config-backtest.json       # Shared backtest/hyperopt config (OKX futures)
    config-dryrun-bucket-a.json  # Live dry-run, bucket A
  research/
    transcripts/       # Source video transcripts (the strategies' provenance)
    BACKTEST_LOG.md    # Running log of results. APPEND, don't rewrite history.
  data/okx/            # Downloaded candles (gitignored — re-download, see below)
```

## Ground rules for agents working here
1. **Never tune on the out-of-sample window.** Convention: in-sample
   `20250801-20260401` (8mo), out-of-sample `20260401-20260816` (4.5mo). If you
   re-tune later, roll BOTH windows forward and log it in BACKTEST_LOG.md.
2. **Log every backtest/hyperopt run** in `user_data/research/BACKTEST_LOG.md`
   (date, strategy, window, params, result). Results without provenance are noise.
3. **Dry-run before live, always.** No live keys in configs. Secrets go in
   Zo Settings > Advanced env vars, never in the repo.
4. **This server cannot reach Binance or Bybit (HTTP 451/403 geo-block).** Use OKX
   (primary) or Gate. Kraken/KuCoin reachable but not used for futures.
5. Python env: `.venv/` at repo root (gitignored). Rebuild:
   `python3 -m venv .venv && .venv/bin/pip install -e ".[hyperopt]"`
6. Re-download data:
   `.venv/bin/freqtrade download-data --exchange okx --pairs GRT/USDT:USDT BTC/USDT:USDT ETH/USDT:USDT -t 1h 4h 1d --timerange 20250501- --trading-mode futures`
7. Work on feature branches; `develop` tracks upstream freqtrade.
8. Leverage is pinned to 1x in every strategy until Bryce explicitly changes that.

## Known sharp edges
- Freqtrade config `"timeframe"` overrides the strategy's own timeframe — leave it
  OUT of shared configs; strategies declare their own.
- OKX funding-rate history only goes back ~3 months; older futures backtests
  under-count funding fees slightly. Acceptable for strategy comparison.
- pandas 3.x + freqtrade 2026.8-dev in this venv; qtpylib imports come from
  `technical` (`from technical import qtpylib`), the vendored copy is deprecated.
