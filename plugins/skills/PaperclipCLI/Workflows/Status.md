# Status Workflow

Get a comprehensive view of the Paperclip organization — agents, issues, costs.

## Steps

### 1. Get Dashboard Overview

```bash
cli-anything-paperclip --json dashboard
```

### 2. List All Agents with Status

```bash
cli-anything-paperclip --json agent list
```

Display as a table:
| Agent | Role | Status | Last Heartbeat | Monthly Spend |
|-------|------|--------|----------------|---------------|

### 3. Check Pending Issues

```bash
cli-anything-paperclip --json issue list --status in_progress
cli-anything-paperclip --json issue list --status todo
```

### 4. Check Pending Approvals

```bash
cli-anything-paperclip --json approval list --status pending
```

### 5. Cost Summary

```bash
cli-anything-paperclip --json cost summary
```

## Output Format

Present a clean summary:
```
## Paperclip Status — [timestamp]

### Agents (X total)
[table of agents with status]

### Active Work
- [issue title] → assigned to [agent] (status: in_progress)

### Pending Approvals
- [approval type] — requested by [agent]

### Costs (This Month)
- Total: $X.XX
- Top spender: [agent] ($X.XX)
```
