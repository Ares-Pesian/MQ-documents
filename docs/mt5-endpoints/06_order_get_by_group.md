# OrderGetByGroup - Retrieve Active Orders by Group Mask (Cache)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns all pending/active orders for users matching the group mask from the pump cache. Requires `PUMP_MODE_ORDERS`.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.OrderGetByGroup(group_mask: str) -> list[MTOrder]` |

## Example Code

```python
orders = manager.OrderGetByGroup("*")
for order in orders:
    print(order.Order, order.Login, order.Symbol,
          order.Type, order.TypeFill, order.TypeTime,
          order.VolumeCurrent, order.PriceOrder,
          order.PriceCurrent, order.PriceSL, order.PriceTP, order.State)
```

## Response Fields

_No data returned (endpoint may require active data or different permissions)_
