# Garden AGENTS Guide

This file defines the working conventions for this Obsidian vault.

## Purpose

This vault stores information that may become reusable knowledge assets.
Work in this repository should preserve that workflow and extend it consistently.

## Core Design

There are two separate concerns:

1. Whether a note is worth keeping as an asset
2. What structural type the note has

These concerns must not be mixed.

## Tags

`🎁Topic/...`
- Means the note is considered worth keeping as an asset.
- This is a broad asset classification.
- A note with this tag is not necessarily a `reading-note`.

`🧩rn/...`
- Used for reading-note related sub-classification.
- `🧩rn/candidate` is a temporary workflow tag.
- When a note is converted into a reading-note, remove `🧩rn/candidate`.

## Reading Notes

`reading-note` is a structural type for notes that represent a compact reusable unit such as:
- one quote
- one concept
- one claim
- one scene
- one phrasing

Reading notes are identified by frontmatter, not by `🎁Topic/...` alone.

Minimum frontmatter:

```yaml
---
type: reading-note
source_type: legacy
source_container:
topic: []
moc: []
status: inbox
---
```

### Property meanings

`type`
- Structural note type.
- Use `reading-note` for notes that should participate in the reading-note workflow.

`source_type`
- Source category such as `kindle`, `web`, `video`, or `legacy`.

`source_container`
- Link or pointer to the original source note when known.

`topic`
- Theme-oriented grouping.

`moc`
- Links to MOC notes.

`status`
- Workflow state.
- Default is `inbox`.

## Source Material Layers

Use these layers intentionally:

- Source notes: Kindle imports, web clips, article notes, video notes
- Candidate notes: notes marked for conversion
- Reading notes: normalized reusable units
- Knowledge/MOC notes: higher-level synthesis and organization

Do not collapse all layers into one note type.

## Kindle Workflow

Kindle source notes live in:

- `400_Kindle`

These are treated as editable source notes for selection.

### Supported markers in Kindle notes

`%% pick %%`
- Convert a single highlighted passage into a single reading note.

`%% group: ... %%`
- Group multiple highlighted passages into one reading note.

`%% title: ... %%`
- Override the reading note title.
- Works for both `pick` and `group`.

### Kindle conversion script

Use:

- [scripts/generate_kindle_reading_notes.py](/Users/isikurahiromitu/Documents/Garden/scripts/generate_kindle_reading_notes.py)

This script:
- reads flagged notes from `400_Kindle`
- creates reading notes in `200_Inbox/Reading Notes`
- supports `pick`, `group`, and `title`

## Candidate Conversion Workflow

When notes already exist in the vault and should become reading notes:

1. Add `🧩rn/candidate`
2. Convert them into `reading-note`
3. Remove `🧩rn/candidate`

Use:

- [scripts/convert_rn_candidate_notes.py](/Users/isikurahiromitu/Documents/Garden/scripts/convert_rn_candidate_notes.py)

This script:
- finds notes tagged `🧩rn/candidate`
- adds the minimum `reading-note` frontmatter when needed
- removes `🧩rn/candidate`

## Legacy Lexicon Migration

Older notes tagged `🎁Topic/Lexicon` were bulk-migrated into the reading-note schema.

Use:

- [scripts/migrate_lexicon_to_reading_notes.py](/Users/isikurahiromitu/Documents/Garden/scripts/migrate_lexicon_to_reading_notes.py)

This script is for legacy migration, not everyday note conversion.

## Classification Guidance

Use tags for broad and convenient navigation in Obsidian.
Use frontmatter for structural workflow.

Recommended split:

- `🎁Topic/...`: asset category
- `🧩rn/...`: reading-note specific subcategory
- `type`: structural note type
- `source_type`: source kind
- `status`: workflow state

Do not use `🎁Topic/...` alone to represent reading-note structure.

## Editing Rules

When modifying notes in this vault:

- Preserve existing content unless the task is explicitly a rewrite
- Prefer adding minimum frontmatter over redesigning a note
- Do not remove `🎁Topic/...` tags unless explicitly requested
- Remove `🧩rn/candidate` after successful conversion into a reading note
- Prefer incremental migration over large conceptual rewrites

## Safe Defaults

If classification is unclear:

- set `type: reading-note` only when the note clearly represents one reusable unit
- otherwise keep the note as-is
- use `source_type: legacy` when the source cannot be confidently inferred
- leave `source_container:` blank rather than guessing
- leave `topic` and `moc` empty rather than inventing values

## Expected Outcomes

Work in this repository should make it easier to:

- capture reusable fragments
- normalize them into reading notes
- review them later
- connect them to MOCs and knowledge notes
- preserve source traceability without overfitting the schema
