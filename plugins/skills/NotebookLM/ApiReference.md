# NotebookLM CLI & API Reference

Full reference for the `notebooklm` CLI (v0.3.3). Uses undocumented Google APIs — rate limits apply.

## Authentication

```bash
notebooklm login          # Opens browser for Google OAuth
```

Credentials stored locally in encrypted storage. One-time setup.

## Notebook Management

```bash
notebooklm create "<name>"              # Create new notebook
notebooklm list                         # List all notebooks
notebooklm use <notebook_id>            # Set active notebook
notebooklm rename "<new_name>"          # Rename active notebook
notebooklm delete                       # Delete active notebook
notebooklm share --link <public|private>                    # Share link
notebooklm permissions add <email> <viewer|editor>          # Add collaborator
```

## Source Management

```bash
notebooklm source add "<url>"           # Add URL source
notebooklm source add "./file.pdf"      # Add local file (PDF, Word, MD, audio, video, image)
notebooklm source list                  # List all sources
notebooklm source refresh               # Refresh sources
notebooklm source delete <source_id>    # Remove a source
```

**Supported source types:** URL, YouTube, PDF, text, Markdown, Word, audio, video, images, Google Drive, pasted text.

## Content Generation

All generation commands support `--wait` to block until complete.

### Audio Overview
```bash
notebooklm generate audio "<instructions>" --wait
```
| Option | Values |
|--------|--------|
| Format | `deep-dive`, `brief`, `critique`, `debate` |
| Length | `short`, `medium`, `long` |
| Language | 50+ languages (e.g., `en`, `es`, `ja`) |

### Video Overview
```bash
notebooklm generate video --style <style> --wait
```
| Option | Values |
|--------|--------|
| Format | `standard`, `dynamic` |
| Style | `classic`, `whiteboard`, `kawaii`, `anime` + 5 more |

### Quiz
```bash
notebooklm generate quiz --difficulty <easy|medium|hard> --quantity <less|normal|more>
```

### Flashcards
```bash
notebooklm generate flashcards --quantity <less|normal|more> --difficulty <easy|medium|hard>
```

### Slide Deck
```bash
notebooklm generate slide-deck
```
Format: `detailed` or `presenter`

### Infographic
```bash
notebooklm generate infographic --orientation <portrait|landscape|square>
```
Detail: `simple`, `moderate`, `detailed`

### Mind Map
```bash
notebooklm generate mind-map
```

### Data Table
```bash
notebooklm generate data-table "<description>"
```

### Report
```bash
notebooklm generate report --template <briefing|study-guide|blog-post>
```
Optional: `--custom-prompt "<extra instructions>"`

## Downloads

```bash
notebooklm download audio ./podcast.mp3
notebooklm download video ./overview.mp4
notebooklm download quiz --format <json|markdown|html> ./quiz.md
notebooklm download flashcards --format <json|markdown|html> ./cards.json
notebooklm download slide-deck ./slides.pdf          # or .pptx
notebooklm download infographic ./image.png
notebooklm download mind-map ./mindmap.json
notebooklm download data-table ./data.csv
notebooklm download report ./report.md
```

## Chat & Research

```bash
notebooklm ask "<question>"                                    # Query sources
notebooklm research web "<query>" --fast|--deep --auto-import  # Web research agent
notebooklm research drive "<query>" --fast|--deep --auto-import # Drive research agent
```

## Python API (Async)

```python
import asyncio
from notebooklm import NotebookLMClient

async def main():
    async with await NotebookLMClient.from_storage() as client:
        # Create notebook
        nb = await client.notebooks.create("Research")

        # Add sources
        await client.sources.add_url(nb.id, "https://example.com", wait=True)
        await client.sources.add_youtube(nb.id, "https://youtube.com/watch?v=...", wait=True)
        await client.sources.add_file(nb.id, "./doc.pdf", wait=True)

        # Generate audio
        status = await client.artifacts.generate_audio(
            nb.id, instructions="engaging overview",
            format="deep-dive", length="medium", language="en"
        )
        await client.artifacts.wait_for_completion(nb.id, status.task_id)
        await client.artifacts.download_audio(nb.id, "podcast.mp3")

        # Chat
        result = await client.chat.ask(nb.id, "Summarize the key findings")
        print(result.answer)

        # Research
        research = await client.research.web_search(
            nb.id, "quantum computing breakthroughs",
            mode="deep", auto_import=True
        )

asyncio.run(main())
```

## Timing Expectations

| Deliverable | Typical Wait |
|-------------|-------------|
| Text analysis / chat | Seconds |
| Audio overview | 2-5 minutes |
| Video overview | 5-10 minutes |
| Infographic | 3-5 minutes |
| Slide deck | 5-15 minutes |
| Quiz / Flashcards | 1-2 minutes |
| Mind map / Data table | 1-2 minutes |
| Report | 2-5 minutes |
