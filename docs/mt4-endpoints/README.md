# MT4 Manager API — Complete Endpoint Reference

> **Server tested:** `88.218.200.140:443` | **Manager login:** `52`
> **Documentation date:** 2026-03-24

---

## Integration Method

The MT4 Manager API is a **Windows-only C++ DLL** (`mtmanapi.dll` 32-bit).
It is accessed from Python using `ctypes`. There is no pip package for MT4.

```
mtmanapi.dll  ←  loaded via ctypes.WinDLL()
     │
     └──  MtManCreate()  →  CManagerInterface  (the live manager object)
               │
               ├── Connect("server:port")     ← TCP connection
               ├── Login(login, password)      ← authentication
               └── <all API methods>
```

> **⚠️ Windows only.** This DLL runs exclusively on Windows (32-bit preferred).
> Deploy the MT4 collector service on a Windows EC2 instance or Windows Docker container.
> Use `mtmanapi.dll` (32-bit) — the 64-bit version is unsupported and missing key methods.

---

## Two Operational Modes

| Mode | Description | Use For |
|------|-------------|---------|
| **Direct** | Standard request/response calls | Historical data, config, admin ops |
| **Pumping** | Server pushes live updates to callback | Real-time ticks, live order updates |

For the AI FXDealer collector, use **Direct mode** for bootstrap + incremental sync.
Use **Pumping mode** optionally for real-time tick capture.

---

## DLL Factory Pattern

```python
import ctypes

# Load the DLL (path from AWS Secrets Manager — never hardcode)
lib = ctypes.WinDLL("path/to/mtmanapi.dll")

# Get the factory function
MtManCreate = lib.MtManCreate
MtManCreate.restype = ctypes.c_void_p
MtManCreate.argtypes = [ctypes.c_int]  # version

# Create manager interface (version 1 = standard)
manager_ptr = MtManCreate(1)
```

---

## Endpoints Documented

| File | Endpoint Category | Key Methods |
|------|------------------|-------------|
| [01_connection.md](01_connection.md) | Connection & Auth | Connect, Login, Ping, ManagerRights |
| [02_users_request.md](02_users_request.md) | Users / Accounts | UsersRequest, UserRecordsRequest, AdmUsersRequest |
| [03_trades_open.md](03_trades_open.md) | Open Orders | TradesRequest, TradesGetByLogin, AdmTradesRequest |
| [04_trades_history.md](04_trades_history.md) | Trade History (Deals) | TradesUserHistory, ReportsRequest |
| [05_symbols.md](05_symbols.md) | Symbols | SymbolsRefresh, SymbolsGetAll, SymbolGet |
| [06_groups.md](06_groups.md) | Groups / Config | GroupsRequest, CfgRequestGroup |
| [07_server_logs.md](07_server_logs.md) | Server Logs / Journal | JournalRequest |
| [08_online_sessions.md](08_online_sessions.md) | Online Sessions | OnlineRequest |
| [09_exposure.md](09_exposure.md) | Exposure | ExposureGet, ExposureValueGet |
| [10_margin.md](10_margin.md) | Margin State | MarginsGet, MarginLevelGet |
| [11_summary.md](11_summary.md) | Summary Positions | SummaryGetAll, SummaryGet |
| [12_reports.md](12_reports.md) | Daily Reports | DailyReportsRequest, ReportsRequest |
| [13_ticks.md](13_ticks.md) | Ticks / Price Data | TickInfoLast, ChartRequest |

---

## Complete Python Collector Script

See [`../../collect_mt4_responses.py`](../../collect_mt4_responses.py) for a fully working
collector script that connects to the server, calls every endpoint, and saves responses to JSON.

---

## C++ to ctypes Type Mapping

| C++ Type | ctypes Type |
|----------|-------------|
| `int` | `ctypes.c_int` |
| `unsigned int` | `ctypes.c_uint` |
| `long` | `ctypes.c_long` |
| `double` | `ctypes.c_double` |
| `float` | `ctypes.c_float` |
| `char[N]` | `ctypes.c_char * N` |
| `wchar_t[N]` | `ctypes.c_wchar * N` |
| `__int64` | `ctypes.c_int64` |
| `DWORD` | `ctypes.c_uint32` |
| `WORD` | `ctypes.c_uint16` |
| `BYTE` | `ctypes.c_uint8` |
| `time_t` | `ctypes.c_int64` |
| `bool` | `ctypes.c_bool` |
| `void*` | `ctypes.c_void_p` |

---

## Return Codes

| Code | Constant | Meaning |
|------|----------|---------|
| `0` | `RET_OK` | Success |
| `1` | `RET_OK_NONE` | Success, no data |
| `2` | `RET_ERROR` | Generic error |
| `3` | `RET_INVALID_DATA` | Invalid parameters |
| `4` | `RET_TECH_PROBLEM` | Technical problem |
| `5` | `RET_NO_CONNECT` | No connection |
| `6` | `RET_NOT_ENOUGH_RIGHTS` | Insufficient permissions |
| `7` | `RET_TOO_MANY_REQUESTS` | Rate limit |
| `9` | `RET_TRADE_DISABLED` | Trading disabled |
| `64` | `RET_ACC_BAD_ACCOUNT` | Bad account |
| `65` | `RET_ACC_BAD_PASSWORD` | Bad password |
