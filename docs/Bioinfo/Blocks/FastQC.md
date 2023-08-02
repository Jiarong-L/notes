


## Install
```
conda install fastqc -y
```
注意，如果出现以下错误，则需要**本地打开[Xming](https://sourceforge.net/projects/xming/)**，然后```export DISPLAY=localhost:0```
```
Exception in thread "main" java.awt.AWTError: Can't connect to X11 window server using 'localhost:0' as the value of the DISPLAY variable
```
（参考[Linux Tricks](../../Tricks/Linux.md#graphic)）

## Usage
```
mkdir OutDir
fastqc -t 12 -o OutDir E_R1.fq.gz E_R2.fq.gz
```

## Result
```
ls OutDir

E_R1_fastqc.html  E_R1_fastqc.zip  E_R2_fastqc.html  E_R2_fastqc.zip
```
示例报告: [E_R1_fastqc.html](FastQC/E_R1_fastqc.html)


## 参考
https://zhuanlan.zhihu.com/p/88655260



