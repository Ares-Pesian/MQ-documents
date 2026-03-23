# OrderGetByLogins - Get Active Orders for Specific Users (Cache)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns all active/pending orders for specific user logins from the pump cache.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.OrderGetByLogins(logins: list[int], group: str) -> list[MTOrder]` |

## Example Code

```python
orders = manager.OrderGetByLogins([1036], "*")
for order in orders:
    print(order.Order, order.Symbol, order.Type, order.VolumeCurrent)
```

## Response Fields

> **Error encountered:** `(-2, <EnMTAPIRetcode.MT_RET_ERROR: 2>, 'Invalid number of arguments')`

_No data returned (endpoint may require active data or different permissions)_
