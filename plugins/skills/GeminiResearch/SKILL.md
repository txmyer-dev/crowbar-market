---
name: GeminiResearch
description: Gemini CLI fallback for blocked sites. USE WHEN user says 'fetch reddit', 'get reddit thread', 'reddit discussion', 'can't access this site with Claude', 'use gemini to fetch', 'gemini research', 'fetch from X', 'fetch twitter', 'blocked site', OR when WebFetch/WebSearch fails on a known-blocked domain (reddit.com, x.com, twitter.com). This is a SUPPLEMENTARY tool — not a replacement for the Research skill.
context: fork
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/GeminiResearch/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the GeminiResearch skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **GeminiResearch** skill to ACTION...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# GeminiResearch Skill

Gemini CLI fallback for fetching content from sites that Claude Code cannot access directly (Reddit, X/Twitter, and other blocked domains).

## Why This Exists

Claude Code's WebFetch and WebSearch tools are blocked from certain domains (Reddit, X/Twitter, some forums). Gemini CLI has broader web access and can fetch content from these sites directly. This skill routes those requests through `gemini -p` in headless mode.

**This is NOT a replacement for the Research skill.** Use Research for multi-agent research queries. Use GeminiResearch specifically when you need to fetch content from a URL that Claude cannot access.

---

## Workflow Routing

### Content Fetching (Primary)
- Fetch content from Reddit, X/Twitter, or other blocked sites -> `Workflows/GeminiFetch.md`
- "Use gemini to get this page" -> `Workflows/GeminiFetch.md`
- WebFetch failed on a URL -> `Workflows/GeminiFetch.md`

---

## When to Activate This Skill

### Direct Triggers
- "fetch this reddit thread"
- "get the reddit discussion about X"
- "use gemini to fetch [URL]"
- "gemini research [topic]"
- "fetch from X/Twitter"
- "can't access this with Claude"

### Automatic Fallback Triggers
- WebFetch returns error on reddit.com, x.com, twitter.com
- WebFetch blocked by a site that Gemini can likely access
- Research skill agents unable to access specific URLs

### Known Blocked Domains (Route Here Automatically)
- `reddit.com` / `old.reddit.com`
- `x.com` / `twitter.com`
- Other domains discovered to be blocked (add to this list over time)

---

## Core Capabilities

- **Headless Gemini CLI execution** via `gemini -p "prompt"`
- **Content extraction** from blocked domains
- **Markdown output** for downstream processing
- **Fallback escalation** to BrightData/Apify if Gemini also fails

---

## Integration

### Feeds Into
- **Research** — provides content from blocked sites for multi-agent synthesis
- **ExtractWisdom** — fetches source content for wisdom extraction
- **SecondBrain** — content saved to Knowledge/ with proper frontmatter

### Uses
- **Gemini CLI** (`gemini -p`) — the core tool
- **BrightData** — fallback if Gemini fails
- **Apify** — second fallback

---

## File Organization

**Scratch (temporary work artifacts):** `~/.claude/MEMORY/WORK/{current_work}/scratch/`
- Read `~/.claude/MEMORY/STATE/current-work.json` to get the `work_dir` value

**History (permanent):** `~/.claude/History/research/YYYY-MM/YYYY-MM-DD_[topic]/`

---

**Last Updated:** 2026-02-22
