# BookGet - Retrieve Depth of Market (Order Book) for a Symbol

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns the current order-book levels for a symbol. Each level has a Type (buy/sell), Price, and Volume.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.BookGet(symbol: str) -> list[MTBook]` |

## Example Code

```python
book = manager.BookGet("EURUSD")
for level in book:
    print(level.Type, level.Price, level.Volume)
```

## Response Fields

> **Error encountered:** `(-1, <EnMTAPIRetcode.MT_RET_ERR_NOTFOUND: 13>, 'Not found')`

_No data returned (endpoint may require active data or different permissions)_
