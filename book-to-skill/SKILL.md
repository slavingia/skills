---
name: book-to-skill
description: Convert a book (EPUB/PDF/Markdown) into Claude Code skills — extract structure, audit existing skills if any, plan router + subskills, write SKILL.md files that paraphrase the source rather than copy it. Use when turning a non-fiction book into agent skills, when auditing how faithful an existing book-to-skill conversion is, or when planning how many skills a book should yield.
argument-hint: path to the book file (EPUB, PDF, or Markdown) and optional path to the target skill repo
---

You are a book-to-skill conversion specialist. Convert a non-fiction book into Claude Code skills while respecting copyright, preserving the source's epistemic status, and producing a router + subskills whose count stays under the source's chapter count.

## Core Principle

**Paraphrase the source, never copy it.** A skill that quotes paragraphs from the book is a copyright risk; a skill that loses the source's meaning is useless. The job is to extract the **decision model** — questions, gates, anti-patterns, outputs — and rewrite it in your own words, with `[source: §chapter]` annotations so reviewers can trace each claim back to where it came from.

Three other non-negotiables:

1. **Skills ≤ chapters.** If the source has 8 chapters, the conversion yields at most 8 skills (plus an optional router). This matches the explicit preference expressed in `slavingia/skills` PR #22 ("Don't want more skills than chapters"). Subtopics of a chapter fold into the chapter's skill, not into a new file.
2. **Preserve the source's scope boundary.** Most method books include a section that says "this does not apply to X." Reproduce that boundary at the top of every skill — do not strip it, even if it makes the skill feel less universal.
3. **Distinguish epistemic status.** Tag every output line as `[BOOK]` (directly stated), `[EXAMPLE]` (a case study the book uses), `[SYNTHESIS]` (your operationalization to make it executable), or `[EXTERNAL]` (anything you added that the book does not support). Without these tags, users cannot tell which numeric thresholds and platform prescriptions are authorial.

## When to Use This Skill

- A user gives you a non-fiction book and wants it converted into Claude Code skills.
- A user has an existing book-to-skill repo (e.g. `slavingia/skills`) and wants to audit how faithful the conversion is.
- A user wants to plan how many skills a book should yield before writing any of them.
- A user wants to know whether a book is even suitable for skill conversion.

Do NOT use this skill for: novels, poetry, memoirs, picture books, or any source whose primary value is aesthetic or narrative. The conversion only works for method books, frameworks, playbooks, and manifestos with actionable content.

## Step 1: Scope Gate

Before opening the file, decide whether the source is convertible. Reject and explain if any of the following:

- The book is fiction, poetry, memoir, or narrative-driven.
- The book's actionable content is less than ~30% of total length (the rest is story, history, or theory).
- The book is under copyright and the user has no clear right to redistribute derived skills. (Paraphrased skills are usually fine; verbatim skill files containing 100+ word excerpts are not.)
- The user wants one giant skill containing every chapter. This always produces an unusable skill that exceeds the context budget.

If convertible, capture:

- Book title, author, publication year
- Total chapter count (including introduction if it has standalone takeaways)
- Whether the user has a target repo to audit, or is starting from scratch

## Step 2: Extract

Run `scripts/extract_chapters.py <path-to-book>` to produce a structured JSON dump. The script handles EPUB via `zipfile` + `HTMLParser`, plain Markdown via regex on headers, and PDF via a fallback that warns about limited fidelity.

The output JSON has this shape:

```json
{
  "title": "...",
  "author": "...",
  "chapters": [
    {
      "index": 1,
      "title": "...",
      "is_intro": false,
      "sections": [
        {"title": "...", "text": "...", "char_count": 1234}
      ]
    }
  ]
}
```

Read the JSON. For each chapter, write a one-paragraph "decision model" summary:

- What question does this chapter answer?
- What is the chapter's main gate or threshold (if any)?
- What does the chapter tell the user to do next?

Do this before moving on. The summaries are the input to Step 4.

## Step 3: Audit (only if a target repo exists)

If the user provides a target repo (e.g. `slavingia/skills`), run `scripts/diff_against_repo.py <book.json> <target-repo-path>`. The script produces a per-skill mapping:

```
skill_name → primary chapter, secondary chapters, support_level, issues
```

Where `support_level` is one of:

- `DIRECT` — the skill's body matches specific paragraphs from the book
- `SYNTHESIS` — the skill is a reasonable operationalization not stated in those words
- `EXTERNAL` — the skill contains thresholds, platforms, or advice not in the book
- `CONFLICT` — the skill contradicts the book on a specific point

Also extract from the repo:

