
此教程是为了理解 Jeecg-库存管理网站 进行的学习，业务只需普通的 HTTP 单次请求

如果希望制作 Chatbot（会话/即时交互），建立连接--多次交互--断开，即需要搭建 Socket 长连接（TCP/IP），建议使用 [Socket.IO](https://socket.io/zh-CN/docs/v4/) 


## 工具

* [IntelliJ IDEA Ultimate](https://www.jetbrains.com/idea/download/other.html) 中通过 [Maven](https://maven.apache.org/) 管理包：.pom文件
    - 本地安装Maven后: IDEA中File--Settings--搜索maven--设置home/cfg/repo等信息
    - 随后可以创建Maven项目，[尝试一下IT码徒](https://www.itmatu.com/1529.html)，[公司会提供正版IDEA](https://www.idejihuo.com/)


* Mysql 数据库运行后，可以用 Navicat 可视化管理其中的 table

* [Postman](https://www.postman.com/) 测试 server API


## 概念

* MVC
```
       Model   处理数据逻辑----JavaBean
  Controller   对请求选择合适的Model和View----Servlet (url)
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



## 教程导航

* Tips
    - 右键目录，选择生成class/servlet/..
    - 右键 或 Alt+Insert 自动生成类的 Getter/Setter 等代码
    - 右键--Project Structure--Facets--点击项目--点击标红目录进行自动创建
    - 非java代码都放在resources文件夹中

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


### [黑马Spring教程](https://www.bilibili.com/video/BV1rt4y1u7q5) + [SSM教程](https://www.bilibili.com/video/BV1Fi4y1S7ix)

* 为什么要用 [Bean](https://blog.csdn.net/yuxiangdeming/article/details/122876550)？[IoC、DI、AOP 以降低对象间耦合度](./JavaWeb/6.png)

* [Spring-AOP 配置方法](./JavaWeb/10.png),[AOP工作流程](./JavaWeb/11.png),[AOP切入点表达式（支持通配符）](./JavaWeb/12.png)，[Spring AOP 五大通知类型](https://www.cnblogs.com/chuijingjing/p/9806651.html)

* 记得引入xml-header部分的xmlns、xsi，以及pom中相关依赖

* 通过BeanFactory配置/创建/管理Beans，步骤
    1. 简单创建一个Maven项目后，配置 [spring-context](https://central.sonatype.com/artifact/org.springframework/spring-context)
    2. 创建 UserService 接口
    3. UserServiceImpl 是 UserService 的实现类（可配置为Bean）
    4. IDEA 右键目录 New 一个 XML Configuration File，[配置](./JavaWeb/7.png) ```<bean id="userService" class="xx.xx.impl.UserServiceImpl">...</bean>```
    5. 如果某Bean中还需要引用另一个Bean，[例如](https://blog.csdn.net/weixin_42214698/article/details/122781230) ，
        - 则```...```处增加： ```<property name="bean2" ref="bean2"></property>```
        - 或```autowire="byName"```：实现类中设定```setBean2(Bean2 bean2)```方法，寻找容器中```name/id=bean2```者，自动注入
        - 或```autowire="byType"```：寻找容器中类型为Bean2类型者，若有重复则会报错，e.g.当Bean2接口对应两个Impl实现类，配置成两个Bean
    6. 如果是有参构造，例如```class XImpl```的构造方法```public XImpl(String argname){}```，则```...```处增加： ```<constructor-arg name="argname" value="123"></constructor-arg>```
    7. 总结：ref="BeanXxx"， value=String/int/boolean， 如果需要注入的是ref/value的List，则 
    ```
    <property name="xxx">
    <list>
        <value>aaa</value> 
        <value>bbb</value> 
    </list>
    </property>
    ```

```java
// 创建工厂对象
DefaultListableBeanFactory beanFactory = new DefaultListableBeanFactory();
// 读取xml
XmlBeanDefinitionReader reader = new XmlBeanDefinitionReader(beanFactory);
reader.loadBeanDefinitions("beans.xml");
// 根据id获取Bean实例对象 -- 首次调用getBean()时才将被调用的Beans实例化、初始化
UserService userService = (UserService) beanFactory.getBean("serv1");
```

* ApplicationContext (Spring容器) 中封装了BeanFactory，并且扩展了功能API（监听、国际化等），[getBean方法](./JavaWeb/8.png)
```java
// 创建容器 -- 此时就将Beans实例化、初始化
ApplicationContext applicationContext = new ClassPathXmlApplicationContext("beans.xml");
UserService userService = (UserService) applicationContext.getBean("serv1");   // bean xml的优先顺序：(name1,name2)>id>class
```

* 设定test/dev环境
    - 希望使用大标签```<beans profile="dev">....bean1234....</beans>```内的Beans
    - 则main方法中 ```System.setProperty("spring.profiles.active","dev")```


* 有时项目过大，可以吧Beans分开写进不同的xml中，然后```<import resource="classpath:aa.xml"></import>```至相关```<beans>```大标签中

* 许多外部包提供非自定义的Beans，JDBC组件库Druid示例如下；[Mybatis-SqlSessionFactory](https://mybatis.net.cn/getting-started.html)同理，其InputStream可设置为静态BeanFactory
```java
// main函数中，Druid的正常用法
DruidDataSource dataSource = new DruidDataSource();
dataSource.setUrl("jdbc:mysql://xxx:port/xxx");
dataSource.set....

// <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
// dataSource.setXxx等改为在 <property> 标签中设置（如果是构造对象时就需要的参数，使用<constructor-arg>，例如返回Connection的DriveManager.getConnection方法）
// xml中进行以上设置后，main改为：
ApplicationContext applicationContext = new ClassPathXmlApplicationContext("beans.xml");
Object dataSource = applicationContext.getBean("dataSource");
```


* [以上xml配置可以通过@注解进行替代](./JavaWeb/9.png)
```java
// xml中  <context:component-scan base-package="com.proj"/>
@Component("beanName") //get时byName，不填则需byType
public class UserServiceImpl implements UserService {...}
```


* [SpringMVC的使用](https://cloud.tencent.com/developer/article/1711650)类似Servlet：导入spring-webmvc + servlet坐标，beans config配置同上文Spring，[初始化DispathcerServlet](./JavaWeb/13.png)，随后即可使用（建议遵循[RESTful风格](./JavaWeb/14.png)），[Postman测试5种类型参数的传递](https://www.bilibili.com/video/BV1Fi4y1S7ix?p=50)、[Postman测试json格式参数的传递（@RequestBody）](https://www.bilibili.com/video/BV1Fi4y1S7ix?p=50)
```java
@Controller
public class UserController{
    @RequestMapping(value="/users/{}",method=RequestMethod.DELETE)      // 访问/users/1 意味着输入形参id=1
    @ResponseBody                                                       // 设置响应内容为当前返回值，无需解析（建议返回json格式）
    public String delete(@PathVariabla Integer id){                     //  /users/1?name=aa&age=bb可提供name、age两个形参
        return "{'val':'ok'}"                                           // 
    }

    @RequestMapping("/users")                                            // /users?name=aa&age=22可提供name、age两个形参
    @ResponseBody                                                      
    public String test(@RequestParam("name") String userName,int age){  // 形参名一致可直接输入，但不一致则用RequestParam绑定关系
        return "{'val':'ok'}"                                            // 也可直接接收POJO对象 User{name='aa',age='22'} 
    }                                                                   // String[] 直接接收数组 v.s. @RequestParam List<String> 给集合对象赋值
}
```

* [SSM = Spring + SpringMVC + MyBatis 概览](./JavaWeb/15.png)

* SpringBoot进一步简化了SpringMVC，并且整合了Tomcat
    1. IDEA 勾选 Spring Initializr---web---Spring web 初始化SpringBoot项目，只需留下pom文件和src文件夹
    2. New Controller，@RestController
    3. [application.properties/.yaml](https://docs.spring.io/spring-boot/how-to/properties-and-configuration.html)

```java
// .yaml中  lesson:abc
@RestController
@RestMapping("/ab")
public class AbController{
    @Value("${lesson}")         //从.yaml中获取lesson取值
    private String lesson;

    @GetMapping("/{id}")
    public String test(@PathVariabla Integer id){
        System.out.println(lesson);    
        return "ok";
    }
}
```


* [MyBatisPlus 进一步简化了MyBatis，使用步骤](https://baomidou.com/getting-started/)
    1. 生成一个SpringBoot项目：IDEA 勾选 Spring Initializr---web---Spring web，---SQL---MyBatis Framework，---SQL---MySQL Driver
    2. application.yml 配置数据源
    3. 定义数据层接口映射配置（教程所例的**BaseMapper接口**提供了基本CRUD操作接口）

```java
@Mapper
public interface UserDao{
    @Select("select * from user where id=#{id}")
    public User getById(Long id);
}
```





