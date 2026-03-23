# RequestGet - Retrieve Pending Trade Requests (Dealer Queue)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Accesses pending trade requests in the dealer queue. Use `RequestTotal()` for count, `RequestGet(index)` for each item.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.RequestGet(index: int) -> MTRequest  |  manager.RequestTotal() -> int` |

## Example Code

```python
total = manager.RequestTotal()
for i in range(total):
    req = manager.RequestGet(i)
    print(req.ID, req.Login, req.Symbol, req.Type, req.Volume, req.Price)
```

## Response Fields

_No data returned (endpoint may require active data or different permissions)_
