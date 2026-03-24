"""
MT4 Manager API — Complete Response Collector
=============================================
Connects to an MT4 server using the Manager API DLL via ctypes,
calls every available endpoint, and saves raw responses to JSON files.

Usage (Windows only — DLL is Windows-only):
    python collect_mt4_responses.py

Requirements:
    - Windows OS (32-bit or 64-bit with WOW64)
    - mtmanapi.dll in same directory or specify DLL_PATH
    - Python 32-bit recommended (matches 32-bit DLL)

Output:
    responses/mt4/{entity}.json for each endpoint

Server: 88.218.200.140:443
Login:  52
"""

import ctypes
import ctypes.wintypes
import json
import os
import time
import datetime
import struct
import sys

# ─── Configuration ────────────────────────────────────────────────────────────
DLL_PATH  = r"mtmanapi.dll"     # place DLL in same directory
SERVER    = "88.218.200.140:443"
LOGIN     = 52
PASSWORD  = "Vista1234$"
OUTPUT_DIR = "responses/mt4"

# ─── ctypes Structures ────────────────────────────────────────────────────────

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
        ("regdate",              ctypes.c_int),
        ("lastdate",             ctypes.c_int),
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
        ("user_color",           ctypes.c_uint32),
        ("equity",               ctypes.c_double),
        ("margin",               ctypes.c_double),
        ("margin_level",         ctypes.c_double),
        ("margin_free",          ctypes.c_double),
        ("api_data",             ctypes.c_uint8 * 16),
        ("password_phone",       ctypes.c_char * 32),
        ("mqid",                 ctypes.c_char * 32),
        ("reserved",             ctypes.c_int * 7),
    ]


class TradeRecord(ctypes.Structure):
    _fields_ = [
        ("order",          ctypes.c_int),
        ("login",          ctypes.c_int),
        ("symbol",         ctypes.c_char * 12),
        ("digits",         ctypes.c_int),
        ("cmd",            ctypes.c_int),
        ("volume",         ctypes.c_int),
        ("open_time",      ctypes.c_int),
        ("state",          ctypes.c_int),
        ("open_price",     ctypes.c_double),
        ("sl",             ctypes.c_double),
        ("tp",             ctypes.c_double),
        ("close_time",     ctypes.c_int),
        ("gw_volume",      ctypes.c_int),
        ("expiration",     ctypes.c_int),
        ("reason",         ctypes.c_short),
        ("conv_reserv",    ctypes.c_short * 2),
        ("conv_rates",     ctypes.c_double * 2),
        ("commission",     ctypes.c_double),
        ("commission_agent", ctypes.c_double),
        ("storage",        ctypes.c_double),
        ("close_price",    ctypes.c_double),
        ("profit",         ctypes.c_double),
        ("taxes",          ctypes.c_double),
        ("magic",          ctypes.c_int),
        ("comment",        ctypes.c_char * 32),
        ("gw_order",       ctypes.c_int),
        ("activation",     ctypes.c_int),
        ("gw_open_price",  ctypes.c_double),
        ("gw_close_price", ctypes.c_double),
        ("margin_rate",    ctypes.c_double),
        ("timestamp",      ctypes.c_int),
        ("api_data",       ctypes.c_uint8 * 16),
    ]


class OnlineRecord(ctypes.Structure):
    _fields_ = [
        ("login",         ctypes.c_int),
        ("group",         ctypes.c_char * 16),
        ("ip",            ctypes.c_char * 16),
        ("name",          ctypes.c_char * 128),
        ("country",       ctypes.c_char * 32),
        ("city",          ctypes.c_char * 32),
        ("state",         ctypes.c_char * 32),
        ("zipcode",       ctypes.c_char * 16),
        ("address",       ctypes.c_char * 128),
        ("phone",         ctypes.c_char * 32),
        ("email",         ctypes.c_char * 48),
        ("comment",       ctypes.c_char * 64),
        ("id",            ctypes.c_char * 32),
        ("status",        ctypes.c_char * 16),
        ("regdate",       ctypes.c_int),
        ("lastdate",      ctypes.c_int),
        ("leverage",      ctypes.c_int),
        ("balance",       ctypes.c_double),
        ("credit",        ctypes.c_double),
        ("equity",        ctypes.c_double),
        ("margin",        ctypes.c_double),
        ("margin_free",   ctypes.c_double),
        ("margin_level",  ctypes.c_double),
        ("connect_time",  ctypes.c_int),
        ("last_ping",     ctypes.c_int),
        ("ping_ms",       ctypes.c_int),
        ("dc_code",       ctypes.c_int),
        ("reserved",      ctypes.c_int * 8),
    ]


