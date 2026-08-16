"""Multi-coin validation for AdxSmaBreakout.

Anti-overfit methodology (read before trusting output):
  1. GRT-tuned params are used UNCHANGED on every coin. We do NOT re-tune
     per coin. If one fixed parameter set generalizes across many coins, that
     is evidence of a real edge — not curve-fitting. (The video's
     "pair-optimized" version re-tunes per coin, which is the overfit trap.)
  2. Coins are SELECTED on the in-sample window only (the legitimate tuning
     window): qualify if IS profit > 0 with >= MIN_TRADES trades.
  3. Out-of-sample is REPORTED as verification, never used to select. This
     avoids selecting on the test set (multiple-comparisons overfitting).
  4. The portfolio OOS number on the qualified basket is the real result.

Usage: .venv/bin/python user_data/research/validate_basket.py
"""

import json
import re
import subprocess
import sys

IS = "20250801-20260401"
OOS = "20260401-20260816"
MIN_TRADES = 6
CFG = "user_data/configs/config-backtest.json"
STRAT = "AdxSmaBreakout"

UNIVERSE = open("/tmp/universe.txt").read().split()
# GRT and ETH already validated in the prior pass — include them in the basket test.
UNIVERSE = ["GRT/USDT:USDT", "ETH/USDT:USDT"] + [p for p in UNIVERSE if p not in ("GRT/USDT:USDT", "ETH/USDT:USDT")]


def run(pairs, timerange, max_open):
    cfg = json.load(open(CFG))
    cfg["exchange"]["pair_whitelist"] = pairs
    cfg["max_open_trades"] = max_open
    json.dump(cfg, open("/tmp/cfg_run.json", "w"))
    out = subprocess.run(
        [".venv/bin/freqtrade", "backtesting", "-c", "/tmp/cfg_run.json",
         "--strategy", STRAT, "--timerange", timerange],
        capture_output=True, text=True).stdout
    prof = re.search(r"Total profit %\s*│\s*(-?[\d.]+)%", out)
    trades = re.search(r"Total/Daily Avg Trades\s*│\s*(\d+)", out)
    dd = re.search(r"Drawdown \(Account\)\s*│\s*(-?[\d.]+)%", out)
    pf = re.search(r"Profit factor\s*│\s*(-?[\d.]+)", out)
    return (
        float(prof.group(1)) if prof else 0.0,
        int(trades.group(1)) if trades else 0,
        float(dd.group(1)) if dd else 0.0,
        float(pf.group(1)) if pf else 0.0,
    )


print(f"Per-coin standalone (GRT-tuned params, max_open_trades=1)\n{'coin':<14}{'IS%':>9}{'IS_tr':>7}{'OOS%':>9}{'OOS_tr':>7}  qualifies?")
print("-" * 62)
qualified = []
for pair in UNIVERSE:
    isp, ist, _, _ = run([pair], IS, 1)
    oosp, oost, _, _ = run([pair], OOS, 1)
    q = isp > 0 and ist >= MIN_TRADES
    if q:
        qualified.append(pair)
    coin = pair.split("/")[0]
    print(f"{coin:<14}{isp:>8.1f}%{ist:>7}{oosp:>8.1f}%{oost:>7}  {'YES' if q else 'no'}")

print(f"\nQualified on IS (profit>0, >={MIN_TRADES} trades): "
      f"{', '.join(p.split('/')[0] for p in qualified)}")

if qualified:
    n = min(len(qualified), 5)
    print(f"\nPortfolio backtest — {len(qualified)} coins, max_open_trades={n}:")
    for label, tr in [("IN-SAMPLE ", IS), ("OUT-SAMPLE", OOS)]:
        p, t, d, pf = run(qualified, tr, n)
        print(f"  {label}: {p:+.1f}%  trades {t}  maxDD {d:.1f}%  PF {pf:.2f}")

    with open("/tmp/qualified.txt", "w") as f:
        f.write(json.dumps(qualified))
