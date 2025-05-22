---
created: 2023-06-18 10:17
tags:
  - Knowledge
  - 🎁Topic/Tech
---
---

## TypeScriptにおける型宣言
### 変数宣言
- **基本構文**
	- `const(or let) 変数名: 型名 = 値`
	- `例： const username: string = "Ken"`
- 明示的な型宣言を行わなくても、代入される値から型を推論してくれる
	- これを型推論と呼ぶ
	- `const username = "Ken"`と書いても、文字列が代入されていることから`username`がstring型であることを推論してくれる
	- 基本的に型推論を使ってよい

### 型宣言の基本的な方法
```ts
const str: string = "hello" // 文字列
const num: number = 123 // 数字
const bool: boolean = true // 真偽値

// 配列
// 要素の型が統一されている場合
const arr: Array<boolean> = [true, false, false] // 真偽値の配列（boolean[]と書くことも可能）
// 要素の型が統一されていない場合
const arr2: Array<string | number> = [0, 1, "hello"] // 文字列と数字で構成された配列（string | number[]と書くことも可能）
  
// オブジェクト
// string型のfirstとstring型のlastというキーで構成されたオブジェクトをNAME型として定義する
// キーの後に'?'をつけると、そのキーの値の存在が任意となる
interface NAME {
  first: string
  last: string | null // string型またはnull型の値を取る
  age?: number // ageは存在しなくてもよいという意味
}
// NAME型のオブジェクトを作成する
const obj: NAME = {first: "Yamada", last: null}

// 関数
// 引数の型の指定は必須、返り値の型の指定は任意
const func1 = (x: number, y:number):number => {
  return x + y
```

- オブジェクトの型宣言は、`interface`を使う方法と`type`を使う方法がある
	- 違いは要調査
	- [[オブジェクトの型宣言におけるinterfaceとtypeの違いを調べる]]

### Intersection Types
- 複数の型を結合する方法のこと
- `type 型名 = 結合する型1 & 結合する型2`と書く
```ts
//Intersection Types
type PROFILE = {
  age: number
  city: string
}

type LOGIN = {
  username: string
  password: string
}

// PROFILE型とLOGIN型を結合したUSER型を定義する
type USER = PROFILE & LOGIN
  
const userA: USER = {
  age: 30,
  city: "Tokyo",
  username: "xxx",
  password: "yyy"
}
```

### Union Types
- 変数に代入できる値の型を複数割り当てるための方法のこと
-  `変数名: 型1 | 型2`と書く
```ts
//Unioin Types
let value: boolean | number
value = true //OK
value = 123 //OK
value = "hello" //ERROR

// 配列におけるUnion Types
let arrayUni: (number | string)[]
arrayUni = [0, 1, "hello"] //OK
arrayUni = [0, 1, "hello", true] //ERROR
```

