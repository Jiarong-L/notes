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
</style>



![](./Basis/.png) 



## 描述性统计

| -- | 样本 | 总体 |
| -- | -- | -- |
| 列说明 | 从总体N中取n测量值 | 有n个测量值的有限总体 |
| 均值 | $$\overline{y}=\frac{\sum\limits_{i=1}^{n}y_i}{n}$$ | $\mu$ |
| 方差 | $$s^2=\frac{\sum\limits_{i=1}^{n}(y_i-\overline{y})^2}{n-1}$$ | $$\sigma^2=\frac{\sum\limits_{i=1}^{n}(y_i-\mu)^2}{n}$$ |
| 标准差 | $$s=\sqrt{s^2}$$ | $$\sigma=\sqrt{\sigma^2}$$ |
| z score | $$z=\frac{y-\overline{y}}{s}$$ | $$z=\frac{y-\mu}{\sigma}$$ |

* 经验法则：68% 观测值位于 $\overline{y}\pm s$，95% 位于 $\overline{y}\pm 2s$，几乎所有位于 $\overline{y}\pm 3s$
* 切比雪夫法则：$(1-\frac{1}{k^2})$观测值位于k个标准差范围内($\overline{y}\pm ks$)
* z score：以标准差为单位，观测值y相对于均值的位置
* IQR=上四分位-下四分位，box plot 内篱笆为 1.5 IQR 范围内，外篱笆为 3 IQR；超出外篱笆者很可能是异常值



## 概率

* **概率**：给定模型参数，结果是否合理：均匀硬币，拋20次得15次正面的概率
* **似然**：给定观测值，描述模型参数是否合理：拋20次得15次正面，硬币均匀的可能性
* **简单事件**是一个试验的基本结果，不能被分解为更简单的结果；试验的**样本空间**是所有可能的简单事件的集合; 
    - e.g. 对于 0-1-2 随机选择，0是一个简单事件，{0,1,2}是样本空间
    - 简单事件的概率在 [0,1] 之间，且样本空间中所有简单事件的概率和等于1
    - **事件A**的概率等于事件A中所包含的简单事件的概率之和；e.g. A：{观测到1或2}
* 事件A的**补**$A^c$指所有不在A中的简单事件组成的事件， $P(A)+P(A^c)= 1$    
* **复合事件**可视为两个或更多事件的组合
    - A或B $= P(A \cup B)$
    - A和B同时发生 $= P(A \cap B) = P(A,B)$，如果A与B**互斥**（不能同时发生），$P(A,B)=0$
    - $P(A \cup B) = P(A) + P(B) - P(A,B)$
* **条件概率** $P(A|B)$：Given B 时，事件A发生的概率
    - $P(A,B) = P(A|B)P(B) = P(B|A)P(A)$
* 贝叶斯法则：通过已知的概率计算未知条件概率
    ![](./Basis/3-1.png) 
    - 先验概率：不依靠观测数据的概率分布
    - 后验概率：基于观测数据得到的条件概率

* 从N中一次取n的不同**排列**个数：$A_N^n=N(N-1)...(N-n+1)=\frac{N!}{(N-n)!}$
* 从N中一次取n的不同**组合**个数：$C_N^n=\binom{N}{n}=\frac{N!}{n!(N-n)!}$
* 从N中取k个集合大小为$n_i$的集合，不同的分割方法个数：$A=\frac{N!}{n_1!n_2!...n_k!}$

* N中每个样本都有相等的被选中概率，如是被选出的n个样本可被称为**随机样本**
* $P(A|B)=P(A)$，B不影响A的概率，则A、B相互**独立**



## 离散随机变量








## 参考
先验概率、后验概率、似然概率：https://zhuanlan.zhihu.com/p/397960221  



