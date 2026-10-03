---
title: Notion日次ログ連携の引き継ぎ
type: documentation
status: setup-pending
created: 2026-10-03
---

# Notion日次ログ連携の引き継ぎ

このPCで続きを進めるための作業記録です。実装は完了しています。次はNotionとGitHubの認証設定を確認し、GitHub Actionsから初回の書き込みを検証します。日常運用の説明は [[scripts/NOTION_DAILY_LOG|Notion日次ログの設定・運用手順]] にあります。

## 目的と実装した動作

Gardenの1日分のコミット差分をOpenAI APIでトピックにまとめ、NotionのLogデータベースにトピックごとのレコードを作成・更新します。毎日、日本時間00:15に前日分を集計します。10月4日00:15の実行対象は10月3日です。GitHubにpush済みで、デフォルトブランチから到達できるコミットが対象です。

Notionには日付とトピックごとに専用の行を作ります。「やったこと」にトピックの要約を記録し、本文には関連コミットの時刻、メッセージ、作者、コミットURL、変更ファイル一覧を記録します。モデルへ送る差分は1日10万文字までです。

同じ日付を再実行すると既存の専用行を更新します。同日の通常のログや、手書きで追記した内容は保ちます。更新対象は「やったこと」の管理マーカー内と、管理キャプションを持つ専用コードブロックです。

## 2026年10月3日に確認した状態

| 項目                             | 状態                                                        |
| ------------------------------ | --------------------------------------------------------- |
| ワークフロー、同期スクリプト、設定ファイル          | 作成済み                                                      |
| 自動テスト                          | 11件成功。引き継ぎ文書の作成時にも再実行済み                                   |
| 実際のコミットを使ったローカルプレビュー           | 成功                                                        |
| ローカルブランチ                       | `main`                                                    |
| ローカルとGitHubのmain               | 文書作成前の確認で、両方とも `d3b0478729abb4a9de45b3598d4f68aeddc743dd` |
| NotionのLogスキーマ                 | 接続済みのNotionツールで確認済み                                       |
| GitHub SecretのNOTION_TOKEN     | 登録状況は未確認                                                  |
| GitHub SecretのOPENAI_API_KEY   | トピック要約に必要。登録状況は未確認                                        |
| Actions用のNotionインテグレーションの接続・権限 | 設定状況は未確認                                                  |
| GitHub Actionsからの本番書き込み        | 未検証                                                       |

上のコミットIDは確認時点の記録です。Obsidianの自動バックアップによって、その後もコミットが増えることがあります。GitHubへ反映済みであることと、Notionへの自動記録が動作することは別に確認します。

## 作業場所とファイル

