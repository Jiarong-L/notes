


vue是JS库框架，可自动更新页面，简化了DOM操作，更适合中大型项目  

关联：React (TBA)

## Vue2
### 核心功能
通过CDN加载在线vue.js，或将其下载到本地; 详细示例见: [VueBasicDemo](Vue/VueBasic.html)

```html
<script src="https://cdn.jsdelivr.net/npm/vue@2.7.14/dist/vue.js"></script>

<div id="myid">
<p>{{ ValA }}</p>
<p>{{ func1 () }}</p>
<p>{{ comp1 }}</p>
</div>

<script>
    const vm = new Vue({
        el: '#myid',
        data () { return {ValA:'A',ArrB:[1,2,3],ObjC:{c:"3"},BoolD:true} },
        methods: { func1(){},func2(){}   },
        computed: { comp1(){},comp2(){}   },
        watch: { ValA(newV, oldV){}   }
    })
</script>
```
**插值表达式**```{{  }}```可以在html中同步展示data与methods/computed的返回值，此外还可以有一些简单的计算逻辑判断，例如```{{ 1+2+3 }}```，```{{ true ? 'yes':'no' }}```


| -- | 说明 | 解释 | 引用方法 | 其它 |
| -- | -- | -- | -- | -- |
| el | -- | Vue的生效位置 | -- | 上例中，作用域为id=myid的div内 |
| data | 相应式数据 | 若数值变化则页面同步更新 | Vue(..this.ValA); vm.ValA; ```{{ValA}}```; v-text="ValA"... | -- |
| methods | 方法属性 | 可理解为functions | ```{{func1()}}``` | 每次引用都会执行 |
| computed | 计算属性 | 可理解为缓存的methods结果   | ```{{comp1}}``` | 缓存：多次引用时，如果return的结果没有变化，就不会重复执行；变化一次再执行一次 |
| watch | 侦听器 | 监听某个数据是否出现变化，若出现变化则再干点什么 | -- | -- |


此外，Vue中还有一些**v-指令**，部分示例：
```html
<div id="myid">
    <!-- 标签内容/html设置为ValA的值 -->
    <p v-text="ValA"></p>
    <p v-html="ValA"></p>
    <!-- for loop 批量展示 -->
    <p v-for="item in 5">v-for: num's {{item}}</p>
    <p v-for="item in ArrB">v-for: arr's {{item}}</p>
    <p v-for="(item,key,index) in ObjC">v-for: obj's {{item}} {{key}} {{index}}</p>
    <!-- 标签是否存在/显示 -->
    <p v-if="false">v-if:p标签是否存在/销毁</p>
    <p v-show="false">v-if:p标签是否显示(style="display:none")</p>
    <!-- 属性bind -->
    <p v-bind:title="ValA">v-bind:title</p>
    <p :title="ValA">v-bind:title</p>
    <!-- 事件on -->
    <button v-on:click="func2">func2 click</button><br>
    <button @click="func2">func2 click</button><br>
    <!-- 数据、视图双向绑定；i.e. 一个变了另一个也跟着变 -->
    <!-- 修饰符: 用于简单内容处理, e.g. trim -->
    <input type="text" v-model="myinputVal">
    <input type="text" v-model.trim="myinputVal">
    <p>{{ myinputVal }}</p>
    <p v-text="myinputVal">123</p>
</div>
```


### Vue CLI

npm是node.js的装包工具，安装Vue CLI
```
npm install @vue/cli
vue --version
```

Vue CLI 快速创建名为 vue2-proj 的项目/文件夹，然后运行项目: 
```bash
vue create vue2-proj  // 选择vue2
cd vue2-proj
npm run serve
```

部分项目目录：

* package.json: 一些可使用的功能
* node_modules/: 依赖包，无需改动
* public/: 不参与编译的资源
* src/: 参与编译的资源
    - components/: 自定义组件
    - App.vue: 根组件
    - main.js: Vue应用入口


