#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional


HIGHLIGHT_PATTERN = re.compile(
    r"^(?P<quote>.+?)\s+— location: \[(?P<location>\d+)\]\((?P<link>[^)]*)\) \^(?P<ref>ref-\d+)\s*$"
)
FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class BookMeta:
    note_name: str
    title: str
    author_raw: str
    authors: List[str]
    asin: str
    path: Path


@dataclass
class Highlight:
    quote: str
    location: int
    kindle_link: str
    highlight_id: str
    memo: str


def extract_frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def split_authors(author_raw: str) -> List[str]:
    normalized = author_raw.replace(" and ", ", ")
    parts = re.split(r"[、,，]", normalized)
    return [part.strip() for part in parts if part.strip()]


def parse_book(path: Path) -> BookMeta:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise ValueError(f"frontmatter not found: {path}")

    frontmatter = match.group(1)
    title = extract_frontmatter_value(frontmatter, "title") or path.stem
    author_raw = extract_frontmatter_value(frontmatter, "author")
    asin = extract_frontmatter_value(frontmatter, "asin")

    return BookMeta(
        note_name=path.stem,
        title=clean_book_title(title),
        author_raw=author_raw,
        authors=split_authors(author_raw),
        asin=asin,
        path=path,
    )


def clean_book_title(title: str) -> str:
    return re.sub(r"\s+\([^)]*\)$", "", title).strip()


def parse_highlights(path: Path) -> List[Highlight]:
    text = path.read_text(encoding="utf-8")
    if "## Highlights" not in text:
        return []

    body = text.split("## Highlights", 1)[1].strip()
    chunks = [chunk.strip() for chunk in re.split(r"\n\s*---\s*\n", body) if chunk.strip()]

    highlights: List[Highlight] = []
    for chunk in chunks:
        lines = [line.rstrip() for line in chunk.splitlines()]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and lines[-1].strip() in {"", "---"}:
            lines.pop()
        if not lines:
            continue

        match = HIGHLIGHT_PATTERN.match(lines[0])
        if not match:
            continue

        memo_lines = [line for line in lines[1:] if line.strip() and line.strip() != "---"]
        memo = "\n".join(memo_lines).strip()
        highlights.append(
            Highlight(
                quote=match.group("quote").strip(),
                location=int(match.group("location")),
                kindle_link=match.group("link").strip(),
                highlight_id=match.group("ref").strip(),
                memo=memo,
            )
        )

    return highlights


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[/:*?\"<>|]", "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def build_filename(book: BookMeta, highlight: Highlight) -> str:
    return sanitize_filename(
        f"{book.note_name}__loc-{highlight.location}__{highlight.highlight_id}.md"
    )


def build_heading(quote: str, limit: int = 32) -> str:
    compact = re.sub(r"\s+", " ", quote).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def format_list_block(items: Iterable[str], indent: str = "  ") -> str:
    rows = [f"{indent}- {yaml_quote(item)}" for item in items]
    return "\n".join(rows) if rows else f"{indent}- {yaml_quote('')}"


def render_note(book: BookMeta, highlight: Highlight) -> str:
    heading = build_heading(highlight.quote)
    source_link = f"[[998_Resource/Kindle/{book.note_name}]]"
    lines = [
        "---",
        "type: reading-note",
        "source_type: kindle",
        f"source_book: {yaml_quote(source_link)}",
        f"book_title: {yaml_quote(book.title)}",
        "book_author:",
        format_list_block(book.authors),
        f"source_asin: {yaml_quote(book.asin)}",
        f"kindle_location: {highlight.location}",
        f"highlight_id: {yaml_quote(highlight.highlight_id)}",
        "topic: []",
        "concept: []",
        "use_case: []",
        "reaction: []",
        "status: inbox",
        "importance: 3",
        "review_score: 3",
        "reviewed: false",
        "review_due:",
        "moc: []",
        "---",
        "",
        f"# {heading}",
        "",
        f"> {highlight.quote}",
        "",
        f"出典: {source_link}",
        f"Kindle: [location {highlight.location}]({highlight.kindle_link})",
        "",
        "## Memo",
    ]

    if highlight.memo:
        lines.extend(highlight.memo.splitlines())
    else:
        lines.append("")

    lines.extend(
        [
            "",
            "## My Take",
            "",
            "## Links",
            f"- ![[998_Resource/Kindle/{book.note_name}#^{highlight.highlight_id}]]",
            "",
        ]
    )
    return "\n".join(lines)


def make_entry_key(asin: str, highlight_id: str) -> str:
    return f"{asin}::{highlight_id}"


def collect_existing_keys(dest_dir: Path) -> set[str]:
    keys = set()
    for path in dest_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        highlight_match = re.search(
            r"^highlight_id:\s*['\"]?(ref-\d+)['\"]?\s*$", text, re.MULTILINE
        )
        asin_match = re.search(r"^source_asin:\s*['\"]?(.+?)['\"]?\s*$", text, re.MULTILINE)
        if highlight_match and asin_match:
            keys.add(make_entry_key(asin_match.group(1), highlight_match.group(1)))
    return keys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate one-note-per-highlight reading notes from Kindle import notes."
    )
    parser.add_argument(
        "--source",
        default="998_Resource/Kindle",
        help="Folder that contains Kindle source notes.",
    )
    parser.add_argument(
        "--dest",
        default="200_Inbox/Reading Notes",
        help="Folder where generated reading notes will be written.",
    )
    parser.add_argument(
        "--book",
        action="append",
        default=[],
        help="Only process source notes whose filename contains this string. Repeatable.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Stop after generating this many notes. 0 means no limit.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files with the same generated filename.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print a summary without writing files.",
    )
    args = parser.parse_args()

    source_dir = Path(args.source)
    dest_dir = Path(args.dest)
    dest_dir.mkdir(parents=True, exist_ok=True)

    book_filters = args.book or []
    existing_keys = set() if args.overwrite else collect_existing_keys(dest_dir)
    created = 0
    skipped = 0
    parse_failures = 0

    for source_path in sorted(source_dir.glob("*.md")):
        if book_filters and not any(token in source_path.name for token in book_filters):
            continue

        book = parse_book(source_path)
        for highlight in parse_highlights(source_path):
            entry_key = make_entry_key(book.asin, highlight.highlight_id)
            if entry_key in existing_keys:
                skipped += 1
                continue

            filename = build_filename(book, highlight)
            target_path = dest_dir / filename
            if target_path.exists() and not args.overwrite:
                skipped += 1
                continue

            note = render_note(book, highlight)
            if not note.strip():
                parse_failures += 1
                continue

            if args.dry_run:
                print(target_path)
            else:
                target_path.write_text(note, encoding="utf-8")

            existing_keys.add(entry_key)
            created += 1

            if args.limit and created >= args.limit:
                print(f"created={created} skipped={skipped} parse_failures={parse_failures}")
                return 0

    print(f"created={created} skipped={skipped} parse_failures={parse_failures}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