| 用途                | 場所                                                      |
| ----------------- | ------------------------------------------------------- |
| このPCのVault        | `D:\Obsidian\Garden`                                    |
| リポジトリ             | [utimoriNI/Garden](https://github.com/utimoriNI/Garden) |
| ワークフロー            | `.github/workflows/notion-daily-log.yml`                |
| 同期スクリプト           | `scripts/sync_notion_daily_log.py`                      |
| データソース・プロパティ・除外設定 | `scripts/notion_daily_log.json`                         |
| テスト               | `scripts/tests/test_sync_notion_daily_log.py`           |
| 設定・運用手順           | `scripts/NOTION_DAILY_LOG.md`                           |

既存の `.github/workflows/create-daily-note.yml` はObsidianの日次ノートを23:50に作成する別の処理です。Notion連携は独立したワークフローで動きます。

## このPCで再開するときの確認

PowerShellで次を実行します。GitHub CLIの `gh` は作業時点では見つからなかったため、GitHub側の設定と実行はブラウザで行えます。

```powershell
Set-Location -LiteralPath 'D:\Obsidian\Garden'
git status --short
git branch --show-current
git log -3 --oneline
git ls-remote origin refs/heads/main

$gardenPython = 'C:\Users\royal\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
Test-Path -LiteralPath $gardenPython
& $gardenPython --version
& $gardenPython -B -m unittest discover -s scripts/tests -p test_sync_notion_daily_log.py
& $gardenPython -B scripts/sync_notion_daily_log.py --date 2026-10-03 --dry-run
```

最後のコマンドの日付は、確認したい日付に変更できます。テストでは既存の同期処理を確認します。dry-runはOpenAI APIでトピックを作り、Notionへは書き込みません。OpenAI API keyが必要です。ローカル実行では現在の `HEAD` の履歴を使います。

このPCでは通常の `python` コマンドでPythonを起動できなかったため、確認済みの同梱Pythonを絶対パスで指定しています。上の `Test-Path` が `False` なら、利用できるPython 3.10以降の実行ファイルに `$gardenPython` を変更します。同期スクリプトに追加のPythonパッケージは不要です。`-B` は検証時のキャッシュファイル作成を抑止します。

## 次に進める手順

1. Notionの内部インテグレーションを確認または作成し、コンテンツの読み取り・挿入・更新を許可します。
2. [Logデータベース](https://www.notion.so/fd75d92fd4ad44a2891d9cf4a89b2f6d) にそのインテグレーションを接続します。CodexのNotion接続は、GitHub Actionsの認証には使われません。
3. [GitHubのActions用Secrets設定](https://github.com/utimoriNI/Garden/settings/secrets/actions) で `NOTION_TOKEN` と `OPENAI_API_KEY` の登録を確認します。未登録ならNotionインテグレーションのトークンとOpenAI API keyをRepository secretとして登録します。値は文書やログに保存しません。
4. [ワークフローの画面](https://github.com/utimoriNI/Garden/actions/workflows/notion-daily-log.yml) を開きます。mainの最新実装が反映されていることを確認します。
5. `Run workflow` でブランチを `main`、`date` をコミットのある日付にし、`dry_run` を選択して実行します。例として `2026-10-03` を指定できます。
6. `Update Notion log` ステップのプレビューを確認し、同じ日付で `dry_run` を外して実行します。dry-runにも `OPENAI_API_KEY` が必要です。
7. Notionで専用の行、「更新日」、「やったこと」、本文のコミット一覧を確認します。
8. 同じ日付でもう一度実行し、行と管理ブロックが増えないことを確認します。手書きの追記を検証する場合は、マーカーの外や別ブロックに追記してから再実行します。

日付を省略すると、日本時間の前日分になります。コミットがない日はNotionを更新せず終了します。そのため、初回の書き込み確認にはコミットがある日付を指定します。

## 接続先の設定

| 設定 | 値 |
| --- | --- |
| NotionデータベースID | `fd75d92f-d4ad-44a2-891d-9cf4a89b2f6d` |
| NotionデータソースID | `47945a02-8c29-46d3-a019-357fef84d0ee` |
| タイトルプロパティ | `更新` / `title` |
| 日付プロパティ | `更新日` / `date` |
| 集計プロパティ | `やったこと` / `rich_text` |
| 必須Secret | `NOTION_TOKEN`, `OPENAI_API_KEY` |
| 任意のRepository variable | `NOTION_DATA_SOURCE_ID` |

接続先はJSONに設定済みです。Repository variableの `NOTION_DATA_SOURCE_ID` が設定されていれば、その値を優先します。現在のLogを使う場合は、別のIDを設定する必要はありません。データベースIDをデータソースIDの代わりに指定しないでください。

## エラーが出た場合

| 表示・症状 | 確認すること |
| --- | --- |
| `Set the NOTION_TOKEN ...` | Repository secretの名前と登録先 |
| `HTTP 401` | トークンの有効性 |
| `HTTP 403` / `HTTP 404` | Logへの接続、インテグレーションの権限、データソースID |
| `Notion property ... must be ...` | JSONのプロパティ名とNotion側の型 |
| `Multiple matching daily logs ...` | 同じ専用タイトルと日付の行が重複していないか |
| `Multiple managed log blocks ...` | 同じ管理キャプションを持つブロックが重複していないか |
| `managed summary markers are damaged ...` | 「やったこと」の開始・終了マーカーを変更していないか |
| `No commits on ...` | 対象日、push状況、コミットのcommitter日時 |

通信障害が起きた場合は、復旧後に同じ日付で再実行します。作成や追記が保存された後に通信が失敗する場合もあるため、先にNotionで現在の状態を確認します。重複やマーカー破損の修正では、手書き内容を確認してから対応します。

## 完了と判断する条件

- [ ] Actions用インテグレーション、`NOTION_TOKEN`、`OPENAI_API_KEY` を確認した。
- [ ] GitHub Actionsのプレビューと本番実行が成功した。
- [ ] Notionの対象日とコミット内容が一致した。
- [ ] 同日再実行で重複せず、手書きの追記が残った。
- [ ] 定時実行を1回確認した。

GitHub Actionsが定時処理を実行するので、実行時にこのPCを起動しておく必要はありません。記録したいコミットはGitHubへpushしておきます。

## 次のチャットで作業を引き継ぐ文

> `D:\Obsidian\Garden\scripts\NOTION_DAILY_LOG_HANDOFF.md` と `scripts/NOTION_DAILY_LOG.md` を読んで、Notion日次ログ連携の続きを進めてください。実装とローカルテストは完了しています。GitHub SecretとNotion接続の登録状況を確認し、GitHub Actionsのプレビュー、本番書き込み、同日再実行による重複防止と手書き内容の保持を検証してください。認証情報の値は文書やログに出さないでください。
