# HistoryRequestByGroup - Historical Orders by Group Mask

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns historical orders for all users matching the group mask within the date range.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.HistoryRequestByGroup(group_mask: str, from: datetime, to: datetime) -> list[MTOrder]` |

## Example Code

```python
import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=30)
orders = manager.HistoryRequestByGroup("*", from_date, now)
print(f"Total: {len(orders)} history orders")
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `ActivationFlags` | int | `0` |
| `ActivationMode` | int | `0` |
| `ActivationPrice` | float | `0.0` |
| `ActivationTime` | int | `0` |
| `Comment` | str | `` |
| `ContractSize` | float | `100.0` |
| `Dealer` | int | `0` |
| `Digits` | int | `2` |
| `DigitsCurrency` | int | `2` |
| `ExpertID` | int | `0` |
| `ExternalID` | str | `` |
| `Login` | int | `1011` |
| `ModificationFlags` | int | `0` |
| `Order` | int | `7` |
| `PartyID` | int | `0` |
| `PositionByID` | int | `0` |
| `PositionID` | int | `7` |
| `PriceCurrent` | float | `5155.48` |
| `PriceOrder` | float | `0.0` |
| `PriceSL` | float | `0.0` |
| `PriceTP` | float | `0.0` |
| `PriceTrigger` | float | `0.0` |
| `RateMargin` | float | `1.0` |
| `Reason` | int | `0` |
| `State` | int | `4` |
| `Symbol` | str | `XAUUSD` |
| `TimeDone` | int | `1771859334` |
| `TimeDoneMsc` | int | `1771859334034` |
| `TimeExpiration` | int | `0` |
| `TimeSetup` | int | `1771859334` |
| `TimeSetupMsc` | int | `1771859334029` |
| `Type` | int | `1` |
| `TypeFill` | int | `1` |
| `TypeTime` | int | `0` |
| `VolumeCurrent` | int | `0` |
| `VolumeCurrentExt` | int | `0` |
| `VolumeInitial` | int | `100` |
| `VolumeInitialExt` | int | `1000000` |


## Raw Sample Response

```json
{
  "ActivationFlags": 0,
  "ActivationMode": 0,
  "ActivationPrice": 0.0,
  "ActivationTime": 0,
  "Comment": "",
  "ContractSize": 100.0,
  "Dealer": 0,
  "Digits": 2,
  "DigitsCurrency": 2,
  "ExpertID": 0,
  "ExternalID": "",
  "Login": 1011,
  "ModificationFlags": 0,
  "Order": 7,
  "PartyID": 0,
  "PositionByID": 0,
  "PositionID": 7,
  "PriceCurrent": 5155.48,
  "PriceOrder": 0.0,
  "PriceSL": 0.0,
  "PriceTP": 0.0,
  "PriceTrigger": 0.0,
  "RateMargin": 1.0,
  "Reason": 0,
  "State": 4,
  "Symbol": "XAUUSD",
  "TimeDone": 1771859334,
  "TimeDoneMsc": 1771859334034,
  "TimeExpiration": 0,
  "TimeSetup": 1771859334,
  "TimeSetupMsc": 1771859334029,
  "Type": 1,
  "TypeFill": 1,
  "TypeTime": 0,
  "VolumeCurrent": 0,
  "VolumeCurrentExt": 0,
  "VolumeInitial": 100,
  "VolumeInitialExt": 1000000
}
```
