记得说resize有分辨率损失？？TBA

## Install
注：3.4.2后有部分算法申请了专利，无法使用
```
pip3 install opencv-python
```
import: 
```py
import cv2 as cv
import matplotlib.pyplot as plt
import time
```


## Img Basic
### Load & Save
```py
img_mat = cv.imread('demo.png')    ## BGR
cv.imwrite('demo_w.png',img_mat)   ## BGR

help(img_mat)
```

### Plot
```py
plt.imshow(img_mat[:,:,[2,1,0]])   ## imread:BGR；plt:RGB

## np.hstack((mat1,mat2))  ## 并列展示两张图片
```

### Window
```py
cv.imshow('myWin', img_mat)
key = cv.waitKey(0)         ## 0: waiting；>0: display milliseconds
if key & 0xFF == ord('q'):  ## & 0xFF：取key(int,16位)的后8位；ord：取ascii码(8位)
    cv.destroyAllWindows()  ## 或：exit() 退出程序
```
* imshow必须搭配waitKey；waitKey(0)时会持续等待输入，手动关闭窗口则返回-1；waitKey(10)会在10ms后关闭窗口、返回-1，就算中途关闭窗口也会等满10ms再返回值
* 此外，还可以使用```cv.namedWindow('myWin',cv.WINDOW_NORMAL)```先创建空白window, ```cv.resizeWindow('myWin',500,600)```修改window尺寸    
* 包装到函数中使用Window展示img: 
```py
def show_img_Window(img_mat,winName,waitTime=0,exitKey='q',ifDestroyAll=True):
    cv.imshow(winName, img_mat)
    while True:
        key = cv.waitKey(waitTime)
        if (key & 0xFF ==ord(exitKey)) or (key == -1):
            if ifDestroyAll:
                cv.destroyAllWindows()
            return key     ## exit via exitKey or via click/auto(-1)

## show_img_Window(img_mat,'winName',waitTime=1000,exitKey='q',ifDestroyAll=True)
```
只通过定时/click/exitKey关闭window，成功后返回True

### Mat操作
Mat数据结构于python中转化为ndarray
```py
img_mat_shallow = img_mat.view() ## 浅拷贝
img_mat_deep = img_mat.copy() ## 深拷贝

b,g,r = cv.split(img_mat) ## 分割通道
img_mat_ = cv.merge((b,g,r)) ## 合并通道
```


### 加减乘除
add/substract/multiply/divide: 
```py
img_add = cv.add(img_mat,img_mat)  ## 两个mat逐元素计算  
img_add = img_mat + 50      ## 每个元素加50

img_addw = cv.addWeighted(img_mat,0.4,img_mat_,0.6,0) ## y= x1*w1+x2*w2+b
```
* mat范围为[0,255]
* 理论上，若结果超过[0,255]，一律计为0/255；**实际上** 
    - **Mat255 +1 ==> 0**；这就可以解释为何 Mat255*2 ==> 254
    - Mat255 -256 ==> 65535；不过 Mat255 -255 -1 ==> 255；这是因为 **Mat0 -1 ==> 255**
    - 所以**实际上是超限后+/-255**
* ```cv.add(img_mat,img_mat)```不能写成```cv.add(img_mat,50)```，否则只对第一维度起效；反之亦不能，两个mat必须使用cv.xxx，直接计算会有不能理解的事情发生

### 位运算
bitwise_not/bitwise_and/bitwise_or/bitwise_xor: 
```py
cv.bitwise_not(img_mat)  ## ~255
cv.bitwise_and(img_mat,img_mat) ## 255 & 255
cv.bitwise_or(img_mat,img_mat) ## 255 | 255 = 0
cv.bitwise_xor(img_mat,img_mat) ## 255 ^ 255 
```
* mat范围为[0,255]
* 同理，也可以写成类似：```img_mat ^ 255 ```

