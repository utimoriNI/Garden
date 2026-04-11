---
name: xurl
description: X API を xurl CLI 経由で扱うときに使う。自分のブックマーク取得、キーワード検索、取得結果の JSON 整形をローカルで行いたい場合に使う。認証は xurl の OAuth 設定済みを前提とし、Agent からは秘密情報を直接扱わない。
---

# xurl

`xurl` を使って X API から情報を取得し、あとで整理しやすい JSON に整える skill。

この skill は次の用途を優先する。

- 自分のブックマーク取得
- キーワード検索
- 取得結果の JSON 保存

## 前提

- `xurl` がローカルにインストール済みであること
- 認証設定はユーザーが手動で完了していること
- 作業ディレクトリは Vault ルート (`/Users/isikurahiromitu/Documents/Garden`) を使うこと

`xurl` が未導入なら、まずユーザーが手動で導入する。

```bash
brew install --cask xdevplatform/tap/xurl
```

認証状態だけ確認したいときは次を使う。

```bash
xurl auth status
```

## Secret Safety

- `~/.xurl` は読まない
- トークンや client secret を chat に貼らせない
- `xurl` の秘密情報フラグを agent から直接使わない
- `-v` / `--verbose` は使わない

認証の初期設定や再認証は、必要ならユーザー本人がローカル端末で実行する。

## 基本手順

通常はラッパースクリプトを使う。

```bash
python3 .codex/skills/xurl/scripts/xurl_json.py auth-status
python3 .codex/skills/xurl/scripts/xurl_json.py bookmarks --limit 20
python3 .codex/skills/xurl/scripts/xurl_json.py search --query "obsidian" --limit 20
```

ファイル保存したいときは `--output` を付ける。

```bash
python3 .codex/skills/xurl/scripts/xurl_json.py bookmarks --limit 50 --output 200_Inbox/x/bookmarks.json
python3 .codex/skills/xurl/scripts/xurl_json.py search --query "from:XDevelopers api" --limit 30 --output 200_Inbox/x/search-api.json
```

## 出力方針

ラッパーは常に JSON を stdout に出す。成功時は次の形を基本にする。

```json
{
  "ok": true,
  "action": "bookmarks",
  "fetched_at": "2026-04-11T12:00:00+09:00",
  "request": {},
  "summary": {
    "count": 20,
    "next_token": null
  },
  "items": [],
  "raw": {}
}
```

- `items` は整理しやすい正規化済み配列
- `raw` は元の X API 応答
- `summary.next_token` があれば次ページ取得に使う

## 想定コマンド

```bash
python3 .codex/skills/xurl/scripts/xurl_json.py bookmarks --limit 100 --next-token TOKEN
python3 .codex/skills/xurl/scripts/xurl_json.py search --query "\"second brain\"" --limit 25
python3 .codex/skills/xurl/scripts/xurl_json.py search --query "(obsidian OR roam) lang:ja -is:retweet" --limit 25
```

## エラー時

- ラッパーは失敗時も JSON を stdout に出す
- プロセスは非ゼロ終了にする
- 認証失敗、`xurl` 未導入、JSON 解析失敗、API エラーを区別して返す

必要なら `summary` や `raw.meta.next_token` を見て追加入力を続ける。
