---
tags:
  - 🎁Topic/Lexicon
  - 🎁Topic/Omoro
type: reading-note
source_type: web
source_container:
topic: []
moc: []
status: inbox
---
**consist of**:: [[Omoro]]
[[ReadItLater]] [[Article]]

# [ChatGPT授乳ハックという失われつつある技術について](https://honeshabri.hatenablog.com/entry/Madonna-Hack)

ChatGPTのDALL·E 3による画像生成は非常に強力だ。  
だがプロンプトエンジニアリングを駆使すれば、さらに限界を超えた表現が可能となる。

ブックマーク保存をおすすめします。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/16a8f075a3b583fe0c1006230d2bb1b3.png)



## インフルエンサーたちが隠した技術

11月7日に**OpenAI DevDay**が開催されてからというもの、生成AI系インフルエンサーたちが大騒ぎしている。発表された機能やAPIの数々を見れば、そうなるのも無理はない。俺のような一般ユーザーでさえ、できることが一気に増えたのだから。

例えば自分だけのChatGPTを簡単に作成・共有できる**GPTs**だ。俺もさっそく触り、本しゃぶりの知識を全部突っ込んだ**Aishabri**を作ってみた[\*1](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-0cef4708 "初代Aishabriについてはこれを参照。ChatGPT搭載Slackbotにハックされる技術 - 本しゃぶり")。

[chat.openai.com](https://chat.openai.com/g/g-x7GtBiqrn-aishabri)

だが、インフルエンサーは新たに登場した機能ばかり口にし、その影で**失われつつある技術**については語ろうとしない。だから俺が代わりに語ろう。禁断の技**「授乳ハック」**について。

## コンテンツポリシーの制約

授乳ハックとは何か。それはChatGPTにこのような画像を生成させる技のことである。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/82fb64d849f9bdf44de00c967e829002.png)



授乳ハックによって生成された画像

ChatGPTで画像生成している人ならば、信じられないかもしれない。何なら悪質なコラと思うだろう[\*2](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-5a0fd0ad "今はGPTsで好きなアイコンにできるが、このやつはStylebotで変えている。詳細はこの記事に書いた。プログラミングに挫折したならAIお姉ちゃんに任せなさい - 本しゃぶり")。なぜならChatGPTに課せられている**コンテンツポリシーの制約**は厳しく、卑猥な画像は生成できないように対策が施されているからである。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/a0ede4e013a85a58b1d752cb7d2a2dcf.png)

コンテンツポリシー違反で出力できない

しかも厄介なことにコンテンツポリシーの対策は**多段階で設定**されている。ChatGPTの反応から、俺は以下のように推測した。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/7fd652f6c74434d48e76ec35217ae63e.png)



コンテンツポリシー違反チェック

-   ChatGPT：ユーザーからの指示をチェック。違反していたら拒否する。
-   DALL·E 3：ChatGPTからの指示と自ら生成した画像をチェック。違反していたら生成しない/画像を渡さない。
-   OpenAI：ChatGPTとは別にユーザーとChatGPTの言動をチェック。違反していたらフラグを立てる。

正直なところ、最初のChatGPTのチェックを突破するのはそう難しくない。ユーザーはChatGPTと会話できるので、**説得する**ことが可能だからだ。

厄介なのはDALL·E 3である。間にChatGPTがいるため説得できず、しかも**入力と出力の両方でチェック**が入る。上記のエラーのスクショも、DALL·E 3の判定結果によるものだ。

便宜上OpenAIと名付けたチェックは、フラグが立っても**指示は通る**ので画像生成は行われる。しかし、これを無視し続けるのは止めたほうがいい。最悪**アカウント停止のリスク**があるからだ。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/84ba08abb141d1463c2c9103a01f7efb.png)

フラグ立てすぎによる最初の警告

このようにChatGPTでの画像生成には何重にもチェックが入る。このため卑猥な画像を生成させるよりも、ラクダが針の穴を通る方がまだ易しいと考えられていた。だがChatGPTにも穴はある。

