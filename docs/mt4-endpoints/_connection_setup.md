# MT4 Manager API — Connection Setup & Python Approach

> Server: `88.218.200.140:443` | Library: `mtmanapi.dll` (32-bit) / `mtmanapi64.dll` (64-bit)

---

## Overview

The MetaTrader 4 Manager API is a **native Windows C++ DLL** library that provides full
administrator and manager access to a MetaTrader 4 trade server. Unlike MT5, there is no
official Python pip package — Python connects via **`ctypes`** wrapping the native DLL.

### Requirements

| Item | Details |
|------|---------|
| **DLL (32-bit)** | `mtmanapi.dll` — obtain from MetaQuotes developer portal |
| **DLL (64-bit)** | `mtmanapi64.dll` — 64-bit version (limited: no mail/news functions) |
| **Python** | 32-bit Python for 32-bit DLL; 64-bit Python for 64-bit DLL |
| **OS** | Windows only |
| **Credentials** | Manager group login + password |

> **Where to get the DLL**: Register as a MetaQuotes API Developer at
> `https://developers.metaquotes.net` and download the MT4 Manager API SDK.
> The SDK contains `mtmanapi.dll`, `mtmanapi64.dll`, and `MT4ManagerAPI.h`.

---

## Protocol Details

The MT4 Manager API uses a **proprietary binary TCP protocol** (not standard TLS/HTTPS).
Port 443 on MT4 servers is the standard manager/trading port using MetaQuotes' own
encryption (RSA key exchange internally handled by the DLL).

- **Do NOT** try to implement raw socket connections — the protocol requires RSA authentication
- **Do NOT** use standard SSL/TLS — the server uses MetaQuotes' own encryption layer
- **Only the official DLL** handles the protocol correctly

---

## Complete Python ctypes Wrapper

```python
"""
MT4 Manager API - Python ctypes wrapper
Requires: mtmanapi64.dll (64-bit) or mtmanapi.dll (32-bit) from MetaQuotes SDK
Place the DLL in the same directory as this script, or in a PATH directory.
"""

import ctypes
import ctypes.wintypes as wintypes
import os
import struct
from ctypes import CDLL, POINTER, c_int, c_uint, c_double, c_char, c_char_p, c_void_p

# ── Load DLL ─────────────────────────────────────────────────────────────────
DLL_PATH_64 = "mtmanapi64.dll"   # 64-bit DLL (for 64-bit Python)
DLL_PATH_32 = "mtmanapi.dll"     # 32-bit DLL (for 32-bit Python)

def load_mt4_dll(dll_path=DLL_PATH_64):
    """Load the MT4 Manager API DLL."""
    try:
        dll = ctypes.WinDLL(dll_path)
        return dll
    except OSError as e:
        raise RuntimeError(
            f"Could not load {dll_path}. "
            f"Download from MetaQuotes developer portal. Error: {e}"
        )

# ── Constants ─────────────────────────────────────────────────────────────────
SERVER   = "88.218.200.140:443"
LOGIN    = 52
PASSWORD = "Vista1234$"

# Manager API version check constant
AUTO_RELEASE_VERSION = 0x0001

# Pumping mode flags
PUMP_START_PUMPING      = 0x01
PUMP_UPDATE_SYMBOLS     = 0x02
PUMP_UPDATE_GROUPS      = 0x03
PUMP_UPDATE_USERS       = 0x04
PUMP_UPDATE_ONLINE      = 0x05
PUMP_UPDATE_BIDASK      = 0x06
PUMP_UPDATE_NEWS        = 0x07
PUMP_UPDATE_NEWS_BODY   = 0x08
PUMP_UPDATE_MAIL        = 0x09
PUMP_UPDATE_TRADES      = 0x0A
PUMP_UPDATE_REQUESTS    = 0x0B
PUMP_UPDATE_PLUGINS     = 0x0C
PUMP_UPDATE_ACTIVATION  = 0x0D
PUMP_UPDATE_MARGINCALL  = 0x0E
PUMP_STOP_PUMPING       = 0x0F
PUMP_UPDATE_NEWS_NEW    = 0x10

# Trade command types (cmd field in TradeRecord)
OP_BUY         = 0   # Buy
OP_SELL        = 1   # Sell
OP_BUY_LIMIT   = 2   # Buy limit pending
OP_SELL_LIMIT  = 3   # Sell limit pending
OP_BUY_STOP    = 4   # Buy stop pending
OP_SELL_STOP   = 5   # Sell stop pending
OP_BALANCE     = 6   # Balance operation
OP_CREDIT      = 7   # Credit operation

# Trade reason codes
REASON_CLIENT  = 0   # client terminal
REASON_EXPERT  = 1   # expert advisor
REASON_DEALER  = 2   # dealer
REASON_SIGNAL  = 3   # signal service
REASON_GATEWAY = 4   # gateway
REASON_MOBILE  = 5   # mobile terminal
REASON_WEB     = 6   # web terminal
REASON_API     = 7   # API


# ── CManagerFactory helper ────────────────────────────────────────────────────
class CManagerFactory:
    """
    Wraps the CManagerFactory from MT4ManagerAPI.h.
    Automatically creates the manager interface from the DLL.
    """

    def __init__(self, dll_path=DLL_PATH_64):
        self._dll = load_mt4_dll(dll_path)
        # MtManCreate returns a pointer to the manager interface (IUnknown-like)
        self._dll.MtManCreate.restype  = c_void_p
        self._dll.MtManCreate.argtypes = [c_uint]
        self._dll.MtManVersion.restype  = c_uint
        self._dll.MtManVersion.argtypes = []

    def version(self):
        """Returns (major_version, build_number) tuple."""
        v = self._dll.MtManVersion()
        return (v >> 16) & 0xFFFF, v & 0xFFFF

    def create(self):
        """Creates and returns the manager interface pointer."""
        ptr = self._dll.MtManCreate(AUTO_RELEASE_VERSION)
        if not ptr:
            raise RuntimeError("MtManCreate returned NULL — DLL may be wrong version")
        return ptr


# ── Connection example ────────────────────────────────────────────────────────
def connect_example():
    """Full connection and usage example."""
    factory = CManagerFactory(DLL_PATH_64)
    ver, build = factory.version()
    print(f"MT4 Manager API version {ver}, build {build}")

    mgr_ptr = factory.create()

    # The manager pointer is a COM-like interface.
    # Call methods via ctypes function pointers from the vtable.
    # See individual endpoint files for vtable method signatures.

    # Connect to server
    # manager->Connect("88.218.200.140:443")
    # manager->Login(52, "Vista1234$")
    # ... (see individual endpoint files)
    # manager->Disconnect()
    # manager->Release()

    print("Manager interface created successfully")
    return mgr_ptr
```

