---
name: PaperclipCLI
description: CLI management of Paperclip agent orchestration. USE WHEN paperclip, dispatch agent, wake agent, list agents, agent status, create issue, paperclip CLI, assign task to agent, check agent, paperclip dashboard, agent costs.
---

# PaperclipCLI

CLI interface for managing the Paperclip agent orchestration platform. Dispatch tasks, wake agents, manage issues, and check status — all from the terminal.

## Prerequisites

**First-time setup:** Clone and install the CLI tool:
```bash
cd ~/.claude/skills/PaperclipCLI && git clone https://github.com/txmyer-dev/cli-anything-paperclip.git repo
cd repo && pip install -e .
```

**Environment variables** (set in shell profile or per-session):
```bash
export PAPERCLIP_URL="https://thecrowbarcrew.cc"
export PAPERCLIP_API_KEY="<agent-api-key>"
export PAPERCLIP_COMPANY_ID="1c1a6b91"
```

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Dispatch** | "dispatch to agent", "send task to Builder", "tell Scout to" | `Workflows/Dispatch.md` |
| **Status** | "agent status", "what are agents doing", "paperclip status" | `Workflows/Status.md` |
| **Agents** | "list agents", "manage agents", "wake agent" | `Workflows/Agents.md` |
| **Issues** | "create issue", "list issues", "assign issue" | `Workflows/Issues.md` |

## Quick Reference

**Agents available (Ekko-as-CEO roster):**
- **Builder** (Sonnet) — code, PRs, deploys, infrastructure, DNS, SSL, CI/CD, bug fixes
- **Scout** (Sonnet) — research, analysis, OSINT, competitive intelligence, technical evaluation
- **Writer** (Sonnet) — content, blog posts, newsletters, social media, SecondBrain entries
- **Watchdog** (Haiku) — monitoring, health check investigation (event-driven only, woken by n8n)

**Key design principles:**
- All agents are event-driven (no heartbeat polling)
- Two-tier triage: n8n keyword routing (70%) → Ekko handles ambiguous (30%)
- Agents deliver to Ekko (QA gate), not directly to Tony
- Architecture: n8n triggers → keyword route or Ekko triage → Paperclip dispatch → agent executes

## Examples

**Example 1: Dispatch a task to an agent**
```
User: "Tell Builder to fix the client health check"
→ Invokes Dispatch workflow
→ Creates issue, assigns to Builder, wakes Builder
→ Reports issue ID and agent status
```

**Example 2: Check what agents are doing**
```
User: "What's the paperclip status?"
→ Invokes Status workflow
→ Lists all agents with current state, last activity, spend
→ Shows pending issues and approvals
```

**Example 3: Wake an agent for a specific reason**
```
User: "Wake up Writer to draft the weekly newsletter"
→ Invokes Agents workflow
→ Sends wakeup request with reason
→ Confirms agent is active
```