### Literal Types
- リテラル型：プリミティブ型の特定の値だけを代入可能にする型
	- プリミティブ型：オブジェクトではなく、メソッドを持たないデータのこと
		- `hello`, `123`など
		- プリミティブ型の値に対してメソッドを使用できるのは、オブジェクトとしてラップされているから
		- ![[りあクト！TypeScriptで始めるつらくないReact開発1#2-3-2.プリミティブ値のリテラルとラッパーオブジェクト]]
```ts
//Literal Types
let company: "Facebook" | "Google" | "Amazon"
company = "Facebook" //OK
company = "Microsoft" //ERROR

let memory: 256 | 512
memory = 256 //OK
memory = 128 //ERROR
```

### typeof
- 宣言済みの変数の型を取得するための方法
	- 宣言済みの変数の型を他の変数に適用する時に使う
```ts
//typeof
let msg: string = "hello"
let msg2: typeof msg //msg2はstring型になる
msg2 = "Hi" //OK
msg2 = 123 //ERROR

let animal = {cat: "small cat"}
let newAnimal: typeof animal = {cat: "big cat"} //OK string型の値を持つcatというキーで構成されたオブジェクトとなる
newAnimal = {dog: "big dog"} // ERROR
```
- 実務では取得してきたJSONデータの型を使いまわすために使う
	- 複雑なJSONデータだと型の宣言が大変なため

### keyof
- 既に宣言されたオブジェクトの型のキーのみを受け付ける変数を作るための方法
```ts
let key: keyof KEYS //keyは'primary'か'secondary'の文字列しか受付ない
key = "primary" //OK
key = "tertiary" //ERROR
```

### keyof + typeof
- `keyof`と`typeof`を併用することで、既に定義されたオブジェクトのキーを文字列化したもののみを受け付ける変数を作ることができる
```ts
let keySports: keyof typeof SPROTS //変数keySportsは'soccer'か'baseball'の文字列しか受け付けない
keySports = "soccer" //OK
keySports = "baseball" //OK
keySports = "basketball" //ERROR
```
- `keyof`のみとの違い
	- `keyof`：定義された型を基に受け付ける値を決める
	- `keyof+typeof`：定義されたオブジェクトを基に受け付ける値を決める

### enum(列挙型)
- 自動で連番をつけてくれる機能
	- 列挙した項目に対して番号を対応させる
```ts
//enum
// windowsは0、Macは1、Linuxは2の数値と対応する
enum OS {
  Windows,
  Mac,
  Linux
}
```
- 上記ではWindowsが0、Macが1、Linucが2の数値と対応する
- 実際にこの連番を使ってオブジェクトを定義するには以下のように書く
```ts
//enum

// windowsは0、Macは1、Linuxは2の数値と対応する

enum OS {
  Windows,
  Mac,
  Linux
}
interface PC {
  id: number
  OSType: OS
}

const PC1: PC = {
  id: 1,
  OSType: OS.Windows,
}

const PC2: PC = {
  id: 1,
  OSType: OS.Mac,
}
```
- enumを使うことで、定数をひとまとめにしてそこから定数を呼び出せる
	- バグを減らしたり、コーディングがしやすくなる
- **enumは余り使わないほうがいいらしい**
	- enumはTypeScriptが独自に実装した機能
	- JavaScriptにはない機能であるため、使用するとあまり良くないことが起きるらしい
	- [[300_Input/列挙型(enum)の問題点と代替手段  TypeScript入門『サバイバルTypeScript』|列挙型(enum)の問題点と代替手段  TypeScript入門『サバイバルTypeScript』]]
	- [[300_Input/TypeScriptのenumを使わないほうがいい理由を、Tree-shakingの観点で紹介します|TypeScriptのenumを使わないほうがいい理由を、Tree-shakingの観点で紹介します]]

## 型の互換性
- **型には抽象度が存在する**
	- 例： 文字リテラル型の変数を文字列型の変数に代入することができる
```ts
const comp1 = "test"
let comp2:string = comp1 //OK
```
- `comp1`はリテラル型で、`test`という文字列しか受け付けない
- `comp2`は文字列型で、文字列のみを受け付ける
- `comp1`と`comp2`の型は違うのにもかかわらず、`comp2`に`comp1`を代入できる
	- これは文字列型が文字列リテラル型より抽象度が高いから（文字型は文字列リテラル型を含む型だから）
		- 文字列リテラル型⊂文字列型
- 逆は不可能
```ts
let comp3: string = "test"
let comp4: "test" = comp3 //ERROR
```

### 関数の型の互換性
- 引数の数は同じだが、引数の型が違う2つの関数があるとき、関数を持った変数に引数の型が違う変数を代入することができない
```ts
let funcComp1 = (x:number) => {}
let funcComp2 = (x: string) => {}

funcComp1 = funcComp2 //ERROR
funcComp2 = funcComp1 //ERROR
```

## Generics
- オブジェクトに対して型定義をする際に、キーだけ定義しておいて値の型をオブジェクト定義時に決めることができる
```ts
//Generics
interface GEN<T>{
  item: T
}
const gen0: GEN<string> = {item: "hello"}
const gen1: GEN = { item: "hello"} //ERROR itemの型の宣言がされていないため
const gen2: GEN<number> = {item: 123} //OK
```
- 上記のコードでは`GEN`型オブジェクトに`item`というキーが存在することだけを定義して、`GEN`型オブジェクトを定義するときに`item`の値の型を決められる
- オブジェクト定義時に型を宣言しなかった場合エラーとなるが、デフォルトの型を宣言しておくことでエラーを避けることができる
```ts
interface GEN1<T=string>{
  item: T
}
const gen3: GEN1 = { item: "hello"}
const gen4: GEN1 = { item: 123} //デフォルトの型がstringであるため
```

- `extends`を使うことで動的に定義される型の種類を制限することが可能
```ts
interface GEN3<T extends string | number>{
  item: T
}

const gen5: GEN2<string> = {item: "hello"} //OK
const gen6: GEN2<number> = {item: 123} //OK
const gen7: GEN2<boolean> = {item: true} //ERROR itemに割り当てられるのはstringかnumberのみ
```

### 関数に対するGenerics
- 関数に渡す引数の型をGenericsで動的に変化させる場合、型推論が行われるため明示的に型を宣言する必要が無くなる
```ts
function funcGen<T>(props: T){
  return {item: props}
}
const gen7 = funcGen("test")  //引数の型が自動的に推論される
const gen8 = funcGen<string>("test")　//明示的に宣言することも可能
```
- 関数のGenericに対しても、`Union Types`や`extend`が使用可能
```ts
const gen9 = funcGen<string | null>(null)

function funcGen1<T extends string | null>(props: T){
  return {value: props}
}
```


### Reactでよくある書き方
- Propsの型を定義してそれを関数コンポーネントに渡す時の書き方
```ts
interface Props {
  price: number;
}
function funcGen2<T extends Props>(props: T){
  return {value: props.price}
}
  
const gen10 = funcGen2({price: 10})

//アロー関数での書き方
const funcGen3 = <T extends Props>(props: T) => {
  return {value: props.price}
}

```

## JSON型推論をやってみる
- JSONplaceholderから取得したJSONデータの型をtypeofで取得できる
```ts
import Data from "./data.json" //JSONplaceholderからJSONをコピーしたファイル
type USERS = typeof Data
```


## React×TypeScriptでの型定義
### Propsの型定義
- 関数コンポーネントの型：**React.FC**
```tsx
const App: React.FC = () => {
  return (
    <div className="App">
    </div>
  );
}
```

- 関数コンポーネントが受け取るPropsの型を定義する方法
```tsx
interface Props {
  text: string
}

const TestComponent: React.FC<Props> = (props) => {
  return (
    <div>TestComponent</div>
  )
}
```

### Stateの型定義
- useStateを使う時に、stateの初期値を指定しておくとstateの値の型推論が行われる
	- `const [count, setCount] = useState(0)`と書くと`setCount`の引数と`count`の型はnumberとなる
- 初期値を指定しないと`setCount`の引数と`count`の型はundefined型になってしまうため、Union Typesを指定してundefined型以外の型を取るようにするなどの対策が必要
	- 基本的にstateには初期値を指定するのが望ましい
- interfaceなどで定義した型をstateに割り当てる方法
```tsx
interface UserData {
  id: number
  name: string
}
const TestComponent: React.FC = () => {
  const [user, setUser] = useState<UserData>()
  return (
    <div></div>
  )
}
```


### Event handlerのデータ型
- inputの`onChange`イベントを取得して、stateをvalueで更新する
- イベントの型は、inputタグの`onChange`にカーソルをホバーすることで取得できる
	- `React.ChangeEventHandler<HTMLInputElement>`と表示されるので、`Handler`部分を消して、`e: React.ChangeEvent<HTMLInputElement>`と定義すればよい
	- `onChange`に設定した関数にホバーすれば、返り値の型が取得できるからそっちの方がいい
	- `onChange`にホバーした時
		- ![[Pasted image 20230618132856.png]]
	- 関数名にホバーした時
		- ![[Pasted image 20230618132847.png]]

## 参考文献
- [[300_Input/最速で学ぶTypeScript  Udemy|最速で学ぶTypeScript  Udemy]]
- [[りあクト！TypeScriptで始めるつらくないReact開発1]]

[[2023-06-18]]