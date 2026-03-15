---
title: Blender100レシピ！③海をつくろう｜Miki
source: https://note.com/mikiniki_cg/n/n57d85db0a449
author:
  - "[[Miki]]"
published: 2025-12-11
created: 2026-01-10
description: "こんにちは、Mikiです。  3品目は「海」! これまた背景制作ではよく使いますね～  一見難しそうにも思えますが、要素を分解していくと意外と手軽につくれちゃいます。 それでは早速始めましょう！  完成画像はこんな感じです 用意するもの    Blender : 私は5.0を使用しました(5以下のバージョンでも同様に作れます)    HDRI画像：ポピュラーですが下記のPoly Havenは使いやすいです    HDRIs • Poly HavenPreviously known as HDRI Haven. Hundreds of free HDRI environ"
tags:
  - 🎁Topic/Blender
image: https://assets.st-note.com/production/uploads/images/234421486/rectangle_large_type_2_42c8671aabd9589b50d3bb49d25325ed.png?fit=bounds&quality=85&width=1280
---
![見出し画像](https://assets.st-note.com/production/uploads/images/234421486/rectangle_large_type_2_42c8671aabd9589b50d3bb49d25325ed.png?width=1280)

## Blender100レシピ！③海をつくろう

[Miki](https://note.com/mikiniki_cg)

こんにちは、Mikiです。

3品目は「海」!  
これまた背景制作ではよく使いますね～

一見難しそうにも思えますが、要素を分解していくと意外と手軽につくれちゃいます。  
それでは早速始めましょう！

![画像](https://assets.st-note.com/img/1763782617-Xs9LQEiAdKISVpYu2T4zbrqH.png?width=1200)

完成画像はこんな感じです

## 用意するもの

- Blender: 私は5.0を使用しました(5以下のバージョンでも同様に作れます)
- HDRI画像：ポピュラーですが下記のPoly Havenは使いやすいです

[**HDRIs • Poly Haven** *Previously known as HDRI Haven. Hundreds of free HDRI environ* *polyhaven.com*](https://polyhaven.com/hdris)

## つくりかた

> ※レシピ記事は全て無料で読めますが、サンプルファイルは有料で提供しています。

### 1.シーン設定

まずは作業環境を設定していきます。  
デフォルトキューブを削除し（宿命）、代わりに床となる平面を配置します。スケールは100倍程度にしておけば十分でしょう。

![画像](https://assets.st-note.com/img/1763783022-tlB6cOCYjqeWK0mw8ZL7RMIb.png?width=1200)

床の平面にそれっぽいマットなマテリアルを割り当てましょう。  
今回変更したパラメータは下記のとおりです。

> BaseColor: #393939FF  
> Roughness: 1.0  
> Specular IOR Level: 0.036

![画像](https://assets.st-note.com/img/1763783570-0J79gdiUj4BQakMADvuPsChp.png?width=1200)

Worldのマテリアルにお好きなHDRIを割り当ててライティング環境を設定します。HDRIを探してくるのすらめんどくさければ別にBlenderデフォルトのHDRIでも構いません。

![画像](https://assets.st-note.com/img/1763784137-DIeKp7aJldRrt8WuL21ob9MC.png?width=1200)

左：HDRIをダウンロードした場合のワールドマテリアルセットアップ 右：見た目をいろいろ探ってたら結局デフォルトHDRIに落ち着きました

---

### 2.海のモデリング

シーン設定は完了したので、いよいよ海本体の作成に取り掛かります。  
消したはずのキューブを復活させます（宿命）。  
スケールは2倍にしてみました。

![画像](https://assets.st-note.com/img/1763784761-N2MHwGzOq8bdDkuK7FBx6LoA.png?width=1200)

TabキーでEditモードに入り、右クリックでSubdivideを5回ほど実行します。

![画像](https://assets.st-note.com/img/1763784998-gB0aq23XmFGt7YzpbDduScZQ.png?width=1200)

モディファイアタブに切り替え、Oceanモディファイアを割り当てます。  
変更したパラメータは、画像で赤線を引いたご覧の箇所です。

![画像](https://assets.st-note.com/img/1763785570-8fPSYDJy4TxcANeHpmu3Z1aG.png?width=1200)

ポリゴンの境界が少し目立つので、右クリックでShade Auto Smoothを実行しましょう。  
海らしい波のうねりが表現されましたね。これでモデリングは完了です。

![画像](https://assets.st-note.com/img/1763785847-TOp06UVGFdu7Sa39Mt8ykXl2.png?width=1200)

---

### 3.海のマテリアル

続いてマテリアルで水の質感を表現していきましょう。

基本的な水は下の画像のようなノードとパラメータで表現しています。

AlphaチャンネルにLight PathノードのIs CameraRayを接続しているのは、カメラに映っていないキューブ裏側のポリゴンの表示を消すことで、屈折が歪に見えることを解消しています。（何言ってるのかわからんという方は、接続を抜いたり挿したりAlphaの数値をいじったりしてみてください。何となく分かった気になると思います。）

![画像](https://assets.st-note.com/img/1763796945-UFvm6qbBf8eAwN5Gct3r9YW1.png?width=1200)

さらに水らしさを追加するため、マテリアルにボリュームを追加しましょう。これにより、光が水中で散乱する様子を表現することができます。  
パラメータは画像のように設定しています。

![画像](https://assets.st-note.com/img/1763798901-8AIRMDV2nTamvGX5UHcSQoqJ.png?width=1200)

---

### 4.コースティクス表現

現実世界で、水底にゆらゆらと光の模様や筋が揺れていることがありますよね。あれをコースティクスと呼ぶのですが、レシピの仕上げとして追加しましょう。  
とはいったものの、これでレシピひとつ書けるくらい長くなってしまったので、下のリンク記事を参考にしてみてください～。

  

### 5.完成！

コースティクスも追加すると最終的には下の画像のような感じになります！  
光の筋と模様が綺麗….

![画像](https://assets.st-note.com/img/1763813772-TSlQcb9VWnz6mdhsAH7X5J2g.png?width=1200)

## サンプルファイル

上記手順をたどれば作成できるかと思いますが、  
**「そんなのいちいちメンドクサイ！」「数値とか直接コピペしたい！」「ファイルも直接見てみたい！」** といった方々に向けて、サンプルファイル（Blender 5.0）も用意していますので、そちらもぜひどうぞ！

¥ 350

抽選でnoteポイント 最大100%還元 1/14まで

[ログイン](https://note.com/login?redirectPath=%2Fmikiniki_cg%2Fn%2Fn57d85db0a449)

応援ありがとうございます！いただいたチップは書籍購入などの活動費に使わせていただきます！

## 購入者のコメント

[![買うたび 抽選 ※条件・上限あり ＼note クリエイター感謝祭ポイントバックキャンペーン／最大全額もどってくる！ 12.1 月〜1.14 水 まで](https://assets.st-note.com/poc-image/manual/production/20271127_pointback_note_detail.jpg?width=620&dpr=2)](https://note.com/topic/campaign)

Blender100レシピ！③海をつくろう｜Miki