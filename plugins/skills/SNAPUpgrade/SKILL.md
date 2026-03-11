---
name: SNAPUpgrade
description: Extract system improvements from content AND monitor external sources (Anthropic ecosystem, YouTube). USE WHEN upgrade, improve system, system upgrade, analyze for improvements, check Anthropic, Anthropic changes, new Claude features, check YouTube, new videos. SkillSearch('upgrade') for docs.
context: fork
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/SNAPUpgrade/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.


## 🚨 MANDATORY: Voice Notification (REQUIRED BEFORE ANY ACTION)

**You MUST send this notification BEFORE doing anything else when this skill is invoked.**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running the WORKFLOWNAME workflow in the SNAPUpgrade skill to ACTION"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **WorkflowName** workflow in the **SNAPUpgrade** skill to ACTION...
   ```

**This is not optional. Execute this curl command immediately upon skill invocation.**

# SNAPUpgrade Skill

**Primary Purpose:** Generate prioritized upgrade recommendations for the user's existing SNAP setup by understanding their context and discovering what's new in the ecosystem.

The skill runs **two parallel agent threads** that converge into personalized recommendations:

```
Thread 1: USER CONTEXT           Thread 2: SOURCE COLLECTION
┌─────────────────────┐         ┌─────────────────────┐
│ TELOS Analysis      │         │ Anthropic Sources   │
│ Project Analysis    │         │ YouTube Channels    │
│ Recent Work History │         │ Custom USER Sources │
│ SNAP System State    │         │ Community Updates   │
└─────────────────────┘         └─────────────────────┘
           │                              │
           └──────────┬───────────────────┘
                      ▼
        ┌─────────────────────────────┐
        │  PRIORITIZED RECOMMENDATIONS │
        │  (personalized to user)      │
        └─────────────────────────────┘
```

---


## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Upgrade** | "check for upgrades", "check sources", "any updates", "check Anthropic", "check YouTube", "upgrade", "pai upgrade" | `Workflows/Upgrade.md` |
| **ResearchUpgrade** | "research this upgrade", "deep dive on [feature]", "further research" | `Workflows/ResearchUpgrade.md` |
| **FindSources** | "find upgrade sources", "find new sources", "discover channels" | `Workflows/FindSources.md` |

**Default workflow:** If user says "upgrade" or "check for upgrades" without specifics, run the **Upgrade** workflow.

---

## Primary Output Format

**Granular. Extracted. SNAP-Contextualized.**

The output provides SPECIFIC TECHNIQUES extracted from actual content, not links to watch or recommendations to read. Every tip explains WHY it matters for YOUR SNAP system.

```markdown
# SNAP Upgrade Report
**Generated:** [timestamp]
**Sources Processed:** [N] release notes parsed | [N] videos transcribed | [N] docs analyzed

---

## 🎯 Extracted Techniques

These are SPECIFIC techniques pulled from actual content. Each one maps to your SNAP system.

### From Release Notes

#### [Feature/Change Name]
**Source:** GitHub claude-code v2.1.16, commit abc123

**What It Is (16-32 words):**
[Describe the technique itself - what it does, how it works, what capability it provides. Must be 16-32 words, concrete and specific.]

**How It Helps SNAP (16-32 words):**
[Describe the specific benefit to our SNAP system - which component improves, what gap it fills, what becomes possible. Must be 16-32 words.]

**The Technique:**
> [Exact code pattern, configuration, or approach - quoted or code-blocked]

**Applies To:** `hooks/SecurityValidator.hook.ts`, ISC verification
**Implementation:**
```typescript
// Before (what you have now)
[current pattern]

// After (with this technique)
[new pattern]
```

---

### From YouTube Videos

#### [Specific Technique Name]
**Source:** R Amjad - "Video Title" @ 12:34

**What It Is (16-32 words):**
[Describe the technique itself - what it does, how it works, what capability it provides. Must be 16-32 words, concrete and specific.]

**How It Helps SNAP (16-32 words):**
[Describe the specific benefit to our SNAP system - which component improves, what gap it fills, what becomes possible. Must be 16-32 words.]

**The Technique:**
> "[Exact quote or paraphrased technique from transcript]"

**Applies To:** Browser skill, delegation system
**Implementation:**
[Specific steps to apply this technique]

---

### From Documentation

#### [Specific Capability/Pattern]
**Source:** Claude Docs - Tool Use section, updated 2026-01-20

**What It Is (16-32 words):**
[Describe the technique itself - what it does, how it works, what capability it provides. Must be 16-32 words, concrete and specific.]

**How It Helps SNAP (16-32 words):**
[Describe the specific benefit to our SNAP system - which component improves, what gap it fills, what becomes possible. Must be 16-32 words.]

**The Technique:**
> [Exact documentation excerpt showing the capability]

**Applies To:** `skills/SNAP/SKILL.md`, agent spawning
**Implementation:**
[Specific changes needed]

---

## 📊 Technique Summary

