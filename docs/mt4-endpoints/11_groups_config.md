# GroupsRequest / GroupRecordGet — Account Groups Configuration

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve account group configurations from the MT4 server.
Groups define trading conditions, leverage, spreads, and symbols for sets of accounts.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `GroupsRequest(*total)`, `GroupsGet(*total)` (pumping), `GroupRecordGet(group, *cfg)` (pumping), `CfgRequestGroups(*total)`, `CfgUpdateGroup(*cfg)` |

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login

# --- All groups (direct server request) ---
total = ctypes.c_int(0)
# ConGroup* groups = manager->GroupsRequest(&total)
# for i in range(total.value):
#     g = groups[i]
#     print(g.group.decode(), g.currency.decode(), g.leverage)
# manager->MemFree(groups)

# --- Single group by name (pumping mode) ---
cfg = ConGroup()
# manager->GroupRecordGet("real\\managers", &cfg)

# --- All groups (pumping mode) ---
total = ctypes.c_int(0)
# ConGroup* groups = manager->GroupsGet(&total)

# --- Config API (admin) ---
# ConGroup* cfg_groups = manager->CfgRequestGroups(&total)
```

## Response Fields — `ConGroup` Structure

```python
import ctypes

class ConGroupMargin(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",        ctypes.c_char * 16),  # Symbol name
        ("swap_long",     ctypes.c_double),      # Group swap long override
        ("swap_short",    ctypes.c_double),      # Group swap short override
        ("margin_divider",ctypes.c_double),      # Margin divider override
        ("commission_base",ctypes.c_double),     # Base commission
        ("commission_type",ctypes.c_int),        # Commission type
        ("commission_lots",ctypes.c_double),     # Commission per lot
        ("commission_agent",ctypes.c_double),    # Agent commission
        ("commission_agent_type",ctypes.c_int),  # Agent commission type
        ("spread_diff",   ctypes.c_int),         # Spread difference (points)
        ("lot_min",       ctypes.c_int),         # Min lot (×100)
        ("lot_max",       ctypes.c_int),         # Max lot (×100)
        ("lot_step",      ctypes.c_int),         # Lot step (×100)
        ("ie_deviation",  ctypes.c_int),         # IE deviation override
        ("confirmation",  ctypes.c_int),         # Confirmation required
        ("trade",         ctypes.c_int),         # Trade allowed
        ("execution_mode",ctypes.c_int),         # Execution mode override
        ("acc_type",      ctypes.c_int),         # Account type
        ("hedge_large_leg",ctypes.c_int),        # Hedge use larger leg
        ("reserved",      ctypes.c_int * 5),    # Reserved
    ]

class ConGroup(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("group",              ctypes.c_char * 16),         # Group name
        ("newspaper",          ctypes.c_char * 48),         # Newspaper address
        ("mail_enable",        ctypes.c_int),               # Mail enabled
        ("enable_change_password", ctypes.c_int),           # Allow password change
        ("enable_read_only",   ctypes.c_int),               # Read-only (investor)
        ("enable_send_reports",ctypes.c_int),               # Send reports
        ("report_mode",        ctypes.c_int),               # Report mode
        ("default_leverage",   ctypes.c_int),               # Default leverage
        ("default_deposit",    ctypes.c_double),            # Default deposit
        ("max_symbols",        ctypes.c_int),               # Max symbols
        ("currency",           ctypes.c_char * 16),         # Account currency
        ("price_type",         ctypes.c_int),               # Price type
        ("tax",                ctypes.c_double),            # Tax rate (%)
        ("interest_rate",      ctypes.c_double),            # Interest rate
        ("timeout",            ctypes.c_int),               # Request timeout (sec)
        ("trading",            ctypes.c_int),               # Trading enabled flag
        ("balance_min",        ctypes.c_double),            # Min balance
        ("stopping_level",     ctypes.c_int),               # Stop-out level (%)
        ("loss_limit",         ctypes.c_int),               # Loss limit
        ("margin_call",        ctypes.c_int),               # Margin call level (%)
        ("margin_mode",        ctypes.c_int),               # Margin calc mode
        ("margin_type",        ctypes.c_int),               # Margin type
        ("archive_max_balance",ctypes.c_double),            # Max balance for archive
        ("archive_pending_period", ctypes.c_int),           # Archive pending period
        ("archive_period",     ctypes.c_int),               # Archive period (days)
        ("commission_base",    ctypes.c_double),            # Base commission
        ("commission_type",    ctypes.c_int),               # Commission type
        ("commission_lots",    ctypes.c_double),            # Commission per lot
        ("commission_agent",   ctypes.c_double),            # Agent commission
        ("commission_agent_type", ctypes.c_int),            # Agent comm type
        ("free_margin_mode",   ctypes.c_int),               # Free margin calc mode
        ("transfer_mode",      ctypes.c_int),               # Transfer allowed
        ("transfer_max_money", ctypes.c_double),            # Max transfer
        ("otp_mode",           ctypes.c_int),               # One-time password mode
        ("activate",           ctypes.c_int),               # Auto-activate
        ("close_reopen",       ctypes.c_int),               # Close & reopen mode
        ("hedge_prohibited",   ctypes.c_int),               # Hedge prohibited
        ("close_fifo",         ctypes.c_int),               # FIFO closing
        ("hedge_large_leg",    ctypes.c_int),               # Hedge use larger leg
        ("reserved",           ctypes.c_int * 2),           # Reserved
        ("securities",         ConGroupMargin * 128),       # Per-symbol settings
    ]
```

## ConGroup Key Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `group` | `char[16]` | Group name | `"real\managers"` |
| `currency` | `char[16]` | Account currency | `"USD"` |
| `default_leverage` | `int` | Default leverage | `100` |
| `default_deposit` | `double` | New account default balance | `10000.0` |
| `stopping_level` | `int` | Stop-out level % | `20` |
| `margin_call` | `int` | Margin call level % | `50` |
| `trading` | `int` | Trading allowed: 1=yes, 0=no | `1` |
| `tax` | `double` | Tax rate applied to profits % | `0.0` |
| `interest_rate` | `double` | Interest on balance % | `0.0` |
| `timeout` | `int` | Trade request timeout seconds | `30` |
| `commission_base` | `double` | Base commission amount | `0.0` |
| `commission_type` | `int` | 0=disabled, 1=per lot, 2=% | `0` |
| `balance_min` | `double` | Minimum allowed balance | `0.0` |
| `hedge_prohibited` | `int` | 1=no hedging allowed | `0` |
| `close_fifo` | `int` | 1=FIFO closing required | `0` |

## ConGroupSec (Per-Symbol Security Settings) Key Fields

| Field | C Type | Description |
|-------|--------|-------------|
| `symbol` | `char[16]` | Symbol name |
| `spread_diff` | `int` | Extra spread added (points) |
| `lot_min` | `int` | Minimum lot × 100 |
| `lot_max` | `int` | Maximum lot × 100 |
| `lot_step` | `int` | Lot step × 100 |
| `commission_base` | `double` | Commission base |
| `trade` | `int` | Symbol trading allowed |
| `execution_mode` | `int` | Execution mode override |

## Related Functions

| Function | Description |
|----------|-------------|
| `GroupsRequest(*total)` | All groups direct from server |
| `GroupsGet(*total)` | All groups in pumping mode |
| `GroupRecordGet(group, *cfg)` | Single group in pumping mode |
| `CfgRequestGroups(*total)` | Admin: request group configs |
| `CfgUpdateGroup(*cfg)` | **WRITE ADMIN** — Update group config |
| `CfgDeleteGroup(index)` | **WRITE ADMIN** — Delete group |
