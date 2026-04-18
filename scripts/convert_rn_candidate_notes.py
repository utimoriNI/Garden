#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
TITLE_DIRECTIVE_RE = re.compile(r"^%%\s*title:\s*(?P<title>.+?)\s*%%$", re.IGNORECASE)
CANDIDATE_TAG = "🧩rn/candidate"
READING_NOTES_DIR = Path("300_Input/Reading Notes")
EXCLUDED_PATHS = {
    Path("200_Inbox/タグ保存用.md"),
}


def infer_source_type(path: Path, body: str) -> str:
    path_str = path.as_posix()
    if "kindle://book?action=open" in body:
        return "kindle"
    if path_str.startswith("300_Input/"):
        return "web"
    return "legacy"


def extract_frontmatter_lines(text: str) -> list[str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return []
    return match.group(1).splitlines()


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def sanitize_filename(value: str) -> str:
    value = re.sub(r"[/:*?\"<>|]", "-", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def normalize_title_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value).strip()
    return value.strip(" 　-")


def extract_title_directive(body: str) -> str:
    for line in body.splitlines():
        match = TITLE_DIRECTIVE_RE.match(line.strip())
        if match:
            return normalize_title_text(match.group("title"))
    return ""


def remove_title_directive(body: str) -> str:
    lines = [line for line in body.splitlines() if not TITLE_DIRECTIVE_RE.match(line.strip())]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def frontmatter_has_candidate_tag(lines: list[str]) -> bool:
    in_tags_block = False
    for line in lines:
        if line.startswith("tags: ["):
            inside = line[len("tags: [") :].rstrip("]")
            parts = [part.strip() for part in inside.split(",") if part.strip()]
            return CANDIDATE_TAG in parts

        if line.startswith("tags:"):
            in_tags_block = True
            continue

        if in_tags_block:
            if line.startswith("  - "):
                if line[4:].strip() == CANDIDATE_TAG:
                    return True
                continue
            in_tags_block = False

    return False


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


def target_path_for_title(path: Path, explicit_title: str) -> Path:
    if explicit_title:
        filename = sanitize_filename(f"{explicit_title}.md")
    else:
        filename = path.name
    if not filename:
        return path
    return READING_NOTES_DIR / filename


def ensure_unique_path(target_path: Path, current_path: Path) -> Path:
    if target_path == current_path or not target_path.exists():
        return target_path

    stem = target_path.stem
    suffix = target_path.suffix
    counter = 2
    while True:
        candidate = target_path.with_name(f"{stem} {counter}{suffix}")
        if candidate == current_path or not candidate.exists():
            return candidate
        counter += 1


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


def convert_text(path: Path, text: str) -> tuple[str, Path]:
    match = FRONTMATTER_RE.match(text)
    if match:
        frontmatter_lines = match.group(1).splitlines()
        body = text[match.end():]
    else:
        frontmatter_lines = []
        body = text

    explicit_title = extract_title_directive(body)
    body = remove_title_directive(body)
    frontmatter_lines = remove_candidate_tag(frontmatter_lines)
    source_type = infer_source_type(path, body)

    frontmatter_lines = ensure_key(frontmatter_lines, "type", ["type: reading-note"])
    if explicit_title:
        frontmatter_lines = ensure_key(frontmatter_lines, "title", [f"title: {yaml_quote(explicit_title)}"])
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

    new_text = "---\n" + "\n".join(frontmatter_lines).rstrip() + "\n---\n" + body.lstrip("\n")
    target_path = ensure_unique_path(target_path_for_title(path, explicit_title), path)
    return new_text, target_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert 🧩rn/candidate notes into reading-note schema and remove the candidate tag."
    )
    parser.add_argument("--dry-run", action="store_true", help="Print target files without writing.")
    args = parser.parse_args()

    updated = 0
    READING_NOTES_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(Path(".").rglob("*.md")):
        if path in EXCLUDED_PATHS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        frontmatter_lines = extract_frontmatter_lines(text)
        if not frontmatter_has_candidate_tag(frontmatter_lines):
            continue

        new_text, target_path = convert_text(path, text)
        if new_text == text and target_path == path:
            continue

        if args.dry_run:
            if target_path != path:
                print(f"{path.as_posix()} -> {target_path.as_posix()}")
            else:
                print(path.as_posix())
        else:
            path.write_text(new_text, encoding="utf-8")
            if target_path != path:
                path.rename(target_path)
        updated += 1

    print(f"updated={updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
