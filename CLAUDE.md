# Garden — Claude 作業ガイド

このファイルは、この Obsidian Vault で Claude が作業するときに参照する指示ファイルです。
詳細なルールは各参照先ドキュメントにあります。

---

## Vault の目的

再利用したい知識・断片を蓄積し、reading-note として正規化し、MOC や Knowledge に接続していく。
作業時は運用を壊さず、一貫した形で拡張することを優先する。

作業ディレクトリは Vault ルート（`D:\Obsidian\Garden`）を使う。
シェルコマンドを実行するときは、このディレクトリを起点とする。

---

## フォルダ構造

```
000_Main/         メインノート・ホーム
010_Topics/       トピック別ノート
100_Periodic/     定期ノート（日次・週次など）
110_MOC/          人間が管理するMOC（マップ・オブ・コンテンツ）
200_Inbox/        受信箱・未整理ノート
300_Input/        Web・動画クリップ、Reading Notes
  └─ Reading Notes/  一節ノート（reading-note）の生成先
400_Kindle/       Kindleハイライト原本
500_Fleeting/     フリーティングノート
600_Knowledge/    知識・抽象化ノート
800_Project/      プロジェクトノート
998_Resource/     リソース
999_Archive/      アーカイブ
.agent-wiki/      AIエージェント用wiki（Theme Discovery など）
.codex/skills/    旧Codex用スキル定義（参考資料として参照可）
scripts/          各種Pythonスクリプト
```

---

## タグ体系

| タグ | 役割 |
|------|------|
| `🎁Topic/Life` `🎁Topic/Society` `🎁Topic/Learning` 等 | 資産カテゴリ（大分類） |
| `🧩rn/candidate` | reading-note 化の候補（一時的） |

- `🎁Topic/...` は資産として残したいことを表す分類であり、構造タイプではない
- 構造的な運用は frontmatter（`type`, `status` など）で管理する
- タグを勝手に外さない。特に `🎁Topic/...` は明示的な依頼なしに削除しない

---

## Reading Note とは

`reading-note` は、あとで再利用しやすい最小単位のノート（1つの引用・概念・主張・言い回しなど）。
`reading-note` かどうかは frontmatter の `type` フィールドで判断する。

### 最小 frontmatter

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

### `source_type` の値の例

`kindle` / `web` / `video` / `legacy`

### `status` の値の例

`inbox`（デフォルト）/ `processed` / `archived`

---

## ソースレイヤー

| レイヤー | 説明 |
|----------|------|
| 原本ノート | Kindle import、Webクリップ、動画メモ |
| 候補ノート | `🧩rn/candidate` が付いた、まだ正規化していないノート |
| Reading Note | `300_Input/Reading Notes` にある正規化済みノート |
| Knowledge / MOC | 抽象化・整理済みのノート |

---

## 主なワークフロー

### 1. Reading Note の生成（reading-note-pipeline）

Kindle や 300_Input のマーカーから一節ノートを生成し、候補ノートを変換する。

**自然言語トリガー例：**
- 「一節ノートを作成して」
- 「収集マーカーを元に reading-note を作って」
- `🧩rn/candidate` を reading-note 化して」

**実行コマンド：**

```bash
python3 .codex/skills/reading-note-pipeline/scripts/process_reading_note_collection.py
```

個別に動かしたい場合：

```bash
python3 scripts/convert_rn_candidate_notes.py
python3 scripts/generate_kindle_reading_notes.py
python3 scripts/generate_input_reading_notes.py
```

**収集マーカーの記法（400_Kindle, 300_Input で使う）：**

| マーカー | 意味 |
|----------|------|
| `%% pick %%` | そのハイライト単体を1つの reading-note にする |
| `%% group: ... %%` | 同じグループ名を持つ複数ハイライトをまとめる |
| `%% title: ... %%` | 変換後の reading-note タイトルを指定する |

**確認ポイント：**

```bash
rg -n "🧩rn/candidate" -g '*.md' .
rg -n "%% (pick|group:|title:)" 400_Kindle -g '*.md'
```

