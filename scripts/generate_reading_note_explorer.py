#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from pathlib import Path
import re


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
WIKILINK_RE = re.compile(r"!?(\[\[[^\]]+\]\])")
TOPIC_PREFIXES = ("🎁Topic/", "Topic/")
SECTION_HEADINGS = ("Fragment", "Memo", "My Take", "Links")


@dataclass
class NoteRecord:
    note_id: str
    title: str
    path: str
    topics: list[str]
    tags: list[str]
    source_type: str
    source_container: str
    source_book: str
    mocs: list[str]
    consists_of: list[str]
    links: list[str]
    fragment: str
    memo: str
    my_take: str
    preview: str


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
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip("'\"")
    return ""


def normalize_topic(tag: str) -> str:
    if tag.startswith("🎁Topic/"):
        return "Topic/" + tag[len("🎁Topic/") :]
    if tag.startswith("Topic/"):
        return tag
    return ""


def canonical_link_target(value: str) -> str:
    stripped = value.strip().strip("'\"")
    if stripped.startswith("[[") and stripped.endswith("]]"):
        stripped = stripped[2:-2]
    if stripped.startswith("![[") and stripped.endswith("]]"):
        stripped = stripped[3:-2]
    stripped = stripped.split("|", 1)[0]
    stripped = stripped.split("#", 1)[0]
    return stripped.strip()


