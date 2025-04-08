

[Svelte](https://svelte.yayujs.com/docs/svelte/overview)是一款简洁的前端框架，推荐使用，[视频教程](https://www.bilibili.com/video/BV14aHvesE35/?p=34)


## 简单示例

安装官网教程，```npx sv create myapp``` 创建项目，

```
┌  Welcome to the Svelte CLI! (v0.8.0)
│
◇  Which template would you like?
│  SvelteKit minimal
│
◇  Add type checking with TypeScript?
│  No
│
◆  Project created
│
◇  What would you like to add to your project? (use arrow keys / space bar)
│  none
│
◇  Which package manager do you want to install dependencies with?
│  npm
│
◇  Installing dependencies with npm...
```

进入myapp文件夹后，```npm install``` 安装依赖项，```npm run dev```运行项目

.svelte 包括: ```<style>  <script>  html``` 三部分，和大部分前端框架类似


## 对比 React

Svelte 的操作十分简洁，[项目结构](https://svelte.yayujs.com/docs/kit/project-structure)

模板语法：例如，使用 [```{#each arr as item}...{/each}```](https://svelte.yayujs.com/docs/svelte/each) 处理 arr/obj 的显示与传值（recall: JS扩展运算符 ```{...arr}```）


### Routing

React 需要安装各种外置的 Route 包，声明 组件-Url 的对应关系，但 Svelte 可用文件夹名作为 Route:

```
myapp/src
├── app.html
├── lib
│   └── index.js
└── routes
    ├── +layout.svelte
    ├── +page.svelte              http://localhost:5175/
    └── pathA
        └── +page.svelte          http://localhost:5175/pathA
```

* ```+page.svelte``` 文件即主页内容
* ```+layout.svelte``` 文件中的内容会加入同目录&子目录的 page.svelte 中，建议在此处设置 CSS style & 导航栏，示例：

```
<script>  import AsNavbar from '../lib/Navbar.svelte' </script>
<AsNavbar/>

You can write or import CSS/Script/HTML here or in ../lib/xx.svelte,
'<slot />' is left for contents in +page.svelte

<slot />
```


### [State](https://svelte.yayujs.com/docs/svelte/$state)

React 需要 useState 才能

```js
import React, { useState } from 'react';

function CountClick() {                   
    const [count, setcount] = useState(0)
    return (  
        <div>
            <h1>{count}</h1>
            <button onClick = {() => {setcount(count + 1);}}>Click</button>
        </div>
    )
}

export default CountClick;   
```


```+page.svelte``` 只需要 

```js
<style> </style>

<script module>
	let count = $state(0);
</script>


<h1>{count}</h1>
<button onclick={ ()=> count++}>Click</button>
```

### [Props](https://svelte.yayujs.com/docs/svelte/$props)

父->子传值方法同 React，传递 ```{name, age}``` 两个 props：

```js
<Child name='Ann' age={kidage} /> 
```

接收方式略有不同，React 只需在定义方程时 ```function Child({name, age})``` 即可，svelte 需要 let：

```js
<script>
	export let name;
    export let age;
    // export let { name, age } = $props()    // props.name
</script>

<p>Data from parent page: {name}, {age}</p>
```

注意了，上例中，无论 React 还是 svelte，子组件在接收 props_obj 的时候都是按其顺序给自己的变量进行赋值，因此需注意顺序


子<->父传值可[声明 $bindable](https://svelte.yayujs.com/docs/svelte/$bindable): (Child)```export let value = $bindable()```, (Parent)```<Child bind:value={message} />```


## [global store](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Core/Frameworks_libraries/Svelte_stores)

```
Props 只能一层一层传值/回溯:    CompA <-->  CompB <-->  CompC <--> CompD

                                                Store
                                   |——————————|——————————|——————————|              
Store(Props) 可以从中心存取值:    CompA <-->  CompB <-->  CompC <--> CompD
```


在 ```../lib/alert.js``` 中创建一个 全局变量 'alert'

```js
import { writable } from "svelte/store";
export const alert = writable("Old Value");
```

各个页面都可调用、修改这个 global store 变量

```js
<script>
import { alert } from '../lib/alert.js'
alert.update(  (oldVal) => {return oldVal + ' to new Value'}  )
</script>

Example: {$alert} 
```

global store 变量可以是各种格式：数字/列表/obj/...，对应着各自的 update 方法

