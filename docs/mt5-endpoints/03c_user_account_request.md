# UserAccountRequest - Fetch Account Data Directly from Server

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Fetches account financial data directly from the server (not cache). Returns the same fields as `UserAccountGet` but always fresh.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.UserAccountRequest(login: int) -> MTAccount` |

## Example Code

```python
acc = manager.UserAccountRequest(1036)
print(acc.Balance, acc.Equity, acc.Profit)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `Assets` | float | `0.0` |
| `Balance` | float | `0.0` |
| `BlockedCommission` | float | `0.0` |
| `BlockedProfit` | float | `0.0` |
| `Credit` | float | `0.0` |
| `CurrencyDigits` | int | `2` |
| `Equity` | float | `0.0` |
| `Floating` | float | `0.0` |
| `Liabilities` | float | `0.0` |
| `Login` | int | `1036` |
| `Margin` | float | `0.0` |
| `MarginFree` | float | `0.0` |
| `MarginInitial` | float | `0.0` |
| `MarginLevel` | float | `0.0` |
| `MarginLeverage` | int | `100` |
| `MarginMaintenance` | float | `0.0` |
| `ObsoleteValue` | float | `0.0` |
| `Profit` | float | `0.0` |
| `SOActivation` | int | `0` |
| `SOEquity` | float | `0.0` |
| `SOLevel` | float | `0.0` |
| `SOMargin` | float | `0.0` |
| `SOTime` | int | `0` |
| `Storage` | float | `0.0` |


## Raw Sample Response

```json
{
  "Assets": 0.0,
  "Balance": 0.0,
  "BlockedCommission": 0.0,
  "BlockedProfit": 0.0,
  "Credit": 0.0,
  "CurrencyDigits": 2,
  "Equity": 0.0,
  "Floating": 0.0,
  "Liabilities": 0.0,
  "Login": 1036,
  "Margin": 0.0,
  "MarginFree": 0.0,
  "MarginInitial": 0.0,
  "MarginLevel": 0.0,
  "MarginLeverage": 100,
  "MarginMaintenance": 0.0,
  "ObsoleteValue": 0.0,
  "Profit": 0.0,
  "SOActivation": 0,
  "SOEquity": 0.0,
  "SOLevel": 0.0,
  "SOMargin": 0.0,
  "SOTime": 0,
  "Storage": 0.0
}
```
