# Theme Discovery Schema

This schema defines how the agent should maintain the theme discovery wiki for Garden.

## Purpose

The goal of this wiki is to discover mid-level themes from existing reading-notes.

The target granularity is not a high-level topic like `Life` or `Society`.
The target granularity is a theme like `計測と評価の歪み`:

- broad enough to gather several reading-notes
- narrow enough to become one MOC draft
- useful as a bridge from reading-notes to Knowledge / MOC

## Scope

Current scope is limited to reading-notes that belong to both:

- `🎁Topic/Life`
- `🎁Topic/Society`

The agent should treat the following as the source set:

- folder: `300_Input/Reading Notes`
- required frontmatter: `type: reading-note`
- required tags: both `🎁Topic/Life` and `🎁Topic/Society`

The Obsidian Base [`110_MOC/テーマ候補発見.base`](/Users/isikurahiromitu/Documents/Garden/110_MOC/テーマ候補発見.base) is the primary discovery surface.
Use the `Society x Life` view as the default entry point.

## Non-goals

This wiki does not replace human notes.
This wiki does not write final Knowledge notes automatically.
This wiki does not manage deadlines, commitments, or operational ground truth.
This wiki does not edit source reading-notes.

## Safety Rules

- Human notes are read-only.
- Never modify files in `300_Input/Reading Notes`.
- Never modify files in `110_MOC` unless explicitly requested.
- Never remove or rewrite existing human-written text.
- Keep all agent-generated outputs inside `.agent-wiki/theme-discovery/`.
- Do not change this schema without human approval.

## Output Structure

All outputs live under `.agent-wiki/theme-discovery/`.

- `clusters/`
  - bundles of related reading-notes
- `themes/`
  - theme proposals at mid-level granularity
- `moc-drafts/`
  - draft MOCs for promising themes
- `reports/`
  - candidate-link reports for existing human-facing MOCs
- `configs/`
  - per-MOC config files for report generation
- `index.md`
  - lightweight index of generated files
- `log.md`
  - append-only activity log

## Naming Rules

Use kebab-case ASCII file names for generated files.

Examples:

- `clusters/life-society-batch-01.md`
- `themes/life-society-proposals-01.md`
- `moc-drafts/measurement-and-evaluation-distortion.md`

## Theme Quality Rules

A good theme proposal should:

- be more specific than `Life` or `Society`
- connect at least 3 reading-notes
- usually connect no more than 8 reading-notes in the first pass
- reflect a shared tension, mechanism, pattern, or value conflict
- be usable as one MOC title with minimal rewriting

A weak theme proposal should be rejected if it is:

- just a restatement of a top-level tag
- only a source-book grouping with no clear shared idea
- too broad to guide Knowledge creation
- too narrow to connect multiple notes

## Evidence Rules

Each cluster and theme proposal must include:

- candidate title
- 1-2 sentence rationale
- linked supporting reading-notes
- short note on why these notes belong together

Prefer themes grounded in:

- repeated tensions
- recurring evaluative language
- similar social mechanisms
- shared critiques of norms, status, merit, recognition, pressure, or self-formation

## Standard Workflow

### Step 1: Select input batch

Read from the `Society x Life` view in `110_MOC/テーマ候補発見.base`.

For the first pass:

- start with roughly 20-30 notes
- prefer notes that share `source_book` or obvious conceptual overlap

### Step 2: Cluster notes

Create one file in `clusters/` that groups the batch into candidate bundles.

Each bundle should include:

- provisional bundle name
- 3-8 note links
- short rationale
- possible overlap with other bundles

### Step 3: Propose themes

Create one file in `themes/` based on the cluster file.

For each proposal include:

- proposed theme title
- why it is mid-level rather than high-level
- supporting note links
- nearby alternative titles
- whether it looks promising for a MOC

### Step 4: Draft an MOC

For the 1-3 best themes, create draft MOCs in `moc-drafts/`.

Each MOC draft should include:

- title
- short scope note
- grouped reading-note links
- 2-4 possible Knowledge note directions
- open questions or missing pieces

### Step 5: Update index and log

Whenever files are added:

- update `index.md`
- append an entry to `log.md`

## Steady-State Maintenance

Once a draft is promoted into `110_MOC`, the ongoing maintenance loop changes.

For promoted MOC candidates:

- generate a candidate-link report from new `reading-note` files
- let a human review the report
- only after approval, update the human-facing MOC and the note frontmatter

The current steady-state workflow is documented in:

- `.agent-wiki/theme-discovery/WORKFLOW.md`

## Query Behavior

When asked about theme discovery:

- read `index.md` first
- inspect relevant cluster/theme/MOC draft files
- cite the reading-notes behind the proposal
- present outputs as proposals, not facts

If there is uncertainty, say so explicitly.

## Lint Behavior

Periodic checks should look for:

- duplicate themes with different names
- overly broad themes
- themes with weak evidence
- clusters that should be merged or split
- MOC drafts that duplicate existing human MOCs
- unsupported claims not anchored in reading-notes

## Human Review Rules

The human remains the final editor and curator.

Only humans decide:

- which theme proposals are worth keeping
- which MOC drafts should be promoted to `110_MOC`
- which ideas should become Knowledge notes
- whether the schema itself should change

## First Run Target

The first run should only do this:

1. create one cluster file for `Society x Life`
2. create one theme proposal file from that cluster
3. create up to one MOC draft if a strong candidate appears

Keep the first run small and reviewable.
