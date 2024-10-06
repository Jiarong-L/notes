


[博主 GeekHour](https://www.bilibili.com/video/BV1fm411C7fq) 整理了常见的正则表达式 [RegexCheatSheet-ByGeekHour.pdf](RegEx/RegexCheatSheet-ByGeekHour.pdf)，并推荐 [RegExr](https://regexr.com/) 处进行尝试。但仍需注意：各软件支持的正则版本不同，不一定生效



常用：

```
\bword\b     单词边界
(P|p)a       Pa/pa
(at){3}      atatat
at{3}        attt
at{3,}       attt/atttttttttt... 贪婪模式
at{3,}?      attt(若有)  非贪婪模式
at[A-Z]      atA/atB/.../atZ
at[^A-Z]     at1/ata/...    [^]表示取反
^at$         $表示行的末尾   ^表示行的开头
xx(\d{3})yy    取xx111yy中的1111
xx(?=\d{3})    取xx111中的xx    正向前瞻(?=)即括号内容匹配时取xx，负向前瞻(?!)括号内容不匹配时取xx
(?<=\d{3})yy   取111yy中的yy    正向后顾(?<=)，负向后顾(?<!)
```






