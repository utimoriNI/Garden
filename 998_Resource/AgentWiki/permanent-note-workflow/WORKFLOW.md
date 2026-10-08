# Permanent Note Workflow

## Daily flow

1. Import selected Raindrop articles into `300_Input` as source notes, or capture thoughts in `500_Fleeting`.
2. Ask Codex to extract Reading Note candidates or discover Permanent Note candidates.
3. Review candidates in [[000_Main/Permanent Note候補.base]].
4. If revisions are needed, write a short `review_comment` in the Base or a longer note under `## ユーザーコメント`.
5. Ask Codex to reflect the comments, then review the revised candidate and its comment history.
6. Edit `decision` to `approved`, `hold`, or `rejected`.
7. Ask Codex to preview approved changes.
8. Ask Codex to apply approved candidates.

## Candidate generation

### From Raindrop source articles

- Treat a note with `raindrop_id` as a source container even if it was imported under an older schema.
- Extract one reusable quotation, concept, claim, scene, or expression per Reading Note candidate.
- Preserve exact source wording in `## 抽出内容`.
- Do not invent text absent from the source.
- Create candidate files automatically; do not create official Reading Notes yet.

### From Fleeting and Reading Notes

- Look for repeated mechanisms, tensions, claims, contrasts, or cause-and-effect relationships.
- A Permanent Note candidate must combine at least two distinct notes.
- State one falsifiable or discussable claim rather than a topic label.
- Explain what each source contributes.
- Include a counterpoint, limitation, or unresolved question.
- Do not turn a list of related links into a Permanent Note; route that to Theme Discovery as an MOC candidate.

## Review UI

The Base is the human decision surface. Opening a row shows the candidate rationale, draft, and exact planned changes. Editing `decision` does not modify source or official notes.

Short comments can be entered in the Base `コメント` column. Longer comments can be written between the markers under `## ユーザーコメント` in the candidate file. Ask Codex `候補コメントを反映して` to revise the proposal. Codex records the original comment and response under `## コメント反映履歴`, then clears the outstanding comment. A candidate with unaddressed feedback must not be promoted.

## Apply cycle

Preview:

```bash
python3 scripts/apply_note_candidates.py validate
python3 scripts/apply_note_candidates.py plan
```

Apply after review:

```bash
python3 scripts/apply_note_candidates.py apply --write
```

After applying, rerun validation and summarize created notes.
