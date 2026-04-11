# Theme Discovery Workflow

This document defines the steady-state workflow for keeping the `Life x Society` theme discovery flow running with low overhead.

## Goal

Reduce the manual cost of:

- finding new `reading-note` candidates for existing MOCs
- deciding which notes should connect to a growing MOC
- keeping `.agent-wiki/` as the suggestion layer and `110_MOC/` as the human-facing layer

## Roles

### Agent

- scans `reading-note` files
- generates candidate reports
- proposes clusters, themes, and draft MOCs
- keeps `.agent-wiki/theme-discovery/` updated

### Human

- reviews candidate reports
- approves or rejects additions
- decides what gets promoted into `110_MOC`
- decides when a MOC is mature enough to produce Knowledge notes

## Steady-State Loop

### 1. New note creation

Create `reading-note` files as usual.

Minimum expectation:

- `type: reading-note`
- high-level topic tags are attached

### 2. Candidate report generation

Run the report generator for the target MOC.

Current command:

```bash
python3 scripts/generate_moc_link_report.py \
  --config .agent-wiki/theme-discovery/configs/human-value-captured-by-metrics.json
```

This generates:

- `.agent-wiki/theme-discovery/reports/human-value-captured-by-metrics-report.md`

### 3. Human review

Review the generated report and decide:

- which notes should be connected now
- which notes should be deferred
- which notes belong in a neighboring MOC instead

### 4. Approved update

After approval, update:

- the note's `moc` frontmatter
- the human-facing MOC body in `110_MOC/`

This step should remain human-approved.

### 5. Periodic discovery pass

When enough new notes accumulate:

- rerun cluster generation
- promote new mid-level themes
- draft new MOCs in `.agent-wiki/`

## Current Promotion Path

The current maintained path is:

1. `clusters/life-society-batch-01.md`
2. `themes/life-society-proposals-01.md`
3. `moc-drafts/human-value-captured-by-metrics.md`
4. `110_MOC/指標に回収される人間の価値_MOC.md`

## Current Human-Facing MOC

- `110_MOC/指標に回収される人間の価値_MOC.md`

## Current Report Config

- `.agent-wiki/theme-discovery/configs/human-value-captured-by-metrics.json`

## Principle

The report layer should automate suggestion and reduce search cost.

The final shape of human-facing MOCs should still be decided by human review.
