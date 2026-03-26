# OnlineRequest / OnlineGet — Retrieve Online Connections

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve the list of clients currently connected to the trade server.
Shows connection metadata: IP, client version, agent (platform), login time.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `OnlineRequest(*total)`, `OnlineGet(*total)` (pumping), `OnlineRecordGet(login, *info)` (pumping) |

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login

# --- Direct server request (no pumping needed) ---
total   = ctypes.c_int(0)
# OnlineRecord* online = manager->OnlineRequest(&total)
# print(f"Connected clients: {total.value}")
# for i in range(total.value):
#     r = online[i]
#     print(r.login, r.ip, r.agent.decode(), r.login_time)
# manager->MemFree(online)

# --- Pumping mode (preferred for continuous monitoring) ---
# OnlineRecord* online = manager->OnlineGet(&total)
# (called from PUMP_UPDATE_ONLINE callback)

# --- Single client in pumping mode ---
info = OnlineRecord()
# ret = manager->OnlineRecordGet(52, &info)
```

## Response Fields — `OnlineRecord` Structure

```python
import ctypes

class OnlineRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("login",       ctypes.c_int),        # Account login number
        ("group",       ctypes.c_char * 16),  # Account group
        ("ip",          ctypes.c_uint),       # Client IP address (packed uint32)
        ("login_time",  ctypes.c_int),        # Session start time (Unix timestamp)
        ("last_access", ctypes.c_int),        # Last activity time (Unix timestamp)
        ("agent",       ctypes.c_char * 32),  # Client platform name
        ("version",     ctypes.c_int),        # Client terminal build number
        ("reserved",    ctypes.c_char * 28),  # Reserved
    ]
```

## Field Reference Table

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `login` | `int` | Account login number | `52` |
| `group` | `char[16]` | Account group | `"real\managers"` |
| `ip` | `uint` | Client IP address (uint32 packed) | `3232235777` |
| `login_time` | `int` | Session start (Unix timestamp) | `1700100000` |
| `last_access` | `int` | Most recent activity (Unix timestamp) | `1700100060` |
| `agent` | `char[32]` | Client platform/app string | `"MetaTrader 4"` |
| `version` | `int` | Client terminal build number | `1360` |

### Decode IP Address

```python
import socket, struct

def uint_to_ip(packed_ip):
    """Convert packed uint32 IP to dotted string."""
    return socket.inet_ntoa(struct.pack('<I', packed_ip))

# Example: uint_to_ip(3232235777) -> "192.168.1.1"
```

## Related Functions

| Function | Description |
|----------|-------------|
| `OnlineRequest(*total)` | Direct server request — all online clients |
| `OnlineGet(*total)` | Pumping mode — all online clients |
| `OnlineRecordGet(login, *info)` | Pumping mode — single client by login |
