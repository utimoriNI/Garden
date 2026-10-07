---
title: GitHub Actions棚卸
type: documentation
status: review
created: 2026-10-07
---

# GitHub Actions棚卸

Obsidian Syncへの移行に合わせ、Gardenの自動処理を棚卸した。Garden自身のActionsは2件で、どちらもGitHub上のコミットに依存している。Gitへのpushを止めるなら、現行の2件は廃止またはローカル処理への移行が必要になる。

今回は調査と廃止案の整理を行った。ワークフローの停止・削除、Secretの変更、Notionへの書き込みは実施していない。

## 対象と確認方法

- 対象リポジトリ: [utimoriNI/Garden](https://github.com/utimoriNI/Garden)
- 確認日: 2026-10-07。時刻は日本時間。
- ローカルとGitHubのmainにある2件のワークフロー定義が一致していることを確認した。
- GitHub APIに残っている全18件の実行結果と、最新の成功・失敗ログを確認した。
- スクリプト、設定、テンプレート、関連ドキュメント、日記の生成履歴を確認した。
- Secretの値は取得していない。Notionの現行データや課金額は確認していない。

## 一覧と判断案

| 処理 | 現在の役割 | 実行タイミング | Sync移行後の問題 | 判断案 |
| --- | --- | --- | --- | --- |
| Create daily note | デイリーノートを作成し、Gitで当日追加されたノートのリンク・埋め込みを追記してpush | 毎日23:50予定／手動 | GitHubの変更がSyncへ直接届く経路がない。作成ノートの集計もGit履歴が必要 | Actionsを廃止し、ノート作成をObsidianに移す。追加ノート一覧は必要なら別途置き換える |
| Update Notion daily log | 前日のコミット差分をOpenAI APIでトピック別に要約し、NotionのLogへ記録 | 毎日00:15予定／手動 | push停止後はVaultでの作業を把握できない。現在の定期実行も失敗中 | Gitコミット日報が不要なら廃止。作業日報を残したいならデイリーノートなどを入力にして作り直す |

## 1. Create daily note

定義: [create-daily-note.yml](https://github.com/utimoriNI/Garden/blob/main/.github/workflows/create-daily-note.yml)

実装: [create_daily_note.py](https://github.com/utimoriNI/Garden/blob/main/scripts/create_daily_note.py)

### 動作と依存

`.obsidian/daily-notes.json`に指定した[[998_Resource/Template/Daily|Dailyテンプレート]]を使い、`100_Periodic/Daily/YYYY-MM-DD.md`を作る。既存ノートがあれば、「当日作成されたノート」の管理マーカー内を更新する。

ノート一覧は、ファイルの作成日時ではなく、Gitで追加されたコミットの日付を日本時間に変換して集計する。GitHubにまだpushされていないノートはActionsから見えない。更新した日記は`GITHUB_TOKEN`の`contents: write`権限でGardenへcommit・pushする。外部APIは使わない。

### 実行状況

履歴は11件。定期実行9件のうち4件成功・5件失敗、過去のpush起動は2件とも成功。現在の定義にはpush起動がなく、定期実行と手動実行だけが残っている。

直近4回の定期実行は成功した。ただし[最新実行](https://github.com/utimoriNI/Garden/actions/runs/37521966571)は2026-10-07 04:51に動き、実行日の`2026-10-07.md`を更新して追加ノート0件と記録した。23:50予定の処理が翌日にずれると、前日分を集計できない。GitHubの定期実行には遅延があり得る。[公式仕様](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)

最後に失敗した[2026-10-03の実行](https://github.com/utimoriNI/Garden/actions/runs/37054769970)はcheckout中の`File name too long`が原因だった。これは過去の失敗であり、現在も同じ原因で失敗しているという意味ではない。

### 廃止した場合と代替

停止すると、利用しなかった日も含めた日記の自動作成と、追加ノート一覧の自動更新が止まる。既存の日記は残る。

ObsidianではDaily notesコアプラグインが既に有効で、同じ保存先とテンプレートが設定されている。「今日のデイリーノートを開く」で、その日のノートがなければ作成できる。[公式説明](https://obsidian.md/help/plugins/daily-notes)

この代替はObsidianを使う際のノート作成を担う。未利用日にも定時作成する動作や、追加ノート一覧までは引き継がない。追加ノート一覧を残す場合は、全端末で共通の`created`プロパティなど、Gitに依存しない日付基準を先に決める。

廃止候補ファイルは`.github/workflows/create-daily-note.yml`と`scripts/create_daily_note.py`。Daily notesの設定、Dailyテンプレート、既存の日記は残す。

## 2. Update Notion daily log

定義: [notion-daily-log.yml](https://github.com/utimoriNI/Garden/blob/main/.github/workflows/notion-daily-log.yml)

実装・設定: [sync_notion_daily_log.py](https://github.com/utimoriNI/Garden/blob/main/scripts/sync_notion_daily_log.py)、[notion_daily_log.json](https://github.com/utimoriNI/Garden/blob/main/scripts/notion_daily_log.json)

### 動作と依存

mainの全Git履歴から、前日の日本時間00:00〜24:00にコミットされた変更を集める。差分をOpenAI APIに送り、トピックごとにNotionのLogレコードを作成・更新する。Garden自体にはpushしない。

| 種別 | 名前 | 用途 |
| --- | --- | --- |
| Secret | `OPENAI_API_KEY` | コミット差分の要約 |
| Secret | `NOTION_TOKEN` | Notionへの読み書き |
| 任意のVariable | `OPENAI_MODEL` | 要約モデルの指定 |
| 任意のVariable | `NOTION_DATA_SOURCE_ID` | Notionの接続先の上書き |

GitHub上にコミットがない日は何も記録しない。`--dry-run`でも、コミットがあればOpenAI APIを利用する。Notionへの書き込みだけが省略される。

### 実行状況

履歴は7件。定期実行4件はすべて失敗。手動実行は2件成功・1件キャンセル。

[最新の失敗ログ](https://github.com/utimoriNI/Garden/actions/runs/37525874340)には、次のエラーがある。

```text
Daily log failed: Set the OPENAI_API_KEY GitHub Actions secret to create topic summaries.
```

checkout、Pythonの設定、既存テストは成功し、実際の日報処理で停止している。少なくとも最新実行では、処理に渡された`OPENAI_API_KEY`が空だった。Notionへの書き込みまで到達していないため、現在の`NOTION_TOKEN`の有効性はこの実行だけでは判断できない。

[2026-10-03の手動本番実行](https://github.com/utimoriNI/Garden/actions/runs/37106871943)はNotionへ38コミット分を記録した。ただし、その時点のコードはOpenAIによるトピック要約を導入する前の版だった。旧版の成功は、現在の実装が稼働している証拠にはならない。

### 廃止した場合と代替

停止すると、Notionへのコミット日報の自動記録が止まる。既存のNotionレコードやGardenのノートは残る。

Git同期をやめるなら、APIキーを設定するだけでは移行後の目的を満たせない。Gitコミットの記録が必要か、日々の作業の記録が必要かを分けて判断する。後者を残す場合は、デイリーノートの「やったこと」などを入力にするローカル処理へ移す。その場合は実行担当のPC、起動条件、処理済み判定を決める必要がある。

全面廃止する場合の整理対象は次の6ファイル。

- `.github/workflows/notion-daily-log.yml`
- `scripts/sync_notion_daily_log.py`
- `scripts/notion_daily_log.json`
- `scripts/tests/test_sync_notion_daily_log.py`
- `scripts/NOTION_DAILY_LOG.md`
- `scripts/NOTION_DAILY_LOG_HANDOFF.md`

ローカル版へ移す場合は、スクリプト・テストを流用する余地があるため、先に削除しない。全面廃止後は、この処理専用のRepository Secrets／Variablesも整理対象になる。OpenAIやNotionのキー自体を無効化するかは、他の利用先も含めて別途判断する。

## Gardenの2件以外にある依存

日記と週次ノートには、今回の2件では作られない振り返りの自動更新が残っている。

- [2026-10-07 09:12のコミット](https://github.com/utimoriNI/Garden/commit/2e70173): `Update daily journal reflection for 2026-10-06 [skip ci]`
- [2026-10-05 08:50のコミット](https://github.com/utimoriNI/Garden/commit/f5164cc): `Update weekly journal reflection for 2026-W40 [skip ci]`

両方とも作者は`github-actions[bot]`。[[100_Periodic/Daily/2026-07-20]]にも、AI Memory System／AI_MemoryDB側の処理とGardenへの同期について記録がある。別リポジトリなどからGardenへ書き込む経路があると考えられるが、稼働元のワークフロー定義は未確認。

`utimoriNI/AI_MemoryDB`へのGitHub接続からの参照は404になった。存在しないのか、名前が異なるのか、アクセス権がないのかは判別できない。日次・週次・月次の振り返りを残す場合は、稼働元を特定して生成処理とGardenへの受け渡しを追加で棚卸する必要がある。

Gitのpullを止めると、GitHubに書き込まれた新しい振り返りはローカルVaultへ届かなくなる。Obsidian Syncを導入しても、GitHubへのpushが自動でSyncへ転送されるわけではない。

なお、Obsidian Gitプラグインによるcommit・push・pullはGitHub Actionsとは別の処理。今回の2件を止めることと、Git同期を止めることは別々に実施する。

## 整理する順序の案

1. 日記の作成はObsidian側へ移し、Create daily noteを停止する。追加ノート一覧を残すかは別に決める。
2. Notionのコミット日報が不要ならUpdate Notion daily logも停止する。作業日報を残すなら、ローカル版の入力と実行方法を先に決める。
3. 振り返りを生成している別の処理を確認し、残す機能の受け渡しを移す。
4. 必要な機能の代替を確認してから、Gitのpull・pushを停止する。
5. 不要になったワークフロー、スクリプト、専用設定を整理する。

検証期間はGitHubの「Disable workflow」で停止でき、ファイルを消さずに再有効化できる。[公式手順](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows)
