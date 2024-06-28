

* [LIME](./XAI/LIME.png): 用可解释的模型（线性回归/决策树）等模拟大模型的输出
* Local Explanation: 数据中的什么特征影响了模型的决策？Why do you think its a dog? 
    - 对输入图像进行固定大小的Mask，查看何处对acc/loss影响较大（[Occlusion Sensitivity](./XAI/1.png)）；寻找最小的Mask，以达成对acc/loss的最大影响（ [Deletion Game](./XAI/2.png)）
    - 基于Gradient（dX/dY）：Pixel值的扰动对结果的扰动影响（Saliency Map）；选取一个平均x作为参考背景（[Integrated Gradients](http://home.ustc.edu.cn/~liujunyan/blog/Integrated-Gradients-IG/)）
* Global Explanation: 模型认为图像应该长什么样？What does a dog looks like?
    - GAN生成假图像
    - [Optimize 图像直到它可以骗过模型（加图像复杂度限制。令其更接近人类可理解的图像）](./XAI/3.png)
* [Attention](https://github.com/jessevig/bertviz)



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

SHAP 枚举不同feature加入模型中的顺序，评估它们对结果的贡献，取均值，[示例](./XAI/SHAP.png)




## 背景参考

1. [Explainable ML](https://zhuanlan.zhihu.com/p/339294365)
2. [XAI](https://blog.csdn.net/FelicityXu/article/details/121972644)
3. [XAI](https://cloud.tencent.com/developer/article/1552427)
4. [初探Explainable AI](https://zhuanlan.zhihu.com/p/238202269)
5. [XAI 视频介绍](https://www.bilibili.com/video/BV1c94y1P7vC/)
6. [XAI](https://blog.csdn.net/wxc971231/article/details/121184091)
7. [**Captum: Model Interpretability for PyTorch**](https://captum.ai/tutorials/)
8. [Usable XAI: 10 Strategies Towards Exploiting Explainability in the LLM Era](https://github.com/JacksonWuxs/UsableXAI_LLM)
