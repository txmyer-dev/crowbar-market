# Fabric — User Preferences

## Auto-Save extract_wisdom to SecondBrain (MANDATORY)

When running the `extract_wisdom` pattern (via `/extract-wisdom` or any Fabric extract_wisdom invocation), **automatically save the output** to `C:\Users\txmye_ficivtv\My Drive\SecondBrain\Knowledge\` after displaying it. This applies ONLY to extract_wisdom, not other Fabric patterns.

### Save Rules

Follow the same conventions as the ExtractWisdom skill customization:

1. **Filename:** `{Speaker}-{Short-Topic}.md` in Title-Case-With-Hyphens. No dates in filename. No pattern name in filename.
2. **Frontmatter:** type `wisdom-extraction`, appropriate domain, 2-6 kebab-case tags, source URL, status `active`.
3. **Related section:** End with `## Related` containing `[[wiki-links]]` to related existing files in `C:\Users\txmye_ficivtv\My Drive\SecondBrain\Knowledge\`.
4. **Deduplication:** Check if file exists first. Warn if duplicate.
5. **No permission needed:** Save automatically, then confirm filename to user.

### Show Abbreviations for Episode Naming

MW (Modern Wisdom), DOAC (Diary of a CEO), JRE (Joe Rogan Experience), HL (Huberman Lab), IF (Impact Theory), LI (Lex Fridman)
