# FormatForPlatform Workflow

**Mode:** Content reformatting + clipboard copy | **Tools:** Bash (clipboard)

## When to Use

- User has content and wants it formatted for a specific platform
- User wants to copy AI output ready to paste into LinkedIn, X, Slack, etc.
- Multi-platform distribution — format the same content for several platforms

## Workflow

### Step 1: Identify Target Platform

Determine which platform(s) the user wants. If unclear, ask:

```
Which platform should I format this for?
→ LinkedIn | X/Twitter | Email | Slack | Notion | GitHub | Multiple
```

### Step 2: Reformat Content Using Platform Rules

Apply the platform-specific formatting rules below. **Do NOT rewrite the content** — preserve the user's message, tone, and meaning. Only change the formatting.

---

## Platform Formatting Rules

### LinkedIn

**Character limit:** 3,000 (posts), 700 visible before "see more"
**Hook rule:** First 2 lines must hook — they're visible before the fold.

**Formatting conventions:**
- Use emoji bullets instead of markdown bullets: `→`, `✅`, `📌`, `💡`, `🔑`, `⚡`
- Double line breaks between every paragraph (LinkedIn collapses single breaks)
- NO markdown bold/italic — LinkedIn doesn't render it
- Use CAPS for emphasis instead of bold: `THIS is important`
- Short paragraphs (1-3 sentences max)
- End with a question or CTA to drive engagement
- Hashtags at the bottom (3-5 max), each on its own line
- No links in body (kills reach) — put link in first comment

**Template:**
```
[Hook line — provocative or surprising statement]

[Supporting point 1]

→ [Bullet insight 1]
→ [Bullet insight 2]
→ [Bullet insight 3]

[Bridge sentence]

[Supporting point 2 with detail]

💡 [Key takeaway]

[CTA question to audience]

---

#hashtag1
#hashtag2
#hashtag3
```

---

### X/Twitter

**Character limit:** 280 per post
**Thread format:** Number posts [1/N] for threads

**Formatting conventions:**
- No markdown — plain text only
- Use line breaks for readability (2 line breaks = visual separator)
- Hashtags inline or at end (1-3 max, more looks spammy)
- Mentions with @ when referencing people
- For threads: strong hook in post 1, key insight per post, final post = CTA
- Emojis sparingly — 1-2 per post max
- Short sentences. Punchy. Direct.

**Single post template:**
```
[Statement under 280 chars]

[Optional hashtag]
```

**Thread template:**
```
🧵 [Hook — strongest claim or question] [1/N]

[Point 1 with detail] [2/N]

[Point 2 with detail] [3/N]

[Key takeaway or surprising insight] [4/N]

[CTA — follow, reply, repost] [5/N]
```

---

### Email

**Character limit:** None practical
**Subject line:** Under 50 chars, no ALL CAPS, no spam trigger words

**Formatting conventions:**
- Clean paragraphs with single blank line between
- NO emoji (unless casual/internal)
- NO markdown (renders as plaintext in most clients)
- Use indentation or dashes for lists, not bullets
- Bold via **double asterisks** ONLY if HTML email, otherwise skip
- Short paragraphs (2-4 sentences)
- Clear CTA at the end
- Professional sign-off

**Template:**
```
[Greeting],

[Opening — context or purpose in 1-2 sentences]

[Body — key points in short paragraphs]

- [List item if needed]
- [List item if needed]

[Closing — clear next step or CTA]

[Sign-off],
[Name]
```

---

### Slack

**Character limit:** 40,000 per message (practical limit: keep under 500 for readability)
**Uses Slack mrkdwn (NOT standard markdown)**

