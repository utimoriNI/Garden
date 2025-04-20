## 再レンダリングが起きる条件
- **stateが更新されたコンポーネント**は再レンダリング
- **propsが変更されたコンポーネント**は再レンダリング
- **再レンダリングされたコンポーネント配下の子要素**は再レンダリング

#### 例
![[Pasted image 20230423195113.png | 500]]
- Bのstateが更新された時
	- Bはstateが更新されたコンポーネントなので再レンダリングされる
	- CはBの子要素なので、更新されたstateをpropsとして受け取っていなくても再レンダリングされる

## レンダリング最適化
#### propsとして受けとっているstateが更新されたときだけ再レンダリングする
- コンポーネントをメモ化する
- `コンポーネント=memo(()=>{内容})`

#### 関数を渡す過程で再レンダリングされないようにする
- メモ化したコンポーネントはpropsが変更されない限り再レンダリングされない
- 関数を親から受け取っている場合、親がレンダリングされる度に新しい関数が子に渡されていると判断するため、子の再レンダリングが発生する
- 処理が変わらない関数が、新しい関数として判断されないようにするために**useCallback**を使う
	- `useCallback`は第二引数に配列を取り、その配列の要素が変更されたときのみ新しい関数を生成する
		- 配列を空にすると、新しい関数を生成しなくなる

## 様々なCSSの当て方に触れる
#### Inline Styles
- .jsxファイル内にオブジェクトでstyleを定義する
- HTMLタグのstyle属性にオブジェクトを渡すことで適用する

#### CSS Modules
- `コンポーネント名.modules.scss`というファイルにcssを記述する
	- scssファイルなので通常のcssと同じように記述できる
- jsxファイルからscssファイルをimportして、`import名.クラス名`でHTMLタグにクラスとcssを適用する

#### Styled JSX
- jsxファイル内にstyleタグを使ってcssを記述する
- classnameでクラスをつけることでcssを適用する

#### Styled Components
- スタイルを適用したHTMLタグをコンポーネントとして扱うことができる
```js
export const StyledComponents = () => {

return (
<Container>
	<Title>-Styled Components-</Title>
	<Button>FIGHT</Button>
</Container>
);
};

const Container = styled.div`
	border: solid 2px #392eff;
	border-radius: 20px;
	padding: 8px;
	margin: 8px;
	display: flex;
	justify-content: space-around;
	align-items: center;
`;
```
- `styled.HTMLタグ`でコンポーネントを定義できる

#### Emotion
- 上記のスタイル適用方法が色々使える


## ルーティングの基礎(React Router)
### react-router-domを使ったページ遷移
- react-router-domから`BrouwserRouter`と`Link`をimportする
	- BrouwserRouter:URLによって表示を変えたい領域を囲んで示す
	- Link:aタグのようなもの。`<Link to="/">`と書くことでリンクを変えられる
- Switch,Routeコンポーネントで表示を切り替える
	- Switchタグで囲った中で、Routeタグを使って、URLに応じたコンポーネントを表示する
	- ルートページのRouteタグにはexactを指定する
		- exactを指定すると完全一致した時のみ、そのタグの中身が表示される
		- `/`にexactを指定しないと、`/page1`などのURLでも`/`のページが表示されてしまう

```js
import { BrowserRouter, Link, Switch, Route } from "react-router-dom";

import { Home } from "./Home";
import { Page1 } from "./Page1";
import { Page2 } from "./Page2";
import "./styles.css";

export default function App() {
return (
	<BrowserRouter>
		<div className="App">
			<Link to="/">Home</Link>
			<br />
			<Link to="/page1">Page1</Link>
			<br />
			<Link to="/page2">Page2</Link>
		</div>
		<Switch>
			<Route exact path="/">
			<Home />d
			</Route>
			
			<Route path="/page1">
			<Page1 />
			</Route>
			
			<Route path="/page2">
			<Page2 />
			</Route>
		</Switch>
	</BrowserRouter>
);

}
```