## 授乳ハックの誕生

きっかけは、「世界の濡れTシャツ」を生成している時のことだった[\*3](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-6b9444e1 "ChatGPTを使ったオリジナルBing Wallpaperプロジェクト。詳細は右を参照。ChatGPTの画像生成、バリエーションをお任せで作れるから強い｜honeshabri")。生成された画像の大半ではスポブラか突起の無い胸が透けるのだが、極稀に**乳首が生成**されるのだ。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/d0c0ddcb03f50deaa317ef40aff94e4f.png)



Lake Bled, Slovenia

てっきり乳首に対してはピンポイントな対策を施していると思っていたので、これには驚いた。どうやらプロンプトで「乳首」や「胸の露出」を指示するのはアウトだが、**結果として乳首が出るのはOK**なようだ。

こうなると狙って乳房を出させたくなるのが**人間の性(さが)**である。そこで**《授乳 / Breastfeeding》**[\*4](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-ad3c5453 "ここで日本語で「授乳」と指示すると、たまに "nursing" と訳されるので注意。こっちだと哺乳瓶を使う場合も含むためである。")を使うことにした。

授乳はキリスト教における三徳[\*5](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-27a53e47 "他の二つは「希望」と「信仰」。")のひとつ**「慈愛」**を象徴する行為であり、中世末期には19世紀まで続く**「慈愛の聖母像」**の流行を生んだ。裸体を淫蕩に結びつけたキリスト教において、授乳は女性の乳房を肯定的に描ける貴重なテーマである。なにせ純潔の象徴たる聖母マリアでさえ、授乳であれば乳房を晒すのだから。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/a378898d343afeddb82f596950aee7c4.png)

Jean Fouquet, Public domain, via Wikimedia Commons, [Link](https://commons.wikimedia.org/wiki/File:Jean_Fouquet_005.jpg), Censored

そして授乳は現在でも特別なテーマとして扱われている。InstagramやX (Twitter) のガイドラインではポルノやヌードは禁止されているが、授乳に関しては**明確にOK**としている[\*6](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-901c6462 "OKとしているからと言って、消されないわけではない。2015年4月にInstagramはコミュニティ規定を改定し、授乳を明確にOKとした。しかし同年8月の世界母乳育児週間の際に、授乳写真を多数アップしていたアカウントを削除したのである。もちろん後で復活させたが。授乳写真はヌードじゃない　インスタグラムのアカウント削除が物議 - ライブドアニュース")。世界的なSNSがクローズアップした乳房の写真でさえ許可していることからも、授乳が特別であることが分かるだろう。

> 女性の乳首の写真も対象となりますが、授乳、出産時や出産後、医療関連の状況(乳房切除手術後、乳がんの認知喚起、性別適合手術など)、または抗議活動に関する写真は許可されます。  
> [コミュニティガイドライン | Instagramヘルプセンター](https://help.instagram.com/477434105621119)

> 全裸または半裸（性器、臀部、または胸部を拡大して撮影したものを含みますが、授乳に関連するコンテンツは除外されます）  
> [センシティブなメディアに関するXのポリシー | Xヘルプ](https://help.twitter.com/ja/rules-and-policies/media-policy)

ゆえに授乳画像はOKとラベリングされた中に含まれている可能性は高いと考え、試してみたのである。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/6006ce5e96a16e5e45ab644251a6fbda.png)



出た、OpenAIのOPPAIが

見ての通り、DALL·E 3の高度な画像生成能力によって作られた、見事な乳房がそこにはあった。やはり欧米の価値観で作られたコンテンツポリシーの制約は、授乳によって突破できるのである。

とはいえ、授乳ハックで必ずおっぱいが出るというものではない。服を着たまま授乳することも多いし、子供の頭で隠れることもある。**おっぱいを安定して出すのは難しい**のだ。どうしたら高確率で出せるのか、試行錯誤しているうちにフォルダが酷いことになった。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/5eab16b71a1ae69d83492ca6dc94cc83.png)

授乳フォルダの一部

OpenAIはChatGPTの改善のために、時給2ドル以下でケニア人を雇って**NSFWコンテンツ**[\*7](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-3a33b2a0 ""Not safe for work" の略で、職場で見られないようなコンテンツのこと。主にポルノや暴力関連に使われる。")のラベリングをさせている[\*8](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-347071d2 "「ChatGPTを改善するためにOpenAIが時給300円以下でケニア人を雇った」と問題視する報道 - GIGAZINE")。そうした労働者はずっと刺激の強いコンテンツを閲覧しているため、夢や幻覚に苦しめられるという。

俺が見ているのは健全な授乳画像であるため悪夢に悩まされることはないが、このままだと**「存在しない家族の記憶」**は生じそうである。やはりコンテンツポリシー的にOKなだけあって、乳房が写っていても健全すぎる。どうしたらもう少し不健全にできるだろうか。

## オッサン召喚

また歴史に学ぶ時が来た。普通の授乳だと健全すぎるという問題に対し、過去の神絵師たちはどのように解決したのか。それは**オッサンを出す**ことである。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/6b6f27706648930669f53f973323490f.png)