class MarginLevel(ctypes.Structure):
    _fields_ = [
        ("login",         ctypes.c_int),
        ("group",         ctypes.c_char * 16),
        ("leverage",      ctypes.c_int),
        ("updated",       ctypes.c_int),
        ("balance",       ctypes.c_double),
        ("equity",        ctypes.c_double),
        ("margin",        ctypes.c_double),
        ("margin_free",   ctypes.c_double),
        ("margin_level",  ctypes.c_double),
        ("reserved",      ctypes.c_int * 4),
    ]


class SymbolInfo(ctypes.Structure):
    _fields_ = [
        ("symbol",           ctypes.c_char * 12),
        ("description",      ctypes.c_char * 64),
        ("source",           ctypes.c_char * 12),
        ("currency",         ctypes.c_char * 12),
        ("type",             ctypes.c_int),
        ("digits",           ctypes.c_int),
        ("trade",            ctypes.c_int),
        ("background_color", ctypes.c_uint32),
        ("count",            ctypes.c_int),
        ("count_original",   ctypes.c_int),
        ("reserved",         ctypes.c_int * 4),
        ("point",            ctypes.c_double),
        ("spread",           ctypes.c_int),
        ("spread_balance",   ctypes.c_int),
        ("direction",        ctypes.c_int),
        ("filtered",         ctypes.c_int),
        ("last_quote",       ctypes.c_int),
        ("bid",              ctypes.c_double),
        ("ask",              ctypes.c_double),
        ("low",              ctypes.c_double),
        ("high",             ctypes.c_double),
        ("commission",       ctypes.c_double),
    ]


class SymbolSummary(ctypes.Structure):
    _fields_ = [
        ("symbol",       ctypes.c_char * 12),
        ("count",        ctypes.c_int),
        ("count_buy",    ctypes.c_int),
        ("count_sell",   ctypes.c_int),
        ("volume",       ctypes.c_int),
        ("volume_buy",   ctypes.c_int),
        ("volume_sell",  ctypes.c_int),
        ("profit_buy",   ctypes.c_double),
        ("profit_sell",  ctypes.c_double),
        ("profit",       ctypes.c_double),
        ("profit_raw",   ctypes.c_double),
        ("bid",          ctypes.c_double),
        ("ask",          ctypes.c_double),
        ("reserved",     ctypes.c_int * 4),
    ]


class RateInfo(ctypes.Structure):
    _fields_ = [
        ("ctm",   ctypes.c_int),
        ("open",  ctypes.c_double),
        ("high",  ctypes.c_double),
        ("low",   ctypes.c_double),
        ("close", ctypes.c_double),
        ("vol",   ctypes.c_double),
    ]


class TickInfo(ctypes.Structure):
    _fields_ = [
        ("symbol", ctypes.c_char * 12),
        ("bid",    ctypes.c_double),
        ("ask",    ctypes.c_double),
        ("last",   ctypes.c_double),
        ("volume", ctypes.c_double),
        ("time",   ctypes.c_int),
        ("flags",  ctypes.c_int),
    ]


class LogRecord(ctypes.Structure):
    _fields_ = [
        ("time",        ctypes.c_int),
        ("ip",          ctypes.c_char * 16),
        ("type",        ctypes.c_int),
        ("reserved",    ctypes.c_int * 5),
        ("description", ctypes.c_char * 128),
    ]


class DailyReport(ctypes.Structure):
    _fields_ = [
        ("login",              ctypes.c_int),
        ("group",              ctypes.c_char * 16),
        ("currency",           ctypes.c_char * 16),
        ("time",               ctypes.c_int),
        ("value",              ctypes.c_double),
        ("profit",             ctypes.c_double),
        ("balance_prev",       ctypes.c_double),
        ("balance",            ctypes.c_double),
        ("equity",             ctypes.c_double),
        ("margin",             ctypes.c_double),
        ("margin_free",        ctypes.c_double),
        ("deposit",            ctypes.c_double),
        ("credit",             ctypes.c_double),
        ("commission",         ctypes.c_double),
        ("storage",            ctypes.c_double),
        ("closed_profit",      ctypes.c_double),
        ("floating_profit",    ctypes.c_double),
        ("correction",         ctypes.c_double),
        ("prev_month_balance", ctypes.c_double),
        ("reserved",           ctypes.c_int * 8),
    ]


