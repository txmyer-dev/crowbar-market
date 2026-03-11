# ExecutePattern Workflow

Execute Fabric patterns natively without spawning the fabric CLI. Patterns are applied directly from local storage for faster, more integrated execution.

---

## Workflow Steps

### Step 1: Identify Pattern from Intent

Based on the user's request, select the appropriate pattern:

| User Intent Contains | Pattern |
|---------------------|---------|
| "extract wisdom", "wisdom" | `extract_wisdom` |
| "summarize", "summary" | `summarize` |
| "5 sentence", "short summary" | `create_5_sentence_summary` |
| "micro summary", "tldr" | `create_micro_summary` |
| "threat model" | `create_threat_model` |
| "stride", "stride model" | `create_stride_threat_model` |
| "analyze claims", "fact check" | `analyze_claims` |
| "analyze code", "code review" | `analyze_code` or `review_code` |
| "main idea", "core message" | `extract_main_idea` |
| "improve writing", "enhance" | `improve_writing` |
| "improve prompt" | `improve_prompt` |
| "extract insights" | `extract_insights` |
| "analyze malware" | `analyze_malware` |
| "create prd" | `create_prd` |
| "mermaid", "diagram" | `create_mermaid_visualization` |
| "rate", "evaluate" | `rate_content` or `judge_output` |

**If pattern is explicitly named:** Use that pattern directly (e.g., "use extract_article_wisdom" -> `extract_article_wisdom`)

### Step 2: Load Pattern System Prompt

Read the pattern's system.md file:

```bash
PATTERN_NAME="[selected_pattern]"
PATTERN_PATH="$HOME/.claude/skills/Fabric/Patterns/$PATTERN_NAME/system.md"

if [ -f "$PATTERN_PATH" ]; then
  cat "$PATTERN_PATH"
else
  echo "Pattern not found: $PATTERN_NAME"
  echo "Available patterns:"
  ls ~/.claude/skills/Fabric/Patterns/ | head -20
fi
```

### Step 3: Apply Pattern to Content

**Native Execution (Preferred):**

The pattern's system.md contains instructions formatted as:
- IDENTITY AND PURPOSE
- STEPS
- OUTPUT INSTRUCTIONS

Apply these instructions to the provided content directly. This is the AI reading and following the pattern instructions, not calling an external tool.

**Example:**
```
[Content from user]
↓
[Read Patterns/extract_wisdom/system.md]
↓
[Follow the STEPS and OUTPUT INSTRUCTIONS]
↓
[Return structured output per pattern spec]
```

### Step 4: Content Extraction for URLs

**YouTube URLs (youtube.com, youtu.be, m.youtube.com):**

**NEVER use WebFetch for YouTube URLs — it will always fail.** Go directly to yt-dlp.

Extract transcript using yt-dlp (no Fabric CLI needed):
```bash
yt-dlp --write-auto-sub --skip-download --sub-format vtt \
  -o /tmp/yt-transcript "$YOUTUBE_URL" 2>/dev/null
# Convert VTT to plain text (strip timestamps and formatting)
sed '/^$/d; /^[0-9]/d; /^NOTE/d; /^WEBVTT/d; /-->/d' /tmp/yt-transcript*.vtt | \
  awk '!seen[$0]++' > /tmp/yt-transcript.txt
```
Then apply the pattern to the extracted transcript text.

**Web URLs:**

Use the WebFetch tool (native to Claude Code) to retrieve page content, then apply the pattern to the fetched content. No external CLI needed.

### Step 5: Format Output

Return the pattern's specified output format. Most patterns define structured sections like:

**extract_wisdom example:**
```
## SUMMARY
[1-sentence summary]

## IDEAS
- [idea 1]
- [idea 2]
...

## INSIGHTS
- [insight 1]
- [insight 2]
...

## QUOTES
- "[quote 1]"
- "[quote 2]"
...

## HABITS
- [habit 1]
...

## FACTS
- [fact 1]
...

## REFERENCES
- [reference 1]
...

## RECOMMENDATIONS
- [recommendation 1]
...
```

---

## Pattern Selection Decision Tree

