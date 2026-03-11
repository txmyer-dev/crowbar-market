---
name: ContentRepurpose
description: Repurpose transcripts and content into platform-native formats in parallel. USE WHEN user says 'repurpose this', 'turn this into tweets', 'make a LinkedIn post from this', 'newsletter from this', 'repurpose for social', 'content from transcript', OR when user has a transcript/article and wants multi-format output. This is a CONTENT GENERATOR — it creates new platform-native content from source material. For reformatting existing content, use ContentFormat instead.
context: fork
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/ContentRepurpose/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# ContentRepurpose — Multi-Format Content Generation

Takes a single piece of source content (transcript, article, video notes, podcast) and generates platform-native content in multiple formats simultaneously.

## How It Differs From ContentFormat

| | ContentFormat | ContentRepurpose |
|---|---|---|
| **Input** | Finished content (markdown, text) | Raw source (transcript, article, notes) |
| **Output** | Same content, different format | New content, platform-native |
| **Purpose** | Reformat for clipboard/paste | Generate shareable content |
| **Example** | "Format this blog post for LinkedIn" | "Turn this podcast transcript into tweets + LinkedIn + newsletter" |

## When to Use

- User has a transcript, article, podcast notes, or long-form content
- User wants to create social media content from source material
- User says "repurpose", "turn this into", "make content from"
- User wants multiple output formats from one source

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **RepurposeContent** | "repurpose this", "turn into tweets", "make LinkedIn post from" | `Workflows/RepurposeContent.md` |