def extract_title(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def extract_wikilinks(text: str) -> list[str]:
    seen: set[str] = set()
    links: list[str] = []
    for match in WIKILINK_RE.finditer(text):
        target = canonical_link_target(match.group(1))
        if target and target not in seen:
            seen.add(target)
            links.append(target)
    return links


def extract_consists_of(text: str) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for line in text.splitlines():
        if not line.lower().startswith("**consist of**::"):
            continue
        for target in extract_wikilinks(line):
            if target not in seen:
                seen.add(target)
                values.append(target)
    return values


def strip_title_block(body: str, title: str) -> str:
    lines = body.splitlines()
    result: list[str] = []
    skipped_title = False
    for line in lines:
        if not skipped_title and line.strip() == f"# {title}":
            skipped_title = True
            continue
        result.append(line)
    return "\n".join(result)


def parse_sections(body: str, title: str) -> dict[str, str]:
    body_without_title = strip_title_block(body, title)
    sections: dict[str, list[str]] = {"__intro__": []}
    current = "__intro__"

    for line in body_without_title.splitlines():
        matched_heading = None
        for heading in SECTION_HEADINGS:
            if line.strip() == f"## {heading}":
                matched_heading = heading
                break
        if matched_heading:
            current = matched_heading
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return {
        key: clean_section_text("\n".join(value))
        for key, value in sections.items()
    }


def clean_section_text(text: str) -> str:
    cleaned_lines: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append("")
            continue
        if stripped.startswith("出典:"):
            continue
        if stripped.startswith("Kindle:"):
            continue
        if stripped == "%content%":
            continue
        cleaned_lines.append(line.rstrip())
    return "\n".join(cleaned_lines).strip()


def build_preview(sections: dict[str, str]) -> str:
    intro = sections.get("__intro__", "")
    if intro:
        return intro
    for key in ("Fragment", "Memo", "My Take"):
        value = sections.get(key, "")
        if value:
            return value
    return ""


def compact_text(text: str, limit: int) -> str:
    single_line = " ".join(text.split())
    if len(single_line) <= limit:
        return single_line
    return single_line[: limit - 1].rstrip() + "..."


def load_note(path: Path, vault_root: Path) -> NoteRecord | None:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    note_type = parse_scalar(frontmatter, "type")
    if note_type != "reading-note":
        return None

    tags = parse_list_block(frontmatter, "tags")
    topics = sorted({topic for tag in tags if (topic := normalize_topic(tag))})
    mocs = [canonical_link_target(item) for item in parse_list_block(frontmatter, "moc")]
    sections = parse_sections(body, extract_title(path, body))
    links = [
        link for link in extract_wikilinks(body)
        if link not in mocs
        and link != canonical_link_target(parse_scalar(frontmatter, "source_container"))
        and link != canonical_link_target(parse_scalar(frontmatter, "source_book"))
    ]

    title = extract_title(path, body)
    return NoteRecord(
        note_id=path.relative_to(vault_root).as_posix(),
        title=title,
        path=path.relative_to(vault_root).as_posix(),
        topics=topics,
        tags=tags,
        source_type=parse_scalar(frontmatter, "source_type"),
        source_container=canonical_link_target(parse_scalar(frontmatter, "source_container")),
        source_book=canonical_link_target(parse_scalar(frontmatter, "source_book")),
        mocs=[item for item in mocs if item],
        consists_of=extract_consists_of(body),
        links=links,
        fragment=sections.get("Fragment", ""),
        memo=sections.get("Memo", ""),
        my_take=sections.get("My Take", ""),
        preview=compact_text(build_preview(sections), 220),
    )


def note_source_key(note: NoteRecord) -> str:
    return note.source_container or note.source_book


def build_related(note: NoteRecord, all_notes: list[NoteRecord], limit: int) -> list[dict[str, object]]:
    related: list[dict[str, object]] = []
    note_topics = set(note.topics)
    note_mocs = set(note.mocs)
    note_links = set(note.links)
    note_consists = set(note.consists_of)
    note_source = note_source_key(note)

    for candidate in all_notes:
        if candidate.note_id == note.note_id:
            continue

        candidate_topics = set(candidate.topics)
        shared_topics = sorted(note_topics & candidate_topics)
        if not shared_topics:
            continue

        score = len(shared_topics) * 5
        reasons: list[str] = [f"same topic: {topic}" for topic in shared_topics]

        candidate_source = note_source_key(candidate)
        if note_source and candidate_source and note_source == candidate_source:
            score += 4
            reasons.append(f"same source: {note_source}")

        shared_mocs = sorted(note_mocs & set(candidate.mocs))
        if shared_mocs:
            score += len(shared_mocs) * 4
            reasons.extend(f"same moc: {moc}" for moc in shared_mocs)

        shared_consists = sorted(note_consists & set(candidate.consists_of))
        if shared_consists:
            score += len(shared_consists) * 3
            reasons.extend(f"shared consist of: {item}" for item in shared_consists)

        shared_links = sorted(note_links & set(candidate.links))
        if shared_links:
            score += len(shared_links) * 2
            reasons.extend(f"shared link: {link}" for link in shared_links[:3])

        related.append(
            {
                "noteId": candidate.note_id,
                "score": score,
                "reasons": reasons[:6],
            }
        )

    related.sort(key=lambda item: (-int(item["score"]), item["noteId"]))
    return related[:limit]


def build_topic_index(notes: list[NoteRecord]) -> list[dict[str, object]]:
    topic_map: dict[str, list[str]] = {}
    for note in notes:
        for topic in note.topics:
            topic_map.setdefault(topic, []).append(note.note_id)

    topics = [
        {
            "name": name,
            "count": len(note_ids),
            "noteIds": sorted(note_ids),
        }
        for name, note_ids in topic_map.items()
    ]
    topics.sort(key=lambda item: (-int(item["count"]), str(item["name"])))
    return topics


def serialize_note(note: NoteRecord, all_notes: list[NoteRecord], related_limit: int) -> dict[str, object]:
    return {
        "id": note.note_id,
        "path": note.path,
        "title": note.title,
        "topics": note.topics,
        "tags": note.tags,
        "sourceType": note.source_type,
        "sourceContainer": note.source_container,
        "sourceBook": note.source_book,
        "mocs": note.mocs,
        "consistsOf": note.consists_of,
        "links": note.links,
        "fragment": note.fragment,
        "memo": note.memo,
        "myTake": note.my_take,
        "preview": note.preview,
        "related": build_related(note, all_notes, related_limit),
    }


def write_output(data: dict[str, object], output_dir: Path, assets_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for asset_name in ("index.html", "app.js", "styles.css"):
        shutil.copyfile(assets_dir / asset_name, output_dir / asset_name)

    data_js = "window.READING_NOTE_EXPLORER_DATA = " + json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    ) + ";\n"
    (output_dir / "data.js").write_text(data_js, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a topic-based reading-note explorer.")
    parser.add_argument(
        "--input-dir",
        default="300_Input/Reading Notes",
        help="Reading-note directory relative to the vault root.",
    )
    parser.add_argument(
        "--output-dir",
        default=".agent-wiki/reading-note-explorer",
        help="Output directory for the generated explorer.",
    )
    parser.add_argument(
        "--related-limit",
        type=int,
        default=12,
        help="Maximum related notes to keep for each reading note.",
    )
    args = parser.parse_args()

    vault_root = Path(".").resolve()
    input_dir = vault_root / args.input_dir
    output_dir = vault_root / args.output_dir
    assets_dir = Path(__file__).resolve().parent / "reading_note_explorer_assets"

    notes: list[NoteRecord] = []
    for path in sorted(input_dir.glob("*.md")):
        note = load_note(path, vault_root)
        if note is not None and note.topics:
            notes.append(note)

    data = {
        "generatedAt": __import__("datetime").datetime.now().isoformat(timespec="seconds"),
        "noteCount": len(notes),
        "topicCount": len({topic for note in notes for topic in note.topics}),
        "topics": build_topic_index(notes),
        "notes": {
            note.note_id: serialize_note(note, notes, args.related_limit)
            for note in notes
        },
    }
    write_output(data, output_dir, assets_dir)

    print(output_dir.relative_to(vault_root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
