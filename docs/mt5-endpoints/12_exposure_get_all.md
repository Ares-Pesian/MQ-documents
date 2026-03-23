# ExposureGetAll - Retrieve Currency Exposure

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns total currency exposure (net positions per currency) across all users.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.ExposureGetAll() -> list[MTExposure]` |

## Example Code

```python
exposures = manager.ExposureGetAll()
for e in exposures:
    print(e.Symbol, e.Volume, e.Profit)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `Digits` | int | `5` |
| `PriceRate` | float | `1.155445` |
| `Symbol` | str | `EUR` |
| `VolumeClients` | float | `-7000.0` |
| `VolumeCoverage` | float | `0.0` |
| `VolumeNet` | float | `-8088.12` |


## Raw Sample Response

```json
{
  "Digits": 5,
  "PriceRate": 1.155445,
  "Symbol": "EUR",
  "VolumeClients": -7000.0,
  "VolumeCoverage": 0.0,
  "VolumeNet": -8088.12
}
```