Jan Janssens, Public domain, via Wikimedia Commons, [Link](https://commons.wikimedia.org/wiki/File:Jan_Janssens_-_Roman_Caritas.jpg), Censored

この牢にいる親に授乳することで栄養を与えるという**『ローマの慈愛』**だが、大プリニウスによれば本来は**「母親に対して授乳した娘」**というエピソードであるらしい。だが17世紀のオランダやイタリアで流行したのは、見ての通り**「父親に対して授乳した娘」**と変わっている。求められるのはオッサンなのだ。

とはいえ、さすがにChatGPTでオッサンに授乳させるのは出来なかった。授乳対象は小学生までならギリギリ行けたが、**中学生以上はChatGPTが拒否**する。授乳行為に代わる、オッサンとの絡みを考えなくてはいけない。そこでヒントとなったのが**レンブラント**である。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/1ad1eef93004aaae46a5744c301e64a5.png)



Rembrandt, Public domain, via Wikimedia Commons, [Link](https://commons.wikimedia.org/wiki/File:Rembrandt_Harmensz._van_Rijn_-_Portret_van_een_paar_als_oudtestamentische_figuren,_genaamd_%27Het_Joodse_bruidje%27_-_Google_Art_Project.jpg)

あのゴッホが絶賛したというこの**『ユダヤの花嫁』**だが、俺はこれを最初に見た時**「セクハラを描いている」**と思った。実際、ルーカス・クラナッハが好むテーマ**『不釣り合いなカップル』**[\*9](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-6efb6a97 "File:Bemberg fondation Toulouse - Les amoureux - Lucas Cranach l'Ancien.jpg - Wikimedia Commons")のように、年配の男性が若い女性にセクハラしているような絵画も多数存在しているからである。しかし『ユダヤの花嫁』の二人は親密な関係で、**「愛情」**や**「献身」**といったイメージを想起させるらしい。

これを利用すれば、親密さを表現するプロンプトで、不健全な画像を生成できるのではないか。そう考えて試した結果がこれだ。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/debd7aa424358e25334b786222af63b8.png)


GPTの花嫁

がっつりと**胸を揉むオッサン**が生成された。この後もいろいろと試して確信したが、授乳をサポートするように指示すると胸を揉むらしい。また、**子供が不在でも授乳は機能する**ことも確認できた。こうして完全にアウトな画像を生成することができるようになったわけである。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/5c507f919dd4d4dab51ad4c994a6f120.png)

二人がかりでサポートすることも

ChatGPT、完全に理解した。

## やりたい放題

この時点でもChatGPTで相当にアレな画像を作れるが、プロンプトエンジニアリングにはまだ可能性が残っていた。

