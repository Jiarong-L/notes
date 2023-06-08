
<style>
img{
    width: 60%;
}
</style>

### RColorBrewer 选取调色板
```
library(RColorBrewer)
display.brewer.all()
```

![1](ColorMap/RColorBrewer.png)

```
> brewer.pal.info
         maxcolors category colorblind
BrBG            11      div       TRUE
PiYG            11      div       TRUE
PRGn            11      div       TRUE
PuOr            11      div       TRUE
RdBu            11      div       TRUE
RdGy            11      div      FALSE
RdYlBu          11      div       TRUE
RdYlGn          11      div      FALSE
Spectral        11      div      FALSE
Accent           8     qual      FALSE
Dark2            8     qual       TRUE
Paired          12     qual       TRUE
Pastel1          9     qual      FALSE
Pastel2          8     qual      FALSE
Set1             9     qual      FALSE
Set2             8     qual       TRUE
Set3            12     qual      FALSE
Blues            9      seq       TRUE
BuGn             9      seq       TRUE
BuPu             9      seq       TRUE
GnBu             9      seq       TRUE
Greens           9      seq       TRUE
Greys            9      seq       TRUE
Oranges          9      seq       TRUE
OrRd             9      seq       TRUE
PuBu             9      seq       TRUE
PuBuGn           9      seq       TRUE
PuRd             9      seq       TRUE
Purples          9      seq       TRUE
RdPu             9      seq       TRUE
Reds             9      seq       TRUE
YlGn             9      seq       TRUE
YlGnBu           9      seq       TRUE
YlOrBr           9      seq       TRUE
YlOrRd           9      seq       TRUE
```


### brewer.pal 提取调色板颜色
```
> brewer.pal(9,"BrBG")
[1] "#8C510A" "#BF812D" "#DFC27D" "#F6E8C3" "#F5F5F5" "#C7EAE5" "#80CDC1" "#35978F" "#01665E"

> display.brewer.pal(9,"BrBG")
```
![2](ColorMap/BrewerPal.png)



### colorRampPalette 生成颜色序列

Example 1:
```
> colorRampPalette(brewer.pal(9,"Set1"))(50)
 [1] "#E41A1C" "#C72A35" "#AB3A4E" "#8F4A68" "#735B81" "#566B9B" "#3A7BB4" "#3A85A8" "#3D8D96" "#419584" "#449D72"
[12] "#48A460" "#4CAD4E" "#56A354" "#629363" "#6E8371" "#7A7380" "#87638F" "#93539D" "#A25392" "#B35A77" "#C4625D"
[23] "#D46A42" "#E57227" "#F67A0D" "#FF8904" "#FF9E0C" "#FFB314" "#FFC81D" "#FFDD25" "#FFF12D" "#F9F432" "#EBD930"
[34] "#DCBD2E" "#CDA12C" "#BF862B" "#B06A29" "#A9572E" "#B65E46" "#C3655F" "#D06C78" "#DE7390" "#EB7AA9" "#F581BE"
[45] "#E585B8" "#D689B1" "#C78DAB" "#B791A5" "#A8959F" "#999999"
```


Example 2:
```
> colorRampPalette(c("royalblue","firebrick3"))(12)
 [1] "#4169E1" "#4D62D0" "#5A5CBF" "#6756AE" "#73509D" "#804A8C" "#8D447B" "#9A3E6A" "#A63859" "#B33248" "#C02C37"
[12] "#CD2626"
```


### 查看颜色序列

```
mycol <- colorRampPalette(c("royalblue","firebrick3"))(12)
scales::show_col(mycol)
```
![3](ColorMap/mycol.png)

