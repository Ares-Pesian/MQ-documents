# Connect / Login — Establish Manager Session

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Connect and authenticate a manager session to the MT4 trade server.
Must be called before any other API method.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` (32-bit) or `mtmanapi64.dll` (64-bit) |
| **Method** | `manager->Connect(server)` then `manager->Login(login, password)` |
| **Auth** | Manager group account (login + password) |

## Example Code

```python
import ctypes, os

# Load DLL (place mtmanapi64.dll in same directory or PATH)
dll = ctypes.WinDLL("mtmanapi64.dll")
dll.MtManCreate.restype  = ctypes.c_void_p
dll.MtManCreate.argtypes = [ctypes.c_uint]

mgr = dll.MtManCreate(0x0001)  # AUTO_RELEASE_VERSION

# The manager interface uses a COM-style vtable.
# Vtable index 3 = Connect, index 4 = Login, etc.
# Use CManagerFactory from MT4ManagerAPI.h for clean access.

# With the official C++ header pattern:
# manager->Connect("88.218.200.140:443")
# int ret = manager->Login(52, "Vista1234$")
# if (ret != RET_OK): handle error

# Disconnect when done:
# manager->Disconnect()
# manager->Release()  # decrements COM ref count, frees memory
```

## Response Fields — `ManagerRights` Structure

After login, call `manager->ManagerRights()` to get manager permissions.

| Field | C Type | Python ctypes | Description |
|-------|--------|---------------|-------------|
| `login` | `int` | `c_int` | Manager login number |
| `name` | `char[32]` | `c_char * 32` | Manager name |
| `email` | `char[48]` | `c_char * 48` | Manager email |
| `rights` | `UINT` | `c_uint` | Permission bitmask |
| `ip_filter` | `char[256]` | `c_char * 256` | Allowed IP filter |
| `groups` | `char[1024]` | `c_char * 1024` | Accessible groups |

### Rights Bitmask Values

| Constant | Value | Description |
|----------|-------|-------------|
| `MANAGER_RIGHT_NORESTRICTIONS` | `0x0001` | No restrictions |
| `MANAGER_RIGHT_ENABLED` | `0x0002` | Manager enabled |
| `MANAGER_RIGHT_MANAGER` | `0x0004` | Full manager rights |
| `MANAGER_RIGHT_MONEY` | `0x0008` | Money operations allowed |
| `MANAGER_RIGHT_ONLINE` | `0x0010` | View online clients |
| `MANAGER_RIGHT_RISKMAN` | `0x0020` | Risk management |
| `MANAGER_RIGHT_BROKER` | `0x0040` | Broker functions |
| `MANAGER_RIGHT_ADMIN` | `0x0080` | Administrator rights |
| `MANAGER_RIGHT_LOGS` | `0x0100` | View logs |
| `MANAGER_RIGHT_REPORTS` | `0x0200` | View reports |
| `MANAGER_RIGHT_TRADES` | `0x0400` | Manage trades |
| `MANAGER_RIGHT_MARKET_WATCH` | `0x0800` | Market watch access |
| `MANAGER_RIGHT_EMAIL` | `0x1000` | Send emails |
| `MANAGER_RIGHT_PUSHES` | `0x2000` | Send push notifications |
| `MANAGER_RIGHT_EXPERTS` | `0x4000` | Manage experts |
| `MANAGER_RIGHT_TECHNICAL` | `0x8000` | Technical access |

## Return Codes

| Code | Value | Meaning |
|------|-------|---------|
| `RET_OK` | `0` | Success |
| `RET_ERROR` | `1` | General error |
| `RET_INVALID_DATA` | `2` | Invalid parameters |
| `RET_TECH_PROBLEM` | `3` | Technical problem |
| `RET_OLD_VERSION` | `4` | Old DLL version |
| `RET_NO_MEMORY` | `5` | Out of memory |
| `RET_WRONG_PASSWORD` | `6` | Wrong password |
| `RET_TOO_MANY_CONNECTIONS` | `7` | Too many connections |
| `RET_ACCOUNT_DISABLED` | `8` | Account disabled |
| `RET_BAD_ACCOUNT_INFO` | `9` | Bad account info |
| `RET_TRADESERVER_BUSY` | `10` | Server busy |
| `RET_OLDVERSION` | `11` | Old server version |
| `RET_NO_CONNECTION` | `12` | No connection |
| `RET_NOT_ENOUGH_RIGHTS` | `13` | Insufficient rights |