### 组件
组件用于封装页面部分功能；每个.vue文件称为单文件组件，由（结构、样式、逻辑）三部分组成。  

* 每个.vue文件export default 导出一个组件对象(它自己)
* 根组件没有父组件，它在Vue应用入口中被调用创建
* el 属性只能在根组件中设置 **！！**
* 父组件在使用子组件时需要 ```import``` 并设置 ```components:{} ```
* 父组件在使用子组件时类似HTML标签，并需传入子组件所需参数, ```<VueSon msg="Hello"></VueSon>```
* 示例: 

子组件 
```html
<template>...HTML...{{ msg }}...</template>

<script>
export default {
name: 'VueSon',
props: {msg: String}
}
</script>

<style>#VueSon {...}</style>
```

父组件 
```html
<template>
<VueSon msg="Hello">
</template>

<script>
import VueSon from './components/VueSon.vue'
export default {
name: 'VueParent',
components: { VueSon }
}
</script>

<style>#VueParent {...}</style>
```


#### 组件通信

| 数据方向 | 父 | 子 | 说明 |
| -- | -- | -- | -- |
| 父->子 | ```<VueSon msg="InputData">``` | ```props: {msg: String}```或<br>```props: { msg: {type: [String,Number],default: 'Default Str',required: false}  }``` | 子中 props 接受父传过来的数值，可限制数值的type，默认值/是否必须 |
| 子->父 |  ```<VueSon @event1="funcParent">```<br>```methods:{ funcParent(sonVal){...}}``` | ```data(){return {sonVal}},```<br>```methods:{funcSon(){this.$emit('event1',this.sonVal)} }``` | 子中emit设置自定义事件 event1, 事件触发则传 sonVal 与父; 父中设置一个监听event，接收sonVal |
| 子->子 | -- | -- | 子->父->子 |
| 层级过多时 | -- | -- | Vuex |


#### 组件插槽
子中template可使用 ```<slot>``` 占位符设置插槽位置/默认值，父引子时 ```<VueSon>AAA</VueSon>``` 中 ```AAA``` 为插槽部位。

***默认插槽：***    
子
```html
<template>
    <slot>Default Val</slot>
</template>
```
父
```html
<VueSon>New Val</VueSon>
```
***具名插槽：当有多个slot时***      
子
```html
<template>
    <slot name="SlotA">Default Val</slot>
    <slot name="SlotB">Default Val</slot>
</template>
```
父
```html
<VueSon>
    <template v-slot:SlotA>New Val</template>
    <template #SlotB>New Val</template>
</VueSon>
```

### VueRouter
Vue是单页面，仅一个HTML，Router检测URL变化，渲染相关页面。  

```vue create proj``` 的时候使用自定义模式，**勾选router**，相比默认多了 router/ 文件夹，于[router/index.js](Vue/router/index.js) 中配置：

* ```mode: 'history'``` 隐藏浏览器显示的路径中的```#```，比较美观
* ```base: Process.env.BASE_URL``` 配置基础地址
* routes，其中 ```component``` 有两种引入方式
    - ```import xxx from 'xxx.vue'```  同步加载
    - ```()=> import('xxx.vue')```  异步加载

<br> 

App.vue 中使用 router-link 控制切换目标，切换内容则会在 router-view 处显示：
```html
<template>
  <div id="app">
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link :to="{ name: 'home' }">Home</router-link>
    </nav>
    <router-view/>
  </div>
</template>
```

#### 嵌套路由
如下例中 VideoPage (一级路由) 与 info1、info2  (二级路由)

