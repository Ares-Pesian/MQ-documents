# SymbolsGetAll / SymbolGet — Retrieve Symbol Configuration

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve symbol (instrument) configuration from the MT4 server.
Returns full `ConSymbol` configuration or lightweight `SymbolInfo` market-watch snapshot.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `SymbolsRefresh()`, `SymbolsGetAll(*total)`, `SymbolGet(symbol, *cs)`, `SymbolInfoGet(symbol, *info)`, `SymbolInfoUpdated(*total)` |

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login

# --- Refresh symbol list from server ---
# manager->SymbolsRefresh()  # updates local symbol cache

# --- Get ALL symbol full configs ---
total = ctypes.c_int(0)
# ConSymbol* syms = manager->SymbolsGetAll(&total)
# print(f"Total symbols: {total.value}")
# for i in range(total.value):
#     print(syms[i].symbol.decode(), syms[i].digits, syms[i].spread)
# manager->MemFree(syms)

# --- Get single symbol config ---
cs = ConSymbol()
# manager->SymbolGet("EURUSD", &cs)

# --- Get lightweight SymbolInfo (Market Watch) ---
info = SymbolInfo()
# manager->SymbolInfoGet("EURUSD", &info)
# print(info.bid, info.ask, info.digits)

# --- Get all updated SymbolInfo (for quotes) ---
total = ctypes.c_int(0)
# SymbolInfo* infos = manager->SymbolInfoUpdated(&total)
# (called from PUMP_UPDATE_BIDASK callback)
```

## Response Fields — `SymbolInfo` Structure (Market Watch / Bid-Ask)

```python
import ctypes

class SymbolInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",        ctypes.c_char * 12),  # Symbol name
        ("digits",        ctypes.c_int),        # Decimal places
        ("spread",        ctypes.c_int),        # Current spread (in points)
        ("spread_float",  ctypes.c_int),        # Floating spread flag
        ("direction",     ctypes.c_int),        # Quote direction
        ("bid",           ctypes.c_double),     # Current bid price
        ("ask",           ctypes.c_double),     # Current ask price
        ("session_price", ctypes.c_double),     # Session open price
        ("high",          ctypes.c_double),     # Session high
        ("low",           ctypes.c_double),     # Session low
        ("time",          ctypes.c_int),        # Last quote time (Unix ts)
        ("reserved",      ctypes.c_int * 8),   # Reserved
    ]
```

## SymbolInfo Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `symbol` | `char[12]` | Symbol name | `"EURUSD"` |
| `digits` | `int` | Decimal precision | `5` |
| `spread` | `int` | Current spread in points | `10` |
| `spread_float` | `int` | 1=floating spread, 0=fixed | `1` |
| `direction` | `int` | Quote direction indicator | `0` |
| `bid` | `double` | Current bid price | `1.08450` |
| `ask` | `double` | Current ask price | `1.08460` |
| `session_price` | `double` | Session open/first price | `1.08300` |
| `high` | `double` | Session high price | `1.08600` |
| `low` | `double` | Session low price | `1.08100` |
| `time` | `int` | Timestamp of last quote | `1700100000` |

## Response Fields — `ConSymbol` Structure (Full Config)

```python
import ctypes

class ConSessions(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("open",    ctypes.c_uint),  # Session open time (minutes from midnight)
        ("close",   ctypes.c_uint),  # Session close time
    ]

class ConSymbol(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",              ctypes.c_char * 12),      # Symbol name
        ("description",         ctypes.c_char * 64),      # Description
        ("source",              ctypes.c_char * 12),      # Feed source
        ("currency",            ctypes.c_char * 12),      # Quote currency
        ("type",                ctypes.c_int),            # Security type
        ("digits",              ctypes.c_int),            # Decimal places
        ("chart_mode",          ctypes.c_int),            # Chart mode
        ("trade",               ctypes.c_int),            # Trade mode
        ("background_color",    ctypes.c_uint),           # UI color
        ("count",               ctypes.c_int),            # Subscribed clients count
        ("count_original",      ctypes.c_int),            # Original count
        ("external_audit",      ctypes.c_int),            # External audit flag
        ("sessions_quotes",     ConSessions * 7 * 7),     # Quote sessions [day][session]
        ("sessions_trade",      ConSessions * 7 * 7),     # Trade sessions [day][session]
        ("profit_mode",         ctypes.c_int),            # Profit calc mode
        ("filter",              ctypes.c_int),            # Filter enabled
        ("filter_counter",      ctypes.c_int),            # Filter counter
        ("filter_limit",        ctypes.c_double),         # Filter limit (points)
        ("filter_smoothing",    ctypes.c_int),            # Filter smoothing
        ("filter_hard",         ctypes.c_int),            # Hard filter enabled
        ("filter_hard_limit",   ctypes.c_double),         # Hard filter limit
        ("logging",             ctypes.c_int),            # Logging enabled
        ("spread",              ctypes.c_int),            # Spread (points)
        ("spread_balance",      ctypes.c_int),            # Balance spread
        ("exemode",             ctypes.c_int),            # Execution mode
        ("swap_enable",         ctypes.c_int),            # Swaps enabled
        ("swap_type",           ctypes.c_int),            # Swap calculation type
        ("swap_long",           ctypes.c_double),         # Long swap rate
        ("swap_short",          ctypes.c_double),         # Short swap rate
        ("swap_rollover3days",  ctypes.c_int),            # 3-day rollover weekday
        ("contract_size",       ctypes.c_double),         # Contract size
        ("tick_size",           ctypes.c_double),         # Minimum price change
        ("tick_price",          ctypes.c_double),         # Tick monetary value
        ("point_size",          ctypes.c_double),         # Point size
        ("multiply",            ctypes.c_double),         # Price multiplier
        ("bid_tickvalue",       ctypes.c_double),         # Bid tick value
        ("ask_tickvalue",       ctypes.c_double),         # Ask tick value
        ("long_only",           ctypes.c_int),            # Long-only restriction
        ("instant_max_volume",  ctypes.c_int),            # Max instant exec volume
        ("margin_mode",         ctypes.c_int),            # Margin calc mode
        ("margin_initial",      ctypes.c_double),         # Initial margin per lot
        ("margin_maintenance",  ctypes.c_double),         # Maintenance margin/lot
        ("margin_hedged",       ctypes.c_double),         # Hedged margin
        ("margin_divider",      ctypes.c_double),         # Margin divider
        ("margin_currency",     ctypes.c_char * 12),      # Margin currency
        ("freeze_level",        ctypes.c_double),         # Freeze level (points)
        ("stops_level",         ctypes.c_int),            # Min stops distance (pts)
        ("ie_deviation",        ctypes.c_int),            # IE allowed deviation
        ("ie_quick_mode",       ctypes.c_int),            # IE quick mode
        ("hedge_prohibited",    ctypes.c_int),            # Hedging prohibited
        ("value_date",          ctypes.c_int),            # Value date offset
        ("quote_list",          ctypes.c_int),            # In selected symbols list
        ("recount",             ctypes.c_int),            # Recount flag
        ("reserved",            ctypes.c_int * 23),       # Reserved
    ]
