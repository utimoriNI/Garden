#!/usr/bin/env python3
"""Import Raindrop.io items with a given tag into 300_Input as reading notes.

The generated notes use the Garden reading-note frontmatter schema. Page
content is extracted with Defuddle when available; otherwise Raindrop
metadata, notes, and highlights are preserved.

Authentication:
    RAINDROP_ACCESS_TOKEN=<personal access token>

Examples:
    python3 scripts/import_raindrop_obsidian_tag.py --dry-run
    python3 scripts/import_raindrop_obsidian_tag.py --tag Obsidian
    python3 scripts/import_raindrop_obsidian_tag.py --tag Obsidian --limit 10
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_BASE = "https://api.raindrop.io/rest/v1"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
INVALID_FILENAME_CHARS = re.compile(r'[/:*?"<>|]')
RAINDROP_TO_OBSIDIAN_TOPIC = {
    "コミュニケーション": "🎁Topic/Life",
    "名文": "🎁Topic/Rhetoric",
    "例え": "🎁Topic/Rhetoric",
}


def normalize_tag(value: str) -> str:
    return value.strip().lstrip("#").casefold()


def request_json(
    path: str,
    access_token: str,
    query: dict[str, str | int] | None = None,
) -> dict[str, Any]:
    url = f"{API_BASE}{path}"
    if query:
        url = f"{url}?{urlencode(query)}"

    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "User-Agent": "Garden-Raindrop-Importer/1.0",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Raindrop API error {exc.code}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach Raindrop API: {exc.reason}") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("Raindrop API returned an unexpected response")
    return payload


def fetch_tagged_items(
    access_token: str,
    tag: str,
    collection_id: int,
    limit: int | None,
) -> list[dict[str, Any]]:
    wanted = normalize_tag(tag)
    items: list[dict[str, Any]] = []
    page = 0
    perpage = 50

    while True:
        payload = request_json(
            f"/raindrops/{collection_id}",
            access_token,
            {"page": page, "perpage": perpage, "sort": "-created"},
        )
        page_items = payload.get("items", [])
        if not isinstance(page_items, list):
            raise RuntimeError("Raindrop API returned an invalid items list")

        for item in page_items:
            if not isinstance(item, dict):
                continue
            tags = item.get("tags", [])
            if isinstance(tags, list) and any(
                normalize_tag(str(item_tag)) == wanted for item_tag in tags
            ):
                items.append(item)
                if limit is not None and len(items) >= limit:
                    return items

        if len(page_items) < perpage:
            break
        page += 1

    return items


def split_frontmatter(text: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def frontmatter_value(frontmatter: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", frontmatter, re.MULTILINE)
    if not match:
        return ""
    value = match.group(1).strip().strip("'\"")
    return value


def existing_sources(input_dir: Path) -> set[str]:
    sources: set[str] = set()
    for path in input_dir.glob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        frontmatter, _ = split_frontmatter(text)
        source = frontmatter_value(frontmatter, "source")
        if source:
            sources.add(source)
    return sources


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def yaml_scalar(value: str) -> str:
    return yaml_quote(value) if value else ""


def clean_filename(value: str) -> str:
    value = INVALID_FILENAME_CHARS.sub("-", value)
    value = re.sub(r"\s+", " ", value).strip().strip(".")
    return value or "Raindrop import"


def infer_source_type(source: str) -> str:
    """Infer the original content type while keeping Raindrop as provenance."""
    lowered = source.casefold()
    if "youtube.com" in lowered or "youtu.be" in lowered:
        return "video"
    return "web"


def topic_tags_from_raindrop(tags: list[Any], trigger_tag: str) -> list[str]:
    """Convert Raindrop tags to the vault's 🎁Topic/... convention."""
    converted: list[str] = []
    seen: set[str] = set()
    trigger = normalize_tag(trigger_tag)

    for value in tags:
        raw = str(value).strip().lstrip("#")
        if not raw or normalize_tag(raw) == trigger:
            continue

        mapped_topic = RAINDROP_TO_OBSIDIAN_TOPIC.get(normalize_tag(raw))
        if mapped_topic:
            topic = mapped_topic
        elif raw.startswith("🎁Topic/"):
            topic = raw
        elif raw.startswith("Topic/"):
            topic = f"🎁{raw}"
        else:
            topic = f"🎁Topic/{raw}"

        # Obsidian tags cannot contain spaces. Keep nested slash tags intact.
        topic = re.sub(r"\s+", "-", topic).strip("/")
        key = topic.casefold()
        if topic and key not in seen:
            converted.append(topic)
            seen.add(key)

    return converted


def unique_path(input_dir: Path, title: str) -> Path:
    base = input_dir / f"{clean_filename(title)}.md"
    if not base.exists():
        return base

    counter = 2
    while True:
        candidate = input_dir / f"{clean_filename(title)} {counter}.md"
        if not candidate.exists():
            return candidate
        counter += 1


