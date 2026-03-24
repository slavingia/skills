---
name: validate-idea
description: >
  Use when someone has a business idea and wants to know if it's worth pursuing.
  Triggers: "validate this idea", "is this worth building", "should I build X",
  "business idea", "startup idea", "will this work".
---

## Shared Context

- Read `../_shared/conventions.md` for cross-skill conventions.
- Read `gotchas.md` before every run — validation has specific failure modes.

## Core Principle

**Validation happens through selling, not building.** Most founders spend months building what nobody wants. Validate by selling a manual version first.

## 4-Step Validation Process

### 1. Define the Problem (not the solution)

- Who specifically has this problem? ("freelance designers who struggle with invoicing" not "businesses")
- How are they solving it today? (Current workarounds = real competition)
- How painful is it? (Mild annoyance vs. hair-on-fire)
- Would they pay to make it go away?

### 2. Can You Solve It Manually First?

Sahil calls this **"processizing"** — a manual valuable process before any code.

- Do it yourself. Write down every step on paper.
- If you can solve it manually for a few people, you can eventually automate it.
- Example: Gumroad started as Sahil manually collecting PayPal info and paying creators.

### 3. Will People Pay?

The ultimate validation is a transaction.

- Can you charge for this manual service right now?
- Have you talked to at least 10 potential customers?
- Have at least 3 said they'd pay (or actually paid)?
- What price point feels natural?

### 4. Four Build Questions

Before writing code, answer all four. See `references/four-build-questions.md` for full detail.

1. Can I ship it in a weekend?
2. Is it making customers' lives a little better?
3. Is a customer willing to pay for it?
4. Can I get feedback quickly?

## Red/Green Flags

| Red Flag | Green Flag |
|----------|------------|
| Nobody currently solving this problem | People paying for inferior solutions |
| Can't name 10 specific people with the problem | Manually solved it for a few people — they loved it |
| Only validation is "friends think it's cool" | Community actively complaining about this |
| Need to educate people they have the problem | Can describe customer + pain in one sentence |
| Building for a community you don't belong to | Scratching your own itch |

## Tool Integration

| Tool | Purpose |
|------|---------|
| Exa `company_research_exa` | Search for existing companies solving this problem |
| Perplexity `perplexity_search` / `perplexity_research` | Market size, trends, competitor landscape |
| Instant Domain Search `search_domains` | Quick domain availability check (but domain != validation) |

Run competitor search early — existing solutions are signal, not blockers.

## Output

Give a clear verdict:

- **Validated** — Strong signals across all 4 steps. Proceed to MVP.
- **Needs more validation** — Specific next steps to gather missing evidence.
- **Pivot** — Fundamental problems found. Suggest alternative directions.
