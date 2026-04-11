#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

DEFAULT_TWEET_FIELDS = [
    "id",
    "text",
    "author_id",
    "created_at",
    "lang",
    "conversation_id",
    "public_metrics",
    "entities",
    "attachments",
    "referenced_tweets",
    "source",
]

DEFAULT_USER_FIELDS = [
    "id",
    "name",
    "username",
    "profile_image_url",
    "verified",
    "public_metrics",
]

DEFAULT_MEDIA_FIELDS = [
    "media_key",
    "type",
    "url",
    "preview_image_url",
    "width",
    "height",
    "alt_text",
]

DEFAULT_EXPANSIONS = [
    "author_id",
    "attachments.media_keys",
]


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text or "")


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def emit(payload: dict, exit_code: int) -> int:
    sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")
    return exit_code


def error_payload(error_type: str, message: str, **extra: object) -> dict:
    payload = {
        "ok": False,
        "error": {
            "type": error_type,
            "message": message,
        },
        "fetched_at": now_iso(),
    }
    if extra:
        payload["error"].update(extra)
    return payload


def parse_json_output(text: str) -> dict:
    cleaned = strip_ansi(text).strip()
    if not cleaned:
        raise ValueError("xurl returned empty output")
    decoder = json.JSONDecoder()
    parsed, _ = decoder.raw_decode(cleaned)
    return parsed


def run_xurl(command_args: List[str]) -> Tuple[int, str, str]:
    xurl_path = shutil.which("xurl")
    if not xurl_path:
        raise FileNotFoundError("xurl command not found in PATH")

    process = subprocess.run(
        [xurl_path, *command_args],
        capture_output=True,
        text=True,
        check=False,
    )
    return process.returncode, process.stdout, process.stderr


def build_query(params: Dict[str, object]) -> str:
    normalized = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, list):
            normalized[key] = ",".join(str(v) for v in value)
        else:
            normalized[key] = value
    return urlencode(normalized, doseq=False)


def fetch_auth_status(args: argparse.Namespace) -> Tuple[dict, int]:
    try:
        code, stdout, stderr = run_xurl(["auth", "status"])
    except FileNotFoundError as exc:
        return error_payload("missing_dependency", str(exc)), 127

    payload = {
        "ok": code == 0,
        "action": "auth-status",
        "fetched_at": now_iso(),
        "raw_text": strip_ansi(stdout).strip(),
    }
    if stderr.strip():
        payload["stderr"] = strip_ansi(stderr).strip()
    return payload, code


def fetch_me(args: argparse.Namespace) -> dict:
    endpoint = "/2/users/me?" + build_query(
        {
            "user.fields": DEFAULT_USER_FIELDS,
        }
    )
    command = []
    if args.app:
        command.extend(["--app", args.app])
    if args.username:
        command.extend(["--username", args.username])
    command.append(endpoint)
    code, stdout, stderr = run_xurl(command)
    parsed = parse_json_output(stdout)
    if code != 0:
        message = "failed to fetch /2/users/me"
        if stderr.strip():
            message = strip_ansi(stderr).strip()
        raise RuntimeError(json.dumps(error_payload("auth_error", message, raw=parsed), ensure_ascii=False))
    return parsed


def build_xurl_command(args: argparse.Namespace, endpoint: str) -> List[str]:
    command = []
    if args.app:
        command.extend(["--app", args.app])
    if args.username:
        command.extend(["--username", args.username])
    command.append(endpoint)
    return command


def normalize_includes(raw: dict) -> Tuple[Dict[str, dict], Dict[str, dict]]:
    users = {}
    for user in raw.get("includes", {}).get("users", []) or []:
        users[user.get("id")] = user

    media = {}
    for item in raw.get("includes", {}).get("media", []) or []:
        media[item.get("media_key")] = item

    return users, media


def normalize_tweets(raw: dict) -> List[dict]:
    users, media_index = normalize_includes(raw)
    items = []

    for tweet in raw.get("data", []) or []:
        author = users.get(tweet.get("author_id"), {})
        media_keys = (((tweet.get("attachments") or {}).get("media_keys")) or [])
        media_items = [media_index[key] for key in media_keys if key in media_index]
        username = author.get("username")
        items.append(
            {
                "id": tweet.get("id"),
                "text": tweet.get("text"),
                "created_at": tweet.get("created_at"),
                "lang": tweet.get("lang"),
                "conversation_id": tweet.get("conversation_id"),
                "source": tweet.get("source"),
                "public_metrics": tweet.get("public_metrics"),
                "author": {
                    "id": author.get("id"),
                    "name": author.get("name"),
                    "username": username,
                    "verified": author.get("verified"),
                    "profile_image_url": author.get("profile_image_url"),
                },
                "url": f"https://x.com/{username}/status/{tweet.get('id')}" if username and tweet.get("id") else None,
                "media": media_items,
                "entities": tweet.get("entities"),
                "referenced_tweets": tweet.get("referenced_tweets"),
            }
        )

    return items


