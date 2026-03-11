---
name: Query
description: Query financial data via SSH to VPS hledger
triggers:
  - balance
  - networth
  - net worth
  - expenses
  - income
  - accounts
---

# Query Workflow

Run hledger queries against Tony's journal on the VPS.

## Steps

1. **Parse the command** — determine which hledger subcommand to run:
   - `balance` → `hledger bal`
   - `networth` → `hledger bal assets liabilities --depth=1 --total`
   - `expenses [period]` → `hledger bal expenses --flat [--monthly] [-p period]`
   - `income [period]` → `hledger is [--monthly] [-p period]`
   - `accounts` → `hledger accounts`

2. **Execute via SSH:**
   ```bash
   bash ~/.claude/skills/Finance/Tools/ssh-hledger.sh bal
   ```

3. **Format and return** the output to Tony. For net worth, highlight the total. For expenses, show the breakdown by category.

## Period Formats

hledger accepts natural periods: `this month`, `last month`, `2026-03`, `2026Q1`, `this year`
