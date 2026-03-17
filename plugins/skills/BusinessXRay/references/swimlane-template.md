# Swim Lane Mermaid Template

Use this template when mapping a core system (Lead Gen, Sales, or Fulfillment) in Phase 2.

## Template

```mermaid
graph TD
    classDef bottleneck fill:#ff6b6b,stroke:#c0392b,color:#fff
    classDef automated fill:#2ecc71,stroke:#27ae60,color:#fff
    classDef manual fill:#f39c12,stroke:#e67e22,color:#fff

    subgraph Owner["👤 Owner (Manual)"]
        O1[Step description]:::manual
        O2[Step description]:::manual
        O3[Step description]:::bottleneck
    end

    subgraph AI["🤖 AI / Automation"]
        A1[Step description]:::automated
        A2[Step description]:::automated
    end

    subgraph Output["📦 Output"]
        R1[Result description]
        R2[Result description]
    end

    O1 --> A1
    A1 --> R1
    O2 --> O3
    O3 --> A2
    A2 --> R2
```

## Class Guide

| Class | Meaning | When to use |
|-------|---------|-------------|
| `:::bottleneck` | Human doing repetitive work AI could handle | The core finding — this is what gets automated |
| `:::automated` | Already handled by a system or tool | Show what's working to give credit |
| `:::manual` | Human step that's appropriate (judgment, relationship) | Not everything needs automating |

## Example: Lead Gen System

```mermaid
graph TD
    classDef bottleneck fill:#ff6b6b,stroke:#c0392b,color:#fff
    classDef automated fill:#2ecc71,stroke:#27ae60,color:#fff
    classDef manual fill:#f39c12,stroke:#e67e22,color:#fff

    subgraph Owner["👤 Owner"]
        O1["Record video (weekly)"]:::manual
        O2["Write newsletter (2hrs)"]:::bottleneck
        O3["Reply to DMs (1hr/day)"]:::bottleneck
    end

    subgraph AI["🤖 AI / Automation"]
        A1["Auto-publish to YT + socials"]:::automated
        A2["Repurpose video → clips"]:::automated
        A3["CRM tags new leads"]:::automated
    end

    subgraph Output["📦 Output"]
        R1["3-5 leads/week from content"]
        R2["Email list grows 50/week"]
        R3["DM convos → booked calls"]
    end

    O1 --> A1
    A1 --> A2
    A2 --> R1
    O2 --> R2
    O3 --> A3
    A3 --> R3
```

In this example, `O2` and `O3` are bottlenecks — the owner spends 3+ hours/day on tasks that could be AI-assisted (newsletter drafting, DM triage).
