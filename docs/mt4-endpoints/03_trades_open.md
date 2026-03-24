# Open Trades / Orders

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Trading / Orders](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_trade/manager_api_trade_order)

---

## Overview

Open trades (positions) in MT4 are `TradeRecord` structs where `close_time == 0`.
These include all market orders that have not yet been closed, as well as pending orders.

In MT4 terminology, an **order** and an **open position** are the same thing — both are `TradeRecord`
entries with `close_time = 0`.

---

## Methods

| Method | Purpose | When to Use |
|--------|---------|-------------|
| `TradesRequest` | Get ALL open orders (all accounts) | Bootstrap full sync |
| `TradeRecordsRequest` | Get orders by ticket list | Targeted fetch |
| `AdmTradesRequest` | Admin: get orders by group/account/ticket | Full re-sync by group |
| `TradesGetByLogin` | Get orders for one account (pumping) | Real-time per account |
| `TradesGetBySymbol` | Get orders for one symbol (pumping) | Real-time per symbol |
| `TradesGet` | Get all open orders (pumping) | Real-time full snapshot |
| `TradeRecordGet` | Get single order by ticket (pumping) | Single order lookup |

---

## Example Code

```python
import ctypes

# ─── TradesRequest — all open orders ────────────────────────────────────────
total = ctypes.c_int(0)
trades_ptr = manager.TradesRequest(ctypes.byref(total))

if not trades_ptr:
    print("TradesRequest failed")
else:
    print(f"Open orders: {total.value}")

    TradeRecordArray = TradeRecord * total.value
    trades = ctypes.cast(trades_ptr, ctypes.POINTER(TradeRecordArray)).contents

    records = [struct_to_dict(t) for t in trades]
    manager.MemFree(trades_ptr)

    # Filter: only open positions (close_time == 0, cmd in BUY/SELL range)
    open_positions = [r for r in records if r["close_time"] == 0 and r["cmd"] < 2]
    pending_orders = [r for r in records if r["close_time"] == 0 and r["cmd"] >= 2]

    print(f"Open positions: {len(open_positions)}")
    print(f"Pending orders: {len(pending_orders)}")


# ─── TradeRecordsRequest — by ticket list ───────────────────────────────────
tickets = (ctypes.c_int * 3)(100001, 100002, 100003)
total2 = ctypes.c_int(0)
trades_ptr2 = manager.TradeRecordsRequest(tickets, 3, ctypes.byref(total2))
# ... same pattern


# ─── AdmTradesRequest — admin, by group ─────────────────────────────────────
total3 = ctypes.c_int(0)
trades_ptr3 = manager.AdmTradesRequest(b"real\\standard", ctypes.byref(total3))
# request string: comma-separated groups, logins, or tickets
# ... same pattern
```

---

## TradeRecord Structure

The core MT4 trading record. Used for BOTH open positions AND trade history.
Differentiate by `close_time`: `0` = open/pending, `> 0` = closed.

```python
class TradeRecord(ctypes.Structure):
    _fields_ = [
        ("order",          ctypes.c_int),          # ticket number
        ("login",          ctypes.c_int),          # account login
        ("symbol",         ctypes.c_char * 12),    # trading symbol
        ("digits",         ctypes.c_int),          # price decimal digits
        ("cmd",            ctypes.c_int),          # trade command (see enum below)
        ("volume",         ctypes.c_int),          # volume in lots * 100
        ("open_time",      ctypes.c_int),          # open timestamp (time_t)
        ("state",          ctypes.c_int),          # order state
        ("open_price",     ctypes.c_double),       # open price
        ("sl",             ctypes.c_double),       # stop loss
        ("tp",             ctypes.c_double),       # take profit
        ("close_time",     ctypes.c_int),          # close timestamp (0=open)
        ("gw_volume",      ctypes.c_int),          # gateway volume
        ("expiration",     ctypes.c_int),          # pending order expiry (time_t)
        ("reason",         ctypes.c_short),        # close reason
        ("conv_reserv",    ctypes.c_short * 2),    # reserved
        ("conv_rates",     ctypes.c_double * 2),   # conversion rates
        ("commission",     ctypes.c_double),       # commission charged
        ("commission_agent", ctypes.c_double),     # agent commission
        ("storage",        ctypes.c_double),       # overnight swap
        ("close_price",    ctypes.c_double),       # close/current price
        ("profit",         ctypes.c_double),       # floating or realized P&L
        ("taxes",          ctypes.c_double),       # tax amount
        ("magic",          ctypes.c_int),          # EA magic number
        ("comment",        ctypes.c_char * 32),    # order comment
        ("gw_order",       ctypes.c_int),          # gateway order ID
        ("activation",     ctypes.c_int),          # activation flag
        ("gw_open_price",  ctypes.c_double),       # gateway open price
        ("gw_close_price", ctypes.c_double),       # gateway close price
        ("margin_rate",    ctypes.c_double),       # margin conversion rate
        ("timestamp",      ctypes.c_int),          # last modification time
        ("api_data",       ctypes.c_uint8 * 16),   # plugin data
    ]
```

---

## Response Fields

