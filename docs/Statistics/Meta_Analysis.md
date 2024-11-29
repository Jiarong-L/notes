

Meta分析教程[(需登录)](https://training.cochrane.org/handbook/current/chapter-10)/[(R)](https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/intro.html)：整合多个studies的结果


## 流程


1. 汇总每项研究的统计量，例如：风险比、均值之差、...
2. **综合统计量**可以是各研究统计量的加权平均，study_i 的贡献权重一般是 1/variance_i
3. 异质性检验(I2)：根据[统计量的齐性检验(I2)](https://blog.csdn.net/m0_37228052/article/details/134138794)，选择 Fixed-Effects Model (I2 < 50%) 或 Random-Effects Model (I2 > 50%)
  - Fixed-Effects Model 假设每一个y_i都有其对应的真值，因此根据i的真值拟合y_i
  - Random-Effects Model 假设每一个y_i都是从一个总体正态分布中获得的取样，因此以总体分布的均值为真值拟合y_i
4. 展示综合统计量及其权重、置信区间，e.g.森林图

目的是探讨：不同研究所得的结果差异是否仍可归于随机误差？差异太大的话，表明不同研究之间的干预效果不一致

此外还需要考虑数据丢失的问题, [参考Survival](./Survival.md)



## 参考
```
Fixed/Random模型的区别   https://wviechtb.github.io/metafor/reference/misc-models.html
CMH检验      https://blog.csdn.net/nixiang_888/article/details/117842865
Meta分析     https://www.sciencedirect.com/science/article/pii/S2772594422001169  
Meta示例     https://blog.csdn.net/m0_37228052/article/details/133026057
```
