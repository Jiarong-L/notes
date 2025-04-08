

直接返回JSX，所以或许更适合较简单的网站？

其它前端框架：[React（直接返回JSX）](./React.md)，[Svelte（简洁易用）](./Svelte.md)

后端框架：[Express (NodeJS)](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Extensions/Server-side/Express_Nodejs)/Django/Flask/SpringBoot/...

## 关于 node

[国内建议使用 n 进行安装](https://nodejs.org/en/download)，需要 sudo，若有旧版本需要手动删除

npm 是 Node.js 的包管理器，[npx 是运行器](https://dev.nodejs.cn/learn/the-npx-nodejs-package-runner/)

```npm install xxx``` 进行本地安装（加```-g```则全局安装），本地安装的依赖声明见每个项目的 package.json 文件



## 创建 React 项目

```bash
npm install create-react-app     ## 本地安装 React 
npx create-react-app myapp       ## 创建项目
cd myapp
npm i --save-dev @types/react
npm start                        ## 运行项目
```

随后，编辑 src 文件夹中的 .js 文件（每个文件即一个组件）

其中，src/App.js 是根组件 ```<App />```，从它开始一层层包含其余子组件

组件可以视为一个JSX模板，接收父组件的 Props（不可更新）、State（可变值）、...


### Props 父-->子

关于组件的格式：其中 className 建议如此取名，以便进行 CSS 设置

```js
import React, { use... } from 'react';
import Child from './Child_Component';  // 假设 Child_Component.js 中的 function Child() 被 export

function MyComp(props) {
    const kidage = 12    // JS here for logics & value settings
    return (        // JSX  here as Outputs
        <div className="MyComp-Container">
            <Child name='Ann' age={kidage} /> 
            <p>{props.valueA}</p>
        </div>
    )
}

export default MyComp;   
```

MyComp（父组件）向 Child（子组件）传递了 ```{name, age}``` 两个 props，Chind 中调用即 ```props.age```(见下)

**子-->父** 只能：父分享 State，子 Set State，然后才能作为 props 由父分享给其它子节点 **(HOW???)**


### useState

```useState(init)```会返回 ```[var, setVarFunc]```，常见的初始值为 0 或者 false

```js
import React, { useState } from 'react';

function Child(props) {                     // 或者直接  Child({name, age})
    const [isLiked, setIsLiked] = useState(false)
    return (  
        <div className="Child">
            <p>Child Name is {props.name}</p>
            <p>Age is {props.age}</p>
            <button onClick = {() => {setIsLiked(!isLiked);}}> This kid {isLiked ? "Likes":"Dislikes"} Tomato   </button>
        </div>
    )
}

export default Child;   
```

State Change = Trigger + Render + Commit，故而一定不能直接 assign V=V+1 --- not persist（Render Phase 会刷新？），而是使用对应的 **setV(V+1) --- 但ASYNC也会带来问题，故而需要useEffect**


### useEffect

监控某个变量的变化，然后做点什么


```js

function ChatRoom({ roomId }) {
    //
    const MyFunc = () => { console.log('Do Something'); }  //  一般是 get("/api/xxx").then(onSucc)

    useEffect(MyFunc, [varA,roomId]) // 每当 varA 或 roomId 变化时，call MyFunc --- 注意：Effect 代码中使用的每个 响应式值 都必须声明为依赖项
    useEffect(MyFunc, [])            // ChatRoom 组件第一次被 Render 时（即 on mount），call MyFunc
    useEffect(MyFunc)                // ChatRoom 组件每次被 Render 时，call MyFunc
    return ()
}

```

### Router

App/Home/... 的 JSX 中指定 route_path 以及对应的组件，然后可以在导航栏以 link 的形式指向这些 URL = base_URL + route_path


有各种包/版本：[npx create-react-router](https://reactrouter.com/start/framework/routing)，[@reach/router](https://reach.tech/router/)，[React Router](https://react-guide.github.io/react-router-cn/docs/guides/basics/RouteConfiguration.html) --- 一般需要额外从npm进行安装


## 参考

[React 前端框架全面教程](https://blog.csdn.net/m0_70474954/article/details/143259099)

[子-->父](https://juejin.cn/post/7216182414710784037)

[useEffect - React 中文文档](https://zh-hans.react.dev/reference/react/useEffect)
