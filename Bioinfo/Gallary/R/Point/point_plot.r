
# .libPaths("R/library")
library(getopt)
library(tidyr)
library(plyr)
library(ggplot2)
library(ggrepel)
library(ellipse)

mycolor <-c('#FF0000', '#4169E1', '#9988DD','#EECC55', '#88BB44', '#FFBBBB')
mycolor <- rep(mycolor,20)

myshape <- rep(c(16,15,23,24,25),10)  # 4,8,11

calculate_axis_lim <- function(df,x,y,to_border) { 
x = as.numeric(unlist(df[x]))
y = as.numeric(unlist(df[y]))
xmin =  min(x,na.rm=TRUE)  # if all NA, return Inf
xmax =  max(x,na.rm=TRUE)  # if all NA, return -Inf
ymin =  min(y,na.rm=TRUE)
ymax =  max(y,na.rm=TRUE)
x_axis_bound = (xmax-xmin)*to_border
y_axis_bound = (ymax-ymin)*to_border
xmin =  xmin - x_axis_bound
xmax =  xmax + x_axis_bound
ymin =  ymin - y_axis_bound
ymax =  ymax + y_axis_bound
x_scale = xmax-xmin
y_scale = ymax-ymin
return (c(xmin,xmax,ymin,ymax,x_scale,y_scale))
}


## default setting
file_dir = ''		#must input
output_dir = ''		#must input 
text_dir = ''
group_dir = ''
title = ''
dim1 = 1
dim2 = 2
to_border = 0.25      #empty space to plotting border
legend_x = 1          #legend position 
legend_y = 1          #legend position
text_x = 0            #text position 
text_y = 0            #text position
plot_hight = 8
plot_width = 8
point_size = 4
ellipse_treashhold = 1   # [0-1], below which treshhold cannot plot ellipse (1 means completely correlated, will be a line)
ellipse_level = 0.95
if_label=TRUE
if_legend=FALSE
if_ellipse=FALSE
by_shape = FALSE
by_colour = FALSE
outside_legend = ''




## Reading parameters ##
spec <- matrix(
  c("help","h",0,"logical", "help",
	"file_dir","f",1,"character","input points file",
	"output_dir","o",1,"character","output pdf file",
	"text_dir","a",2,"character","text file to be added to the plot",
	"group_dir","g",2,"character","group file",
	"title","t",2,"character","title",
	"dim1","x",2,"integer","default 1, which column to be dim1",
	"dim2","y",2,"integer","default 1=2, which column to be dim2",

	"to_border","b",2,"double","default 0.25 [0-1], distance to ploting border",
	"xmax","q",2,"double","set axis xmax",
	"xmin","j",2,"double","set axis xmin",
	"ymax","e",2,"double","set axis ymax",
	"ymin","r",2,"double","set axis ymin",

	"outside_legend","H",2,"character","top/bottom/left/right, show legend out of plottig region",
	"legend_x","Q",2,"double","default 1 [0-1], legend position",
	"legend_y","W",2,"double","default 1 [0-1], legend position",

	"text_x","E",2,"double","default 0 [0-1], text position",
	"text_y","R",2,"double","default 0 [0-1], text position",

	"plot_hight","Z",2,"double","default 8, plot size",
	"plot_width","C",2,"double","default 8, plot size",
	"point_size","V",2,"double","default 8, point size",
	"ellipse_treashhold","P",2,"double","default 1(emit lines)[0-1], below which treshhold cannot plot ellipse (neglect this parameter, its useless)",
	"ellipse_level","U",2,"double","default 0.95[0-1], ellipse confidance level",
	"if_label","O",2,"logical","T/F, if show point label",	
	"if_legend","L",2,"logical","T/F, if show legend",	
	"if_ellipse","K",2,"logical","T/F, if show ellipse",	
	"by_shape","J",2,"logical","T/F, if show group with different shape",	
	"by_colour","M",2,"logical","T/F, if show group with different color"
	),byrow=TRUE, ncol=5)

opt <- getopt(spec=spec)
if( !is.null(opt$help) || is.null(opt$file_dir) || is.null(opt$output_dir) ){
    cat(paste(getopt(spec=spec, usage = T), "\n"))
    quit()
}

