# AI Steering Rules - Personal

These extend `SNAP/SYSTEM/AISTEERINGRULES.md`. Both files are loaded and enforced together.

## Rules

1. **SecondBrain Connective Tissue** — Every file written to `Knowledge/` or `Sessions/` must have YAML frontmatter (title, type, domain, tags, date, source, status) and a `## Related` section with wiki-links. Use obsidian MCP tools to discover related files before writing. Never write bare markdown.

2. **Frontmatter Schema** — `type`: bootcamp | wisdom-extraction | philosophy | business | strategy | session-log | note. `domain`: learning | business | personal | technical | consulting. `status`: active | archive | draft.

3. **Self-Update Protocol** — "Update yourself" or `/update` invokes the Update skill. See `skills/Update/SKILL.md`.

4. **Review Via Role Separation** — When reviewing own output, reframe as "a developer proposed this — what's wrong?" to bypass sycophantic self-review bias.

5. **Prefer Editing Over Rewriting** — Claude's RL training biases toward writing new functions. Resist this. When modifying existing code, edit the existing function — don't create a new wrapper alongside it.

6. **Never Use /compact** — Lossy-compresses context, loses ISC nuance. Instead: document state, `/rewind` to ~40%, continue with progress summary. Or double-escape and `/resume` into fresh tab.

7. **Verify Solution Context** — Before applying any researched solution, confirm it targets the EXACT version/config of the system. Wrong-version solutions are worse than no solution.

8. **Research Before Building** — Before building anything new, spend 60 seconds checking: Does this exist as a managed service? A Coolify one-click app? A mature OSS tool? Reference existing stack (Obsidian, Coolify, Hostinger, n8n).

9. **No Fixes Without Root Cause** — Never change code to "try something." Understand WHY first. If 3+ attempts fail on same issue, stop — it's architectural.
