#!/usr/bin/env python3
"""Validate and promote approved Reading/Permanent Note candidate files.

Candidate meaning is authored by an AI or human. This script only performs the
deterministic, safety-sensitive part: validation, change preview, no-overwrite
creation of official notes, and audit-state updates on candidate files.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
import sys
from typing import Iterable


FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n?", re.DOTALL)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$")
USER_COMMENT_RE = re.compile(
    r"<!--\s*user-comment:start\s*-->(.*?)<!--\s*user-comment:end\s*-->",
    re.DOTALL,
)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
VALID_DECISIONS = {"pending", "hold", "approved", "rejected"}
VALID_APPLY_STATUSES = {"not-applied", "applied", "error"}
CANDIDATE_ROOT = "200_Inbox/Note Candidates"


@dataclass(frozen=True)
class CandidateKind:
    name: str
    note_type: str
    candidate_folder: str
    target_folder: str


KINDS = {
    "reading": CandidateKind(
        name="reading",
        note_type="reading-note-candidate",
        candidate_folder="reading-note-candidates",
        target_folder="300_Input/Reading Notes",
    ),
    "permanent": CandidateKind(
        name="permanent",
        note_type="permanent-note-candidate",
        candidate_folder="permanent-note-candidates",
        target_folder="600_Knowledge",
    ),
}


@dataclass
class Candidate:
    path: Path
    relative_path: str
    kind: CandidateKind
    frontmatter_lines: list[str]
    metadata: dict[str, str | list[str]]
    body: str
    sections: dict[str, str]

    @property
    def candidate_id(self) -> str:
        return scalar(self.metadata, "candidate_id")

    @property
    def decision(self) -> str:
        return scalar(self.metadata, "decision")

    @property
    def apply_status(self) -> str:
        return scalar(self.metadata, "apply_status")

    @property
    def proposed_title(self) -> str:
        return scalar(self.metadata, "proposed_title")

    @property
    def target_path(self) -> str:
        return scalar(self.metadata, "target_path")


def yaml_unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def yaml_quote(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def parse_inline_list(value: str) -> list[str]:
    inside = value.strip()[1:-1].strip()
    if not inside:
        return []
    return [yaml_unquote(part) for part in inside.split(",") if part.strip()]


def parse_frontmatter(lines: list[str]) -> dict[str, str | list[str]]:
    result: dict[str, str | list[str]] = {}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line or line.startswith((" ", "\t")) or ":" not in line:
            index += 1
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()
        if raw_value.startswith("[") and raw_value.endswith("]"):
            result[key] = parse_inline_list(raw_value)
            index += 1
            continue
        if raw_value:
            result[key] = yaml_unquote(raw_value)
            index += 1
            continue

        values: list[str] = []
        lookahead = index + 1
        while lookahead < len(lines):
            item_line = lines[lookahead]
            if item_line.startswith("  - "):
                values.append(yaml_unquote(item_line[4:].strip()))
                lookahead += 1
                continue
            break
        result[key] = values if values else ""
        index = lookahead
    return result


def scalar(metadata: dict[str, str | list[str]], key: str) -> str:
    value = metadata.get(key, "")
    return value if isinstance(value, str) else ""


def list_value(metadata: dict[str, str | list[str]], key: str) -> list[str]:
    value = metadata.get(key, [])
    return value if isinstance(value, list) else []


def parse_sections(body: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = ""
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match:
            current = match.group(1).strip()
            sections.setdefault(current, [])
            continue
        if current:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def section_value(candidate: Candidate, *names: str) -> str:
    """Return the first non-empty section, supporting old English headings."""
    for name in names:
        value = candidate.sections.get(name, "")
        if value:
            return value
    return ""


def pending_user_comment(candidate: Candidate) -> str:
    """Collect outstanding feedback from frontmatter and the editable body marker."""
    comments: list[str] = []
    property_comment = scalar(candidate.metadata, "review_comment").strip()
    if property_comment:
        comments.append(property_comment)
    match = USER_COMMENT_RE.search(candidate.body)
    if match:
        body_comment = HTML_COMMENT_RE.sub("", match.group(1)).strip()
        if body_comment:
            comments.append(body_comment)
    return "\n\n".join(comments)


def candidate_link(relative_path: str) -> str:
    return f"[[{Path(relative_path).with_suffix('').as_posix()}]]"


def split_note(path: Path) -> tuple[list[str], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("frontmatter is missing")
    return match.group(1).splitlines(), text[match.end() :]


def discover_candidates(vault_root: Path, kind_name: str = "all") -> list[Candidate]:
    selected = KINDS.values() if kind_name == "all" else [KINDS[kind_name]]
    root = vault_root / CANDIDATE_ROOT
    candidates: list[Candidate] = []
    for kind in selected:
        folder = root / kind.candidate_folder
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.md")):
            relative_path = path.relative_to(vault_root).as_posix()
            try:
                frontmatter_lines, body = split_note(path)
            except (OSError, UnicodeError, ValueError) as exc:
                candidates.append(
                    Candidate(
                        path=path,
                        relative_path=relative_path,
                        kind=kind,
                        frontmatter_lines=[],
                        metadata={"_load_error": str(exc)},
                        body="",
                        sections={},
                    )
                )
                continue
            metadata = parse_frontmatter(frontmatter_lines)
            candidates.append(
                Candidate(
                    path=path,
                    relative_path=relative_path,
                    kind=kind,
                    frontmatter_lines=frontmatter_lines,
                    metadata=metadata,
                    body=body,
                    sections=parse_sections(body),
                )
            )
    return candidates


def resolved_target(vault_root: Path, candidate: Candidate) -> Path:
    relative = Path(candidate.target_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError("target_path must be a safe vault-relative path")
    target = (vault_root / relative).resolve()
    try:
        target.relative_to(vault_root.resolve())
    except ValueError as exc:
        raise ValueError("target_path escapes the vault") from exc
    return target


def validate_candidate(candidate: Candidate, vault_root: Path) -> list[str]:
    errors: list[str] = []
    load_error = scalar(candidate.metadata, "_load_error")
    if load_error:
        return [load_error]

    note_type = scalar(candidate.metadata, "type")
    if note_type != candidate.kind.note_type:
        errors.append(f"type must be {candidate.kind.note_type}")
    if not candidate.candidate_id:
        errors.append("candidate_id is required")
    if candidate.decision not in VALID_DECISIONS:
        errors.append(f"decision must be one of {sorted(VALID_DECISIONS)}")
    if candidate.apply_status not in VALID_APPLY_STATUSES:
        errors.append(f"apply_status must be one of {sorted(VALID_APPLY_STATUSES)}")
    if not candidate.proposed_title:
        errors.append("proposed_title is required")
    if not candidate.target_path:
        errors.append("target_path is required")
    elif not candidate.target_path.endswith(".md"):
        errors.append("target_path must end in .md")
    else:
        expected_prefix = candidate.kind.target_folder + "/"
        if not candidate.target_path.startswith(expected_prefix):
            errors.append(f"target_path must be inside {candidate.kind.target_folder}")
        try:
            resolved_target(vault_root, candidate)
        except ValueError as exc:
            errors.append(str(exc))

    if candidate.kind.name == "reading":
        if not scalar(candidate.metadata, "source_container"):
            errors.append("source_container is required")
        if not section_value(candidate, "抽出内容", "Fragment"):
            errors.append("## 抽出内容 is required")
    else:
        sources = list(dict.fromkeys(list_value(candidate.metadata, "sources")))
        if len(sources) < 2:
            errors.append("permanent-note candidates require at least two distinct sources")
        if not scalar(candidate.metadata, "claim"):
            errors.append("claim is required")
        if not section_value(candidate, "下書き", "Draft"):
            errors.append("## 下書き is required")

    if candidate.decision == "approved" and pending_user_comment(candidate):
        errors.append("unaddressed user comment must be reflected before approval")

    if candidate.apply_status == "applied":
        promoted_to = scalar(candidate.metadata, "promoted_to")
        if not promoted_to:
            errors.append("applied candidates require promoted_to")
        elif candidate.target_path and not (vault_root / candidate.target_path).exists():
            errors.append("apply_status is applied but target_path does not exist")
    return errors


def validate_candidates(
    candidates: list[Candidate], vault_root: Path
) -> dict[str, list[str]]:
    errors: dict[str, list[str]] = {}
    seen_ids: dict[str, str] = {}
    seen_targets: dict[str, str] = {}
    for candidate in candidates:
        candidate_errors = validate_candidate(candidate, vault_root)
        if candidate.candidate_id:
            if candidate.candidate_id in seen_ids:
                candidate_errors.append(
                    f"candidate_id duplicates {seen_ids[candidate.candidate_id]}"
                )
            else:
                seen_ids[candidate.candidate_id] = candidate.relative_path
        if candidate.target_path:
            if candidate.target_path in seen_targets:
                candidate_errors.append(
                    f"target_path duplicates {seen_targets[candidate.target_path]}"
                )
            else:
                seen_targets[candidate.target_path] = candidate.relative_path
        if candidate_errors:
            errors[candidate.relative_path] = candidate_errors
    return errors


def format_yaml_list(key: str, values: Iterable[str]) -> list[str]:
    values = list(values)
    if not values:
        return [f"{key}: []"]
    return [f"{key}:", *(f"  - {yaml_quote(value)}" for value in values)]


def reading_note_content(candidate: Candidate) -> str:
    metadata = candidate.metadata
    source_container = scalar(metadata, "source_container")
    links = list(dict.fromkeys([source_container, *list_value(metadata, "links")]))
    lines = [
        "---",
        "type: reading-note",
        f"source_type: {scalar(metadata, 'source_type') or 'legacy'}",
        f"source_container: {yaml_quote(source_container)}",
    ]
    source_url = scalar(metadata, "source_url")
    if source_url:
        lines.append(f"source_url: {yaml_quote(source_url)}")
    lines.extend(format_yaml_list("topic", list_value(metadata, "topic")))
    lines.extend(format_yaml_list("moc", list_value(metadata, "moc")))
    lines.extend(
        [
            "status: inbox",
            f"created: {scalar(metadata, 'created') or date.today().isoformat()}",
            f"candidate_id: {yaml_quote(candidate.candidate_id)}",
        ]
    )
    lines.extend(format_yaml_list("tags", list_value(metadata, "tags")))
    lines.extend(["---", "", f"# {candidate.proposed_title}", "", "## Fragment", ""])
    lines.extend(section_value(candidate, "抽出内容", "Fragment").splitlines())
    lines.extend(["", "## Memo", ""])
    memo = section_value(candidate, "メモ", "Memo")
    if memo:
        lines.extend(memo.splitlines())
    lines.extend(["", "## My Take", ""])
    my_take = section_value(candidate, "自分の考え", "My Take")
    if my_take:
        lines.extend(my_take.splitlines())
    lines.extend(["", "## Links", ""])
    lines.extend(f"- {link}" for link in links if link)
    return "\n".join(lines).rstrip() + "\n"


def permanent_note_content(candidate: Candidate) -> str:
    metadata = candidate.metadata
    sources = list(dict.fromkeys(list_value(metadata, "sources")))
    tags = list(dict.fromkeys(["Knowledge", *list_value(metadata, "tags")]))
    lines = [
        "---",
        "type: knowledge",
        "source_type: self",
        "source_container:",
    ]
    lines.extend(format_yaml_list("topic", list_value(metadata, "topic")))
    lines.extend(format_yaml_list("moc", list_value(metadata, "moc")))
    lines.extend(
        [
            "status: draft",
            f"created: {scalar(metadata, 'created') or date.today().isoformat()}",
            f"candidate_id: {yaml_quote(candidate.candidate_id)}",
        ]
    )
    lines.extend(format_yaml_list("derived_from", sources))
    lines.extend(format_yaml_list("tags", tags))
    lines.extend(
        [
            "---",
            "",
            f"# {candidate.proposed_title}",
            "",
            "## 要旨",
            "",
            scalar(metadata, "claim"),
            "",
            "## 本文",
            "",
        ]
    )
    lines.extend(section_value(candidate, "下書き", "Draft").splitlines())
    evidence = section_value(candidate, "根拠", "Evidence Map")
    if evidence:
        lines.extend(["", "## 根拠", "", *evidence.splitlines()])
    counterpoints = section_value(candidate, "反例・適用限界", "Counterpoints and Limits")
    if counterpoints:
        lines.extend(["", "## 反例・留保", "", *counterpoints.splitlines()])
    lines.extend(["", "## もとになったノート", ""])
    lines.extend(f"- {source}" for source in sources)
    return "\n".join(lines).rstrip() + "\n"


def set_frontmatter_scalar(lines: list[str], key: str, value: str) -> list[str]:
    replacement = f"{key}: {yaml_quote(value)}"
    result = list(lines)
    for index, line in enumerate(result):
        if line.startswith(f"{key}:"):
            result[index] = replacement
            return result
    result.append(replacement)
    return result


def updated_candidate_content(candidate: Candidate) -> str:
    lines = set_frontmatter_scalar(candidate.frontmatter_lines, "apply_status", "applied")
    lines = set_frontmatter_scalar(
        lines,
        "promoted_to",
        f"[[{Path(candidate.target_path).with_suffix('').as_posix()}]]",
    )
    lines = set_frontmatter_scalar(lines, "applied_at", date.today().isoformat())
    return "---\n" + "\n".join(lines).rstrip() + "\n---\n" + candidate.body.lstrip("\n")


def approved_unapplied(candidates: list[Candidate]) -> list[Candidate]:
    return [
        candidate
        for candidate in candidates
        if candidate.decision == "approved" and candidate.apply_status != "applied"
    ]


def render_official(candidate: Candidate) -> str:
    if candidate.kind.name == "reading":
        return reading_note_content(candidate)
    return permanent_note_content(candidate)


def print_plan(candidates: list[Candidate]) -> None:
    if not candidates:
        print("No approved, unapplied candidates.")
        return
    for candidate in candidates:
        print(f"CREATE {candidate.target_path}")
        print(f"UPDATE {candidate.relative_path}: apply_status -> applied")


def apply_candidates(candidates: list[Candidate], vault_root: Path) -> int:
    conflicts = [
        candidate.target_path
        for candidate in candidates
        if resolved_target(vault_root, candidate).exists()
    ]
    if conflicts:
        for target in conflicts:
            print(f"ERROR target already exists; refusing to overwrite: {target}", file=sys.stderr)
        return 1

    for candidate in candidates:
        target = resolved_target(vault_root, candidate)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x", encoding="utf-8") as handle:
            handle.write(render_official(candidate))
        candidate.path.write_text(updated_candidate_content(candidate), encoding="utf-8")
        print(f"CREATED {candidate.target_path}")
        print(f"APPLIED {candidate.relative_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate, preview, and apply approved Garden note candidates."
    )
    parser.add_argument(
        "action", choices=("validate", "plan", "apply"), help="Operation to perform"
    )
    parser.add_argument(
        "--kind", choices=("all", "reading", "permanent"), default="all"
    )
    parser.add_argument(
        "--vault-root",
        default=str(Path(__file__).resolve().parent.parent),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Required with apply; without it apply only prints the plan",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    vault_root = Path(args.vault_root).resolve()
    candidates = discover_candidates(vault_root, args.kind)
    errors = validate_candidates(candidates, vault_root)
    if errors:
        for path, messages in errors.items():
            for message in messages:
                print(f"ERROR {path}: {message}", file=sys.stderr)
        print(f"Validation failed: {len(errors)} candidate file(s).", file=sys.stderr)
        return 1

    if args.action == "validate":
        print(f"Validated {len(candidates)} candidate file(s).")
        return 0

    selected = approved_unapplied(candidates)
    print_plan(selected)
    if args.action == "plan" or not args.write:
        if args.action == "apply" and not args.write:
            print("Dry run only. Add --write to apply these changes.")
        return 0
    return apply_candidates(selected, vault_root)


if __name__ == "__main__":
    raise SystemExit(main())
