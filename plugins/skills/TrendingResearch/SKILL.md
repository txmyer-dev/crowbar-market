---
name: TrendingResearch
description: Trending topic discovery and momentum analysis. USE WHEN user says 'what's trending', 'trending topics', 'what's hot', 'viral right now', 'emerging trends', 'trend report', 'what's happening in [domain]', OR when user wants a pulse check on current trends across tech, security, business, or culture. This is a DISCOVERY tool — it finds what's trending, not a deep research tool.
context: fork
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/TrendingResearch/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the DiscoverTrends workflow in the TrendingResearch skill to find trending topics"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **DiscoverTrends** workflow in the **TrendingResearch** skill to find trending topics...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# TrendingResearch Skill

Discover what's trending right now across multiple domains. Returns a structured trend report with momentum signals, source URLs, and category breakdowns.

## Why This Exists

Staying current requires scanning multiple sources across domains. This skill runs parallel WebSearch queries with recency emphasis to surface what's trending in tech, security, business, and culture — then structures the results into an actionable trend report. Unlike the Research skill (which answers specific questions), this discovers what questions you should be asking.

**This is a DISCOVERY tool, not a deep research tool.** It finds emerging trends and momentum signals. For deep dives on specific topics, use the Research skill.

---

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **DiscoverTrends** | "what's trending", "trend report", "pulse check" | `Workflows/DiscoverTrends.md` |

---

## When to Activate This Skill

### Direct Triggers
- "what's trending in AI?"
- "give me a trend report"
- "what's hot in cybersecurity this week?"
- "what's going viral right now?"
- "emerging trends in [domain]"
- "pulse check on [topic]"

### Automatic Triggers
- User asks about "what's new" or "what's happening" in a domain
- Morning briefing or daily update context
- Content planning that requires current trend awareness

---

## Trend Categories

| Category | Focus Areas |
|----------|------------|
| AI & Tech | Models, tools, frameworks, launches, developer trends |
| Security | Vulnerabilities, breaches, threat actor activity, new tools |
| Business | Startups, funding, market moves, strategy shifts |
| Social & Culture | Viral content, platform changes, creator economy, memes |
| Science & Health | Breakthroughs, studies, policy changes |

---

**Last Updated:** 2026-02-22
