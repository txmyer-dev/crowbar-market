---
name: ParallelDispatch
description: Structured parallel agent dispatch for independent problems. USE WHEN multiple failures across different files, parallel tasks, independent bugs, fan-out work, OR dispatching subagents for concurrent investigation.
---

# ParallelDispatch

Dispatch one agent per independent problem domain. Prevents sequential investigation of unrelated failures. Adapted from obra/superpowers `dispatching-parallel-agents`.

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/ParallelDispatch/`

If this directory exists, load and apply:
- `PREFERENCES.md` - User preferences and configuration

These define user-specific preferences. If the directory does not exist, proceed with skill defaults.

## Voice Notification

**When executing a workflow, do BOTH:**

1. **Send voice notification**:
   ```bash
   curl -s -X POST http://localhost:8888/notify \
     -H "Content-Type: application/json" \
     -d '{"message": "Running ParallelDispatch to fan out independent work", "voice_id": "rWyjfFeMZ6PxkHqD3wGC"}' \
     > /dev/null 2>&1 &
   ```

2. **Output text notification**:
   ```
   Running the **Dispatch** workflow in the **ParallelDispatch** skill...
   ```

## The Decision Tree

```
Multiple problems? ──yes──> Are they independent? ──yes──> Shared state? ──no──> PARALLEL DISPATCH
       │                         │                           │
       no                        no (related)                yes
       │                         │                           │
  Single agent              Single agent               Sequential agents
```

**Parallel when:**
- 3+ failures across different files/subsystems with different root causes
- Multiple independent tasks (no shared files, no shared resources)
- Each problem can be understood without context from the others

**Sequential when:**
- Failures are related (fixing one might fix others)
- Exploratory phase (you do not know what is broken yet)
- Agents would edit the same files or use the same resources
- You need full system understanding before acting

## The Agent Prompt Template

Every dispatched agent gets exactly 4 elements:

```markdown
## SCOPE: [One specific problem domain]
[Exactly what files/tests/subsystem this agent owns]

## GOAL: [One clear outcome]
[What "done" looks like — specific and verifiable]

## CONSTRAINTS:
- Do NOT modify files outside [scope]
- Do NOT [specific thing to avoid]
- [Any other boundaries]

## EXPECTED OUTPUT:
Return a summary containing:
1. Root cause identified
2. What you changed and why
3. Verification output (test results, logs, etc.)
4. Whether similar issues exist elsewhere
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Scope too broad ("fix all tests") | One file or subsystem per agent |
| No context in prompt | Paste error messages and test names |
| No constraints | Agent might refactor everything — set boundaries |
| Vague output expectations | Specify: "Return summary of root cause and changes" |
| Dispatching related failures | Investigate together first — fixing one may fix others |

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Dispatch** | "parallel agents", "fan out", "dispatch", "independent problems" | `Workflows/Dispatch.md` |

## Examples

**Example 1: Multiple test file failures**
```
User: "6 tests failing across 3 different files after the refactor"
-> Invokes Dispatch workflow
-> Groups failures by subsystem (abort logic, batch completion, race conditions)
-> Dispatches 3 agents with focused prompts
-> Reviews all results, checks for conflicts, runs full suite
```

**Example 2: Independent subsystem tasks**
```
User: "Update the auth module, fix the email templates, and add the new API endpoint"
-> Invokes Dispatch workflow
-> Confirms no shared state between tasks
-> Dispatches 3 agents (auth, email, API) in parallel
-> Integrates results, runs full verification
```

**Example 3: Deciding NOT to parallelize**
```
User: "These 4 endpoints are all returning 500 errors"
-> Investigates FIRST before dispatching
-> Discovers all 4 share the same database connection pool
-> Single agent fixes the pool config — all 4 endpoints recover
-> Parallel dispatch would have been wasted work
```

## Quick Reference

- **Core rule:** One agent per independent problem domain
- **Template:** SCOPE / GOAL / CONSTRAINTS / EXPECTED OUTPUT
- **After dispatch:** Review summaries → Check conflicts → Full test suite → Spot check
- **Model tip:** Use `haiku` or `sonnet` for parallel agents (speed), `opus` for spot check (accuracy)
