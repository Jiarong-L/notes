
常见流程整合工具，可以提示流程是否成功运行；虽然更偷懒的方式是用自己熟悉的语言生成bash


| -- | 说明/示例 |
| -- | -- |
| [nextflow](https://www.nextflow.io/docs/latest/index.html) | [支持使用通配符读取文件](https://nextflow-io.github.io/patterns/) |
| [snakemake](https://snakemake.github.io/) | 不支持分布式计算 |
| [wdl](https://openwdl.org/getting-started/ ) | [GATK](https://github.com/gatk-workflows/gatk4-germline-snps-indels/blob/master/haplotypecaller-gvcf-gatk4.wdl) |
| [cwl](https://www.commonwl.org/getting-started/) | 最新款？？ |

[推荐参考1](https://www.zhihu.com/question/486052038/answer/2928510142)，[推荐参考2](https://blog.csdn.net/duoluka/article/details/127646163)，关联-[CMake](Make.md)



## WDL/Cromwell

workflow 包含/call tasks, tasks 包含 command + output；二者都需要声明使用的变量

**test.wdl**
```
workflow calltaskA {
  File? inFw
  Boolean hasInw
  String outSSw
  call taskA as tA{
    input:
      inF = inFw,
      hasIn = hasInw,
      outSS = outSSw
  }

  call taskB{
    input:
      TextB = tA.outtext
  }
}


task taskA {
  File? inF
  Boolean hasIn
  String outSS
  String commandText = if(hasIn) then "echo" + " inF" else "echo no inF"
  command {
    echo "hi" > ${outSS}.SS 
    ${commandText} >> ${outSS}.SS
  }
  output {
    File outF = "${outSS}.SS"
    String outtext = "ok A"
  }
}

task taskB {
  String TextB
  command {
    echo ${TextB} > log.txt
  }
}
```

**test.json** 传参给 wdl pipeline，格式：```“workflow_name.var1":"specific_var1",```；```hasInw=FALSE```时可以不加inFw（因为有?标识）
```
{
    "calltaskA.inFw":"myin.txt",
    "calltaskA.hasInw":"TRUE",
    "calltaskA.outSSw":"myout"
}
```

[**cromwell**](https://help.aliyun.com/zh/batchcompute/use-cases/cromwell-workflow-engine) 运行它
```bash
wget https://github.com/broadinstitute/cromwell/releases/download/86/cromwell-86.jar
java -jar cromwell-86.jar run test.wdl --inputs test.json 
```


太多log了，而且每个task一个文件夹，让事情更加复杂。。

runtime、parameter_meta、meta等是为了适配docker等，[参考 Backends](https://cromwell.readthedocs.io/en/stable/)



