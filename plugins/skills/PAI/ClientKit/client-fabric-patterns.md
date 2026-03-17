# Fabric Pattern Reference Guide

## What Are Fabric Patterns?

Fabric patterns are single-purpose AI workflows. Each pattern does one thing well — extracting wisdom from a transcript, analyzing a sales call, generating a product brief, improving your writing. Think of them as power tools: each shaped for a specific job.

Your SNAP system ships with 259 patterns available as slash commands inside Claude Code.

## How to Use

**In Claude Code** — type the pattern name as a slash command:
```
/extract-wisdom
/summarize-meeting
/analyze-risk
```

**Pipe content in** — paste or pipe any text (article, transcript, meeting notes, code) and the pattern processes it automatically.

**With a file** — reference a file path and the pattern reads it:
```
/analyze-paper path/to/paper.pdf
```

Each pattern outputs clean, structured results. No prompting required.

---

## Role-Based Pattern Curations

The 15-20 patterns below per role are your starting stack. During the Build Session, these get installed and tested against your actual work.

---

### 1. Executive / Business Leader

Strategy, analysis, decision-making, high-stakes communication.

#### Extract
| Pattern | What It Does |
|---------|-------------|
| `extract-wisdom` | Pulls the highest-signal insights, quotes, and lessons from any content |
| `extract-recommendations` | Surfaces actionable recommendations from reports, meetings, or research |
| `extract-predictions` | Identifies forward-looking claims and forecasts in any content |
| `extract-core-message` | Strips to the single most important point in a document or talk |
| `extract-main-idea` | One-paragraph distillation of the central argument |

#### Analyze
| Pattern | What It Does |
|---------|-------------|
| `analyze-risk` | Structures risks, likelihood, and mitigations from any plan or situation |
| `analyze-claims` | Evaluates the validity and evidence behind assertions |
| `analyze-presentation` | Scores a presentation on structure, clarity, and persuasiveness |
| `analyze-sales-call` | Extracts outcomes, objections, and next steps from sales conversation |
| `analyze-mistakes` | Identifies errors in reasoning, process, or execution |
| `find-logical-fallacies` | Flags weak arguments and logical errors in any text |

#### Create
| Pattern | What It Does |
|---------|-------------|
| `create-hormozi-offer` | Structures your product or service as a compelling, value-dense offer |
| `create-keynote` | Builds a presentation outline from raw ideas or source material |
| `create-better-frame` | Reframes a situation, idea, or message for maximum clarity and impact |
| `create-mermaid-visualization` | Turns processes, org structures, or timelines into diagrams |

#### Improve
| Pattern | What It Does |
|---------|-------------|
| `improve-writing` | Elevates prose clarity, structure, and impact without changing voice |
| `solve-with-cot` | Works through complex problems step-by-step using chain-of-thought reasoning |

---

### 2. Marketer / Content Creator

Writing, content strategy, audience analysis, campaign ideation.

#### Extract
| Pattern | What It Does |
|---------|-------------|
| `extract-ideas` | Pulls the best standalone ideas from any source material |
| `extract-insights` | Surfaces non-obvious connections and takeaways |
| `extract-article-wisdom` | Distills the most valuable points from articles and long reads |
| `extract-business-ideas` | Identifies business angles and monetization opportunities in content |
| `extract-questions` | Generates the questions an audience would ask about your content |

#### Analyze
| Pattern | What It Does |
|---------|-------------|
| `analyze-comments` | Synthesizes audience sentiment, themes, and reactions from comment sections |
| `analyze-prose` | Evaluates writing quality, tone, and readability |
| `get-wow-per-minute` | Scores content density — how much value per unit of audience attention |
| `rate-content` | Rates content quality on multiple dimensions with reasoning |
| `rate-value` | Assesses how much real value a piece of content delivers |

#### Create
| Pattern | What It Does |
|---------|-------------|
| `create-article-from-idea` | Expands a single idea into a full article draft |
| `create-summary` | Creates a polished, shareable summary of any content |
| `create-5-sentence-summary` | Distills any content to five tight, high-value sentences |
| `create-aphorisms` | Generates quotable, memorable one-liners from your ideas |
| `create-quiz` | Builds an interactive quiz from any topic or content set |

#### Improve
| Pattern | What It Does |
|---------|-------------|
| `improve-writing` | Elevates prose without flattening your voice |
| `create-tags` | Generates optimized tags and categories for content distribution |
| `compare-and-contrast` | Structures clear comparisons between products, ideas, or approaches |
| `label-and-rate` | Categorizes and scores a batch of content items |

---

### 3. Software Developer

Code review, documentation, architecture planning, learning acceleration.

#### Extract
| Pattern | What It Does |
|---------|-------------|
| `extract-insights` | Surfaces architectural and design insights from technical content |
| `extract-recommendations` | Pulls implementation recommendations from docs, papers, or discussions |
| `extract-book-ideas` | Distills the key technical ideas from a programming book or talk |

#### Analyze
| Pattern | What It Does |
|---------|-------------|
| `analyze-paper` | Full academic/technical paper breakdown: contributions, methods, findings |
| `analyze-claims` | Validates technical assertions and evaluates supporting evidence |
| `analyze-risk` | Surfaces risks in a technical design, architecture, or plan |
| `find-logical-fallacies` | Identifies flawed reasoning in technical arguments or proposals |