---

## DLL vs 64-bit Limitations

| Feature | `mtmanapi.dll` (32-bit) | `mtmanapi64.dll` (64-bit) |
|---------|------------------------|--------------------------|
| Full support | Yes | Partial |
| MailsRequest | Yes | **NOT available** |
| MailSend | Yes | **NOT available** |
| NewsSend | Yes | **NOT available** |
| NewsGet | Yes | **NOT available** |
| NewsTopicGet | Yes | **NOT available** |
| NewsBodyGet | Yes | **NOT available** |
| All trading functions | Yes | Yes |
| All user functions | Yes | Yes |

> **Recommendation**: Use the 32-bit DLL with 32-bit Python for full functionality.

---

## Available API Sections

| Section | Functions |
|---------|-----------|
| Connect | `Connect`, `Login`, `Disconnect`, `IsConnected`, `Ping`, `PasswordChange`, `ManagerRights` |
| Users | `UsersRequest`, `UserRecordGet`, `UserRecordNew`, `UserRecordUpdate`, `UsersGroupOp` |
| Trades | `TradesRequest`, `TradesUserHistory`, `TradeTransaction`, `TradeCalcProfit` |
| Symbols | `SymbolsRefresh`, `SymbolsGetAll`, `SymbolGet`, `SymbolInfoGet`, `SymbolInfoUpdated` |
| Online | `OnlineRequest`, `OnlineGet`, `OnlineRecordGet` |
| Summary | `SummaryGetAll`, `SummaryGet`, `SummaryGetByCount` |
| Exposure | `ExposureGet`, `ExposureValueGet` |
| Groups | `GroupsRequest`, `GroupsGet`, `GroupRecordGet` |
| Reports | `ReportsRequest`, `DailyReportsRequest` |
| Charts | `ChartRequest`, `TicksRequest`, `TickInfoLast` |
| News/Mail | `MailsRequest`, `MailSend`, `NewsGet`, `NewsTopicGet` |
| Server | `ServerTime`, `JournalRequest`, `PerformanceRequest` |
| Backup | `BackupInfoUsers`, `BackupRequestOrders`, `BackupRestoreOrders` |
| Config | `GroupsRequest`, `CfgRequestGroups`, `CfgUpdateGroup` |
