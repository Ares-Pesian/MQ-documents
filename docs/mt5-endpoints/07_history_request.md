# HistoryRequest - Retrieve Historical Orders for a User

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Fetches historical (filled/cancelled/rejected) orders for a user within a date range. Same MTOrder structure as active orders but with final `State` values.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.HistoryRequest(login: int, from: datetime, to: datetime) -> list[MTOrder]` |

## Example Code

```python
import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=90)
orders = manager.HistoryRequest(1036, from_date, now)
for order in orders:
    print(order.Order, order.Symbol, order.Type, order.State,
          order.VolumeCurrent, order.PriceOrder, order.TimeSetup, order.TimeDone)
```

## Response Fields

> **Error encountered:** `(-1, <EnMTAPIRetcode.MT_RET_ERR_NOTFOUND: 13>, 'Not found')`

_No data returned (endpoint may require active data or different permissions)_
