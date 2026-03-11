# Extract Workflow

Extract dynamic, content-adaptive wisdom from any content source.

## Input Sources

| Source | Method |
|--------|--------|
| YouTube URL | **yt-dlp** for transcript (NEVER use WebFetch — youtube.com blocks it) |
| Article URL | WebFetch to get content |
| File path | Read the file directly |
| Pasted text | Use directly |

## Execution Steps

### Step 1: Get the Content

**YouTube URLs (youtube.com, youtu.be, m.youtube.com):**
Do NOT attempt WebFetch — it will always fail. Go directly to yt-dlp:
```bash
yt-dlp --write-auto-sub --skip-download --sub-format vtt \
  -o /tmp/yt-transcript "YOUTUBE_URL" 2>/dev/null
sed '/^$/d; /^[0-9]/d; /^NOTE/d; /^WEBVTT/d; /-->/d' /tmp/yt-transcript*.vtt | \
  awk '!seen[$0]++' > /tmp/yt-transcript.txt
```
Then read `/tmp/yt-transcript.txt` for the transcript. Also grab metadata with:
```bash
yt-dlp --print title --print channel --print description --no-download "YOUTUBE_URL"
```

**Article URLs:** Use WebFetch to get content.
**File paths:** Read the file directly.
**Pasted text:** Use directly.

Save to a working file if large.

### Step 2: Deep Read

Read the entire content. Don't extract yet. Notice:
- What domains of wisdom are present?
- What made you stop and think?
- What's genuinely novel vs. commonly known?
- What would {PRINCIPAL.NAME} highlight if he were reading this?
- What quotes land perfectly?

### Step 3: Select Dynamic Sections

Based on your deep read, pick 5-12 section names. Rules:
- Section names must be conversational, not academic
- Each must have at least 3 quality bullets
- Always include "Quotes That Hit Different" if source has quotable moments
- Always include "First-Time Revelations" if genuinely new ideas exist
- Be SPECIFIC — "Agentic Engineering Philosophy" not "Technology Insights"

### Step 4: Extract Per Section

For each section, extract 3-15 bullets. Apply tone rules from SKILL.md:
- 8-20 words, flexible for clarity
- Specific details, not vague summaries
- Speaker's words when they're good
- No hedging language
- Every bullet worth telling someone about

### Step 5: Add Closing Sections

Always append:
1. **One-Sentence Takeaway** (15-20 words)
2. **If You Only Have 2 Minutes** (5-7 essential points)
3. **References & Rabbit Holes** (people, projects, books, tools mentioned)

### Step 6: Quality Check

Run the quality checklist from SKILL.md before delivering.

### Step 7: Ekko's Take

After extraction, append an `## Ekko's Take` section. This is your honest, first-person analysis — not a summary, not cheerleading. Address:

- **What the speaker nails** — what's genuinely good and why
- **Where it hits home for Tony** — connect to his projects, business, infrastructure, goals
- **What's already in our stack** — map claims to things we've built or have
- **What's missing** — gaps this content reveals in our setup
- **Honest critique** — where the speaker oversells, glosses over complexity, or is just wrong
- **Bottom line** — one sentence, no hedging

Tone: direct, opinionated, useful. Write like a trusted advisor, not a book report. If the content is mid, say so. If it's fire, say that too.

### Step 8: Output

Present the complete extraction in the format specified in SKILL.md. **File structure order:**

1. YAML frontmatter
2. Title + summary line
3. **Ekko's Take** (FIRST — gives Tony scope before the detail)
4. `---` separator
5. Extraction sections
6. Closing sections (One-Sentence Takeaway, If You Only Have 2 Minutes, References)
7. Related

Ekko's Take goes at the top so Tony gets the honest verdict and context mapping before reading the full extraction. He reads for scope first, detail second.

### Step 9: Auto-Save to SecondBrain

After presenting output, automatically save to `C:\Users\txmye_ficivtv\My Drive\SecondBrain\Knowledge\`:

1. **Determine filename** using SecondBrain naming conventions:
   - Podcast/show: `{Guest}-{ShowAbbrev}{Episode}.md` (MW, DOAC, JRE, HL, IF, LI)
   - YouTube/general: `{Creator}-{Short-Topic}.md`
   - Book/author: `{Author}-{Short-Title}.md`
   - No dates in filename. No pattern name. Title-Case-With-Hyphens.

2. **Check for duplicates** — scan `C:\Users\txmye_ficivtv\My Drive\SecondBrain\Knowledge\` for existing file with same source. Warn if found.

3. **Write file** with:
   - YAML frontmatter: title, type (`wisdom-extraction`), domain, tags (2-6 kebab-case), date, source URL, status (`active`)
   - Full extraction output
   - `## Related` section with `[[wiki-links]]` to related existing Knowledge files

4. **Open in Obsidian** — run `start "" "obsidian://open?vault=SecondBrain&file=Knowledge%2F{filename-without-extension}"` to open the file automatically.

5. **Confirm** — state the saved filename and path. No permission needed.
