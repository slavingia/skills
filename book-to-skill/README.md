# book-to-skill

A Claude Code skill for converting non-fiction books into Claude Code skills.

## What it does

Given a book file (EPUB, Markdown, or PDF) and optionally a target skill repo to audit, this skill:

1. Decides whether the book is convertible (rejects fiction, poetry, and pure narrative)
2. Extracts the chapter structure into a JSON dump
3. Audits any target repo for fidelity to the source
4. Plans a router + subskills whose count stays under the chapter count
5. Writes each `SKILL.md` by paraphrasing the source, never copying it

It deliberately does **not** fork the repo, create a branch, commit, push, or open a pull request. Those steps are out of scope; ship the conversion manually.

## Files

```
book-to-skill/
  SKILL.md                          # the skill itself
  README.md                         # this file
  references/
    legal-checklist.md              # copyright rules for paraphrasing
    frontmatter-schema.md           # YAML fields Claude Code expects
    style-patterns.md               # how to match existing skill voice
    audit-rubric.md                 # 10-dimension fidelity scoring rubric
  scripts/
    extract_chapters.py             # EPUB/MD/PDF -> JSON
    diff_against_repo.py            # book JSON + repo -> per-skill audit
    cite_tracker.py                 # verify [source] tags in SKILL.md files
```

## Usage

In Claude Code, invoke the skill and provide:

- Path to the book file (EPUB, Markdown, or PDF)
- Optional path to the target skill repo to audit

The skill will:

1. Run `scripts/extract_chapters.py` against the book
2. Read the JSON output and write a one-paragraph decision-model summary per chapter
3. If a target repo is given, run `scripts/diff_against_repo.py` for a per-skill audit
4. Output a plan table mapping skills to chapters
5. Write each `SKILL.md` per the plan
6. Run `scripts/cite_tracker.py` to verify citation discipline

The skill is meant to be invoked once per book. It produces the conversion output; the user reviews and ships.

## What this skill is not

- It is not a one-shot "give me a book, give me 10 skills" button. The decision of how many skills, what to merge, what to drop requires human judgment.
- It is not a copyright safe harbor. The legal-checklist.md reference is a workflow rule, not legal advice.
- It is not a substitute for reading the source. The skill's output quality depends on the converter actually engaging with the book's arguments.

## Scope guardrails

The skill enforces these limits on itself:

- Skills ≤ chapters (plus optional router)
- No verbatim copying longer than 90 characters
- Every claim tagged `[BOOK]`, `[EXAMPLE]`, `[SYNTHESIS]`, `[EXTERNAL]`, or `[UNVERIFIED]`
- No invented numeric thresholds
- Scope boundary from the source preserved at the top of every relevant skill
- External-facing actions (email, posting, spending) gated behind human confirmation

## Testing

Run the scripts directly against a known EPUB to verify:

```bash
python3 scripts/extract_chapters.py path/to/book.epub > book.json
python3 scripts/diff_against_repo.py book.json path/to/target-repo > audit.json
python3 scripts/cite_tracker.py path/to/target-repo/skills
```

`cite_tracker.py` exits non-zero if any skill has problems; use this as a CI gate.

## License

This skill and its scripts are released under the same terms as the rest of the project (see project root). The reference documents paraphrase operational rules and do not contain source material from any specific book.