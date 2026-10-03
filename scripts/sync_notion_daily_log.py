#!/usr/bin/env python3
"""Upsert a Garden daily commit log, preserving unrelated Notion content."""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime, time as day_time, timedelta, timezone
from fnmatch import fnmatchcase
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.error import HTTPError
from urllib.parse import quote, unquote, urlencode
from urllib.request import Request, urlopen
from uuid import UUID


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "scripts/notion_daily_log.json"
JST = timezone(timedelta(hours=9))
API_VERSION = "2025-09-03"
BEGIN = "[Garden GitHub log:begin]"
END = "[Garden GitHub log:end]"
MAX_TEXT = 80_000  # <=40 rich-text items; also leaves room below the 500 KB limit.


@dataclass
class Commit:
    sha: str
    timestamp: int
    author: str
    subject: str
    changes: list[tuple[str, str]]


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.run(
        ["git", *args], cwd=root, check=True, capture_output=True,
        text=True, encoding="utf-8",
    ).stdout


def log_date(value: str | None, now: datetime | None = None) -> date:
    if value:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("--date must use YYYY-MM-DD.")
        return date.fromisoformat(value)
    return (now or datetime.now(JST)).astimezone(JST).date() - timedelta(days=1)


def collect_commits(target: date, excludes: list[str], root: Path = ROOT) -> list[Commit]:
    start = datetime.combine(target, day_time.min, JST)
    end = start + timedelta(days=1)
    # since-as-filter walks the history even when commit dates are out of order.
    raw = git("log", "-z", "--reverse", f"--since-as-filter={start.isoformat()}",
              "--format=%H%x00%ct%x00%an%x00%s", "HEAD", root=root)
    fields = raw.split("\0")
    if fields[-1] == "":
        fields.pop()
    commits = []
    for offset in range(0, len(fields), 4):
        sha, timestamp, author, subject = fields[offset:offset + 4]
        if not start.timestamp() <= int(timestamp) < end.timestamp():
            continue
        # Treat renames as deletion + addition and include root and merge commits.
        changes_raw = git("diff-tree", "--root", "--no-commit-id", "--name-status",
                          "--no-renames", "-r", "-m", "-z", sha, root=root)
        tokens = changes_raw.split("\0")
        if tokens[-1] == "":
            tokens.pop()
        changes = set()
        for index in range(0, len(tokens), 2):
            status, path = tokens[index:index + 2]
            if not any(fnmatchcase(path, pattern) for pattern in excludes):
                changes.add((status, path))
        commits.append(Commit(sha, int(timestamp), author, subject, sorted(changes)))
    return commits


def render_log(target: date, repository: str, commits: list[Commit]) -> tuple[str, str]:
    changes: dict[str, set[str]] = defaultdict(set)
    for commit in commits:
        for status, path in commit.changes:
            changes[status].add(path)
    notes = {path for paths in changes.values() for path in paths if path.lower().endswith(".md")}
    summary = (f"{repository}: {len(commits)}コミット、{len(notes)}ノートに変更。\n"
               f"ファイルの追加 {len(changes['A'])} / 更新 {len(changes['M'])} / "
               f"削除 {len(changes['D'])}（各区分の重複パスを除く）。")
    lines = [f"{target} のコミットログ（日本時間 00:00–24:00）", summary, "", "コミット"]
    for commit in commits:
        at = datetime.fromtimestamp(commit.timestamp, JST).strftime("%H:%M:%S")
        lines.extend([f"{at} {commit.sha[:7]} {commit.subject} — {commit.author}",
                      f"https://github.com/{repository}/commit/{commit.sha}"])
    labels = {"A": "追加", "M": "更新", "D": "削除", "T": "種類変更"}
    for status, paths in sorted(changes.items()):
        lines.extend(["", f"変更ファイル：{labels.get(status, status)}"])
        lines.extend(sorted(paths))
    return summary, "\n".join(lines)


def rich_text(value: str) -> list[dict]:
    if len(value) > MAX_TEXT:
        raise ValueError("Notion text is too large; shorten handwritten summary content.")
    return [{"type": "text", "text": {"content": value[i:i + 2000]}}
            for i in range(0, len(value), 2000)]


