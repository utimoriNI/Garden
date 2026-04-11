# Theme Discovery System

This page describes the full system boundary for integrating `reading-note` files into the LLM wiki workflow.

## Base Layer

The base input layer is:

- `300_Input/Reading Notes`
- `type: reading-note`

This is the widest useful source set for theme discovery.

## Scope Layers

Theme discovery operates in nested scopes.

### 1. All Reading Notes

Use this when you want to understand the whole `reading-note` population:

- how many notes exist
- which notes are still not connected to MOCs
- what source mix exists
- which narrower scopes should be explored next

Registry:

- `.agent-wiki/theme-discovery/configs/all_reading_notes_registry.json`

### 2. Single-Tag Scopes

Use this when you want to discover themes within one asset category.

Current example:

- `Society only`

Registry:

- `.agent-wiki/theme-discovery/configs/society_only_registry.json`

### 3. Cross-Tag Scopes

Use this when you want sharper mid-level themes from overlapping note populations.

Current example:

- `Life x Society`

Registry:

- `.agent-wiki/theme-discovery/configs/moc_registry.json`

## Human-Facing Interpretation

The intended interpretation is:

- `All Reading Notes`
  - inventory and system integration
- `Society only`
  - within-tag exploration
- `Life x Society`
  - cross-tag theme discovery

## Principle

The whole `reading-note` set should be part of the LLM wiki system.

But not every scope serves the same purpose.

The broadest scope is for visibility and integration.
The narrower scopes are for thematic discovery and MOC growth.
