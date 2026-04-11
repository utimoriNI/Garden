# Theme Discovery Agent Guide

This file defines how Codex should operate the theme discovery workflow by natural-language instruction.

## Principle

The user should not need to remember shell commands.

If the user asks in natural language for theme discovery maintenance, Codex should map the request to the appropriate script and run it.

## Default Action

When the user asks for any broad maintenance action related to:

- `theme discovery`
- `Life / Society / Learning`
- `Life x Society`
- `MOC候補`
- `候補レポート`
- `reading-note から MOC を見つける`

Codex should default to running:

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json
```

If the request specifically mentions `Life x Society` or asks for current MOC candidate reports, Codex should run:

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
- `Life / Society / Learning を llm wiki に組み込んで`
- `Life と Society と Learning を見て`
- `主に考えに関わる reading-note を見て`
- `コアなテーマ発見を更新して`
- `Life x Society の候補を更新して`
- `MOC候補レポートを出して`
- `reading-note から今のMOC候補を見直して`
- `テーマ発見フローを更新して`

The following should be interpreted as a request to run the `Life only` cycle:

- `Life 単体で theme discovery を回して`
- `Life の候補を更新して`
- `Life タグだけで関連を見つけて`
- `Life の reading-note を束ねて`

The following should be interpreted as a request to run the `Society only` cycle:

- `Society 単体で theme discovery を回して`
- `Society の候補を更新して`
- `Society タグだけで関連を見つけて`
- `Society の reading-note を束ねて`

The following should be interpreted as a request to run the `Learning only` cycle:

- `Learning 単体で theme discovery を回して`
- `Learning の候補を更新して`
- `Learning タグだけで関連を見つけて`
- `Learning の reading-note を束ねて`

The following should be interpreted as a request to run the `Life x Learning` cycle:

- `Life x Learning の候補を更新して`
- `Life と Learning の交差を見て`

The following should be interpreted as a request to run the `Society x Learning` cycle:

- `Society x Learning の候補を更新して`
- `Society と Learning の交差を見て`

The following should be interpreted as a request to run the `All Reading Notes` cycle:

- `reading-note 全体を見て`
- `reading-note 全体を llm wiki に組み込む作業を進めて`
- `全 reading-note の状況を更新して`
- `reading-note 全体の棚卸しをして`

The following should be interpreted as a request to inspect the latest outputs without necessarily rerunning:

- `最新の候補を見せて`
- `今どんなMOC候補がありますか`
- `直近のtheme discoveryの結果を説明して`

## Current Scope

Current primary thematic layer:

- `Life`
- `Society`
- `Learning`

Additional supported scope:

- `All Reading Notes`
- `Core Thinking Topics`
- `Life only`
- `Society only`
- `Learning only`
- `Life x Society`
- `Life x Learning`
- `Society x Learning`

Current registry:

- `.agent-wiki/theme-discovery/configs/all_reading_notes_registry.json`
- `.agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json`
- `.agent-wiki/theme-discovery/configs/life_only_registry.json`
- `.agent-wiki/theme-discovery/configs/moc_registry.json`
- `.agent-wiki/theme-discovery/configs/learning_only_registry.json`
- `.agent-wiki/theme-discovery/configs/life_learning_registry.json`
- `.agent-wiki/theme-discovery/configs/society_learning_registry.json`
- `.agent-wiki/theme-discovery/configs/society_only_registry.json`

## Safety

- Do not update human-facing MOCs automatically unless the user explicitly asks.
- Running the standard cycle is safe.
- Promotion into `110_MOC` still requires human intent.
