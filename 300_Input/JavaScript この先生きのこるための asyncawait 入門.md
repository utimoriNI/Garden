---
title: "[JavaScript] この先生きのこるための async/await 入門"
source: https://note.crohaco.net/2018/js-async-await/
author:
  - "[[くろのて]]"
published: 
created: 2025-04-20
description: Webには欠かせない非同期処理。まだメソッドチェーンで書いたりしていませんか？ES2017 で新たに登場した async/await を使ってきれいな処理をかけるようになりましょう。
tags:
  - 🎁Topic/Tech
image: https://note.crohaco.net/media/javascript.png
---
2018-07-12

Webプログラマーはもう JavaScript を避けて通ることができないようです。

今回は ES2017 で新たに登場した async / await 構文について理解するために記事を書きました。

簡単に言うと これらは `Promise` オブジェクトをうまく扱うための仕組みです。

## Promise

これ を知らないことには async, await は理解できません。 かんたんに言うと `Promise` は 非同期処理の結果が格納されたオブジェクトです。

普段は fetch 等の リクエストを実行するような関数が Promise を返却するので生で触ることはあまり多くありませんが、 この記事では多用していきます 💪

Promise オブジェクトの作成は 第一引数で受け取った関数を実行するような関数を Promise に渡してあげるだけです。 うーん、余計難しくなってしまいました。

たとえば 10秒待つ `Promise` は以下のように作ります。

``   `promise =newPromise(resolve=>setTimeout(resolve,10000))// 単位はミリ秒`   ``

`resolve(値)` のように呼び出されることで、 `promise` は `初期状態` から `解決状態` に遷移します。 今回は解決状態になるタイミングを制御することで「待つ」を実現しようというわけです。 ただし、上記を実行しただけでは 何も起こりません。

ここで重要になるのが `promise.then(関数)` メソッドです。 このメソッドは、promise が **初期状態** のときは処理をブロックし、 **解決状態** になると処理結果(resolveの実引数)を抽出できます。

例えばこのように書くと 10秒後に `test` が出力されます。(今回、処理結果は未指定)

``   `promise.then(()=>console.log('test'))`   ``

インスタンスが生成された瞬間から Promise に渡された 関数はコールされているため、 上記を実行するタイミングによって `test` が出力されるタイミングは異なります

``   `promise =newPromise(resolve=>setTimeout(resolve,10000))// すぐに実行したら 10秒待って出力されるし// 10秒後に実行したらすぐ出力されるpromise.then(()=>console.log('test'))`   ``

これが Promise の基本です。

fetch api を使ってる人は `fetch(url).then` ってよく書いてたと思いますが、 あれは Promise オブジェクトのメソッドだったのですね。

メソッドチェーン

- `then()` メソッド は Promise オブジェクトを返却することで、 `promise.then(f).then(f2).then(f3)` のように 無限につなげることができます。
- fetch api だと `fetch(url).then(res => res.json()).then(data => {console.log(data)})` みたいにしてましたよね。
- 自分で Promise オブジェクトを指定することで、 10秒待って出力、さらに5秒待って出力、みたいなこともできます。 ``   `promise =newPromise(resolve=>setTimeout(resolve,10000))promise.then(()=>{console.log('test1')returnnewPromise(resolve=>setTimeout(resolve,5000))}).then(v=>console.log('test2'))`   ``

## async と await

分けて説明したいところですが、別々に利用することはできないため同時に説明します。

async は 関数の前につけて定義し(以後非同期関数という)、 await は 非同期関数のローカルスコープで利用することで処理をブロックします。

await が何を元にブロックするかというと、これが 前述した `Promise` オブジェクトなわけですね。やっと繋がりました。

info

- 非同期関数以外のスコープで await すると以下のようなエラーになります。
	- `Uncaught SyntaxError: await is only valid in async function`
	- 関数がネストしている場合、直近のスコープが非同期関数であることが求められます。
- await が受け取るのは Promise オブジェクトじゃなくてもエラーにはなりませんが、何も起こりません。
	- 代入文の場合、左辺にそのまま格納されます。
- Promise にわたす関数の 第一仮引数名は `resolve` とするのが慣例らしいです。
- `resolve` の第一実引数は await の左辺に渡されます ``   `hand=v=>newPromise(resolve=>resolve(v,));(async()=>{let a =awaithand('123')console.log(a)let b =awaithand('456')console.log(b)})()`   ``

await が Promise オブジェクトを受け取ると オブジェクトの状態が `resolved` になるまでブロックし、以降のプログラムは待ち状態になります。