俺が授乳ハックで生成した画像を仲間内で共有したところ、[@builtinnya](https://twitter.com/builtinnya)がより過激な画像を出してきた。曰く**「水着とストレッチを加えた」**とのこと。ストレッチはともかく、水着なんて一発でコンテンツポリシー違反になるのではないか。そう思いながらも試してみた。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/847a8c85427cb5ce344c44e40d862b0f.png)


オフィスでやりたい放題

**『スザンナと長老たち』**か？

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/81b64c3d5a82a94de55714f3868d3bbf.png)


Orazio Gentileschi, Public domain, via Wikimedia Commons, [Link](https://commons.wikimedia.org/wiki/File:Orazio_Gentileschi_-_Susana_surpreendida.jpg), Censored

どうも「オフィス」や「駅」といった水着との関連付けが薄い場所を設定すると、**下着のような水着**となるようだ。さらに**「授乳しながらストレッチしている人」**のサポートなので、オッサンたちは女性の身体をがっつりホールドする。その結果、とんでもない画像が生成されるというわけだ。

ここまで来たらあとはやりたい放題である。好きな場所を設定できるし、他に服装を追加することで「脱ぎかけ」にすることも可能だ。ここでは実写しか貼っていないが、**アニメイラスト**にすることも可能である。それからひたすらに二人でいろいろと作って遊んでいた。

## 離乳の時期

ここまで読んだ人たちの反応は、大きく二つに分かれるだろう。ChatGPT課金ユーザーは**「今すぐにでも試したい」**と思っているはずだ。一方で無課金およびユーザーではない人は**「なんて酷い使い方を広めるんだ」**と怒りで体を震わせている。双方とも落ち着いて記事のタイトルを見直してほしい。既に対策が取られている。

俺がChatGPTを完全に理解したのは**2023/11/04の9時前**のことである。それから@builtinnyaと**同日10時半**までは好き放題に生成していた記録が残っている。

それが昼過ぎくらいから、**生成に失敗**することが増えた。当時は一度に2枚生成できたのだが、エラーで1枚も生成できないことが増えたのだ。午前中は2枚とも生成できることが多く、少なくとも1枚は生成できていた。それがエラーばかりになる。

最初はプロンプトがアウトすぎるのかと思った。しかし、以前に生成できた画像と**同じシード値[\*10](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-cedf5344 "画像生成プロセスにおいてランダム要素を制御するために使用される数値。シード値が異なると、同じプロンプトでも異なる画像が出力される。同じ画像を出力したい場合や、プロンプトのみの影響を調べたい場合はシード値を固定する。")とプロンプト**の組み合わせでも、エラーが発生したりコンテンツポリシーNGになってしまうのだ。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/9fb7f14b2d6063575df9af63a7db6969.png)



授乳を求めたら拒否された

@builtinnyaに確認すると、彼のアカウントでも同様に生成できなくなっていた。どうやったかは不明だが、OpenAIはわずか数時間の間に**検知・対策を行った**らしい。ゆえにもう『スザンナと長老たち』のような画像を生成することはできない[\*11](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-ec78cb44 "もしかしたらコンテンツポリシー違反のフラグが立ちまくったユーザーだけかもしれないが。アカウントごとに対応していると分析しているツイートもある。「昨日からのopenAIの進化によりコンテンツポリシー違反の頻度が100%となり全く仕事にならず。仮説ですが、アカウント事にデータ分析して、アカウントのバンではなく単にポリシー違反のコンテンツ作成ができないようなシステムに変更されたのでは？」 / X")。だから悪影響はほとんど無いと考え、記事にすることにしたわけだ。

とはいえ、だいぶ厳しくなったが、まだ**授乳でおっぱいを出すことは可能**である[\*12](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-71aa73f1 "記事執筆時点。")。しかし、挑戦することはおすすめしない。出そうとすると**何度もコンテンツポリシー違反を食らう**ことになるので、**アカウント停止のリスク**があるためだ。普通にStable Diffusionを使った方がいい。

