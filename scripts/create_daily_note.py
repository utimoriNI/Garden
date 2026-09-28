#!/usr/bin/env python3
"""Create today's Obsidian daily note from the vault's configured template."""

from __future__ import annotations

import argparse
import json
import re
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
    if output_path.exists():
        print(f"Already exists; leaving unchanged: {output_path.relative_to(VAULT_ROOT)}")
        return 0

    content = render_template(template_file.read_text(encoding="utf-8"), note_date)
    output_path.write_text(content, encoding="utf-8")
    print(f"Created: {output_path.relative_to(VAULT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
