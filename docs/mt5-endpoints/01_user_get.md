# UserGet - Retrieve a Single User from Cache

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Retrieves a single user record from the local pump cache by login number. Requires `PUMP_MODE_USERS` pumping to be active on the connection.

Returns an `MTUser` object on success, or `False` on failure.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.UserGet(login: int) -> MTUser` |

## Example Code

```python
import MT5Manager
manager = MT5Manager.ManagerAPI()
manager.Connect("157.180.9.122:443", 1036, "***",
                MT5Manager.ManagerAPI.EnPumpModes.PUMP_MODE_USERS, 60000)
user = manager.UserGet(1036)
if user is False:
    print(MT5Manager.LastError())
else:
    print(user.Login, user.Name, user.Balance, user.Equity)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `Account` | str | `` |
| `Address` | str | `` |
| `Agent` | int | `0` |
| `Balance` | float | `0.0` |
| `BalancePrevDay` | float | `0.0` |
| `BalancePrevMonth` | float | `0.0` |
| `CertSerialNumber` | int | `0` |
| `City` | str | `` |
| `ClientID` | int | `0` |
| `Color` | int | `4278190080` |
| `Comment` | str | `` |
| `CommissionAgentDaily` | float | `0.0` |
| `CommissionAgentMonthly` | float | `0.0` |
| `CommissionDaily` | float | `0.0` |
| `CommissionMonthly` | float | `0.0` |
| `Company` | str | `` |
| `Country` | str | `Turkiye` |
| `Credit` | float | `0.0` |
| `EMail` | str | `` |
| `EquityPrevDay` | float | `0.0` |
| `EquityPrevMonth` | float | `0.0` |
| `FirstName` | str | `RPG` |
| `Group` | str | `managers\administrators` |
| `ID` | str | `` |
| `InterestRate` | float | `0.0` |
| `Language` | int | `31` |
| `LastAccess` | int | `1774273822` |
| `LastIP` | str | `78.188.40.41` |
| `LastName` | str | `Web` |
| `LastPassChange` | int | `1774273410` |
| `LeadCampaign` | str | `` |
| `LeadSource` | str | `` |
| `Leverage` | int | `100` |
| `LimitOrders` | int | `0` |
| `LimitPositionsValue` | float | `0.0` |
| `Login` | int | `1036` |
| `MQID` | str | `0` |
| `MiddleName` | str | `` |
| `Name` | str | `RPG Web` |
| `OTPSecret` | str | `` |
| `Phone` | str | `` |
| `PhonePassword` | str | `` |
| `Registration` | int | `1772147760` |
| `Rights` | int | `2403` |
| `State` | str | `` |
| `Status` | str | `` |
| `VisitorID` | int | `5188371006944969790` |
| `ZIPCode` | str | `` |


## Raw Sample Response

```json
{
  "Account": "",
  "Address": "",
  "Agent": 0,
  "Balance": 0.0,
  "BalancePrevDay": 0.0,
  "BalancePrevMonth": 0.0,
  "CertSerialNumber": 0,
  "City": "",
  "ClientID": 0,
  "Color": 4278190080,
  "Comment": "",
  "CommissionAgentDaily": 0.0,
  "CommissionAgentMonthly": 0.0,
  "CommissionDaily": 0.0,
  "CommissionMonthly": 0.0,
  "Company": "",
  "Country": "Turkiye",
  "Credit": 0.0,
  "EMail": "",
  "EquityPrevDay": 0.0,
  "EquityPrevMonth": 0.0,
  "FirstName": "RPG",
  "Group": "managers\\administrators",
  "ID": "",
  "InterestRate": 0.0,
  "Language": 31,
  "LastAccess": 1774273822,
  "LastIP": "78.188.40.41",
  "LastName": "Web",
  "LastPassChange": 1774273410,
  "LeadCampaign": "",
  "LeadSource": "",
  "Leverage": 100,
  "LimitOrders": 0,
  "LimitPositionsValue": 0.0,
  "Login": 1036,
  "MQID": "0",
  "MiddleName": "",
  "Name": "RPG Web",
  "OTPSecret": "",
  "Phone": "",
  "PhonePassword": "",
  "Registration": 1772147760,
  "Rights": 2403,
  "State": "",
  "Status": "",
  "VisitorID": 5188371006944969790,
  "ZIPCode": ""
}
```
