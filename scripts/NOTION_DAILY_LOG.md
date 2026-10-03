# GitHubのコミットをNotionの日次ログに記録する

`.github/workflows/notion-daily-log.yml` が毎日 **日本時間00:15** に起動し、前日の00:00〜24:00にコミットされた変更をNotionの [Log](https://www.notion.so/fd75d92fd4ad44a2891d9cf4a89b2f6d) に記録します。たとえば10月4日00:15の実行は10月3日分です。

## 初回設定

1. Notionで内部インテグレーションを作り、コンテンツの読み取り・挿入・更新を許可します。
2. Logデータベースの接続メニューから、そのインテグレーションにアクセスを付与します。
3. [GardenのActions設定](https://github.com/utimoriNI/Garden/settings/secrets/actions) にRepository secret **`NOTION_TOKEN`** を登録します。値はNotionインテグレーションのトークンです。CodexのNotion接続とは別の認証です。トークンをソースやノートに書かないでください。
4. 作成したファイルをGitHubのデフォルトブランチ（`main`）へ反映します。
5. [Actions](https://github.com/utimoriNI/Garden/actions) の **Update Notion daily log → Run workflow** で `date` を指定し、最初は `dry_run` を選択して内容を確認します。確認後、`dry_run` を外して実行するとNotionに記録します。

対象データソースIDと既存のプロパティ名は `scripts/notion_daily_log.json` に設定済みです。別のデータソースを使う場合はRepository variable **`NOTION_DATA_SOURCE_ID`** でIDを上書きできます。データベースIDとデータソースIDは別物です。

| プロパティ | 型 | 記録内容 |
| --- | --- | --- |
| 更新 | title | `2026-10-03 Garden：コミットログ` のような日別タイトル |
| 更新日 | date | コミットを集計した日本時間の日付 |
| やったこと | rich_text | コミット数、変更ノート数、追加・更新・削除したファイル数 |

本文の専用コードブロックにコミット時刻、メッセージ、作者、GitHubへのURL、変更ファイル一覧を記録します。分野・メモなどのプロパティはそのままです。

## 集計と再実行

- GitHubのデフォルトブランチで到達できるコミットを、**committer日時を日本時間に変換した日付**で集計します。未pushの変更や別ブランチだけのコミットは含みません。
- 日付境界で取りこぼさないよう翌日実行します。GitHubのスケジュールは遅延する場合があります。日をまたぐほどの遅延や実行漏れがあれば `date` を指定して再実行してください。
- 日付指定を省略した手動実行も前日分です。当日分は当日の日付を指定すると、実行時点までのコミットを記録できます。
- 同じ専用タイトルと日付の行を更新します。同日に存在する通常のログはそのまま残し、Garden用の行を1件作成します。同じ日に再実行しても行や専用ブロックを追加しません。
- 「やったこと」の `[Garden GitHub log:begin]`〜`[Garden GitHub log:end]` 内と、本文の `Garden GitHub log | ...` キャプションを持つ専用ブロックを更新します。手書きの追記はマーカーの外や別ブロックに書いてください。専用ブロックのキャプションは識別に使うので変更しないでください。
- 自動バックアップのコミットも数えます。端末セッションやObsidianの一部キャッシュは変更ファイル一覧から除外します。除外設定はJSONの `exclude_paths` にあります。
- リネームは旧パスの削除と新パスの追加として記録します。同じパスは各区分で1回だけ数えます。追加後に更新されたノートは両方の区分に入ります。
- コミットがない日は行を作りません。詳細が表示上限を超えた場合は省略を明記します。
- 権限・スキーマ不一致・重複・壊れたマーカーはエラーとして停止します。ページ作成／ブロック追記で通信障害が起きたら、復旧後に再実行してください。既に保存された行／ブロックを検索して更新します。

## ローカルで確認

```bash
python scripts/sync_notion_daily_log.py --date 2026-10-03 --dry-run
python -m unittest discover -s scripts/tests -p test_sync_notion_daily_log.py
```

dry-runはNotionへアクセスせず、トークンも不要です。Python 3.10以降とGitがあれば動き、追加のPythonパッケージは不要です。ActionsではPython 3.12を使います。

仕様の参照: [GitHubのスケジュール](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#onschedule)、[NotionのデータソースAPI](https://developers.notion.com/guides/get-started/upgrade-guide-2025-09-03)、[Notionのリクエスト制限と再試行](https://developers.notion.com/reference/request-limits)。
