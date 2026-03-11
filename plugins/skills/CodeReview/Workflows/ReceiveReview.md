# ReceiveReview Workflow

## Prerequisites
- Code review feedback (PR comments, inline review, verbal feedback)
- Access to the codebase under review

## Execution

### Step 1: Read Complete Feedback

1. **Read ALL items** before reacting to any single one
2. **Number each item** for tracking
3. **Note dependencies** — some items may be related or contradictory

**Gate:** Do NOT start implementing until you have read and understood the full scope of feedback.

### Step 2: Classify Each Item

For each review item, classify:

| Classification | Action |
|---------------|--------|
| **Clear + Correct** | Queue for implementation |
| **Clear + Questionable** | Verify against codebase before implementing |
| **Unclear** | Add to clarification list |
| **Conflicts with existing decisions** | Flag for Tony |

**If ANY items are unclear:** Stop. Ask for clarification on ALL unclear items at once. Do not partially implement.

### Step 3: YAGNI Check (for "improvement" suggestions)

For any item that suggests adding features, abstractions, or "proper" implementations:

```bash
# Check if the thing is actually used
grep -r "FEATURE" --include="*.ts" --include="*.py" --include="*.tsx"
```

- **Used:** Proceed with implementation
- **Not used:** Push back with evidence: "Nothing calls this. YAGNI?"

### Step 4: Verify Questionable Items

For items classified as "Clear + Questionable":

1. **Check the codebase** — Is the reviewer correct about how things work?
2. **Check history** — Why was the current implementation chosen?
   ```bash
   git log --oneline -10 -- [file]
   git blame [file] | grep [relevant-line]
   ```
3. **Check compatibility** — Does the suggestion work on all targets?
4. **Decide:**
   - Reviewer is right → Implement
   - Reviewer is wrong → Push back with technical reasoning and code evidence
   - Can not determine → State limitation, ask for direction

### Step 5: Implement Accepted Items

Process accepted items one at a time:

1. **Pick one item** (priority: blocking issues → simple fixes → complex changes)
2. **Make the change**
3. **Test the change individually:**
   ```bash
   # Run relevant tests AFTER each change
   ```
4. **Verify no regressions**
5. **Move to next item**

**Response format for each fix:**
```
Fixed. [Brief description of what changed and where.]
```

Do NOT say: "Great catch!", "You're absolutely right!", "Thanks for the feedback!"

### Step 6: Push Back on Rejected Items

For items you are rejecting:

```markdown
Item [N]: [Restate the suggestion]
Reason: [Technical reasoning with evidence]
Evidence: [Code reference, test output, or compatibility data]
Alternative: [What you suggest instead, if applicable]
```

### Step 7: Report Summary

After all items are processed:

```markdown
## Review Response

**Implemented:** [count] items
- Item 1: [what changed]
- Item 3: [what changed]

**Pushed back:** [count] items
- Item 2: [reason with evidence]

**Needs clarification:** [count] items
- Item 4: [what is unclear]

**Verification:** [test output showing everything works]
```

## Output

- Per-item responses (implemented, pushed back, or needs clarification)
- Full test suite output after all changes
- No performative language anywhere
