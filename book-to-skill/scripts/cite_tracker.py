#!/usr/bin/env python3
"""Verify citation discipline across a directory of SKILL.md files.

Checks each `SKILL.md` for:
  - at least one [source: ...] or [BOOK] / [SYNTHESIS] / [EXTERNAL] / [EXAMPLE] / [UNVERIFIED] tag
  - no more than 3 [UNVERIFIED] tags per skill
  - no paragraph longer than ~90 chars without a tag (rough paraphrase-discipline heuristic)
  - no fabricated numeric thresholds not preceded by a [SYNTHESIS] or [EXTERNAL] tag

Outputs a per-skill report and a summary count.

Usage:
  python3 cite_tracker.py /path/to/skills-dir
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


TAG_PATTERN = re.compile(
    r"\[(source:[^\]]+|BOOK|SYNTHESIS|EXAMPLE|EXTERNAL|UNVERIFIED)\]",
    re.I,
)
THRESHOLD_PATTERN = re.compile(
    r"\b(\d{2,}\+?\s+(?:paying|customers|users|people|interviews)|"
    r"\d{2}[\u2013-]\d{2}\s*%|"
    r"one in \d+|at least \d+|"
    r"\d+\s+customers?\s+per\s+\w+)\b",
    re.I,
)
PARAGRAPH_RE = re.compile(r"(?:\n\s*\n|(?=^##\s))", re.M | re.S)


def _paragraphs(text: str) -> list[str]:
    body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    # Drop the standard role-prompt line(s) that introduce the skill
    body = re.sub(
        r"^You are a business advisor channeling[^\n]*\.\s*",
        "",
        body,
        flags=re.M,
    )
    body = re.sub(r"^##\s.*$", "", body, flags=re.M)
    paras = [p.strip() for p in PARAGRAPH_RE.split(body) if p.strip()]
    return paras


def check_skill(path: Path, source_text: str | None = None) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    tags = [m.group(1) for m in TAG_PATTERN.finditer(text)]
    tag_counts = Counter(t.upper() for t in tags)
    paragraphs = _paragraphs(text)
    long_untagged = []
    for p in paragraphs:
        # Only count paragraphs that contain actionable sentences
        # (skip section headers, blank lines, etc.)
        if len(p) < 90:
            continue
        # If paragraph contains at least one tag, skip
        if TAG_PATTERN.search(p):
            continue
        # Skip paragraphs that are clearly structural (lists, tables, output blocks)
        if p.lstrip().startswith(("- ", "* ", "|", "1.", "2.", "3.", "4.", "5.", "6.")):
            continue
        # Skip blockquotes (typical for short source quotes)
        if p.lstrip().startswith(">"):
            continue
        long_untagged.append(p[:140] + ("..." if len(p) > 140 else ""))

    fabricated_thresholds = []
    for m in THRESHOLD_PATTERN.finditer(text):
        # Allow thresholds if the surrounding paragraph has a [SYNTHESIS] or [EXTERNAL] tag
        snippet = text[max(0, m.start() - 200): min(len(text), m.end() + 50)]
        if re.search(r"\[(SYNTHESIS|EXTERNAL|source:)", snippet, re.I):
            continue
        # If a source text was provided, suppress the warning when the same
        # threshold (or its numeric core) actually appears in the source.
        if source_text:
            num = re.search(r"\d{2,}", m.group(0))
            if num and num.group(0) in source_text:
                continue
        fabricated_thresholds.append(m.group(0))

    problems = []
    if not tags:
        problems.append("no citation tags at all")
    if tag_counts.get("UNVERIFIED", 0) > 3:
        problems.append(f"too many UNVERIFIED tags: {tag_counts['UNVERIFIED']}")
    if long_untagged:
        problems.append(f"{len(long_untagged)} long paragraph(s) without citation tag")
    if fabricated_thresholds:
        problems.append(
            f"fabricated threshold(s) without [SYNTHESIS]/[EXTERNAL] tag: {fabricated_thresholds}"
        )

    return {
        "skill": path.parent.name,
        "tag_counts": dict(tag_counts),
        "problems": problems,
        "long_untagged_samples": long_untagged[:3],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify citation discipline in skill files")
    parser.add_argument("skills_dir", type=Path, help="path to a skills/ directory")
    parser.add_argument(
        "--source",
        type=Path,
        default=None,
        help="optional path to source JSON (from extract_chapters.py); "
        "suppresses false positives for thresholds present in the source",
    )
    args = parser.parse_args()
    if not args.skills_dir.exists():
        print(f"error: directory not found: {args.skills_dir}", file=sys.stderr)
        return 1
    source_text = None
    if args.source and args.source.exists():
        try:
            book = json.loads(args.source.read_text(encoding="utf-8"))
            source_text = "\n\n".join(
                section["text"]
                for ch in book.get("chapters", [])
                for section in ch.get("sections", [])
            )
        except json.JSONDecodeError as e:
            print(f"warning: could not parse {args.source}: {e}", file=sys.stderr)
    skill_dirs = sorted(p for p in args.skills_dir.iterdir() if p.is_dir())
    results = []
    for d in skill_dirs:
        skill_md = d / "SKILL.md"
        if not skill_md.exists():
            continue
        results.append(check_skill(skill_md, source_text=source_text))
    summary = {
        "total_skills": len(results),
        "clean_skills": sum(1 for r in results if not r["problems"]),
        "skills_with_problems": sum(1 for r in results if r["problems"]),
        "details": results,
    }
    json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0 if summary["skills_with_problems"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())