def fetch_bookmarks(args: argparse.Namespace) -> Tuple[dict, int]:
    try:
        me = fetch_me(args)
    except FileNotFoundError as exc:
        return error_payload("missing_dependency", str(exc)), 127
    except RuntimeError as exc:
        return json.loads(str(exc)), 1
    except ValueError as exc:
        return error_payload("parse_error", str(exc)), 1

    user_id = (me.get("data") or {}).get("id")
    if not user_id:
        return error_payload("auth_error", "could not resolve current user id from /2/users/me"), 1

    endpoint = "/2/users/{user_id}/bookmarks?{query}".format(
        user_id=user_id,
        query=build_query(
            {
                "max_results": args.limit,
                "pagination_token": args.next_token,
                "expansions": DEFAULT_EXPANSIONS,
                "tweet.fields": DEFAULT_TWEET_FIELDS,
                "user.fields": DEFAULT_USER_FIELDS,
                "media.fields": DEFAULT_MEDIA_FIELDS,
            }
        ),
    )

    try:
        code, stdout, stderr = run_xurl(build_xurl_command(args, endpoint))
        raw = parse_json_output(stdout)
    except FileNotFoundError as exc:
        return error_payload("missing_dependency", str(exc)), 127
    except ValueError as exc:
        return error_payload("parse_error", str(exc)), 1

    if code != 0:
        message = strip_ansi(stderr).strip() or "xurl bookmarks request failed"
        return error_payload("api_error", message, raw=raw), code

    payload = {
        "ok": True,
        "action": "bookmarks",
        "fetched_at": now_iso(),
        "request": {
            "limit": args.limit,
            "next_token": args.next_token,
            "app": args.app,
            "username": args.username,
        },
        "summary": {
            "count": len(raw.get("data", []) or []),
            "next_token": ((raw.get("meta") or {}).get("next_token")),
        },
        "items": normalize_tweets(raw),
        "raw": raw,
    }
    return payload, 0


def fetch_search(args: argparse.Namespace) -> Tuple[dict, int]:
    if args.limit < 10 or args.limit > 100:
        return (
            error_payload(
                "invalid_argument",
                "search --limit must be between 10 and 100",
                parameter="limit",
                value=args.limit,
            ),
            2,
        )

    endpoint = "/2/tweets/search/recent?{query}".format(
        query=build_query(
            {
                "query": args.query,
                "max_results": args.limit,
                "next_token": args.next_token,
                "expansions": DEFAULT_EXPANSIONS,
                "tweet.fields": DEFAULT_TWEET_FIELDS,
                "user.fields": DEFAULT_USER_FIELDS,
                "media.fields": DEFAULT_MEDIA_FIELDS,
            }
        ),
    )

    try:
        code, stdout, stderr = run_xurl(build_xurl_command(args, endpoint))
        raw = parse_json_output(stdout)
    except FileNotFoundError as exc:
        return error_payload("missing_dependency", str(exc)), 127
    except ValueError as exc:
        return error_payload("parse_error", str(exc)), 1

    if code != 0:
        message = strip_ansi(stderr).strip() or "xurl search request failed"
        return error_payload("api_error", message, raw=raw), code

    payload = {
        "ok": True,
        "action": "search",
        "fetched_at": now_iso(),
        "request": {
            "query": args.query,
            "limit": args.limit,
            "next_token": args.next_token,
            "app": args.app,
            "username": args.username,
        },
        "summary": {
            "count": len(raw.get("data", []) or []),
            "next_token": ((raw.get("meta") or {}).get("next_token")),
        },
        "items": normalize_tweets(raw),
        "raw": raw,
    }
    return payload, 0


def write_output(payload: dict, output: Optional[str]) -> None:
    if not output:
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Structured JSON wrapper around xurl")
    parser.add_argument("--app", help="registered xurl app name")
    parser.add_argument("--username", help="registered xurl oauth2 username")
    parser.add_argument("--output", help="write JSON output to file")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--app", help="registered xurl app name")
    common.add_argument("--username", help="registered xurl oauth2 username")
    common.add_argument("--output", help="write JSON output to file")

    subparsers = parser.add_subparsers(dest="action", required=True)

    subparsers.add_parser("auth-status", help="check xurl auth status", parents=[common])

    bookmarks = subparsers.add_parser("bookmarks", help="fetch current user bookmarks", parents=[common])
    bookmarks.add_argument("--limit", type=int, default=20)
    bookmarks.add_argument("--next-token")

    search = subparsers.add_parser("search", help="search recent tweets", parents=[common])
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--next-token")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.action == "auth-status":
        payload, exit_code = fetch_auth_status(args)
    elif args.action == "bookmarks":
        payload, exit_code = fetch_bookmarks(args)
    else:
        payload, exit_code = fetch_search(args)

    write_output(payload, args.output)
    return emit(payload, exit_code)


if __name__ == "__main__":
    sys.exit(main())
