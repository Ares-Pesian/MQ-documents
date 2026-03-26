# OnlineRequest - Connected Clients

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->OnlineRequest(*total) -> OnlineRecord*` |

## Example Code

```python
total = ctypes.c_int(0)
ptr = manager->OnlineRequest(&total)
online = cast_array(ptr, total.value, OnlineRecord)
manager->MemFree(ptr)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `login` | int | `52` |
| `group` | str | `real\managers` |
| `ip` | int | `3232235520` |
| `login_time` | int | `1700100000` |
| `last_access` | int | `1700100060` |
| `agent` | str | `MetaTrader 4` |
| `version` | int | `1360` |

## Raw Sample

```json
{
  "login": 52,
  "group": "real\\managers",
  "ip": 3232235520,
  "login_time": 1700100000,
  "last_access": 1700100060,
  "agent": "MetaTrader 4",
  "version": 1360
}
```
