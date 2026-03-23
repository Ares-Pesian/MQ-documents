# TickStat - Get Daily Tick Statistics for a Symbol

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Returns current daily tick statistics (high/low bid/ask) for a symbol.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.TickStat(symbol: str) -> MTTickStat` |

## Example Code

```python
stat = manager.TickStat("EURUSD")
print(stat.datetime, stat.bid_high, stat.bid_low, stat.ask_high, stat.ask_low)
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `ask_high` | float | `1.16205` |
| `ask_low` | float | `1.14845` |
| `bid_high` | float | `1.1620300000000001` |
| `bid_low` | float | `1.14835` |
| `datetime` | int | `1774274272` |
| `datetime_msc` | int | `1774274272260` |
| `last_high` | float | `0.0` |
| `last_low` | float | `0.0` |
| `price_aw` | float | `0.0` |
| `price_close` | float | `1.15713` |
| `price_greeks_delta` | float | `0.0` |
| `price_greeks_gamma` | float | `0.0` |
| `price_greeks_omega` | float | `0.0` |
| `price_greeks_rho` | float | `0.0` |
| `price_greeks_theta` | float | `0.0` |
| `price_greeks_vega` | float | `0.0` |
| `price_obsolete` | float | `2.6e-322` |
| `price_open` | float | `1.15416` |
| `price_sensitivity` | float | `0.0` |
| `price_theoretical` | float | `0.0` |
| `price_volatility` | float | `0.0` |
| `symbol` | str | `EURUSD` |
| `trade_buy_orders` | int | `0` |
| `trade_buy_volume` | int | `0` |
| `trade_buy_volume_ext` | int | `0` |
| `trade_deals` | int | `0` |
| `trade_interest` | int | `0` |
| `trade_sell_orders` | int | `0` |
| `trade_sell_volume` | int | `0` |
| `trade_sell_volume_ext` | int | `0` |
| `trade_turnover` | int | `0` |
| `trade_volume` | int | `0` |
| `trade_volume_ext` | int | `0` |
| `vol_high` | int | `0` |
| `vol_high_ext` | int | `0` |
| `vol_low` | int | `0` |
| `vol_low_ext` | int | `0` |


## Raw Sample Response

```json
{
  "ask_high": 1.16205,
  "ask_low": 1.14845,
  "bid_high": 1.1620300000000001,
  "bid_low": 1.14835,
  "datetime": 1774274272,
  "datetime_msc": 1774274272260,
  "last_high": 0.0,
  "last_low": 0.0,
  "price_aw": 0.0,
  "price_close": 1.15713,
  "price_greeks_delta": 0.0,
  "price_greeks_gamma": 0.0,
  "price_greeks_omega": 0.0,
  "price_greeks_rho": 0.0,
  "price_greeks_theta": 0.0,
  "price_greeks_vega": 0.0,
  "price_obsolete": 2.6e-322,
  "price_open": 1.15416,
  "price_sensitivity": 0.0,
  "price_theoretical": 0.0,
  "price_volatility": 0.0,
  "symbol": "EURUSD",
  "trade_buy_orders": 0,
  "trade_buy_volume": 0,
  "trade_buy_volume_ext": 0,
  "trade_deals": 0,
  "trade_interest": 0,
  "trade_sell_orders": 0,
  "trade_sell_volume": 0,
  "trade_sell_volume_ext": 0,
  "trade_turnover": 0,
  "trade_volume": 0,
  "trade_volume_ext": 0,
  "vol_high": 0,
  "vol_high_ext": 0,
  "vol_low": 0,
  "vol_low_ext": 0
}
```
