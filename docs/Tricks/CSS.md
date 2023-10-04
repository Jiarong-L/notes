
CSS简单功能备忘；[cssDemo.zip](./CSS/cssDemo.zip)


## 基本操作
vscode中安装html与css插件后，可以自动生成代码

| 输入 |  |
| -- | -- |
| ! + tab | 生成html主体 |
| .myclass + tab | 生成class="myclass"的div框 |
| div + tab | 生成div框 (p,span...同) |
| link + tab | 引入某种资源 |


在html的header部分引入样式，可以用style，也可以将style内容放在另一个文件
```html
<style> ..... </style>

/* 或将.....内容放置于某个.css文件中 */

<link rel="stylesheet" href="./cssDemo.css">
```

## 选择器
如下代码表示：所有span的背景颜色设定为blanchedalmond
```css
span {
    background-color: blanchedalmond;
}
```

| 选择器 | 样式作用域 |
| -- | -- |
| div {} | 所有div |
| .myclass {} | class="myclass"者 |
| #myid {} | id="myid"者 |
| p.myclass {} | class="myclass"的p标签 |
| .myclass p {} | class="myclass"的标签内的子标签p |
| .myclass p.active {} | class="myclass"的标签内、class="active"的子标签p |
| div:hover {} | 所有div经历hover事件时 |


## 通用属性

| 参数 | 功能 | 示例 |
| -- | -- | -- |
| width/height | 宽/高 | 180px <br> 100% <br> auto |
| border | 边框 | 3px dotted grey |
| border-radius | 边框圆角半径 | 8px |
| padding | 内距(内容与边框距离) | 15px auto <br> （上下，左右） <br> 5px 5px 5px 5px <br> （上，右，下，左） <br> 15px <br>（四周） |
| margin | 外距(边框与外部边界距离) | -- |
| background-color | 背景颜色 | #f9f9f9 |
| background-image | 背景图片 | url(./xx.jpg) |
| box-shadow | 边框阴影 | 5px 5px 5px gray  <br> 右偏移，下偏移，晕染范围，颜色 |


* width/height的100%是相较于其父元素；但浏览器处理时会再加上padding，于是实际呈现的宽会超出父容器；为了避免这个问题，需要再加上```box-sizing: border-box;```

* 一些浏览器有默认设置，为了避免影响，于开头声明
```
* {
    margin: 0;
    padding: 0;
}
```


## 文本属性

| 参数 | 功能 | 示例 |
| -- | -- | -- |
| color | 文字颜色 | red |
| text-shadow | 文字阴影 | 同box-shadow |
| text-indent | 段落(p)首行缩进 | 2em (2字符) |
| font-size | 文字大小 | 50px |
| font-family | 字体 | -- |
| font-weight | 文字粗细 | 400/normal |
| line-height | 行高 <br> 结合height调整垂直方向位置效果(单行时) | 50px |
| text-align | 水平方向位置 | center/left |
| text-decoration | 文本装饰 | underline blue |
| writing-mode | 中文垂直书写，英语字母旋转90度展示 | vertical-lr |
| -- | 英语垂直书写，字母不旋转 | writing-mode: vertical-lr; <br> text-orientation: upright; |



## 布局
 
| 参数 | 功能 | 示例 |
| -- | -- | -- |
| position | 模式 | absolute 子标签绝对定位（参考外部relative标签） <br> relative 父标签设定后，其子标签可以其为参考(否则子标签以body为参考)  <br> fixed 固定在视窗的某处 <br> |
| top/left | 相对于参考元素距离 | 200px |





### Flex 

平行单行自动排版

```css
.flex-container {  
    /* max-width: 800px; */
    min-width: 500px;
    display: flex;
    align-items: flex-end;      /* item垂直位置 */
    justify-content: flex-end;  /* item水平位置 */
    
}

.flex-item {
    max-height: 200px;
    /* max-width: 100px; */
    min-width: 10px;
    flex: 1;
}

/* 设置单数个item的flex */
/* or 固定单数个item的width，
      需要hash掉.flex-item中flex！！ */
.flex-item:nth-child(2n+1) {
    flex: 3;
    width: 10px;
}

```

