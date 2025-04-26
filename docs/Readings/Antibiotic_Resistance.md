


ARG注释是宏基因组项目中较常见的需求，曾经的我只是简单的通过它与可移动原件间距离来假设其HGT的可能性...


## Bacterial Heteroresistance

* MIC - 某抗生素可抑制某菌生长的最低浓度
* [Clinical breakpoint](https://www.eucast.org/clinical_breakpoints) - 临床上，测得某菌的MIC，以此标准来判断其是否敏感(S)/耐药(R)

* 种群分析谱（PAP）在琼脂板上设置抗生素浓度梯度，以鉴定和量化异源耐药菌株。注意，不同测试方法的精度不同，也许不能测出微量的耐药群体。
* 生理药动学模型（PBPK）模拟不同参数 Heteroresistance 可能的结局

### [综述 2019](https://doi.org/10.1038/s41579-019-0218-1)

Heteroresistance 指耐药性在群体中的异质性，即同时存在易感和耐药亚群。治疗时药物杀死敏感亚群，耐药亚群则可能会逐步提升比例，使群体最终发展为完全耐药。当不再使用药物时，一些耐药亚群可能回退至敏感状态（unstable），也可能保持耐药(stable)。

回退的原因可能是突变降低了fitness（额外的开销），另一个原因是：耐药性增加的一个机制是通过串联扩增基因拷贝数，其本身就不稳定（因此，由于实验培养很难完全复刻病人体内环境，在检测过程中也许会恢复为敏感型，i.e.很难检测）


```
Polyclonal Mix 中: 

        此时从Mix中单独提取CloneA，即使检测为敏感，也不一定意味着CloneA之后不会变成耐药
CloneA敏感--↑------------ (Mutate) -------------↓--> CloneA耐药
CloneA敏感--↑--- (获取来自 CloneB 的耐药基因) ----↓--> CloneA耐药     
                                     此时取样，才能测得耐药


Monoclonal 中:

CloneA耐药 ------↓----- CloneA耐药
       此时取样若检测为耐药，可以确定是遗传因素造成的？or在药物的压力选择下人工进化？如果其存在频率高于突变频率，则可能已经是较为稳定的群体？
```


为便于整合多项研究，[Dan Andersson (2019) Fig1](https://doi.org/10.1038/s41579-019-0218-1) 提议提供以下信息：耐药性信息从多克隆还是单克隆中获得，耐药亚群频率固定时的MIC倍数，8倍MIC时耐药亚群的频率，耐药性状稳定与否。


### 串联扩增基因拷贝数


Tandem gene amplifications - 在基因组中的某一特定基因或基因片段的重复拷贝数增加、紧密排列形成串联结构，常见于细菌/肿瘤细胞中

* 可导致特定基因的过表达，e.g. [pmrD 过表达赋予粘菌素耐药性](https://onlinelibrary.wiley.com/doi/10.1111/mmi.13459)
* [致病菌的异质性耐药主要是基因扩增造成的](https://mp.weixin.qq.com/s/1YxWXZH9UK0NWHFpIMh0sw)
* [三种机制（串联扩增等、质粒拷贝数增加、抗性基因转位到隐质粒上）](https://www.nature.com/articles/s41467-024-48233-0)都施加了适应性成本，并且在遗传上不稳定，导致在没有抗生素的情况下迅速恢复到易感性。三种机制在大肠杆菌血液分离株中普遍存在。
* [Fig. 6](https://www.nature.com/articles/s41467-024-46571-7) 显示拷贝数的增加会增加适应性成本，但可以通过二次突变达成适合的平衡、同时保留高效耐药性，因此可以向稳定抗性进化 --- TODO：看下研究方法



### [综述 2025](https://www.nature.com/articles/s44259-025-00076-5)

* Theoretical models of heteroresistance(Fig. 2): 逐步获取耐药能力 or 达到浓度阈值后状态跳跃 

* 临床上，也需要考虑潜在的疾病和免疫系统受损

* 未来还需了解更多机制，以便设计针对阻隔。也需要更加快捷、准确的测试方法。



## 各研究话题

* 环境中ARG分布
* 婴儿肠道中 MGEs 
* [cohort study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12004506/) 显示 E coli bloodstream infections 在乌普萨拉地区耐用性情况 (2025)


## ARG数据库

CARD，以及基于此整合的SARG等，或[AI预测病原微生物耐药性](https://www.frontiersin.org/journals/cellular-and-infection-microbiology/articles/10.3389/fcimb.2024.1482186/full)


