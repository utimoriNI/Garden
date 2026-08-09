# Permanent Note Workflow

## Daily flow

1. Import selected Raindrop articles into `300_Input` as source notes, or capture thoughts in `500_Fleeting`.
2. Ask Codex to extract Reading Note candidates or discover Permanent Note candidates.
3. Review candidates in [[000_Main/Permanent Note候補.base]].
4. Edit `decision` to `approved`, `hold`, or `rejected`.
5. Ask Codex to preview approved changes.
6. Ask Codex to apply approved candidates.

## Candidate generation

### From Raindrop source articles

- Treat a note with `raindrop_id` as a source container even if it was imported under an older schema.
- Extract one reusable quotation, concept, claim, scene, or expression per Reading Note candidate.
- Preserve exact source wording in `## Fragment`.
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
