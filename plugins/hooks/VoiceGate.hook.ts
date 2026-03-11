#!/usr/bin/env bun
/**
 * VoiceGate.hook.ts - Block ALL Voice Curls from Claude Sessions (PreToolUse)
 *
 * PURPOSE:
 * Blocks ALL voice notifications from Claude Code sessions.
 * Voice is reserved exclusively for the heartbeat daily briefing,
 * which runs outside Claude Code via Task Scheduler → run-heartbeat.sh.
 *
 * TRIGGER: PreToolUse (matcher: Bash)
 *
 * DECISION LOGIC:
 * 1. Command doesn't contain "localhost:8888" → PASS (not a voice curl)
 * 2. Command contains "localhost:8888" → BLOCK (all Claude session voice curls)
 *
 * PERFORMANCE: <5ms. Fast-path exit for non-voice commands.
 */

interface HookInput {
  tool_name: string;
  tool_input: {
    command?: string;
  };
  session_id: string;
}

async function main() {
  let input: HookInput;
  try {
    const reader = Bun.stdin.stream().getReader();
    let raw = '';
    const read = (async () => {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        raw += new TextDecoder().decode(value, { stream: true });
      }
    })();
    await Promise.race([read, new Promise<void>(r => setTimeout(r, 200))]);
    if (!raw.trim()) {
      console.log(JSON.stringify({ continue: true }));
      return;
    }
    input = JSON.parse(raw);
  } catch {
    console.log(JSON.stringify({ continue: true }));
    return;
  }

  const command = input.tool_input?.command || '';

  // Fast path: not a voice curl → allow immediately
  if (!command.includes('localhost:8888')) {
    console.log(JSON.stringify({ continue: true }));
    return;
  }

  // It's a voice curl — block ALL from Claude sessions
  // Voice is reserved for heartbeat only (runs outside Claude via Task Scheduler)
  console.log(JSON.stringify({
    decision: "block",
    reason: "Voice curls blocked. Voice is heartbeat-only (runs via Task Scheduler, not Claude sessions)."
  }));
}

main().catch(() => {
  console.log(JSON.stringify({ continue: true }));
});
