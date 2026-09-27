# Style Patterns for Book-Derived Skills

This reference captures the writing style used in well-regarded book-derived skill repos (notably `slavingia/skills`). Match this style when writing new skills so the converted output feels native to Claude Code's skill ecosystem.

## Voice

- **Direct second person.** Address the user as "you", not "the founder" or "users". The skill is coaching the human in front of it.
- **Imperative for actions.** "Do X" not "One should consider doing X".
- **No corporate hedging.** Avoid "may help", "could potentially", "in some cases". The source book probably has opinions; preserve them.
- **One principle per paragraph.** Each section header introduces one idea. Don't blend two principles into one block.

## Paragraph length

- 1-4 sentences per paragraph.
- No paragraph longer than ~6 lines on a standard screen.
- Prefer many short paragraphs over a few long ones.

## Section structure (per skill)

The body of a `SKILL.md` should follow this order:

```
## Core Principle
[One paragraph: the chapter's central thesis in your own words,
with a short quote from the source if it captures the idea tightly.]

## When to Use This Skill
[Bulleted list of situations. 3-6 items.]

## Step 1: <Verb> <Object>
[2-4 paragraphs. One numbered step = one decision or one transformation.]

## Step 2: ...

## Anti-Patterns
[Bulleted list. Each item is a short sentence naming the anti-pattern,
not a paragraph explaining it.]

## Output
[Numbered list, 3-6 items. Each item names a concrete artifact the
agent must produce.]
```

Optional sections, used when the source supports them:

```
## Decision Framework          # when the source gives a checklist
## Key Takeaways                # when the source's own takeaways add value
## Common Mistakes              # alias for Anti-Patterns; use Anti-Patterns
```

Do NOT include sections like "Introduction", "Background", "What is X". The reader already knows what they invoked.

## How to introduce a Core Principle

Three acceptable patterns:

1. **Paraphrased thesis**: state the principle in your own words, then add a 1-line source quote if it captures the idea.
   ```
   **A business is a tool, not an identity.**
   > "When I was no longer on track to become a dollar billionaire,
   > I realized I was a time billionaire."
   ```

2. **Direct principle statement**: one bold sentence, no quote.
   ```
   **Validate by selling, not by building.**
   ```

3. **Conditional principle**: when the source is conditional ("this applies when X"), state the condition first.
   ```
   **If your customer feedback loop is fast, charge from day one.
   If it is slow, you need a different model.**
   ```

Pattern 1 is the default for skills paraphrasing a method book.

## How to write Anti-Patterns

Anti-patterns are short, named, and observable. Not paragraphs.

```
- Confusing a profitable quarter with a sustainable life.
- Staying in the founder seat out of guilt, identity, or fear of being called a quitter.
- Scaling to justify your own past decisions instead of the customers' present needs.
```

Avoid anti-patterns like "Be careful not to..." — that is a warning, not a pattern.

## How to write Output

Output items are deliverables. Each is a noun phrase, not a sentence.

```
1. A clear recommendation (do it / don't do it / simplify it)
2. What the minimalist version of their plan looks like
3. The biggest risk they should watch for
4. One thing to try this week to validate the decision
```

Each item is something the agent can produce. If you cannot describe what the agent should produce for an item, that item does not belong in Output.

## Cross-referencing other skills

Use natural prose, not markdown links to other skills:

```
If the business has not yet been "processized," go back to `processize`
and write the magic piece of paper so it can run without you.
```

This way the skill reads as prose even when invoked without the rest of the repo.

## What NOT to do

- Don't start with "In this skill, we will...". The user invoked it; just start.
- Don't write an "Examples" section that invents fake scenarios. The source may have examples; paraphrase those, don't invent.
- Don't put the Output section at the top. Users skim to the end for deliverables.
- Don't use emoji. The skill ecosystem has settled on plain text.
- Don't use tables unless they replace a checklist. Tables for steps and gates are fine; tables for principles are not.
- Don't quote more than one short line of the source per section. If you find yourself reaching for a second quote, paraphrase instead.

## Length budget

A single `SKILL.md` should be ≤ 250 lines. If you are pushing past 250:

- You may be writing more than one chapter's worth. Split into separate skills.
- You may be including reference content that belongs in `references/`. Move it.
- You may be repeating the same idea in different sections. Cut one.

The existing well-regarded skills in `slavingia/skills` average 50-90 lines. Use that as a sanity check.