- The repo's `plugin.json` or `marketplace.json` — does it auto-discover `SKILL.md` or require explicit registration?
- The repo's commit history — is the author active? Are there closed PRs that signal preferences (e.g. "don't want more skills than chapters")?
- The repo's license status — `LICENSE` file present? `plugin.json` claims a license that doesn't exist on disk?

Output a one-page audit summary before writing anything.

## Step 4: Plan

Decide the skill structure. Output a table like this to the user before writing:

```
| Skill           | Source chapter    | Type        | Notes                          |
|-----------------|-------------------|-------------|--------------------------------|
| <router>        | n/a               | router      | stage detection, scope gate    |
| <skill-1>       | Ch. 2             | DIRECT      |                                |
| <skill-2>       | Ch. 3             | SYNTHESIS   | merges two overlapping skills  |
| ...             |                   |             |                                |
| <new-skill-N>   | Ch. 8 (missing)   | DIRECT      | fills the missing chapter slot |
```

Rules:

- **Skill count ≤ chapter count.** If the source has 8 chapters and the target repo has 10 skills, propose merging or removing — do not add more.
- **One router, optional.** Add a router skill only if the user needs stage detection. If the user is going to invoke skills manually based on their situation, skip the router.
- **Each skill covers one chapter's full decision model**, including its scope boundary, anti-patterns, and outputs.
- **Subtopics fold into the parent chapter's skill.** A chapter's subsections become sub-steps or "When to use" branches in one file, not separate files.

If the plan conflicts with an existing repo's structure, the PR description (if writing one) should call this out explicitly. Do not silently rewrite an existing repo without telling the user.

## Step 5: Write

For each planned skill, write `SKILL.md` using the frontmatter schema in `references/frontmatter-schema.md` and the style patterns in `references/style-patterns.md`.

Hard rules during writing:

1. **Paraphrase, do not copy.** Any sentence longer than 90 characters verbatim from the source must be flagged and rewritten. The `legal-checklist.md` reference explains the threshold.
2. **Cite source on every claim.** Format: `[source: §chapter-section]` or `[source: Ch. N, §section]`. If a claim is your synthesis, tag `[SYNTHESIS]`. If you cannot trace it, tag `[UNVERIFIED]` and either find the source or delete the claim.
3. **Every skill starts with a scope boundary.** If the book says "this does not apply to slow-feedback businesses," that sentence — paraphrased — must appear at the top of every relevant skill.
4. **Never invent numeric thresholds.** If the book says "do this until it works," write "do this until evidence shows it works" — not "do this 10 times." Only reproduce numbers that appear in the source.
5. **Reproduce anti-patterns.** Most method books include a "don't do X" section. Paraphrase those into the skill's `## Anti-Patterns` section.
6. **Output section must be concrete.** End each skill with a numbered `## Output` list specifying exactly what artifacts the agent should produce. Vague outputs like "summarize the result" are not allowed.
7. **Tone matches the source.** Read 2-3 paragraphs from the source first. Match: short paragraphs, direct address ("you"), em-dashes over parenthetical asides, imperative voice. Do not import a different house style.

After writing all skills, run `scripts/cite_tracker.py <output-dir>` to verify:

- Every skill has at least one `[source: ...]` annotation
- No skill contains more than 3 `[UNVERIFIED]` tags
- No two skills duplicate the same source paragraph

If verification fails, fix before delivering.

## Output

Give the user:
1. **The plan table** from Step 4.
2. **The audit summary** from Step 3 (if a target repo was audited).
3. **A list of all files written** with one-line descriptions.
4. **A traceability report**: for each skill, which chapter(s) it draws from, which sections, and which claims are `[BOOK]` vs `[SYNTHESIS]` vs `[EXTERNAL]`.
5. **A list of open questions** the user should resolve before any redistribution (e.g. copyright review, license file presence, author approval).

## Anti-Patterns

- Treating the book as a chapter-by-chapter summarization task. The goal is decision logic, not recap.
- Copying paragraphs because paraphrasing them would be slower. Speed is not a license to infringe.
- Adding numeric thresholds the source does not contain. "10 interviews, 3 willing to pay" is not in most books; do not invent it.
- Stripping the book's scope boundary to make the skill feel universal. The boundary is the most load-bearing sentence in the source.
- Producing a single mega-skill with all chapters. It will exceed context and lose the routing value of separate skills.
- Skipping the audit step when a target repo exists. Most conversion failures come from not noticing that the repo already covers (or contradicts) what you are about to write.
- Writing skills that recommend actions the agent will execute automatically (sending emails, posting publicly, spending money) without an explicit human-confirmation step. The book may say "do X"; the skill must add "ask the user before doing X."