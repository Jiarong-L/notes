<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]
  },
  svg: {
    fontCache:   'global'   // 'local',or 'global' or 'none'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>

<style>
img{
    width: 49.9%;
}
</style>


课程描述：[Systems Biology 2018 ／ Uri Alon](https://www.bilibili.com/video/BV1YT411c7Y9/)

下文默认公式中的 $X$、$Y$ 指它们的浓度

## Lecture 1

人的 GRN 由约 4500 Gene、10k edge 组成，单个 TF 可以影响 1-1000 个基因，单个基因也可以由 0-6 个 TF 共同调控。

假设有一个 TF $X$ 遇见糖分后形变为激活态 $X^{+}$，随后 $X^{+}$ 与 Promoter Zone 结合，影响转录 gene $Y$ 的效率。一般通过实验数据推断 $X^{+}$ 对 $Y$ 的影响。

![](./System_Biology/1-0.png)


可观测到的 $Y$ 生成速率 $\frac{dY}{dt} = \beta - \alpha Y$ 可由 **Removal Rate** $\alpha$ 以及 **Production Rate** $\beta$ 简单表示。

一般而言，生物体出于能源考虑，不会频繁降解蛋白，对于一些细菌而言降解周期是它们的一生。忽略 $\alpha = \frac{1}{Y寿命}$ 时， $Func(\beta,n,k)$ 大体上的表现如下图示。

![](./System_Biology/1-1.png)![](./System_Biology/1-2.png)


**Steady State** 时 $0 = \frac{dY}{dt} = \beta - \alpha Y$，即 $Y_{st} = \frac{\beta}{\alpha}$

**假设**我们从乌有开始生成 $Y$，即突然使其 $\beta: (0 \rightarrow 1)$，则这个瞬间 
$$\frac{dY}{dt} = 1 - \alpha Y_{st}$$
$$Y = Y_{st} （1-e^{-\alpha t}）$$

随着时间变化，达成理论稳态的一半 $Y = \frac{1}{2} Y_{st}$，所需时间 $T_{\frac{1}{2}} = \frac{log2}{\alpha}$

![](./System_Biology/1-4.png)



**假设**现有一个初始的 Steady State $Y_{st}^{Old}$，突然使其 $\beta: (1 \rightarrow 0)$，则这个瞬间 
$$\frac{dY}{dt} = 0 - \alpha Y_{st}^{Old}$$
$$Y = Y_{st}^{Old} e^{-\alpha t}$$

随着时间变化，达成旧稳态的一半 $Y = \frac{1}{2} Y_{st}^{Old}$，所需时间 $T_{\frac{1}{2}} = \frac{log2}{\alpha}$

随着时间变化，达成新稳态 $Y = 0$，所需时间 $T = \infty$

![](./System_Biology/1-3.png)

如此，Removal Rate $\alpha$ 才是达成 $\frac{Y_{st}}{2}$ 的关键。有丝分裂即 $Y_{st} \rightarrow \frac{Y_{st}}{2}$，可以根据 Cell Generation Time $T_{\frac{1}{2}}$ 来估算 $\alpha$


## Lecture 2

回顾 GNN 课程，我们一般会通过对比随机图（networkx里也提供多种模型）来获得一些显著的 Motif，我们也可以很容易的解释这些 Motif 的生物意义。

**Negative Auto-regulation** 是一种重要的调节机制，其 Motif 就是一种 Self-Loop

![](./System_Biology/2-0.png)


已知 Negative Auto-regulation 情况下，随着时间的推进，Production Rate $\beta$ 随着产物浓度的升高而递减；想象 $\beta = f(Y) = \begin{cases} \beta \quad Y<k  \\\\ 0 \quad Y \ge k \end{cases} $ 的情况，此时 

```
    Y    bt
    |   /
  k |  /________ Yst = k 是最终平衡是状态  (Lecture2)
    | /
    |/___________
    0            t
```

如下图所示，当 $\alpha$ 或 $\beta$ 发生变化时，Negative Auto-regulation 曲线的 $Y_{st}$ 变化较小（抵挡噪音），且未平衡时其 $\beta-\alpha$ 曲线间的 Gap 较恒定 $\beta$ 更大（加速达成 $Y_{st}$）

![](./System_Biology/2-1.png)![](./System_Biology/2-2.png)


## Lecture 3

三元素的Motif中有8种 **Feed Forward Loop**，最主要的2种在E.coli网络中占80%

![](./System_Biology/3-0.png)


以第一种 Coherent Feed Forward Loop 为例，我们可以假设 $Z$ 通过一个 Gate 处理来自 $X$ 和 $Y$ 的信号。

当 $X$ 打开或关闭的瞬间，其下游的 $Y^{+}$ 需要一段时间才能达到 k 浓度（开关阈值）。

AND Gate 时，打开 $X$ 后由于需要等待达成 $Y^{+}$，因此生成 $Z$ 的时间相较于 $X$ 的变化有延迟。而关闭 $X$ 则对 $Z$ 即刻起效。这个机制可以过滤掉短暂的激活信号，但灵敏应对任何抑制信号。

OR Gate 时，打开 $X$ 对 $Z$ 即刻起效，而关闭 $X$ 则效果延迟。

![](./System_Biology/3-1.png)



注意，当 Node 间是抑制作用时，Strong Supression 令下游产物归零，Partial Supression 虽然令下游产物的 $Z_{st}$ 降低，但事实上缩短了达成此 low $Z_{st}$ 水平所需的时间，因此也可以被视为一种加速手段。以下图 In-coherent Feed Forward Loop 为例

![](./System_Biology/3-2.png)

想象一下，在面对急性压力时，会唤起快速响应的Loop；当压力转变为长期状态时，打开了其它较慢的Loop。


## Lecture 4



