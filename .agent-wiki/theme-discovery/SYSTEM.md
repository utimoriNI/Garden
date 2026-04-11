# Theme Discovery System

This page describes the full system boundary for integrating `reading-note` files into the LLM wiki workflow.

## Base Layer

The base input layer is:

- `300_Input/Reading Notes`
- `type: reading-note`

This remains the widest useful source set for inventory and integration.

## Primary Thematic Layer

The primary thematic layer for the LLM wiki is narrower than the full `reading-note` set.

Current primary tags:

- `🎁Topic/Life`
- `🎁Topic/Society`
- `🎁Topic/Learning`

These three tags are treated as the main source population for theme discovery because they are closest to the user's enduring interests, values, judgments, and ways of understanding the world.

Other tags such as `Word`, `Rhetoric`, `Illust`, `DTM`, `Tech`, and `Omoro` are still part of the vault, but they should be interpreted more as preservation-oriented scrap layers unless the user explicitly asks to promote them into their own discovery scopes.

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

### 2. Core Thinking Topics

Use this when you want to inspect the full thematic source layer for the LLM wiki.

This scope includes any `reading-note` tagged with at least one of:

- `🎁Topic/Life`
- `🎁Topic/Society`
- `🎁Topic/Learning`

Registry:

- `.agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json`

### 3. Single-Tag Scopes

Use this when you want to discover themes within one asset category.

Current examples:

- `Life only`
- `Society only`
- `Learning only`

Registry:

- `.agent-wiki/theme-discovery/configs/life_only_registry.json`
- `.agent-wiki/theme-discovery/configs/society_only_registry.json`
- `.agent-wiki/theme-discovery/configs/learning_only_registry.json`

### 4. Cross-Tag Scopes

Use this when you want sharper mid-level themes from overlapping note populations.

Current examples:

- `Life x Society`
- `Life x Learning`
- `Society x Learning`

Registry:

- `.agent-wiki/theme-discovery/configs/moc_registry.json`
- `.agent-wiki/theme-discovery/configs/life_learning_registry.json`
- `.agent-wiki/theme-discovery/configs/society_learning_registry.json`

## Human-Facing Interpretation

The intended interpretation is:

- `All Reading Notes`
  - inventory and system integration
- `Core Thinking Topics`
  - the primary LLM wiki source layer for meaningful theme discovery
- `Life only`
  - within-tag exploration of values, judgment, emotion, and life guidance
- `Society only`
  - within-tag exploration
- `Learning only`
  - within-tag exploration of study, practice, and improvement
- `Life x Society`
  - cross-tag theme discovery
- `Life x Learning`
  - cross-tag discovery where personal growth and ways of learning overlap
- `Society x Learning`
  - cross-tag discovery where social structure and learning practice overlap

## Principle

The whole `reading-note` set should be part of the LLM wiki system.

But not every note population should be treated as equally central for thematic discovery.

The broadest scope is for visibility and integration.
The primary thematic layer is `Life / Society / Learning`.
The narrower scopes are for thematic discovery and MOC growth inside that layer.
