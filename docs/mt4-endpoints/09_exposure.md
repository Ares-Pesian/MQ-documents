# Exposure

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Exposure](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_exposure)

---

## Overview

The Exposure API returns the broker's net currency exposure — the aggregate of all client positions
expressed in base currencies. This is the total risk the broker carries on each currency pair.

Two related structures:
- **`SymbolSummary`** — per-symbol aggregate of all client positions (long volume, short volume, profit)
- **`ExposureValue`** — net currency exposure in account currency terms

---

## Methods

| Method | Purpose |
|--------|---------|
| `ExposureGet` | Get all `SymbolSummary` records (pumping mode) |
| `ExposureValueGet` | Get all `ExposureValue` records — net currency exposure |
| `SummaryGetAll` | Get all `SymbolSummary` records (pumping) |
| `SummaryGet` | Get `SymbolSummary` for one symbol |
| `SummaryGetByCount` | Get top N summary records |
| `SummaryGetByType` | Get summary records filtered by trade command |

---

## Example Code

```python
import ctypes

# Must be in pumping mode for ExposureGet / SummaryGetAll

# ─── ExposureValueGet — net currency exposure ────────────────────────────────
total = ctypes.c_int(0)
exp_ptr = manager.ExposureValueGet(ctypes.byref(total))

if exp_ptr:
    print(f"Exposure entries: {total.value}")
    ExposureValueArray = ExposureValue * total.value
    exposures = ctypes.cast(exp_ptr, ctypes.POINTER(ExposureValueArray)).contents
    records = [struct_to_dict(e) for e in exposures]
    # No MemFree — returns internal cache pointer in pumping mode
    print(records)


# ─── SummaryGetAll — per-symbol position summary ─────────────────────────────
total2 = ctypes.c_int(0)
summ_ptr = manager.SummaryGetAll(ctypes.byref(total2))

if summ_ptr:
    print(f"Symbol summaries: {total2.value}")
    SymbolSummaryArray = SymbolSummary * total2.value
    summaries = ctypes.cast(summ_ptr, ctypes.POINTER(SymbolSummaryArray)).contents
    records2 = [struct_to_dict(s) for s in summaries]
    print(records2[0])
```

---

## SymbolSummary Structure

Per-symbol aggregate of all open client positions.

```python
class SymbolSummary(ctypes.Structure):
    _fields_ = [
        ("symbol",         ctypes.c_char * 12),
        ("count",          ctypes.c_int),         # number of open positions
        ("count_buy",      ctypes.c_int),          # count of buy positions
        ("count_sell",     ctypes.c_int),          # count of sell positions
        ("volume",         ctypes.c_int),          # total volume (lots×100)
        ("volume_buy",     ctypes.c_int),          # buy volume
        ("volume_sell",    ctypes.c_int),          # sell volume
        ("profit_buy",     ctypes.c_double),       # floating P&L from buys
        ("profit_sell",    ctypes.c_double),       # floating P&L from sells
        ("profit",         ctypes.c_double),       # total floating P&L
        ("profit_raw",     ctypes.c_double),       # raw P&L before swap/commission
        ("bid",            ctypes.c_double),       # current bid price
        ("ask",            ctypes.c_double),       # current ask price
        ("reserved",       ctypes.c_int * 4),
    ]
```

---

## ExposureValue Structure

Net currency exposure value.

```python
class ExposureValue(ctypes.Structure):
    _fields_ = [
        ("symbol",    ctypes.c_char * 12),    # currency symbol (e.g. "EUR", "USD")
        ("value",     ctypes.c_double),       # net exposure in account currency
        ("margin",    ctypes.c_double),       # margin required for this exposure
        ("reserved",  ctypes.c_int * 4),
    ]
```

---

## Response Fields — SymbolSummary

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `symbol` | `char[12]` | Trading symbol | `"EURUSD"` |
| `count` | `int` | Total open positions on this symbol | `142` |
| `count_buy` | `int` | Number of buy positions | `89` |
| `count_sell` | `int` | Number of sell positions | `53` |
| `volume` | `int` | Total volume (lots×100) | `25300` |
| `volume_buy` | `int` | Total buy volume (lots×100) | `15200` |
| `volume_sell` | `int` | Total sell volume (lots×100) | `10100` |
| `profit_buy` | `double` | Floating P&L from buy positions | `4250.00` |
| `profit_sell` | `double` | Floating P&L from sell positions | `-2100.00` |
| `profit` | `double` | Total floating P&L (all positions) | `2150.00` |
| `profit_raw` | `double` | Raw P&L before swap/commission | `2180.00` |
| `bid` | `double` | Current bid price | `1.08325` |
| `ask` | `double` | Current ask price | `1.08327` |

---

## Response Fields — ExposureValue

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `symbol` | `char[12]` | Base currency exposed | `"EUR"` |
| `value` | `double` | Net exposure in account base currency | `2530000.00` |
| `margin` | `double` | Margin required for this currency exposure | `25300.00` |

---

## Sample Raw Response — SymbolSummary (JSON)

```json
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
}
```

---

## Notes

- `ExposureGet` and `SummaryGetAll` are available in **pumping mode only** — call after `PumpingSwitch`.
- `volume` is stored as lots × 100. Convert: `lots = volume / 100.0`.
- Net volume = `volume_buy - volume_sell`. Positive = net long, negative = net short.
- This data is used for hedging decisions and risk monitoring on the broker book.
