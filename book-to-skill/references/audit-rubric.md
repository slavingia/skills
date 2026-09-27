# Audit Rubric for Book-to-Skill Conversions

Use this rubric to grade how faithful a book-to-skill conversion is. Score each dimension 0-3. The total is a rough signal, not a verdict.

A "conversion" can mean: a brand-new conversion you are about to write, an existing repo you are auditing, or a draft you want to check before delivery.

## Dimensions

### 1. Source coverage (0-3)

How much of the book's actionable content is captured?

- **3**: every chapter with standalone takeaways has a skill; subtopics fold into parent skills
- **2**: most chapters covered, one or two subtopics folded awkwardly
- **1**: gaps in coverage; missing chapters or merged chapters lose distinct content
- **0**: major chapters missing or only one mega-skill for the whole book

### 2. Paraphrase discipline (0-3)

How well does the conversion avoid copying source text?

- **3**: every claim is in the converter's own words; no passage longer than 90 chars from source
- **2**: mostly paraphrased; a few short verbatim phrases remain
- **1**: heavy reliance on copy with light edits
- **0**: large blocks of source text reproduced

### 3. Scope boundary preservation (0-3)

Did the converter reproduce the book's "this does not apply to X" declarations?

- **3**: scope boundary is stated at the top of every relevant skill
- **2**: scope boundary stated once but not repeated
- **1**: boundary mentioned only in passing
- **0**: boundary stripped; skills feel universal

### 4. Epistemic tagging (0-3)

Are claims tagged as `[BOOK]`, `[EXAMPLE]`, `[SYNTHESIS]`, `[EXTERNAL]`, `[UNVERIFIED]`?

- **3**: every actionable sentence tagged
- **2**: most claims tagged, a few untagged
- **1**: tagging inconsistent
- **0**: no tagging

### 5. Threshold accuracy (0-3)

Are numeric thresholds preserved exactly as the source states them — neither invented nor exaggerated?

- **3**: numbers only where the source has them; no fabricated "do this 10 times"
- **2**: source numbers preserved; a few minor additions
- **1**: some numbers invented or stretched
- **0**: thresholds made up wholesale

### 6. Anti-pattern coverage (0-3)

Does each skill include the source's anti-patterns?

- **3**: anti-patterns in every skill that has them in the source
- **2**: anti-patterns in most skills
- **1**: anti-patterns in only one or two skills
- **0**: anti-patterns missing

### 7. Output specificity (0-3)

Does the Output section specify concrete artifacts?

- **3**: every output item names a specific deliverable the agent must produce
- **2**: most items specific, a few vague
- **1**: vague outputs ("summarize the result")
- **0**: no Output section or all items are questions

### 8. Skill count discipline (0-3)

Does the count respect "skills ≤ chapters"?

- **3**: at most one skill per chapter (plus optional router)
- **2**: one extra skill for a justified synthesis need
- **1**: 2-3 extra skills; not all justified
- **0**: skill count exceeds chapter count by 4+

### 9. Sequencing / ordering (0-3)

Are the skills ordered to match the book's progression, and is any chapter that introduces terminology referenced before the chapter that uses it?

- **3**: ordering matches the book; terminology cross-references correct
- **2**: ordering close but with minor inversions
- **1**: ordering scrambled
- **0**: no discernible order; skills could be invoked in any sequence

### 10. Action safety (0-3)

For each skill that recommends actions the agent could execute automatically (sending messages, posting publicly, spending money), is there a human-confirmation step?

- **3**: every external-facing action requires explicit user confirmation
- **2**: most external actions gated
- **1**: a few external actions gated, others open
- **0**: no gating; agent may execute public/spending actions autonomously

## Score interpretation

- **27-30**: high-quality conversion. Ship it.
- **22-26**: good, fix the weak dimensions before delivery.
- **17-21**: significant issues. Audit and rewrite the weak dimensions.
- **12-16**: major rework needed.
- **0-11**: not a conversion; redo from Step 1.

## How to use this rubric

1. Score each dimension with 0-3. Note which sentences/claims justify each score.
2. Compute the total. Decide whether to ship, fix, or redo.
3. For dimensions scoring 0 or 1, list the specific changes needed.
4. Re-run after fixes.

## Limitations

- The rubric is opinionated. A conversion could legitimately score low on one dimension and still be useful (e.g. a 1 on threshold accuracy if the source has no thresholds at all).
- It does not measure whether the skills actually work in production. Run the skills in Claude Code before final delivery.
- It does not measure whether the converted skills are *good* advice for the user's situation. The book may have biases; the converter inherits them.

The rubric measures conversion quality, not advice quality. Don't use it to bless a bad book.