# ReportsRequest / DailyReportsRequest — Trade Reports & Daily Snapshots

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve closed position history for custom reporting (`ReportsRequest`) and
end-of-day account snapshots (`DailyReportsRequest`).

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `ReportsRequest(*req, *total)`, `DailyReportsRequest(*req, *total)` |

## Example Code

```python
import ctypes, time

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login

# --- Closed positions for report generation ---
req = ReportGroupRequest()
req.login       = 52
req.group[:]    = b"real\*\x00"   # group mask
req.from_time   = int(time.time()) - 86400 * 90   # 90 days ago
req.to_time     = int(time.time())
req.request_type = 0   # 0=by login, 1=by group

total = ctypes.c_int(0)
# TradeRecord* closed = manager->ReportsRequest(&req, &total)
# print(f"Closed positions: {total.value}")
# for i in range(total.value):
#     r = closed[i]
#     print(r.order, r.symbol, r.cmd, r.close_time, r.profit)
# manager->MemFree(closed)

# --- Daily account snapshots ---
daily_req = DailyGroupRequest()
daily_req.login     = 52
daily_req.from_time = int(time.time()) - 86400 * 30
daily_req.to_time   = int(time.time())

total = ctypes.c_int(0)
# DailyReport* daily = manager->DailyReportsRequest(&daily_req, &total)
# for i in range(total.value):
#     d = daily[i]
#     print(d.ctm, d.login, d.balance, d.equity, d.profit)
# manager->MemFree(daily)
```

## Response Fields — `DailyReport` Structure

```python
import ctypes

class DailyReport(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",            ctypes.c_int),    # Snapshot date/time (Unix ts)
        ("login",          ctypes.c_int),    # Account login
        ("group",          ctypes.c_char * 16), # Account group
        ("name",           ctypes.c_char * 64), # Client name
        ("balance",        ctypes.c_double), # Balance at end of day
        ("prev_balance",   ctypes.c_double), # Previous day balance
        ("equity",         ctypes.c_double), # Equity at end of day
        ("margin",         ctypes.c_double), # Used margin
        ("margin_free",    ctypes.c_double), # Free margin
        ("margin_level",   ctypes.c_double), # Margin level %
        ("profit",         ctypes.c_double), # Total profit for the day
        ("credit",         ctypes.c_double), # Credit amount
        ("floating",       ctypes.c_double), # Floating P&L at snapshot
        ("reserved",       ctypes.c_int * 8),# Reserved
    ]
```

## DailyReport Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `ctm` | `int` | End-of-day snapshot timestamp | `1700100000` |
| `login` | `int` | Account login | `52` |
| `group` | `char[16]` | Account group | `"real\managers"` |
| `name` | `char[64]` | Client full name | `"John Doe"` |
| `balance` | `double` | Closing balance for the day | `10250.00` |
| `prev_balance` | `double` | Opening balance for the day | `10000.00` |
| `equity` | `double` | Closing equity | `10500.00` |
| `margin` | `double` | Margin in use at close | `500.00` |
| `margin_free` | `double` | Free margin at close | `10000.00` |
| `margin_level` | `double` | Margin level % at close | `2100.0` |
| `profit` | `double` | Daily realized + unrealized P&L | `250.00` |
| `credit` | `double` | Credit/bonus amount | `0.00` |
| `floating` | `double` | Open position floating P&L | `250.00` |

## Request Structures

### `ReportGroupRequest` — Closed Positions Report Request

| Field | C Type | Description |
|-------|--------|-------------|
| `login` | `int` | Specific login (0 = all) |
| `group` | `char[64]` | Group mask (e.g. `"real\*"`) |
| `from_time` | `int` | Start time (Unix timestamp) |
| `to_time` | `int` | End time (Unix timestamp) |
| `request_type` | `int` | 0=by login, 1=by group |

### `DailyGroupRequest` — Daily Reports Request

| Field | C Type | Description |
|-------|--------|-------------|
| `login` | `int` | Specific login (0 = all) |
| `group` | `char[64]` | Group mask |
| `from_time` | `int` | Start date (Unix timestamp) |
| `to_time` | `int` | End date (Unix timestamp) |

## `StateReport` Structure — End-of-Day Trading State

| Field | C Type | Description |
|-------|--------|-------------|
| `login` | `int` | Account login |
| `balance` | `double` | End-of-day balance |
| `equity` | `double` | End-of-day equity |
| `margin` | `double` | Margin in use |
| `margin_free` | `double` | Free margin |
| `profit` | `double` | Day's profit |

## Related Functions

| Function | Description |
|----------|-------------|
| `ReportsRequest(*req, *total)` | Closed position history (for custom reports) |
| `DailyReportsRequest(*req, *total)` | Daily account snapshots |
| `TradesUserHistory(login, from, to, *total)` | Full trade history for a user |
| `AdmTradesRequest(group, *total)` | Admin: all orders from DB |
