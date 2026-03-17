# Changelog — 2026-03-17

## `cb pull-vps` — VPS-to-Repo Skill Sync

### What Changed

Added a new CLI command `cb pull-vps` to the Crowbar Market CLI.

**Files modified:**
- `cli/src/commands/pull-vps.ts` — new command (created)
- `cli/src/index.ts` — registered command + added to help text + documented `VPS_HOST` env var

Binary rebuilt: `cb.exe`

---

### Why It Was Needed

The skill sync system had an incomplete triangle:

```
Local ~/.claude/skills/  ←──cb install──────  crowbar-market repo
         │                                            ↑
         └──cb publish──────────────────────────────►│
                                                      │
VPS /root/.claude/skills/ ──── (MISSING) ────────────┘
```

Paperclip agents running headless on the VPS can create or modify skills in
`/root/.claude/skills/`. Before this change, there was no path to get those
changes back into the crowbar-market repo or local `~/.claude/skills/`. They
would silently diverge and eventually be overwritten on the next `cb install`.

`cb pull-vps` closes that gap. Now the full triangle is:

```
Local ~/.claude/skills/  ←──cb install──────  crowbar-market repo
         │                                            ↑
         └──cb publish──────────────────────────────►│
                                                      │
VPS /root/.claude/skills/ ──── cb pull-vps ──────────┘
```

---

### How It Works

**Transfer method:** SSH + tar pipe. No temp files, no SCP dependency.

```
ssh host "tar czf - -C /root/.claude/skills SKILL_NAME" | tar xzf - -C plugins/skills/
```

This preserves directory structure, handles binary files correctly, and requires
only standard SSH key auth.

**Command signature:**
```
cb pull-vps <skill-name|--all> [--host <user@host>] [--no-push] [--no-seed] [--dry-run]
```

**Default host:** `root@76.13.98.215` — overridable via `--host` flag or `VPS_HOST` env var.

**Control flow:**
1. Parse args, resolve host
2. SSH probe (`ssh host "echo ok"`) — fast fail if unreachable
3. Build skill list (`--all` lists VPS dir and filters private dirs; named skill verifies it exists)
4. For each skill: stream tar from VPS → extract into `plugins/skills/`
5. Re-seed `registry.json` via `bun scripts/seed-registry.ts` (skippable with `--no-seed`)
6. Git add/commit/push (skippable with `--no-push`)

**Error handling:**
- SSH unreachable → hard exit with diagnostic
- Skill not on VPS → hard exit with clear path message
- Seed failure → warning only (files are safe on disk, manual recovery shown)
- Git push failure → shows manual recovery command

**Private dir filtering:** Same `PRIVATE_DIRS` set as `publish.ts` — `USER`, `.git`,
`__pycache__`, `node_modules` — so `--all` never pulls sensitive directories.

**Commit messages:**
```
pull-vps: sync 12 skills from root@76.13.98.215
pull-vps: update BusinessXRay from root@76.13.98.215
```

---

### Usage Examples

```bash
# Check what would be pulled without touching anything
cb pull-vps --all --dry-run

# Pull a single skill, skip the git push
cb pull-vps BusinessXRay --no-push

# Pull all skills from default host, reseed, commit, push
cb pull-vps --all

# Pull from a different host
cb pull-vps --all --host deploy@staging.example.com

# Set host via env var
VPS_HOST=root@1.2.3.4 cb pull-vps --all
```

---

### Future Work

After `cb pull-vps --all`, a full site rebuild is not automatic. Full flow:
```bash
cb pull-vps --all          # sync VPS → repo
bun run build-site         # regenerate site/index.html
# on VPS: docker compose up -d --build
```

Site rebuild automation (e.g., a `--rebuild-site` flag or post-push hook) is
a candidate for a follow-up.