#### 动态路由
router/index.js
```js
...
import all_components from ......

  {
    path: '/video/:id',    ## :id 动态匹配不同的id
    name: 'VideoPage',
    component: VideoView,
    children: [            ## 二级路由
        {path: 'info1', name: 'vinfo1',component: InfoView1}, ## '/video/:id/info1'
        {path: 'info2', name: 'vinfo2',component: InfoView2}, ## '/video/:id/info2'
    ],
    props: true            ## 此子vue得以使用接收到的参数 id
  }
...
```
VideoView.vue (子)
```js
<template>
  <div class="video">
  <p>{{ id }}</p> 
  </div>
</template>

export default {
  name: 'VideoView',
  props: ['id']
}
```
任何需要显示router跳转的template，App.vue 中可以放置 VideoPage，而 VideoView.vue 中放置 vinfo1/vinfo2；此例中id赋值30 
```html
<router-link to="/video/30">VideoPage</router-link> |
<router-link :to="{ name: 'VideoPage', params: {id:30} }">VideoPage</router-link> |
<router-link :to="{ name: 'vinfo1', params: {id:30} }">VideoPage Info1</router-link> |
<router-link :to="{ name: 'vinfo1', params: {id:30} }">VideoPage Info1</router-link> 
<router-view/>
```

#### 编程式导航
实现主动跳转；created() 是vue实例创建后执行的生命周期勾子; 

路由切换时vue实例A可以通过 $router.push 跳转并传输数据给另一个vue对象B；

```js
export default {
  name: 'JumpStartA',
  created () {
    // setTimeout( ()=>{  this.$router.push({ name: 'JumpEndB' });  } ,3000 )
    setTimeout( ()=>{  this.$router.push({ name: 'JumpEndB', query: {sData: 'dataInfo'} });  } ,3000 )
  }
}
```
B通过 $route.query 接收A传递过来的数据
```js
export default {
  name: 'JumpEndB',
  created () {
    console.log(this.$route.query);   // {sData: 'dataInfo'}
  }
}
```

#### 导航守卫
设定**每一次**导航被触发前都进行某种操作，router/index.js 中：
```js
const router = new VueRouter(...)

router.beforeEach((to, from, next) => {
  console.log('触发守卫');  // Do Anything
  next();
});
```


### Vuex
* 状态管理工具  
* ```vue create proj``` 的时候使用自定义，**勾选Vuex**，相比默认多了 store/ 文件夹，于[store/index.js](Vue/store/index.js) 中配置需要全局管理的操作/变量/...


| -- | 说明 | JS中调用 | 其它 | 
| -- | -- | -- | -- | 
| state | 存储全局数据，类似data() | ```this.$store.state.ValA``` | -- | 
| getters | 缓存属性，类似computed  | ```this.$store.getters.len``` | -- | 
| mutations | 修改变量值的methods <br> *不建议在他处修改state数据，易混淆 | ```this.$store.commit('func1',inputVal)``` | 直接使用时是同步执行，actions调用时候可以异步执行 | 
| actions | 调用mutations中的methods | ```this.$store.dispatch('delayfunc1',inputVal)``` | 通过setTimeout设置异步执行，否则也只是不异步的调用 | 
| modules | 分类/分功能/分模块，防止模块间相互调用/修改 | ```this.$store.mA.state.xxx``` <br> ```this.$store.mA.commit('yyy',...)``` | 除了下文示例，也可以将模块封装到a.js/b.js中再export | 

store/index 示例
```js
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state () {          
    return {
      ValA: 'ok'
    }
  },
  getters: {
    len () {console.log('Getters Computed'); return 10}
  },
  mutations: {
    func1 (state, inputVal) {state.ValA = inputVal}
  },
  actions: {
    delayfunc1 (store, inputVal) {
      setTimeout(()=>{store.commit('func1',inputVal)},3000)
    }
  },
  modules: {
    mA: {
      state: {},
      mutations: {},
      actions: {}
    },
    mB: {
      getters: {}
    }
  }
})
```

### 浏览器Vue插件
Vue-Devtools： timeline可追踪状态变更，但不支持异步操作的追踪


## Vue3
**vscode建议安装volar插件**    

Vue3支持Vue2的写法，且相对于Vue2:  

