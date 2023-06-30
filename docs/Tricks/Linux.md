


## .bashrc
此处可设置各种简写（e.g.你自己写的小工具脚本、工作目录），R librarys ...
```
alias cdd='cd /mnt/d/WSL_dir/workdir/'
```



## PATH
```
export PATH=...../anaconda3/bin/:$PATH
```


## Convert img
ref: https://www.cnblogs.com/yymn/p/4479805.html
```
## ImageMagick:  sudo apt install graphicsmagick-imagemagick-compat

convert  in.pdf  out.png
convert -resize  50%x50%  in.png  out.png
```

## strings
查看二进制文件
```
strings /lib/x86_64-linux-gnu/libm.so.6 |grep GLIBC_
```

## GLIBC
系统版本的GLIBC版本过低，于是添加一个高级版本系统的源，[参考](https://blog.csdn.net/huazhang_001/article/details/128828999)
```
sudo vi /etc/apt/sources.list

## ADD TO FILE:   
## deb http://th.archive.ubuntu.com/ubuntu jammy main

sudo apt update
sudo apt install libc6
```

## nohup & 中止
```
nohup xx.sh & 

jobs -l   只能列出当前窗口的
ps -aux   查看所有人的任务

kill -9 <PID>
```

## qsub
```
qsub -l h=hpc0[12345],vf=30G,p=15  xx.sh
qdel：取消作业
qhold：挂起作业
qstat: 查看情况
```

## find
```
find  <dir> -name '**'
```


## Bash
```
echo -n    ## 不换行输出

for dd in {1..5}; do echo $dd ; done
for dd in {1..30}; do echo "my_${dd}_word" ; done   ## must be ""
for dd in {1..5}; do if [ $((dd))+1 != $((3)) ];then echo $((dd +10)) ; fi; done   ## $((string)) convert str to num

ls img/ | while read dd ; do convert -resize 10%x10% img/$dd img_resize/$dd ; done

sed -n 's/from/to/g' xx.fa | less

```
* sed: https://www.runoob.com/linux/linux-comm-sed.html
* awk: https://www.runoob.com/linux/linux-comm-awk.html
* grep: https://www.runoob.com/linux/linux-comm-grep.html  



## SSH
### 简单使用
本地.ssh/config文件示例
```
Host vm1
    HostName <ip>
    User user_name
    Port 10007
    LocalForward 8888 localhost:8888
```
命令行中：
```
ssh vm1
```
第一次登陆有可能需要设置：不使用主机公钥确认
```
ssh -o StrictHostKeyChecking=no vm1
```
### 免密码
清除本地电脑上旧的公钥信息
```
ssh-keygen -R vm1
### or
rm ~/.ssh/known_hosts
```

生成id_dsa并拷贝给远程机器的authorized_keys,此后可以免密登录/拷贝
```
ssh-keygen                                    ## generate id_dsa
ssh-copy-id  -i ~/.ssh/id_rsa.pub  vm1
```


## Graphic
有时候可能需要运行带有GUI或者display/gnuplot，这种情况需要通过 PuTTy/WSL + Xming；方法：[link1](https://blog.csdn.net/Yinyaowei/article/details/108303562),[link2](https://blog.csdn.net/sihsd/article/details/124261374)

```
export DISPLAY=localhost:0
```




