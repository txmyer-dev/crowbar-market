# Pre-Session Checklist Email

> Send this email 3-5 days before the Build Session. It ensures the client arrives with everything ready so you can spend the full session building, not troubleshooting prerequisites.

---

## Email Template

**Subject:** Your SNAP Build Session — What to Prepare Before [Date]

---

Hi [Client Name],

I'm looking forward to our Build Session on **[Date]** at **[Time]**. By the end of our 4-5 hours together, you'll have a fully working Personal AI system — your own AI assistant that knows your goals, remembers your context, and gets smarter every time you use it.

To make sure we spend every minute building (not installing), please complete these 5 items before our session:

---

### Checklist (15-20 minutes total)

**1. Claude Max Subscription** (5 min)
- Sign up at [console.anthropic.com](https://console.anthropic.com)
- Select the **Max plan** ($100/month — this is what powers your AI)
- You'll need this active before our session starts
- *Why:* Claude Max gives you unlimited access to the AI model we'll be configuring

**2. Laptop with Admin Access** (verify)
- Bring the computer you'll use daily with your AI
- You need the ability to install software (admin/sudo access)
- Windows 11 or macOS recommended
- *Why:* We'll install Claude Code, Obsidian, and configure your terminal

**3. "About Me" Document** (10 min)
- Write 1-2 pages about yourself. Include:
  - What you do professionally
  - What you're working on right now (projects, goals)
  - What problems you're trying to solve
  - What kind of AI assistant you want (serious, casual, creative, analytical)
  - Any tools or apps you already use daily
- Keep it informal — bullet points are fine
- *Why:* This is the seed content for your AI's personality and your life operating system

**4. Obsidian Installed** (2 min)
- Download from [obsidian.md](https://obsidian.md) (free for personal use)
- Just install it — don't create a vault yet, we'll do that together
- *Why:* Obsidian becomes your Second Brain — where your AI stores and retrieves knowledge

**5. Todoist Account** (2 min, optional)
- Sign up at [todoist.com](https://todoist.com) (free tier works)
- This is optional — if you use a different task manager, let me know
- *Why:* We'll connect your AI to your task manager so it can create, complete, and search tasks

---

### What to Expect

**Duration:** 4-5 hours (with breaks)

**Format:** Screen-share session — I'll be driving most of the setup while explaining what everything does. You'll take over for the personalization parts.

**By the end, you'll have:**
- A named AI assistant that knows who you are
- A life operating system (Telos) with your goals, projects, and strategies
- 15-20 AI skills matched to your role
- A Second Brain vault for permanent knowledge storage
- Behavioral hooks that enforce quality and security automatically
- A "First Week" playbook so you know exactly what to do on Day 1

**What you DON'T need to prepare:**
- No coding experience required
- No AI knowledge required
- No need to read documentation ahead of time
- Just bring yourself and the items above

---

### Questions?

Reply to this email or text me at [phone/contact]. If any of the items above are unclear or you run into issues, let me know — I'd rather sort it out now than during our session.

Looking forward to building this with you.

[Your Name]
[Your Title/Company]

---

## Consultant Notes (Do Not Include in Email)

### Pre-Session Prep (Your Side)

- [ ] Fresh ClientKit directory ready: `cp -r ~/.claude/skills/SNAP/ClientKit/* [staging-dir]/`
- [ ] Client Telos template ready: `~/.claude/skills/Telos/ClientTemplate/`
- [ ] Review client's "About Me" document when received — note key themes for Telos
- [ ] Prepare role-matched Fabric patterns from `client-fabric-patterns.md`
- [ ] Have hook files staged for quick copy
- [ ] Test your screen-sharing setup
- [ ] Block 5 hours on calendar (4-5 session + 30 min buffer)

### During-Session Quick Reference

| Hour | Focus | Key Files |
|------|-------|-----------|
| 1 | Identity + Telos | client-DAIDENTITY.md, client-KAI.md, Telos ClientTemplate/ |
| 2 | Algorithm + Skills | client-fabric-patterns.md, ExtractWisdom, FirstPrinciples |
| 3 | SecondBrain | client-secondbrain-template.md, Obsidian MCP |
| 4 | Hooks + Custom | client-hooks-package.md, 1 custom hook |
| 5 | Handoff + Review | client-first-week-playbook.md, Telos review |

### Post-Session

- [ ] Send follow-up email with installed file inventory
- [ ] Create 30-day support channel (Slack/Discord)
- [ ] Schedule 2-week check-in call
- [ ] Ask for testimonial at 30-day mark
