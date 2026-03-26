# Ticks / Price Data

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Price Data (Charts)](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_chart)

---

## Overview

The MT4 Server stores historical OHLC bar data and tick data per symbol. The Manager API provides:
- **Bar (OHLC) history** via `ChartRequest` — useful for price history analysis
- **Last tick** via `TickInfoLast` — current bid/ask snapshot
- **Tick history** via feeders — raw tick-by-tick data stream

In pumping mode, `PUMP_UPDATE_BIDASK` fires on every new quote, and `TickInfoLast` returns the latest tick.

---

## Methods

| Method | Purpose |
|--------|---------|
| `ChartRequest` | Get OHLC bar history for a symbol + timeframe + date range |
| `ChartAdd` | Add bars to server history database (admin) |
| `ChartUpdate` | Update existing bars (admin) |
| `ChartDelete` | Delete bars from server history (admin) |
| `TickInfoLast` | Get last tick for a symbol (pumping mode) |
| `TickRequest` | Request tick history for a symbol and time range |

---

## Example Code

```python
import ctypes

# ─── ChartRequest — OHLC bar history ─────────────────────────────────────────
class ChartInfo(ctypes.Structure):
    _fields_ = [
        ("symbol",  ctypes.c_char * 12),
        ("period",  ctypes.c_int),       # timeframe in minutes (see enum)
        ("mode",    ctypes.c_int),       # mode (0 = from server)
        ("timesign", ctypes.c_int),      # start time (time_t)
        ("reserved", ctypes.c_int * 4),
    ]

req = ChartInfo()
req.symbol   = b"EURUSD"
req.period   = 60          # 1-hour bars
req.mode     = 0
req.timesign = int(time.time()) - (7 * 86400)   # last 7 days

total = ctypes.c_int(0)
bars_ptr = manager.ChartRequest(ctypes.byref(req), ctypes.byref(total))

if bars_ptr:
    print(f"Bars returned: {total.value}")
    RateInfoArray = RateInfo * total.value
    bars = ctypes.cast(bars_ptr, ctypes.POINTER(RateInfoArray)).contents
    records = [struct_to_dict(b) for b in bars]
    manager.MemFree(bars_ptr)
    print(records[0])


# ─── TickInfoLast — last tick (pumping mode) ──────────────────────────────────
# Called on PUMP_UPDATE_BIDASK notification
tick = TickInfo()
ret = manager.TickInfoLast(b"EURUSD", ctypes.byref(tick))
if ret == 0:
    print(f"EURUSD last tick: bid={tick.bid} ask={tick.ask} ts={tick.time}")
```

---

## RateInfo Structure (OHLC Bar)

```python
class RateInfo(ctypes.Structure):
    _fields_ = [
        ("ctm",    ctypes.c_int),       # bar open time (time_t UTC)
        ("open",   ctypes.c_double),    # open price
        ("high",   ctypes.c_double),    # high price
        ("low",    ctypes.c_double),    # low price
        ("close",  ctypes.c_double),    # close price
        ("vol",    ctypes.c_double),    # tick volume
    ]
```

---

## TickInfo Structure (Last Tick)

```python
class TickInfo(ctypes.Structure):
    _fields_ = [
        ("symbol", ctypes.c_char * 12),
        ("bid",    ctypes.c_double),
        ("ask",    ctypes.c_double),
        ("last",   ctypes.c_double),
        ("volume", ctypes.c_double),
        ("time",   ctypes.c_int),       # tick timestamp (time_t UTC)
        ("flags",  ctypes.c_int),
    ]
```

---

## TickRecord Structure (Raw Tick from Feed)

```python
class TickRecord(ctypes.Structure):
    _fields_ = [
        ("symbol", ctypes.c_char * 12),
        ("bid",    ctypes.c_double),
        ("ask",    ctypes.c_double),
        ("last",   ctypes.c_double),
        ("volume", ctypes.c_double),
        ("time",   ctypes.c_int),
    ]
```

---

## Timeframe Enum (ChartInfo::period)

| Value | Timeframe | Description |
|-------|-----------|-------------|
| `1` | M1 | 1-minute bars |
| `5` | M5 | 5-minute bars |
| `15` | M15 | 15-minute bars |
| `30` | M30 | 30-minute bars |
| `60` | H1 | 1-hour bars |
| `240` | H4 | 4-hour bars |
| `1440` | D1 | Daily bars |
| `10080` | W1 | Weekly bars |
| `43200` | MN1 | Monthly bars |

---

## Response Fields — RateInfo (OHLC Bar)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `ctm` | `int` (time_t) | Bar open timestamp (UTC) | `1711152000` |
| `open` | `double` | Open price | `1.08200` |
| `high` | `double` | High price | `1.08520` |
| `low` | `double` | Low price | `1.08150` |
| `close` | `double` | Close price | `1.08325` |
| `vol` | `double` | Tick volume (number of ticks in bar) | `1842.0` |

---

## Response Fields — TickInfo (Last Tick)

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `symbol` | `char[12]` | Symbol name | `"EURUSD"` |
| `bid` | `double` | Bid price | `1.08325` |
| `ask` | `double` | Ask price | `1.08327` |
| `last` | `double` | Last trade price (for exchange) | `0.0` |
| `volume` | `double` | Last tick volume | `0.0` |
| `time` | `int` (time_t) | Tick timestamp (UTC) | `1711190400` |
| `flags` | `int` | Tick flags | `0` |

---

## Sample Raw Response — OHLC Bar (JSON)

```json
{
  "ctm": 1711152000,
  "open": 1.08200,
  "high": 1.08520,
  "low": 1.08150,
  "close": 1.08325,
  "vol": 1842.0
}
```

## Sample Raw Response — Last Tick (JSON)

```json
{
  "symbol": "EURUSD",
  "bid": 1.08325,
  "ask": 1.08327,
  "last": 0.0,
  "volume": 0.0,
  "time": 1711190400,
  "flags": 0
}
```

---

## Notes

- `ChartRequest` returns bars **from** `timesign` onwards, up to the server's limit.
- For incremental tick collection: use pumping mode with `PUMP_UPDATE_BIDASK` + `TickInfoLast`.
- For full tick history: use the **DataFeed API** (`SrvFeederLog`) — not the chart API.
- `vol` in `RateInfo` is **tick count** (how many ticks fell in that bar), not true traded volume.
- The `MemFree` call is required after `ChartRequest` — the returned pointer is heap-allocated.
