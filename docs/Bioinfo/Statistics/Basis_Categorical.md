<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>


<style>
img{
    width: 60%;
}
table th:nth-of-type(5) {
    width: 20%;
}
</style>

教材：《统计学（原书第五版）》

![](./Basis/.png) 


## 分类数据
对于分类数据的统计可以制成 单向表 与 双向表（又称：列联表）

### 单向表

单向表只有一行；e.g. A，B，C 三条生产线当日生产的产品数分别为 22，19，20

| A | B | C |
| -- | -- | -- |
| 22 | 19 | 20 |



### 双向表

一般的 $r \times c$ 列联表 有$r$行$c$列；e.g. 生产线 W1 当日生产的 V1 产品数为 100

| - | W1 | W2 | W3 |
| -- | -- | -- | -- |
| V1 | 100 | 19 | 20 |
| V2 | 6 | 8 | 7 |
| V3 | 10 | 16 | 12 |
| V4 | 11 | 15 | 13 |
