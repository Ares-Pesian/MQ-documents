# TradesUserHistory - Trade History

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->TradesUserHistory(login, from, to, *total) -> TradeRecord*` |

## Example Code

```python
total = ctypes.c_int(0)
ptr = manager->TradesUserHistory(52, from_90d, now, &total)
trades = cast_array(ptr, total.value, TradeRecord)
manager->MemFree(ptr)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `order` | int | `123456` |
| `login` | int | `52` |
| `symbol` | str | `EURUSD` |
| `digits` | int | `5` |
| `cmd` | int | `0` |
| `volume` | int | `100` |
| `open_time` | int | `1700000000` |
| `state` | int | `0` |
| `open_price` | float | `1.085` |
| `sl` | float | `1.08` |
| `tp` | float | `1.09` |
| `close_time` | int | `0` |
| `expiration` | int | `0` |
| `reason` | int | `0` |
| `commission` | float | `-2.5` |
| `commission_agent` | float | `0.0` |
| `storage` | float | `-0.5` |
| `close_price` | float | `1.0875` |
| `profit` | float | `250.0` |
| `taxes` | float | `0.0` |
| `magic` | int | `0` |
| `comment` | str | `manual` |
| `margin_rate` | float | `1.0` |
| `timestamp` | int | `1700100000` |

## Raw Sample

```json
{
  "order": 123456,
  "login": 52,
  "symbol": "EURUSD",
  "digits": 5,
  "cmd": 0,
  "volume": 100,
  "open_time": 1700000000,
  "state": 0,
  "open_price": 1.085,
  "sl": 1.08,
  "tp": 1.09,
  "close_time": 0,
  "expiration": 0,
  "reason": 0,
  "commission": -2.5,
  "commission_agent": 0.0,
  "storage": -0.5,
  "close_price": 1.0875,
  "profit": 250.0,
  "taxes": 0.0,
  "magic": 0,
  "comment": "manual",
  "margin_rate": 1.0,
  "timestamp": 1700100000
}
```
