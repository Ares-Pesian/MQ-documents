# SymbolInfoGet - Market Watch Snapshot

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->SymbolInfoGet(symbol, *info) -> int` |

## Example Code

```python
info = SymbolInfo()
ret = manager->SymbolInfoGet("EURUSD", &info)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `symbol` | str | `EURUSD` |
| `digits` | int | `5` |
| `spread` | int | `10` |
| `spread_float` | int | `1` |
| `bid` | float | `1.0845` |
| `ask` | float | `1.0846` |
| `session_price` | float | `1.083` |
| `high` | float | `1.086` |
| `low` | float | `1.081` |
| `time` | int | `1700100000` |

## Raw Sample

```json
{
  "symbol": "EURUSD",
  "digits": 5,
  "spread": 10,
  "spread_float": 1,
  "bid": 1.0845,
  "ask": 1.0846,
  "session_price": 1.083,
  "high": 1.086,
  "low": 1.081,
  "time": 1700100000
}
```
