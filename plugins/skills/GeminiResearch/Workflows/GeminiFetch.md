# GeminiFetch Workflow

**Mode:** Single Gemini CLI headless call | **Timeout:** 60 seconds

## When to Use

- User needs content from Reddit, X/Twitter, or other blocked sites
- WebFetch failed on a specific URL
- User explicitly asks to use Gemini for fetching

## Critical: Model Flag Required

Gemini CLI defaults to `gemini-3-flash-preview` which frequently hits capacity limits. **Always specify the model flag:**

```bash
gemini -p "..." -m gemini-2.5-flash --yolo 2>&1 | grep -v "^Hook\|^Created\|^Expanding\|^YOLO\|^Loaded"
```

**Flags explained:**
- `-p "..."` — headless (non-interactive) mode, MANDATORY
- `-m gemini-2.5-flash` — reliable model, avoids capacity issues
- `--yolo` — auto-approve any tool use (search, web_fetch) without hanging
- `2>&1 | grep -v ...` — filter out Gemini's hook/startup noise from output

## Critical: Search > Direct Fetch

**Gemini's Google Search grounding is the primary capability, not direct URL fetching.** Reddit and X render via JavaScript — direct `web_fetch` returns empty content. But Gemini's search tool finds and summarizes these discussions via Google's index.

**Primary mode: Topic search (Step 2B)**
**Secondary mode: URL-as-search-hint (Step 2A-alt)**

## Workflow

### Step 1: Determine Fetch Type

**User provides a specific URL:**
→ Go to Step 2A

**User wants discussion about a topic on blocked platform:**
→ Go to Step 2B (PREFERRED — higher success rate)

---

### Step 2A: URL-Based Fetch

**First attempt — use the URL as a search hint (most reliable):**
```bash
gemini -p "Find and summarize the content from this URL. Search for it by its title or key phrases if direct access fails. Return: title, author, date, and a detailed summary. URL: [URL]" -m gemini-2.5-flash --yolo 2>&1 | grep -v "^Hook\|^Created\|^Expanding\|^YOLO\|^Loaded"
```

**For Reddit threads specifically:**
```bash
gemini -p "Search for this Reddit thread and summarize it: [URL]. Return the post title, subreddit, author, post summary, and the top 5-10 comment summaries with their authors. Format as clean markdown." -m gemini-2.5-flash --yolo 2>&1 | grep -v "^Hook\|^Created\|^Expanding\|^YOLO\|^Loaded"
```

**For X/Twitter posts specifically:**
```bash
gemini -p "Search for this X/Twitter post and summarize it: [URL]. Return the author, full post text, date, engagement metrics, and notable replies. Format as clean markdown." -m gemini-2.5-flash --yolo 2>&1 | grep -v "^Hook\|^Created\|^Expanding\|^YOLO\|^Loaded"
```

---

### Step 2B: Topic Search on Blocked Platform (PREFERRED)

**Reddit topic search:**
```bash
gemini -p "Search Reddit for recent discussions about [TOPIC]. Find the top 3-5 most relevant threads from the past month. For each, provide: subreddit, title, post body summary, top 3 comments, and the link. Format as clean markdown." -m gemini-2.5-flash --yolo 2>&1 | grep -v "^Hook\|^Created\|^Expanding\|^YOLO\|^Loaded"
```

**X/Twitter topic search:**
```bash
gemini -p "Search X/Twitter for recent posts about [TOPIC]. Find the top 5-10 most engaged posts from the past week. For each, provide: author, post text, engagement metrics, and the link. Format as clean markdown." -m gemini-2.5-flash --yolo 2>&1 | grep -v "^Hook\|^Created\|^Expanding\|^YOLO\|^Loaded"
```

**Multi-platform combined search:**
```bash
gemini -p "Search Reddit AND X/Twitter for recent discussions about [TOPIC]. From Reddit: top 3 threads with summaries. From X: top 5 posts with engagement. Format as clean markdown with separate sections." -m gemini-2.5-flash --yolo 2>&1 | grep -v "^Hook\|^Created\|^Expanding\|^YOLO\|^Loaded"
```

---

### Step 3: Process Output

1. Capture the Gemini CLI output (already filtered via grep)
2. If output is empty or contains only error text → Go to Step 4 (Fallback)
3. If output is good → Return to user in standard format

**Output format:**
```markdown
## GeminiResearch: [Topic/URL]

**Source:** [URL or search query]
**Fetched via:** Gemini CLI (gemini-2.5-flash, Google Search grounding)
**Date:** [today]

---

[Content from Gemini]

---

*Fetched by GeminiResearch skill — content from Gemini CLI fallback*
```

---

### Step 4: Fallback Escalation

If Gemini CLI fails (empty output, error, timeout, 429 rate limit):

**Fallback 1:** Try BrightData skill
```
→ READ: ~/.claude/skills/BrightData/Workflows/Four-tier-scrape.md
→ Execute with the same URL
```

**Fallback 2:** Try Apify RAG browser
```
→ Use mcp__Apify__apify-slash-rag-web-browser with the URL
```

**Fallback 3:** Report failure to user
```
Unable to fetch [URL/topic] through any available method:
- Gemini CLI: [error]
- BrightData: [error]
- Apify: [error]

Suggestion: Try accessing the URL directly in your browser.
```

---

## Speed Targets

| Operation | Target |
|-----------|--------|
| Topic search (2B) | 15-30s |
| URL-based search (2A) | 15-30s |
| With fallback | 60-90s |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| 429 rate limit on default model | Use `-m gemini-2.5-flash` (already in commands above) |
| Hanging/no output | Ensure `--yolo` flag is set. Check `gemini --version` is 0.29+ |
| Empty web_fetch results | Expected for JS-heavy sites. Search grounding works instead. |
| Hook noise in output | The `grep -v` filter handles this. If new noise appears, add patterns. |

## Notes

- Gemini CLI handles its own authentication via Google account (configured at first run)
- No API keys stored in skill files — Gemini CLI manages credentials internally
- **Search grounding is the primary mechanism** — Gemini uses Google Search to find and synthesize content from blocked sites, rather than directly fetching HTML
- Some topics may have limited search results — that's what the fallback chain is for
- Gemini links use `vertexaisearch.cloud.google.com` redirect URLs — these resolve to actual Reddit/X URLs when clicked