### ルーティングの設定を切り出す
- ルーティングの設定がApp.jsに書かれているとコードが見づらいため、ルート設定用のコンポーネントを用意する
	- Switchの中身をコンポーネントとして切り出す
![[Pasted image 20230430115018.png]]
- ネストされたルーティングは、オブジェクトを用意してそれを展開することで表示できる
![[Pasted image 20230430115110.png]]

### 動的ルーティングを行う
- URLのpathに`/page/:URLパラメータ`と書くことで、URLの一部をパラメータとして扱える
- URLに埋め込まれたパラメータはreact-router-domのHooksである**useParams**によって扱える
![[Pasted image 20230430122148.png]]

### クエリパラメータを扱う
- `useLocation`を使うことで、クエリパラメータを受け取ることができる
![[Pasted image 20230430145914.png]]
- クエリパラメータの中身
![[Pasted image 20230430150026.png]]
- searchは?以下の文字列を取得でき、それを`URLSearchParams`に引数として渡すと、クエリパラメータのメソッドを色々使えるようになる

### stateを渡すページ遷移
- LinkタグのtoプロパティにはLocationと対応するオブジェクトを渡すことができる
	- pathname属性にURLを渡すことでページ遷移が可能
	- state属性に値を指定することで、ページ遷移時に値を渡すことができる
渡す側の記述
![[Pasted image 20230430152752.png]]
受け取る側の記述
![[Pasted image 20230430152856.png]]

### Linkを使わないページ遷移
- `useHistory`を使うことでLinkタグを使わずにページ遷移をすることができる
	- ボタンクリック時などにページ遷移をしたいときに使う
- `history.push("遷移先のURL")`を実行することでページ遷移が行える
- `history.goBack()`を実行するとブラウザの戻るボタンと同じ処理を実行できる


## Atomic Design概要
### Atomic Designとは
- 画面要素を5段階に分け、組み合わせることでUIを実現
- コンポーネント化された要素が画面を構成するという考え方
- React, Vue用の考え方ではなく、モダンJavaScriptと相性がいい

#### 5段階のコンポーネント
- ATOMS
	- それ以上分解できない要素
	- ボタン・アイコン・テキストボックスなど
- MOLECULES
	- Atomの組み合わせで意味を持つデザインパーツ
	- アイコン+メニュー名・プロフィール画像+テキストボックスなど
- ORGANISMS
	- Moleculeの組み合わせで構成される、単体である程度の意味を持つ要素群
	- ツイート入力エリア・サイドメニュー・1つのツイートエリアなど
- TEMPLATES
	- ページのレイアウトを表現する要素で実際のデータは持たない
- PAGES
	- 最終的に表示される1画面

### Atomを作る
- styledコンポーネントを使う時には、ベースとなるコンポーネントを作ってそのstyleを上書きすることでAtomを作ることができる
	- ベースのコンポーネントを上書きしたコンポーネントを作るときには、`styled(BaseComponent)`を使う
	- ![[Pasted image 20230430172139.png]]
		- 上記の場合、BaseButtonコンポーネントに当てたstyleに`background-color`を追加している

## グローバルなstate管理
- reactから提供されている`createContext`を使うことでグローバルなstate管理が可能
- `createContext`を使用して定義したコンポーネント内で宣言したstateはグローバルで呼び出せる
	- `コンポーネント名.Provider`タグ内で、value属性を定義すると、そのコンポーネントタグ内はvalueに定義されたstateを呼び出せる
	- ![[Pasted image 20230501220528.png]]
- contextを受け取る側の操作
	- useContextの引数にexportしたcontextを取る
	- `const context = useContext(UserContext);`

## TypeScriptとは
- Microsoftが開発したオープンソースの言語
- JavaScriptで型を扱える
- 安全でバグが少ない

### React×TypeScript
- 拡張子を`.tsx`にすることでTypeScriptを使ったReactコンポーネントを作れる

