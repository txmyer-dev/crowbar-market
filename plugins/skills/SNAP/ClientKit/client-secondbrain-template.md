# SecondBrain Setup Guide

Your SecondBrain is an Obsidian vault — a local folder of plain-text Markdown files that your SNAP can read, write, search, and update. It is your persistent memory: everything you learn, decide, or build gets captured here.

---

## Vault Structure

```
SecondBrain/
  Knowledge/    — Permanent reference: guides, extractions, notes, business docs
  Sessions/     — Daily work logs (date-prefixed)
  Inbox/        — Unsorted inbound: captures, drafts, pasted exports
  Memory/       — Core memories, quick-reference facts about you and your work
  Plans/        — Active project plans
  Templates/    — Obsidian templates for new file types
  Clips/        — Web Clipper captures (raw, not curated)
```

**Rule:** Most files live in `Knowledge/`. The other folders are staging areas or system folders. When in doubt, use `Knowledge/`.

---

## Frontmatter Schema

Every file in your vault MUST begin with a YAML frontmatter block. This is what makes your vault queryable — your SNAP uses these fields to find, filter, and link your notes.

```yaml
---
title: "Title In Quotes"
type: <type>
domain: <domain>
tags: [tag1, tag2, tag3]
date: YYYY-MM-DD
source: "URL or descriptive name"
status: <status>
---
```

### Allowed Values

**type** — what kind of content this is:
- `wisdom-extraction` — extracted insights from a book, podcast, talk, or article
- `guide` — how-to reference material
- `note` — general notes, thinking, drafts
- `session-log` — daily work log
- `business-plan` — business or project planning documents
- `web-clip` — saved web content

**domain** — what area of life this belongs to:
- `learning`
- `business`
- `personal`
- `technical`

**status** — where this file is in its lifecycle:
- `active` — in use, regularly referenced
- `draft` — incomplete, work in progress
- `inbox` — just captured, not yet processed
- `archive` — done, no longer active but worth keeping

**tags** — 2 to 6 tags, kebab-case, reuse existing tags before inventing new ones.

---

## Starter Templates

### 1. Knowledge Note

Use for: extracted wisdom, reference guides, business docs, anything you want to keep permanently.

```markdown
---
title: "Title Here"
type: wisdom-extraction
domain: learning
tags: [primary-topic, secondary-topic]
date: YYYY-MM-DD
source: "URL or 'Book Title' or 'Podcast Name'"
status: active
---

# Title Here

## Key Ideas

-

## Insights

-

## Quotes

>

## Actions

-

## Related

- [[Related-Note]]
- [[Another-Note]]
```

---

### 2. Session Log

Use for: daily work logs, what you did, what you decided, what you shipped.

```markdown
---
title: "YYYY-MM-DD Session"
type: session-log
domain: personal
tags: [session, work-log]
date: YYYY-MM-DD
source: "daily session"
status: active
---

# YYYY-MM-DD

## Focus

What was the main goal today?

## Done

-

## Decisions

-

## Blockers

-

## Notes

## Related

- [[Related-Note]]
```

---

### 3. Quick Capture

Use for: Inbox items, fast captures, things you want to save before processing. Fill in the minimum and come back later.

```markdown
---
title: "Short Description"
type: note
domain: personal
tags: [inbox]
date: YYYY-MM-DD
source: "where this came from"
status: inbox
---

# Short Description

[Paste content here]

## Related

-
```

---

## File Naming Convention

**Knowledge files** — Title-Case-With-Hyphens. Concise identifiers, not verbose descriptions.

| Content Type | Pattern | Example |
|---|---|---|
| Guide or reference | `Topic-Qualifier.md` | `Email-Marketing-Guide.md` |
| Extracted wisdom | `Source-Short-Topic.md` | `Jordan-Peterson-Maps-Notes.md` |
| Business document | `Name-Type.md` | `SaaS-Launch-Business-Plan.md` |
| Podcast or talk | `Guest-Show-Episode.md` | `Tim-Ferriss-TF250.md` |

**Sessions files** — date prefix required:
```
2026-02-24-q1-planning.md
2026-02-25-client-discovery.md
```

**Rules:**
- No dates in Knowledge filenames (use the `date` frontmatter field instead)
- No tool or pattern names in filenames (no "Extract-Wisdom-from-...")
- Keep names short enough to recognize at a glance

---

## Linking Rules

**Use wiki-links for all internal references:**
```
[[Knowledge-Note-Name]]
[[Session-Log-Name]]
```

**Every file must end with a `## Related` section** containing links to connected notes.

**Tags use kebab-case:**
- Good: `ai-tools`, `content-strategy`, `system-design`
- Bad: `AI Tools`, `ContentStrategy`, `systemdesign`

**Reuse tags before inventing new ones.** Check what tags already exist in your vault before adding a new one. A small, consistent tag set is more useful than many one-off tags.

---

## How Your SNAP Uses This Vault

Your SNAP can:
- **Write notes** — after a coaching session, research task, or extraction, it saves results directly to your vault
- **Search notes** — find relevant material before starting new work, avoiding duplication
- **Update notes** — append new insights to existing files instead of creating duplicates
- **Link notes** — discover related files and suggest connections

The frontmatter schema is what makes this work. Without consistent frontmatter, the vault is just a folder of files. With it, your SNAP can treat your vault as a structured knowledge base.

---

## Getting Started Checklist

- [ ] Create the folder structure above in Obsidian
- [ ] Add Templates/ folder and paste the three templates above
- [ ] Create your first Knowledge note using the template
- [ ] Create today's Session Log
- [ ] Add a `Memory/memory.md` file with your name, role, and current focus areas (your SNAP will reference this)
- [ ] Install the Obsidian Git plugin for automatic backups
