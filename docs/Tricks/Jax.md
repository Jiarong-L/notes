


Jax提供自动微分和 JIT 编译功能，不过[@jit](https://jax.ac.cn/en/latest/jit-compilation.html)只能用于静态的func！否则参考‘[有状态计算](https://jax.ac.cn/en/latest/stateful-computations.html)’

jnp操作类似np, 而PyTree类似dict，[具体区别](https://jax.ac.cn/en/latest/notebooks/Common_Gotchas_in_JAX.html)包括 数组更新不可in_place更新 等

与TF基本通用



## 安装

```py
pip install -U jax
pip install -U flax
```

一些基本操作：[Basics_Jax.ipynb](https://github.com/Jiarong-L/GAN_tutorial/blob/main/Basis/Basis_Jax.ipynb)

如何进行NN训练：[Basics_Jax_NN.ipynb](https://github.com/Jiarong-L/GAN_tutorial/blob/main/Basis/Basics_Jax_NN.ipynb)



## 参考

```bash
官方教程 https://jax.ac.cn/en/latest/

安装报错1 https://blog.csdn.net/duoyasong5907/article/details/142324484

纯Python函数的回调!!  https://jax.ac.cn/en/latest/_autosummary/jax.pure_callback.html

教程  https://www.bilibili.com/video/BV1TppqeAEPN/?spm_id_from=333.1007.0.0
```
