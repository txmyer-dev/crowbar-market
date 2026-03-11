# Research Workflow

Use NotebookLM's research agents to search the web or Google Drive, then optionally import findings as notebook sources.

Running the **Research** workflow in the **NotebookLM** skill to run research agent...

## Pre-check

Ensure a notebook is active. If not, create one first via CreateNotebook workflow.

## Intent-to-Command Mapping

### Research Mode Selection

| User Says | Command |
|-----------|---------|
| "web research", "search the web", "find info on" | `notebooklm research web "<query>"` |
| "drive research", "search my drive", "find in drive" | `notebooklm research drive "<query>"` |

### Depth Selection

| User Says | Flag |
|-----------|------|
| "quick", "fast", "brief" | `--fast` |
| "deep", "thorough", "comprehensive" (default) | `--deep` |

### Auto-Import

| User Says | Flag |
|-----------|------|
| "import findings", "add to notebook" (default: yes) | `--auto-import` |
| "just search, don't import" | (omit `--auto-import`) |

## Execute Research

```bash
notebooklm research web "<query>" --deep --auto-import
```

Or for Drive:
```bash
notebooklm research drive "<query>" --deep --auto-import
```

## Post-Research Options

After research completes, suggest:
1. **Ask questions** about the findings via Chat workflow
2. **Generate a deliverable** (briefing report, audio overview) via Generate workflow
3. **Add more sources** to deepen the research
4. **Download the report** if one was generated

## Report to User

- Number of sources found/imported
- Key findings summary (from the research agent output)
- Suggested next steps
