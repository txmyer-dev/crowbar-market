# settings.json Reference

`settings.json` is the configuration file Claude Code reads at startup. It controls
who you are, what your AI knows about your environment, and which operations require
your permission.

This file lives at: `~/.claude/settings.json`

---

## What It Controls

| Block | Purpose |
|---|---|
| `principal` | Your name and timezone — injected into every session as context |
| `daidentity` | Your AI's name and display settings |
| `env` | Environment variables available to your AI during sessions |
| `permissions` | Which operations are auto-approved vs. require your confirmation |

---

## Template

Replace every value in `ALL_CAPS` with your own. Do not change the key names.

```json
{
  "principal": {
    "name": "YOUR_NAME",
    "timezone": "YOUR_TIMEZONE"
  },

  "daidentity": {
    "name": "YOUR_AI_NAME",
    "fullName": "YOUR_AI_FULL_NAME",
    "displayName": "YOUR_AI_DISPLAY_NAME",
    "color": "#3B82F6"
  },

  "env": {
    "SNAP_DIR": "/absolute/path/to/.claude",
    "PROJECTS_DIR": "/absolute/path/to/your/projects",
    "ANTHROPIC_MODEL": "claude-opus-4-5",
    "max_tokens_output": "16000",
    "timeout_ms": "120000"
  },

  "permissions": {
    "allow": [
      "Bash(git:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(bun:*)",
      "Bash(node:*)",
      "Read(*)",
      "Write(*)",
      "Edit(*)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": [],
    "ask": [
      "Bash(rm:*)",
      "Bash(rmdir:*)",
      "Bash(curl * | bash:*)",
      "Bash(npm publish:*)",
      "Bash(git push --force:*)"
    ]
  }
}
```

---

## Field Guide

### principal

| Field | Example | Notes |
|---|---|---|
| `name` | `"Jordan"` | First name or whatever you want your AI to call you |
| `timezone` | `"America/Chicago"` | IANA timezone string. Find yours: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones |

### daidentity

| Field | Example | Notes |
|---|---|---|
| `name` | `"Atlas"` | Short name — used in voice notifications and quick references |
| `fullName` | `"Atlas - Personal AI Infrastructure"` | Shown in formal output headers |
| `displayName` | `"Atlas"` | Usually same as `name` unless you want a different display label |
| `color` | `"#3B82F6"` | Hex color — used in any UI that renders your AI's identity |

### env

| Field | Notes |
|---|---|
| `SNAP_DIR` | **Must be an absolute path.** On Windows use forward slashes: `C:/Users/yourname/.claude`. Do not use `~` here. |
| `PROJECTS_DIR` | Where your code projects live. Your AI will know to look here. |
| `ANTHROPIC_MODEL` | Default model for sessions. `claude-opus-4-5` is the standard. |
| `max_tokens_output` | 16000 is a safe default. Raise to 32000 if you do heavy document generation. |
| `timeout_ms` | 120000 = 2 minutes. Raise to 300000 for long-running tasks. |

### permissions

- **allow**: Operations your AI runs without asking. Common tools and read/write are safe here.
- **deny**: Operations that are always blocked, no exceptions.
- **ask**: Operations that pause and wait for your confirmation. Destructive actions go here.

**Leave permissions as the defaults during your Build Session.** Customize them after
you've used the system for a week and know what patterns your workflow creates.

---

## What to Customize vs. Leave Alone

| Customize | Leave As Default |
|---|---|
| `principal.name` and `timezone` | Key names (don't rename fields) |
| `daidentity.*` — all fields | `permissions.allow` list (for now) |
| `SNAP_DIR` and `PROJECTS_DIR` | `ANTHROPIC_MODEL` (unless you have a specific reason) |
| `color` to match your brand | JSON structure and nesting |
