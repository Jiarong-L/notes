


## Install
```
conda install fastqc -y
```
注意，需要**本地打开[Xming](https://sourceforge.net/projects/xming/)**，然后```export DISPLAY=localhost:0```，否则报错:
```
Exception in thread "main" java.awt.AWTError: Can't connect to X11 window server using 'localhost:0' as the value of the DISPLAY variable
```
（参考[Linux Tricks](../../Tricks/Linux.md#graphic)）

## Usage
```
fastqc -t 12 -o OutDir E_R1.fq E_R2.fq
```

## Result




## 参考
https://zhuanlan.zhihu.com/p/88655260



