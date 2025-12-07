<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
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
    width: 60%;
}
</style>


一些经常被使用的设计

关于DL的基础，可以参考 [CS231n 课程笔记](https://cs231n.github.io/) ，[深度学习（花书 Ian Goodfellow）](https://github.com/exacity/deeplearningbook-chinese)，[Easy-RL](https://datawhalechina.github.io/easy-rl/)


## Transformer

[Attention Is All You Need -- Figure 1: The Transformer](https://arxiv.org/pdf/1706.03762)

[一个简单的数值示例 .ipynb](https://github.com/Jiarong-L/GAN_tutorial/blob/main/Basis/Transformer_PyTorch.ipynb)

Multi Head Attention 就是将多个并行输出的 Attention 进行 weighted sum

如果 K、Q 均来自同一组输入，称之为自注意力（self-attention）

------------------------------------------------------------------------------------------------------------------------------

$attention = softmax(\frac{QK'}{\sqrt{d_K}})V$

```bash
某个批次的输入矩阵 [batch, seq_len, token_embd]
W_ 是可学习的权重矩阵  [token_embd, d_k（用户自定义）]

Q = input @ W_Q    ## query [batch, seq_len, d_k] <== (b,seq,emb) × (emb,d_k)
K = input @ W_K    ##   key [batch, seq_len, d_k]    
V = input @ W_V    ## value [batch, seq_len, d_k]

可见 batch, seq_len 的变化都不影响 W_ 的形状，只要batch内部序列长度对齐就行了

注：NLP中我们会将句子拆成一系列tokens、每个token就是一个向量（token_embd，论文里写成 d_model）
```

上文的 token_embd 中也可以附上 **Positional Encoding** 信息，即将 Transformer 的输入变成 ```concat(token_emb, position_enc)```

$PE_{(pos,2i)} = sin(pos/10000^{2i/d_{token}})$   
$PE_{(pos,2i+1)} = cos(pos/10000^{2i/d_{token}})$  

其中，$pos$指token在句子中的定位，$i$指在token向量中的定位


## Diffusion Model

从噪音生成图像/学习如何**渐进式的**去噪：```T=t (Noise) --> T=t-1 (Less Noisy) --> ...  --> T=0 (Original Image)```

训练过程即：```AddNoise --> (Noise) --> Denoise```

经典模型：[DDPM](https://zhuanlan.zhihu.com/p/563661713)的去噪过程通常需要迭代1000步、适合高质量图像生成；[DDIM](https://www.cnblogs.com/myhz/p/18265650)加快生成速度（通常只需50-100步）、但在复杂纹理上略逊

（忽略论文的公式吧，反正图像loss最终还是MSE）

最近好像流行 Flow Model？（[主流生成模型](https://1wata.github.io/2025/05/20/ai/generative_ai/normalizing_flow_models/)）


## Autoregressive Models

[什么是自回归模型？](https://aws.amazon.com/cn/what-is/autoregressive-models/)

$p(x_t) = \prod \limits_{i=1}^{t-1} p(x_i|x_1, x_2, ... , x_{i-1})$

$y_t = c + \sum \limits_{i=1}^{p}\phi_i y_{t-i} + \epsilon_t$

对于文本：给定前面的词，预测下一个词（似乎很久之前RNN/LSTM就是这样）

## Multimodel ML

[多模态学习 - 知乎](https://zhuanlan.zhihu.com/p/582878508)





