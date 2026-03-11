---
name: FactCheck
description: Claim verification and fact-checking. USE WHEN user says 'fact check', 'verify claims', 'check statistics', 'are these facts correct', 'double check claims', 'verify this', 'source check', OR when generating content that contains statistics, quotes, or factual claims that should be verified before publishing. This is a VERIFICATION tool — not a replacement for the Research skill.
context: fork
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/FactCheck/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the FactCheck skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **FactCheck** skill to ACTION...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# FactCheck Skill

Verify factual claims, statistics, and attributions in any content before publishing. Produces a structured verification table with verdicts, confidence ratings, and source URLs.

## Why This Exists

AI-generated content can contain plausible-sounding but unverified statistics and claims. This skill forces systematic verification — every claim gets searched, every verdict gets evidence. The output table makes it obvious what's verified and what isn't.

**This is NOT a replacement for the Research skill.** Use Research for discovering information. Use FactCheck specifically for verifying claims that already exist in content.

---

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **VerifyClaims** | "fact check this", "verify these claims", "check statistics" | `Workflows/VerifyClaims.md` |

---

## When to Activate This Skill

### Direct Triggers
- "fact check this content"
- "verify these claims"
- "check the statistics in this"
- "double check every claim"
- "are these facts correct"
- "source check this article"

### Automatic Triggers
- Content contains statistics (percentages, dollar amounts, counts)
- Content contains attributed quotes
- Content contains historical dates or event claims
- User is about to publish content with factual assertions

---

## Core Capabilities

- **Claim extraction** from any text content
- **Web search verification** per claim using WebSearch
- **Structured verdict table** with confidence ratings and source URLs
- **Honest reporting** — marks unverified claims as unverified, never rubber-stamps

---

## Integration

### Feeds Into
- **Content publishing workflows** — verify before posting
- **SecondBrain** — verified content gets higher trust

### Uses
- **WebSearch** — primary verification tool
- **WebFetch** — for checking specific source URLs

---

**Last Updated:** 2026-02-22
