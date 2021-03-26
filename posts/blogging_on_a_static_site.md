---
index: 2
title: "Adding a blog to a static site"
excerpt: "I decided to add a blog to my portfolio. Turns out adding one to a statically published site is somehow both easier and simultaneously more difficult than you would think."
publicationDate: "2020-08-05"
slug: blogging_on_a_static_site
tags:
- portfolio
- blog
- GitHub
---

# Blogging on a static site

I decided to add a blog to my portfolio. Turns out adding one to a statically published site is somehow both easier and simultaneously more difficult than you would think.
<!--more-->

Let me start with a little bit of background. My [portfolio website of old](https://vjs.dhruvkb.now.sh), the one I built way back in 2016, contained an interactive terminal. You could navigate the site using keyboard-issued commands. If you wanted to read about me, you could `cat` a file. There was no real file-system backing the terminal, it was emulated some fancy JavaScript that I will get to in a future blog post. Every `cat` command triggered an `XMLHttpRequest` to fetch an HTML page from the host, the contents of which were inserted into the page.

When I updated [my portfolio](https://dhruvkb.github.io) to a modern frontend stack, I wanted it to have a blog but I also wanted to stick to the static nature of my site. Static sites are awesome for many many reasons, another blog post for the future, and I had not the slightest intention of compromising on any bit of that goodness.

So let's take a look at my approach to create a blogging workflow that powers my website. This approach allowed me to retain the statically compiled nature of the site while allowing me to write blog posts identical to the way I write code.

Do note that the code given here highlights the most important and interesting parts of the application. There are many more aspects to it that I cannot fully cover here. To understand it fully, please read the [source code](https://github.com/dhruvkb/portfolio) on GitHub. I assure you it is as well-documented as this blog post.

## 1. Repository structure

As I developer I instinctively Git-track all my projects. Any time I initialise a project, my first course of action is to initialise a Git repo with it. There is simply no denying the role of a VCS in tracking, hosting and deploying software. But what about a blog; are blog posts really that different from code? In other words, do you need a CMS? Do the rules that apply to code translate successfully to blog posts?

Well yes, but actually no. There are some tradeoffs for not using a CMS, such as the lack of a GUI, no SEO, no plugins or themes, but I don't care about any of that. I'd be more than happy to write blog posts from my IDE, my portfolio site is already adequately SEO-optimised and I have painstakingly styled it from the ground up with Sass. I'm more than willing to make this trade-off and I assume many others would be in the same boat as I am.

To start, I made a new repository on GitHub, named it `portfolio-blog` and placed my posts in a `posts/` directory. Each post has a name that matches the post slug. So my previous post, "Easy on the eyes" is contained in `posts/easy_on_the_eyes.md`. This post is `blogging_on_a_static_site.md` and so on. The content of a post file looks like this:

```markdown
---
index: 1
title: "Easy on the eyes"
excerpt: "Making a portfolio is hard. Making it a beauty to look at is harder. Making it literally easy on the eyes is an art. But art doesn't have to be hard."
publicationDate: "2020-07-05"
slug: easy_on_the_eyes
tags:
- portfolio
- colours
- Solarized
---

<!-- posts/easy_on_the_eyes.md -->
# Easy on the eyes
...
```

The thing you see before the actual Markdown content of the blog post is front-matter. Front-matter, popularised by Jekyll, is a block of YAML that gives extra information about the Markdown file. It's not hard to see what my front-matter is doing here. The front-matter is dropped from the Markdown file before it is rendered to HTML.

Each post has a corresponding metadata JSON file (made from the same front-matter) located in the `metadata/` directory on the `metadata` branch.

```json
{
  "_comment": "metadata:metadata/00001.json",
  "index": 1,
  "title": "Easy on the eyes",
  "excerpt": "Making a portfolio is hard. Making it a beauty to look at is harder. Making it literally easy on the eyes is an art. But art doesn't have to be hard.",
  "publicationDate": "2020-07-05",
  "slug": "easy_on_the_eyes",
  "tags": [
    "portfolio",
    "colours",
    "Solarized"
  ]
}
```

I don't manually write this JSON. It's part of my build pipeline, which I'll cover in a [future blog post](https://dhruvkb.github.io/#/blog/post/push_and_its_live).

## 2. Serverless functions

I stumbled across [these serverless functions](https://vercel.com/docs/v2/serverless-functions/introduction) in the Vercel docs. Serverless functions are kind of like a server in that they respond to your HTTP requests with an HTTP response but that's where the similarities end. You don't have access to a computer. You can't write to a database. You can't access a file-system. But since you can run server-side code, it opens a whole world of possibilities.

We are going to be using the GitHub API to get the blog information from the repository. For the little bit of processing that is to be done on these posts, we need to use serverless functions. Having a static site does not have to be the death of remote publishing after all.

Let's see a serverless function in action. Vercel allows you to place your serverless functions in an `api/` directory and it generates the endpoints automatically. For example, if you navigate to [the root of my API](https://api.dhruvkb.now.sh/api), you get the following JSON response.

```json
{
  "message":"Hello, World!"
}
```

The backend for this is a fairly small serverless function written in TypeScript.

```typescript
// api/index.ts
import { NowRequest, NowResponse } from '@vercel/node'

const logic = (name: string, res: NowResponse): void => {
  res.status(200).json({
    message: `Hello, ${name}!`
  })
}

export default (req: NowRequest, res: NowResponse): void => {
  let { nameQuery = 'World' } = req.query
  if (Array.isArray(nameQuery)) {
    nameQuery = nameQuery.join(' & ')
  }

  const name = nameQuery

  logic(name, res)
}
```

Note how I extract the business logic of the function into `logic()` while keeping the plumbing in the main function. This is followed in the other examples as well, although I won't repeat the plumbing portion again and again. Similar to this example, we create the following endpoints. There are some `_utils` directories containing auxiliary files that act as helpers to the main API.

- `api/`
  - `_utils/`
  - `blog_posts/`
    - `_utils/`
    - `index.ts`: get a list of blog posts
    - `[slug].ts`: get the content of a specific blog post
  - `index.ts`: the above 'Hello, World!' endpoint

Vercel generates the paths to the different endpoints based on the folder structure of the API directory. So the `index.ts` in the root folder would be served at [`/api`](https://api.dhruvkb.now.sh/api) and the `index.ts` in the `blog_posts/` folder would be served at [`/api/blog_posts`](https://api.dhruvkb.now.sh/api/blog_posts).

Vercel also allows parameters in the file name, so the `[slug].ts` file in blog posts allows any string to be used in the path, such as [`/api/blog_posts/easy_on_the_eyes`](https://api.dhruvkb.now.sh/api/blog_posts/easy_on_the_eyes) and provides that parameter to the serverless function as an argument.

## 3. Building the API

GitHub API version 4 is built on GraphQL. The [documentation](https://docs.github.com/en/graphql) is terrible and severely lacking to be honest but, for the most part, it's usable and for our small purpose, which is just accessing files and their content, the documentation comes through.

You do need to be authorised to to use the API though. You can [obtain a personal authentication token](https://docs.github.com/en/graphql/guides/forming-calls-with-graphql#authenticating-with-graphql) from your GitHub account settings and then use it as a bearer token in the `Authorization` header.

The best way to explore their API is to play around with in in [GitHub's GraphQL explorer](https://developer.github.com/v4/explorer).

Since we're using TypeScript, let's start by defining some types in a separate file. The first type we need is the interface `Repository`, each instance of which will be an owner-name pair like `'dhruvkb'` and `'portfolio-blog'`.

```typescript
// api/_utils/types.ts
export interface Repository {
  owner: string,
  name: string
}
```

Since we're using GraphQL it also helps to define the request payload type. Each GraphQL request has two parts, a query with placeholders and a dictionary of variables that map these placeholders to actual values. Since the shape of the variables is not fixed, we use generics to allow the variable interface to be set dynamically.

```typescript
// api/_utils/types.ts
import { RequestParameters } from '@octokit/graphql/dist-types/types'

export interface Payload<Variables extends RequestParameters> {
  query: string,
  variables: Variables
}
```

Let's set up some constants. We'll be needing the GitHub personal access token so we'll load it in from the environment constants and then create an authenticated Octokit client with which to access the API.

```typescript
// api/_utils/github.ts
import { graphql as octokit } from '@octokit/graphql'

import { Repository } from './types'

const githubToken: string | undefined = process.env.GITHUB_PERSONAL_ACCESS_TOKEN
if (githubToken === undefined) {
  throw 'GitHub token is undefined!'
}

export const repository: Repository = {
  owner: 'dhruvkb',
  name: 'portfolio-blog',
}

export const client = octokit.defaults({
  headers: {
    Authorization: `Bearer ${githubToken}`
  }
})
```

Any call to the GitHub API's using the client is structured like this:

```javascript
// api/blog_posts/*.ts
import { repository, client } from '../_utils/github'

const payload = {
  query,
  variables: {
    repoOwner: repository.owner,
    repoNmae: repository.name,
    objExpression: '' // see the examples below
  }
}

const data = await client(payload.query, payload.variables)
```

Here I've omitted the TypeScript type hints, as this is a generalised example. We will import and use the authorised GitHub client we created earlier.

The way GraphQL works is that the variables defined in the `variables` dictionary will be used to populate the corresponding variable-placeholders in the `query` string.

- `repoOwner`: would be an organisation or user handle, like `'dhruvkb'`
- `repoName`: would be the name of the repository, like `'portfolio-blog'`
- `objExpression`: would be branch and path to a folder or file

The structure of your JSON response will be the exact same as your query requested so you can just ask for the data you need and then consume all the data you get.

### 3.1. Setting up

Since the entire purpose of the `blog_posts` app in the API is to deal with blogs, we can not make do without setting up the `Post` interface.

```typescript
// api/blog_posts/_utils/types.ts
export interface Post {
  index: number,
  title: string,
  excerpt: string,
  publicationDate: {
    absolute: string,
    relative: string
  } | string, // we parse the string `publicationDate` into an object
  slug: string,
  tags: string[],
  urls?: {
    api: string,
    portfolio: string
  } // we add `urls` during processing
}
```

We should also define the `Variables` type to represent the variables that we will be sending on the requests. Since we're using a very similar query structure for both requests, they can share this interface.

```typescript
// api/blog_posts/_utils/types.ts
import { RequestParameters } from '@octokit/graphql/dist-types/types'

export interface Variables extends RequestParameters {
  repoOwner: string,
  repoName: string,
  objExpression: string
}
```

The next thing of note is the separation of logic from plumbing. Since we're `await`ing calls to the Octokit client, we need to modify the signature the logic function as follows. Also making it `async` has the consequence of having to make the default export `async` as well.

```typescript
import { NowRequest, NowResponse } from '@vercel/node'

const logic = async (args: any, res: NowResponse): Promise<void> => {
  // ...
}

export default async (req: NowRequest, res: NowResponse): Promise<void> => {
  // ...
  const args = [] // Prepare arguments
  await log(args, res)
}
```

### 3.2. Getting a list of blog posts

The first endpoint that we need to check out is one that gives us a list of all files in a given directory on a given branch. Using this endpoint we can get a list of all metadata files, and their JSON content, in the `metadata/` directory on the `metadata` branch, which we can then parse in JavaScript and generate a list of blog posts.

Based on the behaviour we want from this endpoint, our endpoint accepts a `number` offset and a `number` count and returns the post count and information of every post in the specified range.

```typescript
const logic = async (offset: number, count: number, res: NowResponse): Promise<void> => {
  // ...
  res.status(200).json({
    totalCount,
    posts
  })
}
```

Let's define the interfaces relevant to this API query. These would be `Entry` and `List`. The `List` interface represents the outcome of the list query as returned by Octokit and must align with the GraphQL query used in the request.

```typescript
// api/blog_posts/_utils/types.ts
export interface List {
  repository: {
    tree: {
      entries: Entry[]
    }
  }
}

export interface Entry {
  name: string,
  file: {
    text: string
  }
}
```

We can then use these interfaces in the actual script corresponding to the endpoint. All of the following content goes inside the `logic()` function. See the [code for the `blog_posts/index.ts` endpoint](https://github.com/dhruvkb/portfolio-api/blob/master/api/blog_posts/index.ts).

```typescript
// api/blog_posts/index.ts
import { repository, client } from '../_utils/github'
import { Payload } from '../_utils/types'
import { Variables, Entry, List, Post } from './_utils/types'

const payload: Payload<Variables> = {
  query: `
    query($repoOwner: String!, $repoName: String!, $objExpression: String) {
      repository(owner: $repoOwner, name: $repoName) {
        tree: object(expression: $objExpression) {
          ...on Tree {
            entries {
              name
              file: object {
                ...on Blob {
                  text
                }
              }
            }
          }
        }
      }
    }
  `,
  variables: {
    repoOwner: repository.owner,
    repoName: repository.name,
    objExpression: `metadata:metadata`
  }
}
```

You make the request to the GraphQL endpoint and your response will fit neatly into the `List` interface we defined earlier.

```typescript
// api/blog_posts/index.ts
const { repository: { tree: { entries } } }: List = await client(payload.query, payload.variables)
```

We sort the files in reverse order of index, because the last one published is the one that should be at the top. Then we cut off the last entry, for Easter egg purposes. We slice the list for pagination. Then, for each of the posts, we parse the text field as JSON and get the slug, which we use to make URLs from. We ultimately return all this data to the frontend.

```typescript
// api/blog_posts/index.ts
const totalCount = entries.length - 1 // Hide blog post #0
const posts = (entries)
  .sort((a: Entry, b: Entry): number => -a.name.localeCompare(b.name))
  .slice(offset, Math.min(offset + count, totalCount))
  .map(entry => {
    let post: Post = JSON.parse(entry.file.text)
    // Process `post` as Post
    return post
  })
```

### 3.3 Getting the content of a specific blog post

The second endpoint that we need to check out is one that gives us the content of any specific file. Using this endpoint we can get the body of a post (whose slug is known to us) from the `posts/` directory on the `master` branch. We can parse the Markdown contained in it to generate the HTML for the post.

Based on the behaviour we want from this endpoint, our endpoint accepts a `string` slug and returns the attributes and body of the post referenced by the slug.

```typescript
const logic = async (slug: string, res: NowResponse): Promise<void> => {
  // ...
  res.status(200).json({
    attributes,
    body
  })
}
```

Let's define the interface relevant to this API query. This would be `Retrieve`, which represents the outcome of the retrieve query as returned by Octokit and must align with the GraphQL query used in the request.

```typescript
// api/blog_posts/_utils/types.ts
export interface Retrieve {
  repository: {
    file: {
      text: string
    }
  }
}
```

We can then use this interface in the actual script corresponding to the endpoint. All of the following content goes inside the `logic()` function. See the [code for the `blog_posts/[slug].ts` endpoint](https://github.com/dhruvkb/portfolio-api/blob/master/api/blog_posts/[slug].ts).

```typescript
// api/blog_posts/[slug].ts
import { repository, client } from '../_utils/github'
import { Payload } from '../_utils/types'
import { Variables, Retrieve, Post as Attributes } from './_utils/types'

const payload: Payload<Variables> = {
  query: `
    query($repoOwner: String!, $repoName: String!, $objExpression: String) {
      repository(owner: $repoOwner, name: $repoName) {
        file: object(expression: $objExpression) {
          ...on Blob {
            text
          }
        }
      }
    }
  `,
  variables: {
    repoOwner: repository.owner,
    repoName: repository.name,
    objExpression: `master:posts/${slug}.md` // `slug` is supplied as a parameter
  }
}
```

This one needs a little bit more processing and two external libraries. We're using [`gray-matter`](https://github.com/jonschlinkert/gray-matter) to extract the front-matter from the posts and parse it, followed by [`markdown-it`](https://github.com/markdown-it/markdown-it) to convert the post Markdown to HTML.

```typescript
// api/blog_posts/[slug].ts
import frontMatter from 'gray-matter'
import MarkdownIt from 'markdown-it'
```

You make the request to the GraphQL endpoint and your response will fit neatly into the `Retrieve` interface we defined earlier.

```typescript
// api/blog_posts/[slug].ts
const { repository: { file: { text } } }: Retrieve = await client(payload.query, payload.variables)
```

```typescript
// api/blog_posts/[slug].ts
let { data: attributes, content: body } = frontMatter(text)
// Process `attributes` as Attributes
body = markdownIt.render(body)
```

That's all there is to it. I'll not go over the frontend aspects of this because that is boilerplate code to make request to an API that returns HTML and then inserting that into the DOM using `v-html`.

## 4. Portfolio series

This post is part three of my series covering my [new portfolio website](https://dhruvkb.github.io/).

1. [Easy on the eyes](https://dhruvkb.github.io/#/blog/post/easy_on_the_eyes)
2. Blogging on a static site
3. [Push and it's live](https://dhruvkb.github.io/#/blog/post/push_and_its_live)
4. [Back to the future](https://dhruvkb.github.io/#/blog/post/back_to_the_future)

For the tech-savvy, the [open-source, well-documented code](https://github.com/dhruvkb/portfolio) powering my portfolio is available on GitHub. I'm sure that you can either learn something from it or teach me something about it so please reach out!

Hope you enjoyed reading this. Till next time!

~ @dhruvkb