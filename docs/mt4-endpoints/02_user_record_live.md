# UsersRequest - All User Records

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->UsersRequest(group, *total) -> UserRecord*` |

## Example Code

```python
total = ctypes.c_int(0)
ptr = manager->UsersRequest("*", &total)
users = cast_array(ptr, total.value, UserRecord)
manager->MemFree(ptr)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `login` | int | `52` |
| `group` | str | `real\managers` |
| `enable` | int | `1` |
| `name` | str | `John Doe` |
| `country` | str | `Iran` |
| `city` | str | `Tehran` |
| `email` | str | `client@example.com` |
| `leverage` | int | `100` |
| `balance` | float | `10000.0` |
| `credit` | float | `0.0` |
| `prevmonthbalance` | float | `9500.0` |
| `prevbalance` | float | `9900.0` |
| `interestrate` | float | `0.0` |
| `taxes` | float | `0.0` |
| `regdate` | int | `1700000000` |
| `lastdate` | int | `1700100000` |
| `last_ip` | int | `3232235520` |
| `agent_account` | int | `0` |
| `enable_change_password` | int | `1` |
| `enable_read_only` | int | `0` |
| `send_reports` | int | `1` |
| `margin_level` | float | `0.0` |

## Raw Sample

```json
{
  "login": 52,
  "group": "real\\managers",
  "enable": 1,
  "name": "John Doe",
  "country": "Iran",
  "city": "Tehran",
  "email": "client@example.com",
  "leverage": 100,
  "balance": 10000.0,
  "credit": 0.0,
  "prevmonthbalance": 9500.0,
  "prevbalance": 9900.0,
  "interestrate": 0.0,
  "taxes": 0.0,
  "regdate": 1700000000,
  "lastdate": 1700100000,
  "last_ip": 3232235520,
  "agent_account": 0,
  "enable_change_password": 1,
  "enable_read_only": 0,
  "send_reports": 1,
  "margin_level": 0.0
}
```
