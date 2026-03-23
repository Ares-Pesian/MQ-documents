# DealerBalance - Execute Balance / Credit / Bonus Operation (WRITE)

> Captured: 2026-03-23 11:57 UTC | Server: `157.180.9.122:443`

---

## Overview

Performs a balance, credit, or bonus operation on a user account. Returns the resulting **deal ticket ID** (int) on success, or `False` on failure.

**Supported `EnDealAction` values:**
- `MTDeal.EnDealAction.DEAL_BALANCE` - Balance deposit/withdrawal
- `MTDeal.EnDealAction.DEAL_CREDIT` - Credit in/out
- `MTDeal.EnDealAction.DEAL_BONUS` - Bonus
- `MTDeal.EnDealAction.DEAL_COMMISSION` - Commission

> **WRITE OPERATION** - Response is an integer deal ticket, not an object.

## Endpoint Details

| Property | Value |
|----------|-------|
| **Library** | `MT5Manager` |
| **Method** | `manager.DealerBalance(login: int, amount: float, action: EnDealAction, comment: str) -> int` |

## Example Code

```python
deal_ticket = manager.DealerBalance(
    1036,
    100.0,                                         # amount (positive=deposit)
    MT5Manager.MTDeal.EnDealAction.DEAL_BALANCE,
    "API deposit"
)
if deal_ticket is False:
    print(f"Error: {MT5Manager.LastError()}")
else:
    print(f"Created deal ticket: {deal_ticket}")
```

## Response Fields

| Field | Type | Example Value |
|-------|------|---------------|
| `return_value` | str | `int - deal ticket number of the created balance deal` |
