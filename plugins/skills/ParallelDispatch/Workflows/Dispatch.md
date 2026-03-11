# Dispatch Workflow

## Prerequisites
- 2+ independent problems identified
- Confirmed independence (no shared files, no shared state, no causal relationship)

## Execution

### Step 1: Identify Independent Domains

1. **List all problems** — failures, tasks, or investigations needed
2. **Group by domain** — Which files/subsystems does each affect?
3. **Test independence:**
   - Could fixing Problem A also fix Problem B? If yes, they are NOT independent.
   - Would Agent A and Agent B edit the same files? If yes, do NOT parallelize.
   - Does understanding Problem A require context from Problem B? If yes, investigate together.

**Gate:** If any problems are related, investigate the related ones together in a single agent. Only dispatch truly independent domains.

### Step 2: Compose Agent Prompts

For EACH independent domain, fill in this template:

```markdown
## SCOPE: [Domain name]
[List exact files, test names, or subsystem boundaries]

## GOAL: [Specific verifiable outcome]
[e.g., "All 3 tests in agent-tool-abort.test.ts pass"]

## CONSTRAINTS:
- Do NOT modify files outside: [list allowed files]
- Do NOT change: [protected code/config]
- If blocked, return what you found instead of guessing

## EXPECTED OUTPUT:
1. Root cause: [one sentence]
2. Changes made: [file:line descriptions]
3. Verification: [paste test output or proof]
4. Related issues: [similar patterns found elsewhere, or "none"]
```

**Prompt quality checklist:**
- [ ] Scope is specific (one file/subsystem, not "fix everything")
- [ ] Goal is verifiable (pass/fail, not "improve")
- [ ] Constraints prevent scope creep
- [ ] Expected output format is explicit

### Step 3: Select Models and Dispatch

Choose model per agent based on complexity:

| Complexity | Model | When |
|-----------|-------|------|
| Simple (known fix, clear error) | `haiku` | Speed priority |
| Standard (investigation needed) | `sonnet` | Balanced |
| Complex (architectural, ambiguous) | `opus` | Accuracy priority |

Dispatch all agents in a SINGLE message with multiple Task tool calls:

```typescript
Task({ subagent_type: "Engineer", model: "sonnet", prompt: "[Agent 1 prompt]" })
Task({ subagent_type: "Engineer", model: "sonnet", prompt: "[Agent 2 prompt]" })
Task({ subagent_type: "Engineer", model: "sonnet", prompt: "[Agent 3 prompt]" })
```

### Step 4: Review and Integrate

When all agents return:

1. **Read each summary** — Understand what each found and changed
2. **Check for conflicts:**
   ```
   Did any agents edit the same file? → Manual review needed
   Did any agents make contradictory changes? → Resolve before proceeding
   Did any agents fail? → Investigate individually
   ```
3. **Run full verification:**
   ```bash
   # Run the complete test suite, not just individual tests
   # ALL fixes must work together
   ```
4. **Spot check** — Launch a verification agent:
   ```typescript
   Task({
     subagent_type: "Intern",
     model: "haiku",
     prompt: "Review these changes for consistency and correctness: [summaries]"
   })
   ```

## Output

Report to user:
- **Agents dispatched:** [count] agents across [domains]
- **Results:** Summary per agent (root cause + fix)
- **Conflicts:** Any file conflicts detected and resolved
- **Verification:** Full suite output showing all fixes work together
