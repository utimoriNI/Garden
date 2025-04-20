---
created: 2024-05-17 20:29
tags:
  - Knowledge
  - 🎁Topic/Tech
---
---
## Jotaiとは
状態管理を行うためのライブラリで、Recoilと同じくボトムアップアプローチ型である。
軽量でシンプルに開発ができ学習コストが低いことが特徴。
ルールが少ない分、状態管理の方法がカオスになることがある。
TypeScriptで開発されている。

>[!note] Recoilは開発が停止したらしい
> Recoilはmeta社が開発したライブラリだが、主要な開発メンバーが一斉レイオフで解雇されたため、開発が停止してしまった。
> Recoilが注目されてるみたいな話はたまに目にしていたためびっくり。
>
### 実際の使い方
- とりあえずatomとuseAtomさえ使えば状態管理ができる
- atom定義用のファイルにグローバルのatom定義して、それを各コンポーネントで取得する方法で使えば良さそう
- storeやproviderは規模が大きくなって上記の運用が大変になったりパフォーマンスの改善が必要になったりしたら使うものな気がする

## Jotaiの使い方
### Jotaiの4つの主要API

#### 1. atom
状態管理のための最小単位で1つのStateに対応する。
atomを宣言する時は`atom<型>(初期値)`のように宣言する。
宣言されたatomはグローバルのStateとして扱うことができる。

```ts
import { atom } from 'jotai'

const priceAtom = atom(10);
const messageAtom = atom('hello');
const productAtom = atom({ id: 12, name: 'good stuff' });
```

**derived atom**
> derive = 引き出す、由来を辿る、派生する

Jotai特有の概念で、atomからatomを生成する仕組みがある。
既存のatomを参照して新しいatomを定義することができる。

`atom()`は3つの引数を取ることができる。
`atom(初期値, read関数, write関数)`
初期値を書かずにread関数やwrite関数を持たせたatomを定義すると、他のatomを参照して値を返すatom(derived atom)を定義できる。


```ts
const priceAtom = atom(10);

// priceAtomの値段を2倍にして読み取る
const doublePriceAtom = atom((get) => get(priceAtom) * 2)

// priceAtomから引数で受け取ったdiscountを減算した値を書き込む
const discountPriceAtom = atom(
  null, // wirteOnlyなのでnullに設定
  (get, set, discount) => {
    set(priceAtom, get(priceAtom) - discount) //処理後の値をpriceAtomにセットする
  },
)
// praiceAtomを2倍にして読み取り、newPriceの1/2を書き込む
const readWriteAtom = atom(
  (get) => get(priceAtom) * 2,
  (get, set, newPrice) => {
    set(priceAtom, newPrice / 2) // readWriteAtomからpriceAtomの値を変更している
  },
)

```

### 2. useAtom
atomの状態を取得して、状態管理を行う変数にセットする仕組み。
`const [value, setValue] = useAtom(atom);`と書いた場合は、atomのread関数によって`value`に値がセットされる。
`setValue`は関数であり、使用するとatomのwrite関数によって値が更新される。

⚠`useAtom`で状態を変数にセットする際に、変数名はatomの名前と異なる名前を使用する必要がある。
```ts
const priceAtom = atom(100)
const addingPriceAtom = atom(
  (get) => get(priceAtom) / 2,
  (get, set, num: number) => {
    set(priceAtom, get(priceAtom) * num)
  },
)
// valueには50がセットされ、setValue(x)でvalueの値をx倍する
const [value, setValue] = useAtom(addingPriceAtom)

```


### 3. Store
Storeは共有するデータの保管場所を定義するもの。
`createStore`を使用して空のストアを作成する。
Storeは3つのメソッドを持ち、後述するProviderを併用する。
- `get`メソッド:atomの値を取得する
- `set`メソッド:atomの初期値をセットする
- `sub`メソッド:atomの値を更新する

### 4. Provider
`Provider`を使用すると、`Provider`の中にあるコンポーネントだけが使えるatomを提供できる。
また、`Provider`の中にあるコンポーネントはグローバルで宣言されたatomにアクセスできない。

スコープが違う同名のatomを定義できるみたいなもの？
あまり使い道が分からない。
1つのAtomを複数個所で別々のatomとして使う時に使えるらしい。
[【Jotai】Reactの状態管理はコレで決まり！！！  - Qiita](https://qiita.com/al_tarte/items/bfaefc34e9b0be91c72a#provider-%E3%81%A8-store)
> 前章までで **Jotai** の基本的な使い方を見てきましたが、**Provider** は一度も登場していません。それは、1つのAtomを複数箇所で別々に扱う必要がなかったからです。  
例えば、コンポーネント毎にカウンターを独立して持たせたい場合などにProviderが必要になってきます。


```ts
import './App.css'
import { Provider, atom, createStore, useAtom } from 'jotai'

// グローバルステート
const countAtom = atom(0)
// storeを宣言
const myStore = createStore()
// storeの中にcountAtomを初期値100としてセットする
myStore.set(countAtom, 100)

// ボタンを押すと+1されるカウンター
const Counter = () => {
  const [count,setCount] = useAtom(countAtom);
  return (
  <>
    <div>{count}</div>
    <button onClick={ () => setCount((p) => p+1) }>
      +1するボタン
    </button>
  </>
  )
}

const App = () => (
  <>
    <Provider store={myStore}>
      <h1>Proverで切り分けした空間</h1>
      <Counter />
      <Counter />               
    </Provider>
    
    <h1>グローバルステート空間</h1>
    <Counter />
  </>
)

export default App

```


### 非同期な処理をするatom
必要になったら調べる


[[2024-05-17]]
[初学者でも分かるようにJotaiを丁寧に解説していく - Qiita](https://qiita.com/moritakusan/items/9a5e8c315b2565a02848)
[React状態管理ライブラリ Jotai の始め方](https://zenn.dev/jotaifriends/articles/7a5bd147d34ec2)
[【Jotai】Reactの状態管理はコレで決まり！！！ - Qiita](https://qiita.com/al_tarte/items/bfaefc34e9b0be91c72a#provider-%E3%81%A8-store)