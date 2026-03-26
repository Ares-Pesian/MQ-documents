# JournalRequest - Server Log Entries

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->JournalRequest(from, to, *total) -> LogInfo*` |

## Example Code

```python
total = ctypes.c_int(0)
ptr = manager->JournalRequest(now-86400, now, &total)
logs = cast_array(ptr, total.value, LogInfo)
manager->MemFree(ptr)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `ctm` | int | `1700100000` |
| `type` | int | `0` |
| `message` | str | `Login: 52 from 1.2.3.4 MetaTrader 4` |

## Raw Sample

```json
{
  "ctm": 1700100000,
  "type": 0,
  "message": "Login: 52 from 1.2.3.4 MetaTrader 4"
}
```
