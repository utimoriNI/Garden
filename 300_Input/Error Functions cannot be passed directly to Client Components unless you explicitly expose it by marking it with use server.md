[[ReadItLater]] [[StackExchange]]

# [Error: Functions cannot be passed directly to Client Components unless you explicitly expose it by marking it with "use server"](https://stackoverflow.com/questions/75676177/error-functions-cannot-be-passed-directly-to-client-components-unless-you-expli)

Author: [Rafał Kamiński](https://stackoverflow.com/users/6745425/rafa%c5%82-kami%c5%84ski)

Got this error message in Next.js but have no idea what to do with this. Next.js version 13.0.5.

I was passing a prop to a client component in Next.js. Prop is the list of objects, and one of the values is a function. But the question is, what this error message means?

> Error: Functions cannot be passed directly to Client Components unless you explicitly expose it by marking it with "use server"

How can I expose a function by marking it with "use server"?

```
matchesColumns.push({ field: 'pk', headerName: "", flex: 0.3, renderCell: (params, event) => (<Link href={`/matches/${encodeURIComponent(params.row.pk)}`}>Details</Link>) });
(...)
{<Tabela2 rows={matchesRows} columns={matchesColumns}/>}
```

***

Answered by: [Joonas](https://stackoverflow.com/users/13065068/joonas)

This is a new upcoming Next.js feature called server actions.

You can use server actions to pass async functions from **server** to **client** components while having them still be callable from client.

Here's an example:

```
// page.tsx

"use server";

import { ClientComponent } from './ClientComponent.tsx';

async function deleteItem(itemId: string) {
  "use server"; // mark function as a server action (fixes the error)

  // TODO add item deletion logic
  return null;
}

export function Page() {
  return <ClientComponent deleteItem={deleteItem} />
}
```

```
// ClientComponent.tsx

export function ClientComponent({ deleteItem }) {
  return (
    <button onClick={async () => {
      await deleteItem("foobar");
      alert("item has been deleted");
    }}>
      delete item
    </button>
  );
}
```

***

Answered by: [mahalingappa birajdar](https://stackoverflow.com/users/12297064/mahalingappa-birajdar)

If you encounter this error in a `error.(jsx|tsx)` file, note that the `error.(jsx|tsx)` files must be marked as a client component.

[Documentation reference](https://nextjs.org/docs/app/building-your-application/routing/error-handling)

***

Answered by: [FancyFinger](https://stackoverflow.com/users/19969106/fancyfinger)

***Unhandled Runtime Error Error: Functions cannot be passed directly to Client Components unless you explicitly expose it by marking it with "use server". <... src=... width={350} height={350} alt=... loader={function}>***

## Does your error look like this?

*note: this error did not occur when I used same methods @/components/Products.tsx, and imported a component named "ProductCard" inside it, it only happened when tried to do it in a dynamic page with imported component "singleProduct"> see codes below for details*

### TLDR:

**there was a component that would display a single product. That function was giving this error.** **Solution: "use client" where the error was occuring**

This **"SingleProduct"** component (which takes a prop) was called inside a page name **"ProductDetailView**" \[a dynamic route\] which by default should be server rendered , where the single product was fetched from api call.

After doing every thing else like enabling server action, I just wrote "use client" on the single product component and all error went way.

I believe mine happened because I was fetching the data in a dynamic page which was server side but the component was client side. But not sure. if any one know whats going on please let me know. \[btw I am noob\]

```
"dependencies": {
    "@radix-ui/react-dialog": "^1.0.4",
    "@radix-ui/react-navigation-menu": "^1.1.3",
    "@radix-ui/react-slot": "^1.0.2",
    "@types/node": "20.4.5",
    "@types/react": "18.2.17",
    "@types/react-dom": "18.2.7",
    "autoprefixer": "10.4.14",
    "axios": "^1.4.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.0.0",
    "eslint": "8.45.0",
    "eslint-config-next": "13.4.12",
    "lucide-react": "^0.263.1",
    "next": "13.4.12",
    "postcss": "8.4.27",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "tailwind-merge": "^1.14.0",
    "tailwindcss": "3.3.3",
    "tailwindcss-animate": "^1.0.6",
    "typescript": "5.1.6"
  }
```

All codes are as it is.

for ui > shadcn/ui *route > @/ProductDetailView/\[id\]/page.tsx*

```
// product component
// by deafult should be server

import { ProductProps } from "@/components/Products";
import axios from "axios";
import SingleProduct from "@/components/SingleProduct";


export async function getSingleProducts ( id: string ) {

    const res = await axios.get( `https://fakestoreapi.com/products/${ id }`, {
        // timeout after 5 seconds
        // signal: AbortSignal.timeout( 5000 ),
    } )
        .then( response => { return response.data } )
        .catch( err => alert( err ) )

    return res;
}

export default async function ProductDetailView ( { params }: { params: { id: string } } ) {

    const product: ProductProps = await getSingleProducts( params.id );

    return (
        <main className="text-center text-gray-200">
            <SingleProduct props={ product }></SingleProduct>
        </main>
    )
}

```

*route > @/components/SignleProduct*

```
// adding use client solves the issue.
"use client"
import { ProductProps } from "@/components/Products";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import Image from "next/image";

export default function SingleProduct ( { props }: { props: ProductProps } ) {


    const imgLink = ( src: string ) => {
        const image = src.substring( src.indexOf( "img" ) );
        return image
    }

    // beautifully parse it in a variable
    const imgSrc = imgLink( props.image );

    // now the loader
    // always destructure src or an object will be returned 
    const imageLoader = ( { src }: any ) => {
        const imgString = `https://fakestoreapi.com/${ src }`
        return imgString;
    }


    return (
        <main className="text-center text-gray-200">
            <Card>
                <CardHeader>
                    <CardTitle>{ props.title }</CardTitle>
                    <CardDescription>{ props.description }</CardDescription>
                </CardHeader>
                <CardContent>
                    <Image
                        src={ imgSrc }
                        width={ 350 }
                        height={ 350 }
                        alt={ props.title }
                        loader={ imageLoader }
                    >

                    </Image>
                </CardContent>
                <CardFooter>
                    <p>{ props.price }</p>
                    <p>{ props.category }</p>
                </CardFooter>
            </Card>

        </main>
    )
}
```

**The error did not happen when I did this.**

*route > @/component/Products*

```

// wanted to show all products here
import axios from "axios"
import ProductCard from "./ProductCard"

export type ProductProps = {
    id: number,
    title: string,
    price: number,
    category: string,
    description: string,
    image: string
}

export async function getProducts () {


    const res = await axios.get( "https://fakestoreapi.com/products", {
        // timeout after 5 seconds
        // signal: AbortSignal.timeout( 5000 ),
    } )
        .then( response => { return response.data } )
        .catch( err => alert( err ) )

    return res;
}

export default async function Products () {


    const products: ProductProps[] = await getProducts();

    return (
        <div>
            <h1 className="text-center text-3xl font-extrabold text-gray-50">
                Products Count : { products.length };
            </h1>

            <div className="m-5 grid grid-cols-2 gap-4 justify-center items-center">
                {
                    products.map( product => {
                        return (
                            <div key={ product.id } className="col-auto ">
                                <ProductCard props={ product }></ProductCard>
                            </div>
                        )
                    } )
                }
            </div>
        </div>
    )

}
```

**Product Card**

```

// this is product card

import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { ProductProps } from "./Products"
import Link from "next/link"
import Image from "next/image"


export default function ProductCard ( { props }: { props: ProductProps } ) {

    // an elaborated way to get an external image to display
    // if we do this then we don't need to add config inside next.config.js
    // first get the last part of the url as src

    const imgLink = ( src: string ) => {
        const image = src.substring( src.indexOf( "img" ) );
        return image
    }

    // beautifully parse it in a variable
    const imgSrc = imgLink( props.image );

    // now the loader
    // always destructure src or an object will be returned 
    const imageLoader = ( { src }: any ) => {
        const imgString = `https://fakestoreapi.com/${ src }`
        return imgString;
    }

    // clip the description

    const textClip = ( src: string ) => {
        const text = src.substring( 0, 100 );
        return text
    }


    //  parse it in a variable
    const textClipped = textClip( props.description );

    // clip the title

    const titleClip = ( src: string ) => {
        const title = src.substring( 0, 100 );
        return title
    }


    //  parse it in a variable
    const titleClipped = titleClip( props.title );

    return (

        <Card className="flex justify-center items-center h-[300px] bg-slate-950 text-slate-200">
            <CardContent className="flex justify-center items-center">
                <div className="w-auto h-auto pt-6">
                    <Image
                        loader={ imageLoader }
                        src={ `${ imgSrc }` }
                        alt={ props.title }
                        width={ 340 }
                        height={ 340 }
                        layout="responsive"
                        style={ { objectFit: "contain" } }
                    >

                    </Image>
                </div>
            </CardContent>
            <section className=" flex items-start justify-center flex-col">
                <CardHeader className="pb-1 pt-0">
                    <CardTitle className="text-start text-lg">

                        {/* <LinkIcon size={ 40 } spacing={ 10 }></LinkIcon> */ }

                        <Link href={ `/ProductDetailView/${ props.id }` } target="_blank">
                            <p>{ titleClipped }...</p>
                        </Link>

                    </CardTitle>
                    <CardDescription>{ textClipped }...</CardDescription>
                </CardHeader>
                <CardContent className="p-0 ps-6">
                    <p>Category: { props.category }</p>
                </CardContent>
                <CardFooter className="p-0 ps-6" >
                    <p>${ props.price }</p>
                </CardFooter>
            </section>
        </Card>

    )
}

```

***

Answered by: [kejiah](https://stackoverflow.com/users/21298768/kejiah)

Don't know if this would help anyone but i had a similar issues when trying to build my nextjs app (version 13.4.5) the issue was specifically this.

> Error: Functions cannot be passed directly to Client Components unless you explicitly expose it by marking it with "use server".

followed by some props in curly braces

> {parallelRouterKey: ..., segmentPath: ..., error: function, errorStyles: ..., loading: ..., loadingStyles: ..., hasLoading}

NOTE: i wasn't using server actions nor trying to implement it in any way beacause it was still in alpha testing as at time of writing this.

so i resolved the issue by making the error.tsx file in my root directory(the only error file in my project) a client component.

```
"use client"

const Error = ({ error, reset }: { error: Error; reset: () => void }) => {
  return (
    <div className=""></div>
       )
}
```

***

Answered by: [Thuong Vu](https://stackoverflow.com/users/19193340/thuong-vu)

Here's my example:

```
// components/form.tsx
'use client';
import { useState } from "react"

export default function Form(props: { action: Function, className?: string }) {
    const { action, className } = props;
    const [value, setValue] = useState('');
    return (
        <form className={`${className} flex flex-col mb-4 p-10`} onSubmit={(e) => {
            e.preventDefault();
            action(value);
        }}>
            <input className="block w-full px-3 py-2 text-lg border border-green-500 bg-gray-50"
                type="text"
                placeholder="Type anything!"
                value={value}
                onChange={(e) => {
                    setValue(e.target.value);
                }}
            />
        </form >
    )
}
```

and

```
// app/page.tsx
import Form from "@/components/form";

export default async function Home() {
  const formAction = async (data: string) => {
    'use server';
    console.log(data);
  }
  return (
    <main className="w-full h-screen bg-white">
      <Form action={formAction} className="max-w-2xl mx-auto"></Form>
    </main>
  )
}
```