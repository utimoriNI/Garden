## Title
# [Next.jsで静的サイトを開発する際によく使うライブラリやサービス集]

## Source
(https://zenn.dev/h_ymt/articles/c1fc3eb70dc038)
[[ReadItLater]] [[Article]]


## Contents
## はじめに

タイトルのとおりです。個人的によく使用するものをまとめました。

## CSS フレームワーク

（CSS in JS が入っていないのは完全な好みです。）

### CSS Modules

従来の CSS と同じように使えて、学習コストも低いのでよく使用しています。  
Next.js にビルトインサポートされているのも嬉しいポイント。

### Tailwind CSS

ユーティリティファーストな CSS フレームワーク。  
css ファイルを作らないためファイル管理・移動が楽なこと、スタイリングが早くなるのが嬉しい。  
※最初は jsx ファイルに大量のクラスが書かれていることにアレルギー反応があったが、使っているうちに慣れた。

## UI ライブラリ

MUI や Chakra UI などもいいが、スタイリングされていない方が個人的に好きなので Headless 系の UI をよく使用する。

### Headless UI

ドロップダウンメニューやトグルボタン機能など簡単に実装することができる。  
簡易的なサイトはこれで十分かも。

### Radix UI

Headless UI とよりも機能を充実させた感じのライブラリ。  
Primitive とよばれる Headless UI のようなコンポーネントはもちろん、2023 年の 8 月 8 日から`MUI`や`Chakra UI`のようなスタイリングも振る舞いも兼ね備えた Theme の提供が開始した。

### shadcn/ui

Radix UI より見た目が整ったライブラリ。

### daisyUI

Tailwind CSS をベースとして UI コンポーネントライブラリ。

### Floating UI

ツールチップやポップオーバーなどのフローティング要素を作成できるライブラリ。

### Embla

カルーセルを簡単に実装できるライブラリ。  
shadcn/ui でも使われているらしい。

### react-scroll

ページ内リンクに便利なライブラリ

シェアボタンを楽に実装できるライブラリ

### Swiper

使い慣れたスライダーライブラリ

## アニメーション

### Framer Morion

GSAP よりも直感的にアニメーションを指定できます。  
ページ遷移アニメーションも簡単に実装できてオススメです。

### GSAP

いわずと知れた有名なアニメーションライブラリ。

## HeadlessCMS

### microCMS

### Kuroco

### Newt

### Wordpress

WP REST APIを使用して Wordpress を Headless CMS として使用することも可能。  
長年、Wordpress で記事やお知らせの更新をしてきたクライアントには、上記の CMS より親しみやすいしコンテンツを移さなくていいので楽。

## ホスティング

### Vercel

### Netlify

### Cloudflare