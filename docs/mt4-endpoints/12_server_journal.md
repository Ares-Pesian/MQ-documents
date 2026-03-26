# ServerTime / JournalRequest / PerformanceRequest — Server Data

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve server time, journal (log) entries, and performance metrics.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `ServerTime()`, `JournalRequest(*req, *total)`, `PerformanceRequest(from, *total)` |

## Example Code

```python
import ctypes, time

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login

# --- Server current time ---
# time_t srv_time = manager->ServerTime()
# print(f"Server time: {time.ctime(srv_time)}")

# --- Journal (server log) entries ---
req = LogRequest()
req.from_time = int(time.time()) - 3600  # last hour
req.to_time   = int(time.time())
req.filter[0:4] = b"*"   # filter by message text

total = ctypes.c_int(0)
# LogInfo* logs = manager->JournalRequest(&req, &total)
# for i in range(total.value):
#     log = logs[i]
#     print(log.ctm, log.type, log.message.decode())
# manager->MemFree(logs)

# --- Server performance metrics ---
from_time = int(time.time()) - 3600
total = ctypes.c_int(0)
# PerfInfo* perf = manager->PerformanceRequest(from_time, &total)
# for i in range(total.value):
#     p = perf[i]
#     print(p.ctm, p.cpu, p.connection)
# manager->MemFree(perf)
```

## Response Fields — `LogInfo` Structure (Journal)

```python
import ctypes

class LogInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",     ctypes.c_int),        # Log entry timestamp (Unix ts)
        ("type",    ctypes.c_int),        # Log type/level (see below)
        ("message", ctypes.c_char * 512), # Log message text
    ]
```

## LogInfo Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `ctm` | `int` | Log entry timestamp (Unix) | `1700100000` |
| `type` | `int` | Log level/type (see table) | `1` |
| `message` | `char[512]` | Log message text | `"Login: 52 from 1.2.3.4"` |

### Log Type Values

| Value | Description |
|-------|-------------|
| `0` | Information |
| `1` | Warning |
| `2` | Error |
| `3` | Debug |

## LogRequest Structure

| Field | C Type | Description |
|-------|--------|-------------|
| `from_time` | `int` | Start time filter (Unix ts) |
| `to_time` | `int` | End time filter (Unix ts) |
| `filter` | `char[64]` | Text filter (* = all) |

## Response Fields — Performance Metrics

```python
import ctypes

class PerfInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",        ctypes.c_int),   # Measurement time (Unix ts)
        ("cpu",        ctypes.c_int),   # CPU usage %
        ("connection", ctypes.c_int),   # Active connections count
        ("memory",     ctypes.c_int),   # Memory usage MB
        ("network",    ctypes.c_int),   # Network I/O bytes/sec
        ("reserved",   ctypes.c_int * 8), # Reserved
    ]
```

## PerfInfo Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `ctm` | `int` | Measurement timestamp | `1700100000` |
| `cpu` | `int` | CPU usage percentage | `25` |
| `connection` | `int` | Active TCP connections | `142` |
| `memory` | `int` | Memory usage in MB | `512` |
| `network` | `int` | Network bytes per second | `10240` |

## Related Functions

| Function | Description |
|----------|-------------|
| `ServerTime()` | Get current server time |
| `JournalRequest(*req, *total)` | Get server log entries |
| `PerformanceRequest(from, *total)` | Get performance metrics |
| `SrvRestart()` | **WRITE ADMIN** — Restart server |
| `SrvChartsSync()` | **WRITE ADMIN** — Sync history |
| `SrvLiveUpdateStart()` | **WRITE ADMIN** — Start live update |
