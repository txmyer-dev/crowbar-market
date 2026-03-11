# Client Hooks Package — Core 9

> These hooks form the behavioral backbone of your SNAP system. Each one fires automatically on specific Claude Code events, enforcing quality, security, and consistency without you lifting a finger.

---

## What Are Hooks?

Hooks are TypeScript scripts that run automatically when Claude Code events occur — session start, tool use, response generation, session end. They're the "immune system" of your AI: catching bad patterns, enforcing good ones, and maintaining system integrity.

**How they work:** Registered in `settings.json` under the `hooks` key. Each hook specifies:
- **Trigger event** — when it fires (SessionStart, PreToolUse, PostToolUse, Stop, etc.)
- **Matcher** — which tools trigger it (Bash, Task, Skill, etc.)
- **Command** — the TypeScript file to execute

---

## The Core 9 Hooks

### 1. LoadContext.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | SessionStart |
| **Purpose** | Loads SNAP context (Algorithm, steering rules, identity) into every session |
| **What it does** | Reads SKILL.md + AI Steering Rules and injects them as system context |
| **Why essential** | Without this, your AI forgets its training every session |
| **Dependencies** | `skills/SNAP/SKILL.md`, `skills/SNAP/SYSTEM/AISTEERINGRULES.md`, `skills/SNAP/USER/AISTEERINGRULES.md` |

### 2. FormatReminder.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | UserPromptSubmit |
| **Purpose** | Classifies every prompt's depth (FULL/ITERATION/MINIMAL) using AI inference |
| **What it does** | Sends your prompt to a fast classifier, injects the depth directive |
| **Why essential** | Ensures the Algorithm runs at the right depth — not too heavy for simple requests, not too light for complex ones |
| **Dependencies** | `skills/SNAP/Tools/Inference.ts`, `hooks/lib/identity.ts` |

### 3. AlgorithmTracker.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | PostToolUse (Bash, TaskCreate, TaskUpdate, Task) |
| **Purpose** | Tracks Algorithm phase progression and ISC criteria state |
| **What it does** | Detects phase transitions, criteria creation/updates, agent spawns |
| **Why essential** | Provides real-time visibility into what the Algorithm is doing |
| **Dependencies** | `hooks/lib/algorithm-state.ts` |

### 4. SecurityValidator.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | PreToolUse (Bash, Edit, Write, Read) |
| **Purpose** | Validates commands against security patterns before execution |
| **What it does** | Checks for destructive operations, secret exposure, dangerous commands |
| **Why essential** | Prevents accidental `rm -rf`, credential leaks, and unsafe operations |
| **Dependencies** | `hooks/lib/paths.ts`, security patterns config |

### 5. IntegrityCheck.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | SessionEnd |
| **Purpose** | Detects SNAP system file changes and validates document cross-references |
| **What it does** | Parses transcript for changed files, spawns maintenance if needed |
| **Why essential** | Catches drift — when edits break consistency across system files |
| **Dependencies** | `skills/SNAP/Tools/TranscriptParser.ts`, `hooks/handlers/SystemIntegrity.ts`, `hooks/handlers/DocCrossRefIntegrity.ts` |

### 6. SkillGuard.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | PreToolUse (Skill) |
| **Purpose** | Blocks false-positive skill invocations |
| **What it does** | Prevents the model from invoking wrong skills due to position bias in the skill list |
| **Why essential** | Stops the AI from running keybindings-help when you asked about something else |
| **Dependencies** | None (standalone) |

### 7. AgentExecutionGuard.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | PreToolUse (Task) |
| **Purpose** | Enforces background execution for agent spawning |
| **What it does** | Warns when agents are spawned in foreground instead of background |
| **Why essential** | Prevents blocking — agents should run in parallel, not sequentially |
| **Dependencies** | None (standalone) |

### 8. StopOrchestrator.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | Stop (after Claude generates a response) |
| **Purpose** | Orchestrates all post-response handlers |
| **What it does** | Parses transcript ONCE, distributes to voice, capture, tab state, and integrity handlers |
| **Why essential** | Single entry point prevents redundant transcript parsing |
| **Dependencies** | `hooks/handlers/VoiceNotification.ts`, `hooks/handlers/ResponseCapture.ts`, `hooks/handlers/TabState.ts`, `hooks/handlers/SystemIntegrity.ts` |

