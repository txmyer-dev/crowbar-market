---
name: NotebookLM
description: Google NotebookLM integration via notebooklm-py CLI. USE WHEN NotebookLM, notebook, podcast, audio overview, research notebook, generate infographic, generate quiz, generate flashcards, generate slide deck, generate mind map, generate report, NotebookLM analysis. Manages notebooks, sources, content generation, research agents, and chat.
---

## Customization

**Before executing, check for user customizations at:**
`~/.claude/skills/SNAP/USER/SKILLCUSTOMIZATIONS/NotebookLM/`

If this directory exists, load and apply any PREFERENCES.md, configurations, or resources found there. These override default behavior. If the directory does not exist, proceed with skill defaults.

# NotebookLM

Programmatic access to Google NotebookLM — create notebooks, add sources (URLs, YouTube, PDFs, Drive), generate deliverables (audio, video, quiz, flashcards, slides, infographics, mind maps, reports), run research agents, and chat with sources. All via the `notebooklm` CLI.

**Prerequisite:** Must be authenticated. If any command fails with auth error, run `notebooklm login` first.

## Workflow Routing

| Workflow | Trigger | File |
|----------|---------|------|
| **Setup** | "setup notebooklm", "login notebooklm", "authenticate" | `Workflows/Setup.md` |
| **CreateNotebook** | "create notebook", "new notebook", "add sources" | `Workflows/CreateNotebook.md` |
| **Generate** | "generate audio", "generate podcast", "generate video", "generate quiz", "generate flashcards", "generate slides", "generate infographic", "generate mind map", "generate report", "create deliverable" | `Workflows/Generate.md` |
| **Research** | "research with notebooklm", "web research", "drive research" | `Workflows/Research.md` |
| **Chat** | "ask notebooklm", "chat with notebook", "query sources" | `Workflows/Chat.md` |

## Quick Reference

- **CLI prefix:** `notebooklm`
- **Auth:** `notebooklm login` (browser OAuth, one-time)
- **Source types:** URL, YouTube, PDF, text, markdown, Word, audio, video, images, Google Drive
- **Deliverables:** Audio (4 formats, 3 lengths, 50+ langs), Video (9 styles), Quiz, Flashcards, Slides, Infographic, Mind Map, Data Table, Report
- **Generation is async:** Use `--wait` flag or poll for completion

**Full CLI & API reference:** Load `ApiReference.md` on demand.

## Examples

**Example 1: Create a research notebook from YouTube videos**
```
User: "Create a NotebookLM notebook from these 3 YouTube videos and generate an audio overview"
-> Invokes CreateNotebook to create + add sources
-> Invokes Generate to create audio deliverable
-> Downloads MP3 and reports path
```

**Example 2: Generate a slide deck from existing notebook**
```
User: "Generate a slide deck from my research notebook"
-> Invokes Generate workflow
-> Runs: notebooklm generate slide-deck --wait
-> Downloads PDF/PPTX
```

**Example 3: Research a topic and get a briefing**
```
User: "Use NotebookLM to research quantum computing and give me a briefing"
-> Invokes Research workflow with web search
-> Invokes Generate workflow for report (briefing template)
-> Downloads markdown report
```
