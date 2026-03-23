# UserGetByGroup - Retrieve Users by Group Mask (Cache)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns a list of MTUser objects from the pump cache matching the group mask. Use `*` to return all users. Supports wildcards like `demo\\*`.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.UserGetByGroup(group_mask: str) -> list[MTUser]` |

## Example Code

```python
users = manager.UserGetByGroup("*")
print(f"Total users: {len(users)}")
for u in users[:5]:
    print(u.Login, u.Name, u.Group, u.Balance, u.Equity)
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
| `Country` | str | `Uganda` |
| `Credit` | float | `0.0` |
| `EMail` | str | `` |
| `EquityPrevDay` | float | `0.0` |
| `EquityPrevMonth` | float | `0.0` |
| `FirstName` | str | `debug` |
| `Group` | str | `demo\NL\ECNPRO\USD` |
| `ID` | str | `` |
| `InterestRate` | float | `0.0` |
| `Language` | int | `9` |
| `LastAccess` | int | `1772811777` |
| `LastIP` | str | `` |
| `LastName` | str | `` |
| `LastPassChange` | int | `1772811777` |
| `LeadCampaign` | str | `` |
| `LeadSource` | str | `` |
| `Leverage` | int | `100` |
| `LimitOrders` | int | `0` |
| `LimitPositionsValue` | float | `0.0` |
| `Login` | int | `1037` |
| `MQID` | str | `0` |
| `MiddleName` | str | `` |
| `Name` | str | `debug` |
| `OTPSecret` | str | `` |
| `Phone` | str | `` |
| `PhonePassword` | str | `` |
| `Registration` | int | `1772811777` |
| `Rights` | int | `2403` |
| `State` | str | `` |
| `Status` | str | `` |
| `VisitorID` | int | `0` |
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
  "Country": "Uganda",
  "Credit": 0.0,
  "EMail": "",
  "EquityPrevDay": 0.0,
  "EquityPrevMonth": 0.0,
  "FirstName": "debug",
  "Group": "demo\\NL\\ECNPRO\\USD",
  "ID": "",
  "InterestRate": 0.0,
  "Language": 9,
  "LastAccess": 1772811777,
  "LastIP": "",
  "LastName": "",
  "LastPassChange": 1772811777,
  "LeadCampaign": "",
  "LeadSource": "",
  "Leverage": 100,
  "LimitOrders": 0,
  "LimitPositionsValue": 0.0,
  "Login": 1037,
  "MQID": "0",
  "MiddleName": "",
  "Name": "debug",
  "OTPSecret": "",
  "Phone": "",
  "PhonePassword": "",
  "Registration": 1772811777,
  "Rights": 2403,
  "State": "",
  "Status": "",
  "VisitorID": 0,
  "ZIPCode": ""
}
```
