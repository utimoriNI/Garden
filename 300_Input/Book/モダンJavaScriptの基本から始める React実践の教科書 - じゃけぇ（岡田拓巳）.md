---
tags:
  - 📚Book
title: モダンJavaScriptの基本から始める　React実践の教科書
author:
  - じゃけぇ（岡田拓巳）
publisher: SBクリエイティブ
publish: 2021-09-16
total: 272
isbn: 481561072X 9784815610722
cover: http://books.google.com/books/content?id=mK9CEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api
created: 2023-04-07 20:29:46
updated: 2023-04-07 20:29:46
status: 読了
Status: 読了
---

![cover|150](http://books.google.com/books/content?id=mK9CEAAAQBAJ&printsec=frontcover&img=1&zoom=1&edge=curl&source=gbs_api)

# モダンJavaScriptの基本から始める　React実践の教科書

## モダンJavaScriptの機能に触れる
### const,  letでの変数宣言
- varだと上書き可能であるため、意図しない上書きが起こる可能性がある
- const, letがES2015で追加された

##### letでの変数宣言
- letで再宣言は不可能
- 再代入は可能

##### constでの変数宣言
- constは再宣言も上書きも不可能
- const=定数という意味

##### constで定義した変数を変更できる例
- オブジェクト型と呼ばれる、オブジェクト・配列・関数などは変更できる

##### React開発で使用する変数宣言
- Reactでは**constがほとんど**
- 処理の中で値を上書きする変数はletを使う

### テンプレート文字列
- 文字列中に変数を展開するやつ
- `'皆さん${sayHello()}。今日から${month +1}月です。'`

### アロー関数() => {}
- ES2015で追加された関数の記法
- 従来の関数の書き方
```js
function(引数){
	return value;
};
```
- アロー関数での書き方
```js
(引数) => {
	return value;
};
```
- アロー関数の省略記法
	- 引数が1つの場合はカッコを省略できる
	- 処理を単一行で返却する時は波カッコとreturnを省略できる
```js
value => { return value; };

(num1, num2) => num1 + num2;
```
- 返却値が複数行に及ぶ場合には、`()`で囲むことで単一行のようにまとめて返却できる
```js
(val1, val2) => (
	{
		name: val1,
		age: val2,
	}
)
```

### 分割代入{ }, [ ]
- オブジェクトや配列から値を代入する方法
```js
const myProfile = {
	name: "田中",
	age: 24
};

const { name, age } = myProfile;
```
- `{}`を変数宣言部に使用することで、オブジェクトから一致するプロパティを取り出せる
- 順番が違っていたり、一部だけ取り出しても大丈夫
- 抽出するプロパティに別名をつけることもできる
```js
const myProfile = {
	name: "田中",
	age: 24
};

const { name: newName, age: newAge } = myProfile;
const message = `私の名前は${newName}です。`
```

##### 配列の分割代入
- オブジェクトと同じように配列に対しても分割代入を使える
	- 配列に格納されている順に任意の変数名を設定できる
```js
const = ["田中", 24];

// 配列の分割代入
const[name, age] = myProfile;
const message = `私の名前は${name}です。`
```

### スプレッド構文
- 配列やオブジェクトの任意の範囲を展開する方法
```js
const arr1 = [1,2];
console.log(...arr1); // 1 2
```

##### 要素をまとめるためにも使える
```js
const arr1 = [1,2,3,4,5];

const [num1, num2, ...arr3] = arr2;

console.log(num1); //1
console.log(num2); //2
console.log(arr3); //[3,4,5]
```

##### 要素のコピー・結合
```js
const arr4 = [10,20];
const arr5 = [30,40];

// スプレッド構文でコピー
const arr6 = [...arr4]; //[10,20]

// スプレッド構文で結合
const arr7 = [...arr4, ...arr5]; //[10,20,30,40]
```

##### オブジェクトの結合
```js
const obj4 = {val1: 10, val2: 20};
const obj5 = {val2: 30, val3: 40};

// スプレッド構文で結合
const obj7 = {...obj4, ...obj5}; // {val1: 10, val2: 20, val3: 30, val4: 40}
```

##### =でコピーしてはいけない理由
- オブジェクト型の変数を≠でコピーすると、アドレスも引き継がれてしまう
	- =でコピーした後の配列に変更を加えると、コピー元の配列にも影響を与えてしまう
- スプレッド構文でコピーすれば新しい配列を生成してくれる


### オブジェクトの省略記法
- オブジェクトを記述する時に、「オブジェクトのプロパティ名」と「設定する変数名」が同じ場合は省略できる
```js
const name = "田中";
const age = 24;

// 省略しない記法
const user = {
	name: name,
	age: age,
};

//省略する記法
const user = {
	name,
	age,
}
```

### ESLintの特長
- ESLint = 静的解析ツール
- Prettierとセットで導入されることが多い
- チェックできる内容
	- varでの変数宣言
	- 使っていない変数
	- 残っている`console.log`
	- 意味のない式

### map, filter
- 繰り返しを`for`より便利に書く方法
	- 従来は`for(初期値;条件;増分)`で配列のindexに値を入れることで、繰り返し処理をしていた
#### map関数の使い方
- map関数は、配列を順番に処理して処理した結果を配列と知れ受け取ることができる
```js
const nameArr = ["田中", "鈴木", "佐藤"];

const nameAr2 = nameArr.map((name) => {
	return name;
})
```
- 配列の要素を`name`として受け取り、返却する要素を関数内でreturnする
- 返り値を受け取る必要がない時は、新しい配列を定義せずとも使える
```js
nameArr.map((name) => console.log(name));
```

#### filter関数の使い方
- filter関数は、map関数とほとんど同じ使い方で、returnの後に条件式を書くことで条件に一致したもののみが返却される
```js
// fileter関数で奇数のみを取り出す
const numArr = [1, 2, 3, 4, 5];

const newNumArr = numArr.filter((num) => {
	return num % 2 === 1;
});
```

#### map関数でindexを使用する
- ポイントとなるのは`map()`内で実行する関数の引数
```js
const nameArr = ["田中", "鈴木", "佐藤"];

nameArr.map((name,index) => console.log(`${index + 1}番目は${name}です`));
```
- map内の関数は第二引数を書くことができて、書いた場合はその引数に0から順にindexが格納される



## Reactの基本
### JSX記法
- Reactで使われる記法
	- jsファイルの中で、HTMLのようなタグを書ける
- Reactでは`<App />`のように関数名をHTMLタグのように書くことで、コンポーネントとして扱える
- 関数の返り値としてHTMLのタグが記述できて、コンポーネントとして扱うことで画面を構成する
```js
const App = () => {
return <h1>こんにちは！</h1>;
};

ReactDOM.render(<App />, document.getElementById("root"));
```
- ReavtDOMってなんだ？
- return以降は1つのタグで囲われている必要がある
```js
// エラーが発生する例
const App = () => {
	return (
		<h1>こんにちは！</h1>;
		<p>こんにちは！</p>;
	)
};
```
- 不要なDOMを生成したくない時は、`Ftagment`を使用する
```js
const App = () => {
	return (
		<Fragment>
			<h1>こんにちは！</h1>;
			<p>こんにちは！</p>;
		</Fragment>
	)
};
```

##### 基本的な記法
```js
<div id='root'></div>
<script type="text/babel">
fuction RandomNumber(){
	//spanタグに0から10の乱数を生成する
	return (
		<span>{
			Math.floor(Math.random() * 10) // タグ内にJSを書く時は中カッコで囲む
		}</span>
	)
}
ReactDOM.render(
	<RandomNumber />,
	document.getElementById('root') // rootのdivに、RandomNumberをレンダリングする
)

</script>
```


### コンポーネントの使い方
- 関数コンポーネントの方が主流で、クラスコンポーネントはあまり使われない

#### コンポーネントの分割
- 他のファイルで関数コンポーネントを使えるようにするときは、宣言時にexportする
	- `export const App = () => {}`
- exportされたものはimportすることで他のファイルで使える

#### コンポーネントファイルの拡張子
- .jsという拡張子で動作がするが、コンポーネント用の**jsx**という拡張子も用意されている
- どちらでも動作するが、コンポーネントファイルはjsxにする方がオススメ

### イベントやスタイルの扱い方
#### イベントの扱い方

##### ボタンにクリックイベントを入れる
- JSXで書いているreturn以降はHTMLのようなタグの中で、`{}`を囲むとJavaScriptを記述できる
```js
const App = () => {
	return (
		<Fragment>
		{console.log("TEST")} //JavaScriptの処理
			<h1>こんにちは！</h1>;
			<p>こんにちは！</p>;
		</Fragment>
	)
};
```

- 上記を踏まえてクリック処理を実装する
```js
export const App = () => {
	// クリック時の関数
	const onClickButton = () => {
		alert();
	};
	
	return (
		return (
		<Fragment>
			<h1>こんにちは！</h1>;
			<p>こんにちは！</p>;
			<button onClick={onClickButton}>ボタン</button>
		</Fragment>
	);
};
```

#### スタイルの扱い方
- Reactでもタグに**style属性**を記述巣つことでスタイルが適用できる
- 注意点として、CSSの各要素はJavaScriptのオブジェクトとして記述する
```js
return (
		<Fragment>
			<h1 stle={{ color: "red" }}>こんにちは！</h1>;
			<p>こんにちは！</p>;
		</Fragment>
	)
```

### Props
#### Propsとは
- コンポーネントに渡す引数のようなもの
- コンポーネントは受け取ったPropsに応じて表示するスタイルや内容を変化させる

##### 色とテキストをPropsとして受け取って、色付きの文字を返すコンポーネントを作る
- ColorMessageという名前のコンポーネントとする
- Propsを使うためにはPropsを渡すコンポーネントと、受け取るコンポーネントの両方に変更が必要
	- 渡す方はタグの中で**任意の名称でPropsを渡す**
	- `<ColoredMessage color="bluse" message="お元気ですか？" />`
	- 受け取る方は関数の引数として**Propsをオブジェクトとして受け取る**
	```js
export const ColoredMessage = (props) => {
	const contentStyle = {
		color: props.color,
		fontSize: "20px"
	};
```

### children
- Propsではタグ内で任意のキーを設定したが、特別なキーとして**children**がある
	- タグの中のテキストを、任意のキーを設定することなく`props.children`として渡すことができる
```js
<ColoredMessage color="pink">元気です</ColoredMessage>

export const ColoredMessage = (props) => {
const contentStyle = {
	color: props.color,
	fontSize: "20px"
};

return <p style={contentStyle}>{props.children}</p>;
};
```
- また、childrenはタグで囲んだ要素を丸ごと渡せる
```js
<SomeComponent>
	<div>
		<p>テキスト</p>
		<span>テキスト</span>
	</div>
</SomeComponent>
```

### State(useState)
- Reactでは、画面上のデータや、可変の状態を全てStateとして管理する

#### Stateとは
- コンポーネントの状態を表す
	- 状態の例
		- エラーがあるか
		- モーダルウィンドウが開いているか
		- ボタンを押せるか
		- テキストボックスに何を入力したか

#### useState
- 現在主流となっている関数コンポーネントでは、React Hooksと称される機能の中の**useState**という関数でstateを扱う
	- useStateはインポートする必要がある
- useState関数の返り値は配列の形で**1つ目にState変数、2つ目にそのStateを更新するための関数**が設定される
- `const [num, setNum] = useState()`
	- この場合numが状態を持った変数、setNumが更新する関数
	- useStateが関数だから`()`をつけて関数を実行する
	- 関数名は「set+変数名」にするのが一般的
	- `num`に初期値を設定したいときにはuseStateの引数に設定する
		- `const [num, setNum] = useState(0)`

### 再レンダリングと副作用(useEffect)
#### 再レンダリング
- カウントアップ用のボタンをクリックすると、画面をリロードしていないのに画面の表示が変わる
	- これは**コンポーネントが再レンダリングされているから**
	- 参考:![[Pasted image 20230408171818.png]]
- Stateが更新された時に、関数コンポーネントは再び頭から処理が実行される
	- この**変更を検知してコンポーネントを再処理する**ことを再レンダリングする

#### 副作用とuseEffect
- useEffectはコンポーネントの副作用を制御する機能
	- Reactからimportして使う
- `useEffect(実行する関数, [依存する値]);`
- useEffectの役割は、**ある値が変わった時に限り、ある処理を実行する**
	- 例:numというStateの値が変わった時にアラートを表示するなど
```js
export const App = () => {

	useEffect(() => {
		alert();
	}, [num])

}
```
- 第二引数は必ず配列で指定する
	- 複数指定する時は`[num, num2]`のように書く
- useEffectは依存配列の値が変わった時に加え、コンポーネントのマウント時にも必ず実行される
	- useEffectの第二引数に空配列を設定すると、「コンポーネントを表示した初回のみ実行する処理」を記述できる
- この機能がある理由は、**再レンダリングの度に処理が実行されるのを防ぎ、特定の値の変更時にのみ処理を実行するため**



## ReactとCSS
- JavaScriptを使ってCSSを割り当てる方法はいくつか存在する
### Inline Styles
- JavaScriptのオブジェクトでCSSのプロパティと値を指定し、タグのstyleとして設定する方法
- 実際に開発で使うには管理が大変
	- `<p style={{ color: "blue" }}>`
- 注意点
	- プロパティ名はキャメルケースにし、値は文字列or数値

### CSS Modules
- 従来のWeb開発と同様に.cssや.scssファイルを使用する
- Reactの場合は、コンポーネントごとにcssファイルを用意する
	- この時、ファイル名を「ファイル名.module.scss」にする必要がある
		- .cssでも可
- 任意の名前でCSSをimportし、className属性に定義したクラスを指定することでスタイルを適用できる
```js
import classes from "./CssModules.module.scss";

export const CssModules = () => {
	return (
		<div className={classes.container}>
			<p className={classes.title}>CSS Modulesです</p>
			<button className={classes.button}>ボタン</button>
		</div>
	);
};
```

### Styled JSX
- **Next.js**に標準で組み込まれているライブラリ
- CSS in JSと呼ばれる、コンポーネントファイルにCSSを記述していくライブラリ
- 使用方法
```js
<style jsx>{`
	/* ここにCSSを書く */	
`}
</style>
```
- styleタグでHTMLファイル内にcssを書くのと同じ感じ


### styled components
- **スタイルを当てたコンポーネントを定義する**ライブラリ
- Styled JSXと同じように、CSS in JSと呼ばれるコンポーネントファイルにCSSの記述をしていく

#### styled componentsの使用
- classNameにクラスを指定するのではなく、**スタイルを適用したコンポーネントを定義する**
- 例えばpaddingを設定したdivタグを使いたい場合は以下のように書く
```js
import styled from "styled-components";

const StyledDiv = styled.div`
	padding: "8px";
`

<StyledDiv>
	<p>このように使える</p>
</StyledDiv>
```
- styled.の後にHTMLい存在するタグを指定することで、そのタグにスタイルを適用できる
- StyledDivのような大文字で始まる名前を付けることができる
	- 先頭にSを大文字で入れると、styled componentsで作成したコンポーネントかどうかを判断できる
- SCSS記法がそのまま使える

### Emotion
- Inline Styles, Styled JSX, styled componentsと似たような書き方があり、幅広い使い方が用意されている

#### Emotionの使用
- Emotionを使うには以下の記述が必要
```js
/** @jsxImportSource  @emotion/react */
import {jsx} from "@emotion/react";
```

##### Styled JSXのようにコンポーネントファイルにCSSを書く
- Styled JSXとの違いはEmotionに用意されているCSSを用いること
```js
const containerStyle = css`
	border: solid 1px #aaa;
	border-radius: 20px;
	padding: 8px;
	margin: 8px;
	display: flex;
	justify-content: space-around;
	align-items: center;
`;

return (
<>
	<div css={containerStyle}>
		<p className="title">Styled JSX</p>
		<button className="button">ボタン</button>
	</div>
</>
);
```

##### Inline StylesのようにJavaScriptのオブジェクトでCSSを書く
```js
const titleStyle = css({
	margin: 0,
	color: "#aaa"
});

<button className="button">ボタン</button>
```

##### styled-componentsの書き方
```js
const SButton = styled.button`
background-color: #ddd;
border: none;
padding: 8px;
border-radius: 8px;
&:hover {
background-color: #aaa;
color: #fff;
cursor: pointer;
}
`;

<SButton>ボタン</SButton>
```



## 再レンダリングの仕組みと最適化
### 再レンダリングが起きる条件

#### 再レンダリングが起きる3つのパターン
- 再レンダリングが起きるのは以下の3つのパターン
	- 1. Stateが更新されたコンポーネント
	- 2. Propsが変更されたコンポーネント
	- 3. 再レンダリングされたコンポーネント配下のコンポーネント全て
- 3のケースでの再レンダリングは表示が変更されないのに再レンダリングが発生する
	- そのような無駄な再レンダリングはパフォーマンスの低下の原因になる


### レンダリング最適化1(memo)
#### React.memo
- Reactにおいて、コンポーネント・変数・関数などの再レンダリング時の制御をするにはメモ化を行う
	- メモ化とは、前回の処理結果を保持しておくことで処理を高速化する技術
	- 必要な時のみ再計算を実行する
- コンポーネントをメモ化する方法
	- コンポーネント関数全体をカッコで囲むだけで使用できる
	- `const Component = memo(() => {});`
	- これによって**Propsに変更がない限り再レンダリングされない**ようになる
		- 1つ上の親コンポーネントがメモ化されていたらその下はメモ化しなくても再レンダリングされない？

### レンダリング最適化2(useCallback)
#### 関数のメモ化
- 親のstateを更新するような関数を子から実行した場合、stateが変更される親とその関数を実行した子が再レンダリングされてしまう

#### React.useCallback
- **関数の再生成**によって関数をpropsとして渡す時にメモ化されたコンポーネントが再レンダリングされてしまう
- コンポーネントが再レンダリングされる際、定義されている関数は再生成されたと判断される
	- そのため、その関数をpropsとして受け取る子コンポーネントは、propsが変化したと判断し、子コンポーネントの再レンダリングが発生する
- 上記のような事象を回避するために、関数のメモ化を行う
- **useCallback**を使用し、第一引数に関数、第二引数に依存配列をとる(useEffectと一緒)
```js
const onClickButton = useCallback(() => {
	alert('アラート')
}, []);
```
- このコードの場合は依存配列が空なので、最初に作成された関数が使いまわされる
	- 依存配列に値を設定した場合は、その値が変更された時に関数が再生成される


## グローバルなState管理
### グローバルなState管理が必要な理由
- ある程度の規模のアプリケーションになると、ルートコンポーネントから最下層のコンポーネントまで5階層以上になることがある
	- この時、一階層ずつPropsで値の受け渡しをするのは煩雑となる
	- また、1つのコンポーネントが持つPropsが肥大化する
	- Propsが変更されたら再レンダリングされるため、State更新時に多くのコンポーネントが再レンダリングされてしまう
	- この問題を解決するために、グローバルなState管理によってどのコンポーネントからでも値にアクセスできるようにする

### ContextでのState管理
- グローバルなState管理をするライブラリはいくつかあるがReact標準のContextという機能でも実現することができる

#### ContextでのグローバルStateの基本的な使い方
- ContextでのグローバルStateの使用方法は大きく分けて下記の3ステップ
	- 1. React.createContextでContextの器を作成する
	- 2. 作成したContextのProviderでグローバルStateを扱いたいコンポーネントを囲む
	- 3. Stateを参照したいコンポーネントでReact.useContextを使う
- ここの説明はわかりにくかった

### グローバルStateを扱うその他の方法
- Redux
- Recoil
- Apllo Client


## ReactとTypeScript
- フロントエンド開発におけるTypeScriptの利用は、保守性の向上や開発効率のアップなどのメリットがある

### TypeScriptとは
- Microsoftが開発しているオープンソース言語
- **JavaScriptで型(Type)を扱えるようにしたもの**

#### 基本的な型の種類
- 型は指定したい変数の後に`:(型名)`というように記述する
```js
let str: string
let num: number
let bool: boolean
let arr1: Array<number>
let arr2: numebr[]
let null1: null;
let undefined1: undefined;
let any1: any; // どんな値でも入れられるany型。なるべく使わない
```

##### 関数の型指定
- 関数には、「引数の型」と「返り値の型」を指定できる
- 括弧の中に引数の型を、括弧の外に返り値の型を指定する
```js
const funcA = (num: number):void => {
 //関数の処理
};
```
- オブジェクトに対しては、各プロパティごとに型を指定できる
```js
const obj: {str:string, num:number} = {
	str: "A",
	num: 10,
}
```

#### 複合的な型
- intersectionは複数の型を合体して、新たな型を定義できる
	- &で複数の型を指定して使用する
```js
//型 & 型で指定
const obj:{str:string} & {num:number} = {
str: "A",
num: 10,
}
```

- 同じ型定義のプロパティが存在する場合はマージされる
```js
type TypeA = {
	str: string;
	num: number;
}

type TypeB = {
	str: string;
	bool: boolean;
}

type TypeC = TypeA & TypeB;
const obj: TypeC = {
	str: "A",
	num: 10,
	bool: false,
}
```

#### Generics
- Genericsは型の定義を使用時に動的に変更できる機能
```js
type CustomType<T> = {
	val: T;
}

const strObj: CustomType<string> = {val: "A"}
```
- `<T>`の部分がGenerics特有の書き方で、型の後に`<T>`のように型の変数のようなものを定義することで、プロパティvalの値を動的に変更できる
- 使用する側が任意に型を指定できるため、ライブラリの型定義ではよく使われる

#### 設定ファイル(tsconfig)
- TypeScriptでは、プロジェクトごとに細かい設定をカスタマイズできる
- この設定を記述するためのファイルがtsconfig.json
- コンパイルする際のJavaScriptのバージョンを指定したりReact開発で必要な設定を書いたりする

### 型定義の管理方法
- 同じ型の定義を複数個所で使う場合、一つの型を色んなコンポーネントで使いまわせる
- TypeScriptファイル(.ts)に定義し、それをexport・importすることで型を他のファイルで使える
