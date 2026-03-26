# BackupInfoUsers / BackupRequestOrders — Backup Database Access

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Access backup databases on the MT4 server — retrieve archived users and orders,
and restore records from backup files.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `BackupInfoUsers(*total)`, `BackupInfoOrders(*total)`, `BackupRequestUsers(file, *req, *total)`, `BackupRequestOrders(file, *req, *total)`, `BackupRestoreUsers(*users, count)`, `BackupRestoreOrders(*orders, count)` |

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... connect & login (admin rights required)

# --- List available user backup files ---
total = ctypes.c_int(0)
# BackupInfo* backups = manager->BackupInfoUsers(&total)
# for i in range(total.value):
#     b = backups[i]
#     print(f"Backup: {b.file.decode()}, date: {b.date}, records: {b.total}")
# manager->MemFree(backups)

# --- List available order backup files ---
# BackupInfo* backups = manager->BackupInfoOrders(&total)

# --- Request users from specific backup ---
req = BackupRequest()
req.group[0:2] = b"*"       # all groups
req.login_from = 0          # min login
req.login_to   = 999999     # max login

total = ctypes.c_int(0)
# UserRecord* users = manager->BackupRequestUsers("20240101.bck", &req, &total)
# print(f"Found {total.value} users in backup")
# manager->MemFree(users)

# --- Request orders from backup ---
# TradeRecord* orders = manager->BackupRequestOrders("20240101.bck", &req, &total)

# --- Restore users from backup ---
# int ret = manager->BackupRestoreUsers(users, total.value)

# --- Restore orders from backup ---
# int ret = manager->BackupRestoreOrders(orders, total.value)
```

## Response Fields — `BackupInfo` Structure

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `file` | `char[256]` | Backup filename | `"20240101.bck"` |
| `date` | `int` | Backup creation date (Unix ts) | `1704067200` |
| `total` | `int` | Number of records in backup | `1500` |

## `BackupRequest` Filter Structure

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `group` | `char[16]` | Group mask filter | `"*"` |
| `login_from` | `int` | Minimum login number | `0` |
| `login_to` | `int` | Maximum login number | `999999` |
| `from_date` | `int` | Start date filter (Unix ts) | `0` |
| `to_date` | `int` | End date filter (Unix ts) | `0` |

## Related Functions

| Function | Description |
|----------|-------------|
| `BackupInfoUsers(*total)` | List user backup files |
| `BackupInfoOrders(*total)` | List order backup files |
| `BackupRequestUsers(file, *req, *total)` | Read users from backup |
| `BackupRequestOrders(file, *req, *total)` | Read orders from backup |
| `BackupRestoreUsers(*users, count)` | **WRITE** — Restore users |
| `BackupRestoreOrders(*orders, count)` | **WRITE** — Restore orders |
| `AdmUsersRequest(group, *total)` | Read current DB (not backup) |
| `AdmTradesRequest(group, *total)` | Read current trade DB |
