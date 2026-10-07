---
title: Windowsからデイリーノートへタスクを追加
type: documentation
created: 2026-10-07
---

# Windowsからデイリーノートへタスクを追加

Windowsのスタートメニュー、またはPowerToysのアプリ検索から「Obsidian タスク追加」を起動する。入力欄にタスク本文を入れてEnterを押すと、今日のデイリーノートの末尾へ`- [ ] #📎Task 本文`を追加する。キャンセルや空欄では書き込まない。

実装は`scripts/add_daily_task.ps1`。保存先は`.obsidian/daily-notes.json`の`folder`を読む。既存ノートは末尾へ追記し、今日のノートがない場合は現在のDailyテンプレートから作成する。テンプレートの前日・翌日リンクと`{{date}}`、`{{time}}`、`{{title}}`を展開する。未対応のテンプレート式があれば、Obsidianで今日のノートを先に作成するようエラーを出す。

Windows側のショートカットはユーザーのスタートメニューに置く。URLのプレースホルダー、Obsidian CLI、クリップボード、GitHubの同期を使わず、ローカルMarkdownへ直接追記する。Obsidian Syncを有効にしている場合は、そのファイルの変更として同期される。

ランチャーはWindows専用。Vaultを移動した場合はショートカットのスクリプトパスも更新する。使用をやめる場合はスタートメニューの「Obsidian タスク追加」ショートカットを削除する。
