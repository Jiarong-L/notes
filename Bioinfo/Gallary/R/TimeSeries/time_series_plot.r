# .libPaths("R/library")
library(getopt)

mycolor <-c("#E41A1C","#1E90FF","#FF8C00","#4DAF4A","#984EA3","#40E0D0","#FFC0CB","#00BFFF","#FFDEAD","#90EE90","#EE82EE","#00FFFF","#F0A3FF", "#0075DC","#993F00","#4C005C","#2BCE48","#FFCC99","#808080","#94FFB5","#8F7C00","#9DCC00","#C20088","#003380","#FFA405","#FFA8BB","#426600","#FF0010","#5EF1F2","#00998F","#740AFF","#990000","#FFFF00","#CD0000","#3A89CC","#769C30","#D99536","#7B0078","#BFBC3B","#6E8B3D","#00688B","#C10077","#CAAA76","#EEEE00","#458B00","#8B4513","#008B8B","#6E8B3D","#8B7D6B","#7FFF00","#CDBA96","#ADFF2F")
mycolor <- rep(mycolor,20)

## Default settings
day_format = FALSE
date_breaks = '3 days'   # waiver() this needs ggplot2 maybe
date_labels = '%b-%d'    # waiver()
y_axis_lable = ''

group_dir = ''
plot_avg = FALSE
ribbon = ''   # 'sd'  'ci'  'se'
conf_interval = 0.95


ylim_upper_border = 0.20
ylim_lower_border = 0.05


x_angle = 90     # x axis text direction

fig_width = 10
fig_height = 5


legend_x = 0.5
legend_y = 0.99
legend_position= c(legend_x,legend_y)  # 'right'

horizontal_legend = TRUE
if_legend = TRUE


spec <- matrix(
  c("help","h",0,"logical", "help",
	"file_dir","f",1,"character","input time_series file",
	"output_dir","o",1,"character","output pdf file",

    "day_format","B",2,"logical","default F [T/F], if input date is day(ymd) or day-time(dmy_hm)",	

    "date_breaks","Q",2,"character","default '3 days' breaks of x-axis dates",
    "date_labels","W",2,"character","default '%b-%d' format of x-axis dates",
    "y_axis_lable","Z",2,"character","default None, y axis label",
    "y_axis_lable_parse","M",2,"character","default None, y axis label(parsed) cannot! have spacing between non-expr ! usage aa_(m^3/m^3)",

	"group_dir","g",2,"character","group file",
    "plot_avg","Y",2,"logical","T/F, if plot by groups' average",	
    "ribbon","R",1,"character","ribbon's type: sd se ci  (standard deviation/error, confident interval)",
    "conf_interval","U",1,"double","default 0.95, if ribbon is ci, set ci",

    "ylim_upper_border","O",1,"double","default 0.20, ylim porportion to upper bound",
    "ylim_lower_border","P",1,"double","default 0.05, ylim porportion to lower bound",
    "ymin","C",1,"double","default auto, y axis minimal",
    "ymax","X",1,"double","default auto, y axis maximal",

    "x_angle","L",2,"integer","default 90, angle of the x-axis labels",	
    "fig_width","K",2,"integer","default 10, width of fig",
    "fig_height","J",2,"integer","default 5, height of fig",
    "legend_x","H",2,"double","default 0.5 [0-1], legend position",
	"legend_y","G",2,"double","default 0.99 [0-1], legend position",
    "legend_position","F",2,"character","default not used, can be set as: [left right up bottom]",
    "horizontal_legend","D",2,"logical","default T [T/F], if legend is horizontal",
    "if_legend","V",2,"logical","T/F, if show legend"
    ),byrow=TRUE, ncol=5)

opt <- getopt(spec=spec)
if( !is.null(opt$help) || is.null(opt$file_dir) || is.null(opt$output_dir) ){
    cat(paste(getopt(spec=spec, usage = T), "\n"))
    quit()
}

if(!is.null(opt$file_dir)){file_dir<-opt$file_dir}
if(!is.null(opt$output_dir)){output_dir<-opt$output_dir}
if(!is.null(opt$day_format)){day_format<-opt$day_format}
if(!is.null(opt$date_breaks)){date_breaks<-opt$date_breaks}
if(!is.null(opt$date_labels)){date_labels<-opt$date_labels}
if(!is.null(opt$y_axis_lable)){y_axis_lable<-opt$y_axis_lable}
if(!is.null(opt$y_axis_lable_parse)){y_axis_lable<-parse(text = opt$y_axis_lable_parse)}

if(!is.null(opt$group_dir)){group_dir<-opt$group_dir}
if(!is.null(opt$plot_avg)){plot_avg<-opt$plot_avg}
if(!is.null(opt$ribbon)){ribbon<-opt$ribbon ; plot_avg = TRUE}  # set plot_avg as TRUE
if(!is.null(opt$conf_interval)){conf_interval<-opt$conf_interval}
if(!is.null(opt$ylim_upper_border)){ylim_upper_border<-opt$ylim_upper_border}
if(!is.null(opt$ylim_lower_border)){ylim_lower_border<-opt$ylim_lower_border}
if(!is.null(opt$x_angle)){x_angle<-opt$x_angle}
if(!is.null(opt$fig_width)){fig_width<-opt$fig_width}
if(!is.null(opt$fig_height)){fig_height<-opt$fig_height}
if(!is.null(opt$legend_x)){legend_x<-opt$legend_x}
if(!is.null(opt$legend_y)){legend_y<-opt$legend_y}
if(!is.null(opt$legend_position)){legend_position<-opt$legend_position}
if(!is.null(opt$horizontal_legend)){horizontal_legend<-opt$horizontal_legend}
if(!is.null(opt$if_legend)){if_legend<-opt$if_legend}





