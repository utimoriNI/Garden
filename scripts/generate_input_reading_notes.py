#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional


FRONTMATTER_PATTERN = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
PICK_PATTERN = re.compile(r"^%%\s*pick\s*%%$", re.IGNORECASE)
GROUP_PATTERN = re.compile(r"^%%\s*group:\s*(?P<group>.+?)\s*%%$", re.IGNORECASE)
TITLE_PATTERN = re.compile(r"^%%\s*title:\s*(?P<title>.+?)\s*%%$", re.IGNORECASE)
MARKER_LINE_PATTERN = re.compile(r"^%%\s*(?:pick|group:\s*.+?|title:\s*.+?)\s*%%$", re.IGNORECASE)


@dataclass
class SourceMeta:
    path: Path
    title: str
    source_url: str
    authors: list[str]
    source_type: str


@dataclass
class CandidateBlock:
    content: str
    picked: bool
    group_id: Optional[str]
    explicit_title: Optional[str]


def extract_frontmatter(text: str) -> tuple[str, str]:
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def extract_frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def extract_authors(frontmatter: str) -> list[str]:
    match = re.search(r"^author:\s*\n((?:\s+- .+\n?)*)", frontmatter, re.MULTILINE)
    if match:
        authors = []
        for line in match.group(1).splitlines():
            if not line.strip().startswith("- "):
                continue
            value = line.split("- ", 1)[1].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
                value = value[1:-1]
            authors.append(value)
        if authors:
            return authors

    single = extract_frontmatter_value(frontmatter, "author")
    if single:
        return [single]
    return []


def infer_source_type(source_url: str) -> str:
    lowered = source_url.lower()
    if "youtube.com" in lowered or "youtu.be" in lowered:
        return "video"
    return "web"


def parse_source(path: Path) -> SourceMeta:
    text = path.read_text(encoding="utf-8")
    frontmatter, _ = extract_frontmatter(text)
    title = extract_frontmatter_value(frontmatter, "title") or path.stem
    source_url = extract_frontmatter_value(frontmatter, "source")
    authors = extract_authors(frontmatter)
    return SourceMeta(
        path=path,
        title=title,
        source_url=source_url,
        authors=authors,
        source_type=infer_source_type(source_url),
    )


def split_blocks(body: str) -> list[str]:
    return [block.strip("\n") for block in re.split(r"\n\s*\n", body) if block.strip()]


def marker_block_metadata(block: str) -> Optional[tuple[bool, Optional[str], Optional[str]]]:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    if not lines or not all(MARKER_LINE_PATTERN.match(line) for line in lines):
        return None

    picked = any(PICK_PATTERN.match(line) for line in lines)
    group_id = None
    explicit_title = None
    for line in lines:
        group_match = GROUP_PATTERN.match(line)
        if group_match:
            group_id = group_match.group("group").strip()
        title_match = TITLE_PATTERN.match(line)
        if title_match:
            explicit_title = normalize_title_text(title_match.group("title"))
    return picked, group_id, explicit_title


