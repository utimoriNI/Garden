---
title: Obsidian：WebClipを画像サムネ付きにしてみた - Jazzと読書の日々
source: https://wineroses.hatenablog.com/entry/2024/11/15/094052
author:
  - "[[Jazzと読書の日々]]"
published: 2024-11-15
created: 2024-12-01
description: これはこれでインターネット・データベース。 WebClip Obsidian Web Clipperのクリップを閲覧するdataviewスクリプト。 前回ArcSearch用クリッパーを作ったことで「サムネがつくと視認性が上がる」と気づき改良してみました。 こうなるとReadItLater系のアプリとしてObsidianが使えます。 ```dataviewjs const FOLDER = "Clippings" const CSS = "font-size:medium;" const p = dv.el("input","") p.placeholder = "..." p.style =…
tags:
  - Later
  - 🎁Topic/PKM
image: https://cdn.image.st-hatena.com/image/scale/9cfa0cef8826b371b3b90bce6d72a2724bb0db5f/backend=imagemagick;height=1300;version=1;width=1300/https%3A%2F%2Fgyazo.com%2F3fdcb2708cff40527efdd26f497455d5%2Fraw
---
これはこれでインターネット・データベース。
**consist of**:: [[PKM]]
#### WebClip

Obsidian Web Clipperのクリップを閲覧するdataview[スクリプト](https://d.hatena.ne.jp/keyword/%A5%B9%A5%AF%A5%EA%A5%D7%A5%C8)。

前回ArcSearch用クリッパーを作ったことで「サムネがつくと視認性が上がる」と気づき改良してみました。 こうなるとReadItLater系のアプリとしてObsidianが使えます。

```
\`\`\`dataviewjs
const FOLDER = "Clippings"
const CSS = "font-size:medium;"

const p = dv.el("input","")
p.placeholder = "..."
p.style = "width:50%;font-size:large;border-radius:3px;"
const b = dv.el("div", "")
b.style = "max-height:14000px;"
disp()

p.onkeyup = () => disp()

function disp(){
  const  d = dv.pages(\`"${FOLDER}"\`)
  .filter(x => x.title)
  .filter(x => (x.title + x.author + x.description).includes(p.value))
  .sort(x => x.file.mtime, "desc")
  .limit(200)
  .map(x => \`<tr style="${CSS}"><td style="width:20%;"><a class=external-link href='${(x.source)}'><img style="max-height: 100px;" alt="🌏️" src="${x.image || ''}"></a></td><td><a class=internal-link href="${x.file.name}">${x.title}</a><br>${x.description || "..."}</td></tr>\`)
  b.innerHTML = \`<br><table style='width:100%;'>${d.join("\n")}</table>\`
}
\`\`\`
```

#### 使用例

![](https://gyazo.com/3fdcb2708cff40527efdd26f497455d5/raw)

こんな感じですね。 表示上限は200項目にしました。

サムネをタップするとブラウザでWebサイトを開きます。 タイトルをタップすると、Obsidianのノートが開く。 どちらにもアクセスしやすい。

画像が用意されていないサイトは地球儀の絵文字にしました。

検索欄にキーワードを打ち込めば、タイトルとdescriptionを対象に検索します。 本文自体の検索ではないので（dataviewにはできないので）ご注意ください。

#### WebClipperの設定

WebClipperも画像対応に改造しましょう。

![](https://gyazo.com/4fbb96af2beba942693c89164e03b637/raw)

WebClipperを開いたとき、右肩にある歯車ボタンをタップします。

![](https://gyazo.com/018ac0360004019afedccdebb1db5230/raw)

テンプレートの「Default」を開き「プロパティ」で「プロパティを追加」をタップ。 プロパティ名を`image`、値を`{{image}}`にしてください。

設定はこれで完了です。 そのまま閉じても大丈夫。

WebClipで見たときに画像サムネ付きに変わります。

#### まとめ

Webクリップは死蔵しやすい。 それでいて、最近のインターネットは古い記事ほど埋もれやすい。 いい記事が消えていく。

そこをどうするか。 ランダムノートで出てくると面白いかな。