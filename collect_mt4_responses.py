"""
MT4 Manager API - Complete Python ctypes Wrapper & Endpoint Explorer
=====================================================================
Server : 88.218.200.140:443
Login  : 52
Pass   : Vista1234$

REQUIRES: mtmanapi64.dll (64-bit Python) OR mtmanapi.dll (32-bit Python)
  - Download from: https://developers.metaquotes.net  (MT4 Manager API SDK)
  - Place DLL in the same directory as this script, or in a PATH directory.

WHY DLL IS REQUIRED:
  The MT4 Manager API uses a proprietary binary TCP protocol with RSA
  authentication. Unlike MT5Manager (which is a pure Python pip package),
  MT4 only provides a native C++ DLL. Python communicates with it via ctypes.

USAGE:
  python collect_mt4_responses.py

  On first run it will check for the DLL and print all available fields
  from each endpoint into docs/mt4-endpoints/.
"""

import ctypes
import ctypes.wintypes
import os
import sys
import time
import json
import datetime
import struct
import socket

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SERVER   = "88.218.200.140:443"
LOGIN    = 52
PASSWORD = "Vista1234$"

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "docs", "mt4-endpoints")
os.makedirs(DOCS_DIR, exist_ok=True)

DLL_NAME_64 = "mtmanapi64.dll"
DLL_NAME_32 = "mtmanapi.dll"

# ---------------------------------------------------------------------------
# ctypes Structure Definitions  (from MT4ManagerAPI.h)
# ---------------------------------------------------------------------------

class ConSessions(ctypes.Structure):
    _pack_ = 1
    _fields_ = [("open",  ctypes.c_uint),
                ("close", ctypes.c_uint)]


class ConGroupMargin(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",              ctypes.c_char * 16),
        ("swap_long",           ctypes.c_double),
        ("swap_short",          ctypes.c_double),
        ("margin_divider",      ctypes.c_double),
        ("commission_base",     ctypes.c_double),
        ("commission_type",     ctypes.c_int),
        ("commission_lots",     ctypes.c_double),
        ("commission_agent",    ctypes.c_double),
        ("commission_agent_type", ctypes.c_int),
        ("spread_diff",         ctypes.c_int),
        ("lot_min",             ctypes.c_int),
        ("lot_max",             ctypes.c_int),
        ("lot_step",            ctypes.c_int),
        ("ie_deviation",        ctypes.c_int),
        ("confirmation",        ctypes.c_int),
        ("trade",               ctypes.c_int),
        ("execution_mode",      ctypes.c_int),
        ("acc_type",            ctypes.c_int),
        ("hedge_large_leg",     ctypes.c_int),
        ("reserved",            ctypes.c_int * 5),
    ]


class ConGroup(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("group",               ctypes.c_char * 16),
        ("newspaper",           ctypes.c_char * 48),
        ("mail_enable",         ctypes.c_int),
        ("enable_change_password", ctypes.c_int),
        ("enable_read_only",    ctypes.c_int),
        ("enable_send_reports", ctypes.c_int),
        ("report_mode",         ctypes.c_int),
        ("default_leverage",    ctypes.c_int),
        ("default_deposit",     ctypes.c_double),
        ("max_symbols",         ctypes.c_int),
        ("currency",            ctypes.c_char * 16),
        ("price_type",          ctypes.c_int),
        ("tax",                 ctypes.c_double),
        ("interest_rate",       ctypes.c_double),
        ("timeout",             ctypes.c_int),
        ("trading",             ctypes.c_int),
        ("balance_min",         ctypes.c_double),
        ("stopping_level",      ctypes.c_int),
        ("loss_limit",          ctypes.c_int),
        ("margin_call",         ctypes.c_int),
        ("margin_mode",         ctypes.c_int),
        ("margin_type",         ctypes.c_int),
        ("archive_max_balance", ctypes.c_double),
        ("archive_pending_period", ctypes.c_int),
        ("archive_period",      ctypes.c_int),
        ("commission_base",     ctypes.c_double),
        ("commission_type",     ctypes.c_int),
        ("commission_lots",     ctypes.c_double),
        ("commission_agent",    ctypes.c_double),
        ("commission_agent_type", ctypes.c_int),
        ("free_margin_mode",    ctypes.c_int),
        ("transfer_mode",       ctypes.c_int),
        ("transfer_max_money",  ctypes.c_double),
        ("otp_mode",            ctypes.c_int),
        ("activate",            ctypes.c_int),
        ("close_reopen",        ctypes.c_int),
        ("hedge_prohibited",    ctypes.c_int),
        ("close_fifo",          ctypes.c_int),
        ("hedge_large_leg",     ctypes.c_int),
        ("reserved",            ctypes.c_int * 2),
        ("securities",          ConGroupMargin * 128),
    ]


class UserRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("login",                   ctypes.c_int),
        ("group",                   ctypes.c_char * 16),
        ("password",                ctypes.c_char * 16),
        ("enable",                  ctypes.c_int),
        ("enable_change_password",  ctypes.c_int),
        ("enable_read_only",        ctypes.c_int),
        ("enable_send_reports",     ctypes.c_int),
        ("password_phone",          ctypes.c_char * 16),
        ("name",                    ctypes.c_char * 64),
        ("country",                 ctypes.c_char * 64),
        ("city",                    ctypes.c_char * 64),
        ("state",                   ctypes.c_char * 64),
        ("zipcode",                 ctypes.c_char * 16),
        ("address",                 ctypes.c_char * 128),
        ("phone",                   ctypes.c_char * 32),
        ("email",                   ctypes.c_char * 48),
        ("comment",                 ctypes.c_char * 64),
        ("id",                      ctypes.c_char * 32),
        ("status",                  ctypes.c_char * 16),
        ("regdate",                 ctypes.c_int),
        ("lastdate",                ctypes.c_int),
        ("leverage",                ctypes.c_int),
        ("agent_account",           ctypes.c_int),
        ("timestamp",               ctypes.c_int),
        ("last_ip",                 ctypes.c_uint),
        ("balance",                 ctypes.c_double),
        ("prevmonthbalance",        ctypes.c_double),
        ("prevbalance",             ctypes.c_double),
        ("credit",                  ctypes.c_double),
        ("interestrate",            ctypes.c_double),
        ("taxes",                   ctypes.c_double),
        ("prevmonthequity",         ctypes.c_double),
        ("prevequity",              ctypes.c_double),
        ("reserved2",               ctypes.c_double * 2),
        ("margin_level",            ctypes.c_double),
        ("send_reports",            ctypes.c_int),
        ("mqid",                    ctypes.c_char * 32),
        ("user_color",              ctypes.c_uint),
        ("reserved",                ctypes.c_double * 5),
    ]


class TradeRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("order",            ctypes.c_int),
        ("login",            ctypes.c_int),
        ("symbol",           ctypes.c_char * 12),
        ("digits",           ctypes.c_int),
        ("cmd",              ctypes.c_int),
        ("volume",           ctypes.c_int),
        ("open_time",        ctypes.c_int),
        ("state",            ctypes.c_int),
        ("open_price",       ctypes.c_double),
        ("sl",               ctypes.c_double),
        ("tp",               ctypes.c_double),
        ("close_time",       ctypes.c_int),
        ("value_date",       ctypes.c_int),
        ("expiration",       ctypes.c_int),
        ("reason",           ctypes.c_int),
        ("conv_rates",       ctypes.c_double * 2),
        ("commission",       ctypes.c_double),
        ("commission_agent", ctypes.c_double),
        ("storage",          ctypes.c_double),
        ("close_price",      ctypes.c_double),
        ("profit",           ctypes.c_double),
        ("taxes",            ctypes.c_double),
        ("magic",            ctypes.c_int),
        ("comment",          ctypes.c_char * 32),
        ("margin_rate",      ctypes.c_double),
        ("timestamp",        ctypes.c_int),
        ("reserved",         ctypes.c_uint * 4),
    ]


class MarginLevel(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("login",               ctypes.c_int),
        ("group",               ctypes.c_char * 16),
        ("balance",             ctypes.c_double),
        ("equity",              ctypes.c_double),
        ("margin",              ctypes.c_double),
        ("margin_free",         ctypes.c_double),
        ("margin_level",        ctypes.c_double),
        ("margin_initial",      ctypes.c_double),
        ("margin_maintenance",  ctypes.c_double),
        ("profit_loss",         ctypes.c_double),
        ("assets",              ctypes.c_double),
        ("liabilities",         ctypes.c_double),
        ("floating",            ctypes.c_double),
    ]


class OnlineRecord(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("login",       ctypes.c_int),
        ("group",       ctypes.c_char * 16),
        ("ip",          ctypes.c_uint),
        ("login_time",  ctypes.c_int),
        ("last_access", ctypes.c_int),
        ("agent",       ctypes.c_char * 32),
        ("version",     ctypes.c_int),
        ("reserved",    ctypes.c_char * 28),
    ]


class SymbolInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",        ctypes.c_char * 12),
        ("digits",        ctypes.c_int),
        ("spread",        ctypes.c_int),
        ("spread_float",  ctypes.c_int),
        ("direction",     ctypes.c_int),
        ("bid",           ctypes.c_double),
        ("ask",           ctypes.c_double),
        ("session_price", ctypes.c_double),
        ("high",          ctypes.c_double),
        ("low",           ctypes.c_double),
        ("time",          ctypes.c_int),
        ("reserved",      ctypes.c_int * 8),
    ]


class SymbolSummary(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",      ctypes.c_char * 12),
        ("count",       ctypes.c_int),
        ("volume",      ctypes.c_int),
        ("volume_buy",  ctypes.c_int),
        ("volume_sell", ctypes.c_int),
        ("profit",      ctypes.c_double),
        ("hedged",      ctypes.c_int),
        ("hedged_buy",  ctypes.c_double),
        ("hedged_sell", ctypes.c_double),
        ("reserved",    ctypes.c_int * 4),
    ]


class ExposureValue(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("cur_name",      ctypes.c_char * 16),
        ("client_assets", ctypes.c_double),
        ("hedged_assets", ctypes.c_double),
        ("rate_deposit",  ctypes.c_double),
        ("reserved",      ctypes.c_int * 4),
    ]


class RateInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",   ctypes.c_int),
        ("open",  ctypes.c_double),
        ("high",  ctypes.c_double),
        ("low",   ctypes.c_double),
        ("close", ctypes.c_double),
        ("vol",   ctypes.c_double),
    ]


class TickAPI(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm", ctypes.c_int),
        ("bid", ctypes.c_double),
        ("ask", ctypes.c_double),
    ]


class TickInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol", ctypes.c_char * 12),
        ("ctm",    ctypes.c_int),
        ("bid",    ctypes.c_double),
        ("ask",    ctypes.c_double),
    ]


class DailyReport(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",          ctypes.c_int),
        ("login",        ctypes.c_int),
        ("group",        ctypes.c_char * 16),
        ("name",         ctypes.c_char * 64),
        ("balance",      ctypes.c_double),
        ("prev_balance", ctypes.c_double),
        ("equity",       ctypes.c_double),
        ("margin",       ctypes.c_double),
        ("margin_free",  ctypes.c_double),
        ("margin_level", ctypes.c_double),
        ("profit",       ctypes.c_double),
        ("credit",       ctypes.c_double),
        ("floating",     ctypes.c_double),
        ("reserved",     ctypes.c_int * 8),
    ]


class TradeTransInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("type",        ctypes.c_int),
        ("flags",       ctypes.c_int),
        ("cmd",         ctypes.c_int),
        ("order",       ctypes.c_int),
        ("orderby",     ctypes.c_int),
        ("login",       ctypes.c_int),
        ("symbol",      ctypes.c_char * 12),
        ("volume",      ctypes.c_int),
        ("price",       ctypes.c_double),
        ("sl",          ctypes.c_double),
        ("tp",          ctypes.c_double),
        ("ie_deviation",ctypes.c_int),
        ("comment",     ctypes.c_char * 32),
        ("expiration",  ctypes.c_int),
        ("magic",       ctypes.c_int),
        ("reserved",    ctypes.c_int * 2),
    ]


class LogInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("ctm",     ctypes.c_int),
        ("type",    ctypes.c_int),
        ("message", ctypes.c_char * 512),
    ]


class MailBoxHeader(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("subject",  ctypes.c_char * 128),
        ("from_id",  ctypes.c_char * 16),
        ("to",       ctypes.c_char * 128),
        ("date",     ctypes.c_int),
        ("key",      ctypes.c_uint),
        ("reserved", ctypes.c_int * 4),
    ]


class NewsTopic(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("key",      ctypes.c_uint),
        ("time",     ctypes.c_int),
        ("topic",    ctypes.c_char * 128),
        ("category", ctypes.c_char * 32),
        ("reserved", ctypes.c_int * 4),
    ]


class ChartInfo(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",   ctypes.c_char * 12),
        ("period",   ctypes.c_int),
        ("timesign", ctypes.c_int),
        ("count",    ctypes.c_int),
    ]


class TickRequest(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("symbol",    ctypes.c_char * 12),
        ("from_time", ctypes.c_int),
        ("to_time",   ctypes.c_int),
        ("reserved",  ctypes.c_int * 4),
    ]


# ---------------------------------------------------------------------------
# CManagerInterface vtable wrapper
# Wraps the COM-style vtable returned by MtManCreate
# ---------------------------------------------------------------------------

