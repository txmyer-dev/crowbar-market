# DiscoverTrends Workflow

**Mode:** Multi-query trend discovery | **Tools:** WebSearch

## When to Use

- User wants to know what's trending right now
- Morning briefing or pulse check on a domain
- Content planning that requires current awareness
- Scanning for emerging patterns before they go mainstream

## Workflow

### Step 1: Determine Scope

If the user specifies a domain (e.g., "what's trending in AI?"), focus on that category. If unspecified, scan all 5 categories.

```
Which domains should I scan for trends?
-> All (full scan) | AI & Tech | Security | Business | Social & Culture | Science & Health
```

### Step 2: Execute Trend Queries

**CRITICAL: Every query MUST include temporal recency signals.** Use the current year, "this week", "today", "latest", "trending", or "emerging" in every search. Never run a bare topic search without recency.

Run WebSearch queries for each selected category. Use 2-3 queries per category for coverage.

**Query Templates (adapt to current date):**

#### AI & Tech
```
- "trending AI tools and models February 2026"
- "latest tech launches this week 2026"
- "emerging developer frameworks trending 2026"
```

#### Security
```
- "cybersecurity trending news this week 2026"
- "latest vulnerabilities and breaches February 2026"
- "emerging security threats trending 2026"
```

#### Business
```
- "trending startup news and funding this week 2026"
- "business strategy trends emerging February 2026"
- "viral business stories trending today 2026"
```

#### Social & Culture
```
- "what's going viral on social media this week 2026"
- "trending topics Twitter Reddit today 2026"
- "creator economy emerging trends 2026"
```

#### Science & Health
```
- "science breakthroughs trending this week 2026"
- "health research emerging findings February 2026"
```

**Recency Rule:** Replace year/month with actual current values. The queries above are templates — always use today's actual date context.

### Step 3: Assess Trend Momentum

For each discovered trend, assess its momentum signal:

| Signal | Meaning | Indicator |
|--------|---------|-----------|
| **🔥 Surging** | Rapidly growing, high velocity | Multiple independent sources, <48hrs old |
| **📈 Rising** | Growing steadily, gaining traction | 3+ sources, within past week |
| **🌱 Emerging** | Early signal, worth watching | 1-2 quality sources, novel concept |
| **♻️ Recurring** | Cyclical topic resurfacing | Known topic with new developments |

### Step 4: Produce Trend Report

Output a structured report. Group by category. Each trend entry includes:

```markdown
## Trend Report — [Date]

### 🤖 AI & Tech

**1. [Trend Name]** 🔥 Surging
> [1-2 sentence summary of what's happening and why it matters]
> Source: [URL]

**2. [Trend Name]** 📈 Rising
> [1-2 sentence summary]
> Source: [URL]

### 🔒 Security

**1. [Trend Name]** 🔥 Surging
> [1-2 sentence summary]
> Source: [URL]

[...continue for each category...]

---

### Key Takeaways
- [Most significant cross-domain pattern]
- [Trend with highest momentum]
- [Emerging signal worth watching]
```

**Report Rules:**
- 3-5 trends per category (fewer if scanning single domain — go deeper with 5-8)
- Every trend MUST have at least one source URL
- Momentum signal is MANDATORY for each trend
- Summaries are 1-2 sentences max — punchy, not verbose
- Key Takeaways section synthesizes across categories

### Step 5: Optional Deep Dive

After presenting the report, offer:

```
Want me to deep-dive into any of these trends? I can:
-> Research [trend name] in depth (invokes Research skill)
-> Fact-check specific claims (invokes FactCheck skill)
-> Format a trend summary for [platform] (invokes ContentFormat skill)
```

---

## Speed Targets

| Operation | Target |
|-----------|--------|
| Single category scan | 30-60s |
| Full 5-category scan | 2-4min |

## Notes

- This skill DISCOVERS — it does not provide deep analysis. For depth, hand off to Research.
- Recency is everything. A "trend" from 3 months ago is not a trend. Prioritize <7 days old.
- Source URLs are non-negotiable. No trend listed without at least one source.
- Cross-reference when possible. A trend appearing in multiple independent sources has higher momentum.
- When the user specifies a domain, go deeper (5-8 trends) rather than broader.
