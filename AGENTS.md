# Garden 運用ガイド

このファイルは、この Obsidian Vault で作業するときの基本ルールを定義する。

## 目的

この Vault には、あとで再利用したい知識や断片を蓄積していく。
作業時は、その運用を壊さず、一貫した形で拡張することを優先する。

## 基本方針

この Vault では、次の2つを分けて扱う。

1. そのノートを資産として残したいか
2. そのノートがどの構造タイプに属するか

この2つを混同しないこと。

## タグの役割

`🎁Topic/...`
- 資産として残したい情報であることを表す大分類
- `🎁Topic/...` が付いていても、必ずしも `reading-note` ではない

`🧩rn/...`
- reading-note 関連の小分類に使う
- `🧩rn/candidate` は一時的な候補タグ
- `reading-note` に変換したら `🧩rn/candidate` は削除する

## Reading Note の定義

`reading-note` は、あとで再利用しやすい最小単位のノートを指す。
例えば次のようなものが該当する。

- 1つの引用
- 1つの概念
- 1つの主張
- 1つの場面
- 1つの言い回し

`reading-note` かどうかはタグではなく frontmatter で判断する。

最小 frontmatter は次の通り。

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

### プロパティの意味

`type`
- ノートの構造タイプ
- `reading-note` は一節ノートとして運用するノートに使う

`source_type`
- 出典の種類
- 例: `kindle`, `web`, `video`, `legacy`

`source_container`
- 元ノートや元ソースへの導線
- 分からない場合は空欄でよい

`topic`
- テーマ単位の分類

`moc`
- MOC への接続

`status`
- 運用上の状態
- デフォルトは `inbox`

## ソースレイヤーの考え方

この Vault では、次のレイヤーを意識して扱う。

- 原本ノート: Kindle import、Web記事、動画メモなど
- 候補ノート: 一節ノート化したいが、まだ正規化していないもの
- Reading Note: 再利用しやすい単位に整えたノート
- Knowledge / MOC: 抽象化や整理を行ったノート

すべてを同じ型に寄せず、役割に応じて分けること。

## Kindle ハイライト運用

Kindle の原本ノートは次に置く。

- `400_Kindle`

ここは、抽出フラグを付けるソースノートとして扱う。

### Kindle ノートで使う記法

`%% pick %%`
- そのハイライトだけを 1 つの reading-note にする

`%% group: ... %%`
- 同じ group を持つ複数ハイライトを 1 つの reading-note にまとめる

`%% title: ... %%`
- reading-note のタイトルを明示的に指定する
- `pick` と `group` のどちらでも使える

### Kindle 変換スクリプト

次を使う。

- [scripts/generate_kindle_reading_notes.py](/Users/isikurahiromitu/Documents/Garden/scripts/generate_kindle_reading_notes.py)

このスクリプトは次を行う。

- `400_Kindle` のフラグ付きノートを読む
- `200_Inbox/Reading Notes` に reading-note を生成する
- `pick`, `group`, `title` に対応する

## 候補ノートの変換

既に Vault 内にあるノートを reading-note 化したい場合は、次の流れにする。

1. `🧩rn/candidate` を付ける
2. reading-note に変換する
3. `🧩rn/candidate` を削除する

次を使う。

- [scripts/convert_rn_candidate_notes.py](/Users/isikurahiromitu/Documents/Garden/scripts/convert_rn_candidate_notes.py)

このスクリプトは次を行う。

- `🧩rn/candidate` が付いたノートを探す
- 必要なら最小 frontmatter を追加する
- `🧩rn/candidate` を tags から削除する

## 旧 Lexicon ノートの移行

`🎁Topic/Lexicon` の旧ノートは、過去の資産として reading-note schema に寄せている。

移行用スクリプト:

- [scripts/migrate_lexicon_to_reading_notes.py](/Users/isikurahiromitu/Documents/Garden/scripts/migrate_lexicon_to_reading_notes.py)

これは日常運用用ではなく、旧資産の一括移行用と考えること。

## 分類ルール

Obsidian 上で扱いやすくするために、タグは広い分類や見やすさに使う。
構造的な運用は frontmatter で管理する。

推奨する役割分担:

- `🎁Topic/...`: 資産カテゴリ
- `🧩rn/...`: reading-note 関連の小分類
- `type`: ノート構造
- `source_type`: 出典種別
- `status`: 運用状態

`🎁Topic/...` だけで reading-note を表現しないこと。

## ノート編集時のルール

この Vault のノートを編集するときは次を守る。

- 明示的な依頼がない限り、本文を大きく書き換えない
- まずは最小 frontmatter を足す方針を優先する
- `🎁Topic/...` タグは勝手に外さない
- `reading-note` 化が済んだら `🧩rn/candidate` を外す
- 既存ノートを大きく再設計するより、段階的に移行する

## 安全なデフォルト

迷った場合は次を優先する。

- 1ノート = 1断片 と明確に言えないなら `reading-note` にしない
- 出典が分からなければ `source_type: legacy`
- `source_container` は推測で埋めず空欄にする
- `topic` や `moc` は無理に埋めない

## この Vault で目指す状態

このリポジトリでの作業は、次をしやすくする方向に寄せる。

- 再利用したい断片を残す
- 断片を reading-note として正規化する
- 後から見返しやすくする
- MOC や Knowledge に接続しやすくする
- 元ソースへの導線を失わない
