# MT4 Manager API — Complete Endpoint Reference

> **Library:** `mtmanapi.dll` (32-bit) / `mtmanapi64.dll` (64-bit) via Python `ctypes`
> **Server:** `88.218.200.140:443` | **Manager Login:** `52`

---

## How MT4 Manager API Works (vs MT5)

| Aspect | MT5 | MT4 |
|--------|-----|-----|
| Python access | `pip install MT5Manager` | `ctypes` + native DLL |
| DLL required | No | **Yes** — `mtmanapi.dll` or `mtmanapi64.dll` |
| Protocol | Proprietary TCP (handled by library) | Proprietary binary TCP with RSA auth (handled by DLL) |
| Get DLL from | PyPI | MetaQuotes developer portal |
| 64-bit support | Full | Partial (no mail/news in 64-bit DLL) |

## Getting the DLL

1. Register at `https://developers.metaquotes.net`
2. Download the **MetaTrader 4 Manager API SDK**
3. Extract `mtmanapi.dll` (32-bit) or `mtmanapi64.dll` (64-bit)
4. Place the DLL in your project directory or in a Windows PATH directory
5. Use 32-bit Python with 32-bit DLL, or 64-bit Python with 64-bit DLL

---

## Quick Start

```python
import ctypes

# Load DLL (64-bit version shown)
dll = ctypes.WinDLL("mtmanapi64.dll")
dll.MtManCreate.restype  = ctypes.c_void_p
dll.MtManCreate.argtypes = [ctypes.c_uint]

# Create manager interface
mgr = dll.MtManCreate(0x0001)  # AUTO_RELEASE_VERSION

# Connect and login
# (use vtable via CManagerFactory in MT4ManagerAPI.h)
# manager->Connect("88.218.200.140:443")
# manager->Login(52, "Vista1234$")

# Use the API...
# manager->Disconnect()
# manager->Release()
```

See `collect_mt4_responses.py` for the complete production-ready wrapper.

---

## All Endpoints

### Connect & Session

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 1 | [_connection_setup.md](_connection_setup.md) | Setup & DLL loading | `MtManCreate` / `CManagerFactory` |
| 2 | [01_connect_login.md](01_connect_login.md) | Connect + authenticate | `Connect` / `Login` / `ManagerRights` |

### Users

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 3 | [02_user_record.md](02_user_record.md) | All users / single user | `UsersRequest` / `UserRecordGet` |
| — | [02_user_record.md](02_user_record.md) | Create user (WRITE) | `UserRecordNew` |
| — | [02_user_record.md](02_user_record.md) | Update user (WRITE) | `UserRecordUpdate` |
| — | [02_user_record.md](02_user_record.md) | Change password (WRITE) | `UserPasswordSet` |
| — | [02_user_record.md](02_user_record.md) | Verify password | `UserPasswordCheck` |
| — | [02_user_record.md](02_user_record.md) | Group operations (WRITE) | `UsersGroupOp` |
| — | [02_user_record.md](02_user_record.md) | Balance check | `AdmBalanceCheck` |

### Trades & Positions

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 4 | [03_trade_record.md](03_trade_record.md) | All open trades | `TradesRequest` / `TradesGet` |
| — | [03_trade_record.md](03_trade_record.md) | Trades by symbol | `TradesGetBySymbol` |
| — | [03_trade_record.md](03_trade_record.md) | Trades by login | `TradesGetByLogin` |
| — | [03_trade_record.md](03_trade_record.md) | Trade history for user | `TradesUserHistory` |
| — | [03_trade_record.md](03_trade_record.md) | Trades by ticket list | `TradeRecordsRequest` |
| — | [03_trade_record.md](03_trade_record.md) | Calculate trade profit | `TradeCalcProfit` |
| — | [03_trade_record.md](03_trade_record.md) | Validate stop levels | `TradeCheckStops` |
| 5 | [13_trade_transaction.md](13_trade_transaction.md) | Open / Close / Modify (WRITE) | `TradeTransaction` |
| — | [13_trade_transaction.md](13_trade_transaction.md) | Balance / Credit (WRITE) | `TradeTransaction(TT_BR_BALANCE)` |

### Margin & Risk

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 6 | [04_margin_level.md](04_margin_level.md) | Single account margin | `MarginLevelGet` |
| — | [04_margin_level.md](04_margin_level.md) | Multiple accounts margin | `MarginsGet` |

### Online Connections

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 7 | [05_online_record.md](05_online_record.md) | All online clients | `OnlineRequest` / `OnlineGet` |
| — | [05_online_record.md](05_online_record.md) | Single client | `OnlineRecordGet` |

### Symbols & Prices

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 8 | [06_symbol_info.md](06_symbol_info.md) | All symbol configs | `SymbolsGetAll` / `SymbolsRefresh` |
| — | [06_symbol_info.md](06_symbol_info.md) | Single symbol config | `SymbolGet` |
| — | [06_symbol_info.md](06_symbol_info.md) | Market watch snapshot | `SymbolInfoGet` / `SymbolInfoUpdated` |
| 9 | [08_chart_ticks.md](08_chart_ticks.md) | OHLCV bar history | `ChartRequest` |
| — | [08_chart_ticks.md](08_chart_ticks.md) | Raw tick history | `TicksRequest` |
| — | [08_chart_ticks.md](08_chart_ticks.md) | Last N ticks | `TickInfoLast` |

