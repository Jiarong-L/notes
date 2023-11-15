
GNU： 一个 自由软件操作系统   
GCC： GNU **Compiler** Collection   
Make工具： 通过调用makefile文件中用户指定的命令来进行编译和链接   
CMake： 跨平台生成对应平台的makefile


## GCC
GCC是GNU平台的编译器集合，支持C、C++、Java、Objective-C 等多种编程语言。下文默认示例为C，对于C++，将命令中的gcc改为g++即可

### 常见后缀
| 后缀 | 说明 | 其它 | 示例 |
| -- | -- | -- | -- |
| .a | 静态库 | 编译过程中被载入，static object library (archive) <br>```ar -r [libname.a] [.o][.o]...``` 生成 | 若有错，编译时报错;主程序编译完成后删除引用的.a无影响 |
| .so | 动态库 | 程序运行后被载入，shared object library <br>```gcc -shared [.o][.o]... -o [libname.so]``` 生成 | -- |
| .c | C源码 | -- | [hello.c](Make/hello.c) |
| **.cpp** | C++源码 | .C .cc .c++ .cp .cpp .cxx | -- |
| .h | C/C++ header 文件 | .hpp->C++ | -- |
| .i | 预处理后的C源码 | 预处理器(cpp)根据```#```开头的命令修改.c源码文本，例如：直接插入需要include的header文件内容 | [hello.i](Make/hello.i) |
| **.ii** | 预处理后的C++源码 | -- | -- |
| .o | 可重定位目标程序 | 二进制 | [hello.o](Make/hello.o) |
| .s | 汇编程序文本 | -- | [hello.s](Make/hello.s) |

<br>

以[add.c](Make/add.c)、[minus.c](Make/minus.c)为例,   

* .a静态库示例:
```bash
gcc -c add.c  minus.c                       ##  add.o  minus.o
ar -r libname.a add.o  minus.o              ##  libname.a

## use .a lib
gcc hello.c libname.a -o hello_a
gcc hello.c  add.o  minus.o -o hello_direct  ## 默认变成.a静态库后编译
```

* .so动态库示例: **注意，**libxxx.so，-l 应填写xxx; -L是libxxx.so所在的文件夹
```bash
gcc -c -fpic add.c  minus.c                 ##  add.o  minus.o
gcc -shared  add.o  minus.o -o libname.so   ##  libname.so

## use .so lib
###  gcc [.c] -o [exec_file] -l [libname] -L [lib PATH]; 
###                 add in makefile:-Wl,rpath[lib PATH]
gcc hello.c -o hello_so -l name -L ./
```

