---
name: minimalist-review
description: Use when gut-checking any business decision, simplifying an approach, or choosing between options. Triggers on "should I do this?", "review my plan", "is this too complex?", or "help me decide."
argument-hint: "[describe your decision or situation]"
---

Review `_shared/conventions.md` before executing. Review `gotchas.md` for common failure modes.

## First: Determine the User's Stage

Before applying principles, ask what stage they are at. Early-stage founders need different filters than post-revenue businesses. If they are at the wrong stage for this skill, redirect to the right one (see `_shared/conventions.md` skill progression).

## 8 Principles — Evaluation Checklist

Apply these as lenses, not as a rigid sequence. Weight by relevance to the user's situation.

| # | Principle | Key Question |
|---|-----------|-------------|
| 1 | Community First | Does this serve your community, or is it ego/vanity? |
| 2 | Start Manual, Then Automate | Could you do this by hand first? Have you done it enough times to know it works? |
| 3 | Build as Little as Possible | Can you ship this in a weekend? What is the simplest version? |
| 4 | Sell Before You Scale | Have real people paid real money? Manual sales = 99% of early growth. |
| 5 | Spend Time Before Money | Can you do this with time instead of money? Only spend to accelerate what already works. |
| 6 | Profitability is the Goal | Does this move you toward or away from profitability? Is it reversible? |
| 7 | Grow at Customer Speed | Are customers asking for this, or are you guessing? |
| 8 | Build the House You Want to Live In | Would you want to work here in 5 years if you keep making decisions like this? |

## Decision Framework

| Question | Score |
|----------|-------|
| Does this serve my community/customers? | Yes / No / Unclear |
| Is this the simplest approach? | Yes / No / Simpler exists |
| Does this improve profitability? | Yes / No / Neutral |
| Is this reversible if it fails? | Yes / No / Partially |
| Am I spending time or money? | Time / Money / Both |
| Have customers asked for this? | Yes / No / Assumed |
| Does this align with my values? | Yes / No / Untested |
| Will I still want this in a year? | Yes / No / Unsure |

## Tool Integration

Use `qmd query "<topic>" -c minimalist-entrepreneur` for relevant book passages. Cross-reference other skills when the review surfaces stage-specific issues (e.g., pricing problems -> `/pricing`, community gaps -> `/find-community`).

## Output

| Deliverable | Detail |
|-------------|--------|
| Recommendation | Do it / don't do it / simplify it — with reasoning |
| Minimalist version | What the simplest viable version of their plan looks like |
| Biggest risk | The one thing most likely to go wrong |
| This-week action | One concrete thing to try this week to validate the decision |