### 9. CheckVersion.hook.ts
| Field | Value |
|-------|-------|
| **Trigger** | SessionStart |
| **Purpose** | Checks for Claude Code CLI updates |
| **What it does** | Compares installed version against npm latest, displays update notice |
| **Why essential** | Keeps your CLI current without manual checking |
| **Dependencies** | None (standalone) |

---

## Shared Library Dependencies

These `hooks/lib/` files are required by the core hooks above:

| Library File | Used By | Purpose |
|-------------|---------|---------|
| `lib/identity.ts` | FormatReminder | Reads DA name from settings.json |
| `lib/paths.ts` | SecurityValidator | Resolves SNAP directory paths |
| `lib/algorithm-state.ts` | AlgorithmTracker | State read/write, phase transitions, criteria tracking |
| `lib/time.ts` | Multiple | Timestamp formatting utilities |
| `lib/observability.ts` | Multiple | Logging and trace emission |
| `lib/notifications.ts` | StopOrchestrator | Notification routing |

### Handler Files (hooks/handlers/)

| Handler | Used By | Purpose |
|---------|---------|---------|
| `handlers/SystemIntegrity.ts` | IntegrityCheck, StopOrchestrator | Detects SNAP file changes |
| `handlers/DocCrossRefIntegrity.ts` | IntegrityCheck | Validates cross-references |
| `handlers/ResponseCapture.ts` | StopOrchestrator | Captures response metadata |
| `handlers/TabState.ts` | StopOrchestrator | Terminal tab title management |
| `handlers/VoiceNotification.ts` | StopOrchestrator | Voice announcement routing |

---

## Installation During Build Session (Hour 4)

### Step 1: Copy Hook Files
```bash
# Copy the 9 core hooks
cp LoadContext.hook.ts FormatReminder.hook.ts AlgorithmTracker.hook.ts \
   SecurityValidator.hook.ts IntegrityCheck.hook.ts SkillGuard.hook.ts \
   AgentExecutionGuard.hook.ts StopOrchestrator.hook.ts CheckVersion.hook.ts \
   ~/.claude/hooks/

# Copy required lib files
cp -r lib/{identity,paths,algorithm-state,time,observability,notifications}.ts \
   ~/.claude/hooks/lib/

# Copy required handlers
cp -r handlers/{SystemIntegrity,DocCrossRefIntegrity,ResponseCapture,TabState,VoiceNotification}.ts \
   ~/.claude/hooks/handlers/
```

### Step 2: Register in settings.json
The hooks section of settings.json maps events to hook files. Your consultant configures this during the session.

### Step 3: Verify
Start a new Claude Code session. You should see:
- Context loaded (LoadContext fired)
- Version check (CheckVersion fired)
- Algorithm depth classification on first prompt (FormatReminder fired)

---

## Customization After Session

### Adding a Custom Hook (Hour 4 Bonus)
During the session, your consultant builds ONE custom hook for your #1 workflow. This becomes your template for creating more.

### Nice-to-Have Hooks (Future)
These are available but not installed in the core package:
- **StartupGreeting** — ASCII banner and greeting at session start
- **SessionAutoName** — Auto-names sessions based on first prompt
- **SessionSummary** — Generates summary on session exit
- **RatingCapture** — Captures your satisfaction ratings
- **AutoWorkCreation** — Auto-creates work entries for new tasks

---

## Troubleshooting

**Hook not firing:**
1. Check `settings.json` hooks section — is the event and matcher correct?
2. Verify the file path is correct and the file exists
3. Restart Claude Code (hooks load at startup)

**Hook error in output:**
1. Check stderr output for error messages
2. Verify dependencies exist (lib files, handler files)
3. Run the hook manually: `bun hooks/HookName.hook.ts`

**Performance issues:**
- Hooks run in milliseconds (3-50ms each)
- If a session feels slow, check if a hook is doing network calls
- SecurityValidator is the heaviest — still under 50ms
