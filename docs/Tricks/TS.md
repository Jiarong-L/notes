
TypeScript 是一种基于 JavaScript 构建的强类型编程语言  

JavaScript 的严格模式：```"use strict";``` 不能使用未声明的变量; 不过还是弱类型

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
let valF: string | null = null  // 当开启StrictNullChecks时，不能将null赋给其他类型
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
interface myObj {
    name: string,
    val: number
}

const objA: myObj = {
    name: 'abc',
    val: 10
}
```


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


