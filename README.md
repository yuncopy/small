
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
- 注意定时任务配置
- 已部署自助发布平台



### 项目使用Nginx+Uwsgi 部署
- uwsgi --ini uwsgi.ini  //后台运行启动 
- uwsgi  uwsgi.ini --deamonize //后台运行启动   
- uwsgi --stop uwsgi.pid  //停止服务   
- uwsgi --reload uwsgi.pid  //可以无缝重启服务 


### 指定加载配置
- uwsgi --ini uwsgi.ini:dev
```
[uwsgi]
# This will load the app1 section below
ini = :app1
# This will load the defaults.ini file
ini = defaults.ini
# This will load the app2 section from the defaults.ini file!
ini = :app2

[pro]
plugin = rack

[dev]
plugin = php

```

 