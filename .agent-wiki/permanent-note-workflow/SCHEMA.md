# Permanent Note Candidate Schema

## Boundary

- Source notes remain unchanged.
- AI-generated candidates live below `.agent-wiki/permanent-note-workflow/candidates/`.
- Approved Reading Notes are created in `300_Input/Reading Notes`.
- Approved Permanent Notes are created in `600_Knowledge` with `type: knowledge`.
- A Permanent Note must state one claim synthesized from at least two distinct source notes.
- A link-only collection is a MOC and stays in the separate Theme Discovery workflow.

## Decision state

- `pending`: not reviewed
- `hold`: keep for later
- `approved`: authorized for promotion
- `rejected`: do not promote

## Apply state

- `not-applied`: no official note has been created
- `applied`: the official note was created and `promoted_to` records it
- `error`: reserved for a reviewed processing error

Changing `decision` in a Base only edits the candidate file. Promotion is a separate, explicit operation.

## Reading Note candidate

Required:

- `type: reading-note-candidate`
- unique `candidate_id`
- `decision`
- `apply_status`
- `proposed_title`
- safe `target_path` below `300_Input/Reading Notes`
- `source_container`
- non-empty `## Fragment`

## Permanent Note candidate

Required:

- `type: permanent-note-candidate`
- unique `candidate_id`
- `decision`
- `apply_status`
- `proposed_title`
- one-sentence `claim`
- safe `target_path` below `600_Knowledge`
- at least two distinct wikilinks in `sources`
- non-empty `## Draft`

Strong candidates also include `## Evidence Map` and `## Counterpoints and Limits`.

## Promotion safety

The processor must:

1. validate every candidate before writing
2. process only `decision: approved`
3. refuse to overwrite an existing target
4. create one official note per candidate
5. update only the candidate audit fields
6. never modify or delete source notes
