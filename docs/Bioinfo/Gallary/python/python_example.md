<style>
img{
    width: 50%;
}
</style>


* Scripts：[ploting_func.py](ploting_func.py)   
* Example Usage：[Gallary.ipynb](Gallary.ipynb)  

## import packages
```
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cycler

from ploting_func import *
```


## Set color list (optional)
```
cycler_colors = plt.cycler(color=['#FF0000', '#4169E1', '#9988DD','#EECC55', '#88BB44', '#FFBBBB'])
plt.rc('axes', facecolor='black', edgecolor='b',prop_cycle=cycler_colors)

# or: plt.style.use('ggplot')
```


### bar_of_pie_plot
![bar_of_pie_plot](img/bar_of_pie_plot.png)
```
## Example Input
pie_values = [271,560,170]
pie_labels = ['Phylum A', 'Phylum B', 'Unspecified']
bar_values = [33,1,1,54,7,8,1,1,33,1,1,54,7,4,1,7,4,1,1]
bar_labels = ['Spe {}'.format(i+1) for i in range(len(bar_values))]


## Plot and save
fig = bar_of_pie_plot(pie_values,pie_labels,bar_values,bar_labels,
                    figsize=(9, 5),
                    con_color = [0,0,0], ## R G B
                    con_linewidth = 1.5,
                    anno_y_min_gap = 0.05,    ## prevent label text overlap, adjust on y axis & decide if to show bar_label
                    sort_bar_values = True
                    )
```




### donut_pie_plot
![donut_pie_plot](img/donut_pie_plot.png)
```
## Example Input
pie_values = [33,1,1,54,7,8,1,1,33,1,1,54,7,4,1,7,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
pie_labels = ['Spe Axxxxxxxx {}'.format(i+1) for i in range(len(pie_values))]
title_text = 'Phylum XXX'

## Plot and save
fig = donut_pie_plot(pie_values,pie_labels,title_text,
                   figsize=(6, 3),
                   title_fontsize = 15, 
                   startangle = 0,
                   donut_width = 0.5,      ## pie: 1
                   connectionstyle='arc3', ## bar arc 'angle' angle3  arc3
                   text_min_ang = 360*0.02,
                   sort_values = True
                  )
```









