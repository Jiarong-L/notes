
TBA

# Chip-seq 
设计针对目标蛋白的抗体，提取目标蛋白、得到与目标蛋白结合的DNA序列。每次只能针对一个目标蛋白。  
使用ATAC-seq得到全基因组范围内的TFBS后，可结合Chip-seq进行验证

常见的目标蛋白是 TF 或者 Histone


## Pipeline

空白对照：input DNA（不含抗体捕获）, mock IP DNA（不含抗体）




peak-calling  ---> 减去背景噪音（空白对照）  ---> UCSC基因浏览器








