# SymbolGetArray - Retrieve All Available Symbols (Cache)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns the complete list of symbols from the pump cache. Requires `PUMP_MODE_SYMBOLS`.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.SymbolGetArray() -> list[MTSymbol]` |

## Example Code

```python
symbols = manager.SymbolGetArray()
for sym in symbols[:5]:
    print(sym.Symbol, sym.Digits, sym.ContractSize,
          sym.CurrencyBase, sym.CurrencyProfit,
          sym.Spread, sym.SpreadFloat)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `AccruedInterest` | float | `0.0` |
| `Basis` | str | `` |
| `CFI` | str | `` |
| `CalcMode` | int | `0` |
| `Category` | str | `` |
| `ChartMode` | int | `0` |
| `Color` | int | `4278190080` |
| `ColorBackground` | int | `16777184` |
| `ContractSize` | float | `100000.0` |
| `Country` | str | `` |
| `CurrencyBase` | str | `EUR` |
| `CurrencyBaseDigits` | int | `2` |
| `CurrencyMargin` | str | `EUR` |
| `CurrencyMarginDigits` | int | `2` |
| `CurrencyProfit` | str | `USD` |
| `CurrencyProfitDigits` | int | `2` |
| `Description` | str | `Euro vs US Dollar` |
| `Digits` | int | `5` |
| `Exchange` | str | `XCCY` |
| `ExecMode` | int | `2` |
| `ExpirFlags` | int | `15` |
| `FaceValue` | float | `0.0` |
| `FillFlags` | int | `3` |
| `FilterDiscard` | int | `32000` |
| `FilterGap` | int | `0` |
| `FilterGapTicks` | int | `0` |
| `FilterHard` | int | `1600` |
| `FilterHardTicks` | int | `1` |
| `FilterSoft` | int | `50` |
| `FilterSoftTicks` | int | `1` |
| `FilterSpreadMax` | int | `0` |
| `FilterSpreadMin` | int | `0` |
| `FreezeLevel` | int | `0` |
| `GTCMode` | int | `0` |
| `IECheckMode` | int | `0` |
| `IEFlags` | int | `0` |
| `IESlipLosing` | int | `2` |
| `IESlipProfit` | int | `2` |
| `IETimeout` | int | `7` |
| `IEVolumeMax` | int | `0` |
| `IEVolumeMaxExt` | int | `0` |
| `ISIN` | str | `` |
| `Industry` | int | `0` |
| `International` | str | `` |
| `MarginFlags` | int | `0` |
| `MarginHedged` | float | `0.0` |
| `MarginInitial` | float | `0.0` |
| `MarginLimit` | float | `0.0` |
| `MarginLong` | float | `1.0` |
| `MarginMaintenance` | float | `0.0` |
| `MarginRateCurrency` | float | `0.0` |
| `MarginRateLiquidity` | float | `0.0` |
| `MarginShort` | float | `1.0` |
| `MarginStop` | float | `0.0` |
| `MarginStopLimit` | float | `0.0` |
| `Multiply` | float | `100000.0` |
| `OptionsMode` | int | `0` |
| `OrderFlags` | int | `127` |
| `Page` | str | `` |
| `Path` | str | `FX\Forex\EURUSD` |
| `Point` | float | `1e-05` |
| `PriceLimitMax` | float | `0.0` |
| `PriceLimitMin` | float | `0.0` |
| `PriceSettle` | float | `0.0` |
| `PriceStrike` | float | `0.0` |
| `QuotesTimeout` | int | `180` |
| `REFlags` | int | `0` |
| `RETimeout` | int | `7` |
| `Sector` | int | `12` |
| `Source` | str | `` |
| `SpliceTimeDays` | int | `0` |
| `SpliceTimeType` | int | `0` |
| `SpliceType` | int | `0` |
| `Spread` | int | `0` |
| `SpreadBalance` | int | `0` |
| `SpreadDiff` | int | `0` |
| `SpreadDiffBalance` | int | `0` |
| `StopsLevel` | int | `0` |
| `SubscriptionsDelay` | int | `15` |
| `SwapFlags` | int | `0` |
| `SwapLong` | float | `-11.12625` |
| `SwapMode` | int | `1` |
| `SwapRateFriday` | float | `3.0` |
| `SwapRateMonday` | float | `1.0` |
| `SwapRateSaturday` | float | `0.0` |
| `SwapRateSunday` | float | `0.0` |
| `SwapRateThursday` | float | `1.0` |
| `SwapRateTuesday` | float | `1.0` |
| `SwapRateWednesday` | float | `1.0` |
| `SwapShort` | float | `2.5415` |
| `SwapYearDays` | int | `360` |
| `Symbol` | str | `EURUSD` |
| `TickBookDepth` | int | `1` |
| `TickFlags` | int | `1` |
| `TickSize` | float | `0.0` |
| `TickValue` | float | `0.0` |
| `TimeExpiration` | int | `0` |
| `TimeStart` | int | `0` |
| `TradeFlags` | int | `2` |
| `TradeMode` | int | `4` |
| `VolumeLimit` | int | `0` |
| `VolumeLimitExt` | int | `0` |
| `VolumeMax` | int | `500000` |
| `VolumeMaxExt` | int | `5000000000` |
| `VolumeMin` | int | `100` |
| `VolumeMinExt` | int | `1000000` |
| `VolumeStep` | int | `100` |
| `VolumeStepExt` | int | `1000000` |


## Raw Sample Response

```json
{
  "AccruedInterest": 0.0,
  "Basis": "",
  "CFI": "",
  "CalcMode": 0,
  "Category": "",
  "ChartMode": 0,
  "Color": 4278190080,
  "ColorBackground": 16777184,
  "ContractSize": 100000.0,
  "Country": "",
  "CurrencyBase": "EUR",
  "CurrencyBaseDigits": 2,
  "CurrencyMargin": "EUR",
  "CurrencyMarginDigits": 2,
  "CurrencyProfit": "USD",
  "CurrencyProfitDigits": 2,
  "Description": "Euro vs US Dollar",
  "Digits": 5,
  "Exchange": "XCCY",
  "ExecMode": 2,
  "ExpirFlags": 15,
  "FaceValue": 0.0,
  "FillFlags": 3,
  "FilterDiscard": 32000,
  "FilterGap": 0,
  "FilterGapTicks": 0,
  "FilterHard": 1600,
  "FilterHardTicks": 1,
  "FilterSoft": 50,
  "FilterSoftTicks": 1,
  "FilterSpreadMax": 0,
  "FilterSpreadMin": 0,
  "FreezeLevel": 0,
  "GTCMode": 0,
  "IECheckMode": 0,
  "IEFlags": 0,
  "IESlipLosing": 2,
  "IESlipProfit": 2,
  "IETimeout": 7,
  "IEVolumeMax": 0,
  "IEVolumeMaxExt": 0,
  "ISIN": "",
  "Industry": 0,
  "International": "",
  "MarginFlags": 0,
  "MarginHedged": 0.0,
  "MarginInitial": 0.0,
  "MarginLimit": 0.0,
  "MarginLong": 1.0,
  "MarginMaintenance": 0.0,
  "MarginRateCurrency": 0.0,
  "MarginRateLiquidity": 0.0,
  "MarginShort": 1.0,
  "MarginStop": 0.0,
  "MarginStopLimit": 0.0,
  "Multiply": 100000.0,
  "OptionsMode": 0,
  "OrderFlags": 127,
  "Page": "",
  "Path": "FX\\Forex\\EURUSD",
  "Point": 1e-05,
  "PriceLimitMax": 0.0,
  "PriceLimitMin": 0.0,
  "PriceSettle": 0.0,
  "PriceStrike": 0.0,
  "QuotesTimeout": 180,
  "REFlags": 0,
  "RETimeout": 7,
  "Sector": 12,
  "Source": "",
  "SpliceTimeDays": 0,
  "SpliceTimeType": 0,
  "SpliceType": 0,
  "Spread": 0,
  "SpreadBalance": 0,
  "SpreadDiff": 0,
  "SpreadDiffBalance": 0,
  "StopsLevel": 0,
  "SubscriptionsDelay": 15,
  "SwapFlags": 0,
  "SwapLong": -11.12625,
  "SwapMode": 1,
  "SwapRateFriday": 3.0,
  "SwapRateMonday": 1.0,
  "SwapRateSaturday": 0.0,
  "SwapRateSunday": 0.0,
  "SwapRateThursday": 1.0,
  "SwapRateTuesday": 1.0,
  "SwapRateWednesday": 1.0,
  "SwapShort": 2.5415,
  "SwapYearDays": 360,
  "Symbol": "EURUSD",
  "TickBookDepth": 1,
  "TickFlags": 1,
  "TickSize": 0.0,
  "TickValue": 0.0,
  "TimeExpiration": 0,
  "TimeStart": 0,
  "TradeFlags": 2,
  "TradeMode": 4,
  "VolumeLimit": 0,
  "VolumeLimitExt": 0,
  "VolumeMax": 500000,
  "VolumeMaxExt": 5000000000,
  "VolumeMin": 100,
  "VolumeMinExt": 1000000,
  "VolumeStep": 100,
  "VolumeStepExt": 1000000
}
```
