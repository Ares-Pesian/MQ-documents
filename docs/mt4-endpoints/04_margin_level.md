# MarginLevelGet / MarginsGet — Retrieve Margin State

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve real-time margin state (balance, equity, margin, free margin, profit) for
one or multiple accounts. Used for risk management and monitoring.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `MarginLevelGet(login, *margin)`, `MarginsGet(logins[], count, *total)` |
| **Mode** | Requires pumping mode (`PumpingSwitch`) |

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect, login, start pumping

# --- Single account margin state ---
margin = MarginLevel()
# ret = manager->MarginLevelGet(52, &margin)
# print(f"Balance: {margin.balance}, Equity: {margin.equity}")
# print(f"Margin: {margin.margin}, Free: {margin.margin_free}")
# print(f"Level: {margin.margin_level:.1f}%")

# --- Multiple accounts at once ---
logins = (ctypes.c_int * 3)(52, 53, 54)
total  = ctypes.c_int(0)
# MarginLevel* margins = manager->MarginsGet(logins, 3, &total)
# for i in range(total.value):
#     m = margins[i]
#     print(m.login, m.balance, m.equity, m.margin_level)
# manager->MemFree(margins)

# --- All margin-call accounts (from PUMP_UPDATE_MARGINCALL) ---
# MarginLevel* mc = manager->MarginsGet(None, 0, &total)  # all MC accounts
```

## Response Fields — `MarginLevel` Structure

```python
import ctypes

class MarginLevel(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("login",               ctypes.c_int),    # Account login
        ("group",               ctypes.c_char * 16), # Account group
        ("balance",             ctypes.c_double), # Current balance
        ("equity",              ctypes.c_double), # Current equity (balance + floating)
        ("margin",              ctypes.c_double), # Used margin
        ("margin_free",         ctypes.c_double), # Free margin
        ("margin_level",        ctypes.c_double), # Margin level %
        ("margin_initial",      ctypes.c_double), # Initial margin requirement
        ("margin_maintenance",  ctypes.c_double), # Maintenance margin
        ("profit_loss",         ctypes.c_double), # Total floating P&L
        ("assets",              ctypes.c_double), # Total assets
        ("liabilities",         ctypes.c_double), # Total liabilities
        ("floating",            ctypes.c_double), # Floating P&L on open positions
    ]
```

## Field Reference Table

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `login` | `int` | Account login number | `52` |
| `group` | `char[16]` | Account group | `"real\managers"` |
| `balance` | `double` | Current account balance | `10000.00` |
| `equity` | `double` | Balance + floating P&L | `10250.00` |
| `margin` | `double` | Margin currently in use | `500.00` |
| `margin_free` | `double` | Available free margin | `9750.00` |
| `margin_level` | `double` | Margin level as percentage | `2050.0` (%) |
| `margin_initial` | `double` | Initial (required) margin | `500.00` |
| `margin_maintenance` | `double` | Maintenance margin level | `250.00` |
| `profit_loss` | `double` | Net P&L across all positions | `250.00` |
| `assets` | `double` | Total account assets | `10250.00` |
| `liabilities` | `double` | Total liabilities | `0.00` |
| `floating` | `double` | Floating P&L on open trades | `250.00` |

## Related Functions

| Function | Description |
|----------|-------------|
| `MarginLevelGet(login, *margin)` | Single account margin state |
| `MarginsGet(logins[], count, *total)` | Multiple accounts margin state |
| `TradeCalcProfit(*trade)` | Calculate profit for specific trade |
| `TradeCheckStops(cmd, symbol, open, sl, tp)` | Validate stop levels |
