# ChartRequest / TicksRequest / TickInfoLast — Price History & Ticks

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve OHLCV bar history and tick data for any symbol and timeframe.
`ChartRequest` returns bars; `TicksRequest` returns raw tick data; `TickInfoLast` returns the most recent ticks.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `ChartRequest(*req, *total)`, `TicksRequest(*req, *total)`, `TickInfoLast(symbol, count, *total)` |

## Example Code

```python
import ctypes, time

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login

# --- Bar/OHLCV history ---
req = ChartInfo()
req.symbol  = b"EURUSD"
req.period  = 60     # 1-minute bars (M1=1, M5=5, M15=15, M30=30, H1=60,
                     # H4=240, D1=1440, W1=10080, MN1=43200)
req.timesign = int(time.time()) - 86400 * 30  # 30 days ago
req.count   = 1000   # max bars to return

total = ctypes.c_int(0)
# RateInfo* bars = manager->ChartRequest(&req, &total)
# for i in range(total.value):
#     b = bars[i]
#     print(b.ctm, b.open, b.high, b.low, b.close, b.vol)
# manager->MemFree(bars)

# --- Raw tick history ---
tick_req = TickRequest()
tick_req.symbol    = b"EURUSD"
tick_req.from_time = int(time.time()) - 3600  # last hour
tick_req.to_time   = int(time.time())

total = ctypes.c_int(0)
# TickAPI* ticks = manager->TicksRequest(&tick_req, &total)
# for i in range(total.value):
#     t = ticks[i]
#     print(t.ctm, t.bid, t.ask)
# manager->MemFree(ticks)

# --- Last N ticks for a symbol ---
total = ctypes.c_int(0)
# TickInfo* last = manager->TickInfoLast("EURUSD", 100, &total)
# (requires pumping mode with PUMP_UPDATE_BIDASK)
```

## Response Fields — `RateInfo` Structure (OHLCV Bar)

```python
import ctypes

class RateInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",    ctypes.c_int),    # Bar open time (Unix timestamp)
        ("open",   ctypes.c_double), # Open price
        ("high",   ctypes.c_double), # High price
        ("low",    ctypes.c_double), # Low price
        ("close",  ctypes.c_double), # Close price
        ("vol",    ctypes.c_double), # Volume (tick count)
    ]
```

## RateInfo Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `ctm` | `int` | Bar open time (Unix timestamp) | `1700100000` |
| `open` | `double` | Opening price of the bar | `1.08450` |
| `high` | `double` | Highest price within bar | `1.08620` |
| `low` | `double` | Lowest price within bar | `1.08380` |
| `close` | `double` | Closing price of the bar | `1.08550` |
| `vol` | `double` | Tick volume (number of ticks in bar) | `1523.0` |

## Response Fields — `ChartInfo` Request Structure

```python
import ctypes

class ChartInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",   ctypes.c_char * 12), # Symbol name
        ("period",   ctypes.c_int),       # Timeframe in minutes
        ("timesign", ctypes.c_int),       # Start time (Unix ts)
        ("count",    ctypes.c_int),       # Max bars to return
    ]
```

## Timeframe `period` Values

| Value | Constant | Description |
|-------|----------|-------------|
| `1` | `PERIOD_M1` | 1 minute |
| `5` | `PERIOD_M5` | 5 minutes |
| `15` | `PERIOD_M15` | 15 minutes |
| `30` | `PERIOD_M30` | 30 minutes |
| `60` | `PERIOD_H1` | 1 hour |
| `240` | `PERIOD_H4` | 4 hours |
| `1440` | `PERIOD_D1` | 1 day |
| `10080` | `PERIOD_W1` | 1 week |
| `43200` | `PERIOD_MN1` | 1 month |

## Response Fields — `TickAPI` Structure (Tick History)

```python
import ctypes

class TickAPI(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",  ctypes.c_int),    # Tick time (Unix timestamp)
        ("bid",  ctypes.c_double), # Bid price
        ("ask",  ctypes.c_double), # Ask price
    ]
```

## TickAPI Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `ctm` | `int` | Tick timestamp (Unix) | `1700100001` |
| `bid` | `double` | Bid price | `1.08450` |
| `ask` | `double` | Ask price | `1.08460` |

## Response Fields — `TickInfo` Structure (Last Ticks, pumping)

```python
import ctypes

class TickInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol", ctypes.c_char * 12), # Symbol name
        ("ctm",    ctypes.c_int),       # Tick time
        ("bid",    ctypes.c_double),    # Bid price
        ("ask",    ctypes.c_double),    # Ask price
    ]
```

## TickRequest Structure

```python
import ctypes

class TickRequest(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",    ctypes.c_char * 12), # Symbol name
        ("from_time", ctypes.c_int),       # Start time (Unix ts)
        ("to_time",   ctypes.c_int),       # End time (Unix ts)
        ("reserved",  ctypes.c_int * 4),  # Reserved
    ]
```

## Related Functions

| Function | Description |
|----------|-------------|
| `ChartRequest(*req, *total)` | Request bar history |
| `ChartAdd(symbol, period, *bars, count)` | **WRITE** — Add bars to history |
| `ChartUpdate(symbol, period, *bars, count)` | **WRITE** — Update bars |
| `ChartDelete(symbol, period, from, to)` | **WRITE** — Delete bars |
| `TicksRequest(*req, *total)` | Request tick history |
| `TickInfoLast(symbol, count, *total)` | Get last N ticks (pumping) |
| `HistoryCorrect(symbol, period)` | Rebuild higher timeframe bars |
