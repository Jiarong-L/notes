import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
import numpy as np


def bar_of_pie_plot(pie_values,pie_labels,bar_values,bar_labels,
                    figsize=(9, 5),
                    con_color = [0, 0, 0],   ## R G B
                    con_linewidth = 2,
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

    ## Bar Part - auto adjust label on y axis
    bottom = 1
    width = 1
    kw = dict(arrowprops=dict(arrowstyle="-",relpos=(0,0.5),shrinkA=0),
#               bbox=dict(pad=0),    #### for adjustment
              zorder=0, verticalalignment ='center',horizontalalignment='left')
    anno_previous_y = bottom + anno_y_min_gap
    for j, (height, label) in enumerate(reversed([*zip(bar_ratios, bar_labels)])):
        bottom -= height
        bc = ax2.bar(0, height, width, bottom=bottom,  alpha=0.8) # label=label,  # for ax2.legend()
        if height >= anno_y_min_gap:
            ax2.bar_label(bc, labels=[f"{height:.0%}"], label_type='center')
        xtext = width * 1.5
        ytext = min(anno_previous_y -  anno_y_min_gap,(bottom+0.5*height) )
        anno_previous_y = ytext
        ax2.annotate(label, xy=(width*0.5, bottom+0.5*height), xytext=(xtext, ytext),**kw)

    ax2.set_title(pie_labels[0])
    # ax2.legend()    # replaced by ax2.annotate
    ax2.axis('off')
    ax2.set_xlim(- 2.5 * width, 2.5 * width)

    # use ConnectionPatch to draw lines between the two plots
    theta1, theta2 = wedges[0].theta1, wedges[0].theta2
    center, r = wedges[0].center, wedges[0].r
    bar_height = sum(bar_ratios)

    # draw top connecting line
    x = r * np.cos(np.pi / 180 * theta2) + center[0]
    y = r * np.sin(np.pi / 180 * theta2) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, bar_height), coordsA=ax2.transData,xyB=(x, y), coordsB=ax1.transData)
    con.set_color(con_color)  
    con.set_linewidth(con_linewidth)
    ax2.add_artist(con)

    # draw bottom connecting line
    x = r * np.cos(np.pi / 180 * theta1) + center[0]
    y = r * np.sin(np.pi / 180 * theta1) + center[1]
    con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,xyB=(x, y), coordsB=ax1.transData)
    con.set_color(con_color)
    ax2.add_artist(con)
    con.set_linewidth(con_linewidth)
    return fig



def donut_pie_plot(pie_values,pie_labels,title_text,
                   figsize=(6, 3),
                   title_fontsize = 15, 
                   startangle = 0,
                   donut_width = 0.5,      ## pie: 1
                   connectionstyle='arc3', ## bar arc 'angle' angle3  arc3
                   text_min_ang = 3.6,
                   sort_values = True      ## in descending order
                  ):
    plt.close()
    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(aspect="equal"))

    ## sort values
    if sort_values:
        pie_labels,pie_values = zip(*sorted([*zip(pie_labels,pie_values)],key = lambda x: -x[1]))

    ## pie plot
    wedges, texts = ax.pie(pie_values, wedgeprops=dict(width=donut_width), startangle=startangle)

    ## lable
    kw = dict(arrowprops=dict(arrowstyle="-",shrinkA=0,shrinkB=0,connectionstyle=connectionstyle),
    #           bbox=dict(pad=0),
              zorder=0, va="center")
    previous_ang = startangle
    for i, p in enumerate(wedges):
        ang = (p.theta1 + p.theta2)/2
        if (p.theta2 - p.theta1) < text_min_ang:  # if gap_ang < text_min_ang, skip that anno text
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
        ax.set_title(title_text,y=1.2,fontsize=title_fontsize)
    return fig










