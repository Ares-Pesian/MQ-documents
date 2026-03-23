# OrderRequestOpen - Fetch Open Orders from Server for a User

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Fetches all currently active/pending orders for a user directly from the server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.OrderRequestOpen(login: int) -> list[MTOrder]` |

## Example Code

```python
orders = manager.OrderRequestOpen(1036)
for order in orders:
    print(order.Order, order.Symbol, order.Type, order.PriceOrder)
```

## Response Fields

> **Error encountered:** `(-1, <EnMTAPIRetcode.MT_RET_ERR_NOTFOUND: 13>, 'Not found')`

_No data returned (endpoint may require active data or different permissions)_
