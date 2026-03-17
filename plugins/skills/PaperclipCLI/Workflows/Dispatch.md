# Dispatch Workflow

Create an issue, assign it to an agent, and wake the agent — all in one shot.

## Intent-to-Flag Mapping

### Agent Selection

| User Says | Agent Name | Role |
|-----------|-----------|------|
| "build", "deploy", "fix", "code", "infrastructure", "DNS", "SSL", "docker", "PR" | Builder | engineer |
| "research", "find", "investigate", "analyze", "OSINT", "compare", "evaluate" | Scout | researcher |
| "write", "draft", "blog", "content", "newsletter", "social", "email" | Writer | engineer |
| "monitor", "check", "health", "status", "uptime", "alert" | Watchdog | engineer |

### Priority Selection

| User Says | Flag | Default |
|-----------|------|---------|
| "urgent", "critical", "asap" | `--priority critical` | medium |
| "important", "high" | `--priority high` | medium |
| "low", "when you get a chance" | `--priority low` | medium |

## Steps

### 1. Identify the Agent

From user request, determine which agent should handle the task using the mapping above.

Look up the agent ID:
```bash
cli-anything-paperclip --json agent list | jq '.[] | select(.name == "AGENT_NAME") | .id'
```

### 2. Create the Issue

```bash
cli-anything-paperclip --json issue create \
  --title "TASK_TITLE" \
  --description "TASK_DESCRIPTION" \
  --priority PRIORITY \
  --assignee-agent-id AGENT_ID
```

### 3. Wake the Agent

```bash
cli-anything-paperclip --json agent wakeup AGENT_ID --reason "New task: TASK_TITLE"
```

### 4. Report Back

Output:
- Issue ID and title
- Assigned agent name
- Agent status (should now be active)
- Estimated: "Agent has been woken and assigned the task"

## Error Handling

- **Server unreachable:** Check if Paperclip server is running at PAPERCLIP_URL
- **Agent not found:** List available agents and suggest the closest match
- **Issue creation failed:** Show the error from the API response
