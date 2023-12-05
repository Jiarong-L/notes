
TypeScript 是一种基于 JavaScript 构建的强类型编程语言  

JavaScript 的严格模式：```"use strict";``` 不能使用未声明的变量; 不过还是弱类型

注：```tsc --init``` 可在当前文件夹中创建ts的初始化的配置文件 tsconfig.json

## 特点
JS 默认模式中，变量可被修改为不同类型的值，例如：
```js
let mystr = 'abc'
mystr = 10         // JS：成功  TS：错误
```
而TS中，初次给 mystr 赋值时会自动推断其类型为 string （**类型推断**）；TS中，变量不能被赋予其它类型的值。

除了自动推断，也可以显式声明类型（**类型注解**），例如：
```
let mystr:string = 'abc'
```
此外还有**类型断言 (as)**，当确定一定会有返回值的时候使用：
```js
let r = [1,2,3].find(item=>item>2) as number
r * 5        // 若无as，会报错：'r' is possibly 'undefined'.
```

## 类型
### 基本
示例：
```ts
let valA: string = 'abc'
let valB: number = 10
let valC: boolean = true
let valD: null = null
let valE: undefined = void 0
let valF: string | null = null  // 当开启StrictNullChecks时，不能将null赋给其他类型（或class的属性）
let valG: 1 | 2 | 3 = 2         // 限制赋值内容
let arr1 = [1,2,'a'] 
let arr2: number[] = [1,2,3]
let arr3: Array<number> = [1,2,3]
let arr4: [number,number,string] = [1,2,'a']  // 限制每个位置上的类型
let arr5: [number,number,string?] = [1,2]     //  ？对应的内容可在可不在


enum MyEnum {A,B,C}
MyEnum.A === 0
MyEnum.B === 1
MyEnum.C === 2
MyEnum[0] === 'A'
```
### 别名
为了方便使用一些自定义的类型限制，TS支持设置类型别名 (type)：
```ts
type MyStrNum = string | number 
let Valy: MyStrNum = 'abc'
let Valz: MyStrNum = 10
```
### 接口
示例：(相当于自定义了类型)
```ts
interface parentObj {
    Pname: string
}

interface myObj extends parentObj{
    name: string,
    val: number
}

const objA: myObj = {
    Pname: 'Pabc',
    name: 'abc',
    val: 10
}
```

### 类
TS针对 class 设计了一些修饰符，示例：

```ts
class Article {
    title: string
    content: string
    infoA? : string          // 可选属性：未在构造函数中强制设定，可有可无有；不加?的话就不是可选属性，默认为undefined (null)
    private infoB: '-'    // 私有属性、且带默认值
    protected infoC: '-'    // 受保护属性、且带默认值
    static author: string
    constructor (title: string, content: string) {
        this.title = title
        this.content = content
        Article.author = '-'    // class内部访问static属性
    }
}


class Brticle extends Article {
    private _bText: string = ''
    constructor (title: string, content: string) {
        super(title, content)
        this.infoA = '-'  // 继承class可以访问父class的public属性，但不能访问父class的private/protected属性：不能 this.infoC = 'cannot visit'
    } 
    get bText(): string {return this._bText}  // get函数，名字可随意
    set bText(newTxt: string) {this._bText=newTxt} // set函数，名字可随意
}



const A = new Article('titleA','contentA')
const B = new Brticle('titleB','contentB')

A.title   // 外部访问public属性
Article.author  // 外部访问静态属性；注意，不是 A.author！！ 
B.bText  // 使用get函数
B.bText = '-'  // 使用set函数
```

* 默认都是public属性、方法，除非声明 private
* public属性可以外部访问
* private属性只能class内部方法访问，或者对这个属性设置get/set函数来达到访问/赋值的目的（类似java）
* 静态属性（static）将属性设置给class本身，而不是给类实例；引用方法：```classname.staticAttr```
* 可以给静态属性叠加其它声明，比如：```private static readonly author: string = 'me' ```，readonly表示不能重新赋值
* 支持**泛型**：上文任意类型都可替换为T，例如 
    - ```class Article<T>```
    - ```constructor (title: T, content: T)```
    - ```const A = new Article<string>('titleA','contentA')```
    - 所有设置为T的类型都是string


### 抽象类
一般场景：不会直接使用抽象类，只会使用抽象类派生的子类
```ts
abstract class Animal {
    abstract name: string        // 抽象属性
    abstract maskSound (): void  // 抽象方法
    move (): void {}             // 普通方法必须加上函数内容{}，抽象方法可以子类中再设置
}

class Cat extends Animal {   // 子类中必须声明abstract方法、属性
    name: string = 'cat'
    maskSound(): void {}      
}
```

### 类实现接口
示例：
```ts
interface B{
    addInfo: string
}

interface Animal {
    name: string
    get sound(): string
    maskSound (): void
}


class Cat implements Animal,B {
    addInfo: string = '-'
    name: string = 'cat'
    get sound(): string {return '-'}
    maskSound(): void {}
}
```
* 使用接口的原因：**不能同时继承多个类**


## 函数
以下为TS函数的示例：
```ts
function Func0 () {
}

function Func1 (): void {     
}

function Func2 (a: number,b: number): number {           // 可以声明也可以不声明返回值类型  
    return a + b
}

function Func3 (a: number,b = 10,c?:boolean): number | string {    // 引用时 b,c 都可以不输入; b有默认值
    if (c) {return 'abc'}                         
    return a + b
}
Func3(100,10,true)
Func3(100)


function Func4 (a: number,b: number, ...rest:number[]): number | string {   // rest 数目不确定的时候只能声明一种类型的了。。
    return a + b
}

function Func5 (a: number,b: number, ...rest:[string,number|string]): number {    // rest 数目确定的时候依次限制，不过这样意义不大？
    return a + b
}
```
 
TS函数支持泛型 ```<T>```，示例：
```ts
function FuncZ<T> (a: T,b: T): T[] {   
    return [a,b]
}
FuncZ<number>(1,2)
FuncZ<String>('a','b')
```


## 参考
https://ts.nodejs.cn/


