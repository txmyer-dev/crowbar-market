---
name: Add
description: Add a transaction to the hledger journal via SSH
triggers:
  - add
  - transaction
---

# Add Transaction Workflow

Add a new transaction entry to Tony's hledger journal on the VPS.

## Steps

1. **Parse the input** — extract date, description, and postings from the user's request.
   - If minimal info given (e.g., "add groceries $45"), construct a full entry:
     - Date: today's date
     - Description: from the user
     - Debit: infer expense category from description
     - Credit: default to `assets:checking`

2. **Format as hledger entry:**
   ```
   2026-03-02 Grocery Store
       expenses:food:groceries       $45.50
       assets:checking
   ```

3. **Append via SSH:**
   ```bash
   bash ~/.claude/skills/Finance/Tools/ssh-hledger.sh append "ENTRY_TEXT"
   ```

4. **Git auto-commit** happens server-side via the API.

5. **Confirm** to Tony with the entry that was added.

## Account Inference

Common mappings for quick adds:
- groceries, food → `expenses:food:groceries`
- restaurant, eating out → `expenses:food:restaurants`
- rent, mortgage → `expenses:housing:rent`
- electric, water, internet → `expenses:housing:utilities`
- gas, uber, lyft → `expenses:transport`
- netflix, spotify → `expenses:subscriptions`
- salary, paycheck → `income:salary`
