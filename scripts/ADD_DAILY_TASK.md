---
title: Windowsからデイリーノートへタスクを追加
type: documentation
created: 2026-10-07
---

# Windowsからデイリーノートへタスクを追加

PowerToysのCommand Paletteを開き、`task`と入力するとタスク入力ウィンドウが開く。別名`task`を「直接」で登録しているので、候補選択や末尾のスペースは不要。本文を入れてEnterを押すと、今日のデイリーノートの末尾へ`- [ ] #📎Task 本文`を追加する。キャンセルや空欄では書き込まない。Windowsのスタートメニューでは「task - Obsidian タスク追加」からも起動できる。

実装は`scripts/windows/ObsidianTaskLauncher.cs`。`scripts/windows/install_daily_task_launcher.ps1`でコンパイル・登録する。実行ファイルはVault外の`D:\Obsidian\Garden-tools\ObsidianTaskLauncher`に置く。通常の起動時にPowerShellやコンソールは使わない。旧版の`scripts/add_daily_task.ps1`は手動実行用に残している。

保存先は`.obsidian/daily-notes.json`の`folder`を読む。既存ノートは末尾へ追記し、今日のノートがない場合は現在のDailyテンプレートから作成する。テンプレートの前日・翌日リンクと`{{date}}`、`{{time}}`、`{{title}}`を展開する。未対応のテンプレート式があれば、Obsidianで今日のノートを先に作成するようエラーを出す。

Windows側のショートカットはユーザーのスタートメニューに置く。Command PaletteのBookmarksにも`task`として実行ファイルを登録し、同じコマンドへ別名`task`を「直接」で割り当てる。設定の変更前にbookmarks.jsonとsettings.jsonを実行ファイルのフォルダーへバックアップする。再インストール時はCommand Paletteを終了してからスクリプトを実行し、終了後に起動して設定を読み直す。URLのプレースホルダー、Obsidian CLI、クリップボード、GitHubの同期を使わず、ローカルMarkdownへ直接追記する。Obsidian Syncを有効にしている場合は、そのファイルの変更として同期される。

ランチャーはWindows専用。Vaultを移動した場合はインストールスクリプトを再実行する。使用をやめる場合はCommand Paletteの別名`task`を空欄に戻し、`task`ブックマークとスタートメニューの該当ショートカットを削除する。
