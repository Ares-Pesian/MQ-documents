"""
MT5 Manager API - Comprehensive Endpoint Explorer
Connects to MT5 server, calls every major endpoint, captures all response fields,
and writes structured Markdown documentation to docs/mt5-endpoints/.
"""

import MT5Manager
import datetime
import json
import os
import sys

# Force UTF-8 output on Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# -- credentials --------------------------------------------------------------
SERVER   = "157.180.9.122:443"
LOGIN    = 1036
PASSWORD = "Vista1234$"
TIMEOUT  = 60_000   # ms

DOCS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs", "mt5-endpoints")
os.makedirs(DOCS_DIR, exist_ok=True)

# -- helpers ------------------------------------------------------------------

def obj_to_dict(obj):
    if obj is None or obj is False:
        return None
    result = {}
    for name in dir(obj):
        if name.startswith("_"):
            continue
        try:
            val = getattr(obj, name)
            if callable(val):
                continue
            if isinstance(val, bytes):
                val = val.decode("utf-8", errors="replace")
            elif isinstance(val, (int, float, str, bool, type(None))):
                pass
            else:
                val = str(val)
            result[name] = val
        except Exception:
            pass
    return result


def list_to_first(lst):
    if not lst or lst is False:
        return {}
    return obj_to_dict(lst[0]) or {}


def safe(fn, *args):
    try:
        r = fn(*args)
        if r is False:
            return None, str(MT5Manager.LastError())
        return r, None
    except Exception as e:
        return None, str(e)


def field_table(d: dict) -> str:
    if not d:
        return "_No data returned (endpoint may require active data or different permissions)_\n"
    lines = ["| Field | Type | Example Value |", "|-------|------|---------------|"]
    for k, v in d.items():
        typ = type(v).__name__
        val = str(v)
        if len(val) > 120:
            val = val[:117] + "..."
        val = val.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| `{k}` | {typ} | `{val}` |")
    return "\n".join(lines) + "\n"


def write_doc(filename: str, content: str):
    path = os.path.join(DOCS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] wrote {filename}")


def make_doc(title, method, library, description, code, fields_dict, raw_sample=None, error=None):
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    parts = [
        f"# {title}\n",
        f"> Captured: {ts} | Server: `{SERVER}`\n",
        "---\n",
        "## Overview\n",
        f"{description}\n",
        "## Endpoint Details\n",
        "| Property | Value |",
        "|----------|-------|",
        f"| **Library** | `{library}` |",
        f"| **Method** | `{method}` |",
        "",
        "## Example Code\n",
        "```python",
        code.strip(),
        "```\n",
        "## Response Fields\n",
    ]
    if error:
        parts.append(f"> **Error encountered:** `{error}`\n")
    parts.append(field_table(fields_dict or {}))
    if raw_sample:
        parts.append("\n## Raw Sample Response\n")
        parts.append("```json")
        parts.append(json.dumps(raw_sample, indent=2, default=str)[:3000])
        parts.append("```\n")
    return "\n".join(parts)


def log(msg):
    print(msg)


# =============================================================================
# MAIN
# =============================================================================

