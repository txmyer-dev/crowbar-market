# Chat Workflow

Ask questions and chat with notebook sources. NotebookLM answers based on the ingested content.

Running the **Chat** workflow in the **NotebookLM** skill to query sources...

## Pre-check

Ensure a notebook is active with sources loaded.

```bash
notebooklm source list
```

If no sources, redirect to CreateNotebook workflow first.

## Execute Query

### Single Question

```bash
notebooklm ask "<question>"
```

The response comes directly from NotebookLM's analysis of the notebook sources.

### Multi-Turn Conversation

For follow-up questions, just run `notebooklm ask` again — NotebookLM maintains conversation context within a session.

## Common Query Patterns

| User Intent | Example Query |
|-------------|--------------|
| Summarize | "Summarize the key points across all sources" |
| Compare | "Compare the approaches described in source 1 vs source 2" |
| Extract | "What are the main recommendations?" |
| Analyze | "What are the common themes across these sources?" |
| Specific lookup | "What does the author say about X?" |
| Synthesize | "Based on all sources, what's the best approach to Y?" |

## Report to User

- The answer from NotebookLM
- Suggest follow-up questions if appropriate
- Suggest generating a deliverable if the Q&A reveals interesting patterns