#### Create
| Pattern | What It Does |
|---------|-------------|
| `create-coding-project` | Scaffolds a complete project from a description: structure, files, approach |
| `create-coding-feature` | Designs and documents a new feature addition to an existing codebase |
| `create-design-document` | Produces a technical design doc from requirements or whiteboard notes |
| `create-prd` | Generates a Product Requirements Document from a feature idea |
| `create-user-story` | Writes properly structured user stories with acceptance criteria |
| `create-mermaid-visualization` | Converts architecture or data flow descriptions into Mermaid diagrams |
| `create-flash-cards` | Builds study cards from documentation, specs, or new concepts |

#### Improve
| Pattern | What It Does |
|---------|-------------|
| `explain-code` | Explains what a block of code does in plain language |
| `explain-docs` | Clarifies dense technical documentation |
| `explain-terms` | Defines technical terms in context |
| `review-code` | Reviews code for quality, correctness, and maintainability |
| `improve-prompt` | Improves an AI prompt for better, more consistent outputs |

---

### 4. Consultant / Coach

Client deliverables, frameworks, diagnostic analysis, presentations.

#### Extract
| Pattern | What It Does |
|---------|-------------|
| `extract-wisdom` | Pulls the highest-signal lessons and insights from any source |
| `extract-recommendations` | Surfaces prioritized recommendations from research or assessment |
| `extract-predictions` | Identifies forward-looking claims in industry content or client data |
| `extract-core-message` | Finds the single most important point in a document or conversation |

#### Analyze
| Pattern | What It Does |
|---------|-------------|
| `analyze-sales-call` | Extracts outcomes, objections, and follow-ups from a client call |
| `analyze-presentation` | Evaluates deck structure, clarity, and persuasiveness |
| `analyze-personality` | Patterns communication and decision-making style from text or speech |
| `analyze-mistakes` | Identifies what went wrong in a project, engagement, or decision |
| `analyze-risk` | Structures risks and mitigations in any plan or client situation |
| `check-agreement` | Checks whether two parties or documents are actually aligned |

#### Create
| Pattern | What It Does |
|---------|-------------|
| `create-keynote` | Builds a presentation outline from raw notes or source material |
| `create-hormozi-offer` | Structures any service or engagement as a high-value offer |
| `create-better-frame` | Reframes a problem or situation for maximum client clarity |
| `create-reading-plan` | Builds a structured learning plan around a topic or skill gap |
| `create-mermaid-visualization` | Turns frameworks, processes, and models into diagrams |

#### Improve
| Pattern | What It Does |
|---------|-------------|
| `improve-writing` | Polishes client-facing documents and reports |
| `provide-guidance` | Generates structured, actionable guidance on any question or situation |
| `dialog-with-socrates` | Subjects an idea to rigorous Socratic questioning to stress-test it |
| `compare-and-contrast` | Builds clear comparisons between options, approaches, or frameworks |

---

### 5. Researcher / Academic

Paper analysis, claim verification, writing improvement, knowledge extraction.

#### Extract
| Pattern | What It Does |
|---------|-------------|
| `extract-wisdom` | Extracts the highest-value insights and lessons from any source |
| `extract-ideas` | Pulls standalone ideas worth developing further |
| `extract-insights` | Surfaces non-obvious connections across a body of content |
| `extract-predictions` | Identifies empirical claims and forward projections |
| `extract-questions` | Generates the open questions a piece of work raises |
| `capture-thinkers-work` | Structures the core frameworks and contributions of a thinker |

#### Analyze
| Pattern | What It Does |
|---------|-------------|
| `analyze-paper` | Full paper breakdown: problem, method, results, limitations, contributions |
| `analyze-claims` | Evaluates the validity and evidence quality of assertions |
| `summarize-paper` | Concise, structured summary of an academic paper |
| `find-logical-fallacies` | Identifies flawed reasoning in arguments or literature |
| `compare-and-contrast` | Structures comparisons between methodologies, findings, or frameworks |

#### Create
| Pattern | What It Does |
|---------|-------------|
| `create-reading-plan` | Builds a systematic reading plan for a research area |
| `create-flash-cards` | Converts dense material into study and review cards |
| `create-mermaid-visualization` | Diagrams research models, study designs, or conceptual frameworks |
| `summarize-micro` | Ultra-compact summary for literature review or quick reference |
| `create-5-sentence-summary` | Five-sentence distillation for abstracts or executive summaries |

#### Improve
| Pattern | What It Does |
|---------|-------------|
| `improve-writing` | Elevates prose quality while preserving technical precision |
| `improve-academic-writing` | Tightens academic writing: structure, hedging, citation clarity |
| `write-essay` | Constructs a well-structured essay from a thesis or prompt |
| `write-micro-essay` | Produces a tight, high-density short-form essay on any topic |

---

## Quick Reference

All patterns follow the same syntax:

```
/pattern-name
```

Paste your content after invoking the pattern, or reference a file path. Results are always structured, clean, and ready to use or export.

Your installed patterns are in: `~/.claude/skills/`
