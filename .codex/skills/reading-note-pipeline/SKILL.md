---
name: reading-note-pipeline
description: Kindle 収集マーカー（%% pick %% / %% group: ... %% / %% title: ... %%）や 🧩rn/candidate タグをもとに一節ノートを作成し、作成後に収集マーカーや候補タグを片付けるときに使う。
---

# Reading Note 生成フロー

この skill は、この Vault で一節ノート化の一連の流れをまとめて実行するときに使う。

- `400_Kindle` にある `%% pick %%` / `%% group: ... %%` / `%% title: ... %%` を読む
- `300_Input` にある `%% pick %%` / `%% group: ... %%` / `%% title: ... %%` を読む
- `🧩rn/candidate` が付いた既存ノートを `reading-note` に寄せる
- `300_Input/Reading Notes` に一節ノートを生成する
- 成功後、`400_Kindle` から収集マーカーを削除する
- `🧩rn/candidate` は変換時に削除する
- candidate から変換したノートも `300_Input/Reading Notes` に集約する

## 使う場面

次のような依頼ではこの skill を使う。

- 「一節ノートを作成して」
- 「収集マーカーを元に reading-note を作って」
- 「`🧩rn/candidate` を reading-note 化して」
- 「作成後に `pick` / `group` / `title` を消して」

## 前提

- 作業ディレクトリは Vault ルート (`/Users/isikurahiromitu/Documents/Garden`) を使う
- Kindle 原本は `400_Kindle`
- 生成先は `300_Input/Reading Notes`
- `🧩rn/candidate` は frontmatter の `tags` に付いていることを前提にする
- [タグ保存用.md](/Users/isikurahiromitu/Documents/Garden/200_Inbox/タグ保存用.md) はサジェスト用なので candidate 変換の対象外とする

## 既存スクリプト

- Kindle 生成: [`scripts/generate_kindle_reading_notes.py`](/Users/isikurahiromitu/Documents/Garden/scripts/generate_kindle_reading_notes.py)
- candidate 変換: [`scripts/convert_rn_candidate_notes.py`](/Users/isikurahiromitu/Documents/Garden/scripts/convert_rn_candidate_notes.py)

## 基本手順

通常は、次の補助スクリプトを優先して使う。

```bash
python3 .codex/skills/reading-note-pipeline/scripts/process_reading_note_collection.py
```

この補助スクリプトは次を順番に行う。

1. `🧩rn/candidate` が付いたノートを `reading-note` 化する
2. Kindle 収集マーカーから一節ノートを生成する
3. `300_Input` の marker 付き引用や発言から一節ノートを生成する
4. `400_Kindle` の `%% pick %%` / `%% group: ... %%` / `%% title: ... %%` を削除する
5. `400_Kindle` に収集マーカーが残っていないか確認する

## 個別実行が必要な場合

一部だけ動かしたい場合は、既存スクリプトを直接使ってよい。

```bash
python3 scripts/convert_rn_candidate_notes.py
python3 scripts/generate_kindle_reading_notes.py
```

収集マーカー削除だけをもう一度行いたい場合は、補助スクリプトに `--cleanup-only` を付ける。

```bash
python3 .codex/skills/reading-note-pipeline/scripts/process_reading_note_collection.py --cleanup-only
```

## 確認ポイント

処理後は次を確認する。

- `300_Input/Reading Notes` に新しい一節ノートができている
- `🧩rn/candidate` が対象ノートの `tags` から消えている
- `400_Kindle` に `%% pick %%` / `%% group: ... %%` / `%% title: ... %%` が残っていない

必要なら次のように確認する。

```bash
rg -n "🧩rn/candidate" -g '*.md' .
rg -n "%% (pick|group:|title:)" 400_Kindle -g '*.md'
```

## 安全なデフォルト

- `400_Kindle` 以外の説明文や日報に書かれた `%% pick %%` などは削除しない
- `🧩rn/candidate` は説明文の文字列ではなく frontmatter の `tags` だけを対象にする
- [タグ保存用.md](/Users/isikurahiromitu/Documents/Garden/200_Inbox/タグ保存用.md) は変換しない
- 変換や生成に失敗したら、収集マーカー削除には進まない