| # | Technique | Source | SNAP Component | Impact |
|---|-----------|--------|---------------|--------|
| 1 | [technique name] | [source] | [component it affects] | [what changes] |
| 2 | [technique name] | [source] | [component it affects] | [what changes] |

---

## ⏭️ Skipped Content

| Content | Source | Why Skipped |
|---------|--------|-------------|
| [video/doc title] | [source] | [No extractable technique / Not relevant to SNAP / Covers basics you already know] |

---

## 🔍 Sources Processed

**Release Notes Parsed:**
- claude-code v2.1.14, v2.1.15, v2.1.16 → [N] techniques extracted
- MCP 2025-11-25 → [N] techniques extracted

**Videos Transcribed:**
- R Amjad: "Title" (23:45) → [N] techniques extracted
- AI Jason: "Title" (15:20) → 0 techniques (skipped: Gemini focus)

**Docs Analyzed:**
- Claude Tool Use docs → [N] techniques extracted
```

---

## Extraction Rules

**CRITICAL: Extract, don't summarize. Techniques, not recommendations.**

1. **Every output item must be a TECHNIQUE** - A specific pattern, code snippet, configuration, or approach
2. **Quote or code-block the actual content** - Show exactly what was said/written
3. **Map to SNAP components** - Every technique must connect to a specific file, skill, workflow, or system component
4. **Two mandatory description fields (16-32 words each):**
   - **What It Is:** Describe the technique itself - what it does, how it works, what capability it provides
   - **How It Helps SNAP:** Describe the specific benefit - which component improves, what gap it fills, what becomes possible
5. **Provide implementation** - Show before/after code or specific steps
6. **Skip, don't dilute** - If content has no extractable technique, put it in Skipped Content with reason

**Anti-patterns to AVOID:**
- ❌ "Check out this video for more"
- ❌ "This release has improvements"
- ❌ "Consider looking into this"
- ❌ Vague summaries without specific techniques
- ❌ Links without extracted content

**Source Type Labels:**
| Label | Meaning |
|-------|---------|
| `GitHub: claude-code vX.Y.Z` | Specific version release notes |
| `YouTube: Creator @ MM:SS` | Video with timestamp |
| `Docs: Section Name` | Documentation section |
| `Blog: Post Title` | Blog post |

---

## The Two-Thread Architecture

### Thread 1: User Context Analysis

**Purpose:** Deeply understand the user to personalize recommendations.

Launch **parallel agents** to analyze:

| Agent | Focus | Sources |
|-------|-------|---------|
| **TELOS Agent** | User's goals, challenges, current focus | `skills/SNAP/USER/TELOS/*.md` |
| **Project Agent** | Active projects, tech stacks, dependencies | TELOS/PROJECTS.md, recent work context |
| **History Agent** | Recent work patterns, what's been done | `MEMORY/WORK/`, `MEMORY/STATE/current-work.json` |
| **SNAP State Agent** | System capabilities, installed skills, gaps | `skills/`, `hooks/`, `settings.json` |

**Output:** A context object that includes:
- User's current focus areas and priorities
- Active projects and their tech stacks
- Recent work patterns and themes
- SNAP system state and existing capabilities

### Thread 2: Source Collection

**Purpose:** Discover what's new in the ecosystem.

Launch **parallel agents** to check:

| Agent | Focus | Sources |
|-------|-------|---------|
| **Anthropic Agent** | Official Anthropic updates | `Tools/Anthropic.ts` (30+ sources) |
| **YouTube Agent** | Configured channels for new videos | USER customization channels |
| **Custom Source Agent** | Any USER-defined additional sources | USER/SKILLCUSTOMIZATIONS/SNAPUpgrade/ |

**Output:** A collection of discoveries:
- New features, releases, changes from Anthropic
- New videos with transcripts and key insights
- Updates from custom sources

---

## Process Flow

### Step 1: Launch Both Threads in Parallel

Using BACKGROUNDDELEGATION, spawn both analysis threads simultaneously:

```markdown
## Thread 1: User Context (4 parallel agents)

### Agent 1: TELOS Analysis
Read and analyze:
- ~/.claude/skills/SNAP/USER/TELOS/TELOS.md
- ~/.claude/skills/SNAP/USER/TELOS/GOALS.md
- ~/.claude/skills/SNAP/USER/TELOS/PROJECTS.md
- ~/.claude/skills/SNAP/USER/TELOS/CHALLENGES.md
- ~/.claude/skills/SNAP/USER/TELOS/STATUS.md

Extract: Current focus, priorities, active goals, project themes

### Agent 2: Recent Work Analysis
Read and analyze:
- ~/.claude/MEMORY/STATE/current-work.json
- Recent MEMORY/WORK/ directories

Extract: What user has been working on, patterns, open tasks

### Agent 3: SNAP System State
Analyze:
- ~/.claude/skills/ (installed skills)
- ~/.claude/hooks/ (active hooks)
- ~/.claude/settings.json (configuration)

Extract: Current capabilities, potential gaps, system health

### Agent 4: Tech Stack Context
From PROJECTS and recent work, identify:
- Languages and frameworks in use
- Deployment targets
- Integration points

---

## Thread 2: Source Collection (3 parallel agents)

### Agent 1: Anthropic Sources
Run: bun ~/.claude/skills/SNAPUpgrade/Tools/Anthropic.ts
Check all 30+ official sources for updates

### Agent 2: YouTube Channels
Check configured channels for new videos
Extract transcripts from new content

### Agent 3: Custom Sources
Check any USER-defined additional sources
```

### Step 2: Synthesize Results

Once both threads complete:

1. **Merge context:** Combine user analysis into unified context object
2. **Filter discoveries:** Remove items that don't apply to user's stack/focus
3. **Score relevance:** Rate each discovery against user's TELOS and projects
4. **Prioritize:** Sort by (relevance to user × impact × ease)

### Step 3: Generate Recommendations

For each discovery that passes relevance filtering:

1. **Personalize:** Explain why this matters for THIS user specifically
2. **Contextualize:** Map to their projects, goals, and challenges
3. **Actionize:** Provide concrete implementation steps
4. **Estimate:** Rate effort relative to their experience level

### Step 4: Output Report

Generate the prioritized recommendations report (see format above).

---

## Configuration

**Skill Files:**
- `sources.json` - Anthropic sources config (30+ sources)
- `youtube-channels.json` - Base YouTube channels (empty by default)
- `State/last-check.json` - Anthropic state
- `State/youtube-videos.json` - YouTube state

**User Customizations** (`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/SNAPUpgrade/`):
- `EXTEND.yaml` - Extension manifest
- `youtube-channels.json` - User's personal YouTube channels
- Additional source definitions

---

## Tool Reference

| Tool | Purpose |
|------|---------|
| `Tools/Anthropic.ts` | Check Anthropic sources for updates |

---

## Key Principles

1. **Extract, Don't Summarize:** Pull specific techniques from content, never just link to sources
2. **Quote the Source:** Show actual code, documentation quotes, or transcript excerpts
3. **SNAP-Contextualized:** Every technique maps to a specific SNAP file, skill, or component
4. **Explain "Why You":** Use phrases like "This helps because your [X] currently [Y]"
5. **TELOS-Connected:** Reference user's goals and challenges when explaining relevance
6. **Skip Boldly:** If content has no extractable technique, skip it entirely
7. **Implementation-Ready:** Provide actual code changes, not vague recommendations

---

## Examples

**Example 1: Standard upgrade check**
```
User: "check for upgrades"
→ Launch Thread 1 (4 agents analyzing user context)
→ Launch Thread 2 (3 agents checking sources)
→ Wait for both threads
→ Synthesize into prioritized recommendations
→ Output personalized upgrade report
```

**Example 2: Quick Anthropic-only check**
```
User: "check Anthropic only"
→ Run Anthropic.ts tool directly
→ Use cached user context from recent session
→ Quick-match against user focus areas
→ Output filtered recommendations
```

---

## Workflows

- **Upgrade.md** - Primary workflow: full two-thread analysis with prioritized recommendations
- **ResearchUpgrade.md** - Deep dive on a specific upgrade opportunity
- **FindSources.md** - Discover and evaluate new sources to monitor

---

---

## Anti-Patterns (What NOT to Output)

These output patterns are **FAILURES**. If you produce these, you have not completed the skill correctly:

| ❌ Bad Output | Why It's Wrong | ✅ Correct Output |
|---------------|----------------|-------------------|
| "Check out R Amjad's video on Claude Code" | Points to content instead of extracting it | "@ 5:42, R Amjad shows this technique: [quote]" |
| "v2.1.16 has task management improvements" | Vague summary, no technique | "v2.1.16 adds `addBlockedBy` parameter: [code example]" |
| "Consider looking into MCP updates" | Recommendation without extraction | "MCP now supports [specific feature]: [docs quote]" |
| "This could be useful for your workflows" | Vague relevance | "This improves your Browser skill because [specific gap it fills]" |
| "Several videos covered AI agents" | Count without content | "[N] videos skipped - no extractable techniques" |
| "This helps because it improves things" | Vague benefit, no word count | "How It Helps SNAP (16-32 words): Our SecurityValidator currently only blocks commands. This technique enables injecting reasoning context before tool execution, making security decisions more nuanced." |
| "A new hook feature" | No description of what it IS | "What It Is (16-32 words): PreToolUse hooks can return additionalContext that gets injected into the model's context before execution, enabling reasoning-based decisions rather than binary blocks." |

**The test:** If you can say "show me the technique" and there's nothing to show, you've failed.

**Word count test:** Each "What It Is" and "How It Helps SNAP" field MUST be 16-32 words. Count them. If under 16, add specificity. If over 32, condense.

---

**This skill embodies SNAP's commitment to continuous, personalized improvement - understanding YOU first, then discovering what's new, then EXTRACTING the actual techniques that matter to your system.**
