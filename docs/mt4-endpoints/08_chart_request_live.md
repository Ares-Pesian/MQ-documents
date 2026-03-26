# ChartRequest - OHLCV Bar History

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->ChartRequest(*req, *total) -> RateInfo*` |

## Example Code

```python
req = ChartInfo()
req.symbol = b"EURUSD"; req.period = 60; req.count = 500
total = ctypes.c_int(0)
ptr = manager->ChartRequest(&req, &total)
bars = cast_array(ptr, total.value, RateInfo)
manager->MemFree(ptr)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `ctm` | int | `1700100000` |
| `open` | float | `1.0845` |
| `high` | float | `1.0862` |
| `low` | float | `1.0838` |
| `close` | float | `1.0855` |
| `vol` | float | `1523.0` |

## Raw Sample

```json
{
  "ctm": 1700100000,
  "open": 1.0845,
  "high": 1.0862,
  "low": 1.0838,
  "close": 1.0855,
  "vol": 1523.0
}
```
