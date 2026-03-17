# Agents Workflow

List, inspect, and manage Paperclip agents.

## Intent-to-Action Mapping

| User Says | Action | Command |
|-----------|--------|---------|
| "list agents", "show agents" | List all | `agent list` |
| "wake [agent]", "start [agent]" | Wake agent | `agent wakeup` |
| "agent details", "inspect [agent]" | Get details | `agent get` |
| "agent runtime", "what is [agent] doing" | Runtime state | `agent runtime-state` |
| "heartbeat history" | List runs | `agent heartbeat-runs` |

## List Agents

```bash
cli-anything-paperclip --json agent list
```

## Wake an Agent

```bash
cli-anything-paperclip --json agent wakeup AGENT_ID --reason "REASON"
```

Always include a reason — it appears in the agent's context when it starts.

## Get Agent Details

```bash
cli-anything-paperclip --json agent get AGENT_ID
```

## Get Runtime State

```bash
cli-anything-paperclip --json agent runtime-state AGENT_ID
```

Shows: current session, token usage, cost, active task.

## Heartbeat History

```bash
cli-anything-paperclip --json agent heartbeat-runs --agent-id AGENT_ID --limit 5
```

## Notes

- All agents are event-driven — no heartbeat polling
- Use `wakeup` to activate an agent for a specific task
- Agents return to idle after completing their task