```
User Request
    │
    ├─ Contains "wisdom" or "insights"?
    │   └─ Yes → extract_wisdom / extract_insights
    │
    ├─ Contains "summarize" or "summary"?
    │   ├─ "5 sentence" → create_5_sentence_summary
    │   ├─ "micro" or "tldr" → create_micro_summary
    │   └─ Default → summarize
    │
    ├─ Contains "threat model"?
    │   ├─ "stride" → create_stride_threat_model
    │   └─ Default → create_threat_model
    │
    ├─ Contains "analyze"?
    │   ├─ "claims" → analyze_claims
    │   ├─ "code" → analyze_code
    │   ├─ "malware" → analyze_malware
    │   ├─ "paper" → analyze_paper
    │   └─ Match keyword → analyze_[keyword]
    │
    ├─ Contains "improve"?
    │   ├─ "writing" → improve_writing
    │   ├─ "prompt" → improve_prompt
    │   └─ Default → improve_writing
    │
    ├─ Contains "create"?
    │   ├─ "prd" → create_prd
    │   ├─ "mermaid" / "diagram" → create_mermaid_visualization
    │   └─ Match keyword → create_[keyword]
    │
    └─ Pattern explicitly named?
        └─ Use that pattern directly
```

---

## Available Pattern Categories

### Extraction (30+)
`extract_wisdom`, `extract_insights`, `extract_main_idea`, `extract_recommendations`, `extract_article_wisdom`, `extract_book_ideas`, `extract_predictions`, `extract_questions`, `extract_controversial_ideas`, `extract_business_ideas`, `extract_skills`, `extract_patterns`, `extract_references`, `extract_instructions`, `extract_primary_problem`, `extract_primary_solution`, `extract_product_features`, `extract_core_message`

### Summarization (20+)
`summarize`, `create_5_sentence_summary`, `create_micro_summary`, `summarize_meeting`, `summarize_paper`, `summarize_lecture`, `summarize_newsletter`, `summarize_debate`, `youtube_summary`, `summarize_git_changes`, `summarize_git_diff`

### Analysis (35+)
`analyze_claims`, `analyze_code`, `analyze_malware`, `analyze_paper`, `analyze_logs`, `analyze_debate`, `analyze_incident`, `analyze_comments`, `analyze_email_headers`, `analyze_personality`, `analyze_presentation`, `analyze_product_feedback`, `analyze_prose`, `analyze_risk`, `analyze_sales_call`, `analyze_threat_report`, `analyze_bill`, `analyze_candidates`

### Creation (50+)
`create_threat_model`, `create_stride_threat_model`, `create_prd`, `create_design_document`, `create_user_story`, `create_mermaid_visualization`, `create_markmap_visualization`, `create_visualization`, `create_sigma_rules`, `create_report_finding`, `create_newsletter_entry`, `create_keynote`, `create_academic_paper`, `create_flash_cards`, `create_quiz`, `create_art_prompt`, `create_command`, `create_pattern`

### Improvement (10+)
`improve_writing`, `improve_academic_writing`, `improve_prompt`, `improve_report_finding`, `review_code`, `review_design`, `refine_design_document`, `humanize`, `enrich_blog_post`, `clean_text`

### Security (15)
`create_threat_model`, `create_stride_threat_model`, `create_threat_scenarios`, `create_security_update`, `create_sigma_rules`, `write_nuclei_template_rule`, `write_semgrep_rule`, `analyze_threat_report`, `analyze_malware`, `analyze_incident`, `analyze_risk`

### Rating/Evaluation (8)
`rate_ai_response`, `rate_content`, `rate_value`, `judge_output`, `label_and_rate`, `check_agreement`

---

## Error Handling

**Pattern not found:**
```
Pattern '[name]' not found in ~/.claude/skills/Fabric/Patterns/

Similar patterns:
- [suggestion 1]
- [suggestion 2]

Run 'update fabric' to sync latest patterns.
```

**No content provided:**
```
No content provided for pattern execution.
Please provide:
- Text directly
- URL to fetch (via WebFetch)
- YouTube URL (transcript extracted via yt-dlp)
- File path to read
```

---

## Output

Return the structured output as defined by the pattern's OUTPUT INSTRUCTIONS section. Always preserve the pattern's specified format for consistency.
