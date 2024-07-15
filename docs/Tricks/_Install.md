

### Python

如果超时，可以配置国内的源：
```
pip config set global.index-url http://pypi.douban.com/simple

pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
```
写入：C:\Users\.....\AppData\Roaming\pip\pip.ini

```
pip install jupyter

pip uninstall jupyter
```

### Linux

[设置清华源](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)：首先备份旧文件
```
cd /etc/apt
sudo mv sources.list sources.list.old
```
随后生成新的 sources.list
```
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ jammy-backports main restricted universe multiverse
deb http://security.ubuntu.com/ubuntu/ jammy-security main restricted universe multiverse
```

随后记得 ```sudo apt-get update``` 或者  ```sudo apt-get upgrade``` ；之后就可以正常下载软件了：

```
apt install <package_name>

apt remove <package_name>

apt-cache madison <package_name>    ## list version
```


### conda

注意，WSL中Miniconda只能装在/home/，如果装在win盘中则会 ```OSError: [Errno 40] Too many levels of symbolic links```

生成环境+装包
```
conda update --all -y # update packages

conda create --name myenv
conda activate myenv
conda install -c conda-forge r-base


## same as: 
## conda install -n myenv -c conda-forge r-base
## conda create -n myenv -c conda-forge r-base
```
查看环境 删除环境 或 环境中的包
```
conda info --envs

conda remove -n $env_name --all
conda remove --name $env_name $package_name
```
删除单个包（uninstall 时常出错，改用 remove）；如果再删不了，就直接删除conda bin里的程序吧
```
conda uninstall $package_name
```


[conda配置源](https://help.mirrors.cernet.edu.cn/anaconda/)  ```conda config --add/remove channels ```
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
conda config --set show_channel_urls yes

conda config --show channels
```

conda删除源 （源过多会导致错误），如果 ```conda config --set channel_priority flexible``` 也无法解决，就需要手动删除以前配置的源 （也可直接修改~/.condarc）
```
conda config --show channels   ## 查看已安装的源

conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
```

conda搜寻/安装/特定版本
```
conda search -c bioconda diamond 
conda install -c bioconda diamond=2.1.6
```

conda打包yml
```
activate myenv
conda env export > environment.yml
```
conda根据yml生成环境
```
conda env create -f environment.yml
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

* 不用鼠标选择源： 
    - ```chooseCRANmirror(graphics=F)```
    - ```chooseBioCmirror(graphics=F)```
    - [Bioconductor的源](https://www.bioconductor.org/about/mirrors/)

```R
options(BioC_mirror="https://mghp.osn.xsede.org/bir190004-bucket01/archive.bioconductor.org/")
options(repos = c(CRAN="https://mirrors.tuna.tsinghua.edu.cn/CRAN/"))
```



* 有时下载失败，可能需要安装 r/apt 的 openssl，或者更换源，或者干脆设置 ```options(timeout=50000)```


### JAVA
用Maven管理依赖包；IntelliJ IDEA设置一下maven地址

