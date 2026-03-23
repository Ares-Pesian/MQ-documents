# PositionRequestByGroup - Fetch All Positions from Server by Group

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Fetches all open positions for users matching the group mask directly from the server.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.PositionRequestByGroup(group_mask: str) -> list[MTPosition]` |

## Example Code

```python
positions = manager.PositionRequestByGroup("*")
print(f"Total open positions: {len(positions)}")
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `Action` | int | `1` |
| `ActionGateway` | int | `0` |
| `ActivationFlags` | int | `0` |
| `ActivationMode` | int | `0` |
| `ActivationPrice` | float | `0.0` |
| `ActivationTime` | int | `0` |
| `Comment` | str | `` |
| `ContractSize` | float | `100000.0` |
| `Dealer` | int | `0` |
| `Digits` | int | `5` |
| `DigitsCurrency` | int | `2` |
| `ExpertID` | int | `0` |
| `ExpertPositionID` | int | `1648` |
| `ExternalID` | str | `` |
| `Login` | int | `1014` |
| `ModificationFlags` | int | `0` |
| `ObsoleteValue` | float | `0.0` |
| `Position` | int | `1648` |
| `PriceCurrent` | float | `1.15558` |
| `PriceGateway` | float | `0.0` |
| `PriceOpen` | float | `1.15755` |
| `PriceSL` | float | `0.0` |
| `PriceTP` | float | `0.0` |
| `Profit` | float | `1.97` |
| `RateMargin` | float | `1.15755` |
| `RateProfit` | float | `1.0` |
| `Reason` | int | `2` |
| `Storage` | float | `0.34` |
| `Symbol` | str | `EURUSD` |
| `TimeCreate` | int | `1773266188` |
| `TimeCreateMsc` | int | `1773266188765` |
| `TimeUpdate` | int | `1773266188` |
| `TimeUpdateMsc` | int | `1773266188765` |
| `Volume` | int | `100` |
| `VolumeExt` | int | `1000000` |
| `VolumeGatewayExt` | int | `0` |


## Raw Sample Response

```json
{
  "Action": 1,
  "ActionGateway": 0,
  "ActivationFlags": 0,
  "ActivationMode": 0,
  "ActivationPrice": 0.0,
  "ActivationTime": 0,
  "Comment": "",
  "ContractSize": 100000.0,
  "Dealer": 0,
  "Digits": 5,
  "DigitsCurrency": 2,
  "ExpertID": 0,
  "ExpertPositionID": 1648,
  "ExternalID": "",
  "Login": 1014,
  "ModificationFlags": 0,
  "ObsoleteValue": 0.0,
  "Position": 1648,
  "PriceCurrent": 1.15558,
  "PriceGateway": 0.0,
  "PriceOpen": 1.15755,
  "PriceSL": 0.0,
  "PriceTP": 0.0,
  "Profit": 1.97,
  "RateMargin": 1.15755,
  "RateProfit": 1.0,
  "Reason": 2,
  "Storage": 0.34,
  "Symbol": "EURUSD",
  "TimeCreate": 1773266188,
  "TimeCreateMsc": 1773266188765,
  "TimeUpdate": 1773266188,
  "TimeUpdateMsc": 1773266188765,
  "Volume": 100,
  "VolumeExt": 1000000,
  "VolumeGatewayExt": 0
}
```
