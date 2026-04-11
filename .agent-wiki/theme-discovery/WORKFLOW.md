# Theme Discovery Workflow

This document defines the steady-state workflow for keeping the `Life / Society / Learning` theme discovery flow running with low overhead.

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

Run the theme-discovery cycle for the scope you want to inspect.

Primary thematic source layer:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json
```

This updates the union scope for notes tagged with at least one of `Life`, `Society`, or `Learning`.

Current single-tag commands:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/life_only_registry.json
```

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/society_only_registry.json
```

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/learning_only_registry.json
```

Current cross-tag commands:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/moc_registry.json
```

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/life_learning_registry.json
```

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/society_learning_registry.json
```

The current maintained MOC-linked cross-tag path is still `Life x Society`.

This generates:

- `.agent-wiki/theme-discovery/reports/scopes/life-society-scope-report.md`
- `.agent-wiki/theme-discovery/runs/life-society-latest.md`
- `.agent-wiki/theme-discovery/reports/human-value-captured-by-metrics-report.md`

The registry can grow as more human-facing MOCs are added.

For `All Reading Notes`, use:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/all_reading_notes_registry.json
```

### 3. Human review

Review the generated scope report and per-MOC reports, then decide:

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

## Current Scope Configs

- `.agent-wiki/theme-discovery/configs/scopes/core-thinking-topics.json`
- `.agent-wiki/theme-discovery/configs/scopes/life-only.json`
- `.agent-wiki/theme-discovery/configs/scopes/society-only.json`
- `.agent-wiki/theme-discovery/configs/scopes/learning-only.json`
- `.agent-wiki/theme-discovery/configs/scopes/life-society.json`
- `.agent-wiki/theme-discovery/configs/scopes/life-learning.json`
- `.agent-wiki/theme-discovery/configs/scopes/society-learning.json`

## Current Registries

- `.agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json`
- `.agent-wiki/theme-discovery/configs/life_only_registry.json`
- `.agent-wiki/theme-discovery/configs/moc_registry.json`
- `.agent-wiki/theme-discovery/configs/learning_only_registry.json`
- `.agent-wiki/theme-discovery/configs/life_learning_registry.json`
- `.agent-wiki/theme-discovery/configs/society_learning_registry.json`
- `.agent-wiki/theme-discovery/configs/society_only_registry.json`

## Principle

The report layer should automate suggestion and reduce search cost.

The final shape of human-facing MOCs should still be decided by human review.

## Natural-Language Operation

The user should be able to request this workflow in natural language.

Default interpretation:

- if the user asks to `run theme discovery`
- if the user asks to `update Life / Society / Learning candidates`
- if the user asks for the main thematic discovery layer

then Codex should run the core thematic cycle:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json
```

If the user specifically asks to `update Life x Society candidates` or asks for `MOC candidate reports`, Codex should run:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/moc_registry.json
```

After the run, Codex should summarize the updated reports and the most relevant next review step.

Additional interpretation:

- if the user asks to `run Life-only discovery`
- if the user asks to `update Life candidates`
- if the user asks to `find relations only within Life`

then Codex should run:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/life_only_registry.json
```

- if the user asks to `run Society-only discovery`
- if the user asks to `update Society candidates`
- if the user asks to `find relations only within Society`

then Codex should run:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/society_only_registry.json
```

- if the user asks to `run Learning-only discovery`
- if the user asks to `update Learning candidates`
- if the user asks to `find relations only within Learning`

then Codex should run:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/learning_only_registry.json
```

- if the user asks to `run Life x Learning discovery`

then Codex should run:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/life_learning_registry.json
```

- if the user asks to `run Society x Learning discovery`

then Codex should run:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/society_learning_registry.json
```

If the user asks to inspect the whole `reading-note` layer or to integrate all `reading-note` files into the LLM wiki system, Codex should run:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/all_reading_notes_registry.json
```