class CManagerInterface:
    """
    Python wrapper around the CManagerInterface COM-style vtable.
    Vtable offsets are based on MT4ManagerAPI.h (build 1353).
    """

    def __init__(self, ptr, dll):
        self._ptr   = ptr
        self._dll   = dll
        self._vt    = ctypes.cast(
            ctypes.cast(ptr, ctypes.POINTER(ctypes.c_void_p))[0],
            ctypes.POINTER(ctypes.c_void_p)
        )

    def _fn(self, idx, restype, *argtypes):
        """Get vtable function at index idx."""
        fn_ptr = self._vt[idx]
        fn     = ctypes.cast(fn_ptr, ctypes.WINFUNCTYPE(restype, ctypes.c_void_p, *argtypes))
        return fn

    # -- Common ---------------------------------------------------------------
    def Release(self):
        return self._fn(2, ctypes.c_uint)(self._ptr)

    def MemFree(self, ptr):
        self._fn(5, None, ctypes.c_void_p)(self._ptr, ptr)

    def ErrorDescription(self, code):
        fn = self._fn(6, ctypes.c_char_p, ctypes.c_int)
        return fn(self._ptr, code)

    def WorkingDirectory(self, path):
        fn = self._fn(7, ctypes.c_int, ctypes.c_char_p)
        return fn(self._ptr, path.encode() if isinstance(path, str) else path)

    def IsConnected(self):
        return self._fn(9, ctypes.c_int)(self._ptr)

    def BytesSent(self):
        return self._fn(10, ctypes.c_int)(self._ptr)

    def BytesReceived(self):
        return self._fn(11, ctypes.c_int)(self._ptr)

    # -- Connection -----------------------------------------------------------
    def Connect(self, server):
        fn = self._fn(16, ctypes.c_int, ctypes.c_char_p)
        return fn(self._ptr, server.encode() if isinstance(server, str) else server)

    def Disconnect(self):
        self._fn(17, None)(self._ptr)

    def Login(self, login, password):
        fn = self._fn(19, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
        return fn(self._ptr, login,
                  password.encode() if isinstance(password, str) else password)

    def PasswordChange(self, password, is_investor):
        fn = self._fn(22, ctypes.c_int, ctypes.c_char_p, ctypes.c_int)
        return fn(self._ptr,
                  password.encode() if isinstance(password, str) else password,
                  is_investor)

    def Ping(self):
        return self._fn(23, ctypes.c_int)(self._ptr)

    def ServerTime(self):
        return self._fn(24, ctypes.c_int)(self._ptr)

    # -- Users ----------------------------------------------------------------
    def UsersRequest(self, group="*"):
        fn  = self._fn(64, ctypes.c_void_p, ctypes.c_char_p, ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr,
                 group.encode() if isinstance(group, str) else group,
                 ctypes.byref(tot))
        return ptr, tot.value

    def UserRecordGet(self, login):
        fn  = self._fn(65, ctypes.c_int, ctypes.c_int, ctypes.POINTER(UserRecord))
        rec = UserRecord()
        ret = fn(self._ptr, login, ctypes.byref(rec))
        return rec if ret == 0 else None

    def UserRecordNew(self, info):
        fn = self._fn(68, ctypes.c_int, ctypes.POINTER(UserRecord))
        return fn(self._ptr, ctypes.byref(info))

    def UserRecordUpdate(self, info):
        fn = self._fn(69, ctypes.c_int, ctypes.POINTER(UserRecord))
        return fn(self._ptr, ctypes.byref(info))

    def UserPasswordCheck(self, login, password):
        fn = self._fn(71, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
        return fn(self._ptr, login,
                  password.encode() if isinstance(password, str) else password)

    def UserPasswordSet(self, login, pass_type, password):
        fn = self._fn(72, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p)
        return fn(self._ptr, login, pass_type,
                  password.encode() if isinstance(password, str) else password)

    # -- Online ---------------------------------------------------------------
    def OnlineRequest(self):
        fn  = self._fn(80, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, ctypes.byref(tot))
        return ptr, tot.value

    def OnlineRecordGet(self, login):
        fn  = self._fn(81, ctypes.c_int, ctypes.c_int, ctypes.POINTER(OnlineRecord))
        rec = OnlineRecord()
        ret = fn(self._ptr, login, ctypes.byref(rec))
        return rec if ret == 0 else None

    # -- Trades ---------------------------------------------------------------
    def TradesUserHistory(self, login, from_time, to_time):
        fn  = self._fn(96, ctypes.c_void_p,
                       ctypes.c_int, ctypes.c_int, ctypes.c_int,
                       ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, login, from_time, to_time, ctypes.byref(tot))
        return ptr, tot.value

    def TradeTransaction(self, trans):
        fn  = self._fn(101, ctypes.c_int,
                       ctypes.POINTER(TradeTransInfo),
                       ctypes.c_void_p,
                       ctypes.POINTER(ctypes.c_int))
        cnt = ctypes.c_int(0)
        return fn(self._ptr, ctypes.byref(trans), None, ctypes.byref(cnt))

    # -- Margin ---------------------------------------------------------------
    def MarginLevelGet(self, login):
        fn  = self._fn(112, ctypes.c_int, ctypes.c_int, ctypes.POINTER(MarginLevel))
        ml  = MarginLevel()
        ret = fn(self._ptr, login, ctypes.byref(ml))
        return ml if ret == 0 else None

    # -- Reports --------------------------------------------------------------
    def ReportsRequest(self, from_time, to_time, login=0):
        fn  = self._fn(128, ctypes.c_void_p,
                       ctypes.c_int, ctypes.c_int, ctypes.c_int,
                       ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, from_time, to_time, login, ctypes.byref(tot))
        return ptr, tot.value

    # -- Symbols --------------------------------------------------------------
    def SymbolsRefresh(self):
        return self._fn(144, ctypes.c_int)(self._ptr)

    def SymbolInfoGet(self, symbol):
        fn  = self._fn(148, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(SymbolInfo))
        si  = SymbolInfo()
        sym = symbol.encode() if isinstance(symbol, str) else symbol
        ret = fn(self._ptr, sym, ctypes.byref(si))
        return si if ret == 0 else None

    # -- Summary / Exposure ---------------------------------------------------
    def SummaryGetAll(self):
        fn  = self._fn(160, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, ctypes.byref(tot))
        return ptr, tot.value

    def SummaryGet(self, symbol):
        fn  = self._fn(161, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(SymbolSummary))
        ss  = SymbolSummary()
        sym = symbol.encode() if isinstance(symbol, str) else symbol
        ret = fn(self._ptr, sym, ctypes.byref(ss))
        return ss if ret == 0 else None

    def ExposureGet(self):
        fn  = self._fn(176, ctypes.c_void_p, ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, ctypes.byref(tot))
        return ptr, tot.value

    # -- Chart / Ticks --------------------------------------------------------
    def ChartRequest(self, symbol, period, from_time, count=2000):
        req          = ChartInfo()
        req.symbol   = symbol.encode()[:11] if isinstance(symbol, str) else symbol[:11]
        req.period   = period
        req.timesign = from_time
        req.count    = count
        fn  = self._fn(192, ctypes.c_void_p,
                       ctypes.POINTER(ChartInfo), ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, ctypes.byref(req), ctypes.byref(tot))
        return ptr, tot.value

    def TicksRequest(self, symbol, from_time, to_time):
        req           = TickRequest()
        req.symbol    = symbol.encode()[:11] if isinstance(symbol, str) else symbol[:11]
        req.from_time = from_time
        req.to_time   = to_time
        fn  = self._fn(195, ctypes.c_void_p,
                       ctypes.POINTER(TickRequest), ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, ctypes.byref(req), ctypes.byref(tot))
        return ptr, tot.value

    def ServerTimeGet(self):
        return self._fn(24, ctypes.c_int)(self._ptr)

    def JournalRequest(self, from_time, to_time):
        fn  = self._fn(209, ctypes.c_void_p,
                       ctypes.c_int, ctypes.c_int,
                       ctypes.POINTER(ctypes.c_int))
        tot = ctypes.c_int(0)
        ptr = fn(self._ptr, from_time, to_time, ctypes.byref(tot))
        return ptr, tot.value


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def struct_to_dict(obj):
    """Convert a ctypes Structure to a plain Python dict."""
    result = {}
    for name, typ in obj._fields_:
        try:
            val = getattr(obj, name)
            if isinstance(val, bytes):
                val = val.rstrip(b'\x00').decode('utf-8', errors='replace')
            elif hasattr(val, '_length_') and hasattr(val, '_type_'):
                val = list(val)  # ctypes array
            elif isinstance(val, (int, float, bool)):
                pass
            else:
                val = str(val)
            result[name] = val
        except Exception:
            pass
    return result


def array_to_dicts(ptr, count, struct_type):
    """Convert a ctypes pointer+count into a list of dicts."""
    if not ptr or count == 0:
        return []
    arr = ctypes.cast(ptr, ctypes.POINTER(struct_type * count)).contents
    return [struct_to_dict(arr[i]) for i in range(count)]


def uint_to_ip(packed):
    try:
        return socket.inet_ntoa(struct.pack('<I', packed))
    except Exception:
        return str(packed)


def ts_to_str(ts):
    if ts and ts > 0:
        try:
            return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')
        except Exception:
            pass
    return str(ts)


# ---------------------------------------------------------------------------
# Documentation helpers
# ---------------------------------------------------------------------------

def field_table(sample: dict) -> str:
    if not sample:
        return "_No live data — structure fields from MT4ManagerAPI.h_\n"
    lines = ["| Field | Type | Example Value |",
             "|-------|------|---------------|"]
    for k, v in sample.items():
        typ = type(v).__name__
        val = str(v)
        if len(val) > 120:
            val = val[:117] + "..."
        val = val.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| `{k}` | {typ} | `{val}` |")
    return "\n".join(lines) + "\n"


def write_doc(filename: str, title: str, method: str, description: str,
              code: str, sample: dict, error: str = None):
    ts   = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    path = os.path.join(DOCS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"> Captured: {ts} | Server: `{SERVER}`\n\n---\n\n")
        f.write("## Endpoint Details\n\n")
        f.write("| Property | Value |\n|----------|-------|\n")
        f.write(f"| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |\n")
        f.write(f"| **Method** | `{method}` |\n\n")
        f.write("## Example Code\n\n```python\n")
        f.write(code.strip())
        f.write("\n```\n\n## Response Fields\n\n")
        if error:
            f.write(f"> **Note:** `{error}`\n\n")
        f.write(field_table(sample))
        if sample:
            f.write("\n## Raw Sample\n\n```json\n")
            f.write(json.dumps(sample, indent=2, default=str)[:3000])
            f.write("\n```\n")
    print(f"  [OK] {filename}")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main():
    # -- Check for DLL -------------------------------------------------------
    dll_path = None
    for candidate in [DLL_NAME_64, DLL_NAME_32,
                      os.path.join(os.path.dirname(__file__), DLL_NAME_64),
                      os.path.join(os.path.dirname(__file__), DLL_NAME_32)]:
        if os.path.exists(candidate):
            dll_path = candidate
            break

    if dll_path is None:
        print("=" * 60)
        print("DLL NOT FOUND")
        print("=" * 60)
        print(f"Searched for: {DLL_NAME_64}, {DLL_NAME_32}")
        print()
        print("The MT4 Manager API requires the native C++ DLL.")
        print("To get it:")
        print("  1. Register at https://developers.metaquotes.net")
        print("  2. Download 'MetaTrader 4 Manager API SDK'")
        print(f"  3. Place {DLL_NAME_64} (64-bit) or {DLL_NAME_32} (32-bit)")
        print("     in the same directory as this script")
        print()
        print("Generating documentation from official MT4ManagerAPI.h")
        print("structure definitions (no live data)...")
        print()
        generate_docs_from_headers()
        return

    # -- Load DLL and connect ------------------------------------------------
    print(f"Loading {dll_path}...")
    try:
        raw_dll = ctypes.WinDLL(dll_path)
    except OSError as e:
        print(f"Failed to load DLL: {e}")
        generate_docs_from_headers()
        return

    raw_dll.MtManCreate.restype  = ctypes.c_void_p
    raw_dll.MtManCreate.argtypes = [ctypes.c_uint]
    raw_dll.MtManVersion.restype  = ctypes.c_uint

    ver   = raw_dll.MtManVersion()
    major = (ver >> 16) & 0xFFFF
    build = ver & 0xFFFF
    print(f"DLL version: {major}, build: {build}")

    ptr = raw_dll.MtManCreate(0x0001)
    if not ptr:
        print("MtManCreate returned NULL")
        return

    mgr = CManagerInterface(ptr, raw_dll)

    print(f"Connecting to {SERVER}...")
    if mgr.Connect(SERVER) != 0:
        print(f"Connect failed")
        mgr.Release()
        return

    print(f"Logging in as {LOGIN}...")
    if mgr.Login(LOGIN, PASSWORD) != 0:
        print("Login failed")
        mgr.Disconnect()
        mgr.Release()
        return

    print("Connected!\n")

    now      = int(time.time())
    from_90d = now - 90 * 86400
    from_30d = now - 30 * 86400
    from_1d  = now - 86400

    # -- Server Time ---------------------------------------------------------
    print("-- ServerTime --")
    srv_time = mgr.ServerTimeGet()
    write_doc("00_server_time.md",
              title="ServerTime - Get Current Server Time",
              method="manager->ServerTime() -> time_t (int)",
              description="Returns the current Unix timestamp from the trade server.",
              code=f"""srv_time = manager->ServerTime()
print(f"Server time: {{time.ctime(srv_time)}}")
""",
              sample={"server_time_unix": srv_time,
                      "server_time_utc": ts_to_str(srv_time)})

    # -- UsersRequest --------------------------------------------------------
    print("-- UsersRequest --")
    ptr_u, cnt_u = mgr.UsersRequest("*")
    users = array_to_dicts(ptr_u, cnt_u, UserRecord)
    if ptr_u: mgr.MemFree(ctypes.c_void_p(ptr_u))
    sample_user = users[0] if users else {}
    print(f"   UsersRequest(*) -> {cnt_u} users")
    write_doc("02_user_record_live.md",
              title="UsersRequest - Retrieve All User Records (LIVE)",
              method="manager->UsersRequest(group, *total) -> UserRecord*",
              description=f"Fetched {cnt_u} user records from the server.",
              code=f"""total = ctypes.c_int(0)
ptr = manager->UsersRequest("*", &total)
users = cast_array(ptr, total.value, UserRecord)
manager->MemFree(ptr)
""",
              sample=sample_user)

    # -- UserRecordGet (single) ----------------------------------------------
    print("-- UserRecordGet --")
    user_one = mgr.UserRecordGet(LOGIN)
    sample_u1 = struct_to_dict(user_one) if user_one else {}
    write_doc("02b_user_record_get_live.md",
              title="UserRecordGet - Single User in Pumping Mode (LIVE)",
              method="manager->UserRecordGet(login, *info) -> int",
              description=f"Retrieved user record for login {LOGIN}.",
              code=f"""user = UserRecord()
ret = manager->UserRecordGet({LOGIN}, &user)
print(user.login, user.name, user.balance, user.equity)
""",
              sample=sample_u1)

    # -- OnlineRequest -------------------------------------------------------
    print("-- OnlineRequest --")
    ptr_o, cnt_o = mgr.OnlineRequest()
    online = array_to_dicts(ptr_o, cnt_o, OnlineRecord)
    if ptr_o: mgr.MemFree(ctypes.c_void_p(ptr_o))
    sample_online = online[0] if online else {}
    if sample_online.get("ip"):
        sample_online["ip_decoded"] = uint_to_ip(online[0].get("ip", 0)
                                                 if isinstance(online[0].get("ip"), int)
                                                 else 0)
    print(f"   OnlineRequest -> {cnt_o} connections")
    write_doc("05_online_record_live.md",
              title="OnlineRequest - Currently Connected Clients (LIVE)",
              method="manager->OnlineRequest(*total) -> OnlineRecord*",
              description=f"Retrieved {cnt_o} active connections.",
              code="""total = ctypes.c_int(0)
ptr = manager->OnlineRequest(&total)
online = cast_array(ptr, total.value, OnlineRecord)
for r in online:
    print(r.login, r.ip, r.agent, r.version)
manager->MemFree(ptr)
""",
              sample=sample_online)

    # -- Trade History -------------------------------------------------------
    print("-- TradesUserHistory --")
    ptr_t, cnt_t = mgr.TradesUserHistory(LOGIN, from_90d, now)
    trades = array_to_dicts(ptr_t, cnt_t, TradeRecord)
    if ptr_t: mgr.MemFree(ctypes.c_void_p(ptr_t))
    sample_trade = trades[0] if trades else {}
    print(f"   TradesUserHistory({LOGIN}) -> {cnt_t} records")
    write_doc("03_trade_record_live.md",
              title="TradesUserHistory - Trade History for User (LIVE)",
              method="manager->TradesUserHistory(login, from, to, *total) -> TradeRecord*",
              description=f"Retrieved {cnt_t} trade records for login {LOGIN} (last 90 days).",
              code=f"""from_time = int(time.time()) - 90*86400
to_time   = int(time.time())
total = ctypes.c_int(0)
ptr = manager->TradesUserHistory({LOGIN}, from_time, to_time, &total)
trades = cast_array(ptr, total.value, TradeRecord)
for t in trades:
    print(t.order, t.symbol, t.cmd, t.volume/100, t.open_price, t.profit)
manager->MemFree(ptr)
""",
              sample=sample_trade)

    # -- MarginLevel ---------------------------------------------------------
    print("-- MarginLevelGet --")
    ml = mgr.MarginLevelGet(LOGIN)
    sample_ml = struct_to_dict(ml) if ml else {}
    write_doc("04_margin_level_live.md",
              title="MarginLevelGet - Account Margin State (LIVE)",
              method="manager->MarginLevelGet(login, *margin) -> int",
              description=f"Retrieved margin state for login {LOGIN}.",
              code=f"""ml = MarginLevel()
ret = manager->MarginLevelGet({LOGIN}, &ml)
print(ml.balance, ml.equity, ml.margin, ml.margin_free, ml.margin_level)
""",
              sample=sample_ml)

    # -- SymbolInfoGet -------------------------------------------------------
    print("-- SymbolInfoGet --")
    sym_test = "EURUSD"
    si = mgr.SymbolInfoGet(sym_test)
    sample_si = struct_to_dict(si) if si else {}
    write_doc("06_symbol_info_live.md",
              title="SymbolInfoGet - Market Watch Snapshot (LIVE)",
              method="manager->SymbolInfoGet(symbol, *info) -> int",
              description=f"Retrieved live bid/ask data for {sym_test}.",
              code=f"""info = SymbolInfo()
ret = manager->SymbolInfoGet("{sym_test}", &info)
print(info.symbol, info.bid, info.ask, info.spread, info.high, info.low)
""",
              sample=sample_si)

    # -- SummaryGet ----------------------------------------------------------
    print("-- SummaryGet --")
    ss = mgr.SummaryGet(sym_test)
    sample_ss = struct_to_dict(ss) if ss else {}
    write_doc("07_summary_live.md",
              title="SummaryGet - Symbol Position Summary (LIVE)",
              method="manager->SummaryGet(symbol, *summary) -> int",
              description=f"Retrieved aggregated position summary for {sym_test}.",
              code=f"""ss = SymbolSummary()
ret = manager->SummaryGet("{sym_test}", &ss)
print(ss.symbol, ss.count, ss.volume/100, ss.profit)
""",
              sample=sample_ss)

    # -- ChartRequest --------------------------------------------------------
    print("-- ChartRequest --")
    ptr_c, cnt_c = mgr.ChartRequest(sym_test, 60, from_30d, count=500)
    bars = array_to_dicts(ptr_c, cnt_c, RateInfo)
    if ptr_c: mgr.MemFree(ctypes.c_void_p(ptr_c))
    sample_bar = bars[0] if bars else {}
    print(f"   ChartRequest({sym_test}, H1) -> {cnt_c} bars")
    write_doc("08_chart_request_live.md",
              title="ChartRequest - OHLCV Bar History (LIVE)",
              method="manager->ChartRequest(*req, *total) -> RateInfo*",
              description=f"Retrieved {cnt_c} H1 bars for {sym_test}.",
              code=f"""req = ChartInfo()
req.symbol   = b"{sym_test}"
req.period   = 60        # H1
req.timesign = int(time.time()) - 30*86400
req.count    = 500
total = ctypes.c_int(0)
ptr = manager->ChartRequest(&req, &total)
bars = cast_array(ptr, total.value, RateInfo)
for b in bars[:5]:
    print(time.ctime(b.ctm), b.open, b.high, b.low, b.close, b.vol)
manager->MemFree(ptr)
""",
              sample=sample_bar)

    # -- TicksRequest --------------------------------------------------------
    print("-- TicksRequest --")
    ptr_tk, cnt_tk = mgr.TicksRequest(sym_test, now - 3600, now)
    ticks = array_to_dicts(ptr_tk, cnt_tk, TickAPI)
    if ptr_tk: mgr.MemFree(ctypes.c_void_p(ptr_tk))
    sample_tick = ticks[0] if ticks else {}
    print(f"   TicksRequest({sym_test}, 1h) -> {cnt_tk} ticks")
    write_doc("08b_ticks_request_live.md",
              title="TicksRequest - Raw Tick History (LIVE)",
              method="manager->TicksRequest(*req, *total) -> TickAPI*",
              description=f"Retrieved {cnt_tk} ticks for {sym_test} (last hour).",
              code=f"""req = TickRequest()
req.symbol    = b"{sym_test}"
req.from_time = int(time.time()) - 3600
req.to_time   = int(time.time())
total = ctypes.c_int(0)
ptr = manager->TicksRequest(&req, &total)
ticks = cast_array(ptr, total.value, TickAPI)
for t in ticks[:5]:
    print(time.ctime(t.ctm), t.bid, t.ask)
manager->MemFree(ptr)
""",
              sample=sample_tick)

    # -- Reports (closed positions) ------------------------------------------
    print("-- ReportsRequest --")
    ptr_r, cnt_r = mgr.ReportsRequest(from_90d, now, LOGIN)
    reports = array_to_dicts(ptr_r, cnt_r, TradeRecord)
    if ptr_r: mgr.MemFree(ctypes.c_void_p(ptr_r))
    sample_rep = reports[0] if reports else {}
    print(f"   ReportsRequest({LOGIN}) -> {cnt_r} closed positions")
    write_doc("09_reports_request_live.md",
              title="ReportsRequest - Closed Position History (LIVE)",
              method="manager->ReportsRequest(from, to, login, *total) -> TradeRecord*",
              description=f"Retrieved {cnt_r} closed positions for login {LOGIN} (last 90 days).",
              code=f"""total = ctypes.c_int(0)
ptr = manager->ReportsRequest(from_90d, now, {LOGIN}, &total)
closed = cast_array(ptr, total.value, TradeRecord)
for r in closed:
    print(r.order, r.symbol, r.open_price, r.close_price, r.profit)
manager->MemFree(ptr)
""",
              sample=sample_rep)

    # -- Journal -------------------------------------------------------------
    print("-- JournalRequest --")
    ptr_j, cnt_j = mgr.JournalRequest(from_1d, now)
    logs = array_to_dicts(ptr_j, cnt_j, LogInfo)
    if ptr_j: mgr.MemFree(ctypes.c_void_p(ptr_j))
    sample_log = logs[0] if logs else {}
    print(f"   JournalRequest (24h) -> {cnt_j} log entries")
    write_doc("12_journal_request_live.md",
              title="JournalRequest - Server Journal/Log Entries (LIVE)",
              method="manager->JournalRequest(from, to, *total) -> LogInfo*",
              description=f"Retrieved {cnt_j} log entries from the last 24 hours.",
              code="""total = ctypes.c_int(0)
from_time = int(time.time()) - 86400
ptr = manager->JournalRequest(from_time, int(time.time()), &total)
logs = cast_array(ptr, total.value, LogInfo)
for log in logs[:10]:
    print(log.ctm, log.type, log.message.decode())
manager->MemFree(ptr)
""",
              sample=sample_log)

    mgr.Disconnect()
    mgr.Release()
    print(f"\nDone! Docs: {DOCS_DIR}")
    print(f"Files: {len(os.listdir(DOCS_DIR))}")


def generate_docs_from_headers():
    """Generate docs from MT4ManagerAPI.h definitions when DLL is unavailable."""
    print("Generating structure-based docs (no live data)...")

    # Representative samples from official header definitions
    samples = {
        "UserRecord": {
            "login": 52, "group": "real\\managers", "enable": 1,
            "name": "John Doe", "country": "Iran", "city": "Tehran",
            "email": "client@example.com", "leverage": 100,
            "balance": 10000.00, "credit": 0.0, "prevmonthbalance": 9500.0,
            "prevbalance": 9900.0, "interestrate": 0.0, "taxes": 0.0,
            "regdate": 1700000000, "lastdate": 1700100000,
            "last_ip": 3232235520, "agent_account": 0,
            "enable_change_password": 1, "enable_read_only": 0,
            "send_reports": 1, "margin_level": 0.0
        },
        "TradeRecord": {
            "order": 123456, "login": 52, "symbol": "EURUSD", "digits": 5,
            "cmd": 0, "volume": 100, "open_time": 1700000000, "state": 0,
            "open_price": 1.08500, "sl": 1.08000, "tp": 1.09000,
            "close_time": 0, "expiration": 0, "reason": 0,
            "commission": -2.50, "commission_agent": 0.0,
            "storage": -0.50, "close_price": 1.08750,
            "profit": 250.00, "taxes": 0.0, "magic": 0,
            "comment": "manual", "margin_rate": 1.0,
            "timestamp": 1700100000
        },
        "MarginLevel": {
            "login": 52, "group": "real\\managers",
            "balance": 10000.0, "equity": 10250.0,
            "margin": 500.0, "margin_free": 9750.0,
            "margin_level": 2050.0, "margin_initial": 500.0,
            "margin_maintenance": 250.0, "profit_loss": 250.0,
            "assets": 10250.0, "liabilities": 0.0, "floating": 250.0
        },
        "OnlineRecord": {
            "login": 52, "group": "real\\managers",
            "ip": 3232235520, "login_time": 1700100000,
            "last_access": 1700100060, "agent": "MetaTrader 4",
            "version": 1360
        },
        "SymbolInfo": {
            "symbol": "EURUSD", "digits": 5, "spread": 10,
            "spread_float": 1, "bid": 1.08450, "ask": 1.08460,
            "session_price": 1.08300, "high": 1.08600,
            "low": 1.08100, "time": 1700100000
        },
        "RateInfo": {
            "ctm": 1700100000, "open": 1.08450,
            "high": 1.08620, "low": 1.08380,
            "close": 1.08550, "vol": 1523.0
        },
        "TickAPI": {
            "ctm": 1700100001, "bid": 1.08450, "ask": 1.08460
        },
        "DailyReport": {
            "ctm": 1700100000, "login": 52,
            "group": "real\\managers", "name": "John Doe",
            "balance": 10250.0, "prev_balance": 10000.0,
            "equity": 10500.0, "margin": 500.0,
            "margin_free": 10000.0, "margin_level": 2100.0,
            "profit": 250.0, "credit": 0.0, "floating": 250.0
        },
        "SymbolSummary": {
            "symbol": "EURUSD", "count": 42, "volume": 5000,
            "volume_buy": 3000, "volume_sell": 2000,
            "profit": 1250.50, "hedged": 1000,
            "hedged_buy": 1000.0, "hedged_sell": 0.0
        },
        "ExposureValue": {
            "cur_name": "USD", "client_assets": 2500000.0,
            "hedged_assets": 500000.0, "rate_deposit": 1.0
        },
        "LogInfo": {
            "ctm": 1700100000, "type": 0,
            "message": "Login: 52 from 1.2.3.4 MetaTrader 4"
        },
    }

    entries = [
        ("00_server_time.md", "ServerTime - Get Current Server Time",
         "manager->ServerTime() -> time_t",
         "Returns current Unix timestamp from the trade server.",
         f"""srv_time = manager->ServerTime()
print(f"Server UTC: {{time.ctime(srv_time)}}")
""", {"server_time_unix": 1700100000, "server_time_utc": "2023-11-15 12:00:00 UTC"}),

        ("02_user_record_live.md", "UsersRequest - All User Records",
         "manager->UsersRequest(group, *total) -> UserRecord*",
         "Get all client account records matching a group mask.",
         """total = ctypes.c_int(0)
ptr = manager->UsersRequest("*", &total)
users = cast_array(ptr, total.value, UserRecord)
manager->MemFree(ptr)
""", samples["UserRecord"]),

        ("03_trade_record_live.md", "TradesUserHistory - Trade History",
         "manager->TradesUserHistory(login, from, to, *total) -> TradeRecord*",
         "Get all trade records (open, closed, balance ops) for a user.",
         f"""total = ctypes.c_int(0)
ptr = manager->TradesUserHistory({LOGIN}, from_90d, now, &total)
trades = cast_array(ptr, total.value, TradeRecord)
manager->MemFree(ptr)
""", samples["TradeRecord"]),

        ("04_margin_level_live.md", "MarginLevelGet - Account Margin State",
         "manager->MarginLevelGet(login, *margin) -> int",
         "Get balance, equity, margin, free margin and margin level.",
         f"""ml = MarginLevel()
ret = manager->MarginLevelGet({LOGIN}, &ml)
""", samples["MarginLevel"]),

        ("05_online_record_live.md", "OnlineRequest - Connected Clients",
         "manager->OnlineRequest(*total) -> OnlineRecord*",
         "Get all currently connected client sessions.",
         """total = ctypes.c_int(0)
ptr = manager->OnlineRequest(&total)
online = cast_array(ptr, total.value, OnlineRecord)
manager->MemFree(ptr)
""", samples["OnlineRecord"]),

        ("06_symbol_info_live.md", "SymbolInfoGet - Market Watch Snapshot",
         "manager->SymbolInfoGet(symbol, *info) -> int",
         "Get current bid/ask, high/low for a symbol.",
         """info = SymbolInfo()
ret = manager->SymbolInfoGet("EURUSD", &info)
""", samples["SymbolInfo"]),

        ("07_summary_live.md", "SummaryGet - Symbol Position Summary",
         "manager->SummaryGet(symbol, *summary) -> int",
         "Get aggregated client positions and exposure for a symbol.",
         """ss = SymbolSummary()
ret = manager->SummaryGet("EURUSD", &ss)
""", samples["SymbolSummary"]),

        ("08_chart_request_live.md", "ChartRequest - OHLCV Bar History",
         "manager->ChartRequest(*req, *total) -> RateInfo*",
         "Get historical OHLCV bars for any symbol and timeframe.",
         """req = ChartInfo()
req.symbol = b"EURUSD"; req.period = 60; req.count = 500
total = ctypes.c_int(0)
ptr = manager->ChartRequest(&req, &total)
bars = cast_array(ptr, total.value, RateInfo)
manager->MemFree(ptr)
""", samples["RateInfo"]),

        ("08b_ticks_request_live.md", "TicksRequest - Raw Tick History",
         "manager->TicksRequest(*req, *total) -> TickAPI*",
         "Get raw bid/ask tick data for a symbol within a time range.",
         """req = TickRequest()
req.symbol = b"EURUSD"; req.from_time = now-3600; req.to_time = now
total = ctypes.c_int(0)
ptr = manager->TicksRequest(&req, &total)
ticks = cast_array(ptr, total.value, TickAPI)
manager->MemFree(ptr)
""", samples["TickAPI"]),

        ("09_reports_request_live.md", "ReportsRequest - Closed Position History",
         "manager->ReportsRequest(from, to, login, *total) -> TradeRecord*",
         "Get closed position history for reporting.",
         f"""total = ctypes.c_int(0)
ptr = manager->ReportsRequest(from_90d, now, {LOGIN}, &total)
closed = cast_array(ptr, total.value, TradeRecord)
manager->MemFree(ptr)
""", samples["TradeRecord"]),

        ("12_journal_request_live.md", "JournalRequest - Server Log Entries",
         "manager->JournalRequest(from, to, *total) -> LogInfo*",
         "Get server journal entries (logins, errors, warnings).",
         """total = ctypes.c_int(0)
ptr = manager->JournalRequest(now-86400, now, &total)
logs = cast_array(ptr, total.value, LogInfo)
manager->MemFree(ptr)
""", samples["LogInfo"]),
    ]

    for fname, title, method, desc, code, sample in entries:
        write_doc(fname, title, method, desc, code, sample,
                  error="DLL not found — fields from MT4ManagerAPI.h header definitions")

    print(f"Generated {len(entries)} docs from header definitions.")
    print(f"Docs: {DOCS_DIR}")


if __name__ == "__main__":
    main()
