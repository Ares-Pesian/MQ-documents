# ServerTime - Get Current Server Time

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->ServerTime() -> time_t` |

## Example Code

```python
srv_time = manager->ServerTime()
print(f"Server UTC: {time.ctime(srv_time)}")
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `server_time_unix` | int | `1700100000` |
| `server_time_utc` | str | `2023-11-15 12:00:00 UTC` |

## Raw Sample

```json
{
  "server_time_unix": 1700100000,
  "server_time_utc": "2023-11-15 12:00:00 UTC"
}
```
