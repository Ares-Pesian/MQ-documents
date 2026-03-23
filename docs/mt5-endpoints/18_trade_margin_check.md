# TradeMarginCheck - Calculate Required Margin for a Trade

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Calculates the margin requirements for a hypothetical trade without executing it.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.TradeMarginCheck(login: int, symbol: str, type: int, volume: float) -> MTMarginCheck` |

## Example Code

```python
# type: 0=buy, 1=sell
margin = manager.TradeMarginCheck(1036, "EURUSD", 0, 1.0)
print(margin.Margin, margin.MarginFree, margin.Equity)
```

## Response Fields

> **Error encountered:** `(-2, <EnMTAPIRetcode.MT_RET_ERROR: 2>, 'Incorrect parameter type')`

_No data returned (endpoint may require active data or different permissions)_
