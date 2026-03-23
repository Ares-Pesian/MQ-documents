# DealRequest - Retrieve Deal History for a User

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Fetches the complete deal history for a specific user within a date range directly from the server. Returns a list of `MTDeal` objects.

Each deal represents a single trade execution (open/close leg) or a balance/credit/bonus operation.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.DealRequest(login: int, from: datetime, to: datetime) -> list[MTDeal]` |

## Example Code

```python
import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=90)
deals = manager.DealRequest(1036, from_date, now)
print(f"Got {len(deals)} deals")
for deal in deals[:5]:
    print(deal.Deal, deal.Login, deal.Symbol, deal.Action,
          deal.Volume, deal.Price, deal.Profit, deal.Time)
```

## Response Fields

> **Error encountered:** `(-1, <EnMTAPIRetcode.MT_RET_ERR_NOTFOUND: 13>, 'Not found')`

_No data returned (endpoint may require active data or different permissions)_