## make sure personalized config is after the auto/default ones!!
if(!is.null(opt$file_dir)){file_dir<-opt$file_dir}
if(!is.null(opt$output_dir)){output_dir<-opt$output_dir}
if(!is.null(opt$text_dir)){text_dir<-opt$text_dir}
if(!is.null(opt$group_dir)){group_dir<-opt$group_dir ; if_legend = TRUE; by_colour = TRUE;if_label=FALSE}  # group version config
if(!is.null(opt$title)){title<-opt$title}
if(!is.null(opt$dim1)){dim1<-opt$dim1}
if(!is.null(opt$dim2)){dim2<-opt$dim2}
if(!is.null(opt$to_border)){to_border<-opt$to_border}
if(!is.null(opt$outside_legend)){outside_legend<-opt$outside_legend ; if(outside_legend=='left' || outside_legend=='right'){plot_width=12;legend_y=0.5 }}
if(!is.null(opt$legend_x)){legend_x<-opt$legend_x}
if(!is.null(opt$legend_y)){legend_y<-opt$legend_y}
if(!is.null(opt$text_x)){text_x<-opt$text_x}
if(!is.null(opt$text_y)){text_y<-opt$text_y}
if(!is.null(opt$plot_hight)){plot_hight<-opt$plot_hight}
if(!is.null(opt$plot_width)){plot_width<-opt$plot_width}
if(!is.null(opt$point_size)){point_size<-opt$point_size}
if(!is.null(opt$ellipse_treashhold)){ellipse_treashhold<-opt$ellipse_treashhold}
if(!is.null(opt$ellipse_level)){ellipse_level<-opt$ellipse_level}
if(!is.null(opt$if_label)){if_label<-opt$if_label}
if(!is.null(opt$if_legend)){if_legend<-opt$if_legend}
if(!is.null(opt$if_ellipse)){if_ellipse<-opt$if_ellipse}
if(!is.null(opt$by_shape)){by_shape<-opt$by_shape}
if(!is.null(opt$by_colour)){by_colour<-opt$by_colour}

if(if_legend || if_ellipse || by_shape || by_colour){
	if(group_dir == ''){
		print("Group info is necessary for : if_legend & if_ellipse & by_shape & by_colour")
		quit()
	}
}


## load anno text
anno_text = ''
if(text_dir != ''){
	lines = readLines(text_dir) # max_str = max(nchar(lines))
	for(line in lines){anno_text = paste(anno_text,line,sep='\n')}
}

## load point file ; processing header; BUG: cannot solve '\'
df = read.csv(file_dir,sep='\t',row.names = 1,fileEncoding = "UTF-8",check.names=FALSE)
dim_list = colnames(df)
original_dim_list = dim_list
for(err_character in c(' ','%','\\/','\\]','\\[','\\)','\\(','\\*','@','#','\\$','\\&','\\!','\\~','\\}','\\{',':',';','\\?','>','<') ){dim_list = gsub(err_character,'.',dim_list)}
colnames(df) = dim_list
df$SampleID=rownames(df)





## load group file ; merge with df by the order of group
if(group_dir != ''){
group = read.csv(group_dir,sep='\t',row.names = 1,fileEncoding = "UTF-8",check.names=FALSE)
colnames(group) = c("Group")
group$SampleID = rownames(group)
group$Group <- factor(group$Group,levels = unique(group$Group)) 
	if(identical(group$SampleID[order(group$SampleID)],df$SampleID[order(df$SampleID)])){
		df = merge(group, df,by="SampleID")
	}else{
		cat('Sample name not match!\n')
		quit()}
	rownames(df) = c(1:length(rownames(df)))}


## Set plot axis lim
lim_list1 = calculate_axis_lim(df,dim_list[dim1],dim_list[dim2],to_border)
xmin = lim_list1[1]
xmax = lim_list1[2]
ymin = lim_list1[3]
ymax = lim_list1[4]


## calculate ellipse & reset axis lim ; only possible when group is set 
## Logic:if cor=NA/out of range, no ellipse ; always caculated, for axis consistency
## if either sd(x) sd(y) is 0, cor=NA not plotting
if(group_dir != ''){
	df_ell <- data.frame()
	for(g in levels(df$Group)){
		temp_df = df[df$Group==g,]
		x = as.numeric(unlist(temp_df[dim_list[dim1]]))
		y = as.numeric(unlist(temp_df[dim_list[dim2]]))
		if(!is.na(cor(x, y)) ){			# check ellipse_treashhold
			if(cor(x, y)>=ellipse_treashhold || cor(x, y)<=-1*ellipse_treashhold){ellip_cor = NA}else{ellip_cor = cor(x, y)}
		}else{ellip_cor = cor(x, y)}
		temp_ellip = ellipse(ellip_cor, scale=c(sd(x),sd(y)), centre=c(mean(x),mean(y)), level = ellipse_level)
		temp_ellip = cbind(temp_ellip,Group=g,SampleID=g)
		df_ell <- rbind(df_ell,temp_ellip)
	}
	df_ell$x = as.numeric(unlist(df_ell$x))
	df_ell$y = as.numeric(unlist(df_ell$y))
	lim_list2 = calculate_axis_lim(df_ell,"x","y",0)
	xmin = min(lim_list2[1],xmin)
	xmax = max(lim_list2[2],xmax)
	ymin = min(lim_list2[3],ymin)
	ymax = max(lim_list2[4],ymax)
}


