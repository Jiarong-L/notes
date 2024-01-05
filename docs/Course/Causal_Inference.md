---
header-includes:
  - \usepackage{MnSymbol}      ## $\upmodels$ 失败
  - \usepackage{amssymb}
  - \usepackage{amsfonts}
  - \usepackage{fdsymbol}      ## $\Vbar$ 失败
output:
  pdf_document:
    keep_tex: true
---

<script>
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']]
  },
  svg: {
    fontCache:   'global'   // 'local',or 'global' or 'none'
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
table th:nth-of-type(5) {
    width: 20%;
}
</style>

<!-- https://bearnok.com/grva/en/knowledge/software/mathjax -->
<!-- https://tex.stackexchange.com/questions/562924/how-to-add-latex-packages-to-markdown -->



TBA



| 图胚公理 | -- | $\perp$表示相互独立（默认：Z条件下） |
| -- | -- | -- |
| $(X \perp Y \| Z) \Rightarrow (Y \perp X \| Z)$ | 对称性 | “从节点子集X到节点子集Y的路径均被节点子集Z阻断” |
| $(X \perp YW \| Z) \Rightarrow (X \perp Y \| Z)$ | 分解性 | 如果YW与X无关，其拆分项W、Y也都与X无关 |
| $(X \perp YW \| Z) \Rightarrow (X \perp Y \| ZW)$ | 弱联合性 | 由 分解性 可知拆分项W、Y都与X无关，那么，得知W并不能使Y变得与X相关 |
| $(X \perp Y \| Z) \& (X \perp W \| ZY)$ $\Rightarrow (X \perp Y \| Z) \& (X \perp W \| Z)$ $\Rightarrow (X \perp YW \| Z)$ | 收缩性 | 如果得知与X无关的Y后判定W与X无关，那么，得知Y之前W也与X无关 |
| $(X \perp W \| ZY) \& (X \perp Y \| ZW) \Rightarrow (X \perp YW \| Z)$ | 相交性 | 如果得知W后Y与X无关 且 得知Y后W与X无关，则W、Y都与X无关 |