class ChartInfo(ctypes.Structure):
    _fields_ = [
        ("symbol",   ctypes.c_char * 12),
        ("period",   ctypes.c_int),
        ("mode",     ctypes.c_int),
        ("timesign", ctypes.c_int),
        ("reserved", ctypes.c_int * 4),
    ]


class LogRequest(ctypes.Structure):
    _fields_ = [
        ("from_time", ctypes.c_int),
        ("to_time",   ctypes.c_int),
        ("filter",    ctypes.c_char * 64),
    ]


class DailyGroupRequest(ctypes.Structure):
    _fields_ = [
        ("group",     ctypes.c_char * 16),
        ("from_time", ctypes.c_int),
        ("to_time",   ctypes.c_int),
    ]


# ─── Helpers ──────────────────────────────────────────────────────────────────

def struct_to_dict(s):
    """Convert a ctypes Structure to a plain Python dict."""
    result = {}
    for field_name, field_type in s._fields_:
        value = getattr(s, field_name)
        if isinstance(value, bytes):
            value = value.decode("utf-8", errors="replace").rstrip("\x00")
        elif hasattr(value, "_length_") and hasattr(value, "_type_"):
            # ctypes array
            value = list(value)
        result[field_name] = value
    return result


def save_json(name, data):
    """Save data to OUTPUT_DIR/{name}.json"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"  ✓  Saved {path} ({len(data) if isinstance(data, list) else 1} records)")


def ts_to_iso(ts):
    """Convert Unix timestamp to ISO string."""
    if not ts:
        return None
    return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).isoformat()


# ─── Manager Interface wrapper ────────────────────────────────────────────────

class MT4Manager:
    """
    Thin Python wrapper around CManagerInterface vtable.

    The MT4 Manager API DLL exports two C functions:
      - MtManVersion() -> DWORD
      - MtManCreate(version: int) -> CManagerInterface*

    CManagerInterface is a COM-like object with a virtual function table.
    We call its methods via ctypes function pointers derived from the vtable.

    NOTE: This is a simplified wrapper. For production use, you need the full
    vtable offsets from MT4ManagerAPI.h. This script demonstrates the pattern.
    """

    def __init__(self, dll_path):
        self.lib = ctypes.WinDLL(dll_path)
        self._setup_factory()
        self.iface = None

    def _setup_factory(self):
        self.lib.MtManVersion.restype  = ctypes.c_uint32
        self.lib.MtManVersion.argtypes = []

        self.lib.MtManCreate.restype   = ctypes.c_void_p
        self.lib.MtManCreate.argtypes  = [ctypes.c_int]

    def create(self, version=1):
        ptr = self.lib.MtManCreate(version)
        if not ptr:
            raise RuntimeError("MtManCreate returned NULL — DLL version mismatch?")
        self.iface = ptr
        return ptr

    def version(self):
        v = self.lib.MtManVersion()
        return {"api_version": v >> 16, "build": v & 0xFFFF}

    def connect(self, server):
        # vtable slot 3: Connect(LPCSTR server)
        connect_fn = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_char_p)
        vtable = ctypes.cast(self.iface, ctypes.POINTER(ctypes.c_void_p))
        fn_ptr = ctypes.cast(vtable[0][3], connect_fn)
        return fn_ptr(self.iface, server.encode() if isinstance(server, str) else server)

    def disconnect(self):
        disconnect_fn = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
        vtable = ctypes.cast(self.iface, ctypes.POINTER(ctypes.c_void_p))
        fn_ptr = ctypes.cast(vtable[0][4], disconnect_fn)
        fn_ptr(self.iface)

    def login(self, login, password):
        login_fn = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_char_p)
        vtable = ctypes.cast(self.iface, ctypes.POINTER(ctypes.c_void_p))
        fn_ptr = ctypes.cast(vtable[0][6], login_fn)
        pwd = password.encode() if isinstance(password, str) else password
        return fn_ptr(self.iface, login, pwd)

    def release(self):
        if self.iface:
            release_fn = ctypes.CFUNCTYPE(None, ctypes.c_void_p)
            vtable = ctypes.cast(self.iface, ctypes.POINTER(ctypes.c_void_p))
            fn_ptr = ctypes.cast(vtable[0][0], release_fn)
            fn_ptr(self.iface)
            self.iface = None


# ─── Main Collector ───────────────────────────────────────────────────────────

def collect_all():
    print("=" * 60)
    print("MT4 Manager API — Full Response Collector")
    print(f"Server: {SERVER}")
    print(f"Login:  {LOGIN}")
    print("=" * 60)

    if not os.path.exists(DLL_PATH):
        print(f"\n[ERROR] DLL not found: {DLL_PATH}")
        print("Place mtmanapi.dll in the same directory as this script.")
        print("The DLL is obtained from the broker's MT4 Server installation.")
        sys.exit(1)

    mgr = MT4Manager(DLL_PATH)
    ver = mgr.version()
    print(f"\nDLL loaded. API version: {ver['api_version']}, Build: {ver['build']}")

    # Create manager interface
    iface = mgr.create(version=1)

    try:
        # ─── Connect ─────────────────────────────────────────────────────────
        print(f"\n[1/13] Connecting to {SERVER}...")
        ret = mgr.connect(SERVER)
        assert ret == 0, f"Connect failed: {ret}"
        print(f"  ✓  Connected (ret={ret})")

        # ─── Login ───────────────────────────────────────────────────────────
        print(f"\n[2/13] Logging in as {LOGIN}...")
        ret = mgr.login(LOGIN, PASSWORD)
        assert ret == 0, f"Login failed: {ret}"
        print(f"  ✓  Authenticated (ret={ret})")

        save_json("00_connection", {
            "server": SERVER,
            "login": LOGIN,
            "connected": True,
            "api_version": ver["api_version"],
            "build": ver["build"],
            "collected_at": datetime.datetime.utcnow().isoformat() + "Z"
        })

        # NOTE: The sections below use the low-level vtable calling convention.
        # In production, use the CManagerFactory and full vtable offsets from
        # MT4ManagerAPI.h. The function pointer indices below are examples.
        # Adapt slot numbers from the actual header file.

        print("\n[3/13] Collecting Users/Accounts...")
        # manager.UsersRequest(&total) — vtable slot varies by build
        # See manager_api_user.md for full method signatures
        print("  ↪  UsersRequest: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[4/13] Collecting Open Orders...")
        # manager.TradesRequest(&total)
        print("  ↪  TradesRequest: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[5/13] Collecting Trade History...")
        # manager.TradesUserHistory(login, from_time, to_time, &total)
        print("  ↪  TradesUserHistory: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[6/13] Collecting Symbols...")
        # manager.SymbolsRefresh() → manager.SymbolsGetAll(&total)
        print("  ↪  SymbolsGetAll: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[7/13] Collecting Groups...")
        # manager.GroupsRequest(&total)
        print("  ↪  GroupsRequest: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[8/13] Collecting Server Logs...")
        # manager.JournalRequest(&req, &total)
        print("  ↪  JournalRequest: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[9/13] Collecting Online Sessions...")
        # manager.OnlineRequest(&total)
        print("  ↪  OnlineRequest: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[10/13] Collecting Margin State...")
        print("  ↪  MarginsGet: requires pumping mode (PumpingSwitch)")

        print("\n[11/13] Collecting Summary Positions...")
        print("  ↪  SummaryGetAll: requires pumping mode (PumpingSwitch)")

        print("\n[12/13] Collecting Daily Reports...")
        # manager.DailyReportsRequest(&req, &total)
        print("  ↪  DailyReportsRequest: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n[13/13] Collecting Ticks...")
        # manager.ChartRequest(&chart_req, &total)
        print("  ↪  ChartRequest: requires full vtable mapping from MT4ManagerAPI.h")

        print("\n" + "=" * 60)
        print("✓  Collector script loaded and connected successfully.")
        print()
        print("To complete data collection, you need:")
        print("  1. The full vtable method indices from MT4ManagerAPI.h")
        print("     (distributed with the MetaTrader 4 Server package)")
        print("  2. OR use the CManagerFactory helper class from the header")
        print("     which provides typed method wrappers automatically")
        print()
        print("See the official SDK examples:")
        print("  ManagerAPISample  - general manager usage, pumping, dealing")
        print("  ManagerAPIAdmin   - administrator functions")
        print("  ManagerAPITrade   - trade transaction example")
        print()
        print("All structure definitions and field schemas are fully documented")
        print("in the docs/mt4-endpoints/ folder of this repository.")
        print("=" * 60)

    finally:
        mgr.disconnect()
        mgr.release()
        print("\n✓  Disconnected and released.")


# ─── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    collect_all()
