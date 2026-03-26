# TradesRequest / TradesUserHistory — Retrieve Trade Records

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve open positions, pending orders, and closed trade history.
The `TradeRecord` structure covers all order types in MT4.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `TradesRequest(*total)`, `TradesUserHistory(login, from, to, *total)`, `TradeRecordsRequest(tickets[], count, *total)` |

## Example Code

```python
import ctypes, time

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login first

# --- All open/pending orders (pumping mode) ---
total = ctypes.c_int(0)
# TradeRecord* trades = manager->TradesGet(&total)
# Iterate: for i in range(total.value): trade = trades[i]
# Free: manager->MemFree(trades)

# --- Trade history for a specific user ---
from_time = int(time.mktime(time.strptime("2025-01-01", "%Y-%m-%d")))
to_time   = int(time.time())
total = ctypes.c_int(0)
# TradeRecord* hist = manager->TradesUserHistory(52, from_time, to_time, &total)
# print(f"Got {total.value} history records")

# --- Specific orders by ticket numbers ---
tickets = (ctypes.c_int * 3)(1001, 1002, 1003)
total   = ctypes.c_int(0)
# TradeRecord* records = manager->TradeRecordsRequest(tickets, 3, &total)

# --- All trades from admin DB ---
# TradeRecord* all = manager->AdmTradesRequest("*", &total)
```

## Response Fields — `TradeRecord` Structure

```python
import ctypes

class TradeRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("order",            ctypes.c_int),        # Order ticket number
        ("login",            ctypes.c_int),        # Account login
        ("symbol",           ctypes.c_char * 12),  # Symbol (e.g. "EURUSD")
        ("digits",           ctypes.c_int),        # Price decimal places
        ("cmd",              ctypes.c_int),        # Operation type (see below)
        ("volume",           ctypes.c_int),        # Volume in 0.01 lots (e.g. 100=1.00)
        ("open_time",        ctypes.c_int),        # Open/place time (Unix ts)
        ("state",            ctypes.c_int),        # Order state (see below)
        ("open_price",       ctypes.c_double),     # Open/limit price
        ("sl",               ctypes.c_double),     # Stop loss price
        ("tp",               ctypes.c_double),     # Take profit price
        ("close_time",       ctypes.c_int),        # Close time (Unix ts); 0=open
        ("value_date",       ctypes.c_int),        # Value date (for balance ops)
        ("expiration",       ctypes.c_int),        # Expiration time (pending orders)
        ("reason",           ctypes.c_int),        # Modification reason (see below)
        ("conv_rates",       ctypes.c_double * 2), # Conversion rates [open, close]
        ("commission",       ctypes.c_double),     # Commission charged
        ("commission_agent", ctypes.c_double),     # Agent commission
        ("storage",          ctypes.c_double),     # Accumulated swap/rollover
        ("close_price",      ctypes.c_double),     # Close price
        ("profit",           ctypes.c_double),     # Profit/loss (in deposit currency)
        ("taxes",            ctypes.c_double),     # Tax amount
        ("magic",            ctypes.c_int),        # EA magic number
        ("comment",          ctypes.c_char * 32),  # Order comment
        ("margin_rate",      ctypes.c_double),     # Margin conversion rate
        ("timestamp",        ctypes.c_int),        # Last modification timestamp
        ("reserved",         ctypes.c_uint * 4),  # Reserved
    ]
```

