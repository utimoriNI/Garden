# Theme Discovery

reading-note から MOC 候補となるテーマを発見するワークフローを実行する。
スコープを $ARGUMENTS で指定できる（省略時はコアテーマで実行）。

## 使い方

- `/project:theme-discovery` → コアテーマ（Life / Society / Learning）で実行
- `/project:theme-discovery life-society` → Life x Society で実行
- `/project:theme-discovery life` → Life 単体で実行
- `/project:theme-discovery all` → 全 reading-note で実行

## スコープ別コマンド

引数 $ARGUMENTS に応じて、以下のコマンドを Vault ルートで実行する。

### コアテーマ（デフォルト / "core" / 引数なし）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json
```

### Life x Society（"life-society" / "moc"）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/moc_registry.json
```

### Life 単体（"life"）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/life_only_registry.json
```

### Society 単体（"society"）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/society_only_registry.json
```

### Learning 単体（"learning"）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/learning_only_registry.json
```

### Life x Learning（"life-learning"）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/life_learning_registry.json
```

### Society x Learning（"society-learning"）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/society_learning_registry.json
```

### 全 reading-note（"all"）

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/all_reading_notes_registry.json
```

## 実行後に必ず行うこと

1. 更新されたレポートファイルを確認して要約する
2. 注目すべき候補テーマを提示する
3. 人間レビューが必要な箇所を明示する

## 安全ルール

- `300_Input/Reading Notes` 内のファイルは直接編集しない
- `110_MOC` への反映は人間の明示的な承認なしに行わない
- 提案は `.agent-wiki/theme-discovery/` 内に留める
- `.agent-wiki/theme-discovery/log.md` に作業ログを追記する
