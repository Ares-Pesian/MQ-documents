# Trade History (Closed Deals)

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Trading / Orders](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_trade/manager_api_trade_order)

---

## Overview

Closed trades in MT4 are `TradeRecord` structs where `close_time > 0`.
They represent fully executed and closed positions, as well as balance/credit adjustments.

In MT4 there is no separate "deal" entity like in MT5 — the `TradeRecord` IS the deal.
A closed `TradeRecord` (with `close_time > 0`) is what other platforms call a "deal".

---

## Methods

| Method | Purpose | When to Use |
|--------|---------|-------------|
| `TradesUserHistory` | Get closed trades for one account in a time range | Incremental sync per account |
| `ReportsRequest` | Get report records for a group/date range | Reporting / daily summaries |
| `DailyReportsRequest` | Get daily report records | End-of-day summaries |
| `AdmTradesRequest` | Admin: get all orders (open + closed) by group | Full bootstrap |

---

## Example Code

```python
import ctypes
import time

# ─── TradesUserHistory — closed trades for one account ──────────────────────
login     = 1001
from_time = int(time.mktime(time.strptime("2024-01-01", "%Y-%m-%d")))
to_time   = int(time.time())

total = ctypes.c_int(0)
trades_ptr = manager.TradesUserHistory(login, from_time, to_time, ctypes.byref(total))

if not trades_ptr:
    print("TradesUserHistory failed")
else:
    print(f"Closed trades for login {login}: {total.value}")

    TradeRecordArray = TradeRecord * total.value
    trades = ctypes.cast(trades_ptr, ctypes.POINTER(TradeRecordArray)).contents

    closed = [struct_to_dict(t) for t in trades if t.close_time > 0]
    balance_ops = [struct_to_dict(t) for t in trades if t.cmd == 6]  # OP_BALANCE

    manager.MemFree(trades_ptr)
    print(f"Positions closed: {len(closed)}, Balance ops: {len(balance_ops)}")


# ─── ReportsRequest — group summary report ──────────────────────────────────
class ReportGroupRequest(ctypes.Structure):
    _fields_ = [
        ("group",  ctypes.c_char * 16),
        ("from",   ctypes.c_int),    # start timestamp
        ("to",     ctypes.c_int),    # end timestamp
    ]

req = ReportGroupRequest()
req.group = b"real\\standard"
req.from_time = from_time
req.to_time   = to_time

total_rep = ctypes.c_int(0)
rep_ptr = manager.ReportsRequest(ctypes.byref(req), ctypes.byref(total_rep))
if rep_ptr:
    # Cast to array of DailyReport structs
    manager.MemFree(rep_ptr)
```

---

## TradeRecord Structure (Closed)

Same `TradeRecord` structure as open trades (see `03_trades_open.md`).
The key difference: **`close_time > 0`** marks a closed/historical record.

```python
# Identify closed trades
is_closed = lambda t: t["close_time"] > 0
is_balance_op = lambda t: t["cmd"] == 6   # OP_BALANCE
is_credit_op  = lambda t: t["cmd"] == 7   # OP_CREDIT
is_market_trade = lambda t: t["cmd"] in (0, 1)   # BUY or SELL
```

---

## Response Fields

Same as [03_trades_open.md](03_trades_open.md), with these fields meaningful for closed trades:

| Field | Description | Open | Closed |
|-------|-------------|------|--------|
| `order` | Ticket number | ✅ | ✅ |
| `login` | Account login | ✅ | ✅ |
| `symbol` | Symbol traded | ✅ | ✅ |
| `cmd` | Trade direction (0=BUY, 1=SELL) | ✅ | ✅ |
| `volume` | Volume in lots×100 | ✅ | ✅ |
| `open_time` | When position was opened | ✅ | ✅ |
| `open_price` | Entry price | ✅ | ✅ |
| `sl` | Stop Loss at time of close | ✅ | ✅ |
| `tp` | Take Profit at time of close | ✅ | ✅ |
| `close_time` | When position was closed (**> 0 = closed**) | `0` | `> 0` |
| `close_price` | Exit price | — | ✅ |
| `profit` | **Realized P&L** in account currency | floating | realized |
| `commission` | Commission charged | ✅ | ✅ |
| `storage` | Total swap accrued over holding period | ✅ | ✅ |
| `reason` | Why it was closed (client/stopout/SL/TP/EA) | — | ✅ |
| `taxes` | Tax amount | ✅ | ✅ |
| `magic` | EA magic number | ✅ | ✅ |
| `comment` | Order comment | ✅ | ✅ |

---

## Sample Raw Response — Closed Trade (JSON)

```json
{
  "order": 100001,
  "login": 1001,
  "symbol": "EURUSD",
  "digits": 5,
  "cmd": 0,
  "volume": 100,
  "open_time": 1711190400,
  "state": 3,
  "open_price": 1.08325,
  "sl": 1.07800,
  "tp": 1.09000,
  "close_time": 1711276800,
  "gw_volume": 0,
  "expiration": 0,
  "reason": 0,
  "conv_rates": [1.0, 1.0],
  "commission": -2.50,
  "commission_agent": 0.0,
  "storage": -1.20,
  "close_price": 1.09000,
  "profit": 675.00,
  "taxes": 0.0,
  "magic": 0,
  "comment": "",
  "gw_order": 0,
  "activation": 0,
  "gw_open_price": 0.0,
  "gw_close_price": 0.0,
  "margin_rate": 1.0,
  "timestamp": 1711276800,
  "api_data": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}
```

## Sample Raw Response — Balance Operation (JSON)

```json
{
  "order": 100010,
  "login": 1001,
  "symbol": "",
  "digits": 2,
  "cmd": 6,
  "volume": 0,
  "open_time": 1711190400,
  "state": 3,
  "open_price": 0.0,
  "sl": 0.0,
  "tp": 0.0,
  "close_time": 1711190400,
  "commission": 0.0,
  "storage": 0.0,
  "close_price": 0.0,
  "profit": 5000.00,
  "comment": "Initial deposit",
  "magic": 0,
  "taxes": 0.0
}
```

---

## P&L Calculation

```python
# Net P&L for a closed trade
net_pnl = trade["profit"] + trade["commission"] + trade["commission_agent"] + trade["storage"]

# Duration of the trade (seconds)
duration_secs = trade["close_time"] - trade["open_time"]
duration_hours = duration_secs / 3600

# Volume in standard lots
lots = trade["volume"] / 100.0
```

---

## Notes

- **MT4 has no "deals" table** — use `TradeRecord` with `close_time > 0` as the equivalent of MT5 deals.
- **OP_BALANCE (cmd=6)** entries are deposits, withdrawals, and credit adjustments. They have no symbol.
- **Profit field**: for closed trades, `profit` is the net realized P&L in account currency (excluding commission/swap).
- **`TradesUserHistory` requires a time range** — do not request unbounded history; it will be very slow.
- **Always call `MemFree`** after processing the returned pointer.
