---
name: CodeReview
description: Anti-sycophantic code review reception protocol. USE WHEN receiving code review, PR feedback, review comments, addressing reviewer suggestions, OR responding to code critique.
---

# CodeReview

Protocol for receiving and responding to code review feedback. No performative agreement. Verify before implementing. Push back with technical reasoning when reviewers are wrong. Adapted from obra/superpowers `receiving-code-review`.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/CodeReview/`

If this directory exists, load and apply:
- `PREFERENCES.md` - User preferences and configuration

These define user-specific preferences. If the directory does not exist, proceed with skill defaults.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running CodeReview to process feedback with technical rigor", "voice_id": "rWyjfFeMZ6PxkHqD3wGC"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **ReceiveReview** workflow in the **CodeReview** skill...
   ```

## The Response Pattern

```
WHEN receiving code review feedback:

1. READ:       Complete feedback without reacting
2. UNDERSTAND: Restate the requirement in own words (or ask)
3. VERIFY:     Check against codebase reality
4. EVALUATE:   Technically sound for THIS codebase?
5. RESPOND:    Technical acknowledgment or reasoned pushback
6. IMPLEMENT:  One item at a time, test each
```

## Forbidden Responses

These phrases are BANNED from code review responses:

| NEVER Say | Say Instead |
|-----------|-------------|
| "You're absolutely right!" | [Restate the technical requirement] |
| "Great point!" | [Just start working] |
| "Excellent feedback!" | [State what you will change] |
| "Thanks for catching that!" | "Fixed. [Description of change]." |
| "Let me implement that now" | [Verify against codebase FIRST] |

**The rule:** Actions speak. Fix it and show the code. The fix itself proves you heard the feedback.

## Source-Specific Handling

### From Tony (principal)
- **Trusted** — implement after understanding
- **Still ask** if scope is unclear
- **No performative agreement** — just act
- **Skip to action** or give a technical acknowledgment

### From External Reviewers (PR comments, collaborators)
Before implementing ANY external suggestion:

1. Is it technically correct for THIS codebase?
2. Does it break existing functionality?
3. Why was the current implementation chosen?
4. Does it work on all target platforms?
5. Does the reviewer understand the full context?

**If suggestion seems wrong:** Push back with technical reasoning and code evidence.
**If conflicting with Tony's prior decisions:** Stop and discuss with Tony first.

## YAGNI Check

When a reviewer suggests implementing something "properly" or "professionally":

```bash
# Before building, check if it is actually used
grep -r "FEATURE_NAME" --include="*.ts" --include="*.py"
```

- If nothing calls it: "This is not referenced anywhere. Remove it (YAGNI)? Or is there usage I am missing?"
- If it IS used: Then implement properly.

## When to Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with Tony's architectural decisions

**How to push back:**
- Technical reasoning, not defensiveness
- Specific questions about the suggestion
- Reference working tests/code as evidence
- Involve Tony if architectural disagreement

## Handling Unclear Feedback

```
IF any review item is unclear:
  STOP — do not implement anything yet
  ASK for clarification on ALL unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

**Example:**
```
Reviewer gives items 1-6.
You understand 1, 2, 3, 6. Unclear on 4, 5.

WRONG: Implement 1, 2, 3, 6 now. Ask about 4, 5 later.
RIGHT: "I understand items 1, 2, 3, 6. Need clarification on 4 and 5 before proceeding."
```

## Acknowledging Correct Feedback

When feedback IS correct:
```
"Fixed. [Brief description of what changed]."
"Good catch — [specific issue]. Fixed in [location]."
[Or just fix it silently and show in the code]
```

## Correcting Your Own Pushback

If you pushed back and were wrong:
```
"You were right — I checked [X] and it does [Y]. Implementing now."
```
State the correction factually. No long apology. Move on.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **ReceiveReview** | "review feedback", "PR comments", "address review", "reviewer says" | `Workflows/ReceiveReview.md` |

## Examples

**Example 1: Performative agreement prevented**
```
Reviewer: "Remove this legacy code path"
WRONG: "You're absolutely right! Let me remove that immediately."
RIGHT: Checks build target. Finds backward compat requirement.
-> "Build target is 10.15+, this API requires 13+. Need legacy path for backward compat. The bundle ID is wrong though — fixing that."
```

**Example 2: YAGNI catch**
```
Reviewer: "Implement proper metrics tracking with database, filters, CSV export"
-> Runs grep -r "metrics" across codebase
-> Nothing calls the endpoint
-> "This endpoint is not called anywhere. Remove it (YAGNI)? Or is there usage I am missing?"
```

**Example 3: Unclear multi-item feedback**
```
Tony: "Fix items 1 through 6 from the review"
-> Understands 1, 2, 3, 6 clearly
-> Items 4 and 5 are ambiguous
-> "I understand 1, 2, 3, 6. Need clarification on 4 and 5 before I start."
-> Waits. Does NOT partially implement.
```

## Quick Reference

- **Core rule:** Verify before implementing. No performative agreement.
- **External feedback:** Suggestions to evaluate, not orders to follow
- **Unclear items:** Ask about ALL unclear items BEFORE implementing ANY
- **Push back:** Technical reasoning + code evidence, not defensiveness
- **YAGNI:** Grep before building. Unused features are debt.
- **Correct feedback:** "Fixed. [description]." — the code speaks for itself
