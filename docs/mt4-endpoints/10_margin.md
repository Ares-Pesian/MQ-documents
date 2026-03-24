# Margin State

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Trading / Margin State](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_trade/manager_api_trade_margin)

---

## Overview

The Margin State API returns real-time margin levels for all accounts. Used to identify accounts
approaching margin call or stop-out conditions.

---

## Methods

| Method | Purpose |
|--------|---------|
| `MarginsGet` | Get all margin levels (pumping mode) |
| `MarginLevelGet` | Get margin level for a specific account (pumping) |
| `MarginLevelRequest` | Request margin level for a specific account (direct) |

---

## Example Code

```python
import ctypes

# In pumping mode — after PUMP_UPDATE_MARGINCALL fires:

# ─── MarginsGet — all margin levels ──────────────────────────────────────────
total = ctypes.c_int(0)
margins_ptr = manager.MarginsGet(ctypes.byref(total))

if margins_ptr:
    print(f"Margin records: {total.value}")
    MarginLevelArray = MarginLevel * total.value
    margins = ctypes.cast(margins_ptr, ctypes.POINTER(MarginLevelArray)).contents
    records = [struct_to_dict(m) for m in margins]
    print(records[0])


# ─── MarginLevelGet — single account ─────────────────────────────────────────
ml = MarginLevel()
ret = manager.MarginLevelGet(1001, ctypes.byref(ml))
if ret == 0:
    print(f"Login: {ml.login} Equity: {ml.equity} Level: {ml.margin_level}%")
```

---

## MarginLevel Structure

```python
class MarginLevel(ctypes.Structure):
    _fields_ = [
        ("login",         ctypes.c_int),
        ("group",         ctypes.c_char * 16),
        ("leverage",      ctypes.c_int),
        ("updated",       ctypes.c_int),      # last update timestamp
        ("balance",       ctypes.c_double),
        ("equity",        ctypes.c_double),
        ("margin",        ctypes.c_double),
        ("margin_free",   ctypes.c_double),
        ("margin_level",  ctypes.c_double),   # margin level % (equity/margin*100)
        ("reserved",      ctypes.c_int * 4),
    ]
```

---

## Response Fields

| Field | C++ Type | ctypes | Description | Example |
|-------|----------|--------|-------------|---------|
| `login` | `int` | `c_int` | Account login | `1001` |
| `group` | `char[16]` | `c_char*16` | Account group | `"real\\standard"` |
| `leverage` | `int` | `c_int` | Account leverage | `100` |
| `updated` | `int` (time_t) | `c_int` | Last update timestamp | `1711190400` |
| `balance` | `double` | `c_double` | Account balance | `10000.00` |
| `equity` | `double` | `c_double` | Account equity | `9500.00` |
| `margin` | `double` | `c_double` | Used margin | `8000.00` |
| `margin_free` | `double` | `c_double` | Free margin | `1500.00` |
| `margin_level` | `double` | `c_double` | Margin level % (equity/margin × 100) | `118.75` |

---

## Margin Level Thresholds

| Level % | State |
|---------|-------|
| > 200% | Healthy |
| 100–200% | Watch |
| 100% | **Margin Call** (configured per group) |
| 50% | **Stop Out** (configured per group — closes positions) |
| 0% | No open positions |

Actual margin call and stop-out levels are configured per group in `ConGroup::margin_call` and `ConGroup::margin_stopout`.

---

## Sample Raw Response (JSON)

```json
{
  "login": 1001,
  "group": "real\\standard",
  "leverage": 100,
  "updated": 1711190400,
  "balance": 10000.00,
  "equity": 9500.00,
  "margin": 8000.00,
  "margin_free": 1500.00,
  "margin_level": 118.75
}
```

---

## Notes

- In pumping mode, `PUMP_UPDATE_MARGINCALL` fires when margin state changes. Then call `MarginsGet`.
- `margin_level = 0` when the account has no open positions (margin = 0, division by zero avoided).
- Stop-out accounts will have positions automatically closed by the server — watch for `reason = 3` (`TR_REASON_STOPOUT`) in `TradeRecord`.