```

## ConSymbol Field Reference Table

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `symbol` | `char[12]` | Symbol name | `"EURUSD"` |
| `description` | `char[64]` | Human-readable description | `"Euro vs US Dollar"` |
| `source` | `char[12]` | Data feed source name | `"LMAX"` |
| `currency` | `char[12]` | Quote/profit currency | `"USD"` |
| `type` | `int` | Security type (0=Forex, 1=CFD, etc.) | `0` |
| `digits` | `int` | Decimal places | `5` |
| `trade` | `int` | Trade mode (0=disabled, 1=close-only, 2=full) | `2` |
| `spread` | `int` | Fixed spread in points | `10` |
| `exemode` | `int` | Execution: 0=instant, 1=request, 2=market, 3=exchange | `0` |
| `swap_enable` | `int` | 1=swaps enabled, 0=disabled | `1` |
| `swap_type` | `int` | 0=points, 1=%, 2=money, 3=margin% | `0` |
| `swap_long` | `double` | Long swap per day | `-0.50` |
| `swap_short` | `double` | Short swap per day | `-0.30` |
| `swap_rollover3days` | `int` | Day of 3-day swap (3=Wed) | `3` |
| `contract_size` | `double` | Contract size (e.g. 100000 for forex) | `100000.0` |
| `tick_size` | `double` | Minimum price increment | `0.00001` |
| `tick_price` | `double` | Monetary value of one tick | `1.0` |
| `point_size` | `double` | Point size | `0.00001` |
| `margin_initial` | `double` | Required margin per 1.0 lot | `1000.0` |
| `margin_maintenance` | `double` | Maintenance margin per 1.0 lot | `500.0` |
| `margin_hedged` | `double` | Hedged position margin | `500.0` |
| `margin_currency` | `char[12]` | Margin calculation currency | `"USD"` |
| `freeze_level` | `double` | Price freeze zone (points) | `0.0` |
| `stops_level` | `int` | Minimum distance for stops (points) | `10` |

## SymbolSummary Structure (Open Interest / Exposure)

| Field | C Type | Description |
|-------|--------|-------------|
| `symbol` | `char[12]` | Symbol name |
| `count` | `int` | Number of open positions |
| `volume` | `int` | Total client volume (×100) |
| `volume_buy` | `int` | Total buy volume |
| `volume_sell` | `int` | Total sell volume |
| `profit` | `double` | Total floating profit |
| `hedged` | `int` | Hedged volume |
| `hedged_buy` | `double` | Hedged buy volume |
| `hedged_sell` | `double` | Hedged sell volume |

## Related Functions

| Function | Description |
|----------|-------------|
| `SymbolsRefresh()` | Refresh symbol list from server |
| `SymbolsGetAll(*total)` | All full symbol configs |
| `SymbolGet(name, *cs)` | Single symbol full config |
| `SymbolInfoGet(name, *info)` | Single symbol market-watch snapshot |
| `SymbolInfoUpdated(*total)` | All symbols with updated quotes |
| `SymbolAdd(symbol)` | **WRITE** — Add to Market Watch |
| `SymbolHide(symbol)` | **WRITE** — Remove from Market Watch |
| `SymbolChange(*cs)` | **WRITE** — Modify symbol settings |
| `SymbolSendTick(symbol, bid, ask)` | **WRITE** — Inject tick |
| `SymbolsGroupsGet(*total)` | Symbol group list (pumping) |
