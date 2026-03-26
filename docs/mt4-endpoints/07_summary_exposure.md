# SummaryGetAll / ExposureGet — Aggregated Positions & Exposure

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve aggregated position summaries per symbol and currency exposure data.
Used for risk management, hedging analysis, and open-interest reporting.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `SummaryGetAll(*total)`, `SummaryGet(symbol, *sum)`, `SummaryGetByCount(index, *sum)`, `ExposureGet(*total)`, `ExposureValueGet(name, *exp)` |
| **Mode** | Pumping mode required for real-time updates |

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect, login, start pumping

# --- All symbol summaries ---
total = ctypes.c_int(0)
# SymbolSummary* sums = manager->SummaryGetAll(&total)
# for i in range(total.value):
#     s = sums[i]
#     print(f"{s.symbol.decode()}: clients={s.count}, "
#           f"vol={s.volume/100:.2f}, profit={s.profit:.2f}")

# --- Single symbol summary ---
s = SymbolSummary()
# manager->SummaryGet("EURUSD", &s)

# --- By index ---
# manager->SummaryGetByCount(0, &s)  # first symbol

# --- All currency exposures ---
total = ctypes.c_int(0)
# ExposureValue* exps = manager->ExposureGet(&total)
# for i in range(total.value):
#     e = exps[i]
#     print(f"Currency: {e.cur_name.decode()}, "
#           f"client={e.client_assets:.2f}, hedged={e.hedged_assets:.2f}")

# --- Single exposure by currency name ---
e = ExposureValue()
# manager->ExposureValueGet("USD", &e)
```

## Response Fields — `SymbolSummary` Structure

```python
import ctypes

class SymbolSummary(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",      ctypes.c_char * 12),  # Symbol name
        ("count",       ctypes.c_int),        # Open positions count
        ("volume",      ctypes.c_int),        # Total client volume (×100)
        ("volume_buy",  ctypes.c_int),        # Total buy volume (×100)
        ("volume_sell", ctypes.c_int),        # Total sell volume (×100)
        ("profit",      ctypes.c_double),     # Total floating profit
        ("hedged",      ctypes.c_int),        # Hedged/broker volume (×100)
        ("hedged_buy",  ctypes.c_double),     # Broker buy hedge volume
        ("hedged_sell", ctypes.c_double),     # Broker sell hedge volume
        ("reserved",    ctypes.c_int * 4),   # Reserved
    ]
```

## SymbolSummary Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `symbol` | `char[12]` | Symbol name | `"EURUSD"` |
| `count` | `int` | Number of open client positions | `42` |
| `volume` | `int` | Total client open volume × 100 | `5000` (50.00 lots) |
| `volume_buy` | `int` | Total buy volume × 100 | `3000` (30.00 lots) |
| `volume_sell` | `int` | Total sell volume × 100 | `2000` (20.00 lots) |
| `profit` | `double` | Total unrealized profit | `1250.50` |
| `hedged` | `int` | Broker hedge position volume × 100 | `1000` |
| `hedged_buy` | `double` | Broker hedged buy volume | `1000.0` |
| `hedged_sell` | `double` | Broker hedged sell volume | `0.0` |

## Response Fields — `ExposureValue` Structure

```python
import ctypes

class ExposureValue(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("cur_name",       ctypes.c_char * 16),  # Currency name (e.g. "USD")
        ("client_assets",  ctypes.c_double),     # Total client exposure in currency
        ("hedged_assets",  ctypes.c_double),     # Broker hedged exposure
        ("rate_deposit",   ctypes.c_double),     # Rate to deposit currency
        ("reserved",       ctypes.c_int * 4),   # Reserved
    ]
```

## ExposureValue Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `cur_name` | `char[16]` | Currency name | `"USD"` |
| `client_assets` | `double` | Total client open exposure in currency | `2500000.00` |
| `hedged_assets` | `double` | Broker hedged exposure in currency | `500000.00` |
| `rate_deposit` | `double` | Conversion rate to deposit currency | `1.0` |

## Related Functions

| Function | Description |
|----------|-------------|
| `SummaryGetAll(*total)` | All symbol summaries (pumping) |
| `SummaryGet(symbol, *sum)` | Single symbol summary (pumping) |
| `SummaryGetByCount(index, *sum)` | Summary by index (pumping) |
| `SummaryGetByType(sectype, *total)` | Summaries by security type (pumping) |
| `SummaryCurrency(symbol, currency)` | Set currency for summary calc |
| `ExposureGet(*total)` | All currency exposures |
| `ExposureValueGet(name, *exp)` | Single currency exposure |
