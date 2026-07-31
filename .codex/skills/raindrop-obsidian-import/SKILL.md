---
name: raindrop-obsidian-import
description: Import Raindrop.io items with the Obsidian trigger tag into the Garden vault's 300_Input as Obsidian-compatible Markdown, including Raindrop-to-🎁Topic tag mapping and duplicate prevention. Use when the user asks to import, sync, or pull Raindrop bookmarks tagged Obsidian into Obsidian.
---

# Raindrop to Obsidian Import

Use this skill for the Garden vault's Raindrop-to-Obsidian import workflow.

## Workflow

1. Read the vault's `AGENTS.md` before changing notes.
2. Confirm `RAINDROP_ACCESS_TOKEN` is present without printing its value. If it is missing, stop and tell the user to set it locally.
3. Run the existing importer from the vault root:

   ```bash
   python3 scripts/import_raindrop_obsidian_tag.py --dry-run
   ```

4. Review the preview. If the user requested the import itself, run the same command without `--dry-run`. If the user only asked for a preview, do not write files.
5. Summarize created and skipped notes. Existing notes are not overwritten; duplicate `source` URLs are skipped.

## Import behavior

- Default Raindrop trigger tag: `Obsidian`.
- Default completion tag: `ObsidianImported`.
- Destination: `300_Input`.
- The generated notes are automatically created as `type: reading-note`.
- The reading-note frontmatter includes `source_type` (`web` or `video`), `source_container`, `topic`, `moc`, and `status: inbox`, in addition to the existing Input fields such as `title`, `source`, `author`, `published`, `created`, `description`, `tags`, and `image`.
- `raindrop_id` is retained for provenance and duplicate prevention.
- After a successful import, `ObsidianImported` is appended to the Raindrop item.
- Items that already have `ObsidianImported` are skipped on later runs.
- Existing local duplicates without the completion tag are also marked as `ObsidianImported` during import.
- The trigger tag `Obsidian` is not written as an Obsidian tag.
- Raindrop tags are converted to the vault convention `🎁Topic/...`.
- Current explicit mappings:
  - `コミュニケーション` → `🎁Topic/Life`
  - `名文` → `🎁Topic/Rhetoric`
  - `例え` → `🎁Topic/Rhetoric`
- Unmapped tags fall back to `🎁Topic/<tag>`; `Topic/...` and `🎁Topic/...` are preserved in the vault convention.
- Defuddle is used automatically when the `defuddle` CLI is available. If extraction fails, the importer preserves Raindrop excerpt, notes, and highlights instead.

## Safety

- Never include or log the access token.
- Use `--dry-run` for an initial review, especially when importing many items.
- `--no-mark-imported` disables completion-tag updates when needed.
- The importer does not delete or remove any Raindrop tags.
