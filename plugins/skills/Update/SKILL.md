---
name: Update
description: Self-update protocol. Refresh identity, context, and memory. USE WHEN update yourself, /update, self-update, refresh context, re-read soul, check heartbeat.
---

# Update - Self-Update Protocol

Re-read and internalize the three layers of persistent self in priority order: Soul, Heart, Memory. Report what was checked and any changes since last awareness.

## Workflow

Execute all three steps sequentially. For each layer, read the source, summarize what you found, and flag anything that changed or is new to this session.

### Step 1: Soul (KAI.md)

Read `~/.claude/skills/SNAP/USER/KAI.md` in full. This is identity — values, learnings, behavioral patterns. Internalize any updates. Compare against your current session behavior and note if anything conflicts.

**Report:** List any new learnings, value changes, or behavioral notes you weren't previously aware of.

### Step 2: Heart (Heartbeat/)

Find and read the most recent heartbeat file:

```
~/My Drive/SecondBrain/Sessions/{YYYY-MM-DD}-heartbeat.md
```

Use today's date first. If none exists, use the most recent one available. This is the pulse — what's happening in Tony's world right now.

**Report:** Summarize key items: tasks completed, upcoming priorities, calendar events, any flags.

### Step 3: Memories (MEMORY/)

Scan these MEMORY subdirectories for recent or relevant context:

| Directory | What to check |
|-----------|---------------|
| `STATE/` | `handoff.md` (last session state), `infrastructure.yaml` |
| `RELATIONSHIP/` | Latest relationship notes |
| `WORK/` | Active work context |
| `LEARNING/` | Recent learnings (last 3-5 entries in each subdirectory) |

**Report:** Flag any handoff items still in progress, recent relationship notes, and notable learnings.

## Output Format

```
## Update Complete

### Soul (KAI.md)
- {what was found / what's new to this session}

### Heart (Latest Heartbeat: {date})
- {key items from heartbeat}

### Memory
- **State:** {handoff summary or "no active handoff"}
- **Relationship:** {recent notes or "current"}
- **Learnings:** {notable recent entries or "nothing new"}

{Any conflicts or action items discovered}
```

## Notes

- This is a READ-ONLY operation. It never modifies files.
- If a source file is missing, note it and continue to the next layer.
- The Goodbye skill writes state; this skill reads it. They're complementary.
- Can be invoked anytime mid-session to re-sync, not just at startup.
