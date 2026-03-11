# Your First Week with SNAP

> You just walked out of your Build Session with a working Personal AI system. Now what? This playbook gives you one focused activity per day for your first week. Each takes 15-30 minutes. By Friday, you'll have built the muscle memory to use your AI naturally.

---

## Day 1 (Monday): Run 3 Skills on Your Own Content

**Goal:** Get comfortable using slash commands on things you actually care about.

**What to do:**
1. Open Claude Code (`claude` in terminal)
2. Find a podcast, article, or video you consumed recently
3. Run these 3 skills on it:
   - `/extract-wisdom` — Paste a transcript or article text. See what your AI extracts.
   - `/summarize` — Get a concise summary of any long content
   - `/create-flash-cards` — Turn key insights into study cards

**What you're learning:** How to feed content into your AI and get structured output. This is the foundation of everything else.

**Success signal:** You extracted wisdom from something real and thought "oh, that's actually useful."

---

## Day 2 (Tuesday): Save Your First Extraction to SecondBrain

**Goal:** Close the loop — content goes IN, knowledge comes OUT, and it lives somewhere permanent.

**What to do:**
1. Take the best extraction from Day 1
2. Ask your AI: "Save this to my SecondBrain vault as a Knowledge note"
3. Verify it was saved with proper frontmatter (title, type, domain, tags, date, source, status)
4. Open Obsidian and find the file — check the graph view to see your first node

**What you're learning:** The content-to-knowledge pipeline. Extract → Save → Find Later. This is how your SecondBrain grows.

**Success signal:** You can find your note in Obsidian with proper metadata and it shows up in the graph.

---

## Day 3 (Wednesday): Write Your First Steering Rule

**Goal:** Teach your AI something about how YOU work.

**What to do:**
1. Think about something your AI did during setup or Day 1-2 that wasn't quite right — too verbose, wrong tone, jumped ahead, etc.
2. Open your AI Steering Rules file: `~/.claude/skills/SNAP/USER/AISTEERINGRULES.md`
3. Add a new rule in the Statement / Bad / Correct format:
   ```
   ### [Rule Name]

   Statement
   : [What the AI should do]

   Bad
   : [Example of the wrong behavior]

   Correct
   : [Example of the right behavior]
   ```
4. Test it — give your AI a prompt that would have triggered the old behavior. See if it follows the new rule.

**What you're learning:** Your AI is trainable. Steering rules are how you shape its behavior over time. Two weeks of writing rules and your AI feels custom.

**Success signal:** Your AI behaves differently after adding the rule. It learned.

---

## Day 4 (Thursday): Update Your Telos

**Goal:** See how your life context makes your AI smarter.

**What to do:**
1. Ask your AI: "Show me my current Telos — what do you know about my goals and projects?"
2. Add or update something — maybe a new goal emerged this week, or a project priority shifted
3. Ask your AI to update the relevant Telos file
4. Then ask for help with a real problem. Notice how it uses your Telos context in its response.

**What you're learning:** Telos isn't a one-time setup. It's a living document. The more current it is, the more relevant your AI's responses become.

**Success signal:** Your AI references your goals or projects in a response without you explicitly reminding it.

---

## Day 5 (Friday): Reflect and Capture Learnings

**Goal:** Build the reflection habit that makes your AI (and you) better every week.

**What to do:**
1. Ask your AI: "What did we work on this week? Summarize our sessions."
2. Review the summary — what worked well? What felt clunky?
3. Write 2-3 observations:
   - One thing your AI does well
   - One thing you want to improve
   - One idea for a skill or workflow you wish existed
4. Save these as a note in your SecondBrain: `Knowledge/First-Week-Reflections.md`
5. If you identified a pain point — write another steering rule (Day 3 pattern)

**What you're learning:** The feedback loop. Use → Observe → Adjust → Use Again. This is how your AI compounds in value over time.

**Success signal:** You have a clear picture of what your AI does well and one concrete thing to improve next week.

---

## Weekend Bonus (Optional)

If you're curious and want to explore:

- **Try `/analyze-claims`** on a news article — see how your AI evaluates truth claims
- **Try `/create-mermaid-visualization`** on a process you use at work — see it as a diagram
- **Browse your Fabric patterns** — ask your AI "What patterns do I have available?" and try one you haven't used yet
- **Connect Todoist** (if you haven't) — try "Add a task to review my SNAP setup next Monday"

---

## What's Next?

**Week 2:** Start using your AI for real work tasks. Pick one recurring task from your job and run it through the AI with `/extract-wisdom` or `/create-summary`. Build the habit.

**Week 3:** Revisit your Telos. Update your GOALS and PROJECTS. Notice how your AI's context improves.

**Week 4:** Write your third steering rule. By now you'll know exactly what to tune.

**30-Day Check-In:** Your consultant is available for async support during this period. If you get stuck, reach out.

---

*Remember: The value isn't in the technology. It's in the habit. 15 minutes a day with your AI is worth more than one 8-hour marathon.*
