JavaScript基本功能备忘；[jsDemo.zip](./JS/jsDemo.zip)

记得给vscode安装es6插件；ES6新增的特性见 [ES6](ES6.md)；  

其它关联：[TS](TS.md)，[Vue](Vue.md)

## 基本操作

在html的body或header部分引入script，也可将内容放在另一个文件
```js
<script> ..... </script>

/* 或将.....内容放置于某个.js文件中 */

<script scr="./jsDemo.js"></script>
```

浏览器-右键-审查元素-控制台可以查看console.log输出；alert()则是弹框
```js
console.log('xxx')
window.alert('xxx')
```


数据类型示例
```js
var myNum = 100_000.56
var myStr = "5"
var myBool = true 
var myNull = null
var myUndefined  // 不写，或 = void 0
                 // 不能 = undefined；因为：
                 // 如果在函数中 var undefined = 1，优先级会高于全局变量 undefined
var myObj = {
    name: "ObjName",
    value: "ObjValue"
}

var mySum = 2/1 - 2 * 3 % 4
var myStrConcate = "Ab" + "Cd"
var aTrue = 2>1
var aFalse = 2 === "2"
```


if示例
```js
if (false) {
    console.log('case1')
} else if (false) {
    console.log('case2')
} else if (false) {
    console.log('case3')
} else {
    console.log('case4')
}
```

for示例
```js
for (var i=0; i<10; i++) {
    console.log(i)
}
for (var k in myObj) {
    console.log(k,myObj[k])
}
```


function示例
```js
function myFunc (a,b) {
    return a + b
}
var myFuncRes = myFunc(1,'2')
```
匿名函数(ES6)
```js
myDOM.onclick = () => {alert('clicked!')}

// (input_parameters) => {what_to_do}
// (input_parameters) => (return_parameters)
```

array示例，详情请见ES6相关段落
```js
var myArr = [1,2,3,4,5]
    // idx:  0 1 2 3 4
myArr.splice(1,3)        // 从idx 1开始切取3个元素：返回[2, 3, 4]；myArr=[1,5]
myArr.push(100)          // add to end
myArr.unshift(100)       // add to start
myArr.forEach(function (value,index) {
    console.log(value,index)
})
console.log(myArr.length)
console.log(myArr[0])
```


正则格式常见：```/ /g```，斜杠间定义查找模式，g修饰符表示全局匹配多处（否则默认只匹配第一个match）；```mystr.match(reg)```进行匹配，或```mystr.match(reg,'newstr')```进行替换
```js
const reg = /abc|cde/g        //匹配abc或cde
const reg = /(abc|cde) is/g   //匹配abc is或cde is
const reg = /^abc/g        //匹配在开头的abc
const reg = /abc$/g        //匹配在末尾的abc
const reg = /c?/g          //c可以出现 0 或 1 次
const reg = /c*/g          //c可以出现 0 或 N 次
const reg = /c+/g          //c可以出现 1 或 N 次
const reg = /c{5,8}/g      //c可以出现 5 到 8 次
const reg = /[a-zA-z]/g    //匹配字母集
const reg = /[^a-zA-z]/g   //匹配除字母集外的其它字符
const reg = /\[/g          //转义匹配[，
                    // 或触发预定义模式: 
                    // \d 数字，\D 除数字外的其它字符 [^0-9]
                    // \w 单词字符，\W 除单词外的其它字符

```

* ``` | [] ^ $ ? * + {,} []  ``` 是常见的特殊功能字符，见上方示例
* regexr.com 进行练习


## DOM
### 元素获取
```js
var myDOM = document.getElementById('myDOMid')
myDOM.previousElementSibling.textContent = 'prevSib'
```

| 语句 | 作用 |
| -- | -- |
| document.getElementById('myid') | 根据id选取**单个DOM对象**（第一个match） |
| document.getElementsByTagName('p') | 根据标签选取DOM对象的**HTMLCollection** |
| document.querySelectorAll('p') <br> document.querySelectorAll('#myid') <br> document.querySelectorAll('.myclass') <br> document.querySelectorAll('div.myclass p') | 返回DOM对象的**NodeList**，可以根据标签/id/class选取 |
|  document.querySelector() | 用法同上,但返回**单个DOM对象**（第一个match） |
| myDOM.previousElementSibling <br> myDOM.nextElementSibling | myDOM的前/后同级DOM对象; 可以是不同标签(e.g. div 前一个同级标签可以是 p) |
| myDOM.parentNode <br> myDOM.firstChild/lastChild <br> myDOM.childNodes | myDOM的父/子级DOM对象 <br> 单个/NodeList |


