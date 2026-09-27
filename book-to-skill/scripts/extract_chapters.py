#!/usr/bin/env python3
"""Extract chapter structure from a book file.

Supported formats:
- EPUB: extracts xhtml files via zipfile + HTMLParser, groups by spine order
- Markdown: parses ATX headers (#, ##, ###) as chapters / sections
- PDF: warns about limited fidelity; uses page text if pdfplumber or pypdf is available, else skips

Output: JSON to stdout with shape:
{
  "title": "...",
  "author": "...",
  "chapters": [
    {"index": 1, "title": "...", "is_intro": false,
     "sections": [{"title": "...", "text": "...", "char_count": 1234}]}
  ]
}

Usage:
  python3 extract_chapters.py <path-to-book>
  python3 extract_chapters.py <path-to-book> > book.json
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path


# ---------- EPUB ----------

class XhtmlToSections(HTMLParser):
    """Walk an xhtml file, capture h1/h2/h3 headings and the text blocks that follow each heading."""

    def __init__(self):
        super().__init__()
        self.sections: list[dict] = []
        self.current_section: dict | None = None
        self.current_tag: str | None = None
        self.skip_depth = 0
        self.buffer: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in ("h1", "h2", "h3"):
            self.current_tag = tag
            self.buffer = []
            return
        if tag in ("p", "li", "blockquote"):
            self.buffer.append("")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip_depth:
            self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag in ("h1", "h2", "h3") and self.current_tag == tag:
            title = _normalize("".join(self.buffer))
            if title:
                self.sections.append({"title": title, "text": "", "char_count": 0})
                self.current_section = self.sections[-1]
            self.current_tag = None
            self.buffer = []
            return

    def handle_data(self, data):
        if self.skip_depth:
            return
        text = data.strip()
        if not text:
            return
        if self.current_tag in ("h1", "h2", "h3"):
            self.buffer.append(text)
        elif self.current_section is not None:
            self.current_section["text"] += text + " "

    def finalize(self):
        for section in self.sections:
            cleaned = _normalize(section["text"])
            section["text"] = cleaned
            section["char_count"] = len(cleaned)


def _normalize(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip()
    return html.unescape(s)


def _read_spine_order(zf: zipfile.ZipFile) -> list[str]:
    """Parse OPF spine to get reading order. Falls back to filename sort."""
    opf_names = [n for n in zf.namelist() if n.lower().endswith(".opf") and "META-INF" not in n]
    if not opf_names:
        return []
    opf_raw = zf.read(opf_names[0]).decode("utf-8", errors="ignore")
    spine_matches = re.findall(r'<itemref[^>]*idref="([^"]+)"', opf_raw)
    item_map = {}
    for m in re.finditer(r'<item[^>]*id="([^"]+)"[^>]*href="([^"]+)"', opf_raw):
        item_map[m.group(1)] = m.group(2)
    ordered = []
    for ref in spine_matches:
        href = item_map.get(ref)
        if href:
            ordered.append(href)
    return ordered


def _extract_epub_metadata(zf: zipfile.ZipFile) -> tuple[str, str]:
    """Pull title and creator from the OPF metadata block."""
    opf_names = [n for n in zf.namelist() if n.lower().endswith(".opf") and "META-INF" not in n]
    if not opf_names:
        return "", ""
    opf_raw = zf.read(opf_names[0]).decode("utf-8", errors="ignore")
    title_m = re.search(r"<dc:title[^>]*>(.*?)</dc:title>", opf_raw, re.S)
    creator_m = re.search(r"<dc:creator[^>]*>(.*?)</dc:creator>", opf_raw, re.S)
    title = _normalize(title_m.group(1)) if title_m else ""
    creator = _normalize(creator_m.group(1)) if creator_m else ""
    return title, creator


def _is_front_matter(path: str, title: str) -> bool:
    """Heuristic: skip nav, copyright, index pages and any chapter under ~300 chars."""
    basename = os.path.basename(path).lower()
    if any(
        kw in basename
        for kw in ("nav", "toc", "contents", "copyright", "title_page", "cover", "colophon", "index")
    ):
        return True
    low_title = title.lower()
    if any(kw in low_title for kw in ("contents", "copyright", "title page", "cover", "landmarks", "print page list", "about the author")):
        return True
    return False


def extract_epub(path: Path) -> dict:
    chapters: list[dict] = []
    with zipfile.ZipFile(path) as zf:
        title, author = _extract_epub_metadata(zf)
        spine_hrefs = _read_spine_order(zf)
        # Build map of all xhtml by basename
        xhtml_files = {
            os.path.basename(n): n
            for n in zf.namelist()
            if n.lower().endswith((".xhtml", ".html", ".htm"))
        }
        # Resolve spine relative to opf directory
        opf_dir = ""
        opf_match = next(
            (n for n in zf.namelist() if n.lower().endswith(".opf") and "META-INF" not in n),
            None,
        )
        if opf_match:
            opf_dir = os.path.dirname(opf_match)

        seen = set()
        ordered_names: list[str] = []
        for href in spine_hrefs:
            resolved = os.path.normpath(os.path.join(opf_dir, href))
            # Try both the resolved path and the basename
            candidates = [resolved, os.path.basename(href)]
            for cand in candidates:
                full = next((full for full in xhtml_files.values() if full.endswith(cand)), None)
                if full and full not in seen:
                    ordered_names.append(full)
                    seen.add(full)
                    break
        # Append any xhtml files not in spine (copyright page, etc.)
        for full in sorted(xhtml_files.values()):
            if full not in seen:
                ordered_names.append(full)
                seen.add(full)

        next_index = 0
        for name in ordered_names:
            raw = zf.read(name).decode("utf-8", errors="ignore")
            parser = XhtmlToSections()
            parser.feed(raw)
            parser.finalize()
            if not parser.sections:
                continue
            chapter_title = parser.sections[0]["title"] or os.path.basename(name)
            sections = [s for s in parser.sections[1:] if s["char_count"] > 0]
            if parser.sections[0]["char_count"] > 0:
                first_body = {
                    "title": "(intro)",
                    "text": parser.sections[0]["text"],
                    "char_count": parser.sections[0]["char_count"],
                }
                sections = [first_body] + sections
            total_chars = sum(s["char_count"] for s in sections)
            if _is_front_matter(name, chapter_title) or total_chars < 300:
                continue
            next_index += 1
            is_intro = next_index == 1 and any(
                kw in chapter_title.lower() for kw in ("intro", "foreword", "preface")
            )
            chapters.append(
                {
                    "index": next_index,
                    "title": chapter_title,
                    "is_intro": is_intro,
                    "sections": sections,
                }
            )
    return {"title": title, "author": author, "chapters": chapters}


# ---------- Markdown ----------

MD_HEADER = re.compile(r"^(#{1,3})\s+(.+)$", re.M)


def extract_markdown(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    title = ""
    author = ""
    # Look for frontmatter
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            fm = raw[3:end]
            for line in fm.splitlines():
                if line.lower().startswith("title:"):
                    title = line.split(":", 1)[1].strip().strip('"')
                elif line.lower().startswith("author:"):
                    author = line.split(":", 1)[1].strip().strip('"')
            raw = raw[end + 4:]

    matches = list(MD_HEADER.finditer(raw))
    chapters: list[dict] = []
    for i, m in enumerate(matches):
        level = len(m.group(1))
        title_text = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        body = raw[start:end].strip()
        section_text = _normalize(body)
        chapter = {
            "index": len(chapters) + 1,
            "title": title_text,
            "is_intro": level == 1 and i == 0,
            "sections": [
                {
                    "title": "(body)",
                    "text": section_text,
                    "char_count": len(section_text),
                }
            ],
        }
        chapters.append(chapter)
    if not title and chapters:
        title = chapters[0]["title"]
    return {"title": title, "author": author, "chapters": chapters}


# ---------- PDF (best-effort) ----------

def extract_pdf(path: Path) -> dict:
    text = ""
    try:
        import pypdf  # type: ignore

        reader = pypdf.PdfReader(str(path))
        text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    except ImportError:
        try:
            import pdfplumber  # type: ignore

            with pdfplumber.open(str(path)) as pdf:
                text = "\n\n".join(page.extract_text() or "" for page in pdf.pages)
        except ImportError:
            print(
                "warning: PDF support requires pypdf or pdfplumber; install one and rerun.",
                file=sys.stderr,
            )
            return {"title": path.stem, "author": "", "chapters": []}
    # Best-effort chapter detection: lines matching "Chapter N" or numeric headings
    chapters: list[dict] = []
    chapter_re = re.compile(r"^(Chapter\s+\d+|[0-9]+\.[0-9]*\s+.+)$", re.M)
    matches = list(chapter_re.finditer(text))
    if not matches:
        chapters.append(
            {
                "index": 1,
                "title": path.stem,
                "is_intro": False,
                "sections": [
                    {
                        "title": "(full text)",
                        "text": _normalize(text),
                        "char_count": len(text),
                    }
                ],
            }
        )
    else:
        for i, m in enumerate(matches):
            title_text = m.group(0).strip()
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            body = _normalize(text[start:end])
            chapters.append(
                {
                    "index": len(chapters) + 1,
                    "title": title_text,
                    "is_intro": False,
                    "sections": [
                        {"title": "(body)", "text": body, "char_count": len(body)}
                    ],
                }
            )
    return {"title": path.stem, "author": "", "chapters": chapters}


# ---------- Entry point ----------


def extract(path: Path) -> dict:
    suffix = path.suffix.lower()
    if suffix == ".epub":
        return extract_epub(path)
    if suffix in (".md", ".markdown"):
        return extract_markdown(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    raise ValueError(f"unsupported file type: {suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract chapter structure from a book file")
    parser.add_argument("path", type=Path, help="path to EPUB, Markdown, or PDF file")
    parser.add_argument(
        "--max-chars-per-section",
        type=int,
        default=0,
        help="truncate each section's text to this many chars (0 = no limit)",
    )
    args = parser.parse_args()
    if not args.path.exists():
        print(f"error: file not found: {args.path}", file=sys.stderr)
        return 1
    result = extract(args.path)
    if args.max_chars_per_section > 0:
        for chapter in result["chapters"]:
            for section in chapter["sections"]:
                if section["char_count"] > args.max_chars_per_section:
                    section["text"] = section["text"][: args.max_chars_per_section]
                    section["char_count"] = args.max_chars_per_section
                    section["truncated"] = True
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())