#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
LEXICON_TAG = "🎁Topic/Lexicon"


def has_lexicon_tag(text: str) -> bool:
    return LEXICON_TAG in text or "Topic/Lexicon" in text


def infer_source_type(path: Path, body: str) -> str:
    path_str = path.as_posix()
    if "kindle://book?action=open" in body:
        return "kindle"
    if path_str.startswith("300_Input/"):
        return "web"
    return "legacy"


def ensure_key(lines: list[str], key: str, value_lines: list[str]) -> list[str]:
    simple_key = f"{key}:"
    for idx, line in enumerate(lines):
        if line.startswith(simple_key):
            if len(value_lines) == 1:
                lines[idx] = value_lines[0]
                return lines

            end = idx + 1
            while end < len(lines) and (lines[end].startswith("  ") or lines[end].startswith("\t")):
                end += 1
            lines[idx:end] = value_lines
            return lines

    insert_at = len(lines)
    lines[insert_at:insert_at] = value_lines
    return lines


def migrate_text(path: Path, text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if match:
        frontmatter = match.group(1).splitlines()
        body = text[match.end():]
    else:
        frontmatter = []
        body = text

    source_type = infer_source_type(path, body)

    frontmatter = ensure_key(frontmatter, "type", ["type: reading-note"])
    if not any(line.startswith("source_type:") for line in frontmatter):
        frontmatter = ensure_key(frontmatter, "source_type", [f"source_type: {source_type}"])
    if not any(line.startswith("source_container:") for line in frontmatter):
        frontmatter = ensure_key(frontmatter, "source_container", ["source_container:"])
    if not any(line.startswith("topic:") for line in frontmatter):
        frontmatter = ensure_key(frontmatter, "topic", ["topic: []"])
    if not any(line.startswith("moc:") for line in frontmatter):
        frontmatter = ensure_key(frontmatter, "moc", ["moc: []"])
    if not any(line.startswith("status:") for line in frontmatter):
        frontmatter = ensure_key(frontmatter, "status", ["status: inbox"])

    new_frontmatter = "---\n" + "\n".join(frontmatter).rstrip() + "\n---\n"
    return new_frontmatter + body.lstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Bulk-migrate 🎁Topic/Lexicon notes into the reading-note schema."
    )
    parser.add_argument("--dry-run", action="store_true", help="Print target files without writing.")
    args = parser.parse_args()

    updated = 0
    for path in sorted(Path(".").rglob("*.md")):
        if path.as_posix() == "010_Topics/Lexicon.md":
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        if not has_lexicon_tag(text):
            continue

        migrated = migrate_text(path, text)
        if migrated == text:
            continue

        if args.dry_run:
            print(path.as_posix())
        else:
            path.write_text(migrated, encoding="utf-8")
        updated += 1

    print(f"updated={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