詳細: `.codex/skills/reading-note-pipeline/SKILL.md`

---

### 2. Theme Discovery

reading-note から MOC 候補となるテーマを発見する半自動ワークフロー。
AIエージェントは提案を行い、110_MOC への反映は人間が承認する。

**主要タグスコープ：**

- `🎁Topic/Life` / `🎁Topic/Society` / `🎁Topic/Learning`（コアテーマ）

**自然言語トリガー → 対応コマンド：**

| 依頼の例 | 実行するコマンド |
|----------|----------------|
| 「theme discovery を回して」「Life / Society / Learning を見て」 | `core_thinking_topics_registry.json` |
| 「Life x Society の候補を更新して」「MOC候補レポートを出して」 | `moc_registry.json` |
| 「Life 単体で回して」 | `life_only_registry.json` |
| 「Society 単体で回して」 | `society_only_registry.json` |
| 「Learning 単体で回して」 | `learning_only_registry.json` |
| 「Life x Learning の候補を更新して」 | `life_learning_registry.json` |
| 「Society x Learning の候補を更新して」 | `society_learning_registry.json` |
| 「reading-note 全体を見て」「全 reading-note の棚卸しをして」 | `all_reading_notes_registry.json` |

**実行コマンド（例：コアテーマ）：**

```bash
python3 scripts/run_theme_discovery_cycle.py \
  --registry .agent-wiki/theme-discovery/configs/core_thinking_topics_registry.json
```

**実行後に要約すること：**
- どのレポートが更新されたか
- 注目すべき候補テーマ
- 人間レビューが必要な箇所

詳細: `.agent-wiki/theme-discovery/AGENTS.md` / `WORKFLOW.md` / `SYSTEM.md` / `SCHEMA.md`

---

### 3. 旧 Lexicon の移行

`🎁Topic/Lexicon` の旧ノートを reading-note スキーマに移行する（日常運用ではなく一括移行用）。

```bash
python3 scripts/migrate_lexicon_to_reading_notes.py
```

---

## ノート編集時のルール

- 明示的な依頼がない限り、本文を大きく書き換えない
- まず最小 frontmatter を足す方針を優先する
- `🎁Topic/...` タグは勝手に外さない
- `reading-note` 化が済んだら `🧩rn/candidate` を外す
- 既存ノートを大きく再設計するより、段階的に移行する
- `300_Input/Reading Notes` 内のファイルは直接編集しない（スクリプトで生成するもの）
- `110_MOC` 内のファイルは明示的な依頼がない限り編集しない

---

## 安全なデフォルト

- 1ノート = 1断片 と明確に言えないなら `reading-note` にしない
- 出典が分からなければ `source_type: legacy`
- `source_container` は推測で埋めず空欄にする
- `topic` や `moc` は無理に埋めない
- スクリプト実行前に対象ファイルを確認する
- 変換・生成に失敗したら、収集マーカー削除には進まない
- `タグ保存用.md`（`200_Inbox/タグ保存用.md`）はサジェスト用なので変換対象から除外する

---

## 参照ドキュメント一覧

| ドキュメント | 内容 |
|-------------|------|
| `AGENTS.md` | Vault 全体の基本ルール（旧来のメインガイド） |
| `.agent-wiki/theme-discovery/AGENTS.md` | Theme Discovery の自然言語操作ガイド |
| `.agent-wiki/theme-discovery/WORKFLOW.md` | Theme Discovery の定常フロー |
| `.agent-wiki/theme-discovery/SYSTEM.md` | スコープ設計の全体像 |
| `.agent-wiki/theme-discovery/SCHEMA.md` | テーマ発見の詳細スキーマ |
| `.codex/skills/reading-note-pipeline/SKILL.md` | 一節ノート生成フローの詳細 |
| `.codex/skills/obsidian-markdown/SKILL.md` | Obsidian Flavored Markdown の記法リファレンス |
| `.agent-wiki/theme-discovery/index.md` | 生成ファイルの軽量インデックス |
| `.agent-wiki/theme-discovery/log.md` | アクティビティログ（追記専用） |
