# Server Logs / Journal

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Server Management](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_server)

---

## Overview

The MT4 Server Journal logs all server-side events: logins, trades, errors, config changes,
and system messages. Each entry is a `LogRecord` (also called `ServerLog`) struct.

Requires manager account with sufficient permissions to access journal.

---

## Methods

| Method | Purpose |
|--------|---------|
| `JournalRequest` | Request server log entries for a time range |
| `JournalDirectory` | Get the directory path where journal files are stored |
| `ServerTime` | Get current server time (UTC timestamp) |
| `PerformanceRequest` | Get server performance metrics |

---

## Example Code

```python
import ctypes
import time

# ─── JournalRequest — server logs for a time period ──────────────────────────
class LogRequest(ctypes.Structure):
    _fields_ = [
        ("from",    ctypes.c_int),    # start time (time_t)
        ("to",      ctypes.c_int),    # end time (time_t)
        ("filter",  ctypes.c_char * 64),  # optional text filter
    ]

req = LogRequest()
req.from_time = int(time.time()) - 86400   # last 24 hours
req.to_time   = int(time.time())
req.filter    = b""   # no filter = all entries

total = ctypes.c_int(0)
logs_ptr = manager.JournalRequest(ctypes.byref(req), ctypes.byref(total))

if logs_ptr:
    print(f"Log entries: {total.value}")
    LogRecordArray = LogRecord * total.value
    logs = ctypes.cast(logs_ptr, ctypes.POINTER(LogRecordArray)).contents
    records = [struct_to_dict(l) for l in logs]
    manager.MemFree(logs_ptr)
    print(records[0])


# ─── ServerTime ───────────────────────────────────────────────────────────────
server_ts = manager.ServerTime()
print(f"Server time (UTC): {server_ts}")
# Convert: datetime.datetime.fromtimestamp(server_ts, tz=datetime.timezone.utc)
```

---

## LogRecord / ServerLog Structure

```python
class LogRecord(ctypes.Structure):
    _fields_ = [
        ("time",        ctypes.c_int),          # event timestamp (time_t UTC)
        ("ip",          ctypes.c_char * 16),    # source IP address
        ("type",        ctypes.c_int),          # log entry type (see enum)
        ("reserved",    ctypes.c_int * 5),      # reserved
        ("description", ctypes.c_char * 128),   # log message text
    ]
```

---

## Response Fields

| Field | C++ Type | ctypes | Description | Example |
|-------|----------|--------|-------------|---------|
| `time` | `int` (time_t) | `c_int` | Event timestamp (UTC) | `1711190400` |
| `ip` | `char[16]` | `c_char*16` | Source IP address | `"203.0.113.10"` |
| `type` | `int` | `c_int` | Log entry type/severity (see enum) | `0` |
| `description` | `char[128]` | `c_char*128` | Log message text | `"'1001' login from 203.0.113.10"` |

---

## Log Type Enum

| Value | Constant | Description |
|-------|----------|-------------|
| `0` | `LOG_TYPE_TRADE` | Trade operation log |
| `1` | `LOG_TYPE_ACCOUNT` | Account action (login, logout) |
| `2` | `LOG_TYPE_CONFIG` | Configuration change |
| `3` | `LOG_TYPE_PLUG` | Plugin event |
| `4` | `LOG_TYPE_SYSTEM` | System event |
| `5` | `LOG_TYPE_REQUEST` | Trade request processed |
| `6` | `LOG_TYPE_BACKUP` | Backup operation |
| `7` | `LOG_TYPE_STOP` | Server stop/start |

---

## LogRequest Structure Fields

| Field | Type | Description |
|-------|------|-------------|
| `from` | `int` (time_t) | Start of log period (UTC) |
| `to` | `int` (time_t) | End of log period (UTC) |
| `filter` | `char[64]` | Optional text filter (empty = all entries) |

---

## Sample Raw Response (JSON)

```json
[
  {
    "time": 1711190400,
    "ip": "203.0.113.10",
    "type": 1,
    "description": "'1001' login from 203.0.113.10"
  },
  {
    "time": 1711190420,
    "ip": "192.168.1.1",
    "type": 0,
    "description": "'1001' buy 1.00 EURUSD at 1.08325 sl: 0.00 tp: 0.00 (market)"
  },
  {
    "time": 1711190500,
    "ip": "0.0.0.0",
    "type": 4,
    "description": "Server performance: CPU 12%, RAM 45%"
  }
]
```

---

## PerformanceRequest

Get server performance history (CPU, memory, network).

```python
class PerformanceInfo(ctypes.Structure):
    _fields_ = [
        ("time",     ctypes.c_int),
        ("cpu",      ctypes.c_int),     # CPU usage %
        ("network",  ctypes.c_int),     # network usage
        ("sockets",  ctypes.c_int),     # active socket count
        ("memory",   ctypes.c_int),     # memory usage MB
        ("pfusage",  ctypes.c_int),     # page file usage
        ("fileinfo", ctypes.c_int),     # file info count
        ("reserved", ctypes.c_int * 4),
    ]

total_perf = ctypes.c_int(0)
from_time  = int(time.time()) - 3600  # last hour
perf_ptr   = manager.PerformanceRequest(from_time, ctypes.byref(total_perf))

if perf_ptr:
    PerfArray = PerformanceInfo * total_perf.value
    perfs = ctypes.cast(perf_ptr, ctypes.POINTER(PerfArray)).contents
    for p in perfs:
        print(f"t={p.time} cpu={p.cpu}% mem={p.memory}MB sockets={p.sockets}")
    manager.MemFree(perf_ptr)
```

---

## Notes

- **Always request bounded time ranges** for `JournalRequest` — unbounded requests on busy servers can return millions of records.
- The `filter` field in `LogRequest` is a text substring filter applied server-side.
- `ServerTime()` returns a Unix timestamp (UTC). Use this to align collector cursors to server time.
- Keep a local cursor (`last_log_time`) and only request logs newer than the cursor for incremental sync.
