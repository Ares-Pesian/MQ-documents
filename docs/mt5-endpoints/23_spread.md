# Spread - Retrieve Spread Configurations

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Accesses spread configuration records on the server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.SpreadNext(index: int) -> MTSpread  |  manager.SpreadTotal() -> int` |

## Example Code

```python
total = manager.SpreadTotal()
for i in range(total):
    spread = manager.SpreadNext(i)
    print(spread.Name)
```

## Response Fields

_No data returned (endpoint may require active data or different permissions)_
