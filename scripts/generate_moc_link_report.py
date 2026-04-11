#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
READING_NOTE_PREFIX = "300_Input/Reading Notes/"


@dataclass
class NoteRecord:
    path: Path
    vault_path: str
    title: str
    tags: list[str]
    mocs: list[str]
    note_type: str
    body: str


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def split_frontmatter(text: str) -> tuple[list[str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return [], text
    return match.group(1).splitlines(), text[match.end() :]


def parse_list_block(lines: list[str], key: str) -> list[str]:
    result: list[str] = []
    in_block = False
    key_prefix = f"{key}:"
    inline_prefix = f"{key}: ["

    for line in lines:
        stripped = line.strip()
        if line.startswith(inline_prefix):
            inside = line[len(inline_prefix) :].rstrip("]").strip()
            if not inside:
                return []
            return [part.strip().strip("'\"") for part in inside.split(",") if part.strip()]

        if line.startswith(key_prefix):
            if stripped == key_prefix or stripped == f"{key}: []":
                in_block = True
                continue

        if in_block:
            if line.startswith("  - "):
                result.append(line[4:].strip().strip("'\""))
                continue
            break

    return result


def parse_scalar(lines: list[str], key: str) -> str:
    key_prefix = f"{key}:"
    for line in lines:
        if line.startswith(key_prefix):
            return line[len(key_prefix) :].strip().strip("'\"")
    return ""


def extract_title(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def load_note(path: Path, vault_root: Path) -> NoteRecord:
    text = path.read_text(encoding="utf-8")
    frontmatter_lines, body = split_frontmatter(text)
    return NoteRecord(
        path=path,
        vault_path=path.relative_to(vault_root).as_posix(),
        title=extract_title(path, body),
        tags=parse_list_block(frontmatter_lines, "tags"),
        mocs=parse_list_block(frontmatter_lines, "moc"),
        note_type=parse_scalar(frontmatter_lines, "type"),
        body=body,
    )


def extract_moc_links(moc_text: str) -> set[str]:
    links: set[str] = set()
    for raw_target in WIKILINK_RE.findall(moc_text):
        target = raw_target.split("|", 1)[0].strip()
        if target.startswith(READING_NOTE_PREFIX):
            links.add(target)
    return links


def match_keywords(text: str, keywords: list[str]) -> list[str]:
    matches: list[str] = []
    lowered = text.lower()
    for keyword in keywords:
        if keyword.lower() in lowered:
            matches.append(keyword)
    return matches


def suggest_section(text: str, section_hints: dict[str, list[str]]) -> str:
    best_section = ""
    best_score = 0
    lowered = text.lower()

    for section, keywords in section_hints.items():
        score = sum(1 for keyword in keywords if keyword.lower() in lowered)
        if score > best_score:
            best_section = section
            best_score = score

    return best_section or "要確認"


def build_report(config: dict, notes: list[NoteRecord], linked_notes: set[str], vault_root: Path) -> str:
    required_tags = config["required_tags"]
    keywords = config["keywords"]
    section_hints = config["section_hints"]
    moc_link = config["moc_path"]

    eligible = [
        note
        for note in notes
        if note.note_type == "reading-note" and all(tag in note.tags for tag in required_tags)
    ]

    already_linked = [note for note in eligible if note.vault_path in linked_notes]
    candidates = []

    for note in eligible:
        if note.vault_path in linked_notes:
            continue

        haystack = f"{note.title}\n{note.body}"
        matched_keywords = match_keywords(haystack, keywords)
        if not matched_keywords:
            continue

        score = len(set(matched_keywords))
        candidates.append(
            {
                "note": note,
                "score": score,
                "keywords": sorted(set(matched_keywords)),
                "section": suggest_section(haystack, section_hints),
                "already_has_moc": any("指標に回収される人間の価値_MOC" in moc for moc in note.mocs),
            }
        )

    candidates.sort(key=lambda item: (-item["score"], item["note"].title))

    represented_books = Counter()
    for note in already_linked:
        book_match = re.search(r"source_book:\s*'?\[\[([^\]]+)\]\]'?", split_frontmatter(note.path.read_text(encoding="utf-8"))[0] and note.path.read_text(encoding="utf-8"))
        if book_match:
            represented_books[book_match.group(1)] += 1

    lines: list[str] = []
    lines.append(f"# {config['name']} Link Report")
    lines.append("")
    lines.append(f"Created: {config['created']}")
    lines.append(f"Target MOC: [[{moc_link}]]")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Eligible `reading-note`: {len(eligible)}")
    lines.append(f"- Already linked in target MOC: {len(already_linked)}")
    lines.append(f"- New keyword-matched candidates: {len(candidates)}")
    lines.append("")
    lines.append("## Review Workflow")
    lines.append("")
    lines.append("1. Review `High priority candidates` first")
    lines.append("2. Approve only notes that genuinely sharpen this MOC")
    lines.append("3. After approval, add the note to the `moc` frontmatter and the MOC body")
    lines.append("")
    lines.append("## Already linked notes")
    lines.append("")
    for note in sorted(already_linked, key=lambda item: item.title):
        lines.append(f"- [[{note.vault_path}]]")
    lines.append("")
    lines.append("## High priority candidates")
    lines.append("")

    high = [item for item in candidates if item["score"] >= config["high_priority_score"]]
    if not high:
        lines.append("- None")
    else:
        for item in high:
            note = item["note"]
            keyword_str = ", ".join(item["keywords"])
            lines.append(f"- [[{note.vault_path}]]")
            lines.append(f"  - score: {item['score']}")
            lines.append(f"  - suggested section: {item['section']}")
            lines.append(f"  - matched keywords: {keyword_str}")
            if item["already_has_moc"]:
                lines.append("  - note: frontmatter already points to this MOC candidate")
    lines.append("")
    lines.append("## Medium priority candidates")
    lines.append("")

    medium = [item for item in candidates if item["score"] < config["high_priority_score"]]
    if not medium:
        lines.append("- None")
    else:
        for item in medium:
            note = item["note"]
            keyword_str = ", ".join(item["keywords"])
            lines.append(f"- [[{note.vault_path}]]")
            lines.append(f"  - score: {item['score']}")
            lines.append(f"  - suggested section: {item['section']}")
            lines.append(f"  - matched keywords: {keyword_str}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- This report is a suggestion layer, not an auto-linking step.")
    lines.append("- Final inclusion should still be decided by human review.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a candidate linking report for a target MOC.")
    parser.add_argument("--config", required=True, help="Path to the JSON config file.")
    parser.add_argument("--output", help="Optional output path override.")
    args = parser.parse_args()

    vault_root = Path(".").resolve()
    config_path = Path(args.config)
    if not config_path.is_absolute():
        config_path = vault_root / config_path

    config = load_config(config_path)

    moc_path = vault_root / config["moc_path"]
    moc_text = moc_path.read_text(encoding="utf-8")
    linked_notes = extract_moc_links(moc_text)

    reading_notes_dir = vault_root / config["reading_notes_dir"]
    notes = [load_note(path, vault_root) for path in sorted(reading_notes_dir.glob("*.md"))]

    report = build_report(config, notes, linked_notes, vault_root)

    output_path = Path(args.output) if args.output else (vault_root / config["report_path"])
    if not output_path.is_absolute():
        output_path = vault_root / output_path
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")

    print(output_path.relative_to(vault_root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
