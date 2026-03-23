# TickHistoryRequest - Retrieve Historical Tick Data for a Symbol

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Fetches historical tick (bid/ask/last/volume) data for a symbol within a time range.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.TickHistoryRequest(symbol: str, from: datetime, to: datetime) -> list[MTTick]` |

## Example Code

```python
import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=1)
ticks = manager.TickHistoryRequest("EURUSD", from_date, now)
for t in ticks[:5]:
    print(t.datetime, t.bid, t.ask, t.last, t.volume)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `ask` | float | `1.1543700000000001` |
| `bid` | float | `1.15416` |
| `datetime` | int | `1774224000` |
| `datetime_msc` | int | `1774224000553` |
| `flags` | int | `134` |
| `last` | float | `0.0` |
| `volume` | int | `0` |
| `volume_ext` | int | `0` |


## Raw Sample Response

```json
{
  "ask": 1.1543700000000001,
  "bid": 1.15416,
  "datetime": 1774224000,
  "datetime_msc": 1774224000553,
  "flags": 134,
  "last": 0.0,
  "volume": 0,
  "volume_ext": 0
}
```
