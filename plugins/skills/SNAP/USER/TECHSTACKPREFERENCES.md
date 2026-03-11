# Tech Stack Preferences

**Tony's actual technology stack, infrastructure, and tool preferences.**

This file is read by Ekko at session start. When Tony is building something new, this is the first place to check for "does something already exist that fits?"

---

## Languages

### Primary
- **TypeScript:** SNAP infrastructure, hooks, CLI tools, skills. All new code defaults to TS.
- **Python:** Transcription (faster-whisper), utility scripts, Obsidian vault tooling

### Secondary
- **Bash/Zsh:** Hook scripts, automation glue, quick CLI tools
- **Markdown:** Documentation, skills, PRDs, SecondBrain content

### Avoid
- Java — not in the stack, no plans to add
- Ruby — not in the stack

---

## Runtimes & Package Managers

| Category | Preference | Notes |
|----------|------------|-------|
| JavaScript Runtime | **Bun** | Primary runtime for all SNAP tools and hooks |
| Package Manager | **Bun** | `bun install`, `bun run`, `bun test` |
| Python Package Manager | **UV** | Used for faster-whisper and Python utilities |

---

## Frameworks

### Frontend
- No active frontend framework preference yet
- **Potential:** Astro (static), Next.js (dynamic) — evaluate when needed

### Backend
- **Hono** — lightweight, runs on Cloudflare Workers
- **Express** — familiar fallback

### Full-Stack
- No strong preference yet — evaluate per project

---

## Databases

| Type | Preference | Use Case |
|------|------------|----------|
| Document/KV | **Obsidian vault** (markdown files) | Primary knowledge store — SecondBrain |
| Relational | **PostgreSQL** | When structured data needed (future) |
| Key-Value | **Redis** | Caching (future — evaluate when needed) |

---

## Cloud & Infrastructure

### VPS / Self-Hosting
- **Provider:** Hostinger
- **Management:** Coolify (container orchestration, one-click deploys)
- **Philosophy:** Own the server, own the data. Self-host where practical.

### Coolify One-Click Apps (Available Marketplace)

**This section exists because of the Ghost CMS lesson: always check what Coolify can deploy in one click before building from scratch.**

Known one-click installs include:
- Ghost CMS (blogging, newsletter, membership)
- n8n (workflow automation)
- Plausible Analytics (privacy-friendly analytics)
- Uptime Kuma (monitoring)
- Gitea (self-hosted Git)
- Minio (S3-compatible storage)
- PostgreSQL, Redis, MongoDB (databases)
- Directus, Strapi (headless CMS)
- Grafana (dashboards)
- Many more — check Coolify marketplace before building custom

> **Rule of thumb:** If Coolify has a one-click app for it, use that. Don't build from scratch what you can deploy in 60 seconds.

### Hosting Preferences
| Type | Preference | Notes |
|------|------------|-------|
| Static Sites | Cloudflare Pages or Coolify | |
| APIs/Workers | Cloudflare Workers | Hono-based |
| Containers | Coolify on Hostinger VPS | Self-hosted Docker |
| CI/CD | GitHub Actions → Coolify | Push to deploy |

### DNS / Domains
- **Cloudflare** for DNS management

---

## Development Tools

### Editor/IDE
- **Primary:** Claude Code (CLI-first AI-native development)
- **Secondary:** VS Code (when visual editing needed)

### Terminal
- **Emulator:** Kitty
- **Shell:** zsh
- **Theme:** Tokyo Night Storm
- **Font:** Hack Nerd Font, 19pt
- **Remote control:** Kitty API for hook-driven tab state (UpdateTabTitle, SetQuestionTab)

### Version Control
- **Git CLI** — no GUI
- **Branch Strategy:** Feature branches, PR-based workflow
- **Hosting:** GitHub (private repos for SNAP, public for community)

---

## Libraries & Utilities

### Always Use
| Category | Library | Why |
|----------|---------|-----|
| Validation | zod | Type-safe, TS-native |
| Testing | vitest or bun test | Fast, TS-native |
| HTTP | fetch (native) | No dependencies needed |
| CLI parsing | commander or yargs | SNAP CLI tools pattern |

### Avoid
| Library | Use Instead | Reason |
|---------|-------------|--------|
| axios | native fetch | Unnecessary dependency |
| moment.js | date-fns | Moment is dead, massive bundle |

---

## AI & ML

### LLM Providers
- **Primary:** Anthropic (Claude)
- **Inference routing:** `Tools/Inference.ts` — never call APIs directly
  - `fast` = Haiku (quick lookups, classification)
  - `standard` = Sonnet (agents, workers, moderate tasks)
  - `smart` = Opus (deep reasoning, architecture, main sessions)

### AI Tools
- **Claude Code** — primary development environment
- **ElevenLabs** — voice synthesis (voice ID: rWyjfFeMZ6PxkHqD3wGC)
- **Fabric** — 260 pattern slash commands for content processing

### AI Infrastructure
- Voice server at localhost:8888
- Notification: ntfy.sh (mobile push), Discord (optional)
- Agent system: 45 skills, 167 workflows, 25 hooks

---

## Knowledge & Content

### Primary Knowledge Store
- **Obsidian** — SecondBrain vault at `C:\Users\txmye_ficivtv\My Drive\SecondBrain`
- Frontmatter schema enforced (see CLAUDE.md SecondBrain standards)
- Wiki-links for internal references
- Plans/ directory uses NTFS hardlinks for single-pane access

### Content Processing
- **Fabric patterns** — extract_wisdom, summarize, analyze, etc.
- **YouTube:** yt-dlp for downloads, fabric -y for transcripts, faster-whisper for local transcription
- **Web clipping:** Obsidian Web Clipper

---

## Automation

### Currently Running
- SNAP hooks (25) — session lifecycle, sentiment, ratings, integrity
- GitHub Actions — CI/CD pipelines
- Heartbeat system — proactive check-ins via Task Scheduler

### Planned / In Progress
- **n8n** — workflow automation ($3K upsell for clients, personal use too)
- **Scheduled agents** — continuous background monitoring via Claude Agent SDK

---

## Evaluated & Rejected

**Tools considered and passed on (with reasons). Don't re-suggest these.**

| Tool | Why Rejected | Date |
|------|-------------|------|
| *(none yet — add as Tony evaluates and rejects tools)* | | |

---

## The Ghost CMS Rule

If Tony says "let's build X" and X is something Coolify can deploy in one click, or something that integrates with Obsidian out of the box, or something that already exists as a mature open-source tool — **say so before writing a single line of code.**

The 60-second check: "Does this already exist? Does it fit the stack? Can Coolify deploy it?"

---

*This file is loaded at session start. Update as the stack evolves.*
