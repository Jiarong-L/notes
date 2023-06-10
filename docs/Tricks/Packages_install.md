

### conda

生成环境+装包
```
conda update --all -y # update packages

conda create --name myenv
conda activate myenv
conda install -c conda-forge r-base
```
删除环境 或 环境中的包
```
conda remove -n $env_name --all
conda remove --name $env_name $package_name
```
conda配置清华源
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --set show_channel_urls yes
```



### R
```
## Option 1
install.packages(c('dplyr','ellipse','getopt','ggalluvial','ggplot2','ggrepel','lubridate','plyr','RColorBrewer','Rmisc','tidyr','vegan','ggpubr','ggsignif','reticulate'),repo='https://mirrors.tuna.tsinghua.edu.cn/CRAN/')

## Option 2
install.packages(pkgs = "Tax4Fun2_1.1.5.tar.gz", repos = NULL, source = TRUE)

## Option 3
library(BiocManager)
BiocManager::install('xx')

## Option 4
library(devtools)
install_github('gertvv/gemtc')
```
Option 5: conda装R包
```
conda activate myenv
conda install -c conda-forge r-stringi
conda install -c conda-forge r-stringr
```




