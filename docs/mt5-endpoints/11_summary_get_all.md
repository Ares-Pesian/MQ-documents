# SummaryGetAll - Retrieve All Aggregated Position Summaries

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns the aggregated open position summary per symbol across all users.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.SummaryGetAll() -> list[MTSummary]` |

## Example Code

```python
summaries = manager.SummaryGetAll()
for s in summaries:
    print(s.Symbol, s.VolumeExt, s.Profit, s.Buy, s.Sell)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `Digits` | int | `5` |
| `PositionClients` | int | `7` |
| `PositionCoverage` | int | `0` |
| `PriceBuyClients` | float | `0.0` |
| `PriceBuyCoverage` | float | `0.0` |
| `PriceSellClients` | float | `1.15756` |
| `PriceSellCoverage` | float | `0.0` |
| `ProfitClients` | float | `14.53` |
| `ProfitCoverage` | float | `0.0` |
| `ProfitFullClients` | float | `16.91` |
| `ProfitFullCoverage` | float | `0.0` |
| `ProfitUncovered` | float | `14.53` |
| `ProfitUncoveredFull` | float | `16.91` |
| `Symbol` | str | `EURUSD` |
| `VolumeBuyClients` | int | `0` |
| `VolumeBuyClientsExt` | int | `0` |
| `VolumeBuyCoverage` | int | `0` |
| `VolumeBuyCoverageExt` | int | `0` |
| `VolumeNet` | float | `-0.07` |
| `VolumeSellClients` | int | `700` |
| `VolumeSellClientsExt` | int | `7000000` |
| `VolumeSellCoverage` | int | `0` |
| `VolumeSellCoverageExt` | int | `0` |


## Raw Sample Response

```json
{
  "Digits": 5,
  "PositionClients": 7,
  "PositionCoverage": 0,
  "PriceBuyClients": 0.0,
  "PriceBuyCoverage": 0.0,
  "PriceSellClients": 1.15756,
  "PriceSellCoverage": 0.0,
  "ProfitClients": 14.53,
  "ProfitCoverage": 0.0,
  "ProfitFullClients": 16.91,
  "ProfitFullCoverage": 0.0,
  "ProfitUncovered": 14.53,
  "ProfitUncoveredFull": 16.91,
  "Symbol": "EURUSD",
  "VolumeBuyClients": 0,
  "VolumeBuyClientsExt": 0,
  "VolumeBuyCoverage": 0,
  "VolumeBuyCoverageExt": 0,
  "VolumeNet": -0.07,
  "VolumeSellClients": 700,
  "VolumeSellClientsExt": 7000000,
  "VolumeSellCoverage": 0,
  "VolumeSellCoverageExt": 0
}
```
