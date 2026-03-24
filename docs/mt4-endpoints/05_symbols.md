# Symbols

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Symbols](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_symbol)

---

## Overview

Symbol data in MT4 includes the full specification of each financial instrument: pricing rules,
trading sessions, margin requirements, execution mode, spread settings, and contract sizes.

Two levels of symbol data:
- **`SymbolInfo`** — lightweight: last bid/ask, name, group (from Market Watch cache)
- **`ConSymbol`** — full configuration: all symbol settings from the server config database

---

## Methods

| Method | Purpose |
|--------|---------|
| `SymbolsRefresh` | Download full symbol list from server (cached to `symbols.raw`) |
| `SymbolsGetAll` | Get all symbols from local cache (call after `SymbolsRefresh`) |
| `SymbolGet` | Get single symbol by name from local cache |
| `SymbolInfoGet` | Get `SymbolInfo` (last quote + basic info) for a selected symbol |
| `SymbolsGroupsGet` | Get symbol groups |
| `SymbolAdd` | Add symbol to Market Watch (selected symbols list) |
| `SymbolHide` | Remove symbol from Market Watch |
| `SymbolChange` | Edit spread, execution mode, limit/stop levels for a symbol |
| `SymbolSendTick` | Inject a custom tick into the quote stream |
| `SymbolInfoUpdated` | Get symbols updated since last call (pumping mode) |

---

## Example Code

```python
import ctypes

# ─── SymbolsRefresh — download and cache all symbols ────────────────────────
ret = manager.SymbolsRefresh()
print(f"SymbolsRefresh: {ret}")   # 0 = RET_OK

# ─── SymbolsGetAll — get full list from cache ────────────────────────────────
total = ctypes.c_int(0)
syms_ptr = manager.SymbolsGetAll(ctypes.byref(total))

if syms_ptr:
    print(f"Total symbols: {total.value}")
    ConSymbolArray = ConSymbol * total.value
    symbols = ctypes.cast(syms_ptr, ctypes.POINTER(ConSymbolArray)).contents
    records = [struct_to_dict(s) for s in symbols]
    # No MemFree needed for SymbolsGetAll — returns internal cache pointer
    print(records[0]["symbol"], records[0]["digits"], records[0]["point"])

# ─── SymbolGet — single symbol ───────────────────────────────────────────────
sym = ConSymbol()
ret = manager.SymbolGet(b"EURUSD", ctypes.byref(sym))
if ret == 0:
    print(f"EURUSD digits={sym.digits} spread={sym.spread} point={sym.point}")

# ─── SymbolInfoGet — last quote info ─────────────────────────────────────────
info = SymbolInfo()
ret = manager.SymbolInfoGet(b"EURUSD", ctypes.byref(info))
if ret == 0:
    print(f"EURUSD bid={info.bid} ask={info.ask}")
```

---

## SymbolInfo Structure

Lightweight quote + summary for a symbol in Market Watch.

```python
class SymbolInfo(ctypes.Structure):
    _fields_ = [
        ("symbol",          ctypes.c_char * 12),
        ("description",     ctypes.c_char * 64),
        ("source",          ctypes.c_char * 12),
        ("currency",        ctypes.c_char * 12),
        ("type",            ctypes.c_int),
        ("digits",          ctypes.c_int),
        ("trade",           ctypes.c_int),
        ("background_color", ctypes.c_uint32),
        ("count",           ctypes.c_int),
        ("count_original",  ctypes.c_int),
        ("reserved",        ctypes.c_int * 4),
        ("point",           ctypes.c_double),
        ("spread",          ctypes.c_int),
        ("spread_balance",  ctypes.c_int),
        ("direction",       ctypes.c_int),
        ("filtered",        ctypes.c_int),
        ("last_quote",      ctypes.c_int),       # timestamp of last tick
        ("bid",             ctypes.c_double),
        ("ask",             ctypes.c_double),
        ("low",             ctypes.c_double),
        ("high",            ctypes.c_double),
        ("commission",      ctypes.c_double),
    ]
```

---

## ConSymbol Structure — Key Fields

Full symbol configuration. Very large struct (~500+ bytes).

