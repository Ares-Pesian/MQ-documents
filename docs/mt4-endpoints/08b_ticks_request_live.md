# TicksRequest - Raw Tick History

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->TicksRequest(*req, *total) -> TickAPI*` |

## Example Code

```python
req = TickRequest()
req.symbol = b"EURUSD"; req.from_time = now-3600; req.to_time = now
total = ctypes.c_int(0)
ptr = manager->TicksRequest(&req, &total)
ticks = cast_array(ptr, total.value, TickAPI)
manager->MemFree(ptr)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `ctm` | int | `1700100001` |
| `bid` | float | `1.0845` |
| `ask` | float | `1.0846` |

## Raw Sample

```json
{
  "ctm": 1700100001,
  "bid": 1.0845,
  "ask": 1.0846
}
```
