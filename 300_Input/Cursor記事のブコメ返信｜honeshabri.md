---
title: "Cursor記事のブコメ返信｜honeshabri"
source: "https://note.com/honeshabri/n/nc4355af890d1"
author:
  - "[[note（ノート）]]"
published: 2025-03-24
created: 2025-04-18
description: "最近ハマっていたCursorの記事を書いたらブクマがいっぱいついたので、毎度のごとくブコメ返信をする。  Cursorを使った文章執筆は、AIファーストな環境整備から始まる - 本しゃぶりMarkdown形式での情報一元管理と音声入力、そしてCursorというAIエディタの組み合わせで、執筆環境が一変した体験honeshabri.hatenablog.com  Obsidianがハネた   AIエージェントでObsidianがハネてるよなぁ。データはローカルに囲い込まない形式で再利用性が高いのが良い。昨年末、Notionじゃなくてこっちを選んで良かった（今の"
tags:
  - "Later"
  - "🎁Topic/"
  - "Scrap"
image: "https://assets.st-note.com/production/uploads/images/180645806/rectangle_large_type_2_c90eb142acd167ba0412399f58bff65d.jpeg?fit=bounds&quality=85&width=1280"
---
![見出し画像](https://assets.st-note.com/production/uploads/images/180645806/rectangle_large_type_2_c90eb142acd167ba0412399f58bff65d.jpeg?width=1200)

## Cursor記事のブコメ返信

[honeshabri](https://note.com/honeshabri)

参加中

最近ハマっていたCursorの記事を書いたらブクマがいっぱいついたので、毎度のごとくブコメ返信をする。

[**Cursorを使った文章執筆は、AIファーストな環境整備から始まる - 本しゃぶり** *Markdown形式での情報一元管理と音声入力、そしてCursorというAIエディタの組み合わせで、執筆環境が一変した体験* *honeshabri.hatenablog.com*](https://honeshabri.hatenablog.com/entry/cursor_markdown_ecosystem)

## Obsidianがハネた

> AIエージェントでObsidianがハネてるよなぁ。データはローカルに囲い込まない形式で再利用性が高いのが良い。昨年末、Notionじゃなくてこっちを選んで良かった（今のところ）

[https://b.hatena.ne.jp/entry/4767984885445080225/comment/denimn](https://b.hatena.ne.jp/entry/4767984885445080225/comment/denimn)

これはマジでそう。俺がObsidianに移行した時には既に生成AIが登場していたから、いかにうまく使うかというところに注目していた。当時はObsidianに拡張機能のObsidian Copilotを入れて、従量課金制ながらも好きなAIを使い放題という環境を構築していた。

ただ、従量課金制だとどうしても気軽に使えない。結局Obsidian Copilotの使用をやめ、マークダウンファイルを直接ChatGPTやClaudeにアップロードして対応していた。そんな使い方が続いていたが、CursorによってついにAIがObsidianの保管庫を直接参照できるようになった。

Obsidian自体は何のバージョンアップもしていないのに、いきなり価値が爆上がりしているのが面白い。Notionも一応MCPなどを使えばClaudeやCursorから操作できるが、直接ファイルをいじれる自由度はやはりObsidianの方が上。Obsidianが時流に乗っている感じがして良いね。

## ChatGPTの出力結果の保存

> ChatGPTなどのLLMに対する入出力の結果ってどうmarkdownにしているんだろう。普通はGUI上だと思うけど、一括ダウンロードしてObsidian管理下に置いたりできるんだろうか。

[https://b.hatena.ne.jp/entry/4767984885445080225/comment/soratokimitonoaidani](https://b.hatena.ne.jp/entry/4767984885445080225/comment/soratokimitonoaidani)

これは簡単で、基本的にはObsidianにコピペしている。Obsidianは書式付きテキストを貼り付けると自動的にマークダウンに変換してくれる。ChatGPTとの会話を全部保存したいなら、Ctrl+A、Ctrl+Vで完了だ。

上部に不要な部分が残ることもあるので、適宜選択して一括削除すれば、構造化された状態で出力される。もう少し整えてから貼り付けたい場合は、キャンバスを作ってその内容をコピーしてObsidianにペーストするパターンが多い。

また、CursorにChatGPT拡張機能を入れると、アプリ版のChatGPTがCursorで開いているマークダウンファイルを参照・編集できるようになる。Cursorの使用枠を消費したくない時は、ChatGPTに直接マークダウンファイルをいじらせるということもやっている。

## 文章補完が使えない

> AIの文章補完はぜんぜん使い物にならないんだが...

[https://b.hatena.ne.jp/entry/4767984885445080225/comment/wnd\_x](https://b.hatena.ne.jp/entry/4767984885445080225/comment/wnd_x)

> 取り組みとしては面白けど、AIが文書の次を書き出すとそっち気が取られて雑念がうまれそうなのがね。AIで文章を生成しても何度も書き直すだろうから、自分ならたたき台を書いてもらうぐらいの使い方になると思う。

[https://b.hatena.ne.jp/entry/4767984885445080225/comment/misshiki](https://b.hatena.ne.jp/entry/4767984885445080225/comment/misshiki)

文章補完というのはCursorの機能で、ある程度文章を書いたら次の候補を自動的に出してくれるものだな。Tabを押すとその候補が挿入される。

俺の記事で書いた使い方をよく読んでもらえば分かると思うが、この文章補完はほとんど使っていない。なぜなら、まず全部話してから、それをAIに整えてもらい、さらに修正を重ねていくというスタイルなので、自分で直接入力する機会が少ないのだ。そのため文章補完の出番がない。

ただ、編集時に括弧やマークダウンの記法を入力する際には役立っている。例えば、括弧の始まりを入力すると、文章補完で閉じ括弧も出てくるので便利だ。マークダウンの強調やリンクなどを修正するときも同様に使える。

ブコメでは文章補完が使えないという指摘と、AIが次の文を書き出すと気が散るという懸念が述べられているが、俺の使い方では文章補完の「使えなさ」はあまり問題にならない。むしろ、タグやマークダウン記法の補完という点では十分役立っていると感じる。

## 本人に書いて欲しい

> 一読者としてはAIか本人か書いた境界線が微妙な文章は読みたくない。それこそAIに要約して頂く

[https://b.hatena.ne.jp/entry/4767984885445080225/comment/hetoheto](https://b.hatena.ne.jp/entry/4767984885445080225/comment/hetoheto)

ここから先は有料部分です

本人に書いてもらうのが良くて、AIはやめてほしいという気持ちは理解できる。ところで今回の記事もAIを全面的に活用しているわけだが、これも要約したのだろうか。

一方で、AIが編集したもの以上に俺自身が喋りまくっており、自分で手書きしていた時以上に「俺の気持ち」は乗っているとも言える。読者の自由だが、そもそも「AIが書いたか俺が書いたか」という区別が本当にできるのかは疑問だ。

## 物書きやらなくていいのでは

> うーん、ここまでやらないと文章書けない人は正直、物書きやらなくていいのでは？と思う。生産性生産性って、何を生産しているの？

[https://b.hatena.ne.jp/entry/4767984885445080225/comment/evergreeen](https://b.hatena.ne.jp/entry/4767984885445080225/comment/evergreeen)

これほど短い文章の中でこれだけ的外れなことを述べられるとは感心する。まず、「ここまでやらないと」という前提が間違っている。継続的に文章を書き、資料を見ながら執筆するなら、AIの有無に関わらず情報整理は当然必要だ。これはAI以前の問題であり、俺は生成AI登場以前から情報整理を行なっていた。ただそれがAIの登場でより効率化できるようになったというだけだ。

次に「物書きやらなくていいのでは」という点。俺は10年以上も執筆を続けてきたのであり、当然ChatGPT登場よりも前からだ。物書きをやっているからこそここまで効率化を目指すのであって、順序が逆だ。継続的に文章を書いている人は自分なりのやり方を効率化していくものだ。

さらに言えば、物書き以外でも文章を書く機会は多い。俺は仕事でも多くの文章を書いており、同じ手法で効率化できると便利だ。これを「物書きだけが使う」と狭く考える視野の狭さには驚く。

「何を生産しているの？」という問いにも答えよう。俺はブロガーとして記事を生産しており、これが読者の目に触れる文章そのものだ。noteでも日々執筆し、週刊プレイボーイでも連載している。つまり「文章」を生産しているのは明らかだ。

これほど基本的なことすら理解できずに的外れな批判をする人間に、いくつものスターがついていることにも驚きを隠せない。よくもまあこんな的外れな意見に賛同できるものだと感心する。

[**Throw a marshmallow to 骨しゃぶり | Marshmallow** *Accepting anonymous messages. はてブとニチアサ実況するブロガー* *marshmallow-qa.com*](https://marshmallow-qa.com/honeshabri)

  

## 高評価して応援しよう！

人に対し何かをしてあげるという事は、全て「見返り」を期待しての行為だ。noteのサポートは文章を読むための「見返り」である。

Cursor記事のブコメ返信｜honeshabri