| Field | C++ Type | ctypes | Description | Example |
|-------|----------|--------|-------------|---------|
| `order` | `int` | `c_int` | **Ticket number** — unique order ID | `100001` |
| `login` | `int` | `c_int` | Account login that owns this order | `1001` |
| `symbol` | `char[12]` | `c_char*12` | Trading symbol | `"EURUSD"` |
| `digits` | `int` | `c_int` | Price decimal digits for this symbol | `5` |
| `cmd` | `int` | `c_int` | **Trade command** (see enum below) | `0` (BUY) |
| `volume` | `int` | `c_int` | Volume in lots × 100 (so 1.00 lot = 100) | `100` |
| `open_time` | `int` (time_t) | `c_int` | Order open timestamp (UTC) | `1711190400` |
| `state` | `int` | `c_int` | Order state (see enum below) | `0` |
| `open_price` | `double` | `c_double` | Price at which order was opened | `1.08325` |
| `sl` | `double` | `c_double` | Stop Loss level (0 = none) | `1.07800` |
| `tp` | `double` | `c_double` | Take Profit level (0 = none) | `1.09000` |
| `close_time` | `int` (time_t) | `c_int` | Close timestamp (**0 = still open**) | `0` |
| `gw_volume` | `int` | `c_int` | Gateway/LP order volume | `0` |
| `expiration` | `int` (time_t) | `c_int` | Pending order expiry time (0 = GTC) | `0` |
| `reason` | `short` | `c_short` | Close reason code | `0` |
| `conv_rates[2]` | `double[2]` | `c_double*2` | Currency conversion rates | `[1.0, 1.0]` |
| `commission` | `double` | `c_double` | Commission charged | `-2.50` |
| `commission_agent` | `double` | `c_double` | Agent/IB commission | `0.0` |
| `storage` | `double` | `c_double` | Cumulative overnight swap | `-1.20` |
| `close_price` | `double` | `c_double` | Current market price (for open) | `1.08412` |
| `profit` | `double` | `c_double` | Floating P&L (open) or realized P&L (closed) | `87.00` |
| `taxes` | `double` | `c_double` | Taxes amount | `0.0` |
| `magic` | `int` | `c_int` | EA magic number (0 = manual) | `0` |
| `comment` | `char[32]` | `c_char*32` | Order comment | `"scalp"` |
| `gw_order` | `int` | `c_int` | Gateway order reference | `0` |
| `activation` | `int` | `c_int` | Activation state | `0` |
| `gw_open_price` | `double` | `c_double` | Gateway open price | `0.0` |
| `gw_close_price` | `double` | `c_double` | Gateway close price | `0.0` |
| `margin_rate` | `double` | `c_double` | Margin conversion rate | `1.0` |
| `timestamp` | `int` | `c_int` | Last modification time | `1711190400` |
| `api_data` | `BYTE[16]` | `c_uint8*16` | Plugin reserved data | `[0,...]` |

---

## Enumerations

### `cmd` — Trade Command

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `OP_BUY` | Buy (market) |
| `1` | `OP_SELL` | Sell (market) |
| `2` | `OP_BUY_LIMIT` | Buy Limit (pending) |
| `3` | `OP_SELL_LIMIT` | Sell Limit (pending) |
| `4` | `OP_BUY_STOP` | Buy Stop (pending) |
| `5` | `OP_SELL_STOP` | Sell Stop (pending) |
| `6` | `OP_BALANCE` | Balance operation |
| `7` | `OP_CREDIT` | Credit operation |

### `state` — Order State

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `TS_OPEN_NORMAL` | Open, normal state |
| `1` | `TS_OPEN_REMAND` | Open, on remand (requote pending) |
| `2` | `TS_OPEN_RESTORED` | Open, restored from backup |
| `3` | `TS_CLOSED_NORMAL` | Closed normally |
| `4` | `TS_CLOSED_PART` | Partially closed |
| `5` | `TS_CLOSED_BY` | Closed by opposite position |
| `6` | `TS_DELETED` | Deleted (pending expired/cancelled) |

### `reason` — Close Reason

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `TR_REASON_CLIENT` | Closed by client |
| `1` | `TR_REASON_EXPERT` | Closed by Expert Advisor |
| `2` | `TR_REASON_DEALER` | Closed by dealer |
| `3` | `TR_REASON_STOPOUT` | Closed by stop-out |
| `4` | `TR_REASON_ROLLOVER` | Closed by rollover |
| `5` | `TR_REASON_VMARGIN` | Closed by variation margin |
| `6` | `TR_REASON_GATEWAY` | Closed by gateway (STP) |
| `7` | `TR_REASON_SIGNAL` | Closed by signal service |

---

## Volume Conversion

MT4 stores volume as `int` (lots × 100). To get standard lots:

```python
lots = trade.volume / 100.0   # e.g. volume=100 → 1.00 lot
```

---

## Sample Raw Response (JSON)

```json
{
  "order": 100001,
  "login": 1001,
  "symbol": "EURUSD",
  "digits": 5,
  "cmd": 0,
  "volume": 100,
  "open_time": 1711190400,
  "state": 0,
  "open_price": 1.08325,
  "sl": 1.07800,
  "tp": 1.09000,
  "close_time": 0,
  "gw_volume": 0,
  "expiration": 0,
  "reason": 0,
  "conv_rates": [1.0, 1.0],
  "commission": -2.50,
  "commission_agent": 0.0,
  "storage": -1.20,
  "close_price": 1.08412,
  "profit": 87.00,
  "taxes": 0.0,
  "magic": 0,
  "comment": "",
  "gw_order": 0,
  "activation": 0,
  "gw_open_price": 0.0,
  "gw_close_price": 0.0,
  "margin_rate": 1.0,
  "timestamp": 1711190400,
  "api_data": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
}
```

---

## Notes

- **Memory management**: Always call `manager.MemFree(ptr)` after processing.
- **Volume**: stored as `int` (lots × 100). Convert: `lots = volume / 100.0`.
- **Open vs closed**: filter by `close_time == 0` for open positions.
- **Balance ops**: `cmd == 6` (OP_BALANCE) entries are balance/credit adjustments, not actual trades.
- **Pending orders**: `cmd` in `[2, 3, 4, 5]` are pending orders (not yet filled).
