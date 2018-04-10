






uwsgi --ini uwsgiconfig.ini  
  
uwsgi  uwsgiconfig.ini --deamonize //后台运行启动  
  
uwsgi --stop uwsgi.pid  //停止服务  
  
uwsgi --reload uwsgi.pid  //可以无缝重启服务  