
一些容易忘记的小技巧



### df filtering
参考：https://www.jianshu.com/p/cd957b3d6d4b
```
library(dplyr)
df_sub = df %>% filter(chr == 'chr1' || chr == 'chr2')
```


### Count list elements
```
> table(c('a','a','a','b','b','c','a'))
a b c 
4 2 1 
```


### Save plot
```
pdf('xxx.pdf',height = 10,width = 10)
## ...ploting
dev.off()
```


### patchwork 排版
https://zhuanlan.zhihu.com/p/384456335
```
wrap_plots(list(p1, p2, p3, p4))
p1 / (p2 | p3)
```


