# install.packages("shiny")
# install.packages("leaflet")
## API：https://www.rdocumentation.org/packages/leaflet/versions/2.2.2
## API：https://leafletjs.com/reference.html   --- Map --- Event
## 各数据类型的属性，自行help()

library(shiny)
library(leaflet)

# UI部分
ui <- fluidPage(
  titlePanel("点击地图获取经纬度信息"),
  leafletOutput("map"),
  textOutput("coords")
)

# 服务器逻辑
server <- function(input, output, session) {
  
  # 创建地图
  output$map <- renderLeaflet({
    leaflet() %>%     # 1. leaflet 窗口
      addTiles() %>%  # 2. 添加OpenStreetMap的瓦片
      setView(lng = 0, lat = 0, zoom = 2)  # 3. 设置初始视图
  })
  
  # 响应点击事件
  observeEvent(input$map_click, {   ## eventExpr -- reactive value
    click <- input$map_click          ## 1. 将点击Leaflet Map后返回的数据存储在 map_click 字段 
    output$coords <- renderText({     ## 2. 字段中包含经纬度
      paste("经度: ", round(click$lng, 5), " 纬度: ", round(click$lat, 5))
    })
  })
}

# 启动Shiny应用
shinyApp(ui, server)