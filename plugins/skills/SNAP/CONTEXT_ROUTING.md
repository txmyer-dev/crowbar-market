# Context Routing Table

**Purpose:** Lazy-load documentation on demand instead of preloading everything at session start. When you need specialized context, look up the topic here and `Read` the file.

**Added:** v4-upgrade (2026-03-02) — inspired by SNAP v4.0 context diet pattern.

## System Documentation

| Topic | Path | When to Load |
|-------|------|-------------|
| The Algorithm (full 7-phase) | `skills/SNAP/SKILL.md` | When FormatReminder hook classifies depth as FULL |
| System architecture overview | `skills/SNAP/SYSTEM/SNAPSYSTEMARCHITECTURE.md` | When discussing SNAP design, architecture decisions |
| Memory system (WORK, STATE, LEARNING) | `skills/SNAP/SYSTEM/MEMORYSYSTEM.md` | When working with memory directories, session logs |
| Skill system | `skills/SNAP/SYSTEM/SKILLSYSTEM.md` | When creating/modifying skills, skill triggers |
| Hook system | `skills/SNAP/SYSTEM/THEHOOKSYSTEM.md` | When creating/modifying hooks, hook debugging |
| Agent system | `skills/SNAP/SYSTEM/SNAPAGENTSYSTEM.md` | When spawning agents, agent architecture questions |
| Delegation system | `skills/SNAP/SYSTEM/THEDELEGATIONSYSTEM.md` | When parallelizing work, background agents |
| Browser automation | `skills/SNAP/SYSTEM/BROWSERAUTOMATION.md` | When using Playwright, screenshots, browser testing |
| CLI-first architecture | `skills/SNAP/SYSTEM/CLIFIRSTARCHITECTURE.md` | When building CLI tools, command-line patterns |
| Notification system | `skills/SNAP/SYSTEM/THENOTIFICATIONSYSTEM.md` | When configuring voice, ntfy, visual notifications |
| Tools reference | `skills/SNAP/SYSTEM/TOOLS.md` | When looking up available tools and their usage |
| Fabric system | `skills/SNAP/SYSTEM/THEFABRICSYSTEM.md` | When working with Fabric patterns |
| Terminal tabs | `skills/SNAP/SYSTEM/TERMINALTABS.md` | When managing terminal tab operations |
| Pipelines | `skills/SNAP/SYSTEM/PIPELINES.md` | When building multi-step automation pipelines |
| System/User extendability | `skills/SNAP/SYSTEM/SYSTEM_USER_EXTENDABILITY.md` | When customizing system vs user overrides |
| Documentation index | `skills/SNAP/SYSTEM/DOCUMENTATIONINDEX.md` | When looking for any documentation not listed here |

## User Context

| Topic | Path | When to Load |
|-------|------|-------------|
| User projects registry | `skills/SNAP/USER/PROJECTS/PROJECTS.md` | When discussing projects, deployment, project routing |
| Telos (life goals) | `skills/SNAP/USER/TELOS/PROJECTS.md` | When discussing life goals, challenges, predictions |
| Tech stack preferences | `skills/SNAP/USER/TECHSTACKPREFERENCES.md` | When making technology choices, tool selection |
| Soul file (evolving identity) | `skills/SNAP/USER/KAI.md` | When relationship context needed beyond what LoadContext provides |
| Skill customizations | `skills/SNAP/USER/SKILLCUSTOMIZATIONS/` | When running a skill that has user overrides |

## Loading Protocol

1. Check if the topic matches this table
2. `Read` the file path listed
3. Use the context for the current task
4. Do NOT preload files "just in case" — load only what you need right now
