
假如生态学需要画地图，[画洋流](https://blog.csdn.net/chysxslt/article/details/108508426)，...

或者，画一个吃豆豆活点地图？在线遇见神奇生物？

## 常识

| [GIS常识-叠图层](https://www.bilibili.com/video/BV1dT411F7SH/) | 说明 | 常见格式 | 测绘来源 |
| -- | -- | -- | -- |
| 矢量形状 | 经纬坐标集（点Point，线段LineString，面Polygon） | XML数据：GeoJson KML ... | -- |
| 栅格数据 | 地图瓦片，以应对窗口的放大缩小 | 图片格式 | 航拍/卫星数据 |
| 高程数据 | 各处高度信息：三维地形 | osgb dem ... | 无人机斜拍 |

图层存储在gdb格式中，顾名思义，视为数据库

[GIS用途](https://blog.csdn.net/qq_35582643/article/details/137396004)


## 工具 & 地图获取

ArcGIS-桌面版（最常用ArcMap）：旧版制图教程，[10.8 教程](https://www.bilibili.com/video/BV1P2e7eNENp/)


[ArcGIS 10.8 桌面版](https://www.bilibili.com/video/BV1P2e7eNENp/)：ArcMap 最常用

常见WebGIS框架：[LeafletJS - 2D](https://leafletjs.com/examples.html)，[Cesium - 3D](https://cesium.com/learn/cesiumjs-learn/cesiumjs-quickstart/)


1. ArcGIS 等专业软件的内置地图

2. OpenStreetMap --- 国内似乎连不上，建议翻墙下载到本地使用

3. 高德地图、Google Maps 提供的 API


## [R - Leaflet](https://www.rdocumentation.org/packages/leaflet/versions/2.2.2)


1. [R - leaflet() 用法 Workshop](https://byollin.github.io/ShinyLeaflet/#3) --- 非常友好，可交互

2. 官方文档
    - [Package Functions](https://rstudio.github.io/leaflet/reference/index.html) 以及内置地图
    - [RDocumentation](https://www.rdocumentation.org/packages/leaflet/versions/2.2.2) --- 支持在线运行示例代码

3. 用GPT写了一个最简单的ShinyApp-[GISapp.R](./GIS/GISapp.R)，点击地图获取经纬度
    - 关于 observeEvent 所需的 eventExpr，Leaflet 可能提供了一些相关的 reactive value，比如 ```map_click```。建议查看 Leaflet 的函数，并结合使用 reactiveVal() 或其他反应性编程工具
 

其它：关于 [Shiny Gallery](http://shiny.rstudio.com/gallery/)，[Shiny Lesson](https://shiny.posit.co/r/getstarted/shiny-basics/lesson2/)

