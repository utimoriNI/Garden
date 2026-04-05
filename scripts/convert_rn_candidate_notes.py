#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
CANDIDATE_TAG = "🧩rn/candidate"


def infer_source_type(path: Path, body: str) -> str:
    path_str = path.as_posix()
    if "kindle://book?action=open" in body:
        return "kindle"
    if path_str.startswith("300_Input/"):
        return "web"
    return "legacy"


def ensure_key(lines: list[str], key: str, value_lines: list[str]) -> list[str]:
    prefix = f"{key}:"
    for idx, line in enumerate(lines):
        if line.startswith(prefix):
            if len(value_lines) == 1:
                lines[idx] = value_lines[0]
                return lines

            end = idx + 1
            while end < len(lines) and (lines[end].startswith("  ") or lines[end].startswith("\t")):
                end += 1
            lines[idx:end] = value_lines
            return lines

    lines.extend(value_lines)
    return lines


def remove_candidate_tag(lines: list[str]) -> list[str]:
    result: list[str] = []
    in_tags_block = False

    for line in lines:
        if line.startswith("tags: ["):
            inside = line[len("tags: [") :].rstrip("]")
            parts = [part.strip() for part in inside.split(",") if part.strip()]
            parts = [part for part in parts if part != CANDIDATE_TAG]
            if parts:
                result.append(f"tags: [{', '.join(parts)}]")
            else:
                result.append("tags: []")
            in_tags_block = False
            continue

        if line.startswith("tags:"):
            result.append(line)
            in_tags_block = True
            continue

        if in_tags_block:
            if line.startswith("  - "):
                tag_value = line[4:].strip()
                if tag_value == CANDIDATE_TAG:
                    continue
                result.append(line)
                continue
            in_tags_block = False

        result.append(line)

    return result


def convert_text(path: Path, text: str) -> str:
    match = FRONTMATTER_RE.match(text)
    if match:
        frontmatter_lines = match.group(1).splitlines()
        body = text[match.end():]
    else:
        frontmatter_lines = []
        body = text

    frontmatter_lines = remove_candidate_tag(frontmatter_lines)
    source_type = infer_source_type(path, body)

    frontmatter_lines = ensure_key(frontmatter_lines, "type", ["type: reading-note"])
    if not any(line.startswith("source_type:") for line in frontmatter_lines):
        frontmatter_lines = ensure_key(frontmatter_lines, "source_type", [f"source_type: {source_type}"])
    if not any(line.startswith("source_container:") for line in frontmatter_lines):
        frontmatter_lines = ensure_key(frontmatter_lines, "source_container", ["source_container:"])
    if not any(line.startswith("topic:") for line in frontmatter_lines):
        frontmatter_lines = ensure_key(frontmatter_lines, "topic", ["topic: []"])
    if not any(line.startswith("moc:") for line in frontmatter_lines):
        frontmatter_lines = ensure_key(frontmatter_lines, "moc", ["moc: []"])
    if not any(line.startswith("status:") for line in frontmatter_lines):
        frontmatter_lines = ensure_key(frontmatter_lines, "status", ["status: inbox"])

    return "---\n" + "\n".join(frontmatter_lines).rstrip() + "\n---\n" + body.lstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert 🧩rn/candidate notes into reading-note schema and remove the candidate tag."
    )
    parser.add_argument("--dry-run", action="store_true", help="Print target files without writing.")
    args = parser.parse_args()

    updated = 0
    for path in sorted(Path(".").rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        if CANDIDATE_TAG not in text:
            continue

        new_text = convert_text(path, text)
        if new_text == text:
            continue

        if args.dry_run:
            print(path.as_posix())
        else:
            path.write_text(new_text, encoding="utf-8")
        updated += 1

    print(f"updated={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
