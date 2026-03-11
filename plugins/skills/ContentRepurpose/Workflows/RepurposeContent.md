# RepurposeContent Workflow

## Input

Source content: transcript, article, video notes, podcast notes, or any long-form text.

If the user provides a URL, use Parser skill to extract the content first.
If the user provides a YouTube URL, use ExtractWisdom or Parser to get the transcript first.

## Output Formats

Generate **all three formats in parallel** using the Agent tool (spawn 3 subagents simultaneously). If the user only wants specific formats, generate only those.

### 1. Tweet Thread (5-10 tweets)

**Constraints:**
- Each tweet: 240 characters max (leave room for threading)
- Thread length: 5-10 tweets
- First tweet: hook that makes you stop scrolling
- Last tweet: call to action or provocative closer
- No hashtags unless user specifically requests them
- No "Thread:" or "1/" prefixes — just the content

**Tone:** Conversational, punchy. Short sentences. Opinions welcome. Write like someone with 50K followers who doesn't try too hard.

**Template:**
```
[Hook tweet — the most surprising or contrarian take from the source]

[Supporting insight with specific detail]

[Contrarian angle or "most people think X, but actually Y"]

[Story or example that illustrates the point]

[Practical takeaway — what the reader can do with this]

[Closer — provocative question, bold statement, or callback to hook]
```

### 2. LinkedIn Post (150-300 words)

**Constraints:**
- 150-300 words (hard limit — count them)
- First line: hook (this is what shows above "see more")
- Short paragraphs (1-3 sentences max)
- Line breaks between paragraphs (LinkedIn renders these)
- No markdown formatting (LinkedIn doesn't render it)
- End with a question to drive comments

**Tone:** Professional but human. First person. Tell a micro-story or share an insight. Not corporate jargon. Not motivational poster. The "smart friend who works in your industry" voice.

**Template:**
```
[Hook line — surprising stat, contrarian take, or personal observation]

[Context — 2-3 sentences setting up the insight]

[The insight itself — what you learned or realized]

[Why it matters — practical implication]

[Specific example or detail that proves the point]

[Question for the reader — drives engagement]
```

### 3. Newsletter Draft (500-800 words)

**Constraints:**
- 500-800 words (hard limit)
- Subject line suggestion included
- Clear sections with headers
- One core idea, developed thoroughly
- Includes at least one specific example or story
- Ends with actionable takeaway

**Tone:** Narrative. Like a smart email from someone you respect. Not a blog post — a letter. Conversational but substantial. The reader should feel like they learned something worth sharing.

**Template:**
```
Subject: [Curiosity-driven subject line, 6-10 words]

[Opening hook — story, observation, or surprising fact. 2-3 sentences.]

## [Core Insight Header]

[Development of the main idea. 2-3 paragraphs. Include specific details, examples, numbers.]

## [Practical Application Header]

[What the reader can do with this. Concrete, actionable. Not vague advice.]

## [Closer]

[Tie back to the opening. End with something that sticks.]
```

## Execution

1. **Read the full source content** — don't start generating until you understand the whole piece
2. **Identify the 3-5 strongest insights** — these will anchor all three formats
3. **Spawn 3 parallel agents** — one per format. Each agent gets:
   - The source content (or a summary if very long)
   - The format-specific template and constraints above
   - The 3-5 key insights to build around
4. **Collect results** — present all three formats with clear headers
5. **Word count verification** — confirm each output meets its constraints

## Output Format

```markdown
# REPURPOSED CONTENT

Source: {title or description of source}

---

## Tweet Thread ({N} tweets)

{tweet 1}

{tweet 2}

...

---

## LinkedIn Post ({word count} words)

{post content}

---

## Newsletter Draft ({word count} words)

**Subject line:** {subject}

{newsletter content}
```

## Quality Check

Before delivering:
- [ ] Tweet thread: 5-10 tweets, each under 240 chars, first tweet is a hook
- [ ] LinkedIn post: 150-300 words, first line hooks, ends with question
- [ ] Newsletter: 500-800 words, has subject line, includes specific examples
- [ ] All three formats build on the same core insights but feel different
- [ ] None of them sound like AI slop — they sound like a real person wrote them
- [ ] Specific details from the source are preserved (names, numbers, examples)