### 常用指令
* gcc：识别后缀以决定调用C/C++ compiler，链接、编译程序 (不会自动链接STL)
* c++/g++：调用C++ compiler，链接、编译C++程序 (自动链接标准库STL)
* configure：配置值、创建makefile
* [Options for Linking](https://gcc.gnu.org/onlinedocs/gcc-13.2.0/gcc/Link-Options.html): 
    - ```g++ -stdlib=...``` 指定C++运行时库；此外还有```-static/-pie``` (dynamic linking)，```-shared``` 等选项
    - [libstdc++](https://gcc.gnu.org/onlinedocs/libstdc++/)：g++默认的C++运行时库，包含标准语言的所有C++类和函数
    - [libgcc](https://gcc.gnu.org/onlinedocs/gccint/Libgcc.html)：低级运行时库，包含一些目标处理器不能直接执行的算术运算（如 浮点操作）
    - [glibc](https://www.gnu.org/software/libc/)：the core libraries for the GNU/Linux systems
* **疑问**：libgcc与glibc交叉编译？```gcc -shared-libgcc``` needs to build supplementary stub code for constructors to work
* ```gcc -v -x c -E``` 查看默认header路径
* [GNU Binutils](https://www.gnu.org/software/binutils/)


### C编译步骤
C在执行编译时， ```gcc -o hello hello.c```可依次拆解为：

* 预处理：预处理器(cpp)根据```#```开头的命令修改C源码文本，例如：直接插入需要include的header文件内容
* 编译：编译器(ccl)将C文本转换为汇编文本
* 汇编：汇编器(as)将汇编文本翻译为机器语言指令
* 链接：链接器(ld)链接多个文件，汇合成一个可执行文件；例如: 当 hello程序 需要调用 printf.0 时
```bash
gcc -E hello.c > hello.i     # 预处理, 源码[文本]->预处理源码[文本]     via 预处理器cpp
gcc -S hello.c -o hello.s    #                  ->汇编程序[文本]       via 编译器ccl
gcc -c hello.c -o hello.o    #                  ->可重定位目标程序[二进制]   via 汇编器as
gcc hello.c -o hello         #                  ->可执行目标程序[二进制]     via 链接器ld
```
tips: 每一步输入包含多个文件时，依次放置即可，例如：```gcc -c add.c  minus.c```




## Make

### 基本格式
```Makefile
targets : prerequisties
[tab]command

.PHONY: plabel
plabel:
[tab]command
```
* targets/prerequisties 可以是 label/执行文件/ObjectFile
    - 根据command生成targets文件或label
    - 若当前目录存在targets文件，且早于prerequisties文件生成，会重新生成targets文件；不然就直接使用这个targets文件
* .伪目标只是 label
    - 需要用.PHONY声明伪目标；防止其与本目录文件混淆


#### 示例一
在运行文件夹生成'Makefile' （也可以是'makefile'，无需后缀）；随后命令行运行：```make all```
```Makefile
files := 1.txt 2.txt

all: hello create clean

hello:
	echo "Hello, World"

create: 
	@touch $(files)
	@ls 1.txt

.PHONY: clean
clean:
	rm -r $(files)
```
* ```make all``` 相当于依次执行 ```make hello; make create; make clean```
* ```@``` 隐藏运行的命令，只输出结果
* 如果当前目录存在一个'clean'文件，同时又没有声明 ```.PHONY: clean``` ；会显示 ```make: 'clean' is up to date.``` （将clean视为'clean'文件）


#### 示例二
```Makefile
exec: nofile
	@echo 'exec running'

nofile: routine.o
	@echo 'nofile running'

routine.o: base.c
	@echo 'routine running'
	@cat base.c > routine.o

base.c:
	@echo 'base running'
	@echo 'Hello' > base.c
```


第一次运行```make exec``` ：层层下推运行以取得 prerequisties
```
routine running
nofile running
exec running
```

第二次运行```make exec``` ：routine.o已存在，无需再运行生成
```
nofile running
exec running
```
此时运行 ```make routine.o``` 显示 ```make: 'routine.o' is up to date.```；但如果更新 base.c (使targets文件早于prerequisties文件生成) 再运行 ```make routine.o``` 则显示 ```routine running```


### 变量
```Makefile
var1 := value1
var2 := value2
var3 := value3

.PHONY:exec
exec:${var3}

${var3}: ${var1} $(var2)
	@echo $@      ## target
	@echo $<      ## 1st prerequisties
	@echo $^      ## all prerequisties


${var1}:
	@echo 'get var1'

${var2}:
	@echo 'get var1'	
```
* ```=```是简单的赋值符号，左值将随右值而改变；```:=```立即赋值，右值改变但左值不会随之更改；```?=```对未定义变量进行赋值 (i.e.若此变量已有赋值，```?=```将不做改变)
* ```+=``` 累加：str或int
* ```\``` 续行符：当代码过长时
* ```val := AA```时, ```$(val:%=XX%)``` 返回 ```XXAA```；相当于在val变量前加上某些短句

### 函数
函数调用方法：
```Makefile
callfn := $(fn  args)         ## ${fn  args}

## fn: 函数名
## args: 参数，以','分隔
```

| 常用函数 | 示例 | 说明 |
| -- | -- | -- |
| shell | ```$(shell find . -name '*.c')``` | -- |
| subst | ```$(subst aa,X,aaaaa)```<br> output: XXa | ```$(subst <from>,<to>,<text>)``` <br> 将text中from字段依次替换为to字段 |
| patsubst | ```$(patsubst %.a, X, a.a b.b c.c)```<br> output: X b.b c.c  | ```$(patsubst <pattern>,<to>,<text>)``` <br> 将text中符合pattern的字段替换为to字段 |
| filter | ```$(filter %.a, a.a b.b c.c)```<br> output: a.a  | 获取符合pattern字段 |
| foreach | ```$(foreach  i,'1 2 3',-L${i})```<br> output: -L1 -L2 -L3  | ```$(foreach  <var>,<list>,<text>) ```<br> for each var in list, do text  |
| dir | ```$(dir /d1/aa d2/bb)```<br> output: /d1/ d2/ | ```$(dir <names>)```<br> 取文件名序列中的目录(最后一个```/```前部分) |
| notdir | ```$(notdir /d1/aa d2/bb)```<br> output: aa bb | ```$(notdir <names>)```<br> 取文件名序列中的文件名(最后一个```/```后部分) |
| basename | ```$(basename aa.ao bb.bo)```<br> output: aa bb | ```$(basename <names>)```<br> 去除后缀 |


### C/C++编译

| 选项 | 说明 | 其它 |
| -- | -- | -- |
| ```-m64``` | 编译为64位程序 | -- |
| ```-std=``` | 编译标准 | ```-std=c++11```,```-std=c++14``` |
| ```-g``` | 包含调试信息 | -- |
| ```-w``` | 不显示警告 | -- |
| ```-O``` | 优化等级 | c++通常 -O3 |
| ```-I``` | header文件路径 | -- |
| ```fPIC``` | 全使用相对地址 | 无绝对地址；代码可以被加载到内存的任意位置执行(共享库所要求的，其被加载时于内存的位置不固定) |
| ```-l``` | 库名 | libxxx.so，-l 应填写xxx |
| ```-L``` | 库路径 | libxxx.so所在的文件夹 |
| ```-Wl,<option>``` | -- | 将','分隔的option传递给ld |
| ```rpath=``` | -- | 运行时去此目录下寻找.so文件 |

[**Implicit Rules**](https://www.gnu.org/software/make/manual/html_node/Implicit-Rules.html)

* 当 targets/prerequisties 没有被明确的规则定义的时候，Make会使用相应的隐含规则来实现，e.g. 语句```x: y.o z.o```需要的.o文件当前不存在且没指定生成，make会生成 x/y/z.o 再 ```cc x.o y.o z.o -o x```
* CC, CXX, CFLAGS, CXXFLAGS, CPPFLAGS, LDFLAGS


C编译步骤示例：(动/静态库同样参考上文，其中动态库增加```-Wl,rpath=```)
```makefile
c_srcs := $(shell find . -name '*.c')
c_objs := $(patsubst %.c, %.o, $(c_srcs))

%.o : %.c
	@gcc -c $< -o $@                  ##c++ add flags: -g -O3 -std=c++ -L 
	@echo 'Generating ' $@

exec : $(c_objs)
	@gcc $^ -o $@
	@echo 'Generating ' $@ ' from ' $^

run : exec
	@./$<
	@echo 'running ' $<

.PHONY : clean
clean :
	@rm *.o exec
```


## CMake

* VSCode中安装 CMake、CMake Tools插件，```Ctrl+Shift+p``` 打开指令面板，输入 ```cmake:q``` 快速启动项目，可以得到 main.c 与 CMakeLists.txt 文件
* 对照 [CMake Docs](https://cmake.org/cmake/help/v2.8.12/cmake.html) 可知其含义
* CTest为当前目录，test为设定的项目名称
```
cmake_minimum_required(VERSION 3.0.0)
project(test VERSION 0.1.0 LANGUAGES C)

include(CTest)
enable_testing()

add_executable(test main.c)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```
随后运行```cmake CMakeLists.txt``` 可得到 Makefile


## 参考
makefile, autoconf, automake, libtool: https://blog.csdn.net/zhizhengguan/article/details/112008982   
GCC: https://gcc.gnu.org/onlinedocs/   
GCC Option-Summary: https://gcc.gnu.org/onlinedocs/gcc-13.2.0/gcc/Option-Summary.html    
Make: https://makefiletutorial.com/     
CMake : https://cmake.org/documentation/   
CMake easy: https://zhuanlan.zhihu.com/p/371257515  

