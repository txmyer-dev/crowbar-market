---
name: AsyncWorker
description: Dispatch tasks to the VPS async worker. USE WHEN async, VPS task, remote task, background work, delegate to VPS, run on server, async worker, event-space task.
---

# AsyncWorker

Dispatch tasks to the SNAP Async Worker running on the Hostinger VPS. Tasks run headless via Claude Code on the server, save output as markdown, and notify via ntfy.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/AsyncWorker/`

If this directory exists, load and apply:
- `PREFERENCES.md` - User preferences and configuration

These define user-specific preferences. If the directory does not exist, proceed with skill defaults.

## Infrastructure

- **VPS:** root@76.13.98.215 (Hostinger KVM2, Ubuntu 24.04 + Coolify)
- **Worker:** systemd service `pai-async-worker` on port 7777 (localhost only)
- **Auth:** Token in `/opt/async-worker/.env` on VPS
- **Outputs:** `/opt/async-worker/outputs/` on VPS
- **Clients:** `/opt/async-worker/clients/{name}/CLAUDE.md`
- **ntfy topic:** `pai-worker`

## Usage

```
/async <task description>                    # Generic task
/async <task description> --client event-space  # Task with client context
/async --status <task-id>                    # Check task status
/async --list                                # List active tasks
/async --clients                             # List available clients
/async --output <task-id>                    # Fetch task output
/async --health                              # Check worker health
```

## Workflow: Dispatch

**When invoked with a task:**

1. **Get auth token** from VPS:
   ```bash
   AUTH=$(ssh -o ConnectTimeout=5 root@76.13.98.215 "grep WORKER_AUTH_TOKEN /opt/async-worker/.env | cut -d= -f2")
   ```

2. **Build the payload.** If `--client` is specified, include `"client": "<name>"` in the JSON. Otherwise, send a generic task.

3. **POST to the worker:**
   ```bash
   ssh root@76.13.98.215 "curl -s -X POST \
     -H 'Authorization: Bearer ${AUTH}' \
     -H 'Content-Type: application/json' \
     -d '<payload>' \
     http://127.0.0.1:7777/task"
   ```

4. **Report the task ID** to the user immediately. The task runs async on the VPS.

5. **Optionally poll for results** — if the user seems to want the result now, poll every 10 seconds up to 60 seconds:
   ```bash
   ssh root@76.13.98.215 "curl -s -H 'Authorization: Bearer ${AUTH}' http://127.0.0.1:7777/task/<task-id>"
   ```

6. **When complete, fetch and display the output:**
   ```bash
   ssh root@76.13.98.215 "ls -t /opt/async-worker/outputs/<task-id>* | head -1 | xargs cat"
   ```

## Workflow: Status Check

**When invoked with `--status`, `--list`, `--health`, or `--clients`:**

| Flag | Command |
|------|---------|
| `--health` | `curl -s -H 'Authorization: Bearer ${AUTH}' http://127.0.0.1:7777/health` |
| `--list` | `curl -s -H 'Authorization: Bearer ${AUTH}' http://127.0.0.1:7777/tasks` |
| `--clients` | `curl -s -H 'Authorization: Bearer ${AUTH}' http://127.0.0.1:7777/clients` |
| `--status <id>` | `curl -s -H 'Authorization: Bearer ${AUTH}' http://127.0.0.1:7777/task/<id>` |
| `--output <id>` | `ls -t /opt/async-worker/outputs/<id>* \| head -1 \| xargs cat` |

All commands run via SSH to the VPS. Auth token is fetched fresh each time.

## Output Format

Report results in this format:

```
ASYNC WORKER — Task Dispatched
Task ID:  <task-id>
Client:   <client or "generic">
Status:   <accepted/running/completed/failed>
Task:     <description>

[If completed, show the output content]
[If accepted/running, show: "Task running on VPS. Check with /async --status <id>"]
```

## Available Clients

| Client | Context File | Description |
|--------|-------------|-------------|
| `event-space` | 374 lines, 57 placeholders | AI Chief of Staff for event space business |

New clients are added by creating a directory in `/opt/async-worker/clients/<name>/` with a `CLAUDE.md` file and optional `data/` directory.

## Error Handling

- If SSH fails: report connection error, suggest checking VPS status
- If worker returns 401: auth token mismatch, re-check `/opt/async-worker/.env`
- If worker returns 400: missing task field or invalid client name
- If task fails: check logs at `/opt/async-worker/logs/<task-id>*.log`
