# Online Sessions / Active Connections

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Online Connections](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_online)

---

## Overview

The Online Connections API returns the list of clients currently connected to the MT4 Server.
Each `OnlineRecord` contains: login, IP address, connection type, connection time, and ping latency.

Used for: active session monitoring, IP geolocation, suspicious login detection, session analytics.

---

## Methods

| Method | Purpose |
|--------|---------|
| `OnlineRequest` | Get all active sessions (direct mode) |
| `OnlineGet` | Get all sessions from pumping cache |
| `OnlineRecordGet` | Get session for a specific login (pumping) |

---

## Example Code

```python
import ctypes

# ─── OnlineRequest — all active sessions ─────────────────────────────────────
total = ctypes.c_int(0)
online_ptr = manager.OnlineRequest(ctypes.byref(total))

if online_ptr:
    print(f"Active sessions: {total.value}")
    OnlineRecordArray = OnlineRecord * total.value
    sessions = ctypes.cast(online_ptr, ctypes.POINTER(OnlineRecordArray)).contents
    records = [struct_to_dict(s) for s in sessions]
    manager.MemFree(online_ptr)
    print(records[0])
```

---

## OnlineRecord Structure

```python
class OnlineRecord(ctypes.Structure):
    _fields_ = [
        ("login",         ctypes.c_int),
        ("group",         ctypes.c_char * 16),
        ("ip",            ctypes.c_char * 16),
        ("name",          ctypes.c_char * 128),
        ("country",       ctypes.c_char * 32),
        ("city",          ctypes.c_char * 32),
        ("state",         ctypes.c_char * 32),
        ("zipcode",       ctypes.c_char * 16),
        ("address",       ctypes.c_char * 128),
        ("phone",         ctypes.c_char * 32),
        ("email",         ctypes.c_char * 48),
        ("comment",       ctypes.c_char * 64),
        ("id",            ctypes.c_char * 32),
        ("status",        ctypes.c_char * 16),
        ("regdate",       ctypes.c_int),
        ("lastdate",      ctypes.c_int),
        ("leverage",      ctypes.c_int),
        ("balance",       ctypes.c_double),
        ("credit",        ctypes.c_double),
        ("equity",        ctypes.c_double),
        ("margin",        ctypes.c_double),
        ("margin_free",   ctypes.c_double),
        ("margin_level",  ctypes.c_double),
        ("connect_time",  ctypes.c_int),    # when this session started
        ("last_ping",     ctypes.c_int),    # last ping timestamp
        ("ping_ms",       ctypes.c_int),    # current ping in milliseconds
        ("dc_code",       ctypes.c_int),    # data center / connection code
        ("reserved",      ctypes.c_int * 8),
    ]
```

---

## Response Fields

| Field | C++ Type | ctypes | Description | Example |
|-------|----------|--------|-------------|---------|
| `login` | `int` | `c_int` | Account login | `1001` |
| `group` | `char[16]` | `c_char*16` | Account group | `"real\\standard"` |
| `ip` | `char[16]` | `c_char*16` | Client IP address | `"203.0.113.42"` |
| `name` | `char[128]` | `c_char*128` | Client full name | `"John Smith"` |
| `country` | `char[32]` | `c_char*32` | Country | `"United Kingdom"` |
| `city` | `char[32]` | `c_char*32` | City | `"London"` |
| `leverage` | `int` | `c_int` | Account leverage | `100` |
| `balance` | `double` | `c_double` | Current balance | `10000.00` |
| `credit` | `double` | `c_double` | Credit amount | `0.0` |
| `equity` | `double` | `c_double` | Current equity | `10250.00` |
| `margin` | `double` | `c_double` | Used margin | `1000.00` |
| `margin_free` | `double` | `c_double` | Free margin | `9250.00` |
| `margin_level` | `double` | `c_double` | Margin level % | `1025.0` |
| `connect_time` | `int` (time_t) | `c_int` | Session start timestamp | `1711190000` |
| `last_ping` | `int` (time_t) | `c_int` | Last ping timestamp | `1711190395` |
| `ping_ms` | `int` | `c_int` | Ping latency in milliseconds | `42` |
| `dc_code` | `int` | `c_int` | Data center connection code | `0` |

---

## Sample Raw Response (JSON)

```json
[
  {
    "login": 1001,
    "group": "real\\standard",
    "ip": "203.0.113.42",
    "name": "John Smith",
    "country": "United Kingdom",
    "city": "London",
    "leverage": 100,
    "balance": 10000.00,
    "credit": 0.0,
    "equity": 10250.00,
    "margin": 1000.00,
    "margin_free": 9250.00,
    "margin_level": 1025.0,
    "connect_time": 1711190000,
    "last_ping": 1711190395,
    "ping_ms": 42,
    "dc_code": 0
  }
]
```

---

## Notes

- `OnlineRequest` returns only **currently active** sessions — not historical.
- `connect_time` is when the TCP connection was established (not last trade time).
- `ping_ms` is the round-trip latency from server to client terminal.
- In pumping mode, `PUMP_UPDATE_ONLINE` fires whenever the online list changes (connect/disconnect).
- Useful for: detecting concurrent logins from different IPs, latency monitoring, geo anomaly detection.
