#!/usr/bin/env python3
"""Generate Claude Code slash commands from Fabric patterns.

Scans ~/.claude/skills/Fabric/Patterns/ and creates a .md file in
~/.claude/commands/ for each pattern. Claude Code turns each .md file
into a /command-name slash command.

Usage:
    python3 ~/.claude/skills/Fabric/Tools/GenerateCommands.py
"""

import os
from pathlib import Path

PATTERNS_DIR = Path.home() / ".claude" / "skills" / "Fabric" / "Patterns"
COMMANDS_DIR = Path.home() / ".claude" / "commands"
USER_MD_LINE_THRESHOLD = 10

# Patterns to skip — custom SNAP skills handle these domains better
BLOCKLIST = {
    "extract_wisdom",
    "extract_wisdom_agents",
    "extract_wisdom_dm",
    "extract_wisdom_nometa",
    "extract_wisdom_with_attribution",
    "create_aphorisms",
    "create_threat_model",
}


def pattern_to_command_name(pattern: str) -> str:
    """Convert pattern directory name to slash command name (underscores to hyphens)."""
    return pattern.replace("_", "-")


def has_substantial_user_md(pattern_dir: Path) -> bool:
    """Check if pattern has a user.md with more than threshold lines."""
    user_md = pattern_dir / "user.md"
    if not user_md.exists():
        return False
    try:
        line_count = sum(1 for _ in user_md.open())
        return line_count > USER_MD_LINE_THRESHOLD
    except OSError:
        return False


def generate_standard_template(pattern_name: str) -> str:
    """Generate standard command template (system.md only)."""
    return f"""Apply the Fabric `{pattern_name}` pattern to the provided content.

Read the pattern instructions at: ~/.claude/skills/Fabric/Patterns/{pattern_name}/system.md

Apply those instructions to the following input:

$ARGUMENTS
"""


def generate_extended_template(pattern_name: str) -> str:
    """Generate extended command template (system.md + user.md)."""
    return f"""Apply the Fabric `{pattern_name}` pattern to the provided content.

Read the pattern instructions at: ~/.claude/skills/Fabric/Patterns/{pattern_name}/system.md
Also read the user context at: ~/.claude/skills/Fabric/Patterns/{pattern_name}/user.md

Apply both the system instructions and user context to the following input:

$ARGUMENTS
"""


def generate_master_command(patterns: list[str]) -> str:
    """Generate the master /patterns command file."""
    pattern_list = "\n".join(f"- `/{pattern_to_command_name(p)}`" for p in sorted(patterns))
    return f"""List or search available Fabric patterns.

If $ARGUMENTS is empty, list all {len(patterns)} available patterns grouped by prefix (analyze, create, extract, etc.).

If $ARGUMENTS contains a search term, filter patterns to those matching the term.

Available patterns ({len(patterns)} total):
{pattern_list}
"""


def main():
    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

    # Clean existing pattern command files (but not non-pattern commands)
    pattern_dirs = sorted(
        d.name for d in PATTERNS_DIR.iterdir()
        if d.is_dir() and (d / "system.md").exists() and d.name not in BLOCKLIST
    )
    pattern_command_names = {pattern_to_command_name(p) + ".md" for p in pattern_dirs}
    pattern_command_names.add("patterns.md")

    for existing in COMMANDS_DIR.iterdir():
        if existing.name in pattern_command_names or existing.name.replace(".md", "").replace("-", "_") in {d for d in pattern_dirs}:
            existing.unlink()

    # Generate command files
    generated = 0
    for pattern_name in pattern_dirs:
        pattern_dir = PATTERNS_DIR / pattern_name
        command_name = pattern_to_command_name(pattern_name)
        command_file = COMMANDS_DIR / f"{command_name}.md"

        if has_substantial_user_md(pattern_dir):
            content = generate_extended_template(pattern_name)
        else:
            content = generate_standard_template(pattern_name)

        command_file.write_text(content)
        generated += 1

    # Generate master /patterns command
    master_file = COMMANDS_DIR / "patterns.md"
    master_file.write_text(generate_master_command(pattern_dirs))

    print(f"Generated {generated} pattern commands + 1 master command")
    print(f"Total files in {COMMANDS_DIR}: {generated + 1}")
    print(f"Commands directory: {COMMANDS_DIR}")


if __name__ == "__main__":
    main()
