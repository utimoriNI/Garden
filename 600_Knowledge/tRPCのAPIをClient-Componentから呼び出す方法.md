---
created: 2024-06-01 12:00
tags:
  - Knowledge
  - 🎁Topic/Tech
---
> [!info]- 経緯
> - Server Componentの中でAPIを呼び出す関数を定義して子コンポーネント(Client Component)に渡していたが、その関数を子コンポーネントで定義するように変更しようとした
> 	- [[非同期関数を子コンポーネントに渡す]]
> - Server Componentで関数を定義していた方法でClient Componentでも関数を定義していたら以下のエラーが発生した
> 	- 'You're importing a component that needs next/headers. That only works in a Server Component which is not supported in the pages/ directory. Read more: [https://nextjs.org/docs/getting-started/](https://nextjs.org/docs/getting-started/) react-essentials#server-components'

> [!success] 解決策
> サーバーコンポーネントでのAPIの呼び出し方と、クライアントコンポーネントでの呼び出し方は違うらしい
> クライアントコンポーネントでAPIを呼び出すには、tRPCのフロントエンド用クライアントを使用してAPIを呼び出す
> `useQuery`, `useMutation`, `useContext`などのReact Queryフックを使用する

## tRPC APIをサーバーサイドで呼び出す
tRPCのAPIをServer Component内で呼び出す際は、`createCallerFactory(Router)`によって作成されたCallerを用いてAPIを呼び出す。
T3Stackのテンプレートでアプリを作成した場合は、`src/server.ts`内に定義された`api`をimportすることで、tRPC APIを呼び出すことができる。

[Server Side Calls | tRPC](https://trpc.io/docs/server/server-side-calls)より
```ts
import { initTRPC } from '@trpc/server';
import { z } from 'zod';
 
type Context = {
  foo: string;
};
 
const t = initTRPC.context<Context>().create();
 
const publicProcedure = t.procedure;
const { createCallerFactory, router } = t;
 
interface Post {
  id: string;
  title: string;
}
const posts: Post[] = [
  {
    id: '1',
    title: 'Hello world',
  },
];
const appRouter = router({
  post: router({
    add: publicProcedure
      .input(
        z.object({
          title: z.string().min(2),
        }),
      )
      .mutation((opts) => {
        const post: Post = {
          ...opts.input,
          id: `${Math.random()}`,
        };
        posts.push(post);
        return post;
      }),
    list: publicProcedure.query(() => posts),
  }),
});
 
// 1. create a caller-function for your router
const createCaller = createCallerFactory(appRouter);
 
// 2. create a caller using your `Context`
const caller = createCaller({
  foo: 'bar',
});
 
// 3. use the caller to add and list posts
const addedPost = await caller.post.add({
  title: 'How to make server-side call in tRPC',
});
 
const postList = await caller.post.list();
```

上記コードでは、`const appRouter ~`の箇所でプロシージャ(APIの具体的な処理)を定義し、それを`3. use the caller to add and list posts`以下で呼び出している
`1. create a caller-function for your router`、`2. create a caller using your Context`でAPIを呼び出すためのcallerを定義している。
この部分はT3Stackのテンプレートで事前に作成されているため、自身で記述する必要はない。

テンプレートではcallerは以下のように定義されている。
```ts
// server.ts
import { headers } from "next/headers";
import { cache } from "react";
  
import { createCaller } from "~/server/api/root";
import { createTRPCContext } from "~/server/api/trpc";
  
/**
 * This wraps the `createTRPCContext` helper and provides the required context for the tRPC API when
 * handling a tRPC call from a React Server Component.
 */
const createContext = cache(() => {
  const heads = new Headers(headers());
  heads.set("x-trpc-source", "rsc");
  
  return createTRPCContext({
    headers: heads,
  });
});
  
export const api = createCaller(createContext);
```

上記のコードの中で使用している`headers()`メソッドがServer Componentでしか使用できないメソッドになっているため、この中で定義している`api`をClient Componentで使用した時に以下のエラーが発生していた。
> 'You're importing a component that needs next/headers. That only works in a Server Component which is not supported in the pages/ directory. Read more: [https://nextjs.org/docs/getting-started/](https://nextjs.org/docs/getting-started/) react-essentials#server-components'

そのため、Client ComponentでtRPC APIを呼び出すには次の方法を用いる必要がある。

## tRPCのフロント用クライアント
tRPC APIをClient Componentで呼び出すには、フロントで使用するクライアントをimportし、それを用いてtRPCのサーバーのエンドポイントにアクセスする必要がある。
クライアントは`createTRPCReact`や`createTRPCProxyClient`などで作成でき、T3Stackのテンプレートでは、`src/trpc/react.tsx`で`api`として事前に定義されている。
そのため、Client Componentの中で`react.tsx`から`api`をimportすればtRPC APIを呼び出すことができる。
❗Server Component用のcallerも同じ`api`という名前で定義されているため、importする時には注意❗

> [!tip] クライアントはstateとして定義されている
> クライアントはstateとして定義されているため、Contextを用いてアプリ内でクライアントを共有している
> そのため、ContextとProviderの定義が必要だが、T3Stackテンプレートでは事前に2つの定義がよしなにされている。べんり。

### フロント用クライアントを用いたAPI呼び出し
フロント用クライアントをでAPI呼び出しを行うには、React Queryフックを使用する。
主に使うフックは`useQuery`, `useMutation`, `useContext`の3つである。

`useQuery`と`useMutation`はプロシージャの実装に合わせて使い分ける(?)
```ts
const appRouter = router({
	greeting: publicProcedure
		.input(z.object({ name: z.string() }))
		.query(({ input }) => {
			return { text: `Hello ${input.name}` }
	}),
});
```
もし上記のようなプロシージャが定義されていた場合は、プロシージャが`query`として定義されているため`useQuery`を使用する。

#### useQuery
`useQuery`フックは、データの取得に使用する。
```tsx
import { trpc } from '../path/to/utils/trpc'

export function SampleQueryComponent() {
	const res = trpc.greeting.useQuery({ name: 'john' })
	return <div>{res.data?.text}</div>
}
```
返り値には様々な値が格納されるが、良く使用されるのは以下の4つ
- `isLoading`：読み込み中かどうかを返す真偽値
- `isSuccess`：データの取得に成功したかどうかを返す真偽値
- `isError`：データの取得に失敗したかを返す真偽値
- `refetch`：データの再取得を行うための関数


#### useMutation
`useMutation`フックは、データの更新に使用する。
```tsx
import { trpc } from '../path/to/utils/trpc'

export function SampleMutationComponent() {
	const mutation = trpc.addPost.useMutation({
		onMutate(variables) { 
			// 処理
		},
		onSuccess(data, variables, context) {
			// 処理
		},
		onError(error, variables, context) {
			// 処理
		},
		onSettled(data, error, variables, context) {
			// 処理
		},
	})
	function handleAddContent() {
		mutation.mutate({ content: 'hello' }, {
			onSuccess(data, variables, context) {
				// 処理
			},
			onError(error, variables, context) {
				// 処理
			},
			onSettled(data, error, variables, context) {
				// 処理
			},
		})
	}

	return <div><button onClick={handleAddContent}>add content</button></div>
}
```
`useMutation`からは、`isLoading`, `isSuccess`, `isError`に加えて更新処理を実行するための`mutate`関数が含まれる。
更新処理に必要な`input`の情報を`mutate`関数に渡すことで更新が行われる。

また、`useMutation`では、更新処理の状況に応じて追加で処理をするためのオプションを4種類まで設定できる。
- `onMutate`：更新が行われる前の処理
- `onSuccess`：更新の成功時の処理
- `onError`：更新のエラー時の処理
- `onSettled`：更新のエラー時と成功時の両方の処理

`onMutate`以外の追加の処理は`mutate`でも行うことができ、以下のように使い分ける。
`mutate`:複数個所で`mutate`を呼び出しており、それぞれで成功時などの処理を変えたい場合
`useMutation`:全ての`mutate`の呼び出しで、成功時などの処理を統一したい場合

#### useContext
`useContext`フックはReact Queryのキャッシュ情報にアクセスするためのフック。
規模が大きいアプリで使うものな気がするから詳細は割愛


### References
[[tRPC入門-型安全なwebアプリケーションを効率よく作る-]]
[tRPCの簡易設定 (AppRouter)](https://zenn.dev/hayato94087/articles/08d63958b57fbe#client-components)
[Set up the React Query Integration | tRPC](https://trpc.io/docs/client/react/setup)
[Server Side Calls | tRPC](https://trpc.io/docs/server/server-side-calls)

---
