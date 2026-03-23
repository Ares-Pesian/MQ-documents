# UserPasswordChange - Change a User Password (WRITE)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Changes the trading or investor password for a user.

**Password types:**
- `MTUser.EnUsersPasswords.USER_PASS_MAIN` - Main (trading) password
- `MTUser.EnUsersPasswords.USER_PASS_INVESTOR` - Read-only investor password

> **WRITE OPERATION** - returns `True` on success.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.UserPasswordChange(pass_type: EnUsersPasswords, login: int, new_password: str) -> bool` |

## Example Code

```python
result = manager.UserPasswordChange(
    MT5Manager.MTUser.EnUsersPasswords.USER_PASS_MAIN,
    1036,
    "NewSecurePass123!"
)
print("Success" if result else MT5Manager.LastError())
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `result` | str | `bool - True on success, False on failure` |
