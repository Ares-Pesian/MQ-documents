# News - Retrieve News Items from the Server

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Accesses the MT5 news database. Use `NewsTotal()` for count, `NewsGet(index)` for individual items.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.NewsGet(index: int) -> MTNews  |  manager.NewsTotal() -> int` |

## Example Code

```python
total = manager.NewsTotal()
for i in range(total):
    news = manager.NewsGet(i)
    print(news.Datetime, news.Subject, news.Category, news.Language)
```

## Response Fields

_No data returned (endpoint may require active data or different permissions)_
