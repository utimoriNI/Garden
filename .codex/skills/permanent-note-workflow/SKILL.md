---
name: permanent-note-workflow
description: Generate AI-authored Reading Note candidates from selected Raindrop/Web source notes, discover one-claim Permanent Note candidates from multiple Fleeting/Reading Notes, and preview or apply candidates approved in an Obsidian Base. Use when the user asks to extract candidate notes from imported articles, find similar thoughts, create or update Permanent Note candidates, inspect approved changes, or promote approved candidates into 300_Input/Reading Notes or 600_Knowledge.
---

# Permanent Note Workflow

Keep AI proposals separate from official notes. Use Obsidian Base as the decision surface and the deterministic processor for no-overwrite promotion.

## Start

1. Read the vault-root `AGENTS.md`.
2. Read `.agent-wiki/permanent-note-workflow/SCHEMA.md` and `WORKFLOW.md` completely.
3. Read the matching template under `.agent-wiki/permanent-note-workflow/templates/`.
4. Preserve source notes and existing official notes.

## Choose the operation

- Article/Web extraction request: create Reading Note candidate files.
- Fleeting/Reading synthesis request: create Permanent Note candidate files.
- Change-preview request: run validation and plan only.
- Explicit apply/promote request: validate, show the plan, then apply approved candidates.
- Link-only theme request: use Theme Discovery; do not create a Permanent Note candidate.

## Create Reading Note candidates

Treat files with `raindrop_id` as source containers, including older imports whose `type` is still `reading-note`.

1. Read the requested source note completely.
2. Extract up to five reusable units per article: one quotation, concept, claim, scene, or expression per candidate.
3. Preserve quoted wording exactly. Do not invent source text.
4. Search existing candidates and official Reading Notes for the same `source_container` and fragment; skip duplicates.
5. Create files under `200_Inbox/Note Candidates/reading-note-candidates/` using the template.
6. Use a unique ASCII `candidate_id`, normally `rn-<raindrop-id>-<number>` or `rn-<date>-<short-slug>`.
7. Set `decision: pending` and `apply_status: not-applied`.
8. Run `python3 scripts/apply_note_candidates.py validate`.

Candidate creation is automatic when requested. Do not create the official Reading Note until approved and explicitly applied.

## Create Permanent Note candidates

1. Inspect relevant notes in `500_Fleeting` and `300_Input/Reading Notes`.
2. Group notes by repeated mechanism, tension, contrast, causal relation, or shared claim—not merely shared vocabulary.
3. Use at least two distinct sources; prefer three to eight when the claim remains coherent.
4. State one discussable claim in `claim`. A topic label is insufficient.
5. Write a usable initial synthesis in `## 下書き`.
6. Explain each source's contribution in `## 根拠`.
7. Include a real limitation, counterexample, or missing piece in `## 反例・適用限界`.
8. Check `600_Knowledge`, `110_MOC`, and existing candidates for duplication.
9. Create files under `200_Inbox/Note Candidates/permanent-note-candidates/` using the template.
10. Run validation.

Do not create a Permanent Note when the useful output is only a set of links. Route it to the MOC workflow instead.

## Refine candidates from user comments

Users can leave short feedback in the Base `review_comment` property or longer feedback between the `user-comment:start` and `user-comment:end` markers under `## ユーザーコメント`.

When the user asks to reflect or incorporate candidate comments:

1. Read every candidate with a non-empty `review_comment` or marker body.
2. Revise only the candidate proposal: title, claim, `## 下書き`, `## 根拠`, `## 反例・適用限界`, duplicate check, and planned changes as needed.
3. Preserve `decision`, `apply_status`, source notes, and official notes.
4. Append the date, original comment, and concise response under `## コメント反映履歴`.
5. Clear `review_comment` and reset the marker body to its placeholder after recording the history.
6. Re-run validation. If a comment requests a materially different claim, re-check source support and existing Knowledge/MOC duplication.

Candidates with an outstanding comment must not be promoted. The validator enforces this for `decision: approved` candidates.

## Preview approved changes

Run:

```bash
python3 scripts/apply_note_candidates.py validate
python3 scripts/apply_note_candidates.py plan
```

Report every file that would be created and every candidate audit field that would be updated. Do not apply on a preview-only request.

## Apply approved candidates

Only when the user explicitly requests reflection or promotion, run the preview first and then:

```bash
python3 scripts/apply_note_candidates.py apply --write
python3 scripts/apply_note_candidates.py validate
```

Summarize created official notes. Never work around an existing-target conflict; report it for human resolution.

## Safety

- Base approval changes only candidate frontmatter.
- Promotion creates new files and updates candidate audit fields only.
- Do not modify or delete source notes.
- Do not overwrite existing targets.
- Keep candidates as an audit trail after promotion.
- Keep official Permanent Notes at `status: draft` for later human editing.
