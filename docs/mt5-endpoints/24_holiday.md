# Holiday - Retrieve Holiday / Session Schedules

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Accesses holiday and session schedule records on the server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.HolidayNext(index: int) -> MTHoliday  |  manager.HolidayTotal() -> int` |

## Example Code

```python
total = manager.HolidayTotal()
for i in range(total):
    holiday = manager.HolidayNext(i)
    print(holiday.Symbol, holiday.Mode, holiday.Day, holiday.From, holiday.To)
```

## Response Fields

_No data returned (endpoint may require active data or different permissions)_
