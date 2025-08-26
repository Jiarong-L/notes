

一般用替代矩阵对蛋白质序列联配进行打分，或者对序列进行embedding

## BLOSUM

BLOSUM62 以62%一致性对SWISS-PORT进行局部多重联配（得到许多高度保守的较短区域---无Gap的Blocks），然后对Block中联配计算所有可能的氨基酸对的替代频率

```
           Block     Block              no gap inside Blocks
           +++++     +++++
       ----XAXXX-----XXXXXX--------
       ----XAXXX--X--XXXXX--------      62% similarity alignment
       ----XBXXX-----XXXXX--------        
       ----XAXXXX----XXXXX--------
       ----XCXXX-----XXXXX--------
       ----XAXXX-----XXXXX--------

 A = ...    4     ...           
 B = ...    1     ...           
 C = ...    1     ...
AA = ...    6     ...                q_A = A / (A+B+C)  
AB = ...    4     ...                q_B = B / (A+B+C)
AC = ...    4     ...                p_AB= AB/ SUM(**)
BB = ...    0     ...                              ## real/random
BC = ...    1     ...                S(A,B) = 2*log2[p_AB/(q_A*q_B)]    or
CC = ...    0     ...                S_AB=SUM[ S(A,B) in all position ]  is the score in BLOSUM62 Matrix
```

[NCBI-BLOSUM62](https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/BLOSUM62)

[doi:10.1073/pnas.89.22.10915](https://sci-hub.se/10.1073/pnas.89.22.10915)


## PAM

假设基因发生点突变，改变其编码的氨基酸，且该突变在自然选择过程中被保留

1-PAM 矩阵的计算：[参考](https://zhuanlan.zhihu.com/p/643775292)
```
Step1. 构建系统发育树（该树给出了最少的可解释进化过程，但不一定代表完整的进化过程），统计氨基酸突变数据

                            Seq(4)                                点突变矩阵A    
                ADGHG   DEGHG    AEIKC    CDIHC              A  C  D  E  G  H  I  K
                  \       /        \       / A-C          A     1  1
               E-D \     / A-D   H-K\     / E-D           C  1           1
                    AEGHG            AEIHC                D  1        2
                      \                 /  I-G            E        2
                       \               /   C-G            G     1              1
                        \_____________/                   H                       1
                                                          I              1
                                                          K                 1


Step2. 统计每一次联配
            ADA
            ADB
                A      B      D
所有            3      1      2
突变            1      1      0
相对突变率      1/3    1/1    0/2            m_a = 突变a/所有a ；通常以m_丙氨酸为基准


Step3. 对一条长度为L的蛋白质序列，设定未突变残基的百分比Lambda=99，即每100碱基有1个保留突变（1-PAM），则有 Lambda * m_j 个突变属于氨基酸j，其中有 A_ij / SUM_i(A_ij) 的概率突变为氨基酸i

M_ij = Lambda * m_j * A_ij / SUM_i[A_ij]    if i != j       （j-->i突变的概率）???
M_ij = 1 - Lambda * m_j                     if i == j       （氨基酸保持不变的概率）


PAM1矩阵即 M*100  ## scale factor
```

[NCBI-PAM250](https://www.ncbi.nlm.nih.gov/IEB/ToolBox/C_DOC/lxr/source/data/PAM250) 表示发生250次进化事件（进化距离250），即 1-PAM 矩阵250次方后得到 250-PAM 矩阵




## Embedding

参考[BeeTLe](https://github.com/yuanx749/bcell)，将BLOSUM62用作Embedding Layer的初始参数


```py
a = ## BLOSUM62_np
emb_size = ##
AAs = ["<pad>"] + list("ACDEFGHIKLMNPQRSTVWY") + ["<unk>"]   ## with tokens

w, v = linalg.eigh(np.exp2(a))
v = v * np.sign(v[0])
mat = v.matmul(np.diag(w**0.5))
mat = mat / linalg.norm(mat) * len(mat)
weight = np.eye(len(AAs), M=emb_size, k=-1)
weight[1:21, 0:20] = mat
torch.tensor(weight, dtype=torch.float)
```


