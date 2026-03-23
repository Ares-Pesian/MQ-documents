# LeverageGet - Retrieve Leverage Schedule Configurations

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Accesses leverage schedule configurations on the server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.LeverageGet(index: int) -> MTLeverage  |  manager.LeverageTotal() -> int` |

## Example Code

```python
total = manager.LeverageTotal()
for i in range(total):
    lev = manager.LeverageGet(i)
    print(lev.Name, lev.Description)
```

## Response Fields

_No data returned (endpoint may require active data or different permissions)_