##############################Start



library(lubridate)
library(tidyr)
library(ggplot2)
library(Rmisc)
library(dplyr)


## load data
df = read.csv(file_dir,sep='\t',row.names = NULL,check.names=FALSE)
colnames(df)[1] = 'time'
if(day_format){df$time= as_datetime(ymd(df$time))}else{df$time= dmy_hm(df$time)}

sample_list = colnames(df)[c(2:length(colnames(df)))]
df = gather(df,key=SampleID,value=value, all_of(sample_list))
df$SampleID <- factor(df$SampleID,levels = sample_list)


## load group file ; check if inputs consists ; merge with df by the order of group
if(group_dir != ''){
group = read.csv(group_dir,sep='\t',row.names = 1,fileEncoding = "UTF-8",check.names=FALSE)
colnames(group) = c("Group")
group$SampleID = rownames(group)
if(identical(group$SampleID[order(group$SampleID)],sample_list[order(sample_list)])){
    df = merge(group, df,by="SampleID",all=T)
    df$Group <- factor(df$Group,levels = unique(group$Group))
}else{
    cat('Sample name not match!\n')
    quit()  }
}

## if plot_avg, caculate avg and ribbons
if(group_dir != ''){if(plot_avg){
df = summarySE(df, "value", groupvars = c("Group","time"), na.rm = TRUE, conf.interval = conf_interval)
df$ci = replace_na(df$ci,0)
df$sd = replace_na(df$sd,0)
df$se = replace_na(df$se,0)
df$ci_upper = df$value + df$ci *0.5
df$ci_lower = df$value - df$ci *0.5
df$sd_upper = df$value + df$sd *0.5
df$sd_lower = df$value - df$sd *0.5
df$se_upper = df$value + df$se *0.5
df$se_lower = df$value - df$se *0.5
df$SampleID = df$Group
}}



## ylim of plot
y_range = max(df$value,na.rm = T) -  min(df$value,na.rm = T)
ymax =  max(df$value,na.rm = T) + y_range*ylim_upper_border
ymin =  min(df$value,na.rm = T) - y_range*ylim_lower_border



## if ribbons
if(group_dir != ''){if(plot_avg){if(ribbon != ''){
    ribbon_lower = paste(ribbon,'_lower',sep='')
    ribbon_upper = paste(ribbon,'_upper',sep='')
## Update ylim
    ymax =  max(max(df[ribbon_upper],na.rm = T),ymax,na.rm = T)
    ymin =  min(min(df[ribbon_lower],na.rm = T),ymin,na.rm = T)
}}}


# if user set ylim
if(!is.null(opt$ymin)){ymin<-opt$ymin}
if(!is.null(opt$ymax)){ymax<-opt$ymax}

# init plot settings
if(group_dir != ''){
    time_series_plot = ggplot(df, aes(x = time, y = value, colour = Group ,group = SampleID))
    if(plot_avg){if(ribbon != ''){time_series_plot = time_series_plot + geom_ribbon(aes_string(ymin = ribbon_lower, ymax = ribbon_upper, colour = NULL, fill = "Group"),alpha = 0.3, na.rm = T, show.legend = F)}}
}else{
    time_series_plot = ggplot(df, aes(x = time, y = value, colour = SampleID))
}

# Plot lines ; Set Theme
time_series_plot = time_series_plot + geom_line() 
time_series_plot = time_series_plot + labs(x='Date', y=y_axis_lable, color = '')
time_series_plot = time_series_plot + scale_x_datetime(date_breaks = date_breaks, date_labels = date_labels)
time_series_plot = time_series_plot + scale_y_continuous(limits = c(ymin, ymax))

if(horizontal_legend){
    my_guide_legend = guide_legend(byrow = T,direction='horizontal')
}else{
    my_guide_legend = guide_legend(byrow = F,direction='vertical')
}

time_series_plot = time_series_plot + scale_colour_manual(values = mycolor,guide = my_guide_legend) + scale_fill_manual(values = mycolor)



time_series_plot = time_series_plot + theme_bw()
time_series_plot = time_series_plot + theme(
    panel.grid=element_blank(),
    axis.text.x = element_text(angle = x_angle, hjust = 0.5, vjust = 0.5,color="black", size= 10),#, family = 'TT Times New Roman'),
    axis.text.y = element_text(hjust = 0.5, vjust = 0.5,color="black", size= 10),#, family = 'TT Times New Roman'),
	axis.title.x = element_text(color="black", size= 16),#, family = 'TT Times New Roman'),
	axis.title.y = element_text(color="black", size= 16),#, family = 'TT Times New Roman'),
    legend.justification=legend_position,
	legend.position= legend_position
)


## if show legend
if(if_legend != TRUE){
time_series_plot= time_series_plot + theme(legend.position="none")}

# Save Plot
ggsave(time_series_plot, filename=output_dir,width=fig_width,height=fig_height)





