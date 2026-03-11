---
name: ContentFormat
description: Platform-native content formatting and clipboard copy. USE WHEN user says 'format for LinkedIn', 'format for X', 'format for Twitter', 'format for email', 'format for Slack', 'format for Notion', 'copy to clipboard', 'platform format', 'make this ready for [platform]', OR when user wants to copy output in a platform-specific format. This is a FORMATTING tool — it reformats existing content, not a content creator.
context: fork
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/ContentFormat/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the FormatForPlatform workflow in the ContentFormat skill to format content"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **FormatForPlatform** workflow in the **ContentFormat** skill to format content...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# ContentFormat Skill

Reformat existing content for a specific platform's native format, then copy to clipboard. Eliminates formatting loss when pasting across platforms.

## Why This Exists

AI output is typically markdown. But LinkedIn uses emoji bullets and line breaks, X/Twitter has a 280-char limit, Slack uses its own markup, and email needs clean plaintext or HTML. Copying markdown to these platforms produces broken formatting. This skill converts content to the target platform's native format and copies it to the clipboard ready to paste.

**This is a FORMATTING tool, not a content creator.** It takes existing content and reformats it. For content creation, use other skills.

---

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **FormatForPlatform** | "format for [platform]", "copy for LinkedIn", "clipboard" | `Workflows/FormatForPlatform.md` |

---

## When to Activate This Skill

### Direct Triggers
- "format this for LinkedIn"
- "make this ready for X/Twitter"
- "format for email"
- "copy this to clipboard for Slack"
- "format for Notion"
- "make this paste-ready for [platform]"

### Automatic Triggers
- User mentions copying output to a specific platform
- Content is being prepared for distribution across multiple channels

---

## Supported Platforms

| Platform | Key Format |
|----------|-----------|
| LinkedIn | Emoji bullets, double line breaks, no markdown |
| X/Twitter | 280 chars, thread format, hashtags |
| Email | Clean paragraphs, no special chars |
| Slack | Slack mrkdwn (*bold*, `code`, >quotes) |
| Notion | Standard markdown with callouts |
| GitHub | GFM markdown with task lists |

---

**Last Updated:** 2026-02-22
