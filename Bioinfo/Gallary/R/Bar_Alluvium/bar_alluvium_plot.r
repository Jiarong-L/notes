# .libPaths("R/library")
library(getopt)

## default settings ##
mycolor <-c('#FF0000', '#4169E1', '#9988DD','#EECC55', '#88BB44', '#FFBBBB')
mycolor <- rep(mycolor,20)

x_angle = 90
bar_width = 0.8
legend_title = ''
legend_face = 'plain'
group_dir = ''
allu = FALSE
reverse_order = TRUE
order_by_name = FALSE

## Reading parameters ##
spec <- matrix(
  c("help","h",0,"logical", "help",
    "input","f",1,"character","input table file; each col as a bar",
    "output","o",1,"character","output img/pdf file",
    "group_dir","g",2,"character","group_dir file",
    "x_angle","A",2,"integer","default 90, angle of the x-axis labels",	
    "bar_width","b",2,"double","default 0.8, the width of the bar (out of 1 maybe?)",	
    "legend_title","l",2,"character","default empty, title of the legend",
    "legend_face","p",2,"character","default plain, face of the legend (plain, italic, bold, bold.italic)",
    "fig_width","x",2,"integer","default auto, width of fig",
    "fig_height","y",2,"integer","default auto, height of fig",
     "allu","a",2,"logical","T/F, default F, means not plotting alluvium; BUG:alluvium is extremely slow for very large amount of samples",
     "reverse_order","r",2,"logical","T/F, default T, plot by reversed input order",
     "order_by_name","n",2,"logical","T/F, default F, plot by naming's order"
),byrow=TRUE, ncol=5)

opt <- getopt(spec=spec)

if( !is.null(opt$help) || is.null(opt$input) || is.null(opt$output) ){
    cat(paste(getopt(spec=spec, usage = T), "\n"))
    quit()
}

if(!is.null(opt$group_dir)){group_dir <-opt$group_dir}
if(!is.null(opt$x_angle)){x_angle <-opt$x_angle}
if(!is.null(opt$bar_width)){bar_width <-opt$bar_width}
if(!is.null(opt$legend_title)){legend_title <-opt$legend_title}
if(!is.null(opt$legend_face)){legend_face <-opt$legend_face}
if(!is.null(opt$allu)){allu <-opt$allu}
if(!is.null(opt$reverse_order)){reverse_order <-opt$reverse_order}
if(!is.null(opt$order_by_name)){order_by_name <-opt$order_by_name;if(order_by_name){reverse_order = FALSE}}



library(tidyr)   #gather
library(ggplot2)
library(plyr)    #ddply
library(ggalluvial)
library(RColorBrewer)


## data processing ##
data = read.csv(opt$input,sep='\t',row.names = 1,check.names=FALSE)          # first col as index
data['taxa']=rownames(data)
sample_list = colnames(data)[c(1:length(colnames(data))-1)]       #  x-axis order 

col_order = c(1:length(data$taxa))                                #  coloring order; same as y-axis order only for reverse_taxa

if(reverse_order){                                           #  y-axis order; 
  y_order = c(length(data$taxa):1)
  col_order = y_order
}else{y_order = c(1:length(data$taxa))}
if(order_by_name){
  y_order = order(data$taxa)
}


taxa_list = data$taxa[y_order]
mycolor = mycolor[col_order]        

                                #  below set fig size
fig_width = 1 + 0.3*length(sample_list) + max(nchar(data$taxa)+3)*0.06*ceiling(length(taxa_list)/20) 
fig_height= 6 + max(nchar(sample_list))*0.075
if( fig_width < fig_height+1 ){fig_width=fig_height+1}

if(!is.null(opt$fig_width)){fig_width <-opt$fig_width}
if(!is.null(opt$fig_height)){fig_height <-opt$fig_height}


data <- gather(data,key=SampleID,value=value, all_of(sample_list))
data <- ddply(data,"SampleID",transform,percent= value/sum(value)*100 )
data$SampleID <- factor(data$SampleID,levels = sample_list) 
data$taxa <- factor(data$taxa,levels = taxa_list) 

print(fig_width)
print(fig_height)



## load group file ; merge with data by the order of group
if(group_dir != ''){
group = read.csv(group_dir,sep='\t',row.names = 1,fileEncoding = "UTF-8",check.names=FALSE)
colnames(group) = c("Group")
group$SampleID = rownames(group)
if(identical(group$SampleID[order(group$SampleID)],sample_list[order(sample_list)])){
data = merge(group, data,by="SampleID",all=T)
data$Group <- factor(data$Group,levels = unique(group$Group))
}else{
cat('Sample name not match!\n')
quit()}}

## plot ##
alluvium_plot=ggplot(data,aes(x=SampleID,y=percent,fill=taxa,stratum = taxa,alluvium = taxa))

if(allu == TRUE){
  alluvium_plot= alluvium_plot +
  geom_alluvium(width=bar_width) +
  geom_stratum(width=bar_width,size=0.1)
}else{
  alluvium_plot= alluvium_plot + geom_bar(stat='identity',width=bar_width)
}

alluvium_plot= alluvium_plot + theme_classic()


if(group_dir != ''){
  alluvium_plot= alluvium_plot + facet_grid(. ~ Group,,scales = "free",space="free_x")
  alluvium_plot= alluvium_plot + theme(strip.background = element_rect(fill = "grey85",colour = "black"),
                                       panel.spacing = unit(0, "mm"),
                                       panel.background = element_rect(size = 0.25),
                                       panel.border = element_rect(fill = NA,colour = "grey20"))
  }


alluvium_plot= alluvium_plot + labs(x='', y='Relative Abundance (%)') +
                                scale_y_continuous(expand=c(0, 0)) +
                                scale_fill_manual(values = mycolor) +
                                theme(axis.line.x=element_blank(),legend.text = element_text(face=legend_face),axis.text.x = element_text(angle = x_angle, hjust = 1, vjust = 0.5)) + 
                                labs(fill = legend_title)

ggsave(alluvium_plot, filename=opt$output,width=fig_width,height=fig_height,limitsize = FALSE)

