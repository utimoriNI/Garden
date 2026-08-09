from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "apply_note_candidates.py"
SPEC = importlib.util.spec_from_file_location("apply_note_candidates", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


READING_CANDIDATE = """---
type: reading-note-candidate
candidate_id: 'rn-test-001'
decision: approved
apply_status: not-applied
proposed_title: '一つの断片'
target_path: '300_Input/Reading Notes/一つの断片.md'
source_type: web
source_container: '[[300_Input/Source Article]]'
source_url: 'https://example.com/article'
topic: []
moc: []
tags:
  - '🎁Topic/Life'
created: 2026-08-09
---

# 一つの断片

## Fragment

> 引用本文

## Memo

短いメモ。

## My Take

自分の反応。
"""


PERMANENT_CANDIDATE = """---
type: permanent-note-candidate
candidate_id: 'pn-test-001'
decision: approved
apply_status: not-applied
proposed_title: '可視化できる努力だけが評価される'
claim: '評価制度は努力全体ではなく、外から確認できる努力を選別する。'
target_path: '600_Knowledge/可視化できる努力だけが評価される.md'
sources:
  - '[[500_Fleeting/努力について]]'
  - '[[300_Input/Reading Notes/成果主義について]]'
topic: []
moc: []
tags:
  - '🎁Topic/Society'
created: 2026-08-09
---

# 可視化できる努力だけが評価される

## Draft

努力はそのまま観測できないため、評価制度は成果や説明可能な行動を代理指標として利用する。

## Evidence Map

- [[500_Fleeting/努力について]] は本人の経験を示す。
- [[300_Input/Reading Notes/成果主義について]] は制度側の論点を示す。

## Counterpoints and Limits

可視化は完全に否定できず、共同作業には一定の説明責任も必要になる。
"""


class CandidateWorkflowTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        reading_dir = self.root / ".agent-wiki/permanent-note-workflow/candidates/reading-note-candidates"
        permanent_dir = self.root / ".agent-wiki/permanent-note-workflow/candidates/permanent-note-candidates"
        reading_dir.mkdir(parents=True)
        permanent_dir.mkdir(parents=True)
        self.reading_path = reading_dir / "rn-test-001.md"
        self.permanent_path = permanent_dir / "pn-test-001.md"
        self.reading_path.write_text(READING_CANDIDATE, encoding="utf-8")
        self.permanent_path.write_text(PERMANENT_CANDIDATE, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_validate_and_apply_without_touching_sources(self) -> None:
        source = self.root / "300_Input/Source Article.md"
        source.parent.mkdir(parents=True)
        source.write_text("original source\n", encoding="utf-8")
        candidates = MODULE.discover_candidates(self.root)
        self.assertEqual({}, MODULE.validate_candidates(candidates, self.root))
        self.assertEqual(0, MODULE.apply_candidates(candidates, self.root))

        reading = self.root / "300_Input/Reading Notes/一つの断片.md"
        permanent = self.root / "600_Knowledge/可視化できる努力だけが評価される.md"
        self.assertTrue(reading.exists())
        self.assertTrue(permanent.exists())
        self.assertIn("type: reading-note", reading.read_text(encoding="utf-8"))
        self.assertIn("type: knowledge", permanent.read_text(encoding="utf-8"))
        self.assertIn("apply_status: 'applied'", self.reading_path.read_text(encoding="utf-8"))
        self.assertEqual("original source\n", source.read_text(encoding="utf-8"))

    def test_existing_target_is_never_overwritten(self) -> None:
        target = self.root / "300_Input/Reading Notes/一つの断片.md"
        target.parent.mkdir(parents=True)
        target.write_text("keep me\n", encoding="utf-8")
        candidates = MODULE.discover_candidates(self.root, "reading")
        self.assertEqual(1, MODULE.apply_candidates(candidates, self.root))
        self.assertEqual("keep me\n", target.read_text(encoding="utf-8"))
        self.assertIn("not-applied", self.reading_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
