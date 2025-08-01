


* BS-seq：Bisulfate(BS)处理DNA序列后，可将暴露状态的C变成U(再一轮复制后变成T)，而甲基化的C则不受改变
    - WGBS：用 BSMAP 将全基因组[BS-seq测序](https://www.illumina.com.cn/techniques/sequencing/methylation-sequencing.html)数据 map 至 参考基因组上，可得到全基因组水平的甲基化信息
    - RRBS：富含 CCGG 位点的DNA片段后再BS-seq测序、map... （高性价比）
    - Chip：Illumina提供[Infinium 芯片](https://www.illumina.com.cn/techniques/microarrays/methylation-arrays.html)，以bp分辨率检测CpG位点；[GenomeStudio软件](https://www.illumina.com.cn/techniques/microarrays/array-data-analysis-experimental-design/genomestudio.html )可对Illumina芯片平台生成的数据进行可视化与分析


分析工具：[Bismark](https://docs.hpc.sjtu.edu.cn/app/bioinformatics/bismark.html)



