---
title: Next.js + Supabase でログイン周りの機能を実装する
source: https://qiita.com/masakiwakabayashi/items/716577dbfebf83665378
author:
  - "[[Qiita]]"
published: 2023-03-02
created: 2025-04-20
description: 今回の記事では、Next.jsとSupabaseを使って、・ユーザー登録・ログイン・ログイン中のユーザーの表示・ログアウト・パスワード再設定の機能を実装する方法を解説していきます。また…
tags:
  - 🎁Topic/Tech
image: https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-user-contents.imgix.net%2Fhttps%253A%252F%252Fcdn.qiita.com%252Fassets%252Fpublic%252Farticle-ogp-background-afbab5eb44e0b055cce1258705637a91.png%3Fixlib%3Drb-4.0.0%26w%3D1200%26blend64%3DaHR0cHM6Ly9xaWl0YS11c2VyLXByb2ZpbGUtaW1hZ2VzLmltZ2l4Lm5ldC9odHRwcyUzQSUyRiUyRnFpaXRhLWltYWdlLXN0b3JlLnMzLmFwLW5vcnRoZWFzdC0xLmFtYXpvbmF3cy5jb20lMkYwJTJGMzA4OTI5MyUyRnByb2ZpbGUtaW1hZ2VzJTJGMTY3Mjc5ODIyND9peGxpYj1yYi00LjAuMCZhcj0xJTNBMSZmaXQ9Y3JvcCZtYXNrPWVsbGlwc2UmZm09cG5nMzImcz1jMDY5NjYyNjU1OTkwZjJhMWRmMDM0NTMwMDM4OTdlYQ%26blend-x%3D120%26blend-y%3D467%26blend-w%3D82%26blend-h%3D82%26blend-mode%3Dnormal%26s%3D0592efcb04b0dae67db9bc30843c08b7?ixlib=rb-4.0.0&w=1200&fm=jpg&mark64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTk2MCZoPTMyNCZ0eHQ9TmV4dC5qcyUyMCUyQiUyMFN1cGFiYXNlJTIwJUUzJTgxJUE3JUUzJTgzJUFEJUUzJTgyJUIwJUUzJTgyJUE0JUUzJTgzJUIzJUU1JTkxJUE4JUUzJTgyJThBJUUzJTgxJUFFJUU2JUE5JTlGJUU4JTgzJUJEJUUzJTgyJTkyJUU1JUFFJTlGJUU4JUEzJTg1JUUzJTgxJTk5JUUzJTgyJThCJnR4dC1hbGlnbj1sZWZ0JTJDdG9wJnR4dC1jb2xvcj0lMjMxRTIxMjEmdHh0LWZvbnQ9SGlyYWdpbm8lMjBTYW5zJTIwVzYmdHh0LXNpemU9NTYmdHh0LXBhZD0wJnM9YzIyN2I2MTEwMTkyZmYzMWI2NmVjZDU4OTVkYTgwMzI&mark-x=120&mark-y=112&blend64=aHR0cHM6Ly9xaWl0YS11c2VyLWNvbnRlbnRzLmltZ2l4Lm5ldC9-dGV4dD9peGxpYj1yYi00LjAuMCZ3PTgzOCZoPTU4JnR4dD0lNDBtYXNha2l3YWthYmF5YXNoaSZ0eHQtY29sb3I9JTIzMUUyMTIxJnR4dC1mb250PUhpcmFnaW5vJTIwU2FucyUyMFc2JnR4dC1zaXplPTM2JnR4dC1wYWQ9MCZzPWExZWU2Y2NiM2I4YmFmMDY0ZjA2ZDQwNDNmMWJmOGUz&blend-x=242&blend-y=480&blend-w=838&blend-h=46&blend-fit=crop&blend-crop=left%2Cbottom&blend-mode=normal&s=c3a4a92e144889526c0fe2566171b3ed
---
この記事は最終更新日から1年以上が経過しています。