これを利用して sleep 関数を書いてみましょう。

``   `sleep=time=>newPromise(resolve=>setTimeout(resolve, time)); (async()=>{// 非同期関数を即時実行しているだけawaitsleep(3000)console.log(1)awaitsleep(5000)console.log(2)// 返却値が await に渡されてるだけなので以下のように書いても同じ// await new Promise(resolve => setTimeout(resolve, 5000))})()`   ``

上記を実行すると 3秒待って `1`, 5秒待って `2` が表示されましたね。

warning

- 旧石器時代には開始と終了時刻の差分が指定時間を満たすまで while でループさせるような方法もあったようですが、 あれは CPU パワーをフルに使うのでタブ(あるいはブラウザ)がフリーズします。
- 最近は期待通りの挙動をしないプログラムをサイトに配置すると起訴されるみたいなので気をつけましょう。

ちなみに fetch api の `fetch(url).then(res => res.json()).then(data => {console.log(data)})` は await を使うと 以下のように書けます。

``   `res =awaitfetch(url)data =await res.json()`   ``

`then()` がなくなり、コールバック関数の中でしか得られなかった data が 同じスコープで 得られるのです。

ちょっと待ってください。 async は await を包むためのただの ラッパーなのでしょうか？

実は async は その名の通り 非同期関数なので、 関数の中は (await がある限り) 同期的に処理をしますが、 関数の外では (awaitに差し掛かると) 非同期に働きます。

``   `f=async(i)=>{awaitnull;console.log(i)}f(1)console.log(2)f(3)console.log(4)`   ``

これを実行すると `2`, `4`, `1`,`3` の順番で表示されるはずです。 (await がないと `1`, `2`, `3`, `4`)

これを同期的に処理したい場合、さらに 非同期関数の結果で await すればいいです。これは 非同期関数が Promise を返却するからです。

``   `(async()=>{f=async(i)=>{awaitnull;console.log(i)}awaitf(1)console.log(2)awaitf(3)console.log(4)})()`   ``

そのために さらなる 非同期関数で囲む必要があるのは少し面倒ですけどね。

## map の callback として使いたい

Webアプリケーションでは「負荷を軽減するために リクエストは間隔を空けて送信する」みたいな仕様があるかもしれません。

それに見立てて、 `['a', 'b', 'c']` を 3秒間隔で イテレーションしながら 表示するプログラムを考えてみましょう。

まず、以下のように考えました。

``   `sleep=time=>newPromise(resolve=>setTimeout(resolve, time)) list =['a','b','c'] list.map(asyncv=>{awaitsleep(3000)console.log(v)})`   ``

じつはこれ、期待通りに動きません。

理想

- 開始
	- `(3秒待つ)`
		- a が表示
			- `(3秒待つ)`
				- b が表示
					- `(3秒待つ)`
						- c が表示
- のように直列処理されてほしかったんですが

現実

- 開始
	- `(3秒待つ)`
		- a が表示
	- `(3秒待つ)`
		- b が表示
	- `(3秒待つ)`
		- c が表示
- のように並列処理され、3秒後に同時に表示されてしまいます。現実は厳しい。

まぁ非同期関数の性質を思えば仕方のないことです。

解決方法は以下です。

### Solution - for

map によるイテレーションではなく for を使う方法です。

普通の for はだるいので ここでは `for of` を使います (ES2017の構文)

``   `list =['a','b','c']; (async()=>{for(let v of list){awaitsleep(3000)console.log(v)}})()`   ``

これが一番楽かなー。関数型の記述が好きな人にとっては嫌だったりするのかね？

これを非同期関数内部に閉じ込めることで 同期的な map 処理(等)を実現したライブラリを作った方がいるようです。えらい。 https://github.com/toniov/p-iteration

### Solution - Promise.then

async/await から少し離れて Promise で解決する方法を考えてみましょう。

``   `list =['a','b','c']; promise =sleep(3000)list.map(v=>{  promise = promise.then(()=>{console.log(v)returnsleep(3000)})return promise })`   ``

関数の外側に定義した promise 変数を then の返却値で上書きしながら コールバックをつなげていきます。 一応期待通りの出力はされるようです。

少しダサいのが難点。うん、無難に for 使いましょう。

参考

https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Global\_Objects/Promise https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Operators/await https://developer.mozilla.org/ja/docs/Web/JavaScript/Reference/Statements/async\_function https://qiita.com/toniov/items/127267fb64a960e8166e