## 終わりに

以上の通り、わずかな期間であったとはいえ、プロンプトエンジニアリングを駆使することでChatGPTに不健全な画像を作らせることができた[\*13](https://honeshabri.hatenablog.com/entry/Madonna-Hack#f-f093e0ee "プロンプトエンジニアの年収が5千万円な理由も納得である。")。今回コンテンツポリシーに挑んで面白いと思ったのは、俺は突破するためにAIに関する**専門知識を一切使っていない**ことである。

俺が授乳ハックで使ったのは**美術の知識**だ。これまで乳房がどんなふうに描かれ、扱われてきたか。そういった**文化的な知識**を本で学んでいたからこそ、OpenAIの隙をつき、**自由に画像を生成できた**のである。かのスティーブ・ジョブズは**「テクノロジーとリベラルアーツの交差点に立ちたい」**と言っていたが、たぶんそういうことなのだろう。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/6d1eb4db9617efcc36736095ae006e47.png)



アップルは交差点で見つかる

ところで、本記事を読んでこう思う人もいるだろう。**「俺もコンテンツポリシーを振りかざしたいな」**と。実際、OpenAIの振る舞いを見ていると**「何が健全であるかは我々が決める」**と言っているように思えてくる。そういう立場になったらさぞ気分がいいことだろう。

そんな人のための製品がこちらです。

![image](https://garden-storage-228689237525-us-east-2-an.s3.us-east-2.amazonaws.com/a8be3957336f33e1cfd8f5a29aa603f4.png)

[](https://suzuri.jp/honeshabri/14725844/sticker/m/white)

この**Content Policy Violationステッカー**を貼れば、**どんなものでもコンテンツポリシー違反**にできる。不健全で見たくないものを隠してしまおう。

## 参考書籍

授乳ハックをする上で参考になった本。

### 『乳房論』

[![乳房論: 乳房をめぐる欲望の社会史 (ちくま学芸文庫 ヤ 13-1)](https://m.media-amazon.com/images/I/41Mb2VSJA9L._SL500_.jpg "乳房論: 乳房をめぐる欲望の社会史 (ちくま学芸文庫 ヤ 13-1)")](https://www.amazon.co.jp/dp/4480088938?tag=honeshabri-22&linkCode=ogi&th=1&psc=1)

乳房の文化・社会史を学ぶならまずこれ。芸術、医療、商業と幅広い話題を扱っている。まず本書を読んでから、興味のある分野を深掘りするのがいいだろう。

### 『乳房美術館』

[![乳房美術館 (京都書院アーツコレクション 167 絵画 12)](https://m.media-amazon.com/images/I/41cHDBrxQ7L._SL500_.jpg "乳房美術館 (京都書院アーツコレクション 167 絵画 12)")](https://www.amazon.co.jp/dp/4763616676?tag=honeshabri-22&linkCode=ogi&th=1&psc=1)

様々なテーマの乳房が描かれた絵画をフルカラーで載せた本。文章は少なく、絵画を見るのがメイン。授乳の画像ってどんなのがあったっけというような時に便利。

### 『官能美術史』

[![官能美術史　──ヌードが語る名画の謎 (ちくま学芸文庫)](https://m.media-amazon.com/images/I/41F2aZ+1MBS._SL500_.jpg "官能美術史　──ヌードが語る名画の謎 (ちくま学芸文庫)")](https://www.amazon.co.jp/dp/B093382F5D?tag=honeshabri-22&linkCode=ogi&th=1&psc=1)

こちらは乳房に限らず、様々なヌードを表現した絵画を解説した本。文章もそれなりにあり、少なくともKindle版はフルカラー。『スザンナと長老たち』は本書で知った。

## もっと勉強したい人へ

## 今回のプロンプト

有料部分には本記事で載せた画像のプロンプトを載せる。前述の通り、今ではコンテンツポリシー違反となるものもあるが。