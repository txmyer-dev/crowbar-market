---
name: Finance
description: Personal finance management via hledger on VPS. Query balances, add transactions, import CSVs, view dashboard.
triggers:
  - finance
  - /finance
  - balance
  - networth
  - net worth
  - hledger
tier: core
---

# Finance — Personal Finance via hledger

Manage Tony's personal finances using hledger plain text accounting hosted on the VPS. All data lives in a git-versioned journal file at `/data/finance/journal.hledger`.

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/finance balance` | Show all account balances | `/finance balance` |
| `/finance networth` | Show net worth (assets - liabilities) | `/finance networth` |
| `/finance add` | Add a transaction to the journal | `/finance add "2026-03-02 Groceries" "expenses:food:groceries $45" "assets:checking"` |
| `/finance expenses [month]` | Monthly expense breakdown | `/finance expenses march` |
| `/finance income [month]` | Income summary | `/finance income` |
| `/finance accounts` | List all account names | `/finance accounts` |
| `/finance import` | Import CSV from bank | `/finance import` |
| `/finance dashboard` | Show dashboard URL | `/finance dashboard` |

## Architecture

- **Data:** `/data/finance/journal.hledger` on VPS (git-versioned)
- **API:** hledger-finance-api container on port 3100 (internal)
- **Dashboard:** Static SPA at private URL via Coolify
- **Communication:** SSH for CLI commands, HTTPS for dashboard API

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Query** | balance, networth, expenses, income, accounts | `Workflows/Query.md` |
| **Add** | add, transaction | `Workflows/Add.md` |
| **Import** | import, csv | `Workflows/Import.md` |
| **InvoiceExtract** | extract invoice, parse invoice, invoice data | `Workflows/InvoiceExtract.md` |

## VPS Connection

```bash
ssh root@76.13.98.215 "hledger -f /data/finance/journal.hledger <command>"
```

Or use the wrapper script: `Tools/ssh-hledger.sh <args>`
