#!/usr/bin/env python3
"""Diff an extracted book JSON against a target skill repo.

Reads the JSON output of `extract_chapters.py` and walks the target
repo's `skills/*/SKILL.md` files. For each skill, produces:
  - primary chapter (which chapter of the book it best matches)
  - support level: DIRECT / SYNTHESIS / EXTERNAL / CONFLICT
  - issues: any detected mismatches with the book

Matching is heuristic: word-overlap scoring between the skill body
and each chapter's section text. The score is keyword frequency
without stemming; good enough as a first pass, not authoritative.

Outputs JSON to stdout.

Usage:
  python3 diff_against_repo.py book.json /path/to/skill-repo
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path


STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
    "in", "on", "at", "of", "for", "to", "from", "with", "by", "as",
    "this", "that", "these", "those", "be", "been", "being",
    "it", "its", "you", "your", "their", "they", "them", "we", "our",
    "i", "me", "my", "he", "she", "his", "her",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "should", "could", "can", "may", "might", "must",
    "if", "then", "else", "than", "so", "very", "more", "less",
    "not", "no", "yes",
    "what", "which", "who", "whom", "how", "why", "when", "where",
    "any", "all", "some", "many", "much", "few",
    "use", "using", "used", "make", "makes", "made",
    "skill", "skills",
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
}


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"[a-zA-Z]{3,}", text)]


def _chapter_signature(chapter: dict) -> Counter:
    sig: Counter = Counter()
    for section in chapter["sections"]:
        sig.update(_tokens(section["text"]))
    sig = Counter({k: v for k, v in sig.items() if k not in STOPWORDS})
    return sig


def _skill_signature(skill_text: str) -> Counter:
    sig: Counter = Counter(_tokens(skill_text))
    sig = Counter({k: v for k, v in sig.items() if k not in STOPWORDS})
    return sig


def _overlap(a: Counter, b: Counter) -> float:
    """Symmetric overlap coefficient."""
    if not a or not b:
        return 0.0
    common = sum((a & b).values())
    return common / min(sum(a.values()), sum(b.values()))


def _detect_conflicts(skill_text: str, book_text: str) -> list[str]:
    """Heuristic conflict detection: look for negation patterns that disagree."""
    issues = []
    # Find sentences in skill that contain 'not', 'no', 'never', 'don\'t'
    for sent in re.split(r"(?<=[.!?])\s+", skill_text):
        low = sent.lower()
        if any(neg in low for neg in (" not ", " no ", " never ", "don't ", "do not ")):
            # Search for the same subject in the book without negation
            head = re.match(r"^(.{3,60})", low)
            if not head:
                continue
            fragment = head.group(1).strip()
            if not fragment or len(fragment) < 8:
                continue
            # Look in book for similar fragment without a negation
            for bsent in re.split(r"(?<=[.!?])\s+", book_text):
                blow = bsent.lower()
                if fragment in blow and not any(neg in blow for neg in (" not ", " no ", " never ")):
                    issues.append(
                        f"possible conflict: skill says '{sent.strip()[:120]}' "
                        f"but book says '{bsent.strip()[:120]}'"
                    )
                    break
    return issues[:5]


def diff(book: dict, repo_path: Path) -> dict:
    skills_dir = repo_path / "skills"
    if not skills_dir.exists():
        print(f"error: no skills/ directory in {repo_path}", file=sys.stderr)
        sys.exit(1)

    chapter_sigs = [_chapter_signature(ch) for ch in book["chapters"]]
    chapter_text = "\n\n".join(
        section["text"]
        for ch in book["chapters"]
        for section in ch["sections"]
    )

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    results = []
    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text(encoding="utf-8", errors="ignore")
        sig = _skill_signature(text)
        scores = [_overlap(sig, cs) for cs in chapter_sigs]
        if max(scores, default=0) == 0:
            primary = None
            secondary = []
            support = "EXTERNAL"
        else:
            ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
            primary_idx, primary_score = ranked[0]
            primary = book["chapters"][primary_idx]["title"]
            secondary = [
                book["chapters"][idx]["title"]
                for idx, score in ranked[1:3]
                if score > 0.05
            ]
            if primary_score > 0.15:
                support = "DIRECT"
            elif primary_score > 0.05:
                support = "SYNTHESIS"
            else:
                support = "EXTERNAL"
        # Detect fabricated numeric thresholds (skill contains "10+", "100 ",
        # etc., that are unlikely to appear in the book verbatim)
        threshold_patterns = [
            r"\b10\+?\s+(?:paying|customers|users|people|interviews)\b",
            r"\b3\s+(?:of\s+(?:10|the)|people\s+who)\b",
            r"\b100\s+(?:paying|customers)\b",
            r"\b20[\u2013-]50\s*%",
        ]
        fabricated = []
        for pat in threshold_patterns:
            if re.search(pat, text, re.I):
                if not re.search(pat, chapter_text, re.I):
                    fabricated.append(pat)
        issues = _detect_conflicts(text, chapter_text)
        if fabricated:
            issues.append(
                "fabricated thresholds (not in book): " + ", ".join(fabricated)
            )
        if support == "EXTERNAL" and primary is None:
            primary_label = "(no chapter match)"
        elif primary is not None:
            primary_label = primary
        else:
            primary_label = ""
        results.append(
            {
                "skill": skill_dir.name,
                "primary_chapter": primary_label,
                "secondary_chapters": secondary,
                "support_level": support,
                "issues": issues,
            }
        )
    return {
        "book": {"title": book.get("title", ""), "author": book.get("author", "")},
        "repo": str(repo_path),
        "skills": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Diff extracted book JSON against a target skill repo"
    )
    parser.add_argument("book_json", type=Path, help="path to book JSON from extract_chapters.py")
    parser.add_argument("repo", type=Path, help="path to target skill repo (with skills/ dir)")
    args = parser.parse_args()
    if not args.book_json.exists():
        print(f"error: book JSON not found: {args.book_json}", file=sys.stderr)
        return 1
    if not args.repo.exists():
        print(f"error: repo not found: {args.repo}", file=sys.stderr)
        return 1
    book = json.loads(args.book_json.read_text(encoding="utf-8"))
    result = diff(book, args.repo)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())