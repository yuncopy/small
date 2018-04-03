-启动
/application/python-3.6.5/bin/gunicorn -w 4 -b 0.0.0.0:9008 runweb:app -p gunicorn.pid -D

-D  守护进程
-p  进程ID储存到文件

-重新启动
kill -HUP `cat gunicorn.pid`

-关闭
kill `cat gunicorn.pid`