### 样式处理
详情查看 [HTMLElement：style 属性](https://developer.mozilla.org/zh-CN/docs/Web/API/HTMLElement/style)
```
myDOM.style.color = 'red'
myDOM.style.backgroundColor = 'blue'
```
也可以在style中设定好newClass的style，再```myDOM.className = 'newClass'```
```html
<style>
    .newClass {
        background-color: yellow;
    }
</style>
```
**如果同时设置一个属性，myDOM.style.xx会覆盖style的设置**

### 文本处理
| 语句 | 作用 | 示例 |
| -- | -- | -- |
| myDOM.innerHTML | DOM对象的HTML | ```<p>info str</p>``` |
| myDOM.textContent | DOM对象的文字 | ```info str``` |

### 事件处理
详见[Element](https://developer.mozilla.org/en-US/docs/Web/API/Element/afterscriptexecute_event)的Events。

```js
myDOM.onclick = () => {alert('clicked! 1')}
myDOM.onclick = () => {alert('clicked! 2')}
```
但click1会被覆盖；为了避免事件被后来事件覆盖，使用addEventListener：
```js
myDOM.addEventListener('click', () => {alert('clicked! 1')})
myDOM.addEventListener('click', () => {alert('clicked! 2')})

// myDOM.addEventListener('click', function () {...})
```

## 定时器
**延迟**2s（2000ms）执行```function () {...}```；返回timer的标识（ID）
```js
var myTimer = setTimeout( () => {console.log('timeout')},2000 )

// setTimeout( function () {...} ,  ms )
```

**每间隔**2s（2000ms）执行```alert('timeout')```；返回timer的标识（ID）
```js
var myTimer = setInterval( () => {console.log('timeInterval')},2000 )

// setInterval( function () {...} ,  ms )
```
通过timer的标识（ID），**停止**Timer；下例结合setTimeout达成定时清除
```js
setTimeout( ()=>{clearInterval(myTimer)} ,6000)
// clearInterval()
```

## [Canvas](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API)
绘制简单图形，示例见[link](https://developer.mozilla.org/zh-CN/docs/Web/API/Canvas_API/Tutorial/Drawing_shapes);  

首先有canvas对象，注意，canvas的width、height必须如下设置(不能在css中设置)，否则图形会随着border形状调整而变形
```html
<canvas id="mycanvas" width="100px" height="100px"></canvas>
```

选取canvas对象，画图
```js
var canvas = document.getElementById("mycanvas");
var ctx = canvas.getContext("2d");
ctx.moveTo(0, 0)                 // 移动笔触
ctx.beginPath();                 // 绘画开始
ctx.arc(75, 75, 50, 0, Math.PI * 2, true); 
ctx.stroke(); //ctx.fill()       // 显示/填充图形
```




### 库
一些封装好的特定集合

## [jQuery](https://jquery.com/)

‘\$’ 是jQuery的别称/顶级对象（相当于JS的window）；使用示例：
```js
$(document).ready(                    // 等页面DOM加载完毕后
    () => {
        $('#myid').click(()=>{})             // 点击'#myid'后...
        $('div:eq(2)').css('color','red')   // css('属性','值')
        $('div').eq(2)      // 第二个div，选择效果同上
        $('div').click(
            () = { $(this).siblings("button").hide() } 
        )          // 点击后隐藏同级的button

        $.get( url, [dataObj_opt], [callbackfunc_opt]) // AJAX
        $.post(url, [dataObj_opt], [callbackfunc_opt]) // AJAX
        $.ajax({                        // 综合
            type: '',                // GET POST
            url: '',                 // url
            data: {},                // 请求所带的数据
            auccess: callbackfunc 
        })

    }
)

```

jQuery对象与DOM对象略有不同但可以互相转换:  

| -- | 示例 | 方法 | 说明 | 
| -- | -- | -- | -- | 
| DOM对象 | ```var myDom = document.querySelectorAll('div')``` | ```myDom.style.display = 'none'``` | -- | 
| jQuery对象 | ```var myjQuery = $('div')``` | ```myjQuery.hide()``` | jQuery对象是伪数组的形式；应用方法时将遍历其内所有DOM元素，此过程称为**隐式迭代** | 
| DOM -> jQuery  | ```$(myDom)``` | -- | -- | 
| jQuery -> DOM | ```myjQuery[index]``` <br> ```myjQuery.get(index)``` | index是个数字，e.g. 0 | -- | 


* 更多样式操纵、动画功能、Ajax 请参考 [jQuery官方文档](https://api.jquery.com/)





