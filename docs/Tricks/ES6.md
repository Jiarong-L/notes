
ES6是JavaScript的下一个版本标准，与ES5版本（目前浏览器确定支持）相比引入了一些新特性  

JS基础笔记见: [JS](./JS.md)  
Demo代码：[ES6demo.zip](./JS/ES6demo.zip)

TBA: 异步、await的mdn文档尚未看完

## 常用功能

### 声明&块作用域

| 声明 | 作用域 |
| -- | -- |
| var | 全局；变量 |
| let | 块作用域内；变量 |
| const | 块作用域内；常量 <br> const a = 'a' 不可修改 a = 'c' <br> const obj = {a:'a'} 可修改 obj.a = 'c' |

块作用域```{}```示例:
```js
{
    // var myNum = 8
    // let myNum = 8
    // const myNum = 8
}

console.log(myNum) // let，const 块作用域外不能访问
```


使用var声明变量时可能会失手覆盖/修改，使用let/const声明可以限制其作用域


### 模板字符串
使用反引号\`${}\`，反引号内支持换行
```js
const str1 = 'abc'
const str2 = `def
${str1}
`
console.log(str2)
```


### 解构赋值
可以很方便地将数据赋给常量/变量，简化代码；  
数组依次赋值，```...restVar```表示余下的值都丢给restVar
```js
const [a,b,c,...restVar] = [1,2,3,4,5,6]
console.log(a,b,c,restVar)  // 1,2,3,[4,5,6]
```
obj需要对应数据内的属性名称，但可以通过```oldVar:newVar```来重新命名
```js
const {user,No:Number,...restInfo} = {
    user: 'U1',
    No: '001',
    depart: 'D1',
    site: 'SH'
}
console.log(user,Number,restInfo)
```

### 扩展(...)
数组
```js
arr1 = [1,2,3]
arr2 = [4,5,6]
arr3 = [...arr1,...arr2,7,8,9]
console.log(arr3)
```

对象
```js
obj1 = {a:1}
obj2 = {b:2}
obj3 = {
    c:3,
    ...obj1,
    ...obj2
}
console.log(obj3)
```

### 伪数组
伪数组具备数组的一些功能（长度，下标访问..）但不具备方法（forEach,push..）；  
例如:伪数组```arguments```表示当前传入function的所有实参，需要```Array.from(arguments)```实现forEach方法（push之类的虽然不报错但也没用）
```js
function fn () {
    console.log(arguments)
    //arguments.forEach( (item) => {console.log(item)})  // 伪数组，不能执行
    Array.from(arguments).forEach( (item) => {console.log(item)})
}
fn(1,2,3)
```

### Object浅拷贝

* 浅拷贝：共用一个内存地址，对象的变化相互影响
* 深拷贝：将新对象放到新的内存中，对象的变化不会相互影响

下例中，将```objA,objB,objC```的feature全合给```{}```后赋予```objAll```；**如果存在同名属性，则后面的属性会覆盖前面的属性。(?)**
```js
objAll = Object.assign({},objA,objB,objC)
```



注意，当属性为简单数据类型时(string/number..)，其实进行了深拷贝
```js
objA = {a:1}
objB = {b:2}
objC = {c:3}
objAll = Object.assign({},objA,objB,objC)

objA.a = 100  
console.log(objAll)  // still 1
```

当属性为引用类型时(Object..)，进行的是浅拷贝
```js
objA = {a:{Aa:1}}
objB = {b:2}
objC = {c:3}
objAll = Object.assign({},objA,objB,objC)

objA.a.Aa = 100  
console.log(objAll)  // changed to 100
```


### Class
要素：constructor，自定义函数，继承，override
```js
class A {
    constructor (var1,var2) {
        this.var1 = var1
        this.var2 = var2
    }
    logVar1() {
        console.log(this.var1)
    }
    logVarAll() {
        console.log(this.var1,this.var2)
    }
}

class B extends A {
    constructor (var1,var2,var3){
        super(var1,var2)
        this.var3 = var3
    }
    logVarAll() {
        console.log(this.var1,this.var2,this.var3)
    }
}

const b1 = new B('aa','bb','cc')
b1.logVar1()         //'aa'
b1.logVarAll()       //'aa','bb','cc'
```

### 箭头函数
可以简化function的写法或匿名方程；左侧输入、右侧输出/步骤
```js
() => {alert('empty func')}

(n) => {return 2n+1}
n => 2n+1


