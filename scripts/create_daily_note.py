#!/usr/bin/env python3
"""Create today's Obsidian daily note from the vault's configured template."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


VAULT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = VAULT_ROOT / ".obsidian" / "daily-notes.json"
DATE_FORMAT = "YYYY-MM-DD"
TOKYO = ZoneInfo("Asia/Tokyo")

TEMPLATER_DATE = re.compile(
    r'<%\s*tp\.date\.now\("YYYY-MM-DD",\s*(-?\d+),\s*'
    r'tp\.file\.title,\s*"YYYY-MM-DD"\)\s*%>'
)
SECTION_HEADING = "## 当日作成されたノート"
SECTION_START = "<!-- BEGIN AUTO-CREATED NOTES -->"
SECTION_END = "<!-- END AUTO-CREATED NOTES -->"


def render_template(template: str, note_date: date) -> str:
    def replace_date(match: re.Match[str]) -> str:
        offset = int(match.group(1))
        return (note_date + timedelta(days=offset)).strftime("%Y-%m-%d")

    rendered = TEMPLATER_DATE.sub(replace_date, template)
    if "<%" in rendered:
        raise ValueError(
            "The daily template contains Templater syntax this script cannot render."
        )
    return rendered


def notes_added_on(note_date: date, daily_folder: Path) -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "-c",
            "core.quotepath=false",
            "log",
            "--format=COMMIT:%ct",
            "--name-only",
            "--diff-filter=A",
            "--",
            "*.md",
        ],
        cwd=VAULT_ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )

    added: set[Path] = set()
    commit_timestamp: int | None = None
    for line in result.stdout.splitlines():
        if line.startswith("COMMIT:"):
            commit_timestamp = int(line.removeprefix("COMMIT:"))
            continue
        if not line or commit_timestamp is None:
            continue

        committed_date = datetime.fromtimestamp(commit_timestamp, TOKYO).date()
        path = Path(line)
        if (
            committed_date == note_date
            and path.suffix.lower() == ".md"
            and (VAULT_ROOT / path).is_file()
            and daily_folder not in path.parents
        ):
            added.add(path)

    return sorted(added, key=lambda path: path.as_posix().casefold())


def render_notes_section(paths: list[Path]) -> str:
    if not paths:
        body = "GitHubに追加された当日作成ノートはありません。"
    else:
        entries = []
        for path in paths:
            target = path.with_suffix("").as_posix()
            entries.append(f"- [[{target}]]\n\n![[{target}]]")
        body = "\n\n".join(entries)

    return f"{SECTION_HEADING}\n\n{SECTION_START}\n{body}\n{SECTION_END}"


def update_daily_note(note_path: Path, content: str, notes_section: str) -> bool:
    if not note_path.exists():
        note_path.write_text(f"{content.rstrip()}\n\n{notes_section}\n", encoding="utf-8")
        return True

    existing = note_path.read_text(encoding="utf-8")
    managed_pattern = re.compile(
        rf"{re.escape(SECTION_HEADING)}\s*\n\s*{re.escape(SECTION_START)}.*?"
        rf"{re.escape(SECTION_END)}",
        re.DOTALL,
    )
    if managed_pattern.search(existing):
        updated = managed_pattern.sub(notes_section, existing, count=1)
    else:
        updated = f"{existing.rstrip()}\n\n{notes_section}\n"

    if updated == existing:
        return False
    note_path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--date",
        help="Create a note for this date (YYYY-MM-DD); defaults to today's date in Tokyo.",
    )
    args = parser.parse_args()

    settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    folder = settings.get("folder", "").strip()
    template_path = settings.get("template", "").strip()
    date_format = settings.get("format", DATE_FORMAT)
    if date_format != DATE_FORMAT:
        raise ValueError(
            f"Unsupported daily note format {date_format!r}; expected {DATE_FORMAT!r}."
        )
    if not folder or not template_path:
        raise ValueError("Daily note folder and template must be set in daily-notes.json.")

    note_date = date.fromisoformat(args.date) if args.date else datetime.now(TOKYO).date()
    note_name = note_date.strftime("%Y-%m-%d") + ".md"
    output_dir = (VAULT_ROOT / folder).resolve()
    template_file = (VAULT_ROOT / template_path).resolve()
    if VAULT_ROOT not in output_dir.parents or VAULT_ROOT not in template_file.parents:
        raise ValueError("Daily note folder and template must stay inside the vault.")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / note_name
    daily_folder = Path(folder)
    notes = notes_added_on(note_date, daily_folder)
    notes_section = render_notes_section(notes)
    if output_path.exists():
        changed = update_daily_note(output_path, "", notes_section)
        action = "Updated" if changed else "Already up to date"
    else:
        template = template_file.read_text(encoding="utf-8")
        content = render_template(template, note_date)
        changed = update_daily_note(output_path, content, notes_section)
        action = "Created" if changed else "Already up to date"

    print(f"{action}: {output_path.relative_to(VAULT_ROOT)}")
    print(f"Included {len(notes)} note(s) added on {note_date.isoformat()} (Japan time).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
