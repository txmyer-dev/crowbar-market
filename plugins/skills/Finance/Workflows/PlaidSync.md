---
name: PlaidSync
description: Plaid automated transaction sync management
triggers:
  - plaid
  - plaid sync
  - plaid link
  - plaid status
---

# Plaid Sync Workflow

Manage the automated Plaid → hledger transaction sync system.

## Architecture

- **Sync service:** `/opt/plaid-sync/` on VPS — runs daily at 11 PM via systemd timer
- **Link server:** On-demand Bun+Hono server on port 9876 (start via SSH tunnel when linking new banks)
- **State:** `/opt/plaid-sync/state/items.json` — access tokens + sync cursors
- **Config:** `/opt/plaid-sync/config/` — account mappings + category mappings
- **Source code:** `~/Projects/hledger-finance/plaid/`

## Commands

### Check sync status
```bash
ssh root@76.13.98.215 "systemctl status plaid-sync.timer && journalctl -u plaid-sync --no-pager -n 30"
```

### Run manual sync
```bash
ssh root@76.13.98.215 "cd /opt/plaid-sync && /root/.bun/bin/bun run sync"
```

### Link a new bank
```bash
# 1. Start link server via SSH tunnel
ssh -L 9876:localhost:9876 root@76.13.98.215 "systemctl start plaid-link"

# 2. Create link token
curl -X POST http://localhost:9876/create-link-token \
  -H "Authorization: Bearer <LINK_AUTH_TOKEN>"

# 3. Open hosted_link_url in browser, complete bank login

# 4. Exchange public_token
curl -X POST http://localhost:9876/exchange-token \
  -H "Authorization: Bearer <LINK_AUTH_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"public_token":"public-xxx","institution_name":"Bank Name"}'

# 5. Map accounts in config/accounts.json

# 6. Stop link server
ssh root@76.13.98.215 "systemctl stop plaid-link"
```

### View linked items
```bash
ssh root@76.13.98.215 "cat /opt/plaid-sync/state/items.json | jq '.items[] | {institution: .institution_name, last_sync, status: .last_sync_status, txn_count: .last_txn_count}'"
```

### Deploy updates
```bash
cd ~/Projects/hledger-finance/plaid && bash deploy/install.sh
```
