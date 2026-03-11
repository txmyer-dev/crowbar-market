---
name: InboxCleaner
description: Autonomous email triage — classifies unread emails as important or not, marks unimportant as read. USE WHEN user says 'clean my inbox', 'triage email', 'inbox zero', 'clean up email', 'mark spam as read', 'email cleanup'. Requires Gmail MCP.
context: fork
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/InboxCleaner/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# InboxCleaner — Autonomous Email Triage

Reads all unread emails, classifies each as important or not important using a clear rubric, presents the classification for review, then marks unimportant emails as read.

## When to Use

- User wants to clean up their inbox
- User says "inbox zero", "clean my inbox", "triage email"
- User is overwhelmed by unread count and wants signal separated from noise

## Prerequisites

- Gmail MCP must be connected and working
- Load Gmail tools: `mcp__claude_ai_Gmail__gmail_search_messages`, `mcp__claude_ai_Gmail__gmail_read_message`

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **CleanInbox** | "clean inbox", "triage email", "inbox zero" | `Workflows/CleanInbox.md` |
