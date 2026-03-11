# CleanInbox Workflow

## Classification Rubric (Define BEFORE Execution)

### IMPORTANT (keep as unread)

An email is important if ANY of these are true:
- **Personalized content** — references you by name with specific context (not just "Hi Tony" template)
- **Human-written** — clearly composed by a person, not a system/template
- **Substantive content** — contains information that requires action or decision
- **Known contact with genuine input** — someone you've communicated with before, saying something meaningful
- **Financial alerts** — bank transactions, payment confirmations, billing issues
- **Security alerts** — password changes, login attempts, 2FA codes
- **Calendar/scheduling** — meeting requests, time-sensitive coordination
- **Replies to your emails** — any response in a thread you initiated

### NOT IMPORTANT (safe to mark as read)

An email is not important if ALL of these are true:
- **Automated/system-generated** — newsletters, digests, notification summaries
- **Marketing/promotional** — sales, deals, product announcements, "limited time offer"
- **Cold outreach** — unsolicited pitches from strangers
- **Mass emails** — sent to a list, not specifically to you
- **Social notifications** — "[Person] liked your post", "[Person] started following you"
- **Shipping updates** — "Your package is on the way" (unless user specifically tracks packages)
- **Subscription confirmations** — "Thanks for subscribing", "Welcome to..."

### EDGE CASES — When Uncertain, Keep As Unread

- If you can't confidently classify → keep as unread (false negative is better than false positive)
- Emails from unknown senders with specific questions → keep as unread
- Automated emails that contain actionable items (e.g., "your subscription is expiring") → keep as unread
- First email from a real person, even if it looks like outreach → keep as unread

## Execution Steps

### Step 1: Fetch Unread Emails

Use Gmail MCP to search for unread emails:
```
Search query: "is:unread" (or "is:unread in:inbox" for inbox only)
```

Load the Gmail search tool first via ToolSearch, then fetch messages. For each message, extract:
- From (sender name + email)
- Subject
- Date
- First 200 words of body (enough for classification, not the whole email)

### Step 2: Classify Each Email

Apply the rubric above to each email. Create a classification table:

```markdown
| # | From | Subject | Classification | Reason |
|---|------|---------|---------------|--------|
| 1 | John Smith <john@...> | Re: Project update | IMPORTANT | Reply in active thread |
| 2 | LinkedIn <notifications@...> | You have 5 new notifications | NOT IMPORTANT | Social notification |
| 3 | Unknown <sales@...> | Quick question about your business | IMPORTANT (uncertain) | Could be real person |
```

### Step 3: Present for Review (MANDATORY — Do Not Skip)

Present the full classification table to the user. Ask:

> "Here's how I classified your {N} unread emails. {X} marked as important (keeping unread), {Y} marked as not important (will mark as read). Want me to proceed, or should I reclassify any?"

**Use AskUserQuestion tool** with options:
- "Proceed — mark {Y} emails as read"
- "Let me review the list first"
- "Keep everything as is — don't mark anything"

### Step 4: Mark as Read (Only After Approval)

After user confirms, mark the NOT IMPORTANT emails as read using Gmail MCP.

Report results:
```markdown
## Inbox Cleanup Complete

- **Kept as unread (important):** {X} emails
- **Marked as read:** {Y} emails
- **Total processed:** {N} emails
```

## Safety Rules

1. **NEVER delete emails** — only mark as read
2. **NEVER mark as read without user review** — Step 3 is mandatory
3. **When uncertain, keep as unread** — false negatives are cheap, false positives lose important emails
4. **Show your reasoning** — the "Reason" column lets the user correct misclassifications
5. **Respect the rubric** — don't improvise. If the email doesn't clearly match NOT IMPORTANT criteria, it's IMPORTANT

## Quality Check

Before presenting classification:
- [ ] Every email has a classification AND a reason
- [ ] Uncertain emails are classified as IMPORTANT
- [ ] Financial and security alerts are always IMPORTANT
- [ ] Replies to user's threads are always IMPORTANT
- [ ] Cold outreach from real humans with specific questions → IMPORTANT (uncertain)
- [ ] The user can review before any action is taken
