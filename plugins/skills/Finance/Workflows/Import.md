---
name: Import
description: Import bank CSV transactions into hledger journal
triggers:
  - import
  - csv
---

# CSV Import Workflow

Import bank transaction CSVs into Tony's hledger journal.

## Steps

1. **Get the CSV file** — either:
   - Tony provides a file path to a downloaded CSV
   - Tony pastes CSV data directly

2. **Identify the bank** — check if a rules file exists in `/data/finance/rules/`:
   - `sample-bank.rules` (generic fallback)
   - Future: `chase.rules`, `bofa.rules`, etc.

3. **Upload CSV to VPS** via SCP:
   ```bash
   scp /path/to/transactions.csv root@76.13.98.215:/data/finance/import/
   ```

4. **Run hledger import** via SSH:
   ```bash
   bash ~/.claude/skills/Finance/Tools/ssh-hledger.sh import /data/finance/import/transactions.csv --rules-file /data/finance/rules/sample-bank.rules
   ```

5. **Verify** — run `hledger bal` to confirm the new transactions were imported.

6. **Git auto-commit** happens automatically on the server.

## Creating New Bank Rules

When Tony provides a CSV from a new bank:
1. Read the header row to identify column positions
2. Create a new `.rules` file mapping those columns
3. Upload the rules file to `/data/finance/rules/` on VPS
4. Test with a small sample before full import