def main():
    log("Connecting to MT5 server...")
    manager = MT5Manager.ManagerAPI()

    pump_all = (
        MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS     |
        MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_POSITIONS  |
        MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_ORDERS     |
        MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS
    )

    if not manager.Connect(SERVER, LOGIN, PASSWORD, pump_all, TIMEOUT):
        log(f"FAILED to connect: {MT5Manager.LastError()}")
        return

    log("Connected!\n")

    now      = datetime.datetime.now()
    from_90d = now - datetime.timedelta(days=90)
    from_30d = now - datetime.timedelta(days=30)

    # =========================================================================
    # 1. USER endpoints
    # =========================================================================
    log("-- Users --")

    user, err = safe(manager.UserGet, LOGIN)
    d = obj_to_dict(user) or {}
    write_doc("01_user_get.md", make_doc(
        title="UserGet - Retrieve a Single User from Cache",
        method="manager.UserGet(login: int) -> MTUser",
        library="MT5Manager",
        description=(
            "Retrieves a single user record from the local pump cache by login number. "
            "Requires `PUMP_MODE_USERS` pumping to be active on the connection.\n\n"
            "Returns an `MTUser` object on success, or `False` on failure."
        ),
        code=f"""import MT5Manager
manager = MT5Manager.ManagerAPI()
manager.Connect("{SERVER}", {LOGIN}, "***",
                MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS, 60000)
user = manager.UserGet({LOGIN})
if user is False:
    print(MT5Manager.LastError())
else:
    print(user.Login, user.Name, user.Balance, user.Equity)
""",
        fields_dict=d,
        raw_sample=d,
        error=err,
    ))

    users, err = safe(manager.UserGetByGroup, "*")
    sample_user = list_to_first(users)
    log(f"   UserGetByGroup(*) -> {len(users) if users else 0} users")
    write_doc("02_user_get_by_group.md", make_doc(
        title="UserGetByGroup - Retrieve Users by Group Mask (Cache)",
        method="manager.UserGetByGroup(group_mask: str) -> list[MTUser]",
        library="MT5Manager",
        description=(
            "Returns a list of MTUser objects from the pump cache matching the group mask. "
            "Use `*` to return all users. Supports wildcards like `demo\\\\*`."
        ),
        code="""users = manager.UserGetByGroup("*")
print(f"Total users: {len(users)}")
for u in users[:5]:
    print(u.Login, u.Name, u.Group, u.Balance, u.Equity)
""",
        fields_dict=sample_user,
        raw_sample=sample_user,
        error=err,
    ))

    user_req, err = safe(manager.UserRequest, LOGIN)
    d_req = obj_to_dict(user_req) or {}
    write_doc("03_user_request.md", make_doc(
        title="UserRequest - Fetch a User Directly from Server",
        method="manager.UserRequest(login: int) -> MTUser",
        library="MT5Manager",
        description=(
            "Fetches a user record directly from the trade server (bypasses pump cache). "
            "Works even when pump mode is 0. Slightly slower than `UserGet` but always fresh."
        ),
        code=f"""user = manager.UserRequest({LOGIN})
print(user.Login, user.Name, user.Balance)
""",
        fields_dict=d_req,
        raw_sample=d_req,
        error=err,
    ))

    log("-- User Accounts --")
    uacc, err = safe(manager.UserAccountGet, LOGIN)
    d_uacc = obj_to_dict(uacc) or {}
    write_doc("03b_user_account_get.md", make_doc(
        title="UserAccountGet - Get User Account Financial Data (Cache)",
        method="manager.UserAccountGet(login: int) -> MTAccount",
        library="MT5Manager",
        description=(
            "Returns the account financial summary for a user: balance, equity, margin, "
            "free margin, margin level, floating P&L. From pump cache (`PUMP_MODE_USERS`)."
        ),
        code=f"""acc = manager.UserAccountGet({LOGIN})
print(acc.Login, acc.Balance, acc.Equity, acc.Margin,
      acc.MarginFree, acc.MarginLevel, acc.Profit)
""",
        fields_dict=d_uacc,
        raw_sample=d_uacc,
        error=err,
    ))

    uacc_req, err = safe(manager.UserAccountRequest, LOGIN)
    d_uacc_req = obj_to_dict(uacc_req) or {}
    write_doc("03c_user_account_request.md", make_doc(
        title="UserAccountRequest - Fetch Account Data Directly from Server",
        method="manager.UserAccountRequest(login: int) -> MTAccount",
        library="MT5Manager",
        description=(
            "Fetches account financial data directly from the server (not cache). "
            "Returns the same fields as `UserAccountGet` but always fresh."
        ),
        code=f"""acc = manager.UserAccountRequest({LOGIN})
print(acc.Balance, acc.Equity, acc.Profit)
""",
        fields_dict=d_uacc_req,
        raw_sample=d_uacc_req,
        error=err,
    ))

    # =========================================================================
    # 2. DEAL endpoints
    # =========================================================================
    log("-- Deals --")

    deals, err = safe(manager.DealRequest, LOGIN, from_90d, now)
    sample_deal = list_to_first(deals)
    log(f"   DealRequest -> {len(deals) if deals else 0} deals")
    write_doc("04_deal_request.md", make_doc(
        title="DealRequest - Retrieve Deal History for a User",
        method="manager.DealRequest(login: int, from: datetime, to: datetime) -> list[MTDeal]",
        library="MT5Manager",
        description=(
            "Fetches the complete deal history for a specific user within a date range "
            "directly from the server. Returns a list of `MTDeal` objects.\n\n"
            "Each deal represents a single trade execution (open/close leg) or "
            "a balance/credit/bonus operation."
        ),
        code=f"""import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=90)
deals = manager.DealRequest({LOGIN}, from_date, now)
print(f"Got {{len(deals)}} deals")
for deal in deals[:5]:
    print(deal.Deal, deal.Login, deal.Symbol, deal.Action,
          deal.Volume, deal.Price, deal.Profit, deal.Time)
""",
        fields_dict=sample_deal,
        raw_sample=sample_deal,
        error=err,
    ))

    deals_grp, err = safe(manager.DealRequestByGroup, "*", from_30d, now)
    sample_dg = list_to_first(deals_grp) or sample_deal
    log(f"   DealRequestByGroup(*) -> {len(deals_grp) if deals_grp else 0} deals")
    write_doc("04b_deal_request_by_group.md", make_doc(
        title="DealRequestByGroup - Retrieve Deals for All Users by Group Mask",
        method="manager.DealRequestByGroup(group_mask: str, from: datetime, to: datetime) -> list[MTDeal]",
        library="MT5Manager",
        description=(
            "Returns all deals for users matching the group mask within a date range."
        ),
        code="""import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=30)
deals = manager.DealRequestByGroup("*", from_date, now)
print(f"Got {len(deals)} deals across all groups")
""",
        fields_dict=sample_dg,
        raw_sample=sample_dg,
        error=err,
    ))

    if deals:
        tickets = [deals[0].Deal]
        deal_by_t, err2 = safe(manager.DealRequestByTickets, tickets)
        sample_dbt = list_to_first(deal_by_t) or sample_deal
        write_doc("04c_deal_request_by_tickets.md", make_doc(
            title="DealRequestByTickets - Retrieve Specific Deals by Ticket Numbers",
            method="manager.DealRequestByTickets(tickets: list[int]) -> list[MTDeal]",
            library="MT5Manager",
            description=(
                "Fetches one or more specific deals by their ticket numbers."
            ),
            code=f"""deals = manager.DealRequestByTickets([{tickets[0]}])
for d in deals:
    print(d.Deal, d.Symbol, d.Profit)
""",
            fields_dict=sample_dbt,
            raw_sample=sample_dbt,
            error=err2,
        ))

    write_doc("04d_dealer_balance.md", make_doc(
        title="DealerBalance - Execute Balance / Credit / Bonus Operation (WRITE)",
        method="manager.DealerBalance(login: int, amount: float, action: EnDealAction, comment: str) -> int",
        library="MT5Manager",
        description=(
            "Performs a balance, credit, or bonus operation on a user account. "
            "Returns the resulting **deal ticket ID** (int) on success, or `False` on failure.\n\n"
            "**Supported `EnDealAction` values:**\n"
            "- `MTDeal.EnDealAction.DEAL_BALANCE` - Balance deposit/withdrawal\n"
            "- `MTDeal.EnDealAction.DEAL_CREDIT` - Credit in/out\n"
            "- `MTDeal.EnDealAction.DEAL_BONUS` - Bonus\n"
            "- `MTDeal.EnDealAction.DEAL_COMMISSION` - Commission\n\n"
            "> **WRITE OPERATION** - Response is an integer deal ticket, not an object."
        ),
        code=f"""deal_ticket = manager.DealerBalance(
    {LOGIN},
    100.0,                                         # amount (positive=deposit)
    MT5Manager.MTDeal.EnDealAction.DEAL_BALANCE,
    "API deposit"
)
if deal_ticket is False:
    print(f"Error: {{MT5Manager.LastError()}}")
else:
    print(f"Created deal ticket: {{deal_ticket}}")
""",
        fields_dict={"return_value": "int - deal ticket number of the created balance deal"},
        error=None,
    ))

    # =========================================================================
    # 3. POSITION endpoints
    # =========================================================================
    log("-- Positions --")

    positions, err = safe(manager.PositionGetByGroup, "*")
    sample_pos = list_to_first(positions)
    log(f"   PositionGetByGroup(*) -> {len(positions) if positions else 0} positions")
    write_doc("05_position_get_by_group.md", make_doc(
        title="PositionGetByGroup - Retrieve All Open Positions by Group Mask (Cache)",
        method="manager.PositionGetByGroup(group_mask: str) -> list[MTPosition]",
        library="MT5Manager",
        description=(
            "Returns all currently open positions for users matching the group mask. "
            "Data comes from the pump cache - requires `PUMP_MODE_POSITIONS`."
        ),
        code="""positions = manager.PositionGetByGroup("*")
for pos in positions:
    print(pos.Position, pos.Login, pos.Symbol,
          pos.Action, pos.Volume, pos.Price,
          pos.PriceCurrent, pos.Profit, pos.Storage)
""",
        fields_dict=sample_pos,
        raw_sample=sample_pos,
        error=err,
    ))

    pos_logins, err = safe(manager.PositionGetByLogins, [LOGIN], "*")
    sample_pl = list_to_first(pos_logins) or sample_pos
    write_doc("05b_position_get_by_logins.md", make_doc(
        title="PositionGetByLogins - Get Open Positions for Specific Users (Cache)",
        method="manager.PositionGetByLogins(logins: list[int], group: str) -> list[MTPosition]",
        library="MT5Manager",
        description=(
            "Returns open positions for one or more specific user logins from the pump cache."
        ),
        code=f"""positions = manager.PositionGetByLogins([{LOGIN}], "*")
for pos in positions:
    print(pos.Position, pos.Symbol, pos.Volume, pos.Profit)
""",
        fields_dict=sample_pl,
        raw_sample=sample_pl,
        error=err,
    ))

    pos_req_res, err = safe(manager.PositionRequest, LOGIN)
    sample_pr = list_to_first(pos_req_res) or sample_pos
    write_doc("05c_position_request.md", make_doc(
        title="PositionRequest - Fetch Open Positions Directly from Server",
        method="manager.PositionRequest(login: int) -> list[MTPosition]",
        library="MT5Manager",
        description=(
            "Fetches all open positions for a user directly from the trade server."
        ),
        code=f"""positions = manager.PositionRequest({LOGIN})
for pos in positions:
    print(pos.Position, pos.Symbol, pos.Profit)
""",
        fields_dict=sample_pr,
        raw_sample=sample_pr,
        error=err,
    ))

    pos_req_grp, err = safe(manager.PositionRequestByGroup, "*")
    sample_prg = list_to_first(pos_req_grp) or sample_pos
    log(f"   PositionRequestByGroup(*) -> {len(pos_req_grp) if pos_req_grp else 0} positions")
    write_doc("05d_position_request_by_group.md", make_doc(
        title="PositionRequestByGroup - Fetch All Positions from Server by Group",
        method="manager.PositionRequestByGroup(group_mask: str) -> list[MTPosition]",
        library="MT5Manager",
        description=(
            "Fetches all open positions for users matching the group mask directly from the server."
        ),
        code="""positions = manager.PositionRequestByGroup("*")
print(f"Total open positions: {len(positions)}")
""",
        fields_dict=sample_prg,
        raw_sample=sample_prg,
        error=err,
    ))

    # =========================================================================
    # 4. ORDER endpoints
    # =========================================================================
    log("-- Orders --")

    orders, err = safe(manager.OrderGetByGroup, "*")
    sample_ord = list_to_first(orders)
    log(f"   OrderGetByGroup(*) -> {len(orders) if orders else 0} orders")
    write_doc("06_order_get_by_group.md", make_doc(
        title="OrderGetByGroup - Retrieve Active Orders by Group Mask (Cache)",
        method="manager.OrderGetByGroup(group_mask: str) -> list[MTOrder]",
        library="MT5Manager",
        description=(
            "Returns all pending/active orders for users matching the group mask from the pump cache. "
            "Requires `PUMP_MODE_ORDERS`."
        ),
        code="""orders = manager.OrderGetByGroup("*")
for order in orders:
    print(order.Order, order.Login, order.Symbol,
          order.Type, order.TypeFill, order.TypeTime,
          order.VolumeCurrent, order.PriceOrder,
          order.PriceCurrent, order.PriceSL, order.PriceTP, order.State)
""",
        fields_dict=sample_ord,
        raw_sample=sample_ord,
        error=err,
    ))

    ord_logins, err = safe(manager.OrderGetByLogins, [LOGIN], "*")
    sample_ol = list_to_first(ord_logins) or sample_ord
    write_doc("06b_order_get_by_logins.md", make_doc(
        title="OrderGetByLogins - Get Active Orders for Specific Users (Cache)",
        method="manager.OrderGetByLogins(logins: list[int], group: str) -> list[MTOrder]",
        library="MT5Manager",
        description=(
            "Returns all active/pending orders for specific user logins from the pump cache."
        ),
        code=f"""orders = manager.OrderGetByLogins([{LOGIN}], "*")
for order in orders:
    print(order.Order, order.Symbol, order.Type, order.VolumeCurrent)
""",
        fields_dict=sample_ol,
        raw_sample=sample_ol,
        error=err,
    ))

    ord_open, err = safe(manager.OrderRequestOpen, LOGIN)
    sample_oo = list_to_first(ord_open) or sample_ord
    write_doc("06c_order_request_open.md", make_doc(
        title="OrderRequestOpen - Fetch Open Orders from Server for a User",
        method="manager.OrderRequestOpen(login: int) -> list[MTOrder]",
        library="MT5Manager",
        description=(
            "Fetches all currently active/pending orders for a user directly from the server."
        ),
        code=f"""orders = manager.OrderRequestOpen({LOGIN})
for order in orders:
    print(order.Order, order.Symbol, order.Type, order.PriceOrder)
""",
        fields_dict=sample_oo,
        raw_sample=sample_oo,
        error=err,
    ))

    # =========================================================================
    # 5. HISTORY ORDER endpoints
    # =========================================================================
    log("-- History Orders --")

    hist, err = safe(manager.HistoryRequest, LOGIN, from_90d, now)
    sample_ho = list_to_first(hist)
    log(f"   HistoryRequest -> {len(hist) if hist else 0} history orders")
    write_doc("07_history_request.md", make_doc(
        title="HistoryRequest - Retrieve Historical Orders for a User",
        method="manager.HistoryRequest(login: int, from: datetime, to: datetime) -> list[MTOrder]",
        library="MT5Manager",
        description=(
            "Fetches historical (filled/cancelled/rejected) orders for a user within a date range. "
            "Same MTOrder structure as active orders but with final `State` values."
        ),
        code=f"""import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=90)
orders = manager.HistoryRequest({LOGIN}, from_date, now)
for order in orders:
    print(order.Order, order.Symbol, order.Type, order.State,
          order.VolumeCurrent, order.PriceOrder, order.TimeSetup, order.TimeDone)
""",
        fields_dict=sample_ho,
        raw_sample=sample_ho,
        error=err,
    ))

    hist_grp, err = safe(manager.HistoryRequestByGroup, "*", from_30d, now)
    sample_hg = list_to_first(hist_grp) or sample_ho
    log(f"   HistoryRequestByGroup(*) -> {len(hist_grp) if hist_grp else 0} history orders")
    write_doc("07b_history_request_by_group.md", make_doc(
        title="HistoryRequestByGroup - Historical Orders by Group Mask",
        method="manager.HistoryRequestByGroup(group_mask: str, from: datetime, to: datetime) -> list[MTOrder]",
        library="MT5Manager",
        description=(
            "Returns historical orders for all users matching the group mask within the date range."
        ),
        code="""import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=30)
orders = manager.HistoryRequestByGroup("*", from_date, now)
print(f"Total: {len(orders)} history orders")
""",
        fields_dict=sample_hg,
        raw_sample=sample_hg,
        error=err,
    ))

    # =========================================================================
    # 6. SYMBOL endpoints
    # =========================================================================
    log("-- Symbols --")

    symbols, err = safe(manager.SymbolGetArray)
    sample_sym = list_to_first(symbols)
    log(f"   SymbolGetArray -> {len(symbols) if symbols else 0} symbols")
    write_doc("08_symbol_get_array.md", make_doc(
        title="SymbolGetArray - Retrieve All Available Symbols (Cache)",
        method="manager.SymbolGetArray() -> list[MTSymbol]",
        library="MT5Manager",
        description=(
            "Returns the complete list of symbols from the pump cache. "
            "Requires `PUMP_MODE_SYMBOLS`."
        ),
        code="""symbols = manager.SymbolGetArray()
for sym in symbols[:5]:
    print(sym.Symbol, sym.Digits, sym.ContractSize,
          sym.CurrencyBase, sym.CurrencyProfit,
          sym.Spread, sym.SpreadFloat)
""",
        fields_dict=sample_sym,
        raw_sample=sample_sym,
        error=err,
    ))

    sym_name = symbols[0].Symbol if symbols else "EURUSD"
    sym_one, err = safe(manager.SymbolGet, sym_name)
    d_sym = obj_to_dict(sym_one) or sample_sym
    write_doc("08b_symbol_get.md", make_doc(
        title="SymbolGet - Get a Single Symbol by Name (Cache)",
        method="manager.SymbolGet(symbol: str) -> MTSymbol",
        library="MT5Manager",
        description="Returns a single symbol record from the pump cache.",
        code=f"""sym = manager.SymbolGet("{sym_name}")
print(sym.Symbol, sym.Bid, sym.Ask, sym.Spread, sym.Digits)
""",
        fields_dict=d_sym,
        raw_sample=d_sym,
        error=err,
    ))

    sym_req, err = safe(manager.SymbolRequest, sym_name)
    d_symr = obj_to_dict(sym_req) or sample_sym
    write_doc("08c_symbol_request.md", make_doc(
        title="SymbolRequest - Fetch Symbol Configuration Directly from Server",
        method="manager.SymbolRequest(symbol: str) -> MTSymbol",
        library="MT5Manager",
        description="Fetches symbol configuration directly from the trade server.",
        code=f"""sym = manager.SymbolRequest("{sym_name}")
print(sym.Symbol, sym.ContractSize, sym.CurrencyBase)
""",
        fields_dict=d_symr,
        raw_sample=d_symr,
        error=err,
    ))

    sym_all_req, err = safe(manager.SymbolRequestArray)
    sample_sar = list_to_first(sym_all_req) or sample_sym
    log(f"   SymbolRequestArray -> {len(sym_all_req) if sym_all_req else 0} symbols")
    write_doc("08d_symbol_request_array.md", make_doc(
        title="SymbolRequestArray - Fetch All Symbols from Server",
        method="manager.SymbolRequestArray() -> list[MTSymbol]",
        library="MT5Manager",
        description="Fetches the full symbol list directly from the trade server.",
        code="""symbols = manager.SymbolRequestArray()
print(f"Total symbols: {len(symbols)}")
""",
        fields_dict=sample_sar,
        raw_sample=sample_sar,
        error=err,
    ))

    # =========================================================================
    # 7. GROUP endpoints
    # =========================================================================
    log("-- Groups --")

    groups, err = safe(manager.GroupRequestArray)
    sample_grp = list_to_first(groups)
    log(f"   GroupRequestArray -> {len(groups) if groups else 0} groups")
    write_doc("09_group_request_array.md", make_doc(
        title="GroupRequestArray - Retrieve All User Groups",
        method="manager.GroupRequestArray() -> list[MTGroup]",
        library="MT5Manager",
        description="Returns all groups configured on the MT5 server.",
        code="""groups = manager.GroupRequestArray()
for g in groups:
    print(g.Group, g.Currency, g.Leverage, g.Company)
""",
        fields_dict=sample_grp,
        raw_sample=sample_grp,
        error=err,
    ))

    if groups:
        grp_name = groups[0].Group
        grp_one, err = safe(manager.GroupRequest, grp_name)
        d_grp = obj_to_dict(grp_one) or sample_grp
        write_doc("09b_group_request.md", make_doc(
            title="GroupRequest - Retrieve a Single Group Configuration",
            method="manager.GroupRequest(group: str) -> MTGroup",
            library="MT5Manager",
            description="Fetches a single group's full configuration from the server.",
            code=f"""group = manager.GroupRequest("{grp_name}")
print(group.Group, group.Currency, group.Leverage)
""",
            fields_dict=d_grp,
            raw_sample=d_grp,
            error=err,
        ))

    # =========================================================================
    # 8. TICK / PRICE DATA endpoints
    # =========================================================================
    log("-- Ticks --")

    last_tick, err = safe(manager.TickLast, sym_name)
    d_lt = obj_to_dict(last_tick) or {}
    write_doc("10_tick_last.md", make_doc(
        title="TickLast - Get the Latest Tick for a Symbol",
        method="manager.TickLast(symbol: str) -> MTTick",
        library="MT5Manager",
        description=(
            "Returns the most recent tick for a symbol from the pump cache. "
            "Requires `PUMP_MODE_SYMBOLS`."
        ),
        code=f"""tick = manager.TickLast("{sym_name}")
print(tick.datetime, tick.bid, tick.ask, tick.last, tick.volume)
""",
        fields_dict=d_lt,
        raw_sample=d_lt,
        error=err,
    ))

    tick_stat, err = safe(manager.TickStat, sym_name)
    d_ts = obj_to_dict(tick_stat) or {}
    write_doc("10b_tick_stat.md", make_doc(
        title="TickStat - Get Daily Tick Statistics for a Symbol",
        method="manager.TickStat(symbol: str) -> MTTickStat",
        library="MT5Manager",
        description="Returns current daily tick statistics (high/low bid/ask) for a symbol.",
        code=f"""stat = manager.TickStat("{sym_name}")
print(stat.datetime, stat.bid_high, stat.bid_low, stat.ask_high, stat.ask_low)
""",
        fields_dict=d_ts,
        raw_sample=d_ts,
        error=err,
    ))

    from_1d = now - datetime.timedelta(days=1)
    tick_hist, err = safe(manager.TickHistoryRequest, sym_name, from_1d, now)
    sample_th = {}
    if tick_hist and tick_hist is not False:
        try:
            t0 = tick_hist[0]
            sample_th = obj_to_dict(t0) or {"raw": str(t0)[:200]}
        except Exception as ex:
            sample_th = {"error_reading_item": str(ex)}
    log(f"   TickHistoryRequest -> {len(tick_hist) if tick_hist else 0} ticks")
    write_doc("10c_tick_history_request.md", make_doc(
        title="TickHistoryRequest - Retrieve Historical Tick Data for a Symbol",
        method="manager.TickHistoryRequest(symbol: str, from: datetime, to: datetime) -> list[MTTick]",
        library="MT5Manager",
        description=(
            "Fetches historical tick (bid/ask/last/volume) data for a symbol within a time range."
        ),
        code=f"""import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=1)
ticks = manager.TickHistoryRequest("{sym_name}", from_date, now)
for t in ticks[:5]:
    print(t.datetime, t.bid, t.ask, t.last, t.volume)
""",
        fields_dict=sample_th,
        raw_sample=sample_th,
        error=err,
    ))

    # =========================================================================
    # 9. SUMMARY POSITION endpoints
    # =========================================================================
    log("-- Summary Positions --")

    summaries, err = safe(manager.SummaryGetAll)
    sample_sum = list_to_first(summaries)
    log(f"   SummaryGetAll -> {len(summaries) if summaries else 0} summaries")
    write_doc("11_summary_get_all.md", make_doc(
        title="SummaryGetAll - Retrieve All Aggregated Position Summaries",
        method="manager.SummaryGetAll() -> list[MTSummary]",
        library="MT5Manager",
        description=(
            "Returns the aggregated open position summary per symbol across all users."
        ),
        code="""summaries = manager.SummaryGetAll()
for s in summaries:
    print(s.Symbol, s.VolumeExt, s.Profit, s.Buy, s.Sell)
""",
        fields_dict=sample_sum,
        raw_sample=sample_sum,
        error=err,
    ))

    # =========================================================================
    # 10. EXPOSURE endpoints
    # =========================================================================
    log("-- Exposure --")

    exposures, err = safe(manager.ExposureGetAll)
    sample_exp = list_to_first(exposures)
    log(f"   ExposureGetAll -> {len(exposures) if exposures else 0} exposures")
    write_doc("12_exposure_get_all.md", make_doc(
        title="ExposureGetAll - Retrieve Currency Exposure",
        method="manager.ExposureGetAll() -> list[MTExposure]",
        library="MT5Manager",
        description="Returns total currency exposure (net positions per currency) across all users.",
        code="""exposures = manager.ExposureGetAll()
for e in exposures:
    print(e.Symbol, e.Volume, e.Profit)
""",
        fields_dict=sample_exp,
        raw_sample=sample_exp,
        error=err,
    ))

    # =========================================================================
    # 11. DAILY (End-of-Day) REPORT endpoints
    # =========================================================================
    log("-- Daily Reports --")

    daily, err = safe(manager.DailyRequest, LOGIN, from_90d, now)
    sample_day = list_to_first(daily)
    log(f"   DailyRequest -> {len(daily) if daily else 0} daily records")
    write_doc("13_daily_request.md", make_doc(
        title="DailyRequest - Retrieve Daily Account Reports for a User",
        method="manager.DailyRequest(login: int, from: datetime, to: datetime) -> list[MTDaily]",
        library="MT5Manager",
        description=(
            "Returns end-of-day account snapshots for a user, including balance, equity, "
            "and floating P&L at the end of each trading day."
        ),
        code=f"""import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=90)
daily = manager.DailyRequest({LOGIN}, from_date, now)
for d in daily:
    print(d.Login, d.Datetime, d.Balance, d.Equity,
          d.Profit, d.Credit, d.Margin, d.MarginFree)
""",
        fields_dict=sample_day,
        raw_sample=sample_day,
        error=err,
    ))

    daily_grp, err = safe(manager.DailyRequestByGroup, "*", from_30d, now)
    sample_dg2 = list_to_first(daily_grp) or sample_day
    log(f"   DailyRequestByGroup(*) -> {len(daily_grp) if daily_grp else 0} daily records")
    write_doc("13b_daily_request_by_group.md", make_doc(
        title="DailyRequestByGroup - Daily Account Reports by Group Mask",
        method="manager.DailyRequestByGroup(group_mask: str, from: datetime, to: datetime) -> list[MTDaily]",
        library="MT5Manager",
        description="Returns end-of-day account snapshots for all users matching the group mask.",
        code="""import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=30)
daily = manager.DailyRequestByGroup("*", from_date, now)
print(f"Total daily records: {len(daily)}")
""",
        fields_dict=sample_dg2,
        raw_sample=sample_dg2,
        error=err,
    ))

    # =========================================================================
    # 12. ONLINE (connected) USERS
    # =========================================================================
    log("-- Online Connections --")

    online, err = safe(manager.OnlineGetArray)
    sample_onl = list_to_first(online)
    log(f"   OnlineGetArray -> {len(online) if online else 0} connections")
    write_doc("14_online_get_array.md", make_doc(
        title="OnlineGetArray - Retrieve All Currently Connected Users",
        method="manager.OnlineGetArray() -> list[MTOnline]",
        library="MT5Manager",
        description="Returns all users currently connected to the trade server.",
        code="""connections = manager.OnlineGetArray()
for c in connections:
    print(c.Login, c.IP, c.ConnectTime, c.LastAccessTime, c.Agent)
""",
        fields_dict=sample_onl,
        raw_sample=sample_onl,
        error=err,
    ))

    # =========================================================================
    # 13. NEWS DATABASE
    # =========================================================================
    log("-- News --")

    news_total = manager.NewsTotal()
    sample_news = {}
    if news_total and news_total > 0:
        news_item, _ = safe(manager.NewsGet, 0)
        sample_news = obj_to_dict(news_item) or {}
    log(f"   NewsTotal -> {news_total} news items")
    write_doc("15_news.md", make_doc(
        title="News - Retrieve News Items from the Server",
        method="manager.NewsGet(index: int) -> MTNews  |  manager.NewsTotal() -> int",
        library="MT5Manager",
        description=(
            "Accesses the MT5 news database. Use `NewsTotal()` for count, "
            "`NewsGet(index)` for individual items."
        ),
        code="""total = manager.NewsTotal()
for i in range(total):
    news = manager.NewsGet(i)
    print(news.Datetime, news.Subject, news.Category, news.Language)
""",
        fields_dict=sample_news,
        raw_sample=sample_news,
        error=None,
    ))

    # =========================================================================
    # 14. CLIENT (KYC) records
    # =========================================================================
    log("-- Clients --")

    clients, err = safe(manager.ClientRequestByGroup, "*")
    sample_cli = list_to_first(clients)
    log(f"   ClientRequestByGroup(*) -> {len(clients) if clients else 0} clients")
    write_doc("16_client_request_by_group.md", make_doc(
        title="ClientRequestByGroup - Retrieve Client (KYC) Records by Group",
        method="manager.ClientRequestByGroup(group_mask: str) -> list[MTClient]",
        library="MT5Manager",
        description=(
            "Returns client (KYC) records for users matching the group mask. "
            "Clients are master entities that can be linked to one or more user accounts."
        ),
        code="""clients = manager.ClientRequestByGroup("*")
for c in clients:
    print(c.ID, c.Name, c.Email, c.Phone, c.Country, c.Status)
""",
        fields_dict=sample_cli,
        raw_sample=sample_cli,
        error=err,
    ))

    # =========================================================================
    # 15. DEPTH OF MARKET
    # =========================================================================
    log("-- Depth of Market --")

    book, err = safe(manager.BookGet, sym_name)
    sample_book = {}
    if book and book is not False:
        try:
            sample_book = obj_to_dict(book[0]) or {}
        except Exception:
            pass
    write_doc("17_book_get.md", make_doc(
        title="BookGet - Retrieve Depth of Market (Order Book) for a Symbol",
        method="manager.BookGet(symbol: str) -> list[MTBook]",
        library="MT5Manager",
        description=(
            "Returns the current order-book levels for a symbol. "
            "Each level has a Type (buy/sell), Price, and Volume."
        ),
        code=f"""book = manager.BookGet("{sym_name}")
for level in book:
    print(level.Type, level.Price, level.Volume)
""",
        fields_dict=sample_book,
        raw_sample=sample_book,
        error=err,
    ))

    # =========================================================================
    # 16. TRADE MARGIN / PROFIT calculations
    # =========================================================================
    log("-- Trade Calculations --")

    margin_res, err = safe(manager.TradeMarginCheck, LOGIN, sym_name, 0, 1.0)
    d_margin = obj_to_dict(margin_res) if margin_res else {}
    write_doc("18_trade_margin_check.md", make_doc(
        title="TradeMarginCheck - Calculate Required Margin for a Trade",
        method="manager.TradeMarginCheck(login: int, symbol: str, type: int, volume: float) -> MTMarginCheck",
        library="MT5Manager",
        description="Calculates the margin requirements for a hypothetical trade without executing it.",
        code=f"""# type: 0=buy, 1=sell
margin = manager.TradeMarginCheck({LOGIN}, "{sym_name}", 0, 1.0)
print(margin.Margin, margin.MarginFree, margin.Equity)
""",
        fields_dict=d_margin,
        raw_sample=d_margin,
        error=err,
    ))

    profit_res, err = safe(manager.TradeProfit, LOGIN, sym_name, 0, 1.0, 0.0, 0.0)
    d_profit = {"profit_value": str(profit_res)} if profit_res is not None else {}
    write_doc("18b_trade_profit.md", make_doc(
        title="TradeProfit - Calculate Profit for a Hypothetical Trade",
        method="manager.TradeProfit(login: int, symbol: str, type: int, volume: float, price_open: float, price_close: float) -> float",
        library="MT5Manager",
        description="Calculates the profit/loss for a hypothetical position in account currency.",
        code=f"""profit = manager.TradeProfit({LOGIN}, "{sym_name}", 0, 1.0, 1.0800, 1.0900)
print(f"Estimated profit: {{profit}}")
""",
        fields_dict=d_profit,
        raw_sample=d_profit,
        error=err,
    ))

    # =========================================================================
    # 17. USER WRITE OPERATIONS (documented only)
    # =========================================================================
    write_doc("19_user_add_update.md", make_doc(
        title="UserAdd / UserUpdate - Create or Update a User Account (WRITE)",
        method=(
            "manager.UserAdd(user: MTUser, main_pass: str, investor_pass: str) -> bool\n"
            "manager.UserUpdate(user: MTUser) -> bool"
        ),
        library="MT5Manager",
        description=(
            "**UserAdd** creates a new trading account. Required fields: `Group`, `Leverage`, "
            "`FirstName`, `LastName`. On success, `user.Login` is populated with the assigned login.\n\n"
            "**UserUpdate** saves changes to an existing user record.\n\n"
            "> **WRITE OPERATION** - not executed during field capture."
        ),
        code=f"""# Create a new user
user = MT5Manager.MTUser(manager)
user.Group    = "demo\\\\example"
user.Leverage = 100
user.FirstName = "Jane"
user.LastName  = "Doe"
ok = manager.UserAdd(user, "MainPass123!", "InvPass123!")
print(f"Created login: {{user.Login}}" if ok else MT5Manager.LastError())

# Update existing user
user2 = manager.UserGet({LOGIN})
user2.Comment = "Updated via API"
ok = manager.UserUpdate(user2)
print("Updated" if ok else MT5Manager.LastError())
""",
        fields_dict={"result": "bool - True on success; user.Login populated by server on UserAdd"},
        error=None,
    ))

    write_doc("20_user_password_change.md", make_doc(
        title="UserPasswordChange - Change a User Password (WRITE)",
        method="manager.UserPasswordChange(pass_type: EnUsersPasswords, login: int, new_password: str) -> bool",
        library="MT5Manager",
        description=(
            "Changes the trading or investor password for a user.\n\n"
            "**Password types:**\n"
            "- `MTUser.EnUsersPasswords.USER_PASS_MAIN` - Main (trading) password\n"
            "- `MTUser.EnUsersPasswords.USER_PASS_INVESTOR` - Read-only investor password\n\n"
            "> **WRITE OPERATION** - returns `True` on success."
        ),
        code=f"""result = manager.UserPasswordChange(
    MT5Manager.MTUser.EnUsersPasswords.USER_PASS_MAIN,
    {LOGIN},
    "NewSecurePass123!"
)
print("Success" if result else MT5Manager.LastError())
""",
        fields_dict={"result": "bool - True on success, False on failure"},
        error=None,
    ))

    # =========================================================================
    # 18. PENDING TRADE REQUESTS
    # =========================================================================
    log("-- Trade Requests --")

    req_total = manager.RequestTotal()
    sample_req = {}
    if req_total > 0:
        req_item, _ = safe(manager.RequestGet, 0)
        sample_req = obj_to_dict(req_item) or {}
    log(f"   RequestTotal -> {req_total} pending requests")
    write_doc("21_request_get.md", make_doc(
        title="RequestGet - Retrieve Pending Trade Requests (Dealer Queue)",
        method="manager.RequestGet(index: int) -> MTRequest  |  manager.RequestTotal() -> int",
        library="MT5Manager",
        description=(
            "Accesses pending trade requests in the dealer queue. "
            "Use `RequestTotal()` for count, `RequestGet(index)` for each item."
        ),
        code="""total = manager.RequestTotal()
for i in range(total):
    req = manager.RequestGet(i)
    print(req.ID, req.Login, req.Symbol, req.Type, req.Volume, req.Price)
""",
        fields_dict=sample_req,
        raw_sample=sample_req,
        error=None,
    ))

    # =========================================================================
    # 19. LEVERAGE configurations
    # =========================================================================
    log("-- Leverage Schedules --")

    lev_total = manager.LeverageTotal()
    sample_lev = {}
    if lev_total > 0:
        lev_item, _ = safe(manager.LeverageGet, 0)
        sample_lev = obj_to_dict(lev_item) or {}
    log(f"   LeverageTotal -> {lev_total} leverage schedules")
    write_doc("22_leverage_get.md", make_doc(
        title="LeverageGet - Retrieve Leverage Schedule Configurations",
        method="manager.LeverageGet(index: int) -> MTLeverage  |  manager.LeverageTotal() -> int",
        library="MT5Manager",
        description="Accesses leverage schedule configurations on the server.",
        code="""total = manager.LeverageTotal()
for i in range(total):
    lev = manager.LeverageGet(i)
    print(lev.Name, lev.Description)
""",
        fields_dict=sample_lev,
        raw_sample=sample_lev,
        error=None,
    ))

    # =========================================================================
    # 20. SPREAD configurations
    # =========================================================================
    log("-- Spreads --")

    sp_total = manager.SpreadTotal()
    sample_sp = {}
    if sp_total > 0:
        sp_item, _ = safe(manager.SpreadNext, 0)
        sample_sp = obj_to_dict(sp_item) or {}
    log(f"   SpreadTotal -> {sp_total} spread configurations")
    write_doc("23_spread.md", make_doc(
        title="Spread - Retrieve Spread Configurations",
        method="manager.SpreadNext(index: int) -> MTSpread  |  manager.SpreadTotal() -> int",
        library="MT5Manager",
        description="Accesses spread configuration records on the server.",
        code="""total = manager.SpreadTotal()
for i in range(total):
    spread = manager.SpreadNext(i)
    print(spread.Name)
""",
        fields_dict=sample_sp,
        raw_sample=sample_sp,
        error=None,
    ))

    # =========================================================================
    # 21. HOLIDAYS
    # =========================================================================
    log("-- Holidays --")

    hol_total = manager.HolidayTotal()
    sample_hol = {}
    if hol_total > 0:
        hol_item, _ = safe(manager.HolidayNext, 0)
        sample_hol = obj_to_dict(hol_item) or {}
    log(f"   HolidayTotal -> {hol_total} holidays")
    write_doc("24_holiday.md", make_doc(
        title="Holiday - Retrieve Holiday / Session Schedules",
        method="manager.HolidayNext(index: int) -> MTHoliday  |  manager.HolidayTotal() -> int",
        library="MT5Manager",
        description="Accesses holiday and session schedule records on the server.",
        code="""total = manager.HolidayTotal()
for i in range(total):
    holiday = manager.HolidayNext(i)
    print(holiday.Symbol, holiday.Mode, holiday.Day, holiday.From, holiday.To)
""",
        fields_dict=sample_hol,
        raw_sample=sample_hol,
        error=None,
    ))

    # =========================================================================
    # 22. SERVER TIME
    # =========================================================================
    log("-- Server Time --")

    srv_time, err = safe(manager.TimeServerRequest)
    write_doc("25_time_server.md", make_doc(
        title="TimeServerRequest - Get the Trade Server's Current Time",
        method="manager.TimeServerRequest() -> datetime",
        library="MT5Manager",
        description="Fetches the current time from the trade server for synchronization.",
        code="""server_time = manager.TimeServerRequest()
print(f"Server time: {server_time}")
""",
        fields_dict={"server_time": str(srv_time)} if srv_time else {},
        raw_sample={"server_time": str(srv_time)} if srv_time else None,
        error=err,
    ))

    # =========================================================================
    # WRITE COMPREHENSIVE INDEX
    # =========================================================================
    log("-- Writing README index --")

    index = """# MT5 Manager API - Complete Endpoint Reference

> Auto-generated by `collect_mt5_responses.py`
> **Library:** `MT5Manager` (Python) | **Server:** `157.180.9.122:443`

This index documents every major MT5 Manager API endpoint with:
- Method signature
- Description
- Example Python code
- **Live response fields captured from the server**

---

## Users

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [01_user_get.md](01_user_get.md) | Get single user (cache) | `UserGet(login)` |
| 2 | [02_user_get_by_group.md](02_user_get_by_group.md) | Get users by group (cache) | `UserGetByGroup(mask)` |
| 3 | [03_user_request.md](03_user_request.md) | Fetch user from server | `UserRequest(login)` |
| 4 | [03b_user_account_get.md](03b_user_account_get.md) | Account financial data (cache) | `UserAccountGet(login)` |
| 5 | [03c_user_account_request.md](03c_user_account_request.md) | Account data from server | `UserAccountRequest(login)` |
| 6 | [19_user_add_update.md](19_user_add_update.md) | Create / update user (WRITE) | `UserAdd()` / `UserUpdate()` |
| 7 | [20_user_password_change.md](20_user_password_change.md) | Change password (WRITE) | `UserPasswordChange(type, login, pass)` |

## Deals

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [04_deal_request.md](04_deal_request.md) | Deal history for user | `DealRequest(login, from, to)` |
| 2 | [04b_deal_request_by_group.md](04b_deal_request_by_group.md) | Deals for all users in group | `DealRequestByGroup(mask, from, to)` |
| 3 | [04c_deal_request_by_tickets.md](04c_deal_request_by_tickets.md) | Specific deals by ticket | `DealRequestByTickets([tickets])` |
| 4 | [04d_dealer_balance.md](04d_dealer_balance.md) | Balance/Credit operation (WRITE) | `DealerBalance(login, amount, action, comment)` |

## Positions

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [05_position_get_by_group.md](05_position_get_by_group.md) | All open positions by group (cache) | `PositionGetByGroup(mask)` |
| 2 | [05b_position_get_by_logins.md](05b_position_get_by_logins.md) | Open positions for users (cache) | `PositionGetByLogins([logins], group)` |
| 3 | [05c_position_request.md](05c_position_request.md) | Open positions from server | `PositionRequest(login)` |
| 4 | [05d_position_request_by_group.md](05d_position_request_by_group.md) | All positions from server by group | `PositionRequestByGroup(mask)` |

## Orders (Active / Pending)

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [06_order_get_by_group.md](06_order_get_by_group.md) | Active orders by group (cache) | `OrderGetByGroup(mask)` |
| 2 | [06b_order_get_by_logins.md](06b_order_get_by_logins.md) | Active orders for users (cache) | `OrderGetByLogins([logins], group)` |
| 3 | [06c_order_request_open.md](06c_order_request_open.md) | Open orders from server | `OrderRequestOpen(login)` |

## History Orders (Filled / Cancelled)

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [07_history_request.md](07_history_request.md) | History orders for user | `HistoryRequest(login, from, to)` |
| 2 | [07b_history_request_by_group.md](07b_history_request_by_group.md) | History orders by group | `HistoryRequestByGroup(mask, from, to)` |

## Symbols & Ticks

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [08_symbol_get_array.md](08_symbol_get_array.md) | All symbols (cache) | `SymbolGetArray()` |
| 2 | [08b_symbol_get.md](08b_symbol_get.md) | Single symbol (cache) | `SymbolGet(name)` |
| 3 | [08c_symbol_request.md](08c_symbol_request.md) | Single symbol (server) | `SymbolRequest(name)` |
| 4 | [08d_symbol_request_array.md](08d_symbol_request_array.md) | All symbols (server) | `SymbolRequestArray()` |
| 5 | [10_tick_last.md](10_tick_last.md) | Latest tick | `TickLast(symbol)` |
| 6 | [10b_tick_stat.md](10b_tick_stat.md) | Daily tick statistics | `TickStat(symbol)` |
| 7 | [10c_tick_history_request.md](10c_tick_history_request.md) | Historical tick data | `TickHistoryRequest(symbol, from, to)` |
| 8 | [17_book_get.md](17_book_get.md) | Depth of Market | `BookGet(symbol)` |

## Groups

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [09_group_request_array.md](09_group_request_array.md) | All groups | `GroupRequestArray()` |
| 2 | [09b_group_request.md](09b_group_request.md) | Single group | `GroupRequest(group_name)` |

## Aggregates & Reports

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [11_summary_get_all.md](11_summary_get_all.md) | Summary positions | `SummaryGetAll()` |
| 2 | [12_exposure_get_all.md](12_exposure_get_all.md) | Currency exposure | `ExposureGetAll()` |
| 3 | [13_daily_request.md](13_daily_request.md) | Daily reports for user | `DailyRequest(login, from, to)` |
| 4 | [13b_daily_request_by_group.md](13b_daily_request_by_group.md) | Daily reports by group | `DailyRequestByGroup(mask, from, to)` |

## Connections & Clients

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [14_online_get_array.md](14_online_get_array.md) | Online connections | `OnlineGetArray()` |
| 2 | [16_client_request_by_group.md](16_client_request_by_group.md) | Client (KYC) records | `ClientRequestByGroup(mask)` |

## Trade Calculations

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [18_trade_margin_check.md](18_trade_margin_check.md) | Margin calculation | `TradeMarginCheck(login, symbol, type, volume)` |
| 2 | [18b_trade_profit.md](18b_trade_profit.md) | Profit calculation | `TradeProfit(login, symbol, type, volume, open, close)` |

## Server & Configuration

| # | File | Endpoint | Method Signature |
|---|------|----------|-----------------|
| 1 | [15_news.md](15_news.md) | News database | `NewsGet(index)` / `NewsTotal()` |
| 2 | [21_request_get.md](21_request_get.md) | Pending trade requests | `RequestGet(index)` / `RequestTotal()` |
| 3 | [22_leverage_get.md](22_leverage_get.md) | Leverage schedules | `LeverageGet(index)` / `LeverageTotal()` |
| 4 | [23_spread.md](23_spread.md) | Spread configurations | `SpreadNext(index)` / `SpreadTotal()` |
| 5 | [24_holiday.md](24_holiday.md) | Holiday schedules | `HolidayNext(index)` / `HolidayTotal()` |
| 6 | [25_time_server.md](25_time_server.md) | Server time | `TimeServerRequest()` |

---

## Connection Setup

```python
import MT5Manager

manager = MT5Manager.ManagerAPI()

# Pump modes (combine with bitwise OR)
pump_mode = (
    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS     |
    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_POSITIONS  |
    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_ORDERS     |
    MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_SYMBOLS
)

if manager.Connect("server:port", login, "password", pump_mode, 60000):
    # ... use manager ...
    manager.Disconnect()
else:
    print(MT5Manager.LastError())
```

## Error Handling

```python
result = manager.SomeMethod(...)
if result is False:
    code, retcode, message = MT5Manager.LastError()
    print(f"Error {code}: {message} (retcode={retcode})")
```
"""
    write_doc("README.md", index)

    manager.Disconnect()
    log(f"\nDone! All documentation written to: {DOCS_DIR}")
    log(f"Files written: {len(os.listdir(DOCS_DIR))}")


if __name__ == "__main__":
    main()
