---
name: Goodbye
description: Session exit protocol. Saves state, updates Soul/Brain/Heart, triggers Catch Me Up via n8n. USE WHEN goodbye, end session, /goodbye, session end, signing off.
version: 1.0.0
---

# Goodbye - Session Exit Protocol

End-of-session skill that captures work state and triggers the Catch Me Up pipeline.

## When to Use

- User says "goodbye", "end session", "signing off", or `/goodbye`
- Session is approaching context limits
- User is done for the day/night

## Workflow

### Step 1: Capture Session State

Review the current session and build a handoff document with these sections:

```yaml
in_progress:
  - List of tasks/projects actively being worked on
decisions:
  - Key decisions made during this session
files_modified:
  - Files changed with brief context for each
blockers:
  - Any unresolved errors or blocking issues
next_steps:
  - What the next session should pick up
```

Write this to `~/.claude/MEMORY/STATE/handoff.md` in markdown format:

```markdown
# Session Handoff - {YYYY-MM-DD HH:MM} GMT

## In Progress
- {item}

## Decisions Made
- {item}

## Modified Files
- `{path}` - {context}

## Next Steps
- {item}

## Blockers
- {item or "None"}
```

### Step 2: Update Memory (if applicable)

Check if any **stable patterns** were confirmed during this session that should be saved to MEMORY.md. Only update if:
- A new convention was established
- A recurring problem was solved
- A user preference was expressed
- Infrastructure changed

Do NOT save session-specific state to MEMORY.md (that goes in handoff.md).

### Step 3: Trigger Catch Me Up

POST the session summary to the n8n webhook so the dashboard gets updated:

```bash
curl -s -X POST https://n8n.felaniam.cloud/webhook/catch-me-up \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "'$(date -u +%Y-%m-%dT%H:%M:%SZ)'",
    "completed": ["short description of each thing shipped/completed this session"],
    "handoff": {
      "in_progress": [...],
      "decisions": [...],
      "next_steps": [...],
      "blockers": [...]
    }
  }' > /dev/null 2>&1
```

The `completed` array should contain brief, human-readable descriptions of what was built, fixed, or shipped during this session (e.g., "RSS Feed Scorer deployed to VPS", "Fixed wallpaper API to use IDesktopWallpaper"). These populate the "Completed Today" section on the status dashboard.

### Step 4: Confirm and Sign Off

Tell Tony:
- What was saved to handoff.md
- Whether MEMORY.md was updated (and what changed)
- That n8n was triggered
- A brief sign-off message

## Output Format

```
Session state saved to handoff.md.
{Memory updated: {what} | Memory: no changes needed}
Dashboard updated via n8n.

{Sign-off message from Ekko}
```

## Notes

- The handoff file is overwritten each session (only the latest matters)
- The n8n webhook triggers the full Catch Me Up pipeline: Todoist, VPS health, and session data get combined into the dashboard JSON
- If the n8n webhook fails, still save the handoff file locally. The dashboard is a nice-to-have; the handoff is critical.
- Keep the sign-off brief and human. Not a status report.
