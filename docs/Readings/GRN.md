<style>
img{
    width: 60%;
}
</style>


转录因子(TFs)指调控转录过程的蛋白质，GRN 即是 TFs、靶基因 组成的互作网络。

获知调控网络后，可以使用tf的特定组合将GRN从一种状态引导到另一种状态：干细胞特定分化/成熟，癌细胞易受特定药物影响的状态


## GRN 推断

1. 使用单细胞数据，
    - 聚类：细胞类型/状态 --- 静态：只是推断TF-靶基因的共表达模块
    - 轨迹推断：沿伪时间轴的排序 --- 动态：关心调控过程如何随时间变化(细胞轨迹)和在不同的生物条件(扰动:敲除/过表达)下进行调整

2. 推断
    - Boolean network：从一种状态过渡到另一种状态所需的TFs逻辑组合
    - 共表达分析：TFs与候选靶基因(集)的相关/回归，确定驱动特定细胞状态的MRs(i.e.能够对多个靶基因进行调控的主要TFs)
    - scATAC

常用工具：pySCENIC/GENIE3，BoolNet/SCNS


### Boolean network

以 [BTR: training asynchronous Boolean models using single-cell expression data (2016)](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-016-1235-y) 为例

![Fig. 1](https://media.springernature.com/full/springer-static/image/art%3A10.1186%2Fs12859-016-1235-y/MediaObjects/12859_2016_1235_Fig1_HTML.gif)

**Boolean model**: 
```
n Genes:        x1, x2,..., xn     where x = {0, 1}
n UpdateFunc:   f1, f2,..., fn     即 x1 = f1(st) 
                                         = (Activation_Inputs)∧¬(Inhibition_Inputs) 
AND (∧), OR (∨) and NOT (¬)              = (x3 ∧ x4)∧¬(Inhibition_Inputs)
                                         = (x3 ∧ x4)∧¬(x5 ∨ [x2 ∧ x9])
              
A model state is represented by a Boolean vector st  = {x1t, …, xnt} at simulation step t
A model state space S = {s1, s2,..., st} of all simulation steps
```


**Training Data**:  k_Cell × y_Gene  Matrix
```
n Genes: (of cell k)   yk1, yk2,..., ykn     where y = {0, 1}

A data state vk  = {yk1, …, ykn} of cell k for n genes
A data state space V = {v 1, …, v k } of all states(cells) in an experiment
```

**训练步骤**: (Swarming hill climbing strategy) 通过最小修改(fn)、迭代地探索当前模型在解空间中的邻域，每一步都保留多个最优解，当所有最优解得分收敛时才结束搜索

1. 对每个Cell, Simulating from an initial model state s1 直至动态稳态
    - Asynchronous update scheme: 一次最多更新一个基因
    - 动态稳态: 单个不再变化的st / a cyclic sequence of model states
    - state space S = {s1, s2,..., st}
    
2. 计算 Loss: BSS Scoring 
    - pairwise distance between each model state **st** and data state **vk**
    - model complexity: number of edges --- 详见GNN笔记基础部分
    - input genes i.e. node degree

3. 对比之前的loss，决定是否保留这个模型

4. 修改fn，继续下一个Loop


除此之外，还可引入 general trajectories 信息，如 [SCNS: a graphical tool ...](https://bmcsystbiol.biomedcentral.com/articles/10.1186/s12918-018-0581-y) 定义的 initial/final 顶点对应着 early/late time point (即轨迹上的细胞类型)



## 参考

* [Mapping gene regulatory networks from single-cell omics data](https://pmc.ncbi.nlm.nih.gov/articles/PMC6063279/) ([中文笔记](https://www.jianshu.com/p/25e2383d7d6f))
    - ![](https://cdn.ncbi.nlm.nih.gov/pmc/blobs/32e6/6063279/aed6233d1746/elx046f2.jpg)

* [Gene regulatory network inference in the era of single-cell multi-omics 中文笔记](https://blog.csdn.net/weixin_56751316/article/details/142680655)

* [贝叶斯网络](https://blog.csdn.net/qq_41603411/article/details/104708470) 

* [Gene regulatory networks in disease and ageing](https://www.nature.com/articles/s41581-024-00849-7)

* BTR Boolean model 的一些设置
```
Limits:
    - fn allows a conjunction of up to two input genes in each slot
    - 同一个 fn 中 each input gene x 只能出现一次
    - in-degree limits 默认 6
    - no self-loop
```


