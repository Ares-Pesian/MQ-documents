# SummaryGet - Symbol Position Summary

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->SummaryGet(symbol, *summary) -> int` |

## Example Code

```python
ss = SymbolSummary()
ret = manager->SummaryGet("EURUSD", &ss)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `symbol` | str | `EURUSD` |
| `count` | int | `42` |
| `volume` | int | `5000` |
| `volume_buy` | int | `3000` |
| `volume_sell` | int | `2000` |
| `profit` | float | `1250.5` |
| `hedged` | int | `1000` |
| `hedged_buy` | float | `1000.0` |
| `hedged_sell` | float | `0.0` |

## Raw Sample

```json
{
  "symbol": "EURUSD",
  "count": 42,
  "volume": 5000,
  "volume_buy": 3000,
  "volume_sell": 2000,
  "profit": 1250.5,
  "hedged": 1000,
  "hedged_buy": 1000.0,
  "hedged_sell": 0.0
}
```