**Formatting conventions:**
- Bold: `*bold*` (single asterisks, NOT double)
- Italic: `_italic_` (underscores)
- Strikethrough: `~strikethrough~`
- Code: `` `inline` `` and ` ```block``` `
- Quotes: `> blockquote`
- Lists: Use `•` or `◦` characters (Slack doesn't render `-` as bullets)
- Links: `<URL|display text>`
- Mentions: `@person` or `@channel`
- Emojis: `:emoji_name:` syntax encouraged
- Line breaks respected (single break = new line)

**Template:**
```
*[Title/Topic]*

[Brief context — 1-2 sentences]

• [Point 1]
• [Point 2]
• [Point 3]

> [Key quote or callout]

:point_right: *Next step:* [Action item]
```

---

### Notion

**Character limit:** None
**Uses standard markdown with Notion extensions**

**Formatting conventions:**
- Full markdown support: `**bold**`, `*italic*`, `~~strikethrough~~`
- Headings: `#`, `##`, `###`
- Task lists: `- [ ]` and `- [x]`
- Callout blocks: `> 💡 **Tip:** text` (rendered as callout)
- Toggle blocks: not available in pasted markdown
- Tables: standard markdown tables work
- Code blocks with language tags: ` ```python `
- Dividers: `---`
- Wiki-links: `[[Page Name]]`

**Template:**
```
# [Title]

## Summary
[2-3 sentence overview]

## Key Points
- **[Point 1]:** [Detail]
- **[Point 2]:** [Detail]
- **[Point 3]:** [Detail]

> 💡 **Key Takeaway:** [Most important insight]

## Action Items
- [ ] [Task 1]
- [ ] [Task 2]

---
*Source: [reference]*
```

---

### GitHub

**Character limit:** 65,536 (issues/PRs/comments)
**Uses GitHub Flavored Markdown (GFM)**

**Formatting conventions:**
- Full GFM: bold, italic, strikethrough, tables, task lists
- Code blocks with syntax highlighting: ` ```typescript `
- Collapsible sections: `<details><summary>Title</summary>content</details>`
- Issue/PR references: `#123`, `@user`
- Emoji shortcodes: `:rocket:`, `:bug:`, `:tada:`
- Tables with alignment: `|:---|:---:|---:|`
- Footnotes: `[^1]`

**Template:**
```
## [Title]

[Description — what and why]

### Changes
- [Change 1]
- [Change 2]

### Details

<details>
<summary>Technical details</summary>

[Expanded content here]

</details>

### Checklist
- [ ] [Item 1]
- [ ] [Item 2]
```

---

## Step 3: Copy to Clipboard

After formatting, copy the result to the system clipboard:

```bash
# Windows (Git Bash / Windows)
echo -n "FORMATTED_CONTENT" | clip.exe

# macOS
echo -n "FORMATTED_CONTENT" | pbcopy

# Linux
echo -n "FORMATTED_CONTENT" | xclip -selection clipboard
```

**For multi-line content, use a heredoc:**
```bash
cat <<'CLIP' | clip.exe
[formatted content here]
CLIP
```

**After copying, confirm to user:**
```
✅ Formatted for [Platform] and copied to clipboard. Paste directly into [Platform].
```

---

## Step 4: Multi-Platform (Optional)

If user wants the same content for multiple platforms:

1. Format for each platform separately
2. Present all versions with clear headers
3. Ask which to copy to clipboard (or copy the first one and show the rest)

**Output format:**
```
## LinkedIn Version
[formatted content]

## X/Twitter Version
[formatted content]

## Email Version
[formatted content]

📋 LinkedIn version copied to clipboard. Say "copy X version" for others.
```

---

## Speed Targets

| Operation | Target |
|-----------|--------|
| Single platform format | 10-20s |
| Multi-platform (3) | 30-60s |

## Notes

- This skill REFORMATS — it does not rewrite. Preserve the user's voice and message.
- When in doubt about platform conventions, default to the simpler format
- LinkedIn reach is killed by links in the post body — always note to put links in first comment
- X threads should have a strong hook in post 1 — if the first post is boring, nobody reads the rest
- Clipboard copy uses the platform's native command — detect OS from environment
