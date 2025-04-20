## 目的
- Reactを使った開発方法を思い出す
- TypeScriptを使っていない講座にTypeScriptを用いることでTypeScript力を上げる

## 学び
- Material Iconを子コンポーネントにpropsとして渡す時にはAnyしかなさそう
- `console.log(typeof(変数))`で型を確認できる
- Material UIのボタンやアイコンにCSSをつける際に、自分の書いたCSSよりMaterial UIのCSSが優先されることがある
	- これを防ぐためには自分が書いたCSSに`!important`をつける
	- もっといい方法ないのかな
- Material UIのアイコンにCSSをかけるときは、`.MuiSvgIcon-root`というセレクタで指定できる
- **position: sticky**
	- 高さを有するfixed
	- fixedはウィンドウ全体を基準に指定した位置で固定されるのに対して、stickyはstickyが指定された親要素が表示されている時に固定される
		- [positionプロパティを身に着けよう！stickyの仕様と使い方を解説！ : ビジネスとIT活用に役立つ情報（株式会社アーティス）](https://www.asobou.co.jp/blog/web/css-sticky)
- `overflow: scroll;`を指定した時のスクロールバーは、`::-webkit-scrollbar{ display: none;}`で消すことができる

### Firebaseの設定
- `npm install firebase`でライブラリをインストール
- srcディレクトリ直下にfirebase.jsを作成し、Firebaseの初期化のコードを入力する
	- コードはFirebaseから入手可能
- Cloud Firestoreでデータベースを作成する
	- テストモードで開始するのがオススメ
- Firebaseとアプリを連携する
	- `const db = getFirestore(app)`のように書いて初期化したデータベースを引数に入れることでデータベースを連携できる
	- 変数`db`をexportすることでコンポーネント内でデータベースの値を取得できるようになる　
- コンポーネント側でデータベース内のテーブルを指定してデータを取得する
	- `const postData = collection(db, 'posts')`
- データの取得は非同期処理なので`then`を使って取得したデータを取り出す
```jsx
getDocs(postData).then((querySnapshot) => {
    console.log(querySnapshot.docs.map((doc) => doc.data()))
  })
```
![[Pasted image 20230529192614.png]]

### データベースにデータを追加する
- **addDoc**関数を使う