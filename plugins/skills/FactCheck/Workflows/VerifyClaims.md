# VerifyClaims Workflow

**Mode:** Sequential claim verification | **Tools:** WebSearch, WebFetch

## When to Use

- User provides content and asks to verify claims
- Content contains statistics, quotes, or factual assertions
- Pre-publication verification needed

## Workflow

### Step 1: Extract Claims

Scan the provided content and extract every verifiable claim. A "claim" is any statement that asserts a fact that can be checked:

- **Statistics:** Numbers, percentages, counts, dollar amounts
- **Attributions:** Quotes attributed to specific people
- **Events:** Dates, timelines, historical claims
- **Technical:** Feature capabilities, performance numbers, comparisons
- **Rankings:** "Most popular", "first ever", "largest", etc.

**Skip:** Opinions, subjective assessments, future predictions, and general statements that cannot be fact-checked.

Number each claim sequentially: `[C1]`, `[C2]`, etc.

---

### Step 2: Verify Each Claim via WebSearch

**For EACH extracted claim, you MUST:**

1. **Formulate a search query** — target the specific fact, not the general topic
2. **Run WebSearch** with that query
3. **Evaluate the results** — do sources confirm, contradict, or ignore the claim?
4. **Assign a verdict** using the rating system below
5. **Record the source URL** that supports your verdict

**🚫 CRITICAL: No rubber-stamping.** You MUST actually run WebSearch for each claim. Claiming "Verified" without a search = skill failure. If WebSearch returns no relevant results, the verdict is "Unverified" — not "Verified."

**Search query tips:**
- For statistics: search the exact number + context (e.g., `"4% of GitHub commits" Claude Code`)
- For quotes: search distinctive phrase fragments in quotes
- For events: search the specific date + event description
- For technical claims: search the product/feature + the specific capability claimed

---

### Step 3: Assign Verdicts

| Verdict | Symbol | Definition | Source Requirement |
|---------|--------|------------|--------------------|
| **Verified** | ✅ | Multiple independent sources confirm the claim | At least 1 source URL required |
| **Plausible** | 🟡 | Partial evidence supports it, but not fully confirmed | Source URL if available |
| **Unverified** | ⚪ | No supporting evidence found (not necessarily false) | Note what was searched |
| **Disputed** | ❌ | Contradicting evidence found from credible sources | Contradicting source URL required |
| **Outdated** | 📅 | Was true at one point but newer data contradicts it | Both old and new source URLs |

**Confidence is NOT about how confident you feel — it's about what the evidence shows.**

---

### Step 4: Produce Verification Table

Output the results in this exact format:

```markdown
## FactCheck: Verification Report

**Content:** [Title or first 50 chars of content]
**Claims Found:** [N]
**Verified:** [count] | **Plausible:** [count] | **Unverified:** [count] | **Disputed:** [count]

| # | Claim | Verdict | Source |
|---|-------|---------|--------|
| C1 | [Exact claim text] | ✅ Verified | [Source title](URL) |
| C2 | [Exact claim text] | 🟡 Plausible | [Source title](URL) |
| C3 | [Exact claim text] | ⚪ Unverified | Searched: "[query]" — no results |
| C4 | [Exact claim text] | ❌ Disputed | [Contradicting source](URL) |

### Recommendations

- **Safe to publish:** [List C# that are Verified]
- **Needs rewording:** [List C# that are Plausible — suggest hedging language]
- **Remove or verify manually:** [List C# that are Unverified]
- **Must correct:** [List C# that are Disputed — provide correct information]
```

---

### Step 5: Summary

Provide a brief assessment:
- Overall reliability score: X/N claims verified
- Biggest risk: which unverified/disputed claim is most impactful if wrong
- Recommendation: publish as-is, revise, or hold for more verification

---

## Speed Targets

| Content Size | Target |
|-------------|--------|
| 1-5 claims | 30-60s |
| 5-15 claims | 1-3 min |
| 15+ claims | 3-5 min |

## Troubleshooting

| Issue | Fix |
|-------|-----|
| WebSearch returns no results | Try alternative query phrasing. If still nothing → Unverified. |
| Claim is too vague to verify | Mark as "Not verifiable — too vague" and suggest specific rewording |
| Contradicting sources disagree | Mark as Disputed, cite both sides |
| Paywalled source | Note paywall, mark as Plausible if title/snippet supports claim |

## Notes

- This skill uses WebSearch (built into Claude Code) — no additional APIs needed
- For claims about blocked sites (Reddit, X), use GeminiResearch skill as fallback
- The goal is honest verification, not validation — finding that claims are wrong is a SUCCESS, not a failure
- Always include the "Sources:" section with URLs at the end of your response per WebSearch requirements