| 参数 | 功能 | 示例 |
| -- | -- | -- |
| max-width/min-width <br> max-height/min-height | 自适应范围 | 500px |
| align-items | item垂直位置 | flex-end |
| justify-content | item水平位置 | flex-end |
| flex | item宽度自适应权重 (此时不能设定这个item的max-width，否则不生效；同时保证item加起来不超过container的max-width限制) | 1 |
| width | 固定展示宽，但如果空间不够的话还是会压缩 <br> 若item使用此参数，不能先定义其flex，否则width失效(e.g. 上文.flex-item中) | -- |


### Grid
平行多行自动排版，会自动调整行的数量
```css
.grid-container {
    height: 300px;

    display: grid; 
    /* grid-template-columns: 200px 300px 300px; */
    /* grid-template-columns: 20% 30% 30%; */
    /* grid-template-columns: 2fr 3fr 3fr; */
    /* grid-template-columns: repeat(3,2fr); */
    /* grid-template-columns: repeat(auto-fill,600px); */
    grid-template-columns: 300px auto 300px;

    grid-template-rows: 1fr 2fr;
}


.grid-item {
    overflow: hidden;
}
```
* grid-template-columns：设定每一列的宽度或权重，也可固定几列、余下的自适应
* grid-template-rows：设定每一行的高度/权重
* 如果grid-container限定了height，items堆叠后超出了范围，grid-template-rows会失效；此时需要设定```overflow: hidden``` 截断展示


## 动画展示

### 过渡
下例中，hover发生时，transition-box逐渐改变大小与颜色、位置，速度由时长设定（5s）,模式有linear、ease-in-out等
```css
.transition-box {
    background-color: rgb(243, 83, 14);
    height: 300px;
    width: 300px;
    position: absolute;
    left: 0;
    /* transition: width 5s,width 5s,background-color 2s,left 5s linear ;*/
    transition: all 5s linear;
    
}

.transition-box:hover {
    width: 600px;
    height: 600px;
    background-color: yellow;
    left: 100px;
}
```
* 需要变换的对象初始化时带上：**transition: all 10s linear;**


### 2d变换
使用上文.transition-box，hover发生时
```css
.transition-box {
    ......
    transform-origin: right bottom;
}


.transition-box:hover {
    /* transform: translate(100px,20px);
    transform: rotate(30deg);
    transform: scale(0.5,0.2); */
    transform: skew(0,-50deg);   
}
```
* **transform**似乎一次只能生效一个
* 如果要**设置旋转点**等参数，应该**在初始化transition-box时设置**，因为如果在hover scale中设置，则这些设置将在5s(自己设定的时间)内渐渐生效



### 3d变换
为了展示3d效果，在transform-box外部套一个transform-container、再加一个Z轴-100px的transform-box-innerZ；届时旋转container展示效果
```html
<div class="transform-container">
    <div class="transform-box"></div>
    <div class="transform-box-innerZ"></div>
</div>
```

```css
.transform-container {
    margin: 300px;
    background-color:black;
    height: 500px;
    width: 500px;

    transform-style: preserve-3d;
    perspective: 500px;
    transition: all 5s linear;
}

.transform-box-innerZ {
    background-color:rgb(224, 224, 17);
    height: 100px;
    width: 100px;
    transform: translateZ(-100px);
}

.transform-box {
    background-color:beige;
    height: 200px;
    width: 200px;
    transition: all 5s linear;
}

.transform-box:hover {
    /* transform: translate3d(200px,100px,100px); */
    transform: rotate3d(1,0,0,100deg)
}

.transform-container:hover {
    transform: rotate3d(0,1,0,100deg)
}

```
* 最外层：**transform-style: preserve-3d;**
* translate3d(x,y,z) = translateZ + translateY + translateZ
* rotate3d(0,1,0,100deg) 按y轴旋转180
* perspective 指定了观察者与 z=0 平面的距离，使具有三维位置变换的元素产生透视效果


### 动画
无需事件就能持续发生的变换，可自定义func；以上文transform-container为例
```css
transform-container {
    ......
    animation: myAniFunc 5s linear infinite;
}

@keyframes myAniFunc {
    0% {
        background-color: black;
    }
    50% {
        background-color: rgb(246, 6, 6);
    }
    1000% {
        background-color: black;
    }
    
}
```

* @keyframes函数 + animation属性




## 参考
https://www.runoob.com/css/css-tutorial.html

