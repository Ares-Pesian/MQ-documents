# MailsRequest / NewsGet — Internal Mail & News

> Library: `mtmanapi.dll` (32-bit ONLY) | Server: `88.218.200.140:443`

---

## Overview

Retrieve internal platform mail and news. These functions are available
in the **32-bit DLL only** (`mtmanapi.dll`). The 64-bit version does NOT
support mail/news functions.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` (32-bit only — NOT in mtmanapi64.dll) |
| **Methods** | `MailsRequest(from, *total)`, `MailLast()`, `NewsGet(*total)`, `NewsTopicGet(index)`, `NewsBodyRequest(key)`, `NewsBodyGet(key)` |

## Example Code

```python
import ctypes

# IMPORTANT: Use 32-bit DLL + 32-bit Python for mail/news
dll = ctypes.WinDLL("mtmanapi.dll")   # 32-bit only!
# ... connect & login

# --- Get all recent mails ---
total = ctypes.c_int(0)
from_time = int(time.time()) - 86400 * 7  # last 7 days
# MailBoxHeader* mails = manager->MailsRequest(from_time, &total)
# for i in range(total.value):
#     m = mails[i]
#     print(m.subject.decode(), m.from_id, m.to.decode(), m.date)
# manager->MemFree(mails)

# --- Get last received mail (pumping) ---
# Called from PUMP_UPDATE_MAIL callback
mail = MailBoxHeader()
# manager->MailLast(&mail)

# --- News: get all news keys in cache ---
total = ctypes.c_int(0)
# UINT* keys = manager->NewsGet(&total)

# --- Get total news count ---
# int count = manager->NewsTotal()

# --- Get news header by index ---
topic = NewsTopic()
# manager->NewsTopicGet(0, &topic)

# --- Request news body from server ---
# manager->NewsBodyRequest(key)  # async, result via PUMP_UPDATE_NEWS_BODY
# manager->NewsBodyGet(key)      # sync read after body received
```

## Response Fields — `MailBoxHeader` Structure

```python
import ctypes

class MailBoxHeader(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("subject",  ctypes.c_char * 128),  # Mail subject line
        ("from_id",  ctypes.c_char * 16),   # Sender login/ID
        ("to",       ctypes.c_char * 128),  # Recipients (comma-separated)
        ("date",     ctypes.c_int),         # Send timestamp (Unix ts)
        ("key",      ctypes.c_uint),        # Unique mail key
        ("reserved", ctypes.c_int * 4),    # Reserved
    ]
```

## MailBoxHeader Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `subject` | `char[128]` | Mail subject line | `"Account Update"` |
| `from_id` | `char[16]` | Sender account login or group | `"manager"` |
| `to` | `char[128]` | Recipient logins (comma separated) | `"52,53,54"` |
| `date` | `int` | Send timestamp (Unix) | `1700100000` |
| `key` | `uint` | Unique message identifier | `987654321` |

## Response Fields — `NewsTopic` Structure

```python
import ctypes

class NewsTopic(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("key",        ctypes.c_uint),        # Unique news key
        ("time",       ctypes.c_int),         # Publish timestamp (Unix ts)
        ("topic",      ctypes.c_char * 128),  # News headline/title
        ("category",   ctypes.c_char * 32),   # News category
        ("reserved",   ctypes.c_int * 4),    # Reserved
    ]
```

## NewsTopic Field Reference

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `key` | `uint` | Unique news identifier | `12345678` |
| `time` | `int` | Publication timestamp (Unix) | `1700100000` |
| `topic` | `char[128]` | News headline | `"Fed Rate Decision"` |
| `category` | `char[32]` | News category | `"Forex"` |

## `NewsTopicNew` — Enhanced News Format

| Field | C Type | Description |
|-------|--------|-------------|
| `key` | `uint` | Unique news key |
| `time` | `int` | Publish time (Unix ts) |
| `topic` | `char[128]` | Headline |
| `category` | `char[32]` | Category |
| `language` | `int` | Language code |
| `importance` | `int` | Priority/importance (0–3) |

## Related Functions

| Function | DLL | Description |
|----------|-----|-------------|
| `MailsRequest(from, *total)` | 32-bit only | Get historical mails |
| `MailLast(*mail)` | 32-bit only | Get last mail (pumping) |
| `MailSend(*mail)` | 32-bit only | **WRITE** — Send mail |
| `NewsGet(*total)` | 32-bit only | Get news keys array |
| `NewsTotal()` | 32-bit only | Get news count |
| `NewsTopicGet(index, *topic)` | 32-bit only | Get news header by index |
| `NewsBodyRequest(key)` | 32-bit only | Request news body async |
| `NewsBodyGet(key)` | 32-bit only | Get news body text |
| `NewsSend(*topic, body)` | 32-bit only | **WRITE** — Publish news |
| `NotificationsSend(mqids[], logins[], msg)` | Both | **WRITE** — Push notification |
