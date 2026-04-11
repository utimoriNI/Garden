# Theme Discovery Agent Guide

This file defines how Codex should operate the theme discovery workflow by natural-language instruction.

## Principle

The user should not need to remember shell commands.

If the user asks in natural language for theme discovery maintenance, Codex should map the request to the appropriate script and run it.

## Default Action

When the user asks for any broad maintenance action related to:

- `theme discovery`
- `Life x Society`
- `MOC候補`
- `候補レポート`
- `reading-note から MOC を見つける`

Codex should default to running:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/moc_registry.json
```

Then Codex should summarize:

- which reports were updated
- what the notable candidates are
- whether human review is needed next

## Example Natural-Language Triggers

The following should all be interpreted as a request to run the standard cycle:

- `theme discovery を回して`
- `Life x Society の候補を更新して`
- `MOC候補レポートを出して`
- `reading-note から今のMOC候補を見直して`
- `テーマ発見フローを更新して`

The following should be interpreted as a request to inspect the latest outputs without necessarily rerunning:

- `最新の候補を見せて`
- `今どんなMOC候補がありますか`
- `直近のtheme discoveryの結果を説明して`

## Current Scope

Current standard scope:

- `Life x Society`

Current registry:

- `.agent-wiki/theme-discovery/configs/moc_registry.json`

## Safety

- Do not update human-facing MOCs automatically unless the user explicitly asks.
- Running the standard cycle is safe.
- Promotion into `110_MOC` still requires human intent.
