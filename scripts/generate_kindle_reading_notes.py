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
PICK_PATTERN = re.compile(r"^%%\s*pick\s*%%$", re.IGNORECASE)
GROUP_PATTERN = re.compile(r"^%%\s*group:\s*(?P<group>.+?)\s*%%$", re.IGNORECASE)
TITLE_PATTERN = re.compile(r"^%%\s*title:\s*(?P<title>.+?)\s*%%$", re.IGNORECASE)


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
    picked: bool
    group_id: Optional[str]
    group_title: Optional[str]


@dataclass
class PendingMetadata:
    group_id: Optional[str] = None
    group_title: Optional[str] = None


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
    pending = PendingMetadata()
    for chunk in chunks:
        lines = [line.rstrip() for line in chunk.splitlines()]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and lines[-1].strip() in {"", "---"}:
            lines.pop()
        if not lines:
            continue

        match = HIGHLIGHT_PATTERN.match(lines[0])
        pick = any(PICK_PATTERN.match(line.strip()) for line in lines)
        group_matches = [
            GROUP_PATTERN.match(line.strip())
            for line in lines
            if GROUP_PATTERN.match(line.strip())
        ]
        title_matches = [
            TITLE_PATTERN.match(line.strip())
            for line in lines
            if TITLE_PATTERN.match(line.strip())
        ]

        if not match:
            if group_matches:
                pending.group_id = group_matches[-1].group("group").strip()
            if title_matches:
                pending.group_title = title_matches[-1].group("title").strip()
            continue

        group_id = (
            group_matches[-1].group("group").strip()
            if group_matches
            else pending.group_id
        )
        group_title = (
            title_matches[-1].group("title").strip()
            if title_matches
            else pending.group_title
        )

        memo_lines = [
            line
            for line in lines[1:]
            if line.strip()
            and line.strip() != "---"
            and not PICK_PATTERN.match(line.strip())
            and not GROUP_PATTERN.match(line.strip())
            and not TITLE_PATTERN.match(line.strip())
        ]
        memo = "\n".join(memo_lines).strip()
        highlights.append(
            Highlight(
                quote=match.group("quote").strip(),
                location=int(match.group("location")),
                kindle_link=match.group("link").strip(),
                highlight_id=match.group("ref").strip(),
                memo=memo,
                picked=pick,
                group_id=group_id,
                group_title=group_title,
            )
        )
        pending = PendingMetadata()

    return highlights


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[/:*?\"<>|]", "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def build_heading(quote: str, limit: int = 32) -> str:
    compact = re.sub(r"\s+", " ", quote).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def normalize_title_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    value = value.strip(" 　-")
    return value


def summarize_pick_title(highlight: Highlight) -> str:
    if highlight.memo:
        first_line = normalize_title_text(highlight.memo.splitlines()[0])
        if first_line:
            return first_line

    quote = normalize_title_text(highlight.quote)
    for token in ["。", "！", "？", "—"]:
        if token in quote:
            quote = quote.split(token, 1)[0]
            break
    if len(quote) > 26:
        quote = quote[:25].rstrip() + "…"
    return quote or highlight.highlight_id


def build_filename(highlight: Highlight) -> str:
    title = summarize_pick_title(highlight)
    return sanitize_filename(f"{title}__{highlight.highlight_id}.md")


def build_group_filename(group_id: str, highlights: List[Highlight]) -> str:
    title = next((normalize_title_text(h.group_title or "") for h in highlights if h.group_title), "")
    if not title:
        title = summarize_pick_title(highlights[0])
    return sanitize_filename(f"{title}__group-{group_id}.md")


def format_list_block(items: Iterable[str], indent: str = "  ") -> str:
    rows = [f"{indent}- {yaml_quote(item)}" for item in items]
    return "\n".join(rows) if rows else f"{indent}- {yaml_quote('')}"


def build_source_link(book: BookMeta) -> str:
    return f"[[{book.path.with_suffix('').as_posix()}]]"


def render_note(book: BookMeta, highlight: Highlight) -> str:
    heading = summarize_pick_title(highlight)
    source_link = build_source_link(book)
    lines = [
        "---",
        "type: reading-note",
        "source_type: kindle",
        f"source_container: {yaml_quote(source_link)}",
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
            f"- ![[{book.path.with_suffix('').as_posix()}#^{highlight.highlight_id}]]",
            "",
        ]
    )
    return "\n".join(lines)


def render_group_note(book: BookMeta, group_id: str, highlights: List[Highlight]) -> str:
    source_link = build_source_link(book)
    title = next((normalize_title_text(h.group_title or "") for h in highlights if h.group_title), "")
    if not title:
        title = summarize_pick_title(highlights[0])
    memo_parts = [h.memo for h in highlights if h.memo]
    link_lines = [
        f"- ![[{book.path.with_suffix('').as_posix()}#^{h.highlight_id}]]" for h in highlights
    ]
    body_quotes = []
    for h in highlights:
        body_quotes.append(f"> {h.quote}")
        body_quotes.append("")

    lines = [
        "---",
        "type: reading-note",
        "source_type: kindle",
        f"source_container: {yaml_quote(source_link)}",
        f"source_book: {yaml_quote(source_link)}",
        f"book_title: {yaml_quote(book.title)}",
        "book_author:",
        format_list_block(book.authors),
        f"source_asin: {yaml_quote(book.asin)}",
        f"group_key: {yaml_quote(group_id)}",
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
        f"# {title}",
        "",
    ]
    lines.extend(body_quotes)
    lines.extend(
        [
            f"出典: {source_link}",
            "",
            "## Memo",
        ]
    )
    if memo_parts:
        for idx, memo in enumerate(memo_parts, start=1):
            if len(memo_parts) > 1:
                lines.append(f"### Memo {idx}")
            lines.extend(memo.splitlines())
            lines.append("")
    else:
        lines.append("")
    lines.extend(
        [
            "## My Take",
            "",
            "## Links",
            *link_lines,
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
        description="Generate reading notes from flagged Kindle import notes."
    )
    parser.add_argument(
        "--source",
        default="400_Kindle",
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
    created = 0
    skipped = 0
    parse_failures = 0

    for source_path in sorted(source_dir.glob("*.md")):
        if book_filters and not any(token in source_path.name for token in book_filters):
            continue

        book = parse_book(source_path)
        highlights = parse_highlights(source_path)

        grouped: dict[str, List[Highlight]] = {}
        singles: List[Highlight] = []
        for highlight in highlights:
            if highlight.group_id:
                grouped.setdefault(highlight.group_id, []).append(highlight)
            elif highlight.picked:
                singles.append(highlight)

        for highlight in singles:
            filename = build_filename(highlight)
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

            created += 1
            if args.limit and created >= args.limit:
                print(f"created={created} skipped={skipped} parse_failures={parse_failures}")
                return 0

        for group_id, members in grouped.items():
            filename = build_group_filename(group_id, members)
            target_path = dest_dir / filename
            if target_path.exists() and not args.overwrite:
                skipped += 1
                continue

            note = render_group_note(book, group_id, members)
            if not note.strip():
                parse_failures += 1
                continue

            if args.dry_run:
                print(target_path)
            else:
                target_path.write_text(note, encoding="utf-8")

            created += 1
            if args.limit and created >= args.limit:
                print(f"created={created} skipped={skipped} parse_failures={parse_failures}")
                return 0

    print(f"created={created} skipped={skipped} parse_failures={parse_failures}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