def run_defuddle(url: str) -> str:
    executable = shutil.which("defuddle")
    if not executable:
        return ""

    try:
        result = subprocess.run(
            [executable, "parse", url, "--md"],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""

    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def fallback_content(item: dict[str, Any]) -> str:
    sections: list[str] = []
    note = str(item.get("note") or "").strip()
    excerpt = str(item.get("excerpt") or "").strip()
    highlights = item.get("highlights", [])

    if note:
        sections.append(note)
    if excerpt and excerpt != note:
        sections.append(excerpt)

    if isinstance(highlights, list):
        lines: list[str] = []
        for highlight in highlights:
            if not isinstance(highlight, dict):
                continue
            text = str(highlight.get("text") or "").strip()
            if not text:
                continue
            annotation = str(highlight.get("note") or "").strip()
            block = f"> {text.replace(chr(10), chr(10) + '> ')}"
            if annotation:
                block += f"\n\n{annotation}"
            lines.append(block)
        if lines:
            sections.append("## Highlights\n\n" + "\n\n".join(lines))

    return "\n\n".join(section for section in sections if section).strip()


def render_note(
    item: dict[str, Any],
    content: str,
    import_date: str,
    trigger_tag: str,
) -> str:
    title = str(item.get("title") or item.get("domain") or "Raindrop import").strip()
    source = str(item.get("link") or "").strip()
    source_type = infer_source_type(source)
    description = str(item.get("excerpt") or "").strip()
    image = str(item.get("cover") or "").strip()
    raindrop_id = item.get("_id", "")
    raindrop_created = str(item.get("created") or "").strip()
    tags = item.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    obsidian_tags = topic_tags_from_raindrop(tags, trigger_tag)

    lines = [
        "---",
        "type: reading-note",
        f"source_type: {source_type}",
        "source_container:",
        "topic: []",
        "moc: []",
        "status: inbox",
        f"title: {yaml_scalar(title)}",
        f"source: {yaml_scalar(source)}",
        "author:",
        "published:",
        f"created: {yaml_scalar(import_date)}",
        f"description: {yaml_scalar(description)}",
        "tags:",
    ]
    if obsidian_tags:
        lines.extend(f"  - {yaml_quote(tag)}" for tag in obsidian_tags)
    else:
        lines[-1] = "tags: []"

    lines.extend(
        [
            f"image: {yaml_scalar(image)}",
            f"raindrop_id: {yaml_scalar(str(raindrop_id))}",
        ]
    )

    if raindrop_created:
        lines.append(f"raindrop_created: {yaml_scalar(raindrop_created)}")

    lines.extend(["---", ""])
    if content:
        lines.extend([content, ""])
    if source:
        lines.append(f"[Source]({source})")
    return "\n".join(lines).rstrip() + "\n"


def import_items(
    items: list[dict[str, Any]],
    input_dir: Path,
    dry_run: bool,
    no_fetch: bool,
    trigger_tag: str,
) -> tuple[int, int]:
    input_dir.mkdir(parents=True, exist_ok=True)
    known_sources = existing_sources(input_dir)
    imported = 0
    skipped = 0
    import_date = datetime.now().strftime("%Y-%m-%d")

    for item in items:
        source = str(item.get("link") or "").strip()
        title = str(item.get("title") or item.get("domain") or "Raindrop import").strip()
        if not source:
            print(f"SKIP  no URL: {title}")
            skipped += 1
            continue
        if source in known_sources:
            print(f"SKIP  already imported: {title}")
            skipped += 1
            continue

        content = "" if no_fetch else run_defuddle(source)
        if not content:
            content = fallback_content(item)
        note = render_note(item, content, import_date, trigger_tag)
        target = unique_path(input_dir, title)

        if dry_run:
            print(f"DRY   {target.relative_to(input_dir.parent)}")
        else:
            target.write_text(note, encoding="utf-8")
            print(f"WRITE {target.relative_to(input_dir.parent)}")
        known_sources.add(source)
        imported += 1

    return imported, skipped


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import Raindrop items tagged for Obsidian into 300_Input."
    )
    parser.add_argument("--tag", default="Obsidian", help="Raindrop tag to import")
    parser.add_argument(
        "--collection-id",
        type=int,
        default=0,
        help="Raindrop collection ID; 0 means all collections",
    )
    parser.add_argument(
        "--input-dir",
        default="300_Input",
        help="Destination directory relative to the vault root",
    )
    parser.add_argument("--limit", type=int, default=None, help="Maximum number of items")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files without writing them",
    )
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Do not fetch page content; use Raindrop excerpt, notes, and highlights",
    )
    args = parser.parse_args()

    access_token = os.environ.get("RAINDROP_ACCESS_TOKEN", "").strip()
    if not access_token:
        print("RAINDROP_ACCESS_TOKEN is required", file=sys.stderr)
        return 2

    vault_root = Path(__file__).resolve().parent.parent
    input_dir = vault_root / args.input_dir

    try:
        items = fetch_tagged_items(
            access_token,
            args.tag,
            args.collection_id,
            args.limit,
        )
        imported, skipped = import_items(
            items,
            input_dir,
            args.dry_run,
            args.no_fetch,
            args.tag,
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    mode = "dry-run" if args.dry_run else "import"
    print(f"{mode}: {imported} candidate(s), {skipped} skipped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
