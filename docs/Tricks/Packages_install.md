

### Python
```
pip install jupyter

pip uninstall jupyter
```

### Linux
```
apt upgrade

apt install <package_name>

apt remove <package_name>
```

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
如果win安装时候‘permission denied’，则管理员身份运行Rstudio即可；另一个参考：https://www.jianshu.com/p/1017b57f8d79
```
## Option 1
install.packages(c('dplyr','ellipse','getopt','ggalluvial','ggplot2','ggrepel','lubridate','plyr','RColorBrewer','Rmisc','tidyr','vegan','ggpubr','ggsignif','reticulate'),repo='https://mirrors.tuna.tsinghua.edu.cn/CRAN/')

## Option 2
install.packages(pkgs = "Tax4Fun2_1.1.5.tar.gz", repos = NULL, source = TRUE)

## Option 3
if (!requireNamespace("BiocManager", quietly = TRUE))
install.packages("BiocManager")
library(BiocManager)
BiocManager::install('xx')

## Option 4
library(devtools)
install_github('gertvv/gemtc')  
## or
devtools::install_github("junjunlab/ClusterGVis")

```
Option 5: conda装R包
```
conda activate myenv
conda install -c conda-forge r-stringi
conda install -c conda-forge r-stringr
```
更新
```
# 更新R
updateR()

# 更新library里所有包
update.packages()

# 重新install一下或者
devtools::update_packages()


```



