# CreateNotebook Workflow

Create a new notebook and populate it with sources.

Running the **CreateNotebook** workflow in the **NotebookLM** skill to create notebook...

## Step 1: Create the Notebook

```bash
notebooklm create "<descriptive name>"
```

Note the notebook ID from the output — it becomes the active notebook automatically.

## Step 2: Add Sources

Add sources one at a time. Supported types:

### Intent-to-Command Mapping

| User Provides | Command |
|---------------|---------|
| YouTube URL | `notebooklm source add "https://youtube.com/watch?v=..."` |
| Web URL / article | `notebooklm source add "https://example.com/article"` |
| Local PDF | `notebooklm source add "./path/to/file.pdf"` |
| Local markdown | `notebooklm source add "./path/to/file.md"` |
| Local Word doc | `notebooklm source add "./path/to/file.docx"` |
| Audio file | `notebooklm source add "./path/to/audio.mp3"` |
| Video file | `notebooklm source add "./path/to/video.mp4"` |
| Image file | `notebooklm source add "./path/to/image.png"` |

**Max sources per notebook: 50**

## Step 3: Verify Sources

```bash
notebooklm source list
```

Confirm all sources were added and processed successfully.

## Step 4: Report

Tell the user:
- Notebook name and ID
- Number of sources added
- Any sources that failed to process
- Suggest next steps (generate deliverables, ask questions, research)
