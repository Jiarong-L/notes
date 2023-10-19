
node.js 是跨平台的 JacaScript 运行环境


[官网下载安装：nodejs.org](https://nodejs.org/en)

## 基础示例

准备一个文件：test.js
```js
console.log('Hello Node')
```
命令行运行：
```bash
node test.js
```

nodemon 每一次保存后自动实时运行：（```npm i nodemon```）
```bash
nodemon test.js
```

## Web Server 示例
准备一个文件：web.js
```js
const http = require('http') 

const server = http.createServer(
    (req,res) => {      //（请求对象，响应对象）
        console.log(req.url)  // 相对路径，根目录为'/'
        res.setHeader('Content-Type','text/plain;charset=utf-8')
        if (req.method === 'GET') {
            res.end('GET: Response Info')
        } else if (req.method === 'POST') {
            let body = ''
            req.on('data', chunk=>{    // 内置的'data'事件，接收分段传输的req数据（一般res.on以将res内容准备完毕，此处举例用）
                console.log('---Adding chunks to body-------') // 此例中data-Event未被激发
                body += chunk; 
            })
            req.on('end',()=>{        // 内置的'end'事件，req数据传输完成后激发
                console.log('---data-Event-End-------body: ' + body)
                res.write('POST: Response Info')
                res.end()
            })
        } else {
            res.statusCode = 404
            res.end('Method '+ req.method)
        }
    }
)

server.listen(3000, ()=>{
    console.log('Port 3000: Server is running')
})
```
node 运行 web.js 后通过浏览器/Postman访问:
* ```http://localhost:3000/```


另： URL + querystring 可以parse url数据

## NPM
npm是node.js的装包工具，示例：安装 vue cli
```bash
npm install @vue/cli 
npm i @vue/cli         // 在当前项目目录下安装@vue/cli
npm i @vue/cli -g      // 在node全局安装@vue/cli
```
随后使用vue/cli生成项目 ```vue create myproj``` ，进入项目目录后可运行:
```bash
npm run serve   // 打开静态资源服务器，本地运行项目
npm run build   // 生成以'/'为根目录的打包文件夹 dist
npm run lint    // 修复错误的配置
```
打包文件夹 dist 不能直接打开，需要安装serve [```npm i serve -g```]，然后运行 ```serve dist```

