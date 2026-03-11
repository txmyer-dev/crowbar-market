# Generate Workflow

Generate deliverables from NotebookLM sources. This is the primary value workflow — it offloads heavy analysis to Google's infrastructure (free tokens).

Running the **Generate** workflow in the **NotebookLM** skill to generate deliverable...

## Pre-check

Ensure a notebook is active:
```bash
notebooklm list
```

If no active notebook, ask the user which to use or create one via CreateNotebook workflow.

## Intent-to-Command Mapping

### Deliverable Type Selection

| User Says | Command | Typical Wait |
|-----------|---------|-------------|
| "podcast", "audio", "audio overview" | `notebooklm generate audio` | 2-5 min |
| "video", "video overview" | `notebooklm generate video` | 5-10 min |
| "quiz", "questions" | `notebooklm generate quiz` | 1-2 min |
| "flashcards", "study cards" | `notebooklm generate flashcards` | 1-2 min |
| "slides", "slide deck", "presentation" | `notebooklm generate slide-deck` | 5-15 min |
| "infographic", "visual summary" | `notebooklm generate infographic` | 3-5 min |
| "mind map", "concept map" | `notebooklm generate mind-map` | 1-2 min |
| "data table", "comparison table" | `notebooklm generate data-table` | 1-2 min |
| "report", "briefing", "study guide", "blog post" | `notebooklm generate report` | 2-5 min |

### Audio Options

| User Says | Flag | Values |
|-----------|------|--------|
| "deep dive", "detailed" | `--format deep-dive` | Default |
| "brief", "quick", "short overview" | `--format brief` | Shorter |
| "critical", "critique" | `--format critique` | Analytical |
| "debate", "two sides" | `--format debate` | Point/counterpoint |
| "short" | `--length short` | ~5 min |
| "medium" (default) | `--length medium` | ~10 min |
| "long", "comprehensive" | `--length long` | ~20 min |
| "in Spanish", "in Japanese", etc. | `--language es`, `--language ja` | 50+ langs |

### Video Options

| User Says | Flag |
|-----------|------|
| "whiteboard style" | `--style whiteboard` |
| "classic" | `--style classic` |
| "kawaii", "cute" | `--style kawaii` |
| "anime" | `--style anime` |

### Quiz / Flashcard Options

| User Says | Flag |
|-----------|------|
| "easy", "beginner" | `--difficulty easy` |
| "medium" (default) | `--difficulty medium` |
| "hard", "advanced" | `--difficulty hard` |
| "fewer", "less" | `--quantity less` |
| "more", "lots" | `--quantity more` |

### Infographic Options

| User Says | Flag |
|-----------|------|
| "portrait", "vertical" | `--orientation portrait` |
| "landscape", "wide" | `--orientation landscape` |
| "square" | `--orientation square` |

### Report Templates

| User Says | Flag |
|-----------|------|
| "briefing", "executive summary" | `--template briefing` |
| "study guide" | `--template study-guide` |
| "blog post", "article" | `--template blog-post` |

## Execute Generation

Always use `--wait` to block until complete:

```bash
notebooklm generate <type> [options] --wait
```

If `--wait` is not supported for a type, generate then poll.

## Download the Deliverable

After generation completes, download immediately:

```bash
notebooklm download <type> [--format <format>] <output_path>
```

### Default Output Paths

Use descriptive filenames based on the notebook name:

| Type | Path Pattern |
|------|-------------|
| Audio | `./notebook-name-overview.mp3` |
| Video | `./notebook-name-overview.mp4` |
| Quiz | `./notebook-name-quiz.md` |
| Flashcards | `./notebook-name-flashcards.json` |
| Slides | `./notebook-name-slides.pdf` |
| Infographic | `./notebook-name-infographic.png` |
| Mind Map | `./notebook-name-mindmap.json` |
| Data Table | `./notebook-name-data.csv` |
| Report | `./notebook-name-report.md` |

## Report to User

- Deliverable type and format
- File path where it was saved
- Generation time
- Suggest opening/viewing the file
