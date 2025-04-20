---
created: 2023-10-05
tags:
  - 🎁Topic/Tech
---
## 第5章 JSXでUIを表現する
### 5-1. なぜReactではJSXを使うのか
#### 5-1-3. なぜReactではテンプレートを使わないのか
ReactはHTMLテンプレートをレンダリングに使っていない。
テンプレートに見えるJSXも、本質はオブジェクトを生成するJavaScriptの式である
このように、レンダリングもJavaScriptによって行う思想をJSファーストと呼ぶ（本書内のみの用語？）
※[Pete Hunt: React: Rethinking best practices -- JSConf EU - YouTube](https://youtu.be/x7cQ3mrcKaY)より

現在のフロントエンドアプリケーションフレームワークは、Viewレンダリング方式によって
- HTMLテンプレート派
	- Angular, Vue.js, Ember.jsなど
- JSファースト派
	- React, Preact, Stencil
の2つに分けられる
HTMLテンプレート派は、Webアプリケーションを動的なWebページと考えるため、最終出力のHTML形式に固執する。
JSファースト派は、Webアプリケーションをブラウザがプラットフォームとなったアプリケーションと考えるため、一貫した言語で開発しようとする。