---
title: 【Blender】3DCGを活かして背景イラストを描く方法について｜そとうみ｜pixivFANBOX
source: https://sotoumi.fanbox.cc/posts/11444698?utm_campaign=post_page&utm_medium=share&utm_source=twitter
author:
  - "[[そとうみ]]"
published: 2026-03-13
created: 2026-03-13
description: 今回は、3DCGを活かして背景を描く方法について解説したいと思います。前回とは違ったアプローチとなっています。3DCGを活かして背景イラストを描くメリットは以下の4点だと思っています。・パースを考える必要がない・難しい形状も正確に描写できる・レイアウトを自由に変更できる・一度作ったモデルはほかの作品...
tags:
  - 🎁Topic/Blender
  - 🎁Topic/Illust
image: https://pixiv.pximg.net/c/1200x630_90_a2_g5/fanbox/public/images/post/11444698/cover/KBzGiik8rMMSbhLCE6mjpRFs.jpeg
---
## 【Blender】3DCGを活かして背景イラストを描く方法について

2026年3月13日 17:46・全体公開

今回は、3DCGを活かして背景を描く方法について解説したいと思います。前回とは違ったアプローチとなっています。

  

3DCGを活かして背景イラストを描くメリットは以下の4点だと思っています。

・パースを考える必要がない

・難しい形状も正確に描写できる

・レイアウトを自由に変更できる

・一度作ったモデルはほかの作品に流用できる

## 使用ソフト

・Blender

（ver4.1を使用しています、任意のバージョンで可）

・CLIP STUDIO PAINT

（その他ペイントソフトで代用可能です）

## 手順

1：モデリングの前にラフを大まかに描きます。理想のゲーム部屋が作りたい！という発想からラフを描いています。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/W5YzS1zXuMs3ALPb54I3JPns.jpeg)

モノの配置や、レイアウトなどは3D上で自由に調整できるので、ここでは「何を作るか」を特に意識して描いています。

  

2：モデリングをします。↓こちらが完成したもの。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/krnEDRTS1nbzcVMcXR5QVaN4.jpeg)

↑ラフから3Dを作る段階で、モノの配置やレイアウトを調整しています。ラフの段階ではなかったものも追加しています。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/A7PXBGxVubonNX2uDWH5hguK.jpeg)

↑ゲーミングPCは基本的に立方体と円柱とベジエカーブの組み合わせで作っています。ループカットと押し出し、面の差し込みなどを使っています。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/udlX6Et06nY2YSvveEAT9OWN.jpeg)

↑スピーカーも立方体と円柱の組み合わせです。球体状のくぼみはブーリアンモディファイアを使っています。

  

モデリングのコツ

・実物の写真や図面を見ながら作る。

・特に頻繁に使う基本操作として、法線に沿って押し出し(Alt+E)、面の差し込み（I）、ループカット（Ctrl+R）、ベベル（Ctrl+B）、ループ選択（Alt+左クリック）、プロポーショナル編集（O）などのショートカットを覚える。

・使う頻度の高い「配列」、「ブーリアン」、「ミラー」の3つのモディファイアを覚える。

  

3：Freestyleの適用。レンダープロパティタブの下のほうにあるFreestyleにチェックを入れます。ライン幅モードは絶対値、ライン幅は0.2pxに設定しました。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/c0Oz2gbuwSCUXIGSaUbkmZnw.jpeg)

そして、この設定を適用した状態で画像をレンダリングすると、下記画像のようにオブジェクトのアウトラインに沿って線画ができます。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/ixqU0vFyboM8UKhbj9OGg7ON.jpeg)

Tips：カリグラフィモディファイア

ビューレイヤープロパティからFreestyleの線についていろいろ設定できます。例えばカリグラフィモディファイアを追加すると…

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/B2Z4AXBYQ2tx66ag77sdZ81I.jpeg)

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/CtSBm9tTStuOTyjrPnP4bs9v.jpeg)

