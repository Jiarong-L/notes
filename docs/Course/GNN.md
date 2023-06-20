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
    width: 80%;
}
</style>



课程描述：cs224w    
课程主页：https://web.stanford.edu/class/cs224w/index.html


课程描述：bilibili-图神经网络       
视频链接：https://www.bilibili.com/video/BV1YB4y1S7An/  


## Concepts
此处查看以下概念的计算示例：[concepts.py](GNN/concepts.py),[pagerank.py](GNN/pagerank.py)  

* **G=(V,E)** --- V为顶点(Node)集合，E为边(Edge)集合

* **度(degree):** 与v接触的边的数目；有向图中分为出度、入度

* Matrix --- a<sub>ij</sub> 表示 (i 行，j 列) 的值

* **邻接矩阵(Adjacency):** a<sub>ij</sub> 表示v<sub>i</sub>与v<sub>j</sub>之间的边数；行和(列和)为Node的出(入)度。

* **关联矩阵(Incidence):** a<sub>ij</sub> 表示v<sub>i</sub>与e<sub>j</sub>关联的次数,取值 [0,1,2(自环)]，列和为2；若为有向图，1表示v<sub>i</sub>为起点，-1表示v<sub>i</sub>为终点，列和为0。**Question：有向图的自环怎么表示？**

* 度矩阵: d<sub>ii</sub>=i列之和，其余部分0

* **拉普拉斯矩阵(Laplacian):** L = 度矩阵D - 邻接矩阵A; 对称、每一行元素之和都为0; 实际代表了图的二阶导数

* **子图(Subgraph):** V'为V子集，E'为E子集，则G'=(V',E')为G的子图

* **连通图(Connected Grap):** G中任意两个不同的顶点都连通(有路径)，则称G为连通图；有向图G中，如果每对顶点都强连通（v<sub>i</sub><-->v<sub>j</sub>）,则G是一个**强连通图**，如果原图去掉方向后 每对顶点都连通,则G是一个**弱连通图**

* **连通分量(Connected Components):** 无向图的一个极大连通子图，或有向图的一个极大强连通子图。‘极大’意为：连通图只有一个连通分量，即其自身；非连通图有多个连通分量。

* d(i,j) -- v<sub>i</sub>到v<sub>j</sub>的最短路径(所经过的边)

* 图直径: max(最短路径)

* **度中心性(Degree Centrality):** Degree/(n-1)， n为顶点总数；某一顶点的度中心性越高，就说明在G中这个顶点越重要

* **特征向量中心性(Eigenvector Centrality):** 对邻接矩阵A分解特征值，最大特征值对应的特征向量即为图中各顶点的特征向量中心性。（优点：也体现了邻居顶点的度）

* **中介中心性(Betweenness Centrality):** 除去该顶点外、其余顶点两两间最短路径中，经过改顶点的比例

* **连接中心性(Closeness Centrality):** Closeness = (n-1)/sum(此节点到其余节点最短路径)

* 顶点u的**PageRank**值: $PR(u)$ = $ \frac{1-d}{N} + d * \sum_{v\in B}\frac{PR(v)}{L(v)}$， 其中$B$表示所有指向u的顶点，L(v)表示顶点v的出链数目，d为阻尼因子(damping factor)。  
*d解决了Rank Leak、Rank Sink等问题；现实中，可以假设d为用户按照跳转链接来页面u的概率，余下的为通过u网址而来的概率。*

* **HITS:** $Authority(u)=\sum_{v\in B}Hub(v)$，其中$B$表示所有-->u的顶点；$Hub(u)=\sum_{v\in B}Authority(v)$，其中$B$表示所有u-->的顶点；亦是不断迭代至稳态。

## Graph Embedding


### Deepwalk
G中随机游走生成序列，以此序列集为word2vec的训练资料，达成Node embedding。



### LINE




### word2vec




## 参考
拉普拉斯矩阵: https://zhuanlan.zhihu.com/p/362416124   
连通分量：https://zhuanlan.zhihu.com/p/37792015   
中心性：https://zhuanlan.zhihu.com/p/403076024   
networkx: https://networkx.org/documentation/stable/tutorial.html   
pagerank: https://zhuanlan.zhihu.com/p/137561088     
pagerank: https://zhuanlan.zhihu.com/p/120962803   





