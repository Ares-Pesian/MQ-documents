# TickLast - Get the Latest Tick for a Symbol

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns the most recent tick for a symbol from the pump cache. Requires `PUMP_MODE_SYMBOLS`.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.TickLast(symbol: str) -> MTTick` |

## Example Code

```python
tick = manager.TickLast("EURUSD")
print(tick.datetime, tick.bid, tick.ask, tick.last, tick.volume)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `ask` | float | `1.15551` |
| `bid` | float | `1.15549` |
| `datetime` | int | `1774274272` |
| `datetime_msc` | int | `1774274272260` |
| `flags` | int | `0` |
| `last` | float | `0.0` |
| `volume` | int | `0` |
| `volume_ext` | int | `0` |


## Raw Sample Response

```json
{
  "ask": 1.15551,
  "bid": 1.15549,
  "datetime": 1774274272,
  "datetime_msc": 1774274272260,
  "flags": 0,
  "last": 0.0,
  "volume": 0,
  "volume_ext": 0
}
```
