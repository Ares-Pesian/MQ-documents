# TradeProfit - Calculate Profit for a Hypothetical Trade

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Calculates the profit/loss for a hypothetical position in account currency.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.TradeProfit(login: int, symbol: str, type: int, volume: float, price_open: float, price_close: float) -> float` |

## Example Code

```python
profit = manager.TradeProfit(1036, "EURUSD", 0, 1.0, 1.0800, 1.0900)
print(f"Estimated profit: {profit}")
```

## Response Fields

> **Error encountered:** `(-2, <EnMTAPIRetcode.MT_RET_ERROR: 2>, 'Incorrect parameter type')`

_No data returned (endpoint may require active data or different permissions)_
