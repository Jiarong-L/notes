

Pytorch 使用 Dynamic Computational Graphs，与Eager模式下的Tensorflow类似


练习： [PytorchNN.ipynb](./Pytorch/PytorchNN.ipynb), [PytorchGAN.ipynb](./Pytorch/PytorchGAN.ipynb)
相关： [TensorflowcGAN.ipynb](./Pytorch/TensorflowcGAN.ipynb)


## Install

```
pip install torch
pip install torchvision
```
也可于此处下载： https://pytorch.org/get-started/locally/


## 基本操作

可以将张量移动到设备
```
t = torch.tensor([1,1,1])
t = t.to('cpu')
```

matmul 简写
```
y@y.T      ## y.matmul(y.T)  
```

设置 ```t.requires_grad``` 追踪对于该张量的所有操作，进行自动微分；注意，不适用于 non-scalar Tensor
```
t = torch.rand(2,2,requires_grad=True)     ## t.requires_grad = True
y = 2*t+5                                  ## y.requires_grad = True   y.grad_fn=AddBackward
z = y.mean()                               ## turn to scalar
z.backward()
t.grad                                     ## tensor([[0.5000, 0.5000],     dz/dt
                                           ##         [0.5000, 0.5000]])
```

简单的回归模型 ```f = w*x+b```
```
## x = batch_inputs, y = batch_labels
## ...  

w.grad.data.zero_()
b.grad.data.zero_()
for epoch in range(100):
    y_pred = torch.matmul(x,w) + b
    loss = (y-y_pred).pow(2).mean()       ## MSE = mean of (y-y_pred)^2
    loss.backward()
    with torch.no_grad():                 ## 这一步不需要再跟踪
        w.data -= w.grad.data * lr
        b.data -= b.grad.data * lr
```


## GAN 遇到的问题

1. 如果想要一个 optimizer 传入多个loss: 
```
optimizer = torch.optim.SGD([
    {'params':modelG.parameters()},
    {'params':modelD.parameters()}
    ], lr=1e-3)
```

2. [loss.backward() RuntimeError](https://zhuanlan.zhihu.com/p/666297208) 
```
RuntimeError: Trying to backward through the graph a second time (or directly access saved tensors after they have already been freed). Saved intermediate values of the graph are freed when you call .backward() or autograd.grad(). Specify retain_graph=True if you need to backward through the graph a second time or if you need to access saved tensors after calling backward.
```
需要按顺序放置，并且 retain_graph ：
```
        optimizer.zero_grad()
        lossG.backward(retain_graph=True)
        lossD.backward()
        optimizer.step()

```

3. 判别器过强可能导致生成器只能持续生成噪音（Generator Loss 上升，Discriminator Loss 下降）；但生成器也可能生成无意义但可以欺骗判别器的图像（Discriminator Loss 上升）：需要给生成器多一些训练步骤 / 加大生成器 learning rate

4. 每一步参与forward计算的参数都有gradient信息，不需要的时候（e.g.plot生成的FakeImgs）对其 ```FakeImgs.detach()```


## 参考

pytorch tutorials：https://pytorch.org/tutorials/      
torch-nn：https://pytorch-cn.readthedocs.io/zh/latest/package_references/torch-nn     
torchvision：https://pytorch.org/vision/stable/index.html    
tf eager：https://tensorflow.google.cn/guide/eager?hl=zh-cn    
常见激活函数：https://zhuanlan.zhihu.com/p/172254089    
cifar10 转jpg：https://blog.csdn.net/ctwy291314/article/details/83864405    