### Aggregates

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 10 | [07_summary_exposure.md](07_summary_exposure.md) | All symbol summaries | `SummaryGetAll` / `SummaryGet` |
| — | [07_summary_exposure.md](07_summary_exposure.md) | Currency exposure | `ExposureGet` / `ExposureValueGet` |

### Groups & Configuration

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 11 | [11_groups_config.md](11_groups_config.md) | All groups | `GroupsRequest` / `GroupsGet` |
| — | [11_groups_config.md](11_groups_config.md) | Single group config | `GroupRecordGet` |
| — | [11_groups_config.md](11_groups_config.md) | Admin group config | `CfgRequestGroups` / `CfgUpdateGroup` |

### Reports

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 12 | [09_daily_reports.md](09_daily_reports.md) | Daily account snapshots | `DailyReportsRequest` |
| — | [09_daily_reports.md](09_daily_reports.md) | Closed position history | `ReportsRequest` |

### Mail & News *(32-bit DLL only)*

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 13 | [10_news_mail.md](10_news_mail.md) | Internal mail | `MailsRequest` / `MailLast` |
| — | [10_news_mail.md](10_news_mail.md) | News headers | `NewsGet` / `NewsTopicGet` |
| — | [10_news_mail.md](10_news_mail.md) | News body | `NewsBodyRequest` / `NewsBodyGet` |
| — | [10_news_mail.md](10_news_mail.md) | Send mail (WRITE) | `MailSend` |
| — | [10_news_mail.md](10_news_mail.md) | Send push notification (WRITE) | `NotificationsSend` |

### Server & Diagnostics

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 14 | [12_server_journal.md](12_server_journal.md) | Server time | `ServerTime` |
| — | [12_server_journal.md](12_server_journal.md) | Server journal/logs | `JournalRequest` |
| — | [12_server_journal.md](12_server_journal.md) | Performance metrics | `PerformanceRequest` |

### Pumping (Real-Time Streaming)

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 15 | [14_pumping_mode.md](14_pumping_mode.md) | Start pumping | `PumpingSwitch` |
| — | [14_pumping_mode.md](14_pumping_mode.md) | Extended pumping | `PumpingSwitchEx` |

### Backup

| # | File | Endpoint | Method |
|---|------|----------|--------|
| 16 | [15_backup.md](15_backup.md) | List backup files | `BackupInfoUsers` / `BackupInfoOrders` |
| — | [15_backup.md](15_backup.md) | Read from backup | `BackupRequestUsers` / `BackupRequestOrders` |
| — | [15_backup.md](15_backup.md) | Restore from backup (WRITE) | `BackupRestoreUsers` / `BackupRestoreOrders` |

---

## Structure Overview

| Structure | File | Description |
|-----------|------|-------------|
| `UserRecord` | [02_user_record.md](02_user_record.md) | Full client account record |
| `TradeRecord` | [03_trade_record.md](03_trade_record.md) | Trade / order / balance record |
| `MarginLevel` | [04_margin_level.md](04_margin_level.md) | Account margin state |
| `OnlineRecord` | [05_online_record.md](05_online_record.md) | Connected client info |
| `ConSymbol` | [06_symbol_info.md](06_symbol_info.md) | Full symbol configuration |
| `SymbolInfo` | [06_symbol_info.md](06_symbol_info.md) | Market Watch snapshot (bid/ask) |
| `SymbolSummary` | [07_summary_exposure.md](07_summary_exposure.md) | Aggregated open interest |
| `ExposureValue` | [07_summary_exposure.md](07_summary_exposure.md) | Currency exposure |
| `RateInfo` | [08_chart_ticks.md](08_chart_ticks.md) | OHLCV bar |
| `TickAPI` | [08_chart_ticks.md](08_chart_ticks.md) | Historical tick |
| `TickInfo` | [08_chart_ticks.md](08_chart_ticks.md) | Last tick (pumping) |
| `DailyReport` | [09_daily_reports.md](09_daily_reports.md) | End-of-day account snapshot |
| `MailBoxHeader` | [10_news_mail.md](10_news_mail.md) | Internal mail header |
| `NewsTopic` | [10_news_mail.md](10_news_mail.md) | News item header |
| `ConGroup` | [11_groups_config.md](11_groups_config.md) | Account group configuration |
| `TradeTransInfo` | [13_trade_transaction.md](13_trade_transaction.md) | Trade request (for execution) |
| `LogInfo` | [12_server_journal.md](12_server_journal.md) | Server journal entry |

---

## Key Differences from MT4 to MT5

| Feature | MT4 | MT5 |
|---------|-----|-----|
| Positions | `TradeRecord` (cmd=0,1) | `MTPosition` |
| Pending orders | `TradeRecord` (cmd=2–5) | `MTOrder` |
| History orders | `TradeRecord` (close_time>0) | `MTOrder` (state=filled) |
| Deals | Not separate — same `TradeRecord` | `MTDeal` (separate from positions) |
| Balance ops | `TradeRecord` (cmd=6,7) | `MTDeal` (action=DEAL_BALANCE) |
| Netting | Yes (one position per symbol) | Both netting and hedging |
| Groups | `ConGroup` | `MTGroup` |
