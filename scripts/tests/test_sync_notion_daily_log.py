from __future__ import annotations

from datetime import date, datetime, timezone
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError


SCRIPT = Path(__file__).resolve().parents[1] / "sync_notion_daily_log.py"
SPEC = importlib.util.spec_from_file_location("sync_notion_daily_log", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)
CONFIG = json.loads(MODULE.CONFIG.read_text(encoding="utf-8"))
TARGET = date(2026, 10, 3)
REPOSITORY = "utimoriNI/Garden"
CAPTION = f"Garden GitHub log | {REPOSITORY} | {TARGET}"


class FakeNotion:
    def __init__(self, pages=None, existing=None, blocks=None):
        self.pages = pages or []
        self.existing = existing or []
        self.blocks = blocks or []
        self.calls = []

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if path.startswith("data_sources/"):
            return {"properties": {"更新": {"type": "title"}, "更新日": {"type": "date"},
                                   "やったこと": {"type": "rich_text"}}}
        if method == "GET" and path.startswith("pages/"):
            return {"id": "page", "url": "https://notion.so/page", "properties": {
                "やったこと": {"id": "abc%3A", "rich_text": []}}}
        return {"id": "page", "url": "https://notion.so/page"}

    def list_all(self, method, path, body=None):
        self.calls.append((method, path, body))
        if path.endswith("/query"):
            return self.pages
        if "/properties/" in path:
            return [{"rich_text": item} for item in self.existing]
        return self.blocks

    def writes(self):
        return [(method, path, body) for method, path, body in self.calls
                if method != "GET" and not path.endswith("/query")]