## Field Reference Table

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `order` | `int` | Unique order ticket number | `123456` |
| `login` | `int` | Account login that owns this order | `52` |
| `symbol` | `char[12]` | Trading symbol | `"EURUSD"` |
| `digits` | `int` | Symbol decimal places | `5` |
| `cmd` | `int` | Order type (0–7, see table) | `0` (Buy) |
| `volume` | `int` | Volume × 100 (e.g. 1.00 lot = 100) | `100` |
| `open_time` | `int` | Open/placement time (Unix timestamp) | `1700000000` |
| `state` | `int` | Order state (see table) | `0` (Open) |
| `open_price` | `double` | Open price (market) or limit price (pending) | `1.08500` |
| `sl` | `double` | Stop loss price (0 = no SL) | `1.08000` |
| `tp` | `double` | Take profit price (0 = no TP) | `1.09000` |
| `close_time` | `int` | Close time; 0 for open/pending orders | `0` |
| `value_date` | `int` | Value date for balance operations | `0` |
| `expiration` | `int` | Expiry time for pending orders (0=GTC) | `0` |
| `reason` | `int` | Who placed/modified the order | `0` (Client) |
| `conv_rates[0]` | `double` | Open conversion rate (symbol→deposit) | `1.0` |
| `conv_rates[1]` | `double` | Close conversion rate | `1.0` |
| `commission` | `double` | Commission charged on open | `-2.50` |
| `commission_agent` | `double` | Agent/IB commission | `0.0` |
| `storage` | `double` | Accumulated overnight swap | `-0.50` |
| `close_price` | `double` | Current market price (or close price) | `1.08750` |
| `profit` | `double` | Unrealized/realized profit in account currency | `250.00` |
| `taxes` | `double` | Tax deducted | `0.0` |
| `magic` | `int` | Expert Advisor magic number | `0` |
| `comment` | `char[32]` | Order comment string | `"manual"` |
| `margin_rate` | `double` | Margin currency conversion rate | `1.0` |
| `timestamp` | `int` | Last modification timestamp | `1700000000` |

## `cmd` — Order Type Values

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `OP_BUY` | Market Buy position |
| `1` | `OP_SELL` | Market Sell position |
| `2` | `OP_BUY_LIMIT` | Buy Limit pending order |
| `3` | `OP_SELL_LIMIT` | Sell Limit pending order |
| `4` | `OP_BUY_STOP` | Buy Stop pending order |
| `5` | `OP_SELL_STOP` | Sell Stop pending order |
| `6` | `OP_BALANCE` | Balance deposit/withdrawal |
| `7` | `OP_CREDIT` | Credit operation |

## `state` — Order State Values

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `TS_OPEN_NORMAL` | Open/active order |
| `1` | `TS_OPEN_REMAND` | On hold/suspended |
| `2` | `TS_OPEN_RESTORED` | Restored from backup |
| `3` | `TS_CLOSED_NORMAL` | Closed normally |
| `4` | `TS_CLOSED_PART` | Partially closed |
| `5` | `TS_CLOSED_BY` | Closed by opposite position |
| `6` | `TS_DELETED` | Deleted |

## `reason` — Modification Reason Values

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `REASON_CLIENT` | Client terminal |
| `1` | `REASON_EXPERT` | Expert Advisor |
| `2` | `REASON_DEALER` | Dealer/manager |
| `3` | `REASON_SIGNAL` | Signal service |
| `4` | `REASON_GATEWAY` | Gateway |
| `5` | `REASON_MOBILE` | Mobile terminal |
| `6` | `REASON_WEB` | Web terminal |
| `7` | `REASON_API` | API |

## Related Functions

| Function | Description |
|----------|-------------|
| `TradesRequest(*total)` | All trades from pumping cache |
| `TradesGet(*total)` | All open trades in pumping mode |
| `TradesGetBySymbol(symbol, *total)` | Trades for a symbol (pumping) |
| `TradesGetByLogin(login, group, *total)` | Trades for a login (pumping) |
| `TradesGetByMarket(symbol, *total)` | Market orders for symbol (pumping) |
| `TradeRecordGet(order, *info)` | Single trade by ticket (pumping) |
| `TradesUserHistory(login, from, to, *total)` | Closed history for a user |
| `ReportsRequest(from, to, *request, *total)` | Closed positions for reporting |
| `TradeRecordsRequest(tickets[], count, *total)` | Trades by ticket list |
| `TradeTransaction(*trans, *trans_info, *result)` | **WRITE** — Execute trade |
| `TradeCalcProfit(*trade)` | Calculate profit for an open order |
| `TradeCheckStops(cmd, symbol, open, sl, tp)` | Validate SL/TP levels |
| `AdmTradesRequest(group, *total)` | Admin: all trades from DB |
| `AdmTradesDelete(tickets[], count)` | **WRITE ADMIN** — Delete orders |
| `AdmTradeRecordModify(*trade)` | **WRITE ADMIN** — Modify DB record |