[@masakiwakabayashi (若林 将輝)](https://qiita.com/masakiwakabayashi)

最終更新日 投稿日 2023年03月02日

今回の記事では、Next.jsとSupabaseを使って、

・ユーザー登録  
・ログイン  
・ログイン中のユーザーの表示  
・ログアウト  
・パスワード再設定

の機能を実装する方法を解説していきます。

また、上記の機能をNext.jsとFirebaseを使って実装する方法もこちらの記事で解説しています。

## 開発環境

- macOS Catalina 10.15.7
- Next.js
- Supabase
- Reactstrap

※Next.jsはJavaScriptを使っています。

## プロジェクト作成

Next.jsのプロジェクトを作成します。ターミナルで以下のコマンドを入力してください。

```text
npx create-next-app
```

プロジェクトの作成が終わったら、以下のコマンドを実行します。

```text
npm install
npm run dev
```

ここまでできたら一旦、 [http://localhost:3000/](http://localhost:3000/) にアクセスし、Next.jsの初期画面が表示されることを確認してください。

## Reactstrapのインストール

今回は画面のデザインを整えるためにReactstrapを使います。まず以下のコマンドでReactstrapとBootstrapをインストールしてください。

```text
npm install reactstrap react react-dom
```

```text
npm install --save bootstrap
```

インストールしたら\_app.jsを開いて、以下のように編集します。

pages/\_app.js

```javascript
// globals.cssをコメントアウトする
// import '../styles/globals.css'

// Bootstrapを読み込む
import 'bootstrap/dist/css/bootstrap.min.css';

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default MyApp
```

これでReactstrapが使えるようになります。

## Supabaseのインストール

Supabaseと認証機能の作成に必要なライブラリをインストールします。

まずターミナルで以下のコマンドを入力してSupabaseのパッケージをインストールします。

```text
npm install @supabase/supabase-js
```

続いて、以下のコマンドもターミナルで実行し、認証機能に必要なライブラリもインストールしておきます。

```text
npm install @supabase/auth-helpers-nextjs
```

```text
npm install @supabase/auth-helpers-react
```

## Supabaseの設定

次はSupabaseの認証機能を使うための設定をしていきます。

まずはSupabaseのサイトを開いて「Sign in」を選択し、Supabaseの管理画面にログインしてください。※まだSupabaseのアカウントを作成していない場合は「Start your project」のところからアカウントを作成してください。  
[![スクリーンショット 2023-01-30 16.51.24.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/24cf361f-c603-3c9f-9230-b70c0e8b0ad0.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F24cf361f-c603-3c9f-9230-b70c0e8b0ad0.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=9c2725039d80fc8ce8dad0eae8c6cc6e)

ログインしたら管理画面にある「New project」をクリックします。  
[![スクリーンショット 2023-01-30 16.52.10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/ad6c822f-75a5-3216-d756-5f05c1aa3e98.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2Fad6c822f-75a5-3216-d756-5f05c1aa3e98.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=c6f9be82f16d826c023f9785574d7745)

するとorganizationを選択するポップアップが出てきますので、すでに作成されているorganizationを選択します。  
[![スクリーンショット 2023-01-30 16.52.39.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/b116efc8-fe8c-9fcf-00a4-2937f32daf31.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2Fb116efc8-fe8c-9fcf-00a4-2937f32daf31.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=32c140135667334db357afb25ed5e137)

新しいプロジェクトを作成画面が表示されるので、プロジェクト名とデータベースのパスワードを入力し、Regionを「Northeast Asia (Tokyo)」に変更して「Create new project」をクリックします。  
[![スクリーンショット 2023-01-30 16.54.37.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/c11be5a9-14ae-f953-d363-20ea27d61dbd.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2Fc11be5a9-14ae-f953-d363-20ea27d61dbd.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=2dced9d31e3e011e0e85e6ff19559f27)

プロジェクトの管理画面に遷移されます。この時点でまだプロジェクト名の横に「Setting up project」の表示が出ている場合は、表示が消えるまで待ちます。  
[![スクリーンショット 2023-01-31 10.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/7b1d7a0f-4d19-fa30-11d6-8fc1eea0d447.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F7b1d7a0f-4d19-fa30-11d6-8fc1eea0d447.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=505ec73b3c323a17d4e4e97b00abe544)

「Setting up project」の表示が消えたら、サイドバーにある「Authentication」を選択します。  
[![スクリーンショット 2023-01-30 16.57.37.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/cb98b5d3-9f2f-96a2-f231-00248322cd80.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2Fcb98b5d3-9f2f-96a2-f231-00248322cd80.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=0279dfddc86859c332fccf61d82b3d7d)

「Authentication」の画面を開いたら「Providers」を選択します。  
[![スクリーンショット 2023-01-30 16.57.52.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/32c4be86-95dd-e7d4-02c1-50d91e988d06.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F32c4be86-95dd-e7d4-02c1-50d91e988d06.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=224e8a3eee422bc370b0d60508b6611b)

「email」のところを開きます。  
[![スクリーンショット 2023-01-30 16.59.23.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/28712d6e-42b1-59bf-2c47-5338088a5597.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F28712d6e-42b1-59bf-2c47-5338088a5597.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=3a0a4ce97514bdbed2376b399672c242)

「Confirm email」をオフにして「save」をクリックしてください。今回はメールアドレスの認証を行わなくてもログインできるようにするためにこちらはオフにしておきます。  
[![スクリーンショット 2023-01-30 17.00.01.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/99706877-30b1-7c25-6bf8-9c91414c632b.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F99706877-30b1-7c25-6bf8-9c91414c632b.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=e27cdae30c6d46ac23c0913b87aceaa1)

これでログイン機能を実装するためのSupabaseの管理画面上での設定は完了です。

## .envファイルに環境変数を設定する

Next.jsのプロジェクトのルートディレクトリに.envファイルを作成します。

次にSupabaseのプロジェクトの管理画面を開き、サイドバーにある「Project Setting」を選択します。  
[![スクリーンショット 2023-01-31 11.31.43.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/9f0a0f61-e073-9d42-2308-16c41a7c6ed8.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F9f0a0f61-e073-9d42-2308-16c41a7c6ed8.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=0bbbbb7401a215f408e17fbc7ded8c96)

「API」の画面を開き、

- Project URL
- Project API keys

の値をコピーします。  
[![スクリーンショット 2023-01-31 11.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/8d9691e4-fd3a-b4ea-20e8-11e174ed8b67.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F8d9691e4-fd3a-b4ea-20e8-11e174ed8b67.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=5e590e644621e0e50e8f23a9a7a4246d)

コピーした値を.envに環境変数として設定します。

.env

```shell
NEXT_PUBLIC_SUPABASE_URL=xxxxxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxx
NEXT_PUBLIC_SUPABASE_API_KEY=xxxxxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxx
```

## Supabaseの初期化

まずSupabaseの初期化を行うためのファイルを用意します。プロジェクトのルートディレクトリにutilsというフォルダを新しく作成し、その中にsupabase.jsというファイルを作成します。

supabase.jsの中身は以下のように書いてください。

utils/supabase.js

```javascript
import { createClient } from '@supabase/supabase-js'

// supabaseの初期化を行う
export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_API_KEY
)
```

ここからは実際にNext.jsに認証関連の処理を書いていきます。

## ユーザー登録

まずはユーザー登録機能から実装します。

プロジェクトのpagesディレクトリの中にregister.jsというファイルを新しく作成し、中身を以下のようにしてください。

pages/register.js

```javascript
import styles from '../styles/Home.module.css'
// 現時点で使わないものもあるが今後のことを考えて入れておく
import { Col, Container, Form, FormGroup, Input, Label, Row, Button } from "reactstrap";
import { useState } from 'react';

// supabase
import { supabase } from '../utils/supabase';

export default function Register() {
  // useStateでユーザーが入力したメールアドレスとパスワードをemailとpasswordに格納する
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // supabaseのユーザー登録の関数
  const doRegister =  async () => {
    // supabaseで用意されているユーザー登録の関数
    const { data, error } = await supabase.auth.signUp({ email, password })
    if (error) throw new Error(error.message)
    console.log(data)
  }

  return (
    // Home.module.cssでcardクラスに適用されているCCSを、このdivタグに適用する
    <div className={styles.card}>
      <h1>新規登録</h1>
      <div>
        <Form>
            <FormGroup>
              <Label>
                メールアドレス：
              </Label>
              <Input
                type="email"
                name="email"
                style={{ height: 50, fontSize: "1.2rem" }}
                // onChangeでユーザーが入力した値を取得し、その値をemailに入れる
                onChange={(e) => setEmail(e.target.value)}
              />
            </FormGroup>
            <FormGroup>
              <Label>
                パスワード：
              </Label>
              <Input
                type="password"
                name="password"
                style={{ height: 50, fontSize: "1.2rem" }}
                // onChangeでユーザーが入力した値を取得し、その値をpasswordに入れる
                onChange={(e) => setPassword(e.target.value)}
              />
            </FormGroup>
            <Button
                style={{ width: 220 }}
                color="primary"
                // 登録ボタンがクリックされたとき関数が実行されるようにする
                onClick={()=>{
                  doRegister();
                }}
              >
              登録
            </Button>
        </Form>
      </div>
    </div>
  )
}
```

ユーザーが入力したメールアドレスとパスワードをuseStateを使って受け取り、ユーザー登録のボタンがクリックされたときに、Supabaseで用意されているユーザー登録の関数が実行されるという処理になっています。

Register.jsの中身を書いたら、実際に [http://localhost:3000/register](http://localhost:3000/register) にアクセスし、フォームからユーザーの登録ができるかどうかを確認してみましょう。  
[![スクリーンショット 2023-01-31 16のコピー.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/9af49966-bf8d-10b4-9752-57e126c7ffec.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F9af49966-bf8d-10b4-9752-57e126c7ffec.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=0b026eccdcf16056192aa07a58957c43)

フォームを入力した後にSupabaseの管理画面でAuthenticationのUsersを見て、先ほどRegisterのページから入力したメールアドレスが登録されているかどうかを確認します。

こちらのようにメールアドレスが登録されていれば問題ありません。  
[![スクリーンショット 2023-01-31 16.29.28.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/0f5e3304-970a-015e-7b98-d7e593b5d747.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F0f5e3304-970a-015e-7b98-d7e593b5d747.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=d0757006554f3fdc63f3cee1332873ee)

## ログイン

ユーザー登録と同じようにログイン機能も作成していきます。pagesディレクトリにlogin.jsというファイルを作成して中身を以下のように書いてください。

pages/login.js

```javascript
import styles from '../styles/Home.module.css'
// 現時点で使わないものもあるが今後のことを考えて入れておく
import { Col, Container, Form, FormGroup, Input, Label, Row, Button } from "reactstrap";
import { useEffect, useState } from 'react';

// supabase
import { supabase } from '../utils/supabase';

export default function Register() {
  // useStateでユーザーが入力したメールアドレスとパスワードをemailとpasswordに格納する
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // ログインの関数
  const doLogin =  async () => {
    // supabaseで用意されているログインの関数
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) throw new Error(error.message)
    console.log(data)
  }

  return (
    // Home.module.cssでcardクラスに適用されているCCSを、このdivタグに適用する
    <div className={styles.card}>
      <h1>ログイン</h1>
      <div>
        <Form>
            <FormGroup>
              <Label>
                メールアドレス：
              </Label>
              <Input
                type="email"
                name="email"
                style={{ height: 50, fontSize: "1.2rem" }}
                // onChangeでユーザーが入力した値を取得し、その値をemailに入れる
                onChange={(e) => setEmail(e.target.value)}
              />
            </FormGroup>
            <FormGroup>
              <Label>
                パスワード：
              </Label>
              <Input
                type="password"
                name="password"
                style={{ height: 50, fontSize: "1.2rem" }}
                // onChangeでユーザーが入力した値を取得し、その値をpasswordに入れる
                onChange={(e) => setPassword(e.target.value)}
              />
            </FormGroup>
            <Button
                style={{ width: 220 }}
                color="primary"
                // 登録ボタンがクリックされたとき関数が実行されるようにする
                onClick={()=>{
                  doLogin();
                }}
              >
              ログイン
            </Button>
        </Form>
      </div>
    </div>
  )
}
```

ログインの処理はユーザー登録の処理とほぼ同じです。useStateでユーザーが入力したメールアドレスとパスワードを取得して、ログインボタンがクリックされたときにsupabaseのログイン関数が実行されるような仕組みになっています。

## ログインしているユーザーの表示

続いてはログインしているユーザーの情報を画面に表示する処理を作成していきます。ヘッダーコンポーネントを作成し、そこにログインしているユーザーのメールアドレスが表示されるような処理を書いていきます。

プロジェクトのルートディレクトリにcomponentsフォルダを作成します。その中にHeader.jsというファイルを作成します。Header.jsの中身は以下のように書いてください。

components/Header.js

```javascript
import { Button } from 'reactstrap';
import { useEffect, useState } from 'react';

// supabaseをインポート
import { supabase } from '../utils/supabase';

const Header = () => {
  const [currentUser, setcurrentUser] = useState('');

    // 現在ログインしているユーザーを取得する処理
  const getCurrentUser = async () => {
    // ログインのセッションを取得する処理
    const { data } = await supabase.auth.getSession()
    // セッションがあるときだけ現在ログインしているユーザーを取得する
    if (data.session !== null) {
      // supabaseに用意されている現在ログインしているユーザーを取得する関数
      const { data: { user } } = await supabase.auth.getUser()
      // currentUserにユーザーのメールアドレスを格納
      setcurrentUser(user.email)
    }
  }

  // HeaderコンポーネントがレンダリングされたときにgetCurrentUser関数が実行される
  useEffect(()=>{
    getCurrentUser()
  },[])

  return (
    <div style={{ padding: "1rem" }} >
      { currentUser ? (
        // サーバーサイドとクライアントサイドでレンダーされる内容が違うときにエラーがでないようにする
        <div suppressHydrationWarning={true}>
          <div style={{ paddingBottom: "1rem" }}>{ currentUser } でログインしています。</div>
        </div>
      ):(
        <div suppressHydrationWarning={true}>ログインしていません。</div>
      )}
    </div>
  );
}

export default Header;
```

こちらの部分が現在ログインしているユーザーを取得するための処理です。

この関数は、ログインしていないときに実行されるとコンソールにエラーが出てしまうので、ログインのセッションがある場合だけ実行されるようにしておきます。

では、このヘッダーコンポーネントをログインページにインポートして、ログインしている場合はユーザーのメールアドレス、ログインしていない場合は「ログインしていません」と表示されるようにしていきます。

pagesディレクトリにあるlogin.jsを以下のように編集してください。

pages/login.js

```javascript
import styles from '../styles/Home.module.css'
// 現時点で使わないものもあるが今後のことを考えて入れておく
import { Col, Container, Form, FormGroup, Input, Label, Row, Button } from "reactstrap";
import { useEffect, useState } from 'react';
// supabase
import { supabase } from '../utils/supabase';

// ヘッダーコンポーネントをインポート
import  Header from '../components/Header';
// useRouterをインポート
import { useRouter } from 'next/router';

export default function Register() {
  // useStateでユーザーが入力したメールアドレスとパスワードをemailとpasswordに格納する
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  // supabaseのユーザー登録の関数
  const doLogin =  async () => {
    // supabaseで用意されているユーザー登録の関数
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    if (error) throw new Error(error.message)
    console.log(data)
    // ログインを反映させるためにリロードさせる
    router.reload()
  }

  return (
    // Home.module.cssでcardクラスに適用されているCCSを、このdivタグに適用する
    <div className={styles.card}>
      <h1>ログイン</h1>
      <Header/>
      <div>
        <Form>
            <FormGroup>
              <Label>
                メールアドレス：
              </Label>
              <Input
                type="email"
                name="email"
                style={{ height: 50, fontSize: "1.2rem" }}
                // onChangeでユーザーが入力した値を取得し、その値をemailに入れる
                onChange={(e) => setEmail(e.target.value)}
              />
            </FormGroup>
            <FormGroup>
              <Label>
                パスワード：
              </Label>
              <Input
                type="password"
                name="password"
                style={{ height: 50, fontSize: "1.2rem" }}
                // onChangeでユーザーが入力した値を取得し、その値をpasswordに入れる
                onChange={(e) => setPassword(e.target.value)}
              />
            </FormGroup>
            <Button
                style={{ width: 220 }}
                color="primary"
                // 登録ボタンがクリックされたとき関数が実行されるようにする
                onClick={()=>{
                  doLogin();
                }}
              >
              ログイン
            </Button>
        </Form>
      </div>
    </div>
  )
}
```

ヘッダーコンポーネントを読み込んで表示させるための記述と、ログインしたあとにヘッダーコンポーネントにあるユーザーの情報を取得するgetCurrentUser()が実行されるようにするためのリロードの処理を追加しています。

ここまでできたら実際に [http://localhost:3000/login](http://localhost:3000/login) にアクセスしてログインを行い、ログインしているユーザーのメールアドレスが表示されるかどうかを確認してみましょう。  
[![スクリーンショット 2023-02-01 14.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/9c6d81a0-8e1f-1a55-e238-4a7e2027a8e1.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F9c6d81a0-8e1f-1a55-e238-4a7e2027a8e1.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=67f11a51b17575fccb7e46449b630c21)

## ログアウト

では、先ほど作成したヘッダーコンポーネントにログアウトの処理を追加していきます。Header.jsの内容を以下のように編集してください。

components/Header.js

```javascript
import { Button } from 'reactstrap';
import { useEffect, useState } from 'react';

// supabaseをインポート
import { supabase } from '../utils/supabase';

// useRouterをインポート
import { useRouter } from 'next/router';

const Header = () => {
  const [currentUser, setcurrentUser] = useState('');
  // routerを使うための記述
  const router = useRouter();

    // 現在ログインしているユーザーを取得する処理
  const getCurrentUser = async () => {
    // ログインのセッションを取得する処理
    const { data } = await supabase.auth.getSession()
    // セッションがあるときだけ現在ログインしているユーザーを取得する
    if (data.session !== null) {
      // supabaseに用意されている現在ログインしているユーザーを取得する関数
      const { data: { user } } = await supabase.auth.getUser()
      // currentUserにユーザーのメールアドレスを格納
      setcurrentUser(user.email)
    }
  }

  // HeaderコンポーネントがレンダリングされたときにgetCurrentUser関数が実行される
  useEffect(()=>{
    getCurrentUser()
  },[])

  // ログアウトの処理を追加
  const doLogout = async () => {
    // supabaseに用意されているログアウトの関数
    const { error } = await supabase.auth.signOut()
    if (error) throw new Error(error.message)
    // ログアウトを反映させるためにリロードさせる
    router.reload()
  }

  // ログアウトボタンも追加
  return (
    <div style={{ padding: "1rem" }} >
      { currentUser ? (
        // サーバーサイドとクライアントサイドでレンダーされる内容が違うときにエラーがでないようにする
        <div suppressHydrationWarning={true}>
          <div style={{ paddingBottom: "1rem" }}>{ currentUser } でログインしています。</div>
          <div>
            <Button onClick={()=>{
              doLogout();
            }} >
              ログアウト
            </Button>
          </div>
        </div>
      ):(
        <div suppressHydrationWarning={true}>ログインしていません。</div>
      )}
    </div>
  );
}

export default Header;
```

ログアウトに関してもSupabaseにログアウト関数が用意されているので、そちらを使えばログアウトの機能を実装できます。

また、ログアウトしたときにログイン状態を監視するgetCurrentUser()が呼び出されるように、router.reload()を使ってページをリロードさせています。

ここまで実装を行えば、ログインしている状態でヘッダーにログアウトボタンが表示されるので、ログアウトボタンを押して実際にログアウトできるかどうかを確認してみましょう。  
[![スクリーンショット 2023-02-01 14.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/87172873-07ff-934b-efb9-011f6a08a3df.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2F87172873-07ff-934b-efb9-011f6a08a3df.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=ac8a70b039fc4d59a7f82e51b065bae9)

## パスワード再設定

最後にパスワード再設定機能を実装していきます。

パスワード再設定機能は

- パスワード再設定メールの送信する処理
- パスワード再設定画面でのパスワードの再設定をする処理

の2つに大きくわかれています。まずは、パスワード再設定のためのメールをユーザーに送信するための処理を作成していきます。

プロジェクトのpagesディレクトリにforgot\_password.jsというファイルを作成します。これがパスワードを再設定できるページのリンクが記載されたメールをユーザーのメールアドレスに送信するためのページになります。

forgot\_password.jsの中身は以下のように書きます。

pages/forgot\_password.js

```javascript
import styles from '../styles/Home.module.css'
import { Col, Container, Form, FormGroup, Input, Label, Row, Button } from "reactstrap";
import { useState } from 'react';

// supabase
import { supabase } from '../utils/supabase';

export default function Login() {
  const [email, setEmail] = useState('');

  // 送信ボタンがクリックされるとdoResetEmail関数が実行される
  const sendResetEmail = async () => {
    // supabaseで用意されているパスワード再設定のメールを送信するための関数
    const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
      // 後ほどここにパスワード再設定画面のリンクを設定します
      redirectTo: '',
    })
    if (error) throw new Error(error.message)
    console.log(data)
    // メールが送信されたことをわかりやすくするためのアラート
    alert("メールを送信しました。")
  }

  return (
    <div className={styles.card}>
      <h1>パスワード再設定メールの送信</h1>
      <div>
        <Form>
            <FormGroup>
              <Label>
                メールアドレス：
              </Label>
              <Input
                type="email"
                name="email"
                style={{ height: 50, fontSize: "1.2rem" }}
                // ユーザーが入力したメールアドレスを取得する
                onChange={(e) => setEmail(e.target.value)}
              />
            </FormGroup>
            <Button
                style={{ width: 220 }}
                color="primary"
                // ボタンを押すとdoResetEmaiが実行される
                onClick={()=>{
                  sendResetEmail();
                }}
              >
              送信
            </Button>
        </Form>
      </div>
    </div>
  )
}
```

上記のコードにあるresetPasswordForEmailという関数がSupabaseで用意されているパスワード再設定のメールを送るための関数で、パスワード再設定画面のリンクが記載されたメールを指定のメールアドレスに送信することができます。

パスワード再設定画面のリンクは後ほど設定します。

続いてはパスワード再設定ページでユーザーが新しいパスワードを設定するための画面と処理を作成していきます。

Firebaseの場合はユーザーがパスワードを再設定するための画面もFirebaseの方で用意してくれているので、パスワードの再設定メールを送信する機能だけをつくればパスワードの再設定ができるようになっていました。

しかし、Supabaseではユーザーが新しいパスワードを入力して、パスワードを再設定するための画面と処理もこちらで用意する必要があります。

では、プロジェクトのpagesディレクトリにreset\_password.jsというファイルを作成し、中身を以下のようにしてください。

pages/reset\_password.js

```javascript
import styles from '../styles/Home.module.css'
// 現時点で使わないものもあるが今後のことを考えて入れておく
import { Col, Container, Form, FormGroup, Input, Label, Row, Button } from "reactstrap";
import { useState } from 'react';

// supabase
import { supabase } from '../utils/supabase';
// useRouterをインポート
import { useRouter } from 'next/router';

export default function ResetPassword() {
  const [password, setPassword] = useState('');
  const router = useRouter();

  // パスワードを変更する処理
  const doResetPassword = async () => {
    // supabaseで用意されているユーザー情報を変更するための関数
    const { user, error } = await supabase.auth.updateUser(
        // ユーザーが入力したパスワードがsetPasswordでpasswordに格納される
        {
          password: password
        }
      )
    if (error) throw new Error(error.message)
    // ログインページに遷移
    router.push('/login')
  }

  return (
    <div className={styles.card}>
      <h1>新しいパスワードを入力してください。</h1>
      <div>
        <Form>
            <FormGroup>
              <Label>
                パスワード：
              </Label>
              <Input
                type="password"
                name="password"
                style={{ height: 50, fontSize: "1.2rem" }}
                // ユーザーが入力したメールアドレスを取得する
                onChange={(e) => setPassword(e.target.value)}
              />
            </FormGroup>
            <Button
                style={{ width: 220 }}
                color="primary"
                // ボタンを押すとdoResetEmaiが実行される
                onClick={()=>{
                  doResetPassword();
                }}
              >
              送信
            </Button>
        </Form>
      </div>
    </div>
  );
}
```

reset\_password.jsが新しいパスワードを設定するための画面になるので、先ほどのforgot\_password.jsにこちらの画面のリンクを設置します。

pages/forgot\_password.js

```javascript
// supabaseで用意されているパスワード再設定のメールを送信するための関数
    const { data, error } = await supabase.auth.resetPasswordForEmail(email, {
      // パスワード再設定画面のリンク
      redirectTo: 'http://localhost:3000/reset_password',
    })
```

次に\_app.jsを開いて中身を以下のように編集します。

\_app.js

```javascript
import 'bootstrap/dist/css/bootstrap.min.css';
import { supabase } from '../utils/supabase'
import { useEffect } from 'react';

export default function App({ Component, pageProps }) {
  // パスワードを忘れた場合に再設定するための関数 これがないとパスワード再設定のときにエラーが起きる
  useEffect(() => {
    supabase.auth.onAuthStateChange((event, session) => {
      // パスワード再設定のときにログインしていない状態でもパスワードを変更できるようにするための処理
      if (event == 'PASSWORD_RECOVERY') {
        console.log('PASSWORD_RECOVERY', session)
        showPasswordResetScreen(true)
      }
    })
  },[])

  return <Component {...pageProps} />
}
```

ユーザーがパスワードを忘れてしまった場合のパスワード再設定に関しては、ログインしていない状態でも新しいパスワードを設定することができるように、\_app.jsに以下のような処理を追加しています。

\_app.js

```javascript
// パスワードを忘れた場合に再設定するための関数 これがないとパスワード再設定のときにエラーが起きる
  useEffect(() => {
    supabase.auth.onAuthStateChange((event, session) => {
      // パスワード再設定のときにログインしていない状態でもパスワードを変更できるようにするための処理
      if (event == 'PASSWORD_RECOVERY') {
        console.log('PASSWORD_RECOVERY', session)
        showPasswordResetScreen(true)
      }
    })
  },[])
```

パスワードを忘れてしまって再設定する場合、ユーザーはログインしていない状態なので、こちらの処理を書いておかないと新しいパスワードを登録する処理がエラーになってしまいます。

ここまでできたら、自分のメールアドレスにパスワード再設定メールを送信し、実際に新しいパスワードを設定するところまでやってみましょう。  
[![スクリーンショット 2023-02-01 14.52.02.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/e24483e0-143e-a8ca-0069-e554180adb36.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2Fe24483e0-143e-a8ca-0069-e554180adb36.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=743177de70d34bae474458f9daaddb29)

新しくパスワードを再設定して、そのパスワードでログインできることが確認できたら、パスワード再設定機能の実装は完了です。  
[![スクリーンショット 2023-02-01 14.50.45.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3089293/c1ec05e5-e797-cbda-3891-ad9b1d451770.png)](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.ap-northeast-1.amazonaws.com%2F0%2F3089293%2Fc1ec05e5-e797-cbda-3891-ad9b1d451770.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=d03c645d946c628062d5449dae4196d2)

## まとめ

Supabaseにも

・signUp  
・signInWithPassword  
・onAuthStateChange  
・resetPasswordForEmail  
・updateUser

などのログインやユーザー登録のための関数があらかじめ用意されているので、そういった関数を使うことで認証機能は比較的簡単に実装することができます。

今回の記事で解説したコードのGithubのリポジトリはこちらです。  
[https://github.com/masakiwakabayashi/nextjs\_supabase\_auth](https://github.com/masakiwakabayashi/nextjs_supabase_auth)

[0](https://qiita.com/masakiwakabayashi/items/#comments)

## Qiita Conference 2025 4月23日(水)~25(金)開催！

![](https://cdn.qiita.com/assets/public/official_campaigns/qiita_conference_2025/image-conference_2025_ogp_11sponsors-805d80791d0257ca939e5b6a10fed936.png)

Qiita Conferenceは、Qiita最大規模のテックカンファレンスです！

基調講演ゲスト(敬称略)

ymrl、成瀬 允宣、鹿野 壮、伊藤 淳一、uhyo、徳丸 浩、ミノ駆動、みのるん、桜庭 洋之、tenntenn、けんちょん、こにふぁー

[イベント詳細を見る](https://qiita.com/official-campaigns/conference/2025?utm_source=qiita&utm_medium=banner&utm_campaign=article_footer_banner_default&utm_content=default)

[16](https://qiita.com/masakiwakabayashi/items/716577dbfebf83665378/likers)

8

![](https://cdn.qiita.com/assets/public/push_notification/image-qiitan-572179a3bbde375850422ea48b2b6272.png)

Qiitaから通知を受け取りませんか？

最新のトレンドなどの情報をお届けします