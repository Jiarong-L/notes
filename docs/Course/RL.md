<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache: 'global'
  }
};
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
</script>


<style>
img{
    width: 60%;
}
</style>



参考：[EasyRL - 蘑菇书](https://datawhalechina.github.io/easy-rl/)，CS285旧笔记（见文件夹）

练习工具：[Gymnasium](https://gymnasium.org.cn/introduction/basic_usage/) 为一些常见的强化学习项目提供环境反馈


## 符号表

*t* - timestep *t*  
$s_t$ - state     
$o_t$ - observation   
$a_t$ - action   
$\pi_\theta(a_t|o_t)$ - policy (partially observed)  
$\pi_\theta(a_t|s_t)$ - policy (fully observed)    
$p_{data}(o_t)$ - 符合data分布的数据，i.e. 采样得到的observation   
$p_{\pi_\theta}(o_t)$ - 符合$\pi_\theta$分布的数据，i.e. 运行model得到的新observation    
$\tau$ - Trajectory，运行model得到的一系列($s_t$,$a_t$)组合



## 基本知识