def plain_text(items: list[dict]) -> str:
    return "".join(item.get("plain_text", item.get("text", {}).get("content", ""))
                   for item in items)


def merge_summary(existing: list[dict], summary: str) -> list[dict]:
    """Replace only our marked rich-text range, retaining surrounding formatting."""
    text = plain_text(existing)
    replacement = rich_text(f"{BEGIN}\n{summary}\n{END}")
    if BEGIN not in text and END not in text:
        result = clean_text(existing) + rich_text("\n\n" if text else "") + replacement
    else:
        if text.count(BEGIN) != 1 or text.count(END) != 1 or text.index(END) < text.index(BEGIN):
            raise ValueError("The managed summary markers are damaged or duplicated.")
        start, stop = text.index(BEGIN), text.index(END) + len(END)
        result = slice_text(existing, 0, start) + replacement + slice_text(existing, stop, len(text))
    if len(result) > 100 or len(plain_text(result)) > MAX_TEXT:
        raise ValueError("The summary exceeds Notion's rich-text limits.")
    return result


def clean_text(items: list[dict]) -> list[dict]:
    return [{key: value for key, value in item.items() if key not in {"plain_text", "href"}}
            for item in items]


def slice_text(items: list[dict], start: int, stop: int) -> list[dict]:
    result, position = [], 0
    for original in items:
        length = len(plain_text([original]))
        item = clean_text([original])[0]
        left, right = max(0, start - position), min(length, stop - position)
        if left < right:
            if item.get("type") == "text":
                item = {**item, "text": {**item["text"], "content": item["text"]["content"][left:right]}}
            elif left != 0 or right != length:
                raise ValueError("A summary marker crosses a mention or equation.")
            result.append(item)
        position += length
    return result


