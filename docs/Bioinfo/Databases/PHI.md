
[专栏描述](https://cloud.tencent.com/developer/article/2397525)

## PHI-base
病原体-宿主互作数据库（基因对病原菌致病性的影响）, [releases](https://github.com/PHI-base/data/tree/master/releases)。 

下载蛋白序列后，其 Header 中包含 [Phenotype of mutant - Definition of phenotypes](http://www.phi-base.org/helpLink.htm#fields)，csv中则交代数据来源、宿主、病原体等信息
```bash
wget https://raw.githubusercontent.com/PHI-base/data/master/releases/phi-base_current.fas   ## phi-base_current.csv
```

使用方法为BLAST，注意去除'#'符号
