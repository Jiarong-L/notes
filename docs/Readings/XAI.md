
## SHAP


[SHAP](https://shap.readthedocs.io/en/latest/index.html) 提供模型参数的解释，目前已支持: NN, Tree Model, Linear Model, ... 示例见官网/[TreeExplainer](https://zhuanlan.zhihu.com/p/83412330)

其使用步骤:
```py
## 1. 训练 Explainer
explainer = shap.xxxExplainer(model, eX_train)
## 2. 计算解释值
shap_values = explainer.shap_values(eX)
## 3. 可视化
```

## 背景参考

1. [Explainable ML](https://zhuanlan.zhihu.com/p/339294365)
2. [XAI](https://blog.csdn.net/FelicityXu/article/details/121972644)
3. [XAI](https://cloud.tencent.com/developer/article/1552427)
4. [初探Explainable AI](https://zhuanlan.zhihu.com/p/238202269)




