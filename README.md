
## 本项目是优化数据汇总平台以及常用小工具
- 背景：统计优化数据和小工具应用

#### 正式环境信息

- 域名：`http://47.91.164.93:9009/`
- 后台信息：请咨询相关人员
- 服务器地址：47.91.164.93  ， 请找运维人员加入跳板机
- 项目目录：/application/sub_view/sub_view
- 项目使用：Flask 编写

### 数据库信息
- 数据库配置信息 `/application/sub_view/sub_view/app/__init__.py`

### 注意事项
- 定时任务配置在入口文件中
- 已申请部署自助发布权限
- 区分生产环境配置文件



### 项目使用Nginx+Uwsgi 部署
- uwsgi --ini uwsgi.ini  //后台运行启动 
- uwsgi  uwsgi.ini --deamonize //后台运行启动   
- uwsgi --stop uwsgi.pid  //停止服务   
- uwsgi --reload uwsgi.pid  //可以无缝重启服务 



 