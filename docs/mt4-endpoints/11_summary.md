# Summary Positions

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Summary Positions](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_summary)

---

## Overview

Summary Positions aggregate all client open positions per symbol, giving the broker a view of
their total book exposure on each instrument. Available in pumping mode.

This is the same `SymbolSummary` struct used in the Exposure API (see `09_exposure.md`),
accessed via dedicated summary methods.

---

## Methods

| Method | Purpose |
|--------|---------|
| `SummaryGetAll` | Get all symbol summaries (pumping) |
| `SummaryGet` | Get summary for one symbol by name (pumping) |
| `SummaryGetByCount` | Get top N summaries sorted by open position count |
| `SummaryGetByType` | Get summaries filtered by trade direction (buy/sell) |

---

## Example Code

```python
import ctypes

# Must be in pumping mode
# ─── SummaryGetAll ────────────────────────────────────────────────────────────
total = ctypes.c_int(0)
summ_ptr = manager.SummaryGetAll(ctypes.byref(total))

if summ_ptr:
    SymbolSummaryArray = SymbolSummary * total.value
    summaries = ctypes.cast(summ_ptr, ctypes.POINTER(SymbolSummaryArray)).contents
    records = [struct_to_dict(s) for s in summaries]
    print(f"Summary for {total.value} symbols:")
    for r in records[:5]:
        net_lots = (r["volume_buy"] - r["volume_sell"]) / 100.0
        print(f"  {r['symbol']:12s} buy={r['volume_buy']/100:.2f}L sell={r['volume_sell']/100:.2f}L net={net_lots:+.2f}L P&L={r['profit']:+.2f}")


# ─── SummaryGet — single symbol ───────────────────────────────────────────────
sym = SymbolSummary()
ret = manager.SummaryGet(b"EURUSD", ctypes.byref(sym))
if ret == 0:
    print(f"EURUSD: {sym.count} positions, P&L={sym.profit}")


# ─── SummaryGetByCount — top 10 by number of positions ───────────────────────
total2 = ctypes.c_int(0)
top_ptr = manager.SummaryGetByCount(10, ctypes.byref(total2))
# same pattern
```

---

## SymbolSummary Structure

```python
class SymbolSummary(ctypes.Structure):
    _fields_ = [
        ("symbol",         ctypes.c_char * 12),
        ("count",          ctypes.c_int),
        ("count_buy",      ctypes.c_int),
        ("count_sell",     ctypes.c_int),
        ("volume",         ctypes.c_int),
        ("volume_buy",     ctypes.c_int),
        ("volume_sell",    ctypes.c_int),
        ("profit_buy",     ctypes.c_double),
        ("profit_sell",    ctypes.c_double),
        ("profit",         ctypes.c_double),
        ("profit_raw",     ctypes.c_double),
        ("bid",            ctypes.c_double),
        ("ask",            ctypes.c_double),
        ("reserved",       ctypes.c_int * 4),
    ]
```

---

## Response Fields

| Field | C++ Type | Description | Example |
|-------|----------|-------------|---------|
| `symbol` | `char[12]` | Symbol name | `"EURUSD"` |
| `count` | `int` | Total open positions | `142` |
| `count_buy` | `int` | Buy positions | `89` |
| `count_sell` | `int` | Sell positions | `53` |
| `volume` | `int` | Total volume (lots×100) | `25300` |
| `volume_buy` | `int` | Buy volume (lots×100) | `15200` |
| `volume_sell` | `int` | Sell volume (lots×100) | `10100` |
| `profit_buy` | `double` | Floating P&L — buys | `4250.00` |
| `profit_sell` | `double` | Floating P&L — sells | `-2100.00` |
| `profit` | `double` | Total floating P&L | `2150.00` |
| `profit_raw` | `double` | Raw P&L (before swap/commission) | `2180.00` |
| `bid` | `double` | Current bid | `1.08325` |
| `ask` | `double` | Current ask | `1.08327` |

---

## Sample Raw Response (JSON)

```json
[
  {
    "symbol": "EURUSD",
    "count": 142,
    "count_buy": 89,
    "count_sell": 53,
    "volume": 25300,
    "volume_buy": 15200,
    "volume_sell": 10100,
    "profit_buy": 4250.00,
    "profit_sell": -2100.00,
    "profit": 2150.00,
    "profit_raw": 2180.00,
    "bid": 1.08325,
    "ask": 1.08327
  },
  {
    "symbol": "GBPUSD",
    "count": 87,
    "count_buy": 42,
    "count_sell": 45,
    "volume": 13400,
    "volume_buy": 6200,
    "volume_sell": 7200,
    "profit_buy": 1100.00,
    "profit_sell": 2200.00,
    "profit": 3300.00,
    "profit_raw": 3320.00,
    "bid": 1.26540,
    "ask": 1.26543
  }
]
```

---

## Notes

- Available in **pumping mode only** — call after `PumpingSwitch`.
- `PUMP_UPDATE_TRADES` fires in pumping mode when any position changes; re-query summaries then.
- Net position on a symbol: `(volume_buy - volume_sell) / 100.0` lots. Positive = broker is net short (clients are net long).