* 支持组合式API（Composition API）将相关功能相关代码集中在一起   
* main.js 改用 ```createApp(App).mount('#app')``` （Vue2: ```new Vue({el: '#app',...})```）
* ```<template></template>``` 内不必须加根标签 (Vue2: 必须加e.g. div)
* 用setup语法糖简化了代码： 
```js
<script setup>
import HelloWorld from './components/HelloWorld.vue'
</script>
```
相当于： 
```js
<script>
import HelloWorld from './components/HelloWorld.vue'
export default {
    name: 'App',
    components: {HelloWorld},
    props: {msg:String},
    setup () {}
}
</script>
```


### npm init
也可以使用```vue create proj```
```bash
npm init vue@latest
npm run serve
```

### 常用特性

| -- | 作用 | 说明 | 
| -- | -- | -- | 
| reactive | 响应式数据声明 | 支持多维数据、对任意维度数据的操作 | 
| shallowReactive | 浅响应式数据声明 | 仅支持对第一维度数据的操作 | 
| ref | 计数值的响应式处理 (非objects) | ref创建一个obj，再将计数值挂载到obj.value上； <br> ES6 proxy 支持的参数只能是objects，ref可以将基本类型转换成objects | 
| readonly | 只读 | 不能修改任意维度的数据 | 
| shallowReadonly | 浅只读 | 不能修改第一维度的数据 | 
| computed | -- | 带缓存 | 
| watch | 侦听getter/effect functions, /ref/reactive Objects或其数值的变化，返回(newVal,oldVal) | 如果希望侦听Obj的某个属性，需要通过借用函数返回这个属性、以满足watch的输入要求 | 
| watchEffect | 侦听某个函数所包含元素的变化，一旦有变化则触发函数 | 自动侦听watchEffect的函数内引用的所有变量 | 


```js
<script setuo>
import { computed, reactive, readonly, ref, shallowReactive, shallowReadonly, watch, watchEffect } from 'vue';

const ValA = reactive({B1: 'bb', B2: [1,2,3,4,5]})
ValA.B2.push(6)  // works!
const ValB = shallowReactive({B1: 'bb', B2: [1,2,3,4,5]})
ValB.B2.push(6)  // Not working! 2nd layer

const ValC = ref(0)
ValC.value++

const ValD = readonly({B1: 'bb', B2: [1,2,3,4,5]})
ValD.B2.push(6)  // Not working! read-only
const ValE = shallowReadonly({B1: 'bb', B2: [1,2,3,4,5]})
ValD.B1 = 'cc'   // Not working! 1st layer read-only
ValD.B2.push(6)  // works! 2nd layer not-read-only

const getVal = computed(()=>{return ValC.value})

watch(ValA, (newVal,oldVal)=>{console.log(newVal,oldVal)})
watch(()=>ValA.B2, (newVal,oldVal)=>{console.log(newVal,oldVal)})

watchEffect(()=>{console.log(ValA,ValB)})   // 自动侦听ValA,ValB
</script>
```

### Pinia
Vuex的升级版，stores/xxx.js 中使用的组合式函数会自动识别为状态管理的相关模块。一个 [xxx.js](Vue/store/counter.js) 中声明一个defineStore，即是一个模块。

| Pinia | Vuex | 
| -- | -- | 
| ref | state | 
| computed | getters | 
| function | actions/mutations(x) | 


stores/xxx.js 示例：
```js
export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  function increment() {
    count.value++
  }
  return { count, doubleCount, increment }
})
```

views/AboutView.vue 中导入相应管理模块、使用：
```html
<script>
    import { useCounterStore } from './stores/xxx.js'
    const myStore = useCounterStore()    
</script>


<template>
  <p>{{ myStore.count }}</p>
  <p>{{ myStore.doubleCount }}</p>
  <button @click="myStore.increment()">+1</button>
</template>
```

## 参考
Vue2：https://v2.cn.vuejs.org/v2/guide/installation.html  
Vue3：https://cn.vuejs.org/guide/introduction.html  
B站速成：https://www.bilibili.com/video/BV1oj411D7jk/?spm_id_from=333.788

