---
type: workflow
status: active
tags:
  - Knowledge
  - 🎁Topic/PKM
---

# Permanent Noteワークフロー

> [!summary] 基本原則
> Permanent Noteは、複数のFleeting / Reading Noteから導いた「一つの主張」です。リンクを並べるだけならMOCとして扱います。

## 候補を確認する

![[Permanent Note候補.base#未確認]]

候補を開くと、主張、根拠、反例、正式化したときの変更内容を確認できます。Baseの`判断`を次のいずれかに変更します。

- `approved`：正式化してよい
- `hold`：保留
- `rejected`：却下
- `pending`：未確認

> [!warning] Baseで承認した時点では正式ノートは作られません
> Baseで編集する`decision`や`review_comment`は候補ファイルだけに保存されます。承認済み候補の正式ノートへの反映は別に実行します。

## コメントから候補を直す

短い修正意見はBaseの`コメント`欄に書けます。長いコメントは候補ファイルを開き、`ユーザーコメント`のマーカー内に書きます。

![[Permanent Note候補.base#コメントあり]]

コメントを書いた後、Codexに「候補コメントを反映して」と依頼してください。Codexは主張・下書き・根拠・反例を見直し、元コメントと対応内容を候補内の`コメント反映履歴`に残します。未反映コメントがある候補は正式化できません。

## 反映待ち

![[Permanent Note候補.base#反映待ち]]

Codexに「承認済み候補の変更を確認して」と頼むと、作成予定ファイルをプレビューします。その後「承認済み候補を反映して」と頼むと正式ノートを作成します。

反映時に起きること：

1. Reading Note候補は`300_Input/Reading Notes`へ新規作成
2. Permanent Note候補は`600_Knowledge`へ`type: knowledge`、`status: draft`で新規作成
3. 候補に`apply_status: applied`と作成先を記録
4. 元記事、Fleeting Note、Reading Noteは変更しない
5. 同名ファイルが存在する場合は上書きせず停止

## 反映済み

![[Permanent Note候補.base#反映済み]]

## よく使う依頼

- `Raindropから取り込んだ未処理の記事からReading Note候補を作って`
- `このWeb記事からReading Note候補を作って`
- `FleetingとReading NoteからPermanent Note候補を作って`
- `未確認のPermanent Note候補を5件作って`
- `候補コメントを反映して`
- `承認済み候補の変更を確認して`
- `承認済み候補を反映して`

## 内部仕様

- [[.agent-wiki/permanent-note-workflow/SCHEMA]]
- [[.agent-wiki/permanent-note-workflow/WORKFLOW]]
