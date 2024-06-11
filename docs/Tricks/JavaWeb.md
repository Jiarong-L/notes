

## 工具

* [IntelliJ IDEA Ultimate](https://www.jetbrains.com/idea/download/other.html) 中通过 [Maven](https://maven.apache.org/) 管理包：.pom文件
    - 本地安装Maven后: IDEA中File--Settings--搜索maven--设置home/cfg/repo等信息
    - 随后可以创建Maven项目，[尝试一下，公司会提供正版IDEA](https://www.idejihuo.com/)


* Mysql 数据库运行后，可以用 Navicat 可视化管理其中的 table

* [Postman](https://www.postman.com/) 测试 server API


## 概念

* MVC
```
       Model   处理数据逻辑----JavaBean
  Controller   对请求选择合适的Model和View----Servlet
       View    用于数据展示、与用户交互----前端
```

* SSM框架-三层架构
```
SpringMVC   表现层       Controller+View 处理用户界面和交互逻辑
   Spring   业务逻辑层    Model  应用的核心框架，管理对象及其生命周期
  MyBatis   持久层       与数据库进行交互，增删改查
```

* [Dao层、Entity层、Service层、Servlet层、Utils层](https://blog.csdn.net/Restarting2019/article/details/122296373)

* [POJO、DTO、DAO、PO、BO、VO、QO、ENTITY](https://blog.csdn.net/qq_40610003/article/details/109007539)

* [Token、Cookie for Session](https://blog.csdn.net/weixin_52376041/article/details/134309318) 

* 为什么要用 Bean？[IoC、DI、AOP 以降低耦合度](./JavaWeb/6.png)



## 教程导航

* Tips
    - 右键目录，选择生成class/servlet/..
    - 右键 或 Alt+Insert 自动生成类的 Getter/Setter 等代码
    - 右键--Project Structure--Facets--点击项目--点击标红目录进行自动创建

### [黑马程序员JavaWeb基础教程](https://www.bilibili.com/video/BV1Qf4y1T7Hx/)

基础JavaEE，有助于了解概念和技术发展

* [JDBC API (mysql-connector-java)](https://www.runoob.com/w3cnote/jdbc-use-guide.html) 是 java 与 MySQL 交互的接口，进一步可使用 Druid 连接池分配程序与数据库间的 connection

* [MyBatis](https://mybatis.net.cn/getting-started.html) 是一款持久层框架，简化了JDBC操作：将配置放在config中，SQL语句放在mapper中


```
mybatis-config.xml |  mapper resource="UserMapper.xml"
UserMapper.xml     |  <select id="selectAll" ...>SQL</select>
User.java          |  public class User {...}
UserMapper.java    |  public interface UserMapper {List<User> selectAll();}
Demo.java          |  UserMapper mm = session.getMapper(UserMapper.class);
                   |  List<User> uu = mm.selectAll();
```

可用注解代替xml，此外，[MyBatis 提供SQL 语句构建器](https://mybatis.net.cn/statement-builders.html)
```
public interface UserMapper{
    @Select("select * from tbl where age = #{age}")
    List<User> selectByAge(int age);
}
```


* [Tomcat部署web项目](https://blog.csdn.net/bbj12345678/article/details/105886282): 作为容器创建Servlet对象
    - 打包Maven项目后部署在Tomcat中，注意：pom.xml 添加 ``` <packaging>war</packaging> ```，否则默认打包 ```.jar```
    - 也可以集成至Idea：运行标志边上(下拉栏)--Edit Configuration--Run/Debug Configuration--ADD符号--Tomcat Server--Local--Configure--Server Tab--设置Home--Deployment Tab--ADD符号--xxx.war--OK--Apply--运行标志
    - [也可以以Maven插件的方式集成至当前项目](https://blog.csdn.net/m0_52861000/article/details/128305384)：pom.xml 添加相关依赖--Run Maven--tomcat:run
    - 也可内置于springboot中


* A Servlet is a small Java program that runs within a Web server, 由 [JavaEE](https://docs.oracle.com/javaee/7/api/) 提供规范接口
    - Servlet在容器中运行，其生命周期由容器管理：第一次访问--加载/实例化--init()--处理请求--destroy()
    - Servlet（接口）--- GenericServlet（抽象实现类）--- HttpServlet（封装HTTP协议后的实现类）

```
@WebServlet(urlPatterns = {"/login"})
public class Demo implements Servlet{
    public void init(ServletConfig config) throws ServletException{...}
    public void service(ServletRequest req, ServletResponse res){

        String name = req.getParameter("name");

        res.setHeader("content-type","text/html;charset=utf-8");
        res.getWriter().write('<h1>Hello</h1>');
        }
    public void destroy(){...}
    public ServletConfig getServletConfig(){...}
    public String getServletInfo(){...}
    ...
}
```
开发者的自定义Servlet一般 ```extends HttpServlet```: [doGet()/doPost()](./JavaWeb/1.png)，二者通用：
```
Map<String,String[]> map= httpReq.getParameterMap()
           String[] val = httpReq.getParameterValues(String name)
             String par = httpReq.getParameter(String name)
```
[转发getRequestDispatcher v.s. 重定向sendRedirect 的实现；以及路径中何时需要加虚拟目录](./JavaWeb/2.png)

Response 非纯文本情况下不能 ```res.getWriter().write```，需要先将其转变为字节流: 
```java
FileInputStream fis = new FileInputStream('a.png');
ServletOutputStream os = httpRES.getOutputStream();
// 从File流拷贝至Servlet流
byte[] buff = new byte[1024];
int len = 0;
while ( (len = fis.read(buff))!= -1 ){
    os.write(buff,0,len);
}
fis.close();
```

* [JSP](./JavaWeb/3.png) = HTML + Java，[被访问时由Tomcat将其转换为servlet](https://www.runoob.com/jsp/jsp-life-cycle.html)，用于简化开发：java代码和HTML在一个文件中，response时不用write太多东西
    - 代码难以阅读，已逐渐被 Servlet + html + AJAX 取代
    - [EL 表达式的域](./JavaWeb/4.png)
    - [JSTL取代JSP页面上的Java代码](./JavaWeb/5.png)


### [黑马Spring教程](https://www.bilibili.com/video/BV1rt4y1u7q5)



















### [黑马SpringBoot教程](https://www.bilibili.com/video/BV1rt4y1u7q5)









