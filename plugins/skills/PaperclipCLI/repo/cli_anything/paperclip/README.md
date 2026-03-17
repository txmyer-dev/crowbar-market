# cli-anything-paperclip

CLI harness for the **Paperclip** agent orchestration platform. Provides both
one-shot subcommands and an interactive REPL for managing companies, agents,
issues, projects, goals, approvals, and costs through the Paperclip REST API.

## Prerequisites

**Paperclip server** is a hard dependency. The CLI communicates with a running
Paperclip instance via its REST API.

```bash
# Start Paperclip (from the paperclip source directory)
cd /path/to/paperclip
pnpm install
pnpm dev
# Server starts at http://localhost:3100
```

Requirements: Node.js 20+, pnpm 9.15+, PostgreSQL (embedded or external).

## Installation

```bash
cd paperclip-source/agent-harness
pip install -e .
```

Verify:

```bash
which cli-anything-paperclip
cli-anything-paperclip --help
```

## Configuration

The CLI reads configuration from environment variables or command-line flags:

| Env Variable           | Flag        | Description                |
|------------------------|-------------|----------------------------|
| `PAPERCLIP_URL`        | `--url`     | Server URL (default: http://localhost:3100) |
| `PAPERCLIP_API_KEY`    | `--api-key` | Agent API key              |
| `PAPERCLIP_COMPANY_ID` | `--company` | Default company context    |

Session state is persisted to `~/.cli-anything-paperclip/session.json`.

## Usage

### REPL Mode (default)

```bash
cli-anything-paperclip
```

Enters an interactive REPL. Type `help` for commands, `quit` to exit.

### One-Shot Commands

```bash
# Check server health
cli-anything-paperclip health

# List companies (JSON output)
cli-anything-paperclip --json company list

# Set active company
cli-anything-paperclip company use <company-id>

# List agents
cli-anything-paperclip agent list

# Create an issue
cli-anything-paperclip issue create -t "Fix authentication bug" --priority high

# View dashboard
cli-anything-paperclip dashboard
```

### Command Groups

- `company` — list, get, create, use, update
- `agent` — list, get, me, create, update, heartbeat, wakeup, state, runs
- `issue` — list, get, create, update, checkout, release, comments, comment, context
- `project` — list, get, create, update, workspace
- `goal` — list, get, create, update
- `approval` — list, get, approve, reject
- `dashboard` — overview stats
- `activity` — audit log
- `costs` — cost tracking
- `health` — server status
- `session` — show, save, clear session state

### JSON Output

Add `--json` flag to any command for machine-readable output:

```bash
cli-anything-paperclip --json agent list
cli-anything-paperclip --json issue get <issue-id>
```

## Running Tests

```bash
cd paperclip-source/agent-harness
pip install -e .
python3 -m pytest cli_anything/paperclip/tests/ -v -s

# Force installed command (CI mode):
CLI_ANYTHING_FORCE_INSTALLED=1 python3 -m pytest cli_anything/paperclip/tests/ -v -s
```

## Architecture

```
cli_anything/paperclip/
├── paperclip_cli.py       # Main CLI (Click + REPL)
├── core/
│   ├── session.py         # Session persistence
│   ├── company.py         # Company operations
│   ├── agent.py           # Agent operations
│   ├── issue.py           # Issue/task operations
│   ├── project.py         # Project operations
│   ├── goal.py            # Goal operations
│   ├── approval.py        # Approval operations
│   └── export.py          # Dashboard, activity, costs
├── utils/
│   ├── paperclip_backend.py  # HTTP client (the backend)
│   └── repl_skin.py          # Unified REPL skin
└── tests/
    ├── TEST.md            # Test plan and results
    ├── test_core.py       # Unit tests
    └── test_full_e2e.py   # E2E tests
```
