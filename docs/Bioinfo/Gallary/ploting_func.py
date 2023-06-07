import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np

def cal_pie_wedge_bounds(wedge):
    theta1 = wedge.theta1
    theta2 = wedge.theta2
    center = wedge.center
    r = wedge.r
    top_x = r * np.cos(np.pi / 180 * theta2) + center[0]
    top_y = r * np.sin(np.pi / 180 * theta2) + center[1]
    bottom_x = r * np.cos(np.pi / 180 * theta1) + center[0]
    bottom_y = r * np.sin(np.pi / 180 * theta1) + center[1]
    return (top_x,top_y),(bottom_x,bottom_y)


def connect_axes(ax1,ax2,xyA,xyB,con_color,con_linewidth,con_alpha = 0.5):
    con = ConnectionPatch(xyA=xyA, coordsA=ax2.transData,xyB=xyB, coordsB=ax1.transData)
    con.set_color(con_color)  
    con.set_alpha(con_alpha)
    con.set_linewidth(con_linewidth)
    ax2.add_artist(con)



def anno_arrowprops_pie(ax,wedges,pie_labels,text_min_ang,startangle,connectionstyle):
    kw = dict(arrowprops=dict(arrowstyle="-",shrinkA=0,shrinkB=0,connectionstyle=connectionstyle),
              zorder=0, va="center") #           bbox=dict(pad=0),
    previous_ang = startangle
    for i, p in enumerate(wedges):
        ang = (p.theta1 + p.theta2)/2
        if (p.theta2 - p.theta1) < text_min_ang:          # if gap_ang < text_min_ang, skip that anno text
            continue
        text_ang = min(max(previous_ang + text_min_ang,ang),startangle + text_min_ang +360)
        previous_ang = text_ang
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        ytext = np.sin(np.deg2rad(text_ang)) *1.5
        xtext = int(np.sign(np.cos(np.deg2rad(text_ang)))) *1.5
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(xtext))]
        relpos={-1: (1,0.5), 1: (0,0.5)}[int(np.sign(xtext))]
        kw["arrowprops"].update({"relpos": relpos})
        ax.annotate(pie_labels[i], xy=(x, y), xytext=(xtext, ytext),
                    horizontalalignment=horizontalalignment, **kw)


def donut_pie(ax,pie_values,pie_labels,title_text,
              title_fontsize = 15, 
              startangle = 0,
              donut_width = 0.5,      ## pie: 1
              connectionstyle='arc3', ## bar arc 'angle' angle3  arc3
              text_min_ang = 3.6,
              anno_arrowprops = True
                  ):
    ax.set_title(title_text,y=1.2,fontsize=title_fontsize)
    if anno_arrowprops:
        wedges, _ = ax.pie(pie_values, wedgeprops=dict(width=donut_width), startangle=startangle)
        anno_arrowprops_pie(ax,wedges,pie_labels,text_min_ang,startangle,connectionstyle)
    else:
        pie_values_sum = sum(pie_values)
        wedges, _ = ax.pie(pie_values, 
                           labels = [pie_labels[i] if (pie_values[i]/pie_values_sum)*360 >= text_min_ang else '' for i in range(len(pie_values))],
                           wedgeprops=dict(width=donut_width), startangle=startangle)
    return wedges



def single_bar(ax,bar_ratios,bar_labels,anno_y_min_gap,ax_title=''):       # with arrowprops anno
    width = 1
    bottom = sum(bar_ratios)     # start plotting from the top
    anno_previous_y = bottom + anno_y_min_gap
    kw = dict(arrowprops=dict(arrowstyle="-",relpos=(0,0.5),shrinkA=0),              # for anno text & arrow
              zorder=0, verticalalignment ='center',horizontalalignment='left')      # bbox=dict(pad=0),  ### for adjustment
    for (height, label) in reversed([*zip(bar_ratios, bar_labels)]):
        bottom -= height                                                         # current position
        bc = ax.bar(0, height, width, bottom=bottom,  alpha=0.8)                 # current bar block
        if height >= anno_y_min_gap:
            ax.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')      # label in bar block
        xtext = width * 1.5                                                      # text position (x,y), auto adjust on y axis
        ytext = min(anno_previous_y -  anno_y_min_gap,(bottom+0.5*height) )
        anno_previous_y = ytext
        ax.annotate(label, xy=(width*0.5, bottom+0.5*height), xytext=(xtext, ytext),**kw)
    ax.set_title(ax_title)
    ax.axis('off')
    ax.set_xlim(- 2.5 * width, 2.5 * width)
    return width,sum(bar_ratios)                     # x_bounds:[-width / 2,,width / 2,] ; y_bounds:[0,sum(bar_ratios)]




def bar_of_pie_plot(pie_values,pie_labels,bar_values,bar_labels,
                    figsize=(9, 5),
                    con_color = [0, 0, 0],   ## R G B
                    con_linewidth = 1.5,
                    anno_y_min_gap = 0.05,   ## if <0.05 (5%),adjust on y axis & hide bar_label; prevent label text overlap
                    sort_bar_values = True   ## in descending order
                    ):
    plt.close()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    fig.subplots_adjust(wspace=0)
    
    ## sort_bar_values
    if sort_bar_values == True:
        bar_labels,bar_values = zip(*sorted([*zip(bar_labels,bar_values)],key = lambda x: -x[1]))
    
    ## Conver to ratio
    pie_ratios = [v/sum(pie_values) for v in pie_values]
    bar_ratios = [v/sum(bar_values) for v in bar_values]

    ## Pie Part
    pie_startangle = -180 * pie_ratios[0]
    explode = [0.1] + [0] * (len(pie_ratios)-1)
    wedges, *_ = ax1.pie(pie_ratios, autopct='%1.1f%%', startangle=pie_startangle,labels=pie_labels, explode=explode) 
    top_xyB,bottom_xyB = cal_pie_wedge_bounds(wedges[0])                           # pie bounds    
    

    ## Bar Part - auto adjust label on y axis
    bar_width,bar_height = single_bar(ax2,bar_ratios,bar_labels,anno_y_min_gap,ax_title=pie_labels[0])    # bar bounds
    top_xyA = (-bar_width / 2, bar_height)
    bottom_xyA =(-bar_width / 2, 0)    

    # use ConnectionPatch to draw lines between the two plots
    connect_axes(ax1,ax2,top_xyA,top_xyB,con_color,con_linewidth,con_alpha = 0.5)       # draw top connecting line
    connect_axes(ax1,ax2,bottom_xyA,bottom_xyB,con_color,con_linewidth,con_alpha = 0.5) # draw bottom connecting line
    return fig



def donut_pie_plot(pie_values,pie_labels,title_text,
                   figsize=(6, 3),
                   title_fontsize = 15, 
                   startangle = 0,
                   donut_width = 0.5,      ## pie: 1
                   connectionstyle='arc3', ## bar arc 'angle' angle3  arc3
                   text_min_ang = 3.6,
                   sort_values = True,      ## in descending order
                   anno_arrowprops = True
                  ):
    plt.close()
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))

    ## sort values
    if sort_values:
        pie_labels,pie_values = zip(*sorted([*zip(pie_labels,pie_values)],key = lambda x: -x[1]))

    ## pie plot   
    donut_pie(ax,pie_values,pie_labels,title_text,
              title_fontsize = title_fontsize, 
              startangle = startangle,
              donut_width = donut_width,  
              connectionstyle = connectionstyle,
              text_min_ang = text_min_ang,
              anno_arrowprops = anno_arrowprops)
    return fig