def extract_candidates(path: Path) -> list[CandidateBlock]:
    text = path.read_text(encoding="utf-8")
    _, body = extract_frontmatter(text)
    blocks = split_blocks(body)

    results: list[CandidateBlock] = []
    previous_content: Optional[str] = None
    for block in blocks:
        metadata = marker_block_metadata(block)
        if metadata:
            if previous_content is None:
                continue
            picked, group_id, explicit_title = metadata
            results.append(
                CandidateBlock(
                    content=previous_content.strip(),
                    picked=picked,
                    group_id=group_id,
                    explicit_title=explicit_title,
                )
            )
            previous_content = None
            continue

        previous_content = block

    return results


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def format_list_block(items: Iterable[str], indent: str = "  ") -> str:
    rows = [f"{indent}- {yaml_quote(item)}" for item in items]
    return "\n".join(rows) if rows else f"{indent}- {yaml_quote('')}"


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[/:*?\"<>|]", "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def normalize_title_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value.strip(" 　-")


def content_title(content: str) -> str:
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith(">"):
            line = line.lstrip(">").strip()
        if line.startswith("[") and "](" in line:
            continue
        return normalize_title_text(line)
    return ""


def resolve_title(block: CandidateBlock) -> str:
    if block.explicit_title:
        return block.explicit_title

    title = content_title(block.content)
    for token in ["。", "！", "？", "—"]:
        if token in title:
            title = title.split(token, 1)[0]
            break
    if len(title) > 30:
        title = title[:29].rstrip() + "…"
    return title or "Untitled Reading Note"


def ensure_unique_path(target_path: Path) -> Path:
    if not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    counter = 2
    while True:
        candidate = target_path.with_name(f"{stem} {counter}{suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def build_source_link(path: Path) -> str:
    return f"[[{path.with_suffix('').as_posix()}]]"


def render_note(meta: SourceMeta, block: CandidateBlock) -> str:
    heading = resolve_title(block)
    source_link = build_source_link(meta.path)
    lines = [
        "---",
        "type: reading-note",
        f"source_type: {meta.source_type}",
        f"source_container: {yaml_quote(source_link)}",
        f"source_title: {yaml_quote(meta.title)}",
    ]

    if meta.authors:
        lines.extend(["source_author:", format_list_block(meta.authors)])
    else:
        lines.append("source_author: []")

    if meta.source_url:
        lines.append(f"source_url: {yaml_quote(meta.source_url)}")

    lines.extend(
        [
            "topic: []",
            "moc: []",
            "status: inbox",
            "---",
            "",
            f"# {heading}",
            "",
            "## Fragment",
            "",
            block.content,
            "",
            f"出典: {source_link}",
        ]
    )

    if meta.source_url:
        lines.append(f"URL: {meta.source_url}")

    lines.extend(
        [
            "",
            "## Memo",
            "",
            "## My Take",
            "",
            "## Links",
            f"- {source_link}",
            "",
        ]
    )
    return "\n".join(lines)


def render_group_note(meta: SourceMeta, group_id: str, blocks: list[CandidateBlock]) -> str:
    source_link = build_source_link(meta.path)
    title = next((resolve_title(block) for block in blocks if block.explicit_title), "") or resolve_title(blocks[0])
    lines = [
        "---",
        "type: reading-note",
        f"source_type: {meta.source_type}",
        f"source_container: {yaml_quote(source_link)}",
        f"source_title: {yaml_quote(meta.title)}",
    ]
    if meta.authors:
        lines.extend(["source_author:", format_list_block(meta.authors)])
    else:
        lines.append("source_author: []")
    if meta.source_url:
        lines.append(f"source_url: {yaml_quote(meta.source_url)}")
    lines.extend(
        [
            f"group_key: {yaml_quote(group_id)}",
            "topic: []",
            "moc: []",
            "status: inbox",
            "---",
            "",
            f"# {title}",
            "",
            "## Fragment",
            "",
        ]
    )

    for idx, block in enumerate(blocks, start=1):
        if len(blocks) > 1:
            lines.append(f"### Fragment {idx}")
        lines.extend(block.content.splitlines())
        lines.append("")

    lines.extend(
        [
            f"出典: {source_link}",
        ]
    )
    if meta.source_url:
        lines.append(f"URL: {meta.source_url}")
    lines.extend(
        [
            "",
            "## Memo",
            "",
            "## My Take",
            "",
            "## Links",
            f"- {source_link}",
            "",
        ]
    )
    return "\n".join(lines)


def cleanup_markers(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    filtered = [line for line in lines if not MARKER_LINE_PATTERN.match(line.strip())]
    new_text = "\n".join(filtered)
    if text.endswith("\n"):
        new_text += "\n"
    new_text = re.sub(r"\n{3,}", "\n\n", new_text)
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate reading notes from %% pick %% / %% group %% markers in 300_Input notes."
    )
    parser.add_argument("--source", default="300_Input", help="Folder that contains input source notes.")
    parser.add_argument("--dest", default="300_Input/Reading Notes", help="Destination folder.")
    parser.add_argument("--dry-run", action="store_true", help="Print summary without writing files.")
    parser.add_argument("--limit", type=int, default=0, help="Stop after generating this many notes. 0 means no limit.")
    args = parser.parse_args()

    source_dir = Path(args.source)
    dest_dir = Path(args.dest)
    dest_dir.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0
    cleaned = 0

    for path in sorted(source_dir.rglob("*.md")):
        if path.parent == dest_dir:
            continue
        candidates = extract_candidates(path)
        if not candidates:
            continue

        meta = parse_source(path)
        singles = [block for block in candidates if block.picked and not block.group_id]
        groups: dict[str, list[CandidateBlock]] = {}
        for block in candidates:
            if block.group_id:
                groups.setdefault(block.group_id, []).append(block)

        wrote_for_path = False

        for block in singles:
            if args.limit and created >= args.limit:
                skipped += 1
                continue
            filename = sanitize_filename(f"{resolve_title(block)}.md")
            target_path = ensure_unique_path(dest_dir / filename)
            if args.dry_run:
                print(target_path.as_posix())
            else:
                target_path.write_text(render_note(meta, block), encoding="utf-8")
            created += 1
            wrote_for_path = True

        for group_id, group_blocks in groups.items():
            if args.limit and created >= args.limit:
                skipped += 1
                continue
            filename = sanitize_filename(f"{resolve_title(group_blocks[0])}.md")
            target_path = ensure_unique_path(dest_dir / filename)
            if args.dry_run:
                print(target_path.as_posix())
            else:
                target_path.write_text(render_group_note(meta, group_id, group_blocks), encoding="utf-8")
            created += 1
            wrote_for_path = True

        if wrote_for_path and not args.dry_run:
            if cleanup_markers(path):
                cleaned += 1

    print(f"created={created} skipped={skipped} cleaned={cleaned}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