class Notion:
    def __init__(self, token: str):
        self.token = token

    def request(self, method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
        if data and len(data) > 450_000:
            raise ValueError("Notion request exceeds the payload budget.")
        request = Request(f"https://api.notion.com/v1/{path}", data=data, method=method,
                          headers={"Authorization": f"Bearer {self.token}",
                                   "Notion-Version": API_VERSION, "Content-Type": "application/json"})
        for attempt in range(5):
            try:
                with urlopen(request, timeout=45) as response:
                    return json.load(response)
            except HTTPError as error:
                # Queries and replacement PATCHes are safe to retry. Do not blindly
                # retry creates/appends: an error response may follow a saved write.
                failure = json.loads(error.read().decode("utf-8"))
                safe = method == "GET" or path.endswith("/query") or (
                    method == "PATCH" and not path.endswith("/children"))
                blocked = failure.get("additional_data", {}).get("rate_limit_reason") == "public_api_request_blocked"
                retry = not blocked and (error.code in {429, 529} or (
                    safe and error.code in {500, 502, 503, 504}))
                if not retry or attempt == 4:
                    code = failure.get("code", "unknown_error")
                    raise RuntimeError(f"Notion {method} {path}: HTTP {error.code} ({code}). "
                                       "Check connection permissions/configuration; rerun after recovery.") from None
                time.sleep(float(error.headers.get("Retry-After", min(2 ** attempt, 30))))
        raise AssertionError("unreachable")

    def list_all(self, method: str, path: str, body: dict | None = None) -> list[dict]:
        results, cursor = [], None
        while True:
            parameters = {"page_size": 100}
            if cursor:
                parameters["start_cursor"] = cursor
            if method == "GET":
                response = self.request(method, f"{path}?{urlencode(parameters)}")
            else:
                response = self.request(method, path, {**(body or {}), **parameters})
            results.extend(response["results"])
            if not response.get("has_more"):
                return results
            cursor = response["next_cursor"]


def sync_log(api: Notion, config: dict, target: date, repository: str,
             summary: str, details: str) -> str:
    source = str(UUID(config["data_source_id"]))
    schema = api.request("GET", f"data_sources/{source}")["properties"]
    for key, expected in [("title_property", "title"), ("date_property", "date"),
                          ("summary_property", "rich_text")]:
        if schema.get(config[key], {}).get("type") != expected:
            raise ValueError(f"Notion property {config[key]!r} must be {expected}.")
    title = config["title_format"].format(date=target.isoformat(), repository=repository)
    # Match our reserved title as well as the date; ordinary entries on the same
    # day remain untouched. One date-only match would overwrite a personal log.
    pages = api.list_all("POST", f"data_sources/{source}/query", {"filter": {"and": [
        {"property": config["title_property"], "title": {"equals": title}},
        {"property": config["date_property"], "date": {"equals": target.isoformat()}},
    ]}})
    if len(pages) > 1:
        raise ValueError("Multiple matching daily logs exist; resolve duplicates before rerunning.")
    caption = f"Garden GitHub log | {repository} | {target}"
    if len(details) > MAX_TEXT:
        details = details[:MAX_TEXT - 150] + "\n\n（表示上限により省略。完全な変更はGitHubのコミットを参照してください。）"
    code = {"rich_text": rich_text(details), "language": "plain text", "caption": rich_text(caption)}
    block = {"object": "block", "type": "code", "code": code}
    if not pages:
        properties = {
            config["title_property"]: {"title": rich_text(title)},
            config["date_property"]: {"date": {"start": target.isoformat()}},
            config["summary_property"]: {"rich_text": merge_summary([], summary)},
        }
        page = api.request("POST", "pages", {
            "parent": {"type": "data_source_id", "data_source_id": source},
            "properties": properties, "children": [block],
        })
        return page["url"]
    # Retrieve the page again, rather than relying on query property truncation.
    page = api.request("GET", f"pages/{pages[0]['id']}")
    prop = page["properties"][config["summary_property"]]
    property_id = prop["id"]
    encoded_id = quote(unquote(property_id), safe="")
    full_property = api.list_all("GET", f"pages/{page['id']}/properties/{encoded_id}")
    existing = [item["rich_text"] for item in full_property]
    children = api.list_all("GET", f"blocks/{page['id']}/children")
    managed = [item for item in children if item["type"] == "code" and
               plain_text(item["code"].get("caption", [])) == caption]
    if len(managed) > 1:
        raise ValueError("Multiple managed log blocks exist; resolve duplicates before rerunning.")
    merged = merge_summary(existing, summary)
    api.request("PATCH", f"pages/{page['id']}", {
        "properties": {config["summary_property"]: {"rich_text": merged}}})
    if managed:
        api.request("PATCH", f"blocks/{managed[0]['id']}", {"code": code})
    else:
        api.request("PATCH", f"blocks/{page['id']}/children", {"children": [block]})
    return page["url"]


def main() -> int:
    # Windows redirected consoles can otherwise use cp932 and reject note names.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="YYYY-MM-DD; defaults to yesterday in Japan")
    parser.add_argument("--dry-run", action="store_true", help="Print the log; no Notion access")
    parser.add_argument("--config", type=Path, default=CONFIG)
    parser.add_argument("--repository", default=os.environ.get("GITHUB_REPOSITORY", "utimoriNI/Garden"))
    args = parser.parse_args()
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repository):
        raise ValueError("--repository must be owner/repo.")
    target = log_date(args.date)
    if target > datetime.now(JST).date():
        raise ValueError("Cannot log a future date.")
    config = json.loads(args.config.read_text(encoding="utf-8"))
    config["data_source_id"] = os.environ.get("NOTION_DATA_SOURCE_ID") or config["data_source_id"]
    commits = collect_commits(target, config.get("exclude_paths", []))
    summary, details = render_log(target, args.repository, commits)
    if args.dry_run:
        print(details)
        return 0
    if not commits:
        print(f"No commits on {target} (Japan time); no Notion changes.")
        return 0
    token = os.environ.get("NOTION_TOKEN", "").strip()
    if not token:
        raise ValueError("Set the NOTION_TOKEN GitHub Actions secret before running.")
    url = sync_log(Notion(token), config, target, args.repository, summary, details)
    print(f"Synced {target}: {len(commits)} commits. {url}")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
            output.write(f"{summary}\n\n[Notionログ]({url})\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError, HTTPError, OSError, subprocess.CalledProcessError) as error:
        print(f"Daily log failed: {error}", file=sys.stderr)
        raise SystemExit(1)