↑線にいい感じの手描きっぽい強弱がつきます。

  

4：レンダーパスから線画のみを書き出します。ビューレイヤープロパティからFreestyleのレンダーパスに出力にチェックを入れます。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/oAdYfNjcwgTeMBu2DLc3na5E.jpeg)

次にコンポジットウィンドウを開き、ノードを使用にチェックを入れます。追加→出力→ファイル出力ノードを追加してレンダーレイヤーのFreestyleとつなげます。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/KBwHlcdhLVgAqkI676LUA4EW.jpeg)

基本パスのファイルボタンをクリックするとBlenderファイルビューが出てくるので保存先を指定すると、任意の場所に線画だけを保存できるようになります。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/fz5KQYM5YQiOLuFMLc5sa7We.jpeg)

このまま、画像をレンダリングすると、先ほど指定したファイルに線画がPNG形式で保存されているはずです。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/EpkvRIC8FahLv92sj1Ba4nUy.jpeg)

  

CLIP STUDIO PAINTでの作業に移行

5：↓クリスタで線画を読み込み、それを元にバケツ塗りで色を置いていきましょう。色選びはかなり苦戦するところです、永遠の課題かもしれません。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/FN05hPn0PdtPO6eLeObMBPaX.jpeg)

  

3DCGでのライティングをイラスト上で再現する

6：↓3Dのライティング結果をそのままイラストの影として活用しましょう。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/LFVCh8dL0dOf1zNkzjso9jtN.jpeg)

1：物体が落とす影

ライティングしたレンダリング画像をクリスタに読み込みます。その画像レイヤーを選んでラスタライズ（Z）を選択。さらに色調補正から2値化を適用、閾値を調整して、物体が落とす影を抽出します。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/PaSKeW7hAZse6nznBgSPSheo.jpeg)

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/jSpTrkZ2hYiHxvXzK9u7OwPZ.jpeg)

次にレイヤーの合成モードを乗算にして、色を塗りつぶしたレイヤーでクリッピング→合成モードを比較（明）にします。影の色を変えたい場合は、塗りつぶしレイヤーの色を変えるだけでOKです。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/qRgxFYLeNmwAd02ff4EjEBfw.jpeg)

↓先ほどの下塗りレイヤーと合わせるとこのような感じになります。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/mJICb0fc4R5WMWuVScRNt2QI.jpeg)

影の形が気になる箇所は、あとで加筆して修正しましょう。2値化レイヤー上で黒を塗った部分が影になります。

  

2：全体的な陰影

次に同じように色調補正から2値化を適用、閾値を調整して、全体的な陰影を抽出します。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/hj8alepwlrCxyGRCjK8BjeK3.jpeg)

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/TpN3RGPaeNcpJWEnPv8xf5Tx.jpeg)

こちらをそれぞれ、全体的な光（スクリーン）と影（乗算）に適用します。

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/uv0yeJfhuCHDmxVDNNUlh974.jpeg)

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/04ONxoYeABbft2WcqAaj2BCF.jpeg)

これで3DCGのライティングをイラストに反映させることができました。

↓

この後はお好みで色調補正、加筆、加工、人物などを描き加えて仕上げていきましょう。

↓

完成

![](https://downloads.fanbox.cc/images/post/11444698/w/1200/FhUZOYUe6L1bLU7b5AtZP6L9.jpeg)

明暗のバランスの調整とモニターやゲーミングPCの光などを追加して、ゲーム部屋らしい鮮やかな印象にしました。（今回の作品は2023年に制作したものに微調整を加えたものです）

  

  

## 【blendファイル配布（支援者限定）】

ゲーム部屋のblendファイルを配布しています。モデルをそのままイラスト制作に使ったり、改造して自分好みにアレンジしたり、モデリングの参考にしたりと自由に活用してみてください。

[https://sotoumi.fanbox.cc/posts/11540800](https://sotoumi.fanbox.cc/posts/11540800)