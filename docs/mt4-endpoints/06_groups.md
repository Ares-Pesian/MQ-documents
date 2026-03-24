# Groups / Configuration

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Configuration Databases](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_config)

---

## Overview

Groups in MT4 are the primary way accounts are segmented for trading conditions.
Every account belongs to one group. Groups define: execution mode, margin settings,
symbol-specific commissions, allowed symbols, leverage, and more.

The `CfgRequest*` and `GroupsRequest` methods require **Administrator rights** on the manager account.

---

## Methods

| Method | Purpose |
|--------|---------|
| `GroupsRequest` | Get all groups from server database (direct mode) |
| `GroupsGet` | Get all groups from local cache (pumping mode) |
| `GroupRecordGet` | Get single group by name (pumping mode) |
| `CfgRequestGroup` | Admin: get full `ConGroup` config for a group |
| `CfgUpdateGroup` | Admin: update group configuration |
| `CfgDeleteGroup` | Admin: delete a group |

---

## Example Code

```python
import ctypes

# ─── GroupsRequest — all groups (direct mode) ────────────────────────────────
total = ctypes.c_int(0)
groups_ptr = manager.GroupsRequest(ctypes.byref(total))

if groups_ptr:
    print(f"Groups: {total.value}")
    ConGroupArray = ConGroup * total.value
    groups = ctypes.cast(groups_ptr, ctypes.POINTER(ConGroupArray)).contents
    records = [struct_to_dict(g) for g in groups]
    manager.MemFree(groups_ptr)
    print(records[0]["group"], records[0]["currency"], records[0]["leverage"])
```

---

## ConGroup Structure — Key Fields

| Field | C++ Type | ctypes | Description | Example |
|-------|----------|--------|-------------|---------|
| `group` | `char[16]` | `c_char*16` | Group name | `"real\\standard"` |
| `enable` | `int` | `c_int` | Group enabled: 1=yes | `1` |
| `timeout` | `int` | `c_int` | Requote timeout (seconds) | `10` |
| `adm_rights` | `int` | `c_int` | Admin rights for group | `0` |
| `check_ie_prices` | `int` | `c_int` | Check prices on IE mode | `1` |
| `max_positions` | `int` | `c_int` | Max open positions per account | `200` |
| `close_reopen` | `int` | `c_int` | Close and reopen on partial close | `1` |
| `hedge_prohibited` | `int` | `c_int` | Hedging prohibited: 1=yes | `0` |
| `close_fifo` | `int` | `c_int` | FIFO close rule | `0` |
| `currency` | `char[16]` | `c_char*16` | Account base currency | `"USD"` |
| `credit` | `double` | `c_double` | Default credit | `0.0` |
| `leverage` | `int` | `c_int` | Default leverage for group | `100` |
| `ie_deviation` | `int` | `c_int` | IE price deviation (points) | `10` |
| `margin_call` | `int` | `c_int` | Margin call level % | `100` |
| `margin_mode` | `int` | `c_int` | Margin calculation mode | `0` |
| `margin_stopout` | `int` | `c_int` | Stop-out level % | `50` |
| `interest_rate` | `double` | `c_double` | Annual interest rate | `0.0` |
| `use_swap` | `int` | `c_int` | Swap enabled: 1=yes | `1` |
| `news` | `int` | `c_int` | News mode | `1` |
| `rights` | `int` | `c_int` | Group rights bitmask | `255` |
| `check_stopout_level` | `int` | `c_int` | Stop-out check mode | `0` |
| `report_mode` | `int` | `c_int` | Email report mode | `1` |
| `report_hours` | `int` | `c_int` | Report hour | `23` |
| `report_mins` | `int` | `c_int` | Report minute | `59` |
| `copies` | `int` | `c_int` | Max copies of this group | `10000` |
| `apidata` | `BYTE[16]` | `c_uint8*16` | Plugin data | `[0,...]` |
| `secs` | `ConGroupSec[...]` | struct array | Per-symbol settings | *see below* |
| `secmargins` | `ConGroupMargin[...]` | struct array | Per-symbol margin/swap | *see below* |

---

## ConGroupSec — Per-Symbol Group Settings

| Field | C++ Type | Description |
|-------|----------|-------------|
| `show` | `int` | Symbol visible to group: 1=yes |
| `trade` | `int` | Trading allowed: 0=none, 1=close, 2=full |
| `execution` | `int` | Execution mode override |
| `comm_base` | `double` | Base commission |
| `comm_type` | `int` | Commission type |
| `comm_lots` | `double` | Commission per lot |
| `comm_agent` | `double` | Agent commission |
| `comm_agent_type` | `int` | Agent commission type |
| `spread_diff` | `int` | Spread markup in points |
| `lot_min` | `int` | Min volume (lots×100) |
| `lot_max` | `int` | Max volume (lots×100) |
| `lot_step` | `int` | Volume step (lots×100) |
| `ie_check_mode` | `int` | Instant execution check mode |
| `confirmation` | `int` | Confirmation required |

---

## Sample Raw Response — ConGroup (JSON)

```json
{
  "group": "real\\standard",
  "enable": 1,
  "timeout": 10,
  "adm_rights": 0,
  "check_ie_prices": 1,
  "max_positions": 200,
  "close_reopen": 1,
  "hedge_prohibited": 0,
  "close_fifo": 0,
  "currency": "USD",
  "credit": 0.0,
  "leverage": 100,
  "ie_deviation": 10,
  "margin_call": 100,
  "margin_mode": 0,
  "margin_stopout": 50,
  "interest_rate": 0.0,
  "use_swap": 1,
  "news": 1,
  "rights": 255,
  "check_stopout_level": 0,
  "report_mode": 1,
  "report_hours": 23,
  "report_mins": 59,
  "copies": 10000
}
```

---

## Notes

- `CfgRequest*` methods require `ConManager::admin == 1` on the manager account.
- Group names follow a `parent\\child` naming convention (e.g. `real\\standard`).
- The `rights` bitmask controls what clients in this group can do (trade, withdraw, etc.).
