#!/usr/bin/env python3
"""Convert The Minimalist Entrepreneur book CSV into chapter-organized markdown files."""

import csv
import os
import re
from pathlib import Path

# Table of contents: (start_page, end_page, slug, chapter_name, chapter_number)
TOC = [
    (1, 4, "front-matter", "Front Matter", 0),
    (5, 8, "introduction", "Introduction", 0),
    (9, 21, "ch01-the-minimalist-entrepreneur", "The Minimalist Entrepreneur", 1),
    (22, 48, "ch02-community-first", "Community First", 2),
    (49, 68, "ch03-build-manual-process", "Build a Manual Valuable Process First", 3),
    (69, 86, "ch04-sell-first-100", "Sell to Your First 100 Customers", 4),
    (87, 111, "ch05-market-by-being-you", "Market by Being You", 5),
    (112, 128, "ch06-grow-sustainably", "Grow Yourself and Your Business Sustainably", 6),
    (129, 145, "ch07-build-the-house", "Build the House You Want to Live In", 7),
    (146, 160, "ch08-where-do-we-go", "Where Do We Go from Here?", 8),
]


def page_to_chapter(page_num: int):
    """Return (slug, chapter_name, chapter_number) for a given page number."""
    for start, end, slug, name, num in TOC:
        if start <= page_num <= end:
            return slug, name, num
    return "unknown", "Unknown", -1


def main():
    csv_path = "/tmp/minimalist-entrepreneur-book.csv"
    out_dir = Path("/tmp/danm72-skills/data/book")

    # Track counts per chapter
    chapter_counts = {}

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            title = row["title"].strip()
            content = row["content"].strip()
            tokens = int(row["tokens"].strip())

            # Extract page number from title like "Page 42"
            match = re.match(r"Page\s+(\d+)", title)
            if not match:
                print(f"WARNING: Skipping row with unexpected title: {title}")
                continue
            page_num = int(match.group(1))

            slug, chapter_name, chapter_number = page_to_chapter(page_num)

            # Create chapter directory
            chapter_dir = out_dir / slug
            chapter_dir.mkdir(parents=True, exist_ok=True)

            # Build frontmatter
            frontmatter = f"""---
title: "Page {page_num}"
chapter: "{chapter_name}"
chapter_number: {chapter_number}
page: {page_num}
tokens: {tokens}
---"""

            # Write file
            filename = f"page-{page_num:03d}.md"
            filepath = chapter_dir / filename
            filepath.write_text(f"{frontmatter}\n\n{content}\n", encoding="utf-8")

            # Track counts
            chapter_counts[slug] = chapter_counts.get(slug, 0) + 1

    # Print summary
    total = 0
    print("Pages converted per chapter:")
    print("-" * 55)
    for _, _, slug, name, num in TOC:
        count = chapter_counts.get(slug, 0)
        total += count
        label = f"Ch {num}: {name}" if num > 0 else name
        print(f"  {label:<45} {count:>3} pages")
    print("-" * 55)
    print(f"  {'TOTAL':<45} {total:>3} pages")


if __name__ == "__main__":
    main()