#### TypeScript 型一覧
![[Pasted image 20230504102454.png]]

### tsconfigをいじる
- tsconfig内の`strict`はTypeScriptを書く時の規則を採用するかどうかを決める
	- trueは規則を採用し、falseは規則を採用しない
	- trueの時は、型が宣言されていない変数に対してエラーを吐いてくれたりする
	- 新規でプロジェクトを立ち上げる際にはtrueで進めるのが普通だが、既存のJavaScriptのコードをTypeSccriptに書き換えるときにはfalseで進める
- TypeScriptの規則がカスタマイズできる
	- Any型であることが明示されていない変数にエラーを吐かせないようにするには`"noImplicitAny": false`を追加するなど

### データ型を自分で定義する
- `type`を用いることで型に対して別名をつけることができる
	- オブジェクトの要素のキーとその値の型を定義することで、自分で型を定義したオブジェクトを作ることができる

#### state管理に型を用いる
![[Pasted image 20230504135854.png]]
- `useState`に対して型を指定することで、stateやstateのセット関数に渡す値の型を指定できる

##### propsに型を定義する
![[Pasted image 20230504140033.png]]
- propsを受け取る際に型を指定しておくと、どの値を親から渡されるべきかを指定できる
- この時、指定したキーが親から渡されていないとエラーを吐く
	- `completed?`のようにキーの後に?をつけることで、そのpropsは任意で受け取ることができる

### 型を効率的に管理する
- propsを渡す側と受け取る側で似たような型を定義するのは管理が煩雑になる
	- 型定義用のファイルを用意して、そこで定義したものを他のファイルからインポートすることで型を流用する

##### propsのプロパティの一部だけを取り出す
- 渡す側ではidというプロパティを使うが、受け取る側ではdというプロパティを使わない場合
	- TypeScrriptのPickまたはOmitという機能を使う
		- Pickではpropsから一部のプロパティを取り出して型として定義することができる
		- Omitではpropの一部のプロパティを取り除いた型を定義できる
![[Pasted image 20230504142810.png]]
- userId,title,completedの3つのプロパティを型として定義する
![[Pasted image 20230504143204.png]]
- id以外のプロパティを型として定義する
	- 二枚とも内容は一緒

### オプショナルチェインニングでnull安全なコードを書く
- 一部のプロパティをオプションとした時、プロパティを渡さなかったときにはそのプロパティに対する処理がエラーとなる
	- それを防ぐためにオプショナルチェインニングを使う
![[Pasted image 20230504162654.png]]
- 上記のように?を使うと、そのプロパティの有無によってその先の処理を読むかどうかを決めてくれる

## Chakra UIについて
### 基本的な考え方
- 様々なタグが用意されており、タグごとにFlexレイアウト(Flexタグ)やボタン機能(Buttonタグ)が事前に準備されている
	- レイアウトに関するタグはasプロパティを設定することで、そのレイアウトがどのHTMLタグで展開されるかを指定する
		- `<Flex as='nav'>`と書くと、flexレイアウトになったnavタグが使える

##### 色について
- `色名.数字`という書き方がメイン
	- 数字が大きいと色が濃くなる

### 色々なタグ
- `Heading`:見出し。デフォルトではh2が指定されている
- `Box`:divみたいなやつ
- `Flex`:display: flexがかかっているdiv
	- alignやjustyfy属性を指定してレイアウトをいじれる
- `Stack`囲った要素を縦に等間隔に並べる

#### モーダルの作り方
- `Modal`タグで囲い、`ModalOverlay`を最初に書く
- `ModalContent`の中に書いた内容がモーダルの中に表示される
- モーダル内の見出しは`ModalHeader`
- 閉じるボタンは`ModalCloseButton`タグで置ける
- `ModalBody`でモーダル内のコンテンツを書こう
- モーダルの出現アニメーションは`Modal`タグの`motionPreset`で変更できる