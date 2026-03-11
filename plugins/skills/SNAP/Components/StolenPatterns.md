# Stolen Patterns Reference

Reusable behavioral patterns extracted from Nick Saraev's Claude Code skills (March 2026). These are not skills — they're techniques any skill can apply.

## 1. Minimal Rewrite Constraint

**What:** When modifying existing content (templates, emails, landing pages), constrain the AI to change only 5-10 words/elements rather than rewriting from scratch.

**Why:** Prevents Claude's tendency to over-generate. Preserves what's already working. Forces precision over creativity.

**When to use:** Any template-modification workflow. Content adaptation. Campaign variations. Translating a design for a new client.

**Example prompt fragment:**
> "Find the 3 closest existing campaigns to this niche. For each, create a new version by changing ONLY 5-10 words. Preserve all HTML structure, formatting, and campaign logic. The output should be 95% identical to the original."

---

## 2. State Files for Resume

**What:** For long-running operations that process items sequentially, write progress to a state file (`.tmp/state.json` or similar). Track which items succeeded, which failed, which are pending.

**Why:** Allows re-running after interruption without duplicate work. Essential for operations that cost money per item (API calls, bookings, purchases).

**When to use:** Batch API calls. Multi-step pipelines. Any operation processing 20+ items that takes more than a few minutes.

**Example structure:**
```json
{
  "started_at": "2026-03-03T07:00:00Z",
  "total": 50,
  "completed": ["item-1", "item-2", "item-3"],
  "failed": {"item-4": "rate_limited"},
  "pending": ["item-5", "item-6", "..."]
}
```

**Our existing use:** Plaid sync already does this with `items.json`. Pattern is validated.

---

## 3. Named Design Vocabularies

**What:** Instead of vague descriptions ("modern", "clean", "professional"), create named archetypes with specific visual characteristics.

**Why:** Shared vocabulary between human and AI eliminates ambiguity. "Obsidian Vault" is precise; "dark and modern" is not.

**When to use:** Art skill, website design, brand work, any visual creation workflow.

**Example vocabularies (from Nick's website builder):**
- **Ethereal Clinical** — frosted glass, white space, surgical precision
- **Obsidian Vault** — deep blacks, gold accents, luxury
- **Synthetic Neon** — cyberpunk gradients, electric highlights
- **Moss & Stone** — organic textures, earth tones, warmth

**Action:** Consider adding named aesthetic archetypes to the Art skill's design system.

---

## 4. Rubrics Before Execution

**What:** Define the classification criteria in explicit text BEFORE running any AI classification. Include examples of both positive and negative cases.

**Why:** Reduces misclassification. Makes the AI's decisions auditable. Prevents post-hoc rationalization.

**When to use:** Any classification or triage workflow. Email sorting. Content moderation. Lead scoring. Priority assignment.

**Example (from InboxCleaner):**
> IMPORTANT: personalized, human-written, substantive, from known contact
> NOT IMPORTANT: automated, marketing, cold outreach, mass email
> UNCERTAIN: keep as unread (false negative > false positive)

**Key insight:** Always define the edge case behavior explicitly. "When uncertain, do X" prevents the AI from guessing.

---

## 5. Spot-Check Verification

**What:** After any batch operation, verify a small random sample (3-5 items) before proceeding to the next step.

**Why:** Catches systematic errors early. A bad filter, wrong API parameter, or misclassification shows up in the sample before you've wasted the full batch.

**When to use:** After scraping batches. After batch classification. After bulk API operations. After generating multiple outputs.

**Example workflow:**
1. Scrape 2000 leads
2. **Spot-check 5 leads** — do they match the intended niche? Are the fields populated correctly?
3. If spot-check fails → fix the issue and re-scrape
4. If spot-check passes → proceed to enrichment

**Our existing rule:** SecondBrain standards say "validate on a small sample (5 items) first." This pattern makes it explicit.

---

## 6. Dual-Mode API Strategy

**What:** For APIs that support both single-item and bulk endpoints, auto-select the strategy based on volume.

**Why:** Small batches are faster with concurrent single calls. Large batches are cheaper with bulk API. The threshold varies by API but ~200 items is a common crossover point.

**When to use:** Email enrichment. Data imports. Any API with both single and bulk endpoints.

**Example logic:**
```
if items < 200:
    use concurrent single API (ThreadPoolExecutor, max_workers=20)
else:
    use bulk API (submit job, poll for completion, download results)
```

---

## 7. Reply Check Before Follow-Up

**What:** Before sending any automated follow-up, check if the recipient has replied within a configurable window (default: 48 hours).

**Why:** Prevents annoying people who already responded. Simple heuristic that doesn't require ML or complex tracking.

**When to use:** Any email follow-up automation. Lead nurture sequences. Client check-ins.

**Example logic:**
```
for each pending contact:
    check Gmail for replies in thread within last 48h
    if replied → skip (they're engaged)
    if not replied → send follow-up with tone matched to prior emails
```

**Tone matching:** Instead of asking "what tone should this email be?", examine prior emails in the thread and match the existing style (casual if they used lowercase, formal if they used full sentences, etc.).
