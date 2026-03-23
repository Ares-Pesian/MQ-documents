# DailyRequest - Retrieve Daily Account Reports for a User

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns end-of-day account snapshots for a user, including balance, equity, and floating P&L at the end of each trading day.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.DailyRequest(login: int, from: datetime, to: datetime) -> list[MTDaily]` |

## Example Code

```python
import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=90)
daily = manager.DailyRequest(1036, from_date, now)
for d in daily:
    print(d.Login, d.Datetime, d.Balance, d.Equity,
          d.Profit, d.Credit, d.Margin, d.MarginFree)
```

## Response Fields

> **Error encountered:** `(-1, <EnMTAPIRetcode.MT_RET_ERR_NOTFOUND: 13>, 'Not found')`

_No data returned (endpoint may require active data or different permissions)_
