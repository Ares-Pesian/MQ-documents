# GroupRequestArray - Retrieve All User Groups

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns all groups configured on the MT5 server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.GroupRequestArray() -> list[MTGroup]` |

## Example Code

```python
groups = manager.GroupRequestArray()
for g in groups:
    print(g.Group, g.Currency, g.Leverage, g.Company)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `AuthMode` | int | `0` |
| `AuthOTPMode` | int | `0` |
| `AuthPasswordMin` | int | `8` |
| `Company` | str | `Opo group LLC` |
| `CompanyCatalog` | str | `` |
| `CompanyDepositPage` | str | `` |
| `CompanyEmail` | str | `` |
| `CompanyPage` | str | `MT5-OPOGR-DEV` |
| `CompanySupportEmail` | str | `` |
| `CompanySupportPage` | str | `https://www.mql5.com/[lang:en\|ru\|es\|pt\|zh\|ja\|de\|ko\|fr\|it\|tr]` |
| `CompanyWithdrawalPage` | str | `` |
| `Currency` | str | `USD` |
| `CurrencyDigits` | int | `2` |
| `DemoDeposit` | float | `0.0` |
| `DemoInactivityPeriod` | int | `0` |
| `DemoLeverage` | int | `0` |
| `Group` | str | `managers\administrators` |
| `LimitHistory` | int | `0` |
| `LimitOrders` | int | `0` |
| `LimitPositions` | int | `0` |
| `LimitSymbols` | int | `0` |
| `MailMode` | int | `1` |
| `MarginCall` | float | `50.0` |
| `MarginFlags` | int | `0` |
| `MarginFloatingLeverage` | str | `` |
| `MarginFreeMode` | int | `1` |
| `MarginFreeProfitMode` | int | `0` |
| `MarginMode` | int | `0` |
| `MarginSOMode` | int | `0` |
| `MarginStopOut` | float | `30.0` |
| `NewsCategory` | str | `` |
| `NewsMode` | int | `2` |
| `PermissionsFlags` | int | `2` |
| `ReportsEmail` | str | `` |
| `ReportsFlags` | int | `0` |
| `ReportsMode` | int | `0` |
| `ReportsSMTP` | str | `` |
| `ReportsSMTPLogin` | str | `` |
| `ReportsSMTPPass` | str | `` |
| `Server` | int | `1` |
| `TradeFlags` | int | `31` |
| `TradeInterestrate` | float | `0.0` |
| `TradeTransferMode` | int | `0` |
| `TradeVirtualCredit` | float | `0.0` |


## Raw Sample Response

```json
{
  "AuthMode": 0,
  "AuthOTPMode": 0,
  "AuthPasswordMin": 8,
  "Company": "Opo group LLC",
  "CompanyCatalog": "",
  "CompanyDepositPage": "",
  "CompanyEmail": "",
  "CompanyPage": "MT5-OPOGR-DEV",
  "CompanySupportEmail": "",
  "CompanySupportPage": "https://www.mql5.com/[lang:en|ru|es|pt|zh|ja|de|ko|fr|it|tr]",
  "CompanyWithdrawalPage": "",
  "Currency": "USD",
  "CurrencyDigits": 2,
  "DemoDeposit": 0.0,
  "DemoInactivityPeriod": 0,
  "DemoLeverage": 0,
  "Group": "managers\\administrators",
  "LimitHistory": 0,
  "LimitOrders": 0,
  "LimitPositions": 0,
  "LimitSymbols": 0,
  "MailMode": 1,
  "MarginCall": 50.0,
  "MarginFlags": 0,
  "MarginFloatingLeverage": "",
  "MarginFreeMode": 1,
  "MarginFreeProfitMode": 0,
  "MarginMode": 0,
  "MarginSOMode": 0,
  "MarginStopOut": 30.0,
  "NewsCategory": "",
  "NewsMode": 2,
  "PermissionsFlags": 2,
  "ReportsEmail": "",
  "ReportsFlags": 0,
  "ReportsMode": 0,
  "ReportsSMTP": "",
  "ReportsSMTPLogin": "",
  "ReportsSMTPPass": "",
  "Server": 1,
  "TradeFlags": 31,
  "TradeInterestrate": 0.0,
  "TradeTransferMode": 0,
  "TradeVirtualCredit": 0.0
}
```
