# Connection & Authentication

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API Docs](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_connect)

---

## Overview

The MT4 Manager API connection lifecycle has three steps:
1. **Load DLL** — `ctypes.WinDLL("mtmanapi.dll")`
2. **Connect** — TCP socket to `server:port`
3. **Login** — Authenticate with manager credentials

After login, you can call all data-fetch methods. Use `Ping` to keep the connection alive.

---

## Methods

| Method | Signature | Returns | Purpose |
|--------|-----------|---------|---------|
| `Connect` | `Connect(server: str) -> int` | Return code | TCP connect to server:port |
| `Disconnect` | `Disconnect() -> void` | — | Close connection |
| `IsConnected` | `IsConnected() -> int` | 0/1 | Check connection state |
| `Login` | `Login(login: int, password: str) -> int` | Return code | Authenticate |
| `Ping` | `Ping() -> int` | Return code | Keep-alive / test connection |
| `ManagerRights` | `ManagerRights(rights: ConManager*) -> int` | Return code | Get manager permissions |
| `PasswordChange` | `PasswordChange(password: str, is_investor: int) -> int` | Return code | Change manager password |

---

## Example Code

```python
import ctypes
import json
import datetime

# ─── Load DLL ───────────────────────────────────────────────────────────────
# IMPORTANT: Run on Windows only. DLL path from broker / AWS Secrets Manager.
lib = ctypes.WinDLL(r"C:\MT4\API\mtmanapi.dll")

# Factory function
MtManCreate = lib.MtManCreate
MtManCreate.restype  = ctypes.c_void_p
MtManCreate.argtypes = [ctypes.c_int]

manager = MtManCreate(1)
if not manager:
    raise RuntimeError("MtManCreate returned NULL — check DLL path and version")

# Cast to CManagerInterface
from ctypes import cast, POINTER
# In practice you call methods via interface vtable. See structs.py for full wrapper.

# ─── Connect ────────────────────────────────────────────────────────────────
SERVER   = "88.218.200.140:443"
LOGIN    = 52
PASSWORD = "Vista1234$"

# Connect (returns 0 on success)
ret = manager.Connect(SERVER.encode())
print(f"Connect: {ret}")   # 0 = RET_OK

# ─── Login ──────────────────────────────────────────────────────────────────
ret = manager.Login(LOGIN, PASSWORD.encode())
print(f"Login: {ret}")     # 0 = RET_OK

# ─── Ping ───────────────────────────────────────────────────────────────────
ret = manager.Ping()
print(f"Ping: {ret}")      # 0 = RET_OK

# ─── IsConnected ────────────────────────────────────────────────────────────
connected = manager.IsConnected()
print(f"IsConnected: {connected}")  # 1 = connected

# ─── ManagerRights ──────────────────────────────────────────────────────────
# Returns ConManager struct with permissions bitmask
# See 06_groups.md for ConManager structure definition

# ─── Disconnect ─────────────────────────────────────────────────────────────
manager.Disconnect()
manager.Release()
```

---

## Response: ManagerRights (ConManager struct)

`ManagerRights()` fills a `ConManager` structure describing what this manager account can do.

| Field | C++ Type | ctypes | Description |
|-------|----------|--------|-------------|
| `login` | `int` | `c_int` | Manager account login |
| `name` | `char[32]` | `c_char * 32` | Manager display name |
| `manager` | `int` | `c_int` | Manager permissions bitmask |
| `admin` | `int` | `c_int` | Administrator rights flag (1=yes) |
| `risk_management` | `int` | `c_int` | Risk management rights |
| `transfer` | `int` | `c_int` | Balance transfer rights |
| `confirmation` | `int` | `c_int` | Trade confirmation required |
| `ip_filter` | `int` | `c_int` | IP filter enabled |
| `ip_from` | `char[16]` | `c_char * 16` | Allowed IP range start |
| `ip_to` | `char[16]` | `c_char * 16` | Allowed IP range end |
| `publications` | `int` | `c_int` | Allowed publications |
| `api_data` | `BYTE[16]` | `c_uint8 * 16` | Reserved plugin data |

### Permission Bitmask Values (`manager` field)

| Bit | Hex | Constant | Meaning |
|-----|-----|----------|---------|
| 0 | `0x0001` | `MANAGER_RIGHT_DETAILED_REPORT` | Detailed reports |
| 1 | `0x0002` | `MANAGER_RIGHT_MARKET_WATCH` | Market Watch edit |
| 2 | `0x0004` | `MANAGER_RIGHT_TRANSACTION` | Execute transactions |
| 4 | `0x0010` | `MANAGER_RIGHT_REQUEST` | Handle trade requests |
| 5 | `0x0020` | `MANAGER_RIGHT_TRADES` | Access trade info |
| 8 | `0x0100` | `MANAGER_RIGHT_BROKER_EQUITY` | Broker equity view |
| 9 | `0x0200` | `MANAGER_RIGHT_REPORTS` | Generate reports |
| 10 | `0x0400` | `MANAGER_RIGHT_TECHNICAL` | Technical access |
| 11 | `0x0800` | `MANAGER_RIGHT_PLUGINS` | Plugin management |

---

## Sample Response (JSON)

```json
{
  "connected": true,
  "server": "88.218.200.140:443",
  "login": 52,
  "is_connected": 1,
  "ping_result": 0,
  "login_result": 0,
  "manager_rights": {
    "login": 52,
    "name": "Manager52",
    "admin": 1,
    "manager": 65535,
    "risk_management": 1,
    "transfer": 1
  }
}
```

---

## Error Handling

```python
# Return code meanings
RET_OK           = 0   # success
RET_OK_NONE      = 1   # success, no data
RET_ERROR        = 2   # generic error
RET_NO_CONNECT   = 5   # not connected
RET_NOT_ENOUGH_RIGHTS = 6   # permissions denied
RET_ACC_BAD_PASSWORD  = 65  # wrong password

if ret != 0:
    # Get text description
    error_desc = manager.ErrorDescription(ret)
    print(f"Error {ret}: {error_desc.decode()}")
```

---

## Notes

- Always call `Disconnect()` + `Release()` in a `finally` block to avoid resource leaks.
- The `Connect()` call accepts `"server"` (uses default port 443) or `"server:port"` format.
- Only accounts from the MT4 `managers` group can authenticate via the Manager API.
- Use `Ping()` every 30–60 seconds on idle connections to prevent server-side timeout.
