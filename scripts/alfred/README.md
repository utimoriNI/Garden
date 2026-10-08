# Garden Daily Memo

Alfredからプロジェクトを選び、作業ログ・行き詰まり・Taskを今日のDaily Note末尾へ追加します。Alfred PowerpackとPython 3が必要です。このMacでは`/usr/bin/python3`を使用します。

## 導入

`Garden Daily Memo.alfredworkflow`をダブルクリックし、AlfredでImportを押します。既存のLifelogは変更しません。

## 使い方

1. Alfredで`log `（作業ログ）、`stuck `（行き詰まり）、`task `（Task）のいずれかを入力します。
2. プロジェクト名を入力して候補を絞り、Enterで選びます。「プロジェクトを指定しない」も選べます。
3. 表示されたダイアログへ本文を入力します。作業ログのみ、続いて任意メモを入力します。
4. 「記録」を押すと追記します。キャンセルや空の本文では記録しません。任意メモのキャンセルは記録全体を中止します。

初回にmacOSの許可ダイアログが出た場合は、AlfredからSystem Eventsの操作を許可してください。入力ダイアログを表示するために使います。

出力例は以下のとおりです。

```markdown
- 14:30 [[800_Project/InProgress/個人アプリ開発]] #📝Log ログイン画面を作成した ／ メモ：次は動作確認をする
- 15:10 #🪨Stack 認証エラーの原因が分からない
- [ ] 16:00 #📎Task 画面遷移のログを確認する
```

プロジェクトはファイルパスのみを列挙し、本文は読みません。改行などの空白は一行へまとめます。時刻・日付はMacのローカル時刻を使用します。

## 設定

AlfredのWorkflowsでGarden Daily Memoを選び、Workflowの変数設定で以下を変更できます。

| 変数 | 初期値 | 用途 |
| --- | --- | --- |
| `vault_path` | このGarden Vaultの絶対パス | Vaultの場所 |
| `project_folder` | `800_Project/InProgress` | Vaultからの相対パス |
| `recursive` | `1` | `1`でサブフォルダも検索、`0`で直下のみ |

Daily Noteの保存先・テンプレートは`.obsidian/daily-notes.json`から読みます。日付形式は`YYYY-MM-DD`に対応しています。今日のノートがなければテンプレートから新規作成します。`{{date}}`・`{{time}}`・`{{title}}`と、現在のテンプレートの前日・翌日リンクを展開します。未対応の式がある場合は書き込みを止めるので、Obsidianで今日のノートを先に作成してください。

Mac版はショートカットを経由せずローカルMarkdownへ直接追記します。既存本文は書き換えません。Obsidian Syncが有効なら通常のファイル変更として同期されます。このワークフロー同士の書き込みは直列化しますが、Obsidianや他端末との同時編集をロックするものではありません。

失敗時はAlfredのワークフローデバッガーを確認してください。使用をやめる場合はワークフローを削除します。

## 再ビルド

Vaultルートから`python3 scripts/alfred/build_workflow.py`を実行すると配布ファイルを再生成します。インポート済みのワークフローには自動反映されないため、再インポートしてください。
