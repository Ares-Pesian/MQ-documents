# UsersRequest / UserRecordGet — Retrieve User Accounts

> Library: `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) | Server: `88.218.200.140:443`

---

## Overview

Retrieve one or all client account records from the MT4 trade server.
Returns the `UserRecord` structure containing full account details.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` |
| **Methods** | `UsersRequest(group, total)`, `UserRecordGet(login, info)` (pumping), `UserRecordNew(info)`, `UserRecordUpdate(info)` |

## Example Code

```python
import ctypes

dll = ctypes.WinDLL("mtmanapi64.dll")
# ... (connect & login first — see 01_connect_login.md)

# --- UsersRequest: get ALL user records (direct DB query) ---
total = ctypes.c_int(0)
# manager->UsersRequest("*", &total)
# Returns: UserRecord* array, must free with manager->MemFree()
# "*" = all groups, can use "demo\*" for specific group

# --- UserRecordGet: get single user in pumping mode ---
# Must be in pumping mode (PumpingSwitch called)
user = UserRecord()  # see structure below
# manager->UserRecordGet(login, &user)

# --- AdmUsersRequest: get users with filtering (admin only) ---
# manager->AdmUsersRequest("*", &total)

# --- UserRecordsRequest: get users by login list ---
logins = (ctypes.c_int * 3)(52, 53, 54)
# manager->UserRecordsRequest(logins, 3, &total)
```

## Response Fields — `UserRecord` Structure

> **ctypes definition** — complete `UserRecord` as defined in `MT4ManagerAPI.h`

```python
import ctypes

class UserRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("login",                   ctypes.c_int),        # Account login number
        ("group",                   ctypes.c_char * 16),  # Account group name
        ("password",                ctypes.c_char * 16),  # Hashed password
        ("enable",                  ctypes.c_int),        # Account enabled (1=yes)
        ("enable_change_password",  ctypes.c_int),        # Client can change password
        ("enable_read_only",        ctypes.c_int),        # Investor (read-only) mode
        ("enable_send_reports",     ctypes.c_int),        # Send daily reports
        ("password_phone",          ctypes.c_char * 16),  # Phone password
        ("name",                    ctypes.c_char * 64),  # Client full name
        ("country",                 ctypes.c_char * 64),  # Country
        ("city",                    ctypes.c_char * 64),  # City
        ("state",                   ctypes.c_char * 64),  # State/Province
        ("zipcode",                 ctypes.c_char * 16),  # Zip/Postal code
        ("address",                 ctypes.c_char * 128), # Street address
        ("phone",                   ctypes.c_char * 32),  # Phone number
        ("email",                   ctypes.c_char * 48),  # Email address
        ("comment",                 ctypes.c_char * 64),  # Comment/note
        ("id",                      ctypes.c_char * 32),  # Customer account ID
        ("status",                  ctypes.c_char * 16),  # Account status
        ("regdate",                 ctypes.c_int),        # Registration date (Unix ts)
        ("lastdate",                ctypes.c_int),        # Last modification date
        ("leverage",                ctypes.c_int),        # Account leverage (e.g. 100)
        ("agent_account",           ctypes.c_int),        # Agent/IB account number
        ("timestamp",               ctypes.c_int),        # Last update timestamp
        ("last_ip",                 ctypes.c_uint),       # Last known IP (packed uint32)
        ("balance",                 ctypes.c_double),     # Current balance
        ("prevmonthbalance",        ctypes.c_double),     # Previous month balance
        ("prevbalance",             ctypes.c_double),     # Previous day balance
        ("credit",                  ctypes.c_double),     # Credit amount
        ("interestrate",            ctypes.c_double),     # Interest rate (%)
        ("taxes",                   ctypes.c_double),     # Tax rate (%)
        ("prevmonthequity",         ctypes.c_double),     # Previous month equity
        ("prevequity",              ctypes.c_double),     # Previous day equity
        ("reserved2",               ctypes.c_double * 2),# Reserved fields
        ("margin_level",            ctypes.c_double),     # Custom margin level (%)
        ("send_reports",            ctypes.c_int),        # Reports: 0=no, 1=yes
        ("mqid",                    ctypes.c_char * 32),  # MetaQuotes push ID
        ("user_color",              ctypes.c_uint),       # Display color (RGB)
        ("reserved",                ctypes.c_double * 5), # Reserved
    ]
```

