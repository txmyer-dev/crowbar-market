---
name: SystematicDebugging
description: 4-phase systematic debugging process. USE WHEN debugging, bug fix, test failure, error investigation, root cause analysis, something broken, fix failing tests, OR 3+ failed fix attempts on same issue.
---

# SystematicDebugging

4-phase debugging process adapted from obra/superpowers. Prevents shotgun debugging and symptom-chasing.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/SystematicDebugging/`

If this directory exists, load and apply:
- `PREFERENCES.md` - User preferences and configuration

These define user-specific preferences. If the directory does not exist, proceed with skill defaults.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running SystematicDebugging to investigate the root cause", "voice_id": "rWyjfFeMZ6PxkHqD3wGC"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **Debug** workflow in the **SystematicDebugging** skill...
   ```

## The Hard Rules

1. **NO FIXES WITHOUT ROOT CAUSE INVESTIGATION** — Never change code to "try something." Understand WHY it's broken first.
2. **ONE CHANGE AT A TIME** — Change one thing, verify, proceed. Never batch speculative fixes.
3. **3+ FAILED FIXES = ESCALATE** — If 3 attempts haven't fixed it, stop. The problem is architectural, not tactical. Step back and reassess.
4. **EVIDENCE OVER INTUITION** — Read error messages, stack traces, logs. Don't guess.

## The 4 Phases

### Phase 1: Root Cause Analysis
- Read the FULL error message/stack trace
- Reproduce the failure reliably
- Identify the exact line/function/module where behavior diverges from expectation
- Ask: "What changed?" (recent commits, config changes, dependency updates)
- **Output:** A specific hypothesis about WHY, not just WHERE

### Phase 2: Pattern Analysis
- Is this a known pattern? (race condition, off-by-one, null reference, stale cache)
- Have we seen this before in this codebase?
- Check MEMORY files for similar past issues
- Search codebase for related patterns that might have the same bug
- **Output:** Pattern classification and scope assessment

### Phase 3: Hypothesis Testing
- Form a specific, falsifiable hypothesis: "The bug is caused by X because Y"
- Design a minimal test that proves/disproves the hypothesis
- Run the test BEFORE writing any fix
- If hypothesis is wrong, return to Phase 1 with new information
- **Output:** Confirmed root cause with evidence

### Phase 4: Implementation
- Write the minimal fix that addresses the confirmed root cause
- Run the original failing test to confirm the fix works
- Run the full related test suite to check for regressions
- Document what was wrong and why the fix works
- **Output:** Working fix with verification evidence

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Debug** | "debug", "fix bug", "investigate error", "root cause" | `Workflows/Debug.md` |

## Escalation Signals

Stop and reassess the approach when:
- 3+ fix attempts haven't resolved the issue
- The fix requires changing code you don't understand
- Multiple subsystems are involved
- The error message doesn't match the failure
- "It works on my machine" scenarios

## Examples

**Example 1: Test failure investigation**
```
User: "These 3 tests are failing after the refactor"
-> Invokes Debug workflow
-> Phase 1: Reads full error output, identifies divergence point
-> Phase 2: Recognizes race condition pattern from timing-dependent failures
-> Phase 3: Adds targeted logging, confirms event ordering issue
-> Phase 4: Fixes event ordering, all 3 tests pass, no regressions
```

**Example 2: Escalation after repeated failures**
```
User: "I've tried 4 things and the API still returns 500"
-> Invokes Debug workflow
-> Recognizes 3+ failed attempts = escalation signal
-> Steps back to Phase 1: reads server logs instead of guessing
-> Discovers database connection pool exhaustion (architectural)
-> Fixes pool configuration, not the API handler
```

**Example 3: Production error**
```
User: "Users are reporting intermittent timeouts"
-> Invokes Debug workflow
-> Phase 1: Collects error patterns (when, how often, which endpoints)
-> Phase 2: Identifies as connection leak pattern
-> Phase 3: Monitors connection count to confirm leak hypothesis
-> Phase 4: Fixes unclosed connection in error path, verifies with load test
```

## Quick Reference

- **Phase 1:** Find WHERE and WHY (not just WHERE)
- **Phase 2:** Classify the pattern
- **Phase 3:** Prove your hypothesis before touching code
- **Phase 4:** Minimal fix + verification
- **Hard stop:** 3 failed fixes = step back, reassess
