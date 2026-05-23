# Reading Note パイプライン

Vault の収集マーカーと候補タグをもとに、一節ノートを生成・整理するワークフローを実行する。

## 処理内容（順番に実行）

1. `🧩rn/candidate` が付いたノートを reading-note 化する
2. `400_Kindle` の収集マーカーから一節ノートを生成する
3. `300_Input` の収集マーカーから一節ノートを生成する
4. `400_Kindle` の収集マーカーを削除する
5. 残存マーカーを確認する

## 実行

Vault ルートで補助スクリプトを実行する：

```bash
python3 .codex/skills/reading-note-pipeline/scripts/process_reading_note_collection.py
```

## 個別実行（一部だけ動かしたい場合）

```bash
python3 scripts/convert_rn_candidate_notes.py
python3 scripts/generate_kindle_reading_notes.py
python3 scripts/generate_input_reading_notes.py
```

## クリーンアップのみ

```bash
python3 .codex/skills/reading-note-pipeline/scripts/process_reading_note_collection.py --cleanup-only
```

## 処理後の確認

```bash
rg -n "🧩rn/candidate" -g '*.md' .
rg -n "%% (pick|group:|title:)" 400_Kindle -g '*.md'
```

## 安全ルール

- `300_Input/Reading Notes` 内のファイルは直接編集しない
- `200_Inbox/タグ保存用.md` は変換対象から除外する
- 変換・生成に失敗したら、収集マーカー削除には進まない
- `🧩rn/candidate` は frontmatter の `tags` にあるものだけを対象にする