class DailyLogTests(unittest.TestCase):
    def test_japan_midnight_and_manual_date(self):
        self.assertEqual(MODULE.log_date(None, datetime(2026, 10, 3, 15, 15, tzinfo=timezone.utc)), TARGET)
        self.assertEqual(MODULE.log_date(None, datetime(2026, 10, 3, 14, 59, tzinfo=timezone.utc)), date(2026, 10, 2))
        self.assertEqual(MODULE.log_date("2026-10-03"), TARGET)
        with self.assertRaises(ValueError):
            MODULE.log_date("20261003")

    def test_summary_preserves_handwritten_formatting_and_mentions(self):
        prefix = {"type": "mention", "mention": {"type": "page", "page": {"id": "id"}},
                  "plain_text": "Personal page", "annotations": {"bold": True}}
        body = MODULE.rich_text(f"\n{MODULE.BEGIN}\nold\n{MODULE.END}\nmy note")
        body[0]["annotations"] = {"italic": True}
        result = MODULE.merge_summary([prefix, *body], "new summary")
        self.assertEqual(result[0]["mention"], prefix["mention"])
        self.assertNotIn("plain_text", result[0])
        self.assertTrue(MODULE.plain_text(result).endswith("\nmy note"))
        self.assertEqual(result[-1]["annotations"], {"italic": True})
        result2 = MODULE.merge_summary(result[1:], "newer summary")
        self.assertEqual(MODULE.plain_text(result2).count(MODULE.BEGIN), 1)
        self.assertNotIn("new summary", MODULE.plain_text(result2))

    def test_damaged_markers_fail_without_erasing_content(self):
        for text in [MODULE.BEGIN, MODULE.END, MODULE.END + MODULE.BEGIN,
                     MODULE.BEGIN * 2 + MODULE.END]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                MODULE.merge_summary(MODULE.rich_text(text), "summary")

    def test_create_uses_existing_schema_and_isolates_daily_entry(self):
        api = FakeNotion()
        MODULE.sync_log(api, CONFIG, TARGET, REPOSITORY, "summary", "details")
        query = next(body for _, path, body in api.calls if path.endswith("/query"))
        self.assertEqual(len(query["filter"]["and"]), 2)
        self.assertIn("コミットログ", query["filter"]["and"][0]["title"]["equals"])
        [(method, path, body)] = api.writes()
        self.assertEqual((method, path), ("POST", "pages"))
        self.assertEqual(body["parent"]["data_source_id"], CONFIG["data_source_id"])
        self.assertEqual(set(body["properties"]), {"更新", "更新日", "やったこと"})
        self.assertEqual(body["properties"]["更新日"]["date"]["start"], "2026-10-03")

    def test_rerun_updates_managed_block_and_preserves_other_content(self):
        blocks = [{"id": "manual", "type": "paragraph", "paragraph": {}},
                  {"id": "managed", "type": "code", "code": {"caption": MODULE.rich_text(CAPTION)}}]
        api = FakeNotion([{"id": "page"}], MODULE.rich_text("handwritten"), blocks)
        MODULE.sync_log(api, CONFIG, TARGET, REPOSITORY, "summary", "details")
        writes = api.writes()
        self.assertEqual([(m, p) for m, p, _ in writes],
                         [("PATCH", "pages/page"), ("PATCH", "blocks/managed")])
        saved = writes[0][2]["properties"]["やったこと"]["rich_text"]
        self.assertTrue(MODULE.plain_text(saved).startswith("handwritten\n\n"))
        self.assertIn("pages/page/properties/abc%3A", [path for _, path, _ in api.calls])

    def test_recovers_page_created_without_managed_block(self):
        api = FakeNotion([{"id": "page"}])
        MODULE.sync_log(api, CONFIG, TARGET, REPOSITORY, "summary", "details")
        self.assertEqual(api.writes()[-1][1], "blocks/page/children")

    def test_duplicates_fail_before_writing(self):
        for api in [FakeNotion([{"id": "one"}, {"id": "two"}]),
                    FakeNotion([{"id": "page"}], blocks=[
                        {"id": str(i), "type": "code", "code": {"caption": MODULE.rich_text(CAPTION)}}
                        for i in range(2)])]:
            with self.subTest(api=api), self.assertRaises(ValueError):
                MODULE.sync_log(api, CONFIG, TARGET, REPOSITORY, "summary", "details")
            self.assertEqual(api.writes(), [])

    def test_large_reports_fit_notion_limits(self):
        api = FakeNotion()
        MODULE.sync_log(api, CONFIG, TARGET, REPOSITORY, "summary", "漢" * 200_000)
        payload = api.writes()[0][2]
        self.assertLess(len(json.dumps(payload, ensure_ascii=False).encode()), 450_000)
        parts = payload["children"][0]["code"]["rich_text"]
        self.assertLessEqual(len(parts), 100)
        self.assertTrue(all(len(part["text"]["content"]) <= 2000 for part in parts))
        self.assertIn("省略", MODULE.plain_text(parts))

    def test_query_and_block_pagination(self):
        api = MODULE.Notion("test")
        with patch.object(api, "request", side_effect=[
            {"results": [{"id": "1"}], "has_more": True, "next_cursor": "next"},
            {"results": [{"id": "2"}], "has_more": False},
        ]) as request:
            self.assertEqual(len(api.list_all("POST", "data_sources/id/query", {"filter": {}})), 2)
            self.assertEqual(request.call_args.args[2]["start_cursor"], "next")
            self.assertEqual(request.call_args.args[2]["filter"], {})

    def test_create_is_not_retried_after_ambiguous_server_error(self):
        error = HTTPError("https://api.notion.com", 503, "error", {},
                          io.BytesIO(b'{"code":"service_unavailable"}'))
        with patch.object(MODULE, "urlopen", side_effect=error) as send:
            with self.assertRaises(RuntimeError):
                MODULE.Notion("test").request("POST", "pages", {})
            self.assertEqual(send.call_count, 1)

    def test_actual_git_timezone_boundaries_and_out_of_order_dates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            MODULE.git("init", root=root)
            MODULE.git("config", "user.name", "Test", root=root)
            MODULE.git("config", "user.email", "test@example.com", root=root)
            for filename, timestamp in [
                ("before.md", "2026-10-02T14:59:59+00:00"),
                ("日本語のノート.md", "2026-10-02T15:00:00+00:00"),
                ("after.md", "2026-10-03T15:00:00+00:00"),
                ("old.md", "2026-10-01T10:00:00+00:00"),
                ("end.md", "2026-10-03T14:59:59+00:00"),
            ]:
                (root / filename).write_text("test", encoding="utf-8")
                MODULE.git("add", "--", filename, root=root)
                env = {**os.environ, "GIT_AUTHOR_DATE": timestamp, "GIT_COMMITTER_DATE": timestamp}
                subprocess.run(["git", "commit", "-m", filename], cwd=root, env=env,
                               check=True, capture_output=True)
            commits = MODULE.collect_commits(TARGET, [], root)
            self.assertEqual([c.subject for c in commits], ["日本語のノート.md", "end.md"])
            self.assertEqual(commits[0].changes, [("A", "日本語のノート.md")])
            summary, details = MODULE.render_log(TARGET, REPOSITORY, commits)
            self.assertIn("2コミット、2ノート", summary)
            self.assertIn("00:00:00", details)
            self.assertIn("23:59:59", details)
            self.assertEqual(len(MODULE.collect_commits(TARGET, ["*.md"], root)[0].changes), 0)


if __name__ == "__main__":
    unittest.main()