| Field | C++ Type | ctypes | Description | Example |
|-------|----------|--------|-------------|---------|
| `symbol` | `char[12]` | `c_char*12` | Symbol name | `"EURUSD"` |
| `description` | `char[64]` | `c_char*64` | Full name / description | `"Euro vs US Dollar"` |
| `source` | `char[12]` | `c_char*12` | Data feed source | `"IQ"` |
| `currency` | `char[12]` | `c_char*12` | Profit currency | `"USD"` |
| `type` | `int` | `c_int` | Instrument type (see enum) | `0` |
| `digits` | `int` | `c_int` | Price decimal digits | `5` |
| `point` | `double` | `c_double` | One point value | `0.00001` |
| `multiply` | `double` | `c_double` | Price multiplier | `1.0` |
| `spread` | `int` | `c_int` | Fixed spread in points | `2` |
| `spread_balance` | `int` | `c_int` | Balance spread correction | `0` |
| `stops_level` | `int` | `c_int` | Min SL/TP distance from price (points) | `10` |
| `bid_tickvalue` | `double` | `c_double` | Tick value for 1 lot at bid | `1.0` |
| `ask_tickvalue` | `double` | `c_double` | Tick value for 1 lot at ask | `1.0` |
| `contract_size` | `double` | `c_double` | Contract size (units per lot) | `100000.0` |
| `tick_size` | `double` | `c_double` | Minimum price change | `0.00001` |
| `tick_value` | `double` | `c_double` | Value per tick per lot | `1.0` |
| `profit_mode` | `int` | `c_int` | Profit calc mode (see enum) | `0` |
| `swap_enable` | `int` | `c_int` | Swap enabled: 1=yes | `1` |
| `swap_type` | `int` | `c_int` | Swap calculation type | `0` |
| `swap_long` | `double` | `c_double` | Swap rate for long positions | `-3.5` |
| `swap_short` | `double` | `c_double` | Swap rate for short positions | `1.2` |
| `swap_rollover3days` | `int` | `c_int` | Triple swap day (0=Mon...4=Fri) | `2` |
| `margin_mode` | `int` | `c_int` | Margin calculation mode | `0` |
| `margin_initial` | `double` | `c_double` | Initial margin per lot | `0.0` |
| `margin_maintenance` | `double` | `c_double` | Maintenance margin per lot | `0.0` |
| `margin_hedged` | `double` | `c_double` | Hedged margin rate | `0.5` |
| `margin_divider` | `double` | `c_double` | Margin divider | `1.0` |
| `exemode` | `int` | `c_int` | Execution mode (see enum) | `0` |
| `instant_max_volume` | `int` | `c_int` | Max volume for instant execution | `100` |
| `trade` | `int` | `c_int` | Trading allowed: 0=none,1=close,2=full | `2` |
| `background_color` | `uint32` | `c_uint32` | Chart background color | `0` |

---

## Enumerations

### Symbol Type

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `SYMBOL_TYPE_FOREX` | Forex pair |
| `1` | `SYMBOL_TYPE_CFD` | CFD |
| `2` | `SYMBOL_TYPE_FUTURES` | Futures |
| `3` | `SYMBOL_TYPE_STOCKS` | Stocks |
| `4` | `SYMBOL_TYPE_INDICES` | Indices |
| `5` | `SYMBOL_TYPE_BONDS` | Bonds |
| `6` | `SYMBOL_TYPE_OPTION` | Options |
| `7` | `SYMBOL_TYPE_COMMODITY` | Commodities |

### Execution Mode (`exemode`)

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `EXE_INSTANT` | Instant execution |
| `1` | `EXE_REQUEST` | Request execution |
| `2` | `EXE_MARKET` | Market execution |
| `3` | `EXE_EXCHANGE` | Exchange execution |

### Profit Mode

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `PROFIT_CALC_FOREX` | Forex (with conversion) |
| `1` | `PROFIT_CALC_CFD` | CFD |
| `2` | `PROFIT_CALC_FUTURES` | Futures |

---

## Sample Raw Response — SymbolInfo (JSON)

```json
{
  "symbol": "EURUSD",
  "description": "Euro vs US Dollar",
  "source": "IQ",
  "currency": "USD",
  "type": 0,
  "digits": 5,
  "trade": 2,
  "background_color": 0,
  "count": 150,
  "point": 0.00001,
  "spread": 2,
  "spread_balance": 0,
  "direction": 0,
  "filtered": 0,
  "last_quote": 1711190400,
  "bid": 1.08325,
  "ask": 1.08327,
  "low": 1.08100,
  "high": 1.08500,
  "commission": 0.0
}
```

---

## Notes

- `SymbolsRefresh` saves symbol data to `symbols.raw` in the Manager API working directory.
  On subsequent calls, only changed symbols are re-downloaded.
- The pointer returned by `SymbolsGetAll` points to the **internal cache** — do **not** call `MemFree`.
- For real-time quote updates in pumping mode, use `SymbolInfoUpdated` after `PUMP_UPDATE_BIDASK`.
- `ConSymbol` has many more fields (sessions, margin rates per group, etc.) — see `MT4ManagerAPI.h`.