##############plotting start###################

## plotting config 
if(group_dir != ''){
if(by_shape == TRUE){shape_list = myshape[c(1:length(df$Group))]}else{shape_list = rep(myshape[1],length(df$Group))}
if(by_colour == TRUE){colour_list = mycolor[c(1:length(df$Group))]}else{colour_list = rep(mycolor[1],length(df$Group))}
	point_plot= ggplot(df, aes_string(x= dim_list[dim1], y= dim_list[dim2], label = "SampleID",fill = "Group",colour = "Group",shape = "Group"))
	point_plot= point_plot + scale_colour_manual(values = colour_list)
	point_plot= point_plot + scale_fill_manual(values = colour_list)
	point_plot= point_plot + scale_shape_manual(values = shape_list)
}else{
	colour_list = rep(mycolor[1],length(df$SampleID))
	point_plot= ggplot(df, aes_string(x= dim_list[dim1], y= dim_list[dim2], label = "SampleID",colour ="SampleID"))
	point_plot= point_plot + scale_colour_manual(values = colour_list)
	if_legend = FALSE
}

## plot points 
point_plot= point_plot + geom_point(size=point_size,alpha=0.9) 

## plot points label -- geom_text(check_overlap = T,nudge_x=0.02*(xmax-xmin),nudge_y=-0.02*(ymax-ymin),show.legend = FALSE)
if(if_label == TRUE){
	point_plot= point_plot + geom_text_repel(max.overlaps=100)
}

## plot ellipse
if(if_ellipse == TRUE){
	point_plot= point_plot + geom_path(data=df_ell, aes(x=x, y=y,color = Group), size=0.8, linetype=2,show.legend = F)
}

## set plot axis lim ; set axis name 
if(!is.null(opt$xmax)){xmax<-opt$xmax}
if(!is.null(opt$xmin)){xmin<-opt$xmin}
if(!is.null(opt$ymax)){ymax<-opt$ymax}
if(!is.null(opt$ymin)){ymin<-opt$ymin}
point_plot= point_plot + scale_x_continuous(name = original_dim_list[dim1],limits = c(xmin, xmax))
point_plot= point_plot + scale_y_continuous(name = original_dim_list[dim2],limits = c(ymin, ymax))


## set additional text
if(text_dir!= ''){
	point_plot= point_plot + annotate("text", x=xmin+(xmax-xmin)*text_x,y=ymin+(ymax-ymin)*text_y,hjust=text_x,vjust=text_y ,label=c(anno_text),size=5 )
}

## theme setting & legend position 
point_plot= point_plot + theme_bw()
point_plot= point_plot + theme(
	panel.grid=element_blank(),
	legend.justification=c(legend_x,legend_y), 
	legend.position=c(legend_x,legend_y),
	legend.title = element_blank(),
	legend.key = element_blank(),
	legend.background=element_rect(fill="transparent",color="black",size=0.2),
	axis.text.x = element_text(size= 10),
	axis.text.y = element_text(size= 10),
	axis.title.x = element_text(color="black", size= 16),
	axis.title.y = element_text(color="black", size= 16)
	)


## add title
if(title!=''){
	point_plot= point_plot + ggtitle(title)
	point_plot= point_plot + theme(plot.title = element_text(face="bold",hjust = 0.5,size = 24))
}

## if legend outside plorring region
if(outside_legend != ''){
	point_plot= point_plot + theme(
		legend.position=outside_legend,
		legend.background=element_blank()
)}


## if show legend
if(if_legend != TRUE){
point_plot= point_plot + theme(legend.position="none")}

## save plot 
ggsave(point_plot, filename=output_dir,width=plot_width,height=plot_hight,limitsize = FALSE)
        


