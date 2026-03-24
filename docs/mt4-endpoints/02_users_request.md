# Users / Accounts

> **Server:** `88.218.200.140:443` | **Login:** `52`
> **Source:** [MetaQuotes MT4 Manager API — Users](https://support.metaquotes.net/en/docs/mt4/api/manager_api/manager_api_user)

---

## Overview

Retrieves client/account records from the MT4 Server database. Each record is a `UserRecord` struct
containing full account data: identity, group, balance, leverage, permissions, and metadata.

In MT4, "users" and "accounts" are the same entity — every trading account IS a user record.

---

## Methods

| Method | Purpose | When to Use |
|--------|---------|-------------|
| `UsersRequest` | Get ALL accounts | Bootstrap full sync |
| `UserRecordsRequest` | Get accounts by list of logins | Incremental update by login list |
| `AdmUsersRequest` | Admin: get accounts by group or login (comma-separated) | Full re-sync by group |
| `UsersSnapshot` | Get list of logins available to this manager | Enumerate scope |
| `UserRecordGet` | Get single account in pumping mode | Pumping/real-time |
| `UsersGet` | Get all accounts in pumping mode | Pumping/real-time |

---

## Example Code

```python
import ctypes
import json

# Assume manager is already connected and logged in
# (see 01_connection.md)

# ─── UsersRequest — get ALL accounts ────────────────────────────────────────
total = ctypes.c_int(0)
users_ptr = manager.UsersRequest(ctypes.byref(total))

if not users_ptr:
    print("UsersRequest failed:", manager.ErrorDescription(manager.GetLastError()).decode())
else:
    print(f"Total users: {total.value}")

    # Cast pointer to UserRecord array
    UserRecordArray = UserRecord * total.value
    users = ctypes.cast(users_ptr, ctypes.POINTER(UserRecordArray)).contents

    records = []
    for user in users:
        records.append(struct_to_dict(user))

    # IMPORTANT: free the memory returned by the API
    manager.MemFree(users_ptr)

    print(json.dumps(records[0], indent=2))


# ─── UserRecordsRequest — get accounts by login list ────────────────────────
logins = (ctypes.c_int * 3)(1001, 1002, 1003)
total2 = ctypes.c_int(0)
users_ptr2 = manager.UserRecordsRequest(logins, 3, ctypes.byref(total2))
# ... same pattern, free with MemFree


# ─── AdmUsersRequest — admin method by group ────────────────────────────────
total3 = ctypes.c_int(0)
users_ptr3 = manager.AdmUsersRequest(b"real\\standard", ctypes.byref(total3))
# request string: comma-separated groups or logins, e.g. b"real,demo" or b"1001,1002"
# ... same pattern, free with MemFree
```

---

## UserRecord Structure

The `UserRecord` C++ struct returned for each account.

> **ctypes definition** — copy field names and types exactly from the C++ header `MT4ManagerAPI.h`

```python
class UserRecord(ctypes.Structure):
    _fields_ = [
        ("login",                ctypes.c_int),
        ("group",                ctypes.c_char * 16),
        ("password",             ctypes.c_char * 16),
        ("enable",               ctypes.c_int),
        ("enable_change_password", ctypes.c_int),
        ("enable_read_only",     ctypes.c_int),
        ("enable_otp",           ctypes.c_int),
        ("password_investor",    ctypes.c_char * 16),
        ("name",                 ctypes.c_char * 128),
        ("country",              ctypes.c_char * 32),
        ("city",                 ctypes.c_char * 32),
        ("state",                ctypes.c_char * 32),
        ("zipcode",              ctypes.c_char * 16),
        ("address",              ctypes.c_char * 128),
        ("phone",                ctypes.c_char * 32),
        ("email",                ctypes.c_char * 48),
        ("comment",              ctypes.c_char * 64),
        ("id",                   ctypes.c_char * 32),
        ("status",               ctypes.c_char * 16),
        ("regdate",              ctypes.c_int),       # time_t — registration date
        ("lastdate",             ctypes.c_int),       # time_t — last login date
        ("leverage",             ctypes.c_int),
        ("agent_account",        ctypes.c_int),
        ("timestamp",            ctypes.c_int),
        ("last_ip",              ctypes.c_char * 16),
        ("balance",              ctypes.c_double),
        ("prevmonthbalance",     ctypes.c_double),
        ("prevbalance",          ctypes.c_double),
        ("credit",               ctypes.c_double),
        ("interestrate",         ctypes.c_double),
        ("taxes",                ctypes.c_double),
        ("send_reports",         ctypes.c_int),
        ("user_color",           ctypes.c_uint32),    # COLORREF
        ("equity",               ctypes.c_double),
        ("margin",               ctypes.c_double),
        ("margin_level",         ctypes.c_double),
        ("margin_free",          ctypes.c_double),
        ("api_data",             ctypes.c_uint8 * 16),
        ("password_phone",       ctypes.c_char * 32),
        ("mqid",                 ctypes.c_char * 32),
        ("reserved",             ctypes.c_int * 7),
    ]
```

---

## Response Fields

| Field | C++ Type | ctypes | Description | Example |
|-------|----------|--------|-------------|---------|
| `login` | `int` | `c_int` | Account login number (unique ID) | `1001` |
| `group` | `char[16]` | `c_char*16` | Group name (e.g. "real\\standard") | `"real\\standard"` |
| `password` | `char[16]` | `c_char*16` | Hashed master password (never plaintext) | `"****"` |
| `enable` | `int` | `c_int` | Account enabled: 1=yes, 0=no | `1` |
| `enable_change_password` | `int` | `c_int` | Client can change password | `1` |
| `enable_read_only` | `int` | `c_int` | Read-only account (investor) | `0` |
| `enable_otp` | `int` | `c_int` | OTP (2FA) enabled | `0` |
| `password_investor` | `char[16]` | `c_char*16` | Investor (read-only) password hash | `"****"` |
| `name` | `char[128]` | `c_char*128` | Full client name | `"John Smith"` |
| `country` | `char[32]` | `c_char*32` | Country | `"United Kingdom"` |
| `city` | `char[32]` | `c_char*32` | City | `"London"` |
| `state` | `char[32]` | `c_char*32` | State/province | `""` |
| `zipcode` | `char[16]` | `c_char*16` | Postal code | `"EC1A 1BB"` |
| `address` | `char[128]` | `c_char*128` | Street address | `"123 Main St"` |
| `phone` | `char[32]` | `c_char*32` | Phone number | `"+44..."` |
| `email` | `char[48]` | `c_char*48` | Email address | `"client@example.com"` |
| `comment` | `char[64]` | `c_char*64` | Internal comment | `"VIP"` |
| `id` | `char[32]` | `c_char*32` | External ID (CRM ID) | `"CRM-12345"` |
| `status` | `char[16]` | `c_char*16` | Account status label | `"active"` |
| `regdate` | `int` (time_t) | `c_int` | Registration timestamp (UTC) | `1609459200` |
| `lastdate` | `int` (time_t) | `c_int` | Last login timestamp (UTC) | `1711190400` |
| `leverage` | `int` | `c_int` | Account leverage (e.g. 100 = 1:100) | `100` |
| `agent_account` | `int` | `c_int` | IB/agent account login | `0` |
| `timestamp` | `int` | `c_int` | Last record modification timestamp | `1711190400` |
| `last_ip` | `char[16]` | `c_char*16` | Last login IP address | `"192.168.1.1"` |
| `balance` | `double` | `c_double` | Account balance | `10000.00` |
| `prevmonthbalance` | `double` | `c_double` | Balance at start of previous month | `9500.00` |
| `prevbalance` | `double` | `c_double` | Balance at start of current day | `9800.00` |
| `credit` | `double` | `c_double` | Credit/bonus amount | `0.00` |
| `interestrate` | `double` | `c_double` | Annual interest rate on balance | `0.0` |
| `taxes` | `double` | `c_double` | Cumulative taxes withheld | `0.0` |
| `send_reports` | `int` | `c_int` | Email reports enabled: 1=yes | `1` |
| `user_color` | `uint32` | `c_uint32` | Display color (COLORREF) | `0` |
| `equity` | `double` | `c_double` | Current equity (balance + floating P&L) | `10250.00` |
| `margin` | `double` | `c_double` | Used margin | `1000.00` |
| `margin_level` | `double` | `c_double` | Margin level % (equity/margin * 100) | `1025.0` |
| `margin_free` | `double` | `c_double` | Free margin available | `9250.00` |
| `api_data` | `BYTE[16]` | `c_uint8*16` | Plugin/API reserved data | `[0,0,0...]` |
| `password_phone` | `char[32]` | `c_char*32` | Phone password | `""` |
| `mqid` | `char[32]` | `c_char*32` | MetaQuotes ID | `""` |

---

## Sample Raw Response (JSON)

```json
{
  "login": 1001,
  "group": "real\\standard",
  "password": "****",
  "enable": 1,
  "enable_change_password": 1,
  "enable_read_only": 0,
  "enable_otp": 0,
  "password_investor": "****",
  "name": "John Smith",
  "country": "United Kingdom",
  "city": "London",
  "state": "",
  "zipcode": "EC1A 1BB",
  "address": "123 Main Street",
  "phone": "+44 20 1234 5678",
  "email": "john.smith@example.com",
  "comment": "",
  "id": "CRM-12345",
  "status": "",
  "regdate": 1609459200,
  "lastdate": 1711190400,
  "leverage": 100,
  "agent_account": 0,
  "timestamp": 1711190400,
  "last_ip": "203.0.113.42",
  "balance": 10000.00,
  "prevmonthbalance": 9500.00,
  "prevbalance": 9800.00,
  "credit": 0.00,
  "interestrate": 0.0,
  "taxes": 0.0,
  "send_reports": 1,
  "user_color": 0,
  "equity": 10250.00,
  "margin": 1000.00,
  "margin_level": 1025.00,
  "margin_free": 9250.00,
  "api_data": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
  "password_phone": "",
  "mqid": ""
}
```

---

## Notes

- **Memory management**: `UsersRequest`, `UserRecordsRequest`, and `AdmUsersRequest` return a pointer
  to a heap-allocated array. You **must** call `manager.MemFree(ptr)` after processing to avoid memory leaks.
- **Password field**: passwords are never returned in plaintext — the field contains a hash.
- **Balance vs Equity**: `balance` is the settled balance; `equity` includes floating P&L from open positions.
- **Group filter** in `AdmUsersRequest`: use comma-separated list, e.g. `b"real,demo"` for multiple groups.
- **Timestamp fields** (`regdate`, `lastdate`, `timestamp`) are Unix timestamps (seconds since 1970-01-01 UTC).
