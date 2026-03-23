# OnlineGetArray - Retrieve All Currently Connected Users

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns all users currently connected to the trade server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.OnlineGetArray() -> list[MTOnline]` |

## Example Code

```python
connections = manager.OnlineGetArray()
for c in connections:
    print(c.Login, c.IP, c.ConnectTime, c.LastAccessTime, c.Agent)
```

## Response Fields

_No data returned (endpoint may require active data or different permissions)_
