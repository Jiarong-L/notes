可用三代数据辅助二代数据的组装软件

## Install
首先需要安装 numactl 与 boost; 随后下载release安装：（官方说不能用conda？？）
```bash
sudo apt-get install numactl

wget https://boostorg.jfrog.io/artifactory/main/release/1.83.0/source/boost_1_83_0.tar.gz
tar -xzf boost_1_83_0.tar.gz
cd boost_1_83_0
./bootstrap.sh
./b2 install
cd ..


wget https://github.com/alekseyzimin/masurca/releases/download/v4.1.0/MaSuRCA-4.1.0.tar.gz
tar -xzf MaSuRCA-4.1.0.tar.gz
cd MaSuRCA-4.1.0
## not working：BOOST_ROOT=install ./install.sh
BOOST_ROOT=$PWD/../boost_1_83_0/ ./install.sh
cd ..

export PATH=$PWD/MaSuRCA-4.1.0/bin/:$PATH
```


## Usage
```
masurca -t 16 -i R1.fq.gz,R2.fq.gz
masurca -t 16 -i R1.fq.gz,R2.fq.gz  -r nanopore.fq.gz  ##用二代数据纠正三代长reads
```


设置较多时使用 ```masurca config.txt``` 可生成 [**assemble.sh**](./MaSuRCA/assemble.sh)；  
**config.txt**示例：(参考：/install_path/sr_config_example.txt)
```
## If mean/stdev are unknown use 500 and 50 (safe values work for most runs)
## <two-character prefix> <fragment mean> <fragment stdev> <forward_reads> <reverse_reads(opt)>
## Use FULL_PATH !!! 
DATA
PE= pe 500 50  E_R1.fq.gz  E_R2.fq.gz
PACBIO=E_pacbio.fa
END

PARAMETERS
EXTEND_JUMP_READS=0
GRAPH_KMER_SIZE = auto
USE_LINKING_MATES = 0
USE_GRID=0
GRID_ENGINE=SGE
GRID_QUEUE=all.q
GRID_BATCH_SIZE=500000000
LHE_COVERAGE=25
LIMIT_JUMP_COVERAGE = 300
CA_PARAMETERS =  cgwErrorRate=0.15
CLOSE_GAPS=1
NUM_THREADS = 32
JF_SIZE = 200000000
SOAP_ASSEMBLY=0
FLYE_ASSEMBLY=1
END
```
```bash  ./assemble.sh``` 执行Pipeline



## 参考
Releases: https://github.com/alekseyzimin/masurca/releases  
