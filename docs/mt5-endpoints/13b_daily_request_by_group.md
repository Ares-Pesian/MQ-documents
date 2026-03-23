# DailyRequestByGroup - Daily Account Reports by Group Mask

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns end-of-day account snapshots for all users matching the group mask.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.DailyRequestByGroup(group_mask: str, from: datetime, to: datetime) -> list[MTDaily]` |

## Example Code

```python
import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=30)
daily = manager.DailyRequestByGroup("*", from_date, now)
print(f"Total daily records: {len(daily)}")
```

## Response Fields

> **Error encountered:** `(-1, <EnMTAPIRetcode.MT_RET_ERR_NOTFOUND: 13>, 'Not found')`

_No data returned (endpoint may require active data or different permissions)_
