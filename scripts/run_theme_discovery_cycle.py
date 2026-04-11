#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import re


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)


@dataclass
class NoteRecord:
    vault_path: str
    title: str
    tags: list[str]
    mocs: list[str]
    note_type: str
    source_type: str


def load_json(path: Path) -> dict:
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
    prefix = f"{key}:"
    for line in lines:
        if line.startswith(prefix):
            return line[len(prefix) :].strip().strip("'\"")
    return ""


def extract_title(path: Path, body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem


def load_note(path: Path, vault_root: Path) -> NoteRecord:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    return NoteRecord(
        vault_path=path.relative_to(vault_root).as_posix(),
        title=extract_title(path, body),
        tags=parse_list_block(frontmatter, "tags"),
        mocs=parse_list_block(frontmatter, "moc"),
        note_type=parse_scalar(frontmatter, "type"),
        source_type=parse_scalar(frontmatter, "source_type"),
    )


def build_scope_report(scope_config: dict, notes: list[NoteRecord], generated_reports: list[str]) -> str:
    required_tags = scope_config["required_tags"]
    eligible = [
        note
        for note in notes
        if note.note_type == "reading-note" and all(tag in note.tags for tag in required_tags)
    ]
    eligible.sort(key=lambda item: item.title)

    source_counts = Counter(note.source_type or "unknown" for note in eligible)
    with_moc = [note for note in eligible if note.mocs]
    without_moc = [note for note in eligible if not note.mocs]

    lines: list[str] = []
    lines.append(f"# {scope_config['name']} Scope Report")
    lines.append("")
    lines.append(f"Created: {scope_config['created']}")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Eligible `reading-note`: {len(eligible)}")
    lines.append(f"- Already connected to at least one MOC: {len(with_moc)}")
    lines.append(f"- Still without MOC connection: {len(without_moc)}")
    lines.append("")
    lines.append("## Source Types")
    lines.append("")
    for source_type, count in sorted(source_counts.items()):
        lines.append(f"- `{source_type}`: {count}")
    lines.append("")
    lines.append("## Generated Reports")
    lines.append("")
    for report in generated_reports:
        lines.append(f"- [[{report}]]")
    lines.append("")
    lines.append("## Notes Without MOC Connection")
    lines.append("")
    if not without_moc:
        lines.append("- None")
    else:
        for note in without_moc:
            lines.append(f"- [[{note.vault_path}]]")
    lines.append("")
    lines.append("## Notes Already Connected")
    lines.append("")
    for note in with_moc:
        joined = ", ".join(note.mocs)
        lines.append(f"- [[{note.vault_path}]]")
        lines.append(f"  - moc: {joined}")
    lines.append("")
    lines.append("## Principle")
    lines.append("")
    lines.append("- This report is for discovery and review, not for blind auto-linking.")
    lines.append("- Human-facing MOCs should still be updated only after review.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a full theme-discovery maintenance cycle.")
    parser.add_argument(
        "--registry",
        default=".agent-wiki/theme-discovery/configs/moc_registry.json",
        help="Path to the theme-discovery registry JSON.",
    )
    args = parser.parse_args()

    vault_root = Path(".").resolve()
    registry_path = Path(args.registry)
    if not registry_path.is_absolute():
        registry_path = vault_root / registry_path

    registry = load_json(registry_path)

    scope_config_path = Path(registry["scope_config"])
    if not scope_config_path.is_absolute():
        scope_config_path = vault_root / scope_config_path
    scope_config = load_json(scope_config_path)

    generated_reports: list[str] = []
    generator_script = vault_root / "scripts" / "generate_moc_link_report.py"

    for moc_config_str in registry["moc_configs"]:
        moc_config_path = Path(moc_config_str)
        if not moc_config_path.is_absolute():
            moc_config_path = vault_root / moc_config_path

        result = subprocess.run(
            [sys.executable, str(generator_script), "--config", str(moc_config_path)],
            cwd=vault_root,
            capture_output=True,
            text=True,
            check=True,
        )
        generated_reports.append(result.stdout.strip())

    reading_notes_dir = vault_root / scope_config["reading_notes_dir"]
    notes = [load_note(path, vault_root) for path in sorted(reading_notes_dir.glob("*.md"))]
    scope_report = build_scope_report(scope_config, notes, generated_reports)

    scope_report_path = Path(scope_config["report_path"])
    if not scope_report_path.is_absolute():
        scope_report_path = vault_root / scope_report_path
    scope_report_path.parent.mkdir(parents=True, exist_ok=True)
    scope_report_path.write_text(scope_report, encoding="utf-8")

    run_summary_path = Path(scope_config["run_summary_path"])
    if not run_summary_path.is_absolute():
        run_summary_path = vault_root / run_summary_path

    run_lines = [
        f"# {scope_config['name']} Theme Discovery Run",
        "",
        f"Created: {scope_config['created']}",
        "",
        "## Outputs",
        "",
        f"- [[{scope_report_path.relative_to(vault_root).as_posix()}]]",
    ]
    for report in generated_reports:
        run_lines.append(f"- [[{report}]]")
    run_lines.append("")
    run_summary_path.parent.mkdir(parents=True, exist_ok=True)
    run_summary_path.write_text("\n".join(run_lines) + "\n", encoding="utf-8")

    print(scope_report_path.relative_to(vault_root).as_posix())
    print(run_summary_path.relative_to(vault_root).as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