const arrFunRes = n => 2n+1
arrFunRes(2)  //5
```


## 异步(TBA)
JS中先执行完同步任务后再执行异步任务队列。常见的异步：Timer，Ajax  

本例主要是为了确保成功执行的顺序，i.e.事件B要在事件A成功后才能执行

### [Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)
* [Promise.reject()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise/reject): 返回一个已拒绝（rejected）的 Promise 对象
* [Promise.resolve()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise/resolve): 将给定的值转换为一个 Promise。如果该值是一个 thenable 对象，将调用其 then() 方法；否则，返回的 Promise 将会以该值兑现。
* [Promise.prototype.then()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise/then): 用于 Promise 兑现和拒绝情况的回调函数
* [Promise.prototype.catch()](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise/catch): 用于注册一个在 promise 被拒绝时调用的函数  


简单使用
```js
function onSucc () {console.log('Succ')}
function onFail () {console.log('Fail')}

const p1 = Promise.resolve()  // 'Succ' 'Succ' 'Succ'
.then(onSucc).then(onSucc).then(onSucc).catch(onFail)

const p2 = Promise.reject()   // 'Fail'
.then(onSucc).then(onSucc).then(onSucc).catch(onFail)
```
Promise.resolve()相当于
```js
const p1 = new Promise((resolve,reject)=>{
    resolve()
}).then(...).catch(...)
```


**似乎**(?)如果使用catch(onFail)，then序列中有一次失败就会结束(不再返回Promise，哪怕onFail返回Promise)；不过如果改用then(onSucc,onFail)则可以继续then
```js
function onSucc () {
    console.log('Succ')
    return Promise.reject()
}
function onFail () {
    console.log('Fail')
    return Promise.resolve()
}

// 'Fail'
const p1 = Promise.reject().then(onSucc).then(onSucc).then(onSucc).catch(onFail)
// 'Fail'  'Succ'  'Fail'
const p2 = Promise.reject().then(onSucc,onFail).then(onSucc,onFail).then(onSucc,onFail).catch(onFail)
```


### [Async](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Statements/async_function)
异步处理的语法糖，无需刻意地链式调用 promise。  
```js
function asyncTask () {
    console.log('Doing asyncTask')
    setTimeout(() => {console.log('Finish asyncTask')}, 2000)
}

async function asyncMain () {
    console.log('Start asyncMain')
    asyncTask()  //await asyncTask() doesn't waiting!!
    asyncTask()  //await asyncTask() doesn't waiting!!
    console.log('End asyncMain')
}
p1 = asyncMain()  //p1是Promise对象

//Start asyncMain
//Doing asyncTask
//Doing asyncTask
//End asyncMain
//Finish asyncTask
//Finish asyncTask
```

### [await](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/await)

await用于等待一个异步操作完成后再运行余下代码

```js
// 1.准备一个返回Promise对象的函数
function asyncTask (ms) {
    console.log('Doing asyncTask' + ms)
    return new Promise((resolve) => {setTimeout(() => {resolve('Succ asyncTask' + ms)}, ms)})
}

// 2. async + await
async function asyncMain () {
    console.log('Start asyncMain')
    console.log(await asyncTask(6000))
    console.log(await asyncTask(1000))
    console.log('End asyncMain')
}
asyncMain()

//Start asyncMain
//Doing asyncTask6000
//Succ asyncTask6000
//Doing asyncTask1000
//Succ asyncTask1000
//End asyncMain
```


## [Proxy](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Proxy)
当某个值需要伴随着另一个值更新时；```Proxy(target,handler)```，target必须是object
```js
const handler = {
    get: function (obj, prop){return obj[prop]},
    set: function (obj, prop, val){obj[prop]=val}
}
const myobj = {a:'a'}
const p1 = new Proxy(myobj, handler)

console.log(p1.a)       //a
p1.a = 'b'
console.log(myobj.a)    //b
myobj.a = 'c'
console.log(p1.a)       //c
```

## Module
当代码多的时候，把一些一块儿用的方程或者变量放在同一个js文件里，其它
### ESM
* 适用于浏览器 

M1.js中：
```js
export const str1 = 'M1'
export function FuncM1 () {
    console.log('FuncM1')
}
export default {       //default 只能导出一种
    name: 'M1 Name'
}
```

随后在另一个js文件中import、使用它们；例如，ES6demo.js中：
```js
import module1 from './M1.js'  //module1就是default，即'M1 Name'
import {str1,FuncM1} from './M1.js'
console.log(xxxDefault)
```

对于import module的js文件，html中其script标签需要加上 type="module"
```html
<script src="./ES6demo.js" type="module"></script>
```
**需要设置浏览器允许跨域请求**，可能报错：（原因：CORS 请求不是 http）。


### CommonJS
* 适用于Node.js

M2.js中：
```js
module.exports = {
    a:1,
    b:2
}
```

```js
const moduleM2 = require('./M2')
console.log(moduleM2)
```

随后命令行运行
```bash
node .\ES6demo.js

# { a: 1, b: 2 }
```

