#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[4]
KINDLE_DIR = REPO_ROOT / "400_Kindle"
MARKER_CLEANUP_RE = re.compile(
    r"(?m)^%%\s*(?:pick|group:\s*.*?|title:\s*.*?)\s*%%\s*(?:\^[A-Za-z0-9_-]+)?\n?"
)
MARKER_FIND_RE = re.compile(r"%%\s*(?:pick|group:|title:)")


def run_python_script(relative_path: str) -> None:
    script_path = REPO_ROOT / relative_path
    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def cleanup_kindle_markers() -> int:
    updated = 0
    if not KINDLE_DIR.exists():
        print("cleanup_updated=0")
        return 0

    for path in sorted(KINDLE_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        new_text = MARKER_CLEANUP_RE.sub("", text)
        if new_text == text:
            continue
        path.write_text(new_text, encoding="utf-8")
        updated += 1

    print(f"cleanup_updated={updated}")
    return updated


def find_remaining_markers() -> list[str]:
    remaining: list[str] = []
    if not KINDLE_DIR.exists():
        return remaining

    for path in sorted(KINDLE_DIR.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for lineno, line in enumerate(text.splitlines(), start=1):
            if MARKER_FIND_RE.search(line):
                remaining.append(f"{path.relative_to(REPO_ROOT)}:{lineno}")
    return remaining


def main() -> int:
    parser = argparse.ArgumentParser(
        description="一節ノート生成と収集マーカー片付けをまとめて実行する。"
    )
    parser.add_argument(
        "--cleanup-only",
        action="store_true",
        help="変換や生成を行わず、400_Kindle の収集マーカー削除だけ実行する。",
    )
    args = parser.parse_args()

    if not args.cleanup_only:
        run_python_script("scripts/convert_rn_candidate_notes.py")
        run_python_script("scripts/generate_kindle_reading_notes.py")

    cleanup_kindle_markers()

    remaining = find_remaining_markers()
    if remaining:
        print("remaining_markers:")
        for item in remaining:
            print(item)
        return 1

    print("remaining_markers=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
