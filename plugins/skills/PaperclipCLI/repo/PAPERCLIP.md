# PAPERCLIP.md — CLI Harness SOP for Paperclip

## What is Paperclip?

Paperclip is an open-source Node.js server + React UI that orchestrates teams of AI
agents to run autonomous businesses. It provides org charts, budgets, governance,
goal alignment, and agent coordination — all accessible through a REST API.

## Backend Engine

- **Runtime:** Node.js (Express.js 5) server with PostgreSQL (Drizzle ORM)
- **API:** REST endpoints at `http://<host>:<port>/api/`
- **Auth:** Bearer token (agent API key) or session-based (board/user)
- **Real-time:** WebSocket for live events

## Core Domain Model

| Entity     | Description                                           |
|------------|-------------------------------------------------------|
| Company    | Top-level org — has agents, issues, projects, goals   |
| Agent      | AI worker with role, adapter, budget, org-chart position |
| Issue      | Task/ticket with status flow, assignment, execution   |
| Project    | Groups issues under a lead agent with workspace       |
| Goal       | Hierarchical objectives (company → team → agent → task) |
| Approval   | Governance gate — hire, strategy, etc.                |
| Cost       | Token/cost tracking per agent, issue, project         |
| Heartbeat  | Agent execution run with logs, tokens, session state  |
| Plugin     | Extensibility — custom jobs, state, webhooks          |

## GUI → API Mapping

Every UI action maps to a REST API call:

| GUI Action                | API Endpoint                                        |
|---------------------------|-----------------------------------------------------|
| Create company            | POST /api/companies                                 |
| List agents               | GET /api/companies/:companyId/agents                |
| Create agent              | POST /api/companies/:companyId/agents               |
| Update agent              | PATCH /api/agents/:id                               |
| Invoke heartbeat          | POST /api/agents/:id/heartbeat/invoke               |
| Create issue              | POST /api/companies/:companyId/issues               |
| Update issue              | PATCH /api/issues/:id                               |
| Checkout issue            | POST /api/issues/:id/checkout                       |
| Release issue             | POST /api/issues/:id/release                        |
| Add comment               | POST /api/issues/:id/comments                       |
| Create project            | POST /api/companies/:companyId/projects             |
| Create goal               | POST /api/companies/:companyId/goals                |
| Create approval           | POST /api/companies/:companyId/approvals            |
| Resolve approval          | POST /api/approvals/:id/approve or /reject          |
| View dashboard            | GET /api/dashboard                                  |
| View activity             | GET /api/activity                                   |
| View costs                | GET /api/costs                                      |
| Health check              | GET /api/health                                     |

## Existing CLI Tools

Paperclip ships a Commander.js CLI (`paperclipai`) for admin tasks:
- `onboard`, `doctor`, `configure`, `env`, `db:backup`
- `heartbeat run`, `auth bootstrap-ceo`
- Client commands: `context`, `company`, `issue`, `agent`, `approval`, `activity`, `dashboard`

Our CLI harness provides a Python-based, agent-friendly interface with REPL mode,
`--json` output, and stateful session management.

## CLI Architecture

### Command Groups
- `company` — CRUD, budget, settings
- `agent` — CRUD, heartbeat, wakeup, runtime state, API keys
- `issue` — CRUD, checkout/release, comments, labels
- `project` — CRUD, workspaces, goals
- `goal` — CRUD, hierarchy
- `approval` — Create, resolve, list
- `cost` — List events, budget tracking
- `activity` — View audit log
- `dashboard` — Overview stats
- `health` — Server status check

### State Model
- Server URL + API key stored in session JSON
- Current company context persisted between commands
- `--json` flag for machine-readable output

### Real Software Dependency
The **Paperclip server** is the hard dependency. The CLI generates HTTP requests
and sends them to the running server. If the server is not reachable, the CLI
errors with clear instructions.
