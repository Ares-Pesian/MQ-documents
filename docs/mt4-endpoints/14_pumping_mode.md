# PumpingSwitch / PumpingSwitchEx — Real-Time Data Stream Mode

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Pumping mode is a **push-based subscription model** where the server sends updates
whenever data changes (users, trades, quotes, online status, etc.).
It is the most efficient way to monitor a live trading server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `PumpingSwitch(callback, param)`, `PumpingSwitchEx(callback, param)` |

## Example Code — Basic Pumping

```python
import ctypes, time

dll = ctypes.WinDLL("mtmanapi64.dll")

# Define callback function type
PUMP_FUNC = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_int,
                                ctypes.c_void_p, ctypes.c_void_p)

def on_pump_event(code, type_, data, param):
    """Called by MT4 server when data changes."""
    if code == 0x01:    # PUMP_START_PUMPING
        print("Pumping started - initial data ready")
    elif code == 0x04:  # PUMP_UPDATE_USERS
        print("User accounts updated")
    elif code == 0x05:  # PUMP_UPDATE_ONLINE
        print("Online list updated")
    elif code == 0x06:  # PUMP_UPDATE_BIDASK
        print("Quotes updated")
    elif code == 0x0A:  # PUMP_UPDATE_TRADES
        print("Trades updated")
    elif code == 0x0E:  # PUMP_UPDATE_MARGINCALL
        print("Margin call status changed")
    elif code == 0x0F:  # PUMP_STOP_PUMPING
        print("Pumping stopped")

pump_cb = PUMP_FUNC(on_pump_event)

# Start pumping
# manager->PumpingSwitch(pump_cb, 0)

# After PUMP_START_PUMPING received, query data:
# - Users:   manager->UsersGet(&total)
# - Trades:  manager->TradesGet(&total)
# - Online:  manager->OnlineGet(&total)
# - Quotes:  manager->SymbolInfoUpdated(&total)
# - Margins: manager->MarginsGet(None, 0, &total)
```

## Example Code — Extended Pumping (PumpingSwitchEx)

```python
import ctypes

# Extended pumping provides per-transaction detail
PUMP_EX_FUNC = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_int,
                                   ctypes.c_void_p, ctypes.c_void_p)

TRANS_ADD      = 1  # New record added
TRANS_DELETE   = 2  # Record deleted
TRANS_UPDATE   = 3  # Record updated
TRANS_CHANGE_GRP = 4  # Group changed

def on_pump_ex_event(code, trans_type, data, param):
    """
    code:       Pump event code (PUMP_UPDATE_* constant)
    trans_type: TRANS_ADD / TRANS_DELETE / TRANS_UPDATE / TRANS_CHANGE_GRP
    data:       Pointer to changed data structure (cast based on code)
    param:      Custom parameter passed to PumpingSwitchEx
    """
    if code == 0x04:  # PUMP_UPDATE_USERS
        # data points to UserRecord
        user = ctypes.cast(data, ctypes.POINTER(UserRecord)).contents
        print(f"User {user.login}: balance={user.balance}")

    elif code == 0x0A:  # PUMP_UPDATE_TRADES
        # data points to TradeRecord
        trade = ctypes.cast(data, ctypes.POINTER(TradeRecord)).contents
        print(f"Trade {trade.order}: symbol={trade.symbol.decode()}, profit={trade.profit}")

    elif code == 0x02:  # PUMP_UPDATE_SYMBOLS
        # data points to ConSymbol
        sym = ctypes.cast(data, ctypes.POINTER(ConSymbol)).contents
        print(f"Symbol {sym.symbol.decode()} updated")

pump_ex_cb = PUMP_EX_FUNC(on_pump_ex_event)
# manager->PumpingSwitchEx(pump_ex_cb, 0)
```

## Pumping Event Codes

| Code | Hex | Constant | Data Pointer Type | Action |
|------|-----|----------|-------------------|--------|
| `1` | `0x01` | `PUMP_START_PUMPING` | None | Initial sync done; call Get* methods |
| `2` | `0x02` | `PUMP_UPDATE_SYMBOLS` | `ConSymbol*` | `SymbolsGetAll()` / `SymbolGet()` |
| `3` | `0x03` | `PUMP_UPDATE_GROUPS` | `ConGroup*` | `GroupsGet()` / `GroupRecordGet()` |
| `4` | `0x04` | `PUMP_UPDATE_USERS` | `UserRecord*` | `UsersGet()` / `UserRecordGet()` |
| `5` | `0x05` | `PUMP_UPDATE_ONLINE` | `int*` (login) | `OnlineGet()` / `OnlineRecordGet()` |
| `6` | `0x06` | `PUMP_UPDATE_BIDASK` | `SymbolInfo*` | `SymbolInfoUpdated()` / `TickInfoLast()` |
| `7` | `0x07` | `PUMP_UPDATE_NEWS` | `NewsTopic*` | `NewsGet()` / `NewsTopicGet()` |
| `8` | `0x08` | `PUMP_UPDATE_NEWS_BODY` | `UINT*` (key) | `NewsBodyGet(key)` |
| `9` | `0x09` | `PUMP_UPDATE_MAIL` | `MailBoxHeader*` | `MailLast()` |
| `10` | `0x0A` | `PUMP_UPDATE_TRADES` | `TradeRecord*` | `TradesGet()` / `TradeRecordGet()` |
| `11` | `0x0B` | `PUMP_UPDATE_REQUESTS` | `RequestInfo*` | `RequestsGet()` / `RequestInfoGet()` |
| `12` | `0x0C` | `PUMP_UPDATE_PLUGINS` | None | Plugin settings changed |
| `13` | `0x0D` | `PUMP_UPDATE_ACTIVATION` | `TradeRecord*` | `TradesGet()` with activation flag |
| `14` | `0x0E` | `PUMP_UPDATE_MARGINCALL` | `MarginLevel*` | `MarginsGet()` / `MarginLevelGet()` |
| `15` | `0x0F` | `PUMP_STOP_PUMPING` | None | Pumping stopped; call PumpingSwitch again |
| `16` | `0x10` | `PUMP_UPDATE_NEWS_NEW` | `NewsTopicNew*` | New-format newsletter |

## Trans Type Values (PumpingSwitchEx only)

| Value | Constant | Meaning |
|-------|----------|---------|
| `1` | `TRANS_ADD` | New record added to server |
| `2` | `TRANS_DELETE` | Record deleted from server |
| `3` | `TRANS_UPDATE` | Record data updated |
| `4` | `TRANS_CHANGE_GRP` | Record moved to different group |

## Data Access After Each Pump Event

| Event | Functions to Call |
|-------|------------------|
| `PUMP_START_PUMPING` | `UsersGet`, `TradesGet`, `OnlineGet`, `SummaryGetAll`, `SymbolInfoUpdated`, `MarginsGet`, `GroupsGet`, `SymbolsGetAll` |
| `PUMP_UPDATE_USERS` | `UserRecordGet(login)` |
| `PUMP_UPDATE_TRADES` | `TradeRecordGet(order)`, `SummaryGetAll()`, `ExposureGet()` |
| `PUMP_UPDATE_BIDASK` | `TickInfoLast(symbol, N)`, `SymbolInfoUpdated()` |
| `PUMP_UPDATE_MARGINCALL` | `MarginLevelGet(login)`, `MarginsGet(logins, count)` |
| `PUMP_UPDATE_ONLINE` | `OnlineRecordGet(login)` |
| `PUMP_UPDATE_REQUESTS` | `RequestsGet()`, `RequestInfoGet(index)` |
