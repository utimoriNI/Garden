---
title: Thread by @billtheinvestor
source: https://x.com/billtheinvestor/status/2041995989889024056
author:
  - "[[@billtheinvestor]]"
published: 2026-04-09
created: 2026-04-11
description: Andrej Karpathy がこのツールの開発を提案してから48時間後、Graphify は GitHub でオープンソース化されました。Karpathy の /raw フォルダには、論文、ツイート、スクリーンショット、ノートなどの非構造化データが含まれています。Graphi
tags:
  - 📂Project/LLMWiki
image: https://abs.twimg.com/rweb/ssr/default/v2/og/image.png
---

**Bill The Investor** @billtheinvestor [2026-04-08](https://x.com/billtheinvestor/status/2041995989889024056)

Andrej Karpathy がこのツールの開発を提案してから48時間後、Graphify は GitHub でオープンソース化されました。Karpathy の /raw フォルダには、論文、ツイート、スクリーンショット、ノートなどの非構造化データが含まれています。Graphify は、単一のコマンドで任意のフォルダを構造化された知識グラフに変換します：

\`graphify ./raw\`

出力結果には以下が含まれます：

\- インタラクティブで検索可能、コミュニティでフィルタリング可能な知識グラフ

\- コアノード、予期せぬ関連性、および提案問題を含む自然言語レポート

\- バックリンク付きの記事 Obsidian ライブラリ（オプション）

\- AI Agent がナビゲートするための Wiki (index.md)

コア性能指標：クエリトークン消費が 71.5 倍削減されました。コードベース、論文、画像を含む混合コーパスにおいて、平均クエリコストが ~123K トークンから ~1.7K トークンに低下しました。技術実装：

\- マルチモーダル対応：tree-sitter AST を通じて 19 種のプログラミング言語のコードを処理；Claude Vision を通じて PDF、画像、スクリーンショット、白板写真を処理。

\- ベクタデータベースや Embedding 不要：Leiden コミュニティ検出アルゴリズムを利用してエッジ密度でクラスタを識別し、グラフのトポロジー構造自体が類似性のシグナルとなります。

\- 自動同期：Git hooks を通じて各コミットまたはブランチ切り替え後にグラフを再構築；SHA256 キャッシュを利用して変更ファイルのみを処理。

\- 互換性：Claude Code、Codex、OpenCode、OpenClaw、Factory Droid をサポート。インストールコマンド：

\`pip install graphify && graphify install\`

MIT License。100% オープンソース。

![画像](https://pbs.twimg.com/media/HFaghNJakAAd0hi?format=jpg&name=large)