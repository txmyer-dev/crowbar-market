# Debug Workflow

## Prerequisites
- Error message, stack trace, or description of unexpected behavior
- Access to the failing code/system

## Execution

### Step 1: Root Cause Analysis

1. **Read the full error output** — Do not skim. Read every line of the error message, stack trace, and any surrounding log output.

2. **Reproduce the failure:**
   ```bash
   # Run the specific failing test or trigger the error
   # Record the EXACT output
   ```

3. **Identify the divergence point:**
   - What is the expected behavior?
   - What is the actual behavior?
   - At what exact point do they diverge?

4. **Check what changed:**
   ```bash
   git log --oneline -10      # Recent commits
   git diff HEAD~3            # Recent changes
   ```

5. **Form initial hypothesis:** Write one sentence: "The bug is caused by [X] because [Y]."

**Gate:** Do NOT proceed until you have a specific hypothesis. "Something is wrong with X" is not a hypothesis. "X fails because Y returns null when Z is empty" is.

### Step 2: Pattern Analysis

1. **Classify the pattern:**
   - Race condition / timing issue
   - Null/undefined reference
   - Off-by-one / boundary error
   - Stale cache / stale state
   - Type mismatch / serialization
   - Missing error handling
   - Configuration drift
   - Dependency version conflict

2. **Check for related occurrences:**
   ```bash
   # Search codebase for similar patterns
   grep -r "PATTERN" --include="*.ts" --include="*.py"
   ```

3. **Check memory for past similar issues:**
   - Review `~/.claude/MEMORY/` for related debugging notes
   - Check session history for similar errors

### Step 3: Hypothesis Testing

1. **Design a minimal test:**
   - Write the smallest possible test that will prove or disprove your hypothesis
   - This might be a unit test, a log statement, or a manual verification step

2. **Run the test BEFORE writing any fix:**
   ```bash
   # Execute your diagnostic test
   # Record the result
   ```

3. **Evaluate:**
   - Hypothesis confirmed → Proceed to Step 4
   - Hypothesis disproved → Return to Step 1 with the new information
   - Inconclusive → Refine the test to be more specific

**Escalation check:** If this is your 3rd failed hypothesis, STOP. The problem is likely architectural. Step back and consider:
- Am I looking at the right layer of the system?
- Is this a symptom of a deeper issue?
- Should I read more broadly before guessing again?

### Step 4: Implementation

1. **Write the minimal fix:**
   - Change only what is necessary to address the confirmed root cause
   - Do NOT refactor surrounding code
   - Do NOT add "while I'm here" improvements

2. **Verify the fix:**
   ```bash
   # Run the originally failing test
   # It MUST pass now
   ```

3. **Check for regressions:**
   ```bash
   # Run the full related test suite
   # All tests must pass, not just the one you fixed
   ```

4. **Document:**
   - What was the root cause?
   - Why did the fix work?
   - Are there other places in the codebase with the same pattern?

## Output

Report to the user:
- **Root cause:** One sentence explaining WHY it was broken
- **Fix:** What you changed and why
- **Verification:** Evidence that the fix works (test output)
- **Scope:** Whether similar issues exist elsewhere
