# SyncPatterns Workflow

Sync Fabric patterns from the upstream danielmiessler/fabric repository using git sparse-checkout. No Fabric CLI required.

---

## Workflow Steps

### Step 1: Send Voice Notification

```bash
curl -s -X POST http://localhost:8888/notify \
  -H "Content-Type: application/json" \
  -d '{"message": "Syncing Fabric patterns from upstream repository"}' \
  > /dev/null 2>&1 &
```

### Step 2: Check Current Pattern Count

```bash
CURRENT_COUNT=$(ls -1 ~/.claude/skills/Fabric/Patterns/ 2>/dev/null | wc -l | tr -d ' ')
echo "Current patterns: $CURRENT_COUNT"
```

### Step 3: Git Sparse-Checkout of Patterns

Clone only the `patterns/` directory from upstream (shallow, minimal bandwidth):

```bash
cd /tmp
rm -rf fabric-sync
git clone --depth 1 --filter=blob:none --sparse \
  https://github.com/danielmiessler/fabric.git fabric-sync
cd fabric-sync
git sparse-checkout set patterns
```

### Step 4: Rsync to Both Locations

Sync patterns to the Fabric config directory and the skill directory:

```bash
# Sync to config (canonical source)
rsync -av --delete /tmp/fabric-sync/patterns/ ~/.config/fabric/patterns/

# Sync to skill directory
rsync -av --delete ~/.config/fabric/patterns/ ~/.claude/skills/Fabric/Patterns/
```

### Step 5: Regenerate Slash Commands

Run the command generator to update all slash command files:

```bash
python3 ~/.claude/skills/Fabric/Tools/GenerateCommands.py
```

### Step 6: Cleanup

```bash
rm -rf /tmp/fabric-sync
```

### Step 7: Report Results

```bash
NEW_COUNT=$(ls -1 ~/.claude/skills/Fabric/Patterns/ 2>/dev/null | wc -l | tr -d ' ')
COMMAND_COUNT=$(ls -1 ~/.claude/commands/*.md 2>/dev/null | wc -l | tr -d ' ')
echo ""
echo "Pattern sync complete!"
echo "Previous count: $CURRENT_COUNT"
echo "New count: $NEW_COUNT"
echo "Slash commands: $COMMAND_COUNT"
if [ "$NEW_COUNT" -gt "$CURRENT_COUNT" ]; then
  ADDED=$((NEW_COUNT - CURRENT_COUNT))
  echo "Added: $ADDED new patterns"
elif [ "$NEW_COUNT" -lt "$CURRENT_COUNT" ]; then
  REMOVED=$((CURRENT_COUNT - NEW_COUNT))
  echo "Removed: $REMOVED deprecated patterns"
fi
```

### Step 8: Verify Key Patterns Exist

Confirm critical patterns are present:

```bash
for pattern in extract_wisdom summarize create_threat_model analyze_claims; do
  if [ -d ~/.claude/skills/Fabric/Patterns/$pattern ]; then
    echo "✓ $pattern"
  else
    echo "✗ $pattern MISSING"
  fi
done
```

---

## Verification

After sync, verify with:

```bash
# Count patterns
ls -1 ~/.claude/skills/Fabric/Patterns/ | wc -l

# Count slash commands
ls -1 ~/.claude/commands/*.md | wc -l

# Spot-check a command
cat ~/.claude/commands/extract-wisdom.md
```

---

## Output

Report to user:
- Previous pattern count
- New pattern count
- Number of slash commands generated
- Number of patterns added/removed (if any)
- Confirmation that sync completed successfully
