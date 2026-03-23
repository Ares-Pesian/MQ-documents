# UserAdd / UserUpdate - Create or Update a User Account (WRITE)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

**UserAdd** creates a new trading account. Required fields: `Group`, `Leverage`, `FirstName`, `LastName`. On success, `user.Login` is populated with the assigned login.

**UserUpdate** saves changes to an existing user record.

> **WRITE OPERATION** - not executed during field capture.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.UserAdd(user: MTUser, main_pass: str, investor_pass: str) -> bool
manager.UserUpdate(user: MTUser) -> bool` |

## Example Code

```python
# Create a new user
user = MT5Manager.MTUser(manager)
user.Group    = "demo\\example"
user.Leverage = 100
user.FirstName = "Jane"
user.LastName  = "Doe"
ok = manager.UserAdd(user, "MainPass123!", "InvPass123!")
print(f"Created login: {user.Login}" if ok else MT5Manager.LastError())

# Update existing user
user2 = manager.UserGet(1036)
user2.Comment = "Updated via API"
ok = manager.UserUpdate(user2)
print("Updated" if ok else MT5Manager.LastError())
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `result` | str | `bool - True on success; user.Login populated by server on UserAdd` |
