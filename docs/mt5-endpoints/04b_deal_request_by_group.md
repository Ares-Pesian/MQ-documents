# DealRequestByGroup - Retrieve Deals for All Users by Group Mask

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns all deals for users matching the group mask within a date range.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.DealRequestByGroup(group_mask: str, from: datetime, to: datetime) -> list[MTDeal]` |

## Example Code

```python
import datetime
now = datetime.datetime.now()
from_date = now - datetime.timedelta(days=30)
deals = manager.DealRequestByGroup("*", from_date, now)
print(f"Got {len(deals)} deals across all groups")
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `Action` | int | `2` |
| `ActionGateway` | int | `0` |
| `Comment` | str | `Test` |
| `Commission` | float | `0.0` |
| `ContractSize` | float | `0.0` |
| `Deal` | int | `3` |
| `Dealer` | int | `1002` |
| `Digits` | int | `2` |
| `DigitsCurrency` | int | `2` |
| `Entry` | int | `0` |
| `ExpertID` | int | `0` |
| `ExternalID` | str | `` |
| `Fee` | float | `0.0` |
| `Flags` | int | `0` |
| `Gateway` | str | `` |
| `Login` | int | `1011` |
| `MarketAsk` | float | `0.0` |
| `MarketBid` | float | `0.0` |
| `MarketLast` | float | `0.0` |
| `ModificationFlags` | int | `0` |
| `ObsoleteValue` | float | `0.0` |
| `Order` | int | `0` |
| `PartyID` | int | `0` |
| `PositionID` | int | `0` |
| `Price` | float | `0.0` |
| `PriceGateway` | float | `0.0` |
| `PricePosition` | float | `0.0` |
| `PriceSL` | float | `0.0` |
| `PriceTP` | float | `0.0` |
| `Profit` | float | `10000.0` |
| `ProfitRaw` | float | `0.0` |
| `RateMargin` | float | `0.0` |
| `RateProfit` | float | `0.0` |
| `Reason` | int | `2` |
| `Storage` | float | `0.0` |
| `Symbol` | str | `` |
| `TickSize` | float | `0.0` |
| `TickValue` | float | `0.0` |
| `Time` | int | `1771859202` |
| `TimeMsc` | int | `1771859202353` |
| `Value` | float | `0.0` |
| `Volume` | int | `0` |
| `VolumeClosed` | int | `0` |
| `VolumeClosedExt` | int | `0` |
| `VolumeExt` | int | `0` |
| `VolumeGatewayExt` | int | `0` |


## Raw Sample Response

```json
{
  "Action": 2,
  "ActionGateway": 0,
  "Comment": "Test",
  "Commission": 0.0,
  "ContractSize": 0.0,
  "Deal": 3,
  "Dealer": 1002,
  "Digits": 2,
  "DigitsCurrency": 2,
  "Entry": 0,
  "ExpertID": 0,
  "ExternalID": "",
  "Fee": 0.0,
  "Flags": 0,
  "Gateway": "",
  "Login": 1011,
  "MarketAsk": 0.0,
  "MarketBid": 0.0,
  "MarketLast": 0.0,
  "ModificationFlags": 0,
  "ObsoleteValue": 0.0,
  "Order": 0,
  "PartyID": 0,
  "PositionID": 0,
  "Price": 0.0,
  "PriceGateway": 0.0,
  "PricePosition": 0.0,
  "PriceSL": 0.0,
  "PriceTP": 0.0,
  "Profit": 10000.0,
  "ProfitRaw": 0.0,
  "RateMargin": 0.0,
  "RateProfit": 0.0,
  "Reason": 2,
  "Storage": 0.0,
  "Symbol": "",
  "TickSize": 0.0,
  "TickValue": 0.0,
  "Time": 1771859202,
  "TimeMsc": 1771859202353,
  "Value": 0.0,
  "Volume": 0,
  "VolumeClosed": 0,
  "VolumeClosedExt": 0,
  "VolumeExt": 0,
  "VolumeGatewayExt": 0
}
```