## Field Reference Table

| Field | C Type | Description | Example |
|-------|--------|-------------|---------|
| `login` | `int` | Unique account login number | `52` |
| `group` | `char[16]` | Account group name | `"real\managers"` |
| `password` | `char[16]` | Password hash (not cleartext) | `"***"` |
| `enable` | `int` | Account active: 1=enabled, 0=disabled | `1` |
| `enable_change_password` | `int` | Client can change own password | `1` |
| `enable_read_only` | `int` | Investor (read-only) login: 1=yes | `0` |
| `enable_send_reports` | `int` | Send daily reports to email | `1` |
| `password_phone` | `char[16]` | Phone/IVR password | `"1234"` |
| `name` | `char[64]` | Client full name | `"John Doe"` |
| `country` | `char[64]` | Country name | `"Iran"` |
| `city` | `char[64]` | City | `"Tehran"` |
| `state` | `char[64]` | State or province | `"Tehran"` |
| `zipcode` | `char[16]` | Postal/ZIP code | `"1234567"` |
| `address` | `char[128]` | Street address | `"123 Main St"` |
| `phone` | `char[32]` | Contact phone | `"+98-21-..."` |
| `email` | `char[48]` | Email address | `"user@example.com"` |
| `comment` | `char[64]` | Internal comment/note | `"VIP client"` |
| `id` | `char[32]` | External customer ID | `"CRM-12345"` |
| `status` | `char[16]` | Account status string | `"Active"` |
| `regdate` | `int` | Registration timestamp (Unix) | `1700000000` |
| `lastdate` | `int` | Last modification timestamp | `1700100000` |
| `leverage` | `int` | Leverage multiplier | `100` |
| `agent_account` | `int` | IB/Agent account number | `0` |
| `timestamp` | `int` | Internal timestamp | `1700100000` |
| `last_ip` | `uint` | Last login IP (packed uint32) | `3232235520` |
| `balance` | `double` | Account balance in deposit currency | `10000.00` |
| `prevmonthbalance` | `double` | Balance at end of previous month | `9500.00` |
| `prevbalance` | `double` | Balance at end of previous day | `9900.00` |
| `credit` | `double` | Credit/bonus amount | `500.00` |
| `interestrate` | `double` | Interest rate on balance (%) | `0.0` |
| `taxes` | `double` | Tax rate applied (%) | `0.0` |
| `prevmonthequity` | `double` | Equity at end of previous month | `9600.00` |
| `prevequity` | `double` | Equity at end of previous day | `9950.00` |
| `margin_level` | `double` | Custom stop-out margin level (%) | `0.0` |
| `send_reports` | `int` | Reports enabled: 0=no, 1=yes | `1` |
| `mqid` | `char[32]` | MetaQuotes push notification ID | `"MQ1234..."` |
| `user_color` | `uint` | Account color in Manager UI (RGB) | `16777215` |

## Related Functions

| Function | Description |
|----------|-------------|
| `UsersRequest(group, *total)` | Get all accounts matching group mask (direct DB) |
| `UserRecordsRequest(logins[], count, *total)` | Get specific accounts by login list |
| `UserRecordGet(login, *info)` | Get single account in pumping mode |
| `UsersGet(*total)` | Get all accounts in pumping mode |
| `UserRecordNew(*info)` | **WRITE** — Create new account |
| `UserRecordUpdate(*info)` | **WRITE** — Update account data |
| `UsersGroupOp(group, op, *param)` | **WRITE** — Group operations |
| `UserPasswordCheck(login, password)` | Verify account password |
| `UserPasswordSet(login, type, password)` | **WRITE** — Change password |
| `AdmUsersRequest(group, *total)` | Admin: get users from current DB |
| `AdmBalanceCheck(logins[], count, *total)` | Admin: check balances |
| `UsersSyncStart()` | Internal use only |

## UserInfo (Brief) Structure

For lightweight listing, `SymbolInfoGet` returns `UserInfo`:

| Field | C Type | Description |
|-------|--------|-------------|
| `login` | `int` | Account login |
| `group` | `char[16]` | Group name |
| `leverage` | `int` | Leverage |
| `enable` | `int` | Enabled flag |
| `name` | `char[64]` | Full name |