### 基本变换
```py
h,w,ch = img_mat.shape

img_resize = cv.resize(img_mat,(w*2,h*2)) 

img_flip = cv.flip(img_mat,flipCode=-1)  ## 0: 上下；>0: 左右；<0: 上下左右；

img_rotate = cv.rotate(img_mat,0) ## 0:顺时针90, 1:180, 2:逆时针90

### M = cv.getRotationMatrix2d((90,90),15,1.5) 
src = np.float32([[11,11],[23,56],[99,88]])
dst = np.float32([[21,11],[33,56],[109,88]])
M = cv.getAffineTransform(src,dst) 
img_affine = cv.warpAffine(img_mat,M,(w,h))



src = np.float32([[11,11],[23,56],[99,88],[199,88]])
dst = np.float32([[21,11],[33,56],[109,88],[209,88]])
M = cv.getPerspectiveTransform(src,dst) 
img_perspective = cv.warpPerspective(img_mat,M,(w,h))
```
* 输出的宽/高 正好与原输入顺序相反 
* ```resize(src, dsize[, dst[, fx[, fy[, interpolation]]]])```中interpolation插值算法选项见[cv::InterpolationFlags](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html)
* flipCode, RotateFlags 参数见[Operations on arrays](https://docs.opencv.org/3.4/d2/de8/group__core__array.html)
* [warpAffine(img_mat,M,(w,h))](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga0203d9ee5fcd28d40dbc4a1ea4451983)
* [warpPerspective(img_mat,M,(w,h))](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#gaf73673a7e8e18ec6963e3774e6a94b87)
* 计算变换矩阵：
    - [getRotationMatrix2d(center,angle,scale)](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#gafbbc470ce83812914a70abfb604f4326): 旋转中心、旋转角度、缩放比例
    - [getAffineTransform(src,dst)](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga47069038267385913c61334e3d6af2e0): src、dst各自为原目标、变换后目标对应的**三个**点
    - [getPerspectiveTransform(src,dst)](https://docs.opencv.org/3.4/da/d54/group__imgproc__transform.html#ga15302cbff82bdcddb70158a58b73d981): src、dst各自为原目标、变换后目标对应的**四个**点

### 常用变换
各种卷积的处理方式，详情见[Image Filtering](https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html)

| -- | cv.func | 说明 |
| -- | -- | -- |
| 卷积 | ```filter2D``` | -- |
| 方盒滤波 | ```boxFilter``` | 取kernel的和(不归一化)或者均值(归一化) |
| 均值滤波 | ```blur``` | 取kernel的均值 |
| 中值滤波 | ```medianBlur``` | 取kernel的中位数 |
| 双边滤波 | ```bilateralFilter``` | 图像边缘信息；空间距离高斯函数*灰度距离高斯函数 |
| 高斯滤波 | ```GaussianBlur``` | kernel转换成高斯分布；sigma越大、图像越平滑(模糊) |
| Sobel算子 | ```Sobel``` | 图像边缘信息；一阶求导  |
| Scharr算子 | ```Scharr``` | 与Sobel类似、一阶求导；kernel系数不同，更灵敏 |
| 拉普拉斯算子 | ```Laplacian``` | 图像边缘信息；二阶求导，注意0可能是saddle point |
| 腐蚀 | ```erode``` | -- |

* 需要求导的算法一般默认返回mean(水平f'',垂直f'')；**实际使用时需要手动分开计算水平、垂直**(e.g. dx=1,dy=0)后再add合并结果，否则效果不好
* [Miscellaneous Image Transformations](https://docs.opencv.org/4.x/d7/d1b/group__imgproc__misc.html)
* **漫水填充**：```floodFill```


### 绘图注释
在img上绘图、注释；参考: [Drawing Functions](https://docs.opencv.org/3.4/d6/d6e/group__imgproc__draw.html)  

* arrowedLine()
* circle()
* ellipse()
* line()
* rectangle()
* polylines() 多边形  + fillPoly() 填充多边形
* **putText()** 添加英语字，不支持中文
* ...

```py
demo_mat = cv.line(img_mat,(0,0),(100,900),(0,0,0),2,8,0)
show_img_Window(demo_mat,'myWin',waitTime=0,exitKey='q',ifDestroyAll=True)
```

**注意：**putText()不支持中文，需要使用Pillow + 字体包；Win可至```C:\Windows\Fonts```寻找ttc文件
```py
from PIL import ImageFont,ImageDraw,Image
import numpy as np

font = ImageFont.truetype('demo.ttc',15)
img_pillow = Image.fromarray(img_mat)
draw = ImageDraw.Draw(img_pillow)
draw.text((0,0),'这是一',font=font,fill=(0,0,255))   ## fill=color

img_CN = np.array(img_pillow)   ## back to mat
show_img_Window(img_CN,'myWin',waitTime=0,exitKey='q',ifDestroyAll=True)
```


## Video Basic
### Load
VideoCapture捕获视频，本例中读取10张间隔为1s的摄像机图像，保存于frames中：
```py
frames = []
cam = cv.VideoCapture(0)   ## 0:Camera
while cam.isOpened():                
    ret,frame_mat = cam.read()     ## start loading
    if not ret:
        print('cannot read frame..Break')
        break
    time.sleep(1)  ## second
    frames.append(frame_mat)
    print('show frame:{}'.format(len(frames)) )    ##  plot/window/save...
    if len(frames)>=5:             ## end video
        break

cam.release()
```
* cv.VideoCapture可通过cam.release()释放资源；通过控制每一个frame的持续时间来控制读取速度、不然就是读取每一帧
* cv.VideoCapture(0)使用摄像机，cv.VideoCapture(videoAddr)也使用本地/rtmp流网络视频


### Save
VideoWriter将上例frames保存为视频格式，fourcc提供多媒体文件格式：
```py
fourcc = cv.VideoWriter_fourcc(*'mp4v')
vidWriter = cv.VideoWriter('demo.mp4',fourcc,1,(640,480))  ## file, fourcc, framePerSecond, (dim)[, isColor]
for frame_mat in frames:
    vidWriter.write(frame_mat)

vidWriter.release()
```


### Window
包装到函数中使用Window展示video: 
```py
def show_video_Window(winName,videoAddr,frameIntv=1000,exitKey='q'):  ## frameIntv: ms to show next frame
    cv.namedWindow(winName,cv.WINDOW_NORMAL)
    cam = cv.VideoCapture(videoAddr)     ## 0: camera
    while cam.isOpened():
        ret,frame_mat = cam.read()
        if not ret:
            print('cannot read frame..Break')
            break
        video_exit_key = show_img_Window(frame_mat,winName,waitTime=frameIntv,exitKey=exitKey,ifDestroyAll=False)
        if video_exit_key& 0xFF ==ord(exitKey):
            print('end..')
            break
    cam.release()
    cv.destroyAllWindows()

## show_video_Window('videoWin',0,frameIntv=1000,exitKey='q')
```
只能通过exitKey关闭window


## Event
键盘/鼠标事件与响应的callback: 
```py
def mouse_callback(event,x,y,flags,userdata):  ## MouseEventNO.,x,y,KeyPressFlagsNO.,otherinputData
    print(event,x,y,flags,userdata)        ## e.g. 0,756,166,0,demo userdata  -- 0-EVENT_MOUSEMOVE & 
    
cv.namedWindow('myWin',cv.WINDOW_NORMAL)        ## Step1: new window
cv.setMouseCallback('myWin',mouse_callback,'demo userdata') ## Step2: set callback
show_img_Window(img_mat,'myWin',waitTime=0,exitKey='q')      ## Step3: open img in window
```
* event/flag code 参考：[MouseEventTypes 与 MouseEventFlags](https://docs.opencv.org/4.x/d0/d90/group__highgui__window__flags.html)
* **建议waitKey(0)**，必须搭配imshow

## TrackBar
createTrackbar创建bar，getTrackbarPos、setTrackbarPos获取/设置当前bar的值: 
```py
def bar_callback(value):
    pass

cv.namedWindow('myWin',cv.WINDOW_NORMAL)              ## Step1: new window
cv.createTrackbar('barA','myWin',0,255,bar_callback)  ## Step2: new bar
while True:
    try:
        valA = cv.getTrackbarPos('barA','myWin')      ## opt: get current bar val
        show_img_Window(img_mat-valA,'myWin',waitTime=1,exitKey='q',ifDestroyAll=False)   ## Step3: open img in window
    except:
        break  
```
* **必须waitKey(>0),是为更新频率**；必须搭配imshow


## 色彩空间
* HSV/HSL: Hue-色相(逆时针依次：0红~120绿~240蓝), Saturation-饱和度, Value-明度(0%黑~100%白)/Lightness亮度   
* HWB: Hue, Whiteness, Blackness  
* YUV: 颜色Subsamping编码方式，考虑人类的感知度，允许降低色度的带宽；示例: 4:4:0 = 横向4列中取4列、纵向4行中取1行 (0视为1)
* OPENCV: [Color Space Conversions](https://docs.opencv.org/4.8.0/d8/d01/group__imgproc__color__conversions.html)

```py
img_cvt = cv.cvtColor(img_mat,cv.COLOR_BGR2GRAY)
```

## 目标检测
* ```pip install opencv-contrib-python```安装额外模块；有时版本问题有坑，推荐opencv与contrib都 4.5.4.58
* 详情见：[cascade_classifier Training](https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html) & [cascade_classifier](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)   
* ```pip show opencv-python```找到site-packages，进入其中cv2/data/文件夹；可以找到 **haarcascades_*.XML** 文件
* 只接受灰度图
```py

## train
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.train(faces_lst,id_lst) ### [face_areaA_img1_mat,face_areaB_img1_mat,...]  [id1,id1,...]
recognizer.write('xx.xml')

id_lst, confidence_lst = recognizer.predict(img_mat)

## detect
for x,y,w,h in cv.CascadeClassifier('xx.xml').detectMultiScale(img_mat):
    pass
```

## 参考 
官网：https://opencv.org/    
install：https://opencv.org/get-started/    
Mouse Events in OpenCV: https://pythongeeks.org/mouse-events-in-opencv/    
YUV知乎解说: https://zhuanlan.zhihu.com/p/85620611   
色彩空间 知乎: https://zhuanlan.zhihu.com/p/67930839     
Colors Tutorial：https://www.w3schools.com/colors/colors_hsl.asp       



