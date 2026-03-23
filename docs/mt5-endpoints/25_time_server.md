# TimeServerRequest - Get the Trade Server's Current Time

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Fetches the current time from the trade server for synchronization.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.TimeServerRequest() -> datetime` |

## Example Code

```python
server_time = manager.TimeServerRequest()
print(f"Server time: {server_time}")
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `server_time` | str | `1774274274070` |


## Raw Sample Response

```json
{
  "server_time": "1774274274070"
}
```
