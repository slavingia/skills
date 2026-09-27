# Legal Checklist for Book-to-Skill Conversion

This checklist prevents the most common copyright mistake when converting a book into Claude Code skills: copying source paragraphs into skill files because paraphrasing is harder.

## The core rule

> **Paraphrase, do not copy. Any contiguous text from the source longer than 90 characters must be rewritten before going into a skill file.**

The 90-character threshold is not a legal safe harbor — it is a workflow rule. Copyright protects expression, not ideas, but copying a "short" passage verbatim can still infringe when the passage is qualitatively significant (a memorable sentence, a coined term, a one-line thesis). Use 90 characters as the trigger to *ask* the question, not as the answer.

## What counts as "copying"

The following all count, even if you reformat or wrap them differently:

- Direct quotation longer than 90 characters.
- "Light edits" — swapping a few words, changing tense, splitting a sentence. These are still derivative works under copyright.
- Translating a passage into another language without transforming the structure.
- Reproducing a list whose selection and arrangement is itself expressive (e.g. "the seven principles of X" if the selection is the author's).
- Reproducing a unique coined term used in a defining context (the term itself may be fine; the defining context may not be).

## What does NOT count as copying

These are safe and should be the default:

- Restating a principle in your own words.
- Reproducing a short fact that is not original expression (dates, public statistics, standard definitions).
- Naming the book's concepts (e.g. "processize", "magic piece of paper", "ikigai") — single terms and short phrases are usually fine, especially when the book is the source you are converting.
- Quoting under fair use for the purpose of criticism, comment, or parody. This is not the use case here; skills are operational, not critical.

## What every skill file must contain

Add a short provenance line at the bottom of every `SKILL.md`:

```
---
Source: <book title> by <author> (<year>).
Paraphrased and restructured for skill use. All claims tagged
[source: §chapter] trace to specific passages; [SYNTHESIS] tags
mark operational rewrites not present in the original.
```

This is not a license grant. It is a factual statement that helps reviewers trace claims and tells future readers what the skill is derived from.

## Annotations every claim needs

Inside each skill, every actionable sentence carries one of these tags:

| Tag | Meaning |
|---|---|
| `[source: §N.M]` | Paraphrased from section N.M of the source. |
| `[source: Ch. N, §section]` | Same, with chapter and section names. |
| `[EXAMPLE]` | Paraphrases a case study from the source (e.g. a specific founder's story). The principle is in the book; the example is illustrative. |
| `[SYNTHESIS]` | Your rewrite to make the principle executable as a skill. Not a direct quote. |
| `[EXTERNAL]` | Added by you; not supported by the source. Tag explicitly so the user knows. |
| `[UNVERIFIED]` | You cannot trace the claim. Either find the source or delete. |

The tags are mandatory. They are the cheapest way to keep a converted skill honest as it evolves.

## When you must stop and ask the user

Stop and ask before delivering if any of the following:

- The book is under copyright and you cannot confirm the user owns a copy or has a license.
- The book's license (e.g. CC BY-SA) requires attribution or share-alike that the skill does not yet preserve.
- The conversion produces more than ~20% verbatim text from any single chapter (rough rule of thumb; not a legal standard).
- The book explicitly forbids derivative works.
- The user intends to redistribute the skill publicly. In that case, the user — not you — is responsible for confirming the redistribution is lawful.

## What this checklist is not

- It is not legal advice. If the stakes are high (commercial redistribution, large audience, contested source), the user should consult an attorney.
- It is not a guarantee that any specific paraphrase is safe. Paraphrases can still infringe if they track the original too closely.
- It is not a substitute for getting the author's permission when in doubt. A short email to the author can resolve most ambiguity.

## Workflow

Before writing any skill:

1. Confirm the user has a copy of the book (file path or library access).
2. Confirm the user understands paraphrasing is required, not optional.
3. Confirm whether the output will be private (used by the user only) or public (shared, redistributed).
4. If public: ask the user to confirm they have the right to redistribute derivative skills.

After writing, run `scripts/cite_tracker.py` to verify every claim is tagged.