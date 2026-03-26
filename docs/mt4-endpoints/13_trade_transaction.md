# TradeTransaction — Execute Trade Operations (WRITE)

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Execute trade operations: open/close positions, place/cancel pending orders,
modify SL/TP, perform balance/credit operations.
`TradeTransaction` is the main WRITE endpoint for all trading actions.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Method** | `TradeTransaction(*trans, *trans_result, *result_count)` |
| **Mode** | Can be used in any mode (no pumping required) |

> **WRITE OPERATION** — these calls modify live account data.

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login

# --- Balance deposit ---
trans = TradeTransInfo()
trans.type       = TT_BR_BALANCE     # Balance operation
trans.cmd        = OP_BALANCE        # Balance (6)
trans.login      = 52
trans.price      = 100.0             # Amount to deposit
trans.comment[0:14] = b"API deposit\x00"

result_count = ctypes.c_int(0)
# int ret = manager->TradeTransaction(&trans, None, &result_count)
# if ret == RET_OK: print("Balance deposited")

# --- Open market buy ---
trans = TradeTransInfo()
trans.type       = TT_ORDER_MK_OPEN  # Market open
trans.cmd        = OP_BUY
trans.login      = 52
trans.symbol[0:6] = b"EURUSD"
trans.volume     = 100               # 1.00 lot = 100
trans.price      = 0.0               # 0 = current market price
trans.sl         = 1.08000
trans.tp         = 1.09000

# int ret = manager->TradeTransaction(&trans, None, &result_count)

# --- Close position ---
trans = TradeTransInfo()
trans.type    = TT_ORDER_CLOSE
trans.order   = 123456               # Position ticket to close
trans.price   = 0.0                  # 0 = current market price
trans.volume  = 100                  # volume to close

# int ret = manager->TradeTransaction(&trans, None, &result_count)

# --- Place pending order ---
trans = TradeTransInfo()
trans.type    = TT_ORDER_IE_OPEN
trans.cmd     = OP_BUY_LIMIT
trans.login   = 52
trans.symbol[0:6] = b"EURUSD"
trans.volume  = 100
trans.price   = 1.08000              # Limit price
trans.sl      = 1.07500
trans.tp      = 1.08500
trans.expiration = 0                 # 0 = GTC

# --- Modify SL/TP ---
trans = TradeTransInfo()
trans.type    = TT_ORDER_MODIFY
trans.order   = 123456
trans.sl      = 1.08100
trans.tp      = 1.09100
```

## `TradeTransInfo` Structure

```python
import ctypes

class TradeTransInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("type",       ctypes.c_int),        # Transaction type (TT_*)
        ("flags",      ctypes.c_int),        # Transaction flags
        ("cmd",        ctypes.c_int),        # Order type (OP_*)
        ("order",      ctypes.c_int),        # Order ticket (for modify/close)
        ("orderby",    ctypes.c_int),        # Closed-by order ticket
        ("login",      ctypes.c_int),        # Account login
        ("symbol",     ctypes.c_char * 12),  # Symbol
        ("volume",     ctypes.c_int),        # Volume × 100
        ("price",      ctypes.c_double),     # Price (or amount for balance)
        ("sl",         ctypes.c_double),     # Stop loss
        ("tp",         ctypes.c_double),     # Take profit
        ("ie_deviation",ctypes.c_int),       # IE deviation points
        ("comment",    ctypes.c_char * 32),  # Order comment
        ("expiration", ctypes.c_int),        # Expiry (Unix ts, 0=GTC)
        ("magic",      ctypes.c_int),        # EA magic number
        ("reserved",   ctypes.c_int * 2),   # Reserved
    ]
```

## TradeTransInfo Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `type` | `int` | Transaction type (TT_* constant) | `64` (TT_ORDER_MK_OPEN) |
| `flags` | `int` | Transaction flags | `0` |
| `cmd` | `int` | Order type (OP_* constant) | `0` (OP_BUY) |
| `order` | `int` | Ticket for modify/close operations | `123456` |
| `orderby` | `int` | Close-by opposite position ticket | `0` |
| `login` | `int` | Account login | `52` |
| `symbol` | `char[12]` | Trading symbol | `"EURUSD"` |
| `volume` | `int` | Volume × 100 (1 lot = 100) | `100` |
| `price` | `double` | Price or balance amount | `1.08500` |
| `sl` | `double` | Stop loss price | `1.08000` |
| `tp` | `double` | Take profit price | `1.09000` |
| `ie_deviation` | `int` | IE deviation in points | `10` |
| `comment` | `char[32]` | Order comment | `"API trade"` |
| `expiration` | `int` | Pending order expiry (0=GTC) | `0` |
| `magic` | `int` | Expert Advisor magic number | `0` |

## Transaction Type (`type`) Values

| Value | Constant | Description |
|-------|----------|-------------|
| `64` | `TT_ORDER_MK_OPEN` | Open market order |
| `65` | `TT_ORDER_MK_CLOSE` | Close market order |
| `68` | `TT_ORDER_CLOSE` | Close position |
| `69` | `TT_ORDER_DELETE` | Delete pending order |
| `70` | `TT_ORDER_MODIFY` | Modify SL/TP/price |
| `71` | `TT_ORDER_ACTIVATE` | Activate stop/pending |
| `72` | `TT_ORDER_IE_OPEN` | Open with IE (instant) |
| `73` | `TT_ORDER_IE_CLOSE` | Close with IE |
| `74` | `TT_ORDER_REQ_OPEN` | Open by request |
| `75` | `TT_ORDER_REQ_CLOSE` | Close by request |
| `128` | `TT_BR_BALANCE` | Balance operation |
| `129` | `TT_BR_CREDIT` | Credit operation |
| `130` | `TT_BR_CHARGE` | Charge fee |
| `131` | `TT_BR_CORRECTION` | Balance correction |
| `132` | `TT_BR_BONUS` | Add bonus |
| `133` | `TT_BR_COMMENT` | Add comment |
| `134` | `TT_BR_DIVIDEND` | Dividend |
| `135` | `TT_BR_DIVIDEND_FRANKED` | Franked dividend |
| `136` | `TT_BR_TAX` | Tax deduction |
