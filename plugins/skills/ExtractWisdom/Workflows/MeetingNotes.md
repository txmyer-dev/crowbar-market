# MeetingNotes Workflow

Extracts operational structure from meeting transcripts: action items, decisions, contacts, and open questions. This is **operational extraction** — not insight extraction. For wisdom/insight extraction, use the Extract workflow instead.

## When to Use

- User has a meeting transcript, call recording notes, or meeting summary
- User says "meeting notes", "action items", "what did we decide", "meeting summary"
- User wants to know WHO needs to do WHAT by WHEN

## Input

Meeting transcript, call notes, or audio transcription. Can be:
- Raw transcript (Zoom, Teams, Otter.ai, etc.)
- Meeting notes someone typed
- Audio transcription from Parser skill

## Extraction Categories

### 1. Action Items (Primary Output)

Extract every commitment, task, or follow-up mentioned. Present as a table:

```markdown
| # | Action Item | Owner | Deadline | Context |
|---|-------------|-------|----------|---------|
| 1 | Send revised proposal to client | Sarah | Friday March 7 | Client requested changes to pricing section |
| 2 | Set up staging environment | Tony | No deadline stated | Blocked until DevOps approves access |
| 3 | Schedule follow-up meeting | Unassigned | Next week | Need to review Q2 numbers |
```

**Rules:**
- If no owner is explicitly mentioned, mark as "Unassigned"
- If no deadline is stated, mark as "No deadline stated"
- Context column captures WHY the action item exists (not just WHAT)
- Include implicit action items ("I'll look into that" = action item for that speaker)
- If someone says "we should" without assigning it, mark as "Unassigned — mentioned by [speaker]"

### 2. Decisions Made

Things that were agreed upon, approved, or decided during the meeting:

```markdown
## Decisions Made

- **Pricing model:** Switching from per-seat to usage-based pricing starting Q2
- **Hire timeline:** Will post the senior engineer role by end of week
- **Tech stack:** Going with PostgreSQL over MongoDB for the new service
```

**Rules:**
- Only include actual decisions (consensus reached), not proposals still being debated
- Include the decision AND enough context to understand why
- If a decision reverses a previous decision, note what changed

### 3. Contacts Mentioned

People referenced who aren't in the meeting, or meeting attendees with roles worth noting:

```markdown
## Contacts

| Name | Role/Context | Email/Contact | Follow-Up Needed? |
|------|-------------|---------------|-------------------|
| Maria Chen | Client PM at Acme Corp | maria@acme.com | Yes — send revised proposal |
| Jake (DevOps) | Internal — controls staging access | No email mentioned | Yes — request staging access |
```

**Rules:**
- Extract any email addresses, phone numbers, or handles mentioned
- Note relationship context (client, vendor, internal, prospect)
- Flag if follow-up is needed based on action items

### 4. Open Questions

Things raised but not resolved:

```markdown
## Open Questions

- How will usage-based pricing affect our enterprise clients? (Raised by Sarah)
- Do we need legal review before changing the pricing page? (Raised by Tony)
- What's the budget ceiling for the new hire? (No one answered)
```

**Rules:**
- Include who raised the question
- Note if anyone attempted an answer but it wasn't conclusive
- These are often the seeds of next meeting's agenda

## Output Format

```markdown
# MEETING NOTES: {Meeting Title or Topic}
> {Date} | {Duration if known} | {Attendees if known}

---

## Action Items

| # | Action Item | Owner | Deadline | Context |
|---|-------------|-------|----------|---------|
| ... | ... | ... | ... | ... |

## Decisions Made

- **{Decision}:** {Context and rationale}

## Contacts

| Name | Role/Context | Contact | Follow-Up? |
|------|-------------|---------|------------|
| ... | ... | ... | ... |

## Open Questions

- {Question} (Raised by {person})

---

## Quick Summary

{3-5 sentence summary of what the meeting was about, what was accomplished, and what's next}
```

## Quality Check

Before delivering:
- [ ] Every action item has an owner (even if "Unassigned")
- [ ] Deadlines are specific dates, not vague ("next week" → "week of March 10")
- [ ] Decisions are actual decisions, not proposals still in discussion
- [ ] Open questions capture unresolved items, not rhetorical questions
- [ ] Contacts include any mentioned email/phone/handle
- [ ] Quick summary is useful enough to skip reading the full notes
- [ ] No action items are hidden in the "Decisions" section — if it implies action, it goes in the table
