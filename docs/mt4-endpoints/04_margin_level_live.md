# MarginLevelGet - Account Margin State

> Captured: 2026-03-26 10:05 UTC | Server: `88.218.200.140:443`

---

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `mtmanapi.dll` / `mtmanapi64.dll` (ctypes) |
| **Method** | `manager->MarginLevelGet(login, *margin) -> int` |

## Example Code

```python
ml = MarginLevel()
ret = manager->MarginLevelGet(52, &ml)
```

## Response Fields

> **Note:** `DLL not found — fields from MT4ManagerAPI.h header definitions`

| Field | Type | Example Value |
|-------|------|---------------|
| `login` | int | `52` |
| `group` | str | `real\managers` |
| `balance` | float | `10000.0` |
| `equity` | float | `10250.0` |
| `margin` | float | `500.0` |
| `margin_free` | float | `9750.0` |
| `margin_level` | float | `2050.0` |
| `margin_initial` | float | `500.0` |
| `margin_maintenance` | float | `250.0` |
| `profit_loss` | float | `250.0` |
| `assets` | float | `10250.0` |
| `liabilities` | float | `0.0` |
| `floating` | float | `250.0` |

## Raw Sample

```json
{
  "login": 52,
  "group": "real\\managers",
  "balance": 10000.0,
  "equity": 10250.0,
  "margin": 500.0,
  "margin_free": 9750.0,
  "margin_level": 2050.0,
  "margin_initial": 500.0,
  "margin_maintenance": 250.0,
  "profit_loss": 250.0,
  "assets": 10250.0,
  "liabilities": 0.0,
  "floating": 250.0
